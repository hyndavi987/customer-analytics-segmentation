# Customer Analytics & Segmentation (SQL, Python, Power BI)

## Overview
End-to-end customer analytics project that analyzes customer demographics and transactions to identify behavior patterns,
churn indicators, and high-value customer segments. Outputs are Power BI-ready tables for dashboards.

## What this project does
- Generates synthetic customer + transaction data (safe for public GitHub)
- Builds customer KPIs: recency, frequency, total spend, average transaction value, simple CLV, churn-risk flag
- Segments customers using RFM scoring (VIP, Loyal, At-Risk, Churned/Cold, etc.)
- Produces monthly retention metrics for trend reporting

## Tech Stack
- Python: Pandas, NumPy
- Power BI: dashboard layer (connect to processed outputs)

## How to run (local)
```bash
pip install -r requirements.txt
python src/generate_data.py
python src/customer_segmentation.py


---

## Project 2: Financial Transaction Risk Analysis (SQL, Python)

### Overview
This project analyzes financial transaction data to identify anomalies and potential fraud patterns.
It applies rule-based risk indicators and scoring to flag suspicious transactions and high-risk customers
for further investigation.

### What this project does
- Analyzes transaction behavior by customer, date, category, and amount
- Detects anomalies using customer-level spending patterns and velocity checks
- Applies explainable, rule-based risk scoring
- Produces investigation-ready outputs for risk and fraud teams

### Outputs
> Note: Full datasets are generated locally. Sample outputs are included in the `samples/` folder for demonstration.
Generated in `risk/outputs/`:
- `transaction_risk_flags.csv` – transaction-level risk indicators
- `customer_risk_summary.csv` – aggregated customer risk profiles
- `top_suspicious_transactions.csv` – prioritized investigation list

### How to run (local)
```bash
pip install -r requirements.txt
python src/generate_data.py
python risk/src/risk_scoring.py
