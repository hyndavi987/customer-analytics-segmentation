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

- ## Power BI Dashboard

This Power BI dashboard visualizes insights generated from the customer analytics pipeline in this repository.  
Processed CSV outputs from Python are directly consumed in Power BI to enable business-focused reporting.

### Dashboard Highlights
- **Customer Segment Distribution** – Breakdown of customers across segments such as Regular, VIP, Loyal, At-Risk, and Churned.
- **Average Customer Lifetime Value (CLV)** – Overall average CLV across the customer base.
- **Total Customers KPI** – Total number of unique customers analyzed.
- **Monthly Active Customers Trend** – Engagement trend over time.
- **Revenue by Customer Segment** – Comparison of revenue contribution across customer segments.

### Dashboard Preview

![Customer Analytics Dashboard](assets/powerbi_customer_analytics_dashboard.png)

![Customer Segment Distribution](assets/powerbi_customer_segment_distribution.png)


## How to run (local)
```bash
pip install -r requirements.txt
python src/generate_data.py
python src/customer_segmentation.py


---

---

## Project 2: Financial Transaction Risk Analysis (SQL, Python)

### Overview
This project analyzes financial transaction data to identify anomalous activity and potential fraud patterns using explainable, rule-based risk indicators.

### What this project does
- Analyzes transaction behavior by customer, category, amount, and time
- Flags high-risk transactions using velocity checks and statistical thresholds
- Aggregates customer-level risk profiles for investigation
- Produces investigation-ready outputs for risk and fraud teams

### Tech Stack
- Python (Pandas, NumPy)
- SQL-style aggregations
- Power BI (dashboard layer)

### Outputs
Generated in `risk/outputs/`:
- `transaction_risk_flags.csv` – transaction-level risk indicators
- `customer_risk_summary.csv` – customer risk profiles
- `top_suspicious_transactions.csv` – prioritized investigation list

### Dashboard Outputs (Power BI)

**Risk Analysis Overview**  
![Risk Overview](assets/project2_risk_analysis/risk_dashboard_overview.png)  
_Overview of total transactions vs high-risk transactions._

**High-Risk Transactions by Category**  
![High Risk by Category](assets/project2_risk_analysis/high_risk_transactions_by_category.png)  
_Pharmacy and Grocery show the highest concentration of high-risk transactions._

**Top Suspicious Transactions**  
![Top Suspicious Transactions](assets/project2_risk_analysis/top_suspicious_transactions_table.png)  
_Prioritized list of transactions requiring manual investigation._

### How to run (local)
```bash
pip install -r requirements.txt
python src/generate_data.py
python risk/src/risk_scoring.py
