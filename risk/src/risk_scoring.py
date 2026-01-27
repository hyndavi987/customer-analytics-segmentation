import pandas as pd
import numpy as np

def load_data(path="data/raw/transactions.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    return df

def add_customer_stats(df: pd.DataFrame) -> pd.DataFrame:
    stats = df.groupby("customer_id")["amount"].agg(["mean", "std", "count"]).reset_index()
    stats.columns = ["customer_id", "cust_amt_mean", "cust_amt_std", "cust_txn_count"]
    out = df.merge(stats, on="customer_id", how="left")
    out["cust_amt_std"] = out["cust_amt_std"].fillna(0)
    return out

def add_velocity_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["day"] = out["transaction_date"].dt.date
    daily = out.groupby(["customer_id", "day"])["transaction_id"].count().reset_index()
    daily.rename(columns={"transaction_id": "txns_that_day"}, inplace=True)
    out = out.merge(daily, on=["customer_id", "day"], how="left")
    return out

def add_flags(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    # z-score anomaly per customer
    out["z_score"] = np.where(
        out["cust_amt_std"] > 0,
        (out["amount"] - out["cust_amt_mean"]) / out["cust_amt_std"],
        0
    )

    out["flag_amount_anomaly"] = (out["z_score"] > 3).astype(int)
    out["flag_high_amount"] = (out["amount"] >= 1000).astype(int)
    out["flag_velocity"] = (out["txns_that_day"] >= 8).astype(int)

    # simple extra: risky categories (customize as needed)
    risky_categories = {"Electronics", "Travel"}
    out["flag_risky_category"] = out["category"].isin(risky_categories).astype(int)

    return out

def add_risk_score(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    # Weighted scoring (simple + explainable)
    out["risk_score"] = (
        out["flag_amount_anomaly"] * 50 +
        out["flag_high_amount"] * 25 +
        out["flag_velocity"] * 15 +
        out["flag_risky_category"] * 10
    )

    out["risk_level"] = pd.cut(
        out["risk_score"],
        bins=[-1, 24, 49, 10**9],
        labels=["Low", "Medium", "High"]
    )
    return out

def customer_risk_summary(scored: pd.DataFrame) -> pd.DataFrame:
    summary = scored.groupby("customer_id").agg(
        total_txns=("transaction_id", "count"),
        total_spend=("amount", "sum"),
        total_risk_score=("risk_score", "sum"),
        max_risk_score=("risk_score", "max"),
        high_risk_txns=("risk_level", lambda x: (x == "High").sum())
    ).reset_index()

    summary["customer_risk_tier"] = pd.cut(
        summary["total_risk_score"],
        bins=[-1, 50, 150, 10**9],
        labels=["Low", "Medium", "High"]
    )
    return summary

def main():
    df = load_data()
    df = add_customer_stats(df)
    df = add_velocity_features(df)
    df = add_flags(df)
    df = add_risk_score(df)

    cust = customer_risk_summary(df)

    # outputs (kept separate from Project 1 outputs)
    df.to_csv("risk/outputs/transaction_risk_flags.csv", index=False)
    cust.to_csv("risk/outputs/customer_risk_summary.csv", index=False)

    # quick investigation list: top 50 suspicious
    top = df.sort_values("risk_score", ascending=False).head(50)
    top.to_csv("risk/outputs/top_suspicious_transactions.csv", index=False)

    print("✅ Exported risk outputs to risk/outputs/")

if __name__ == "__main__":
    main()
