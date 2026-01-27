-- Example SQL features for risk analysis (generic SQL)

-- Customer-level spend stats
SELECT
  customer_id,
  COUNT(*) AS txn_count,
  SUM(amount) AS total_spend,
  AVG(amount) AS avg_amount,
  MAX(amount) AS max_amount
FROM transactions
GROUP BY customer_id;

-- Daily velocity (transactions per customer per day)
SELECT
  customer_id,
  CAST(transaction_date AS DATE) AS txn_day,
  COUNT(*) AS txns_that_day,
  SUM(amount) AS spend_that_day
FROM transactions
GROUP BY customer_id, CAST(transaction_date AS DATE);
