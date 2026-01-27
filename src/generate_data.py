import numpy as np
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

def generate_customers(n=2000, seed=42):
    np.random.seed(seed)
    Faker.seed(seed)

    customers = []
    for i in range(1, n + 1):
        created_days_ago = np.random.randint(30, 900)
        signup_date = (datetime.today() - timedelta(days=int(created_days_ago))).date()

        customers.append({
            "customer_id": i,
            "name": fake.name(),
            "gender": np.random.choice(["F", "M"], p=[0.52, 0.48]),
            "age": int(np.clip(np.random.normal(34, 10), 18, 70)),
            "city": fake.city(),
            "state": fake.state_abbr(),
            "signup_date": signup_date,
        })

    return pd.DataFrame(customers)

def generate_transactions(customers_df, avg_txn_per_customer=8, seed=42):
    np.random.seed(seed)

    categories = ["Grocery", "Electronics", "Fashion", "Travel", "Dining", "Pharmacy", "Fuel"]
    regions = ["West", "Midwest", "South", "Northeast"]

    txns = []
    txn_id = 1

    for cid in customers_df["customer_id"].tolist():
        txn_count = max(0, int(np.random.poisson(avg_txn_per_customer)))

        for _ in range(txn_count):
            days_back = np.random.randint(0, 365)
            txn_date = (datetime.today() - timedelta(days=int(days_back))).date()

            amount = float(np.round(np.random.lognormal(mean=3.3, sigma=0.6), 2))
            category = np.random.choice(categories)
            region = np.random.choice(regions)

            if np.random.rand() < 0.01:
                amount *= np.random.randint(10, 30)

            txns.append({
                "transaction_id": txn_id,
                "customer_id": cid,
                "transaction_date": txn_date,
                "amount": amount,
                "category": category,
                "region": region
            })
            txn_id += 1

    return pd.DataFrame(txns)

def main():
    customers = generate_customers()
    transactions = generate_transactions(customers)

    customers.to_csv("data/raw/customers.csv", index=False)
    transactions.to_csv("data/raw/transactions.csv", index=False)

    print("✅ Synthetic customer and transaction data generated")

if __name__ == "__main__":
    main()
