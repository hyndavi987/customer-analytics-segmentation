import pandas as pd
import numpy as np

def compute_customer_kpis(customers: pd.DataFrame, txns: pd.DataFrame) -> pd.DataFrame:
    txns = txns.copy()
    customers = customers.copy()

    txns["transaction_date"] = pd.to_datetime(txns["transaction_date"])
    customers["signup_date"] = pd.to_datetime(customers["signup_date"])

    # reference date = latest txn date + 1 day
    ref_date = txns["transaction_date"].max() + pd.Timedelta(days=1)

    agg = txns.groupby("customer_id").agg(
        last_purchase=("transaction_date", "max"),
        first_purchase=("transaction_date", "min"),
        txn_count=("transaction_id", "count"),
        total_spend=("amount", "sum"),
        avg_txn_value=("amount", "mean"),
    ).reset_index()

    agg["recency_days"] = (ref_date - agg["last_purchase"]).dt.days
    agg["tenure_days"] = (ref_date - agg["first_purchase"]).dt.days.clip(lower=1)

    agg["purchase_frequency_per_month"] = agg["txn_count"] / (agg["tenure_days"] / 30.0)
    agg["clv_simple"] = agg["avg_txn_value"] * agg["purchase_frequency_per_month"] * 12

    # churn heuristic: no purchase in last 90 days
    agg["is_churn_risk"] = (agg["recency_days"] > 90).astype(int)

    out = customers.merge(agg, on="customer_id", how="left")

    # customers with no transactions
    out.fillna({
        "txn_count": 0,
        "total_spend": 0.0,
        "avg_txn_value": 0.0,
        "recency_days": 9999,
        "tenure_days": 0,
        "purchase_frequency_per_month": 0.0,
        "clv_simple": 0.0,
        "is_churn_risk": 1
    }, inplace=True)

    return out

def rfm_segmentation(kpis: pd.DataFrame) -> pd.DataFrame:
    df = kpis.copy()
    has_txn = df["txn_count"] > 0
    scored = df.loc[has_txn].copy()

    # R: lower recency is better -> give higher score to recent buyers
    scored["R"] = pd.qcut(scored["recency_days"], 5, labels=[5, 4, 3, 2, 1]).astype(int)
    scored["F"] = pd.qcut(scored["txn_count"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    scored["M"] = pd.qcut(scored["total_spend"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)

    def label(row):
        if row["R"] >= 4 and row["F"] >= 4 and row["M"] >= 4:
            return "VIP"
        if row["R"] >= 4 and row["F"] >= 3:
            return "Loyal"
        if row["R"] <= 2 and row["F"] >= 3:
            return "At-Risk Loyal"
        if row["R"] <= 2 and row["F"] <= 2:
            return "Churned/Cold"
        if row["F"] <= 2 and row["M"] >= 4:
            return "Big Spender (Rare)"
        return "Regular"

    scored["segment"] = scored.apply(label, axis=1)

    df["segment"] = "No Purchases"
    df.loc[has_txn, "segment"] = scored["segment"].values
    return df

def monthly_retention(txns: pd.DataFrame) -> pd.DataFrame:
    df = txns.copy()
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    df["year_month"] = df["transaction_date"].dt.to_period("M").astype(str)

    active = df.groupby("year_month")["customer_id"].nunique().reset_index()
    active.rename(columns={"customer_id": "active_customers"}, inplace=True)

    # retained = customers active this month AND next month
    df_sorted = df.sort_values(["customer_id", "transaction_date"])
    current = df_sorted[["customer_id", "year_month"]].drop_duplicates()

    df_sorted["next_month"] = (df_sorted["transaction_date"] + pd.offsets.MonthBegin(1)).dt.to_period("M").astype(str)
    nxt = df_sorted[["customer_id", "next_month"]].drop_duplicates().rename(columns={"next_month": "year_month"})

    retained = current.merge(nxt, on=["customer_id", "year_month"], how="inner")
    retained_month = retained.groupby("year_month")["customer_id"].nunique().reset_index()
    retained_month.rename(columns={"customer_id": "retained_next_month"}, inplace=True)

    out = active.merge(retained_month, on="year_month", how="left").fillna(0)
    out["retention_rate_next_month"] = np.where(
        out["active_customers"] > 0,
        out["retained_next_month"] / out["active_customers"],
        0
    )
    return out

def main():
    customers = pd.read_csv("data/raw/customers.csv")
    txns = pd.read_csv("data/raw/transactions.csv")

    kpis = compute_customer_kpis(customers, txns)
    kpis = rfm_segmentation(kpis)
    retention = monthly_retention(txns)

    # outputs for Power BI
    kpis.to_csv("data/processed/customer_kpis_segments.csv", index=False)
    retention.to_csv("data/processed/monthly_retention.csv", index=False)

    print("✅ Exported:")
    print(" - data/processed/customer_kpis_segments.csv")
    print(" - data/processed/monthly_retention.csv")

if __name__ == "__main__":
    main()
