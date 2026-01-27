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
