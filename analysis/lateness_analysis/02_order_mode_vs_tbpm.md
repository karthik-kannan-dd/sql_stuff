# Order Mode vs Time-Based Pay Model (TBPM) Lateness Comparison

> **Analysis Date:** January 8, 2026
> **Data Source:** `edw.opex.fact_dx_fraud_pc_rolling_scores`
> **Data Period:** December 10, 2025 - January 7, 2026 (28 days)
> **Lateness Metric:** Total Lateness = Pickup Lateness + Dropoff Lateness

---

## Summary

Comparing delivery lateness between **Order Mode** (traditional per-order pay) and **Time-Based Pay Models** (TBPM).

---

## Pay Model Distribution

| Pay Model | Delivery Count |
|-----------|----------------|
| Order Mode | 128,308,752 |
| CA Topup | 20,816,734 |
| TimeMode | 11,003,795 |
| NYC Topup | 3,436,297 |
| ONT Topup | 2,436,816 |
| BC Topup | 1,536,509 |
| SEA Topup | 379,616 |
| **Total TBPM** | **39,609,767** |

---

## Overall Comparison: Order Mode vs TBPM

| Metric | Order Mode | Time-Based (TBPM) | Difference |
|--------|------------|-------------------|------------|
| Deliveries | 128.3M | 39.6M | - |
| Avg Pickup Late | 1.16 min | 1.38 min | +0.22 min |
| Avg Dropoff Late | -2.97 min | -2.63 min | +0.34 min |
| **Avg Total Late** | **-1.82 min** | **-1.25 min** | +0.57 min |
| **Median Total Late** | **-1.97 min** | **-1.42 min** | +0.55 min |
| % >10 min late | 4.34% | 4.32% | -0.02% |
| % >15 min late | 1.83% | 1.74% | -0.09% |
| % >30 min late | 0.28% | 0.26% | -0.02% |

### Key Findings

1. **Both groups are generally early** - Negative lateness values indicate deliveries are completed ahead of estimates
2. **Order Mode is slightly more early** - Median -1.97 min vs -1.42 min for TBPM
3. **Late delivery rates are nearly identical** - ~4.3% over 10 min, ~1.8% over 15 min, ~0.3% over 30 min
4. **Differences are minimal** - Only ~0.5 min difference in median lateness

---

## Breakdown by Individual Pay Model

| Pay Model | Deliveries | Avg Pickup | Avg Dropoff | Avg Total | Median Total | % >10min | % >15min | % >30min |
|-----------|------------|------------|-------------|-----------|--------------|----------|----------|----------|
| order mode | 128.3M | 1.16 min | -2.97 min | -1.82 min | -1.97 min | 4.34% | 1.83% | 0.28% |
| CA Topup | 20.8M | 1.04 min | -2.99 min | -1.95 min | -1.97 min | **2.79%** | **1.05%** | **0.14%** |
| TimeMode | 11.0M | 1.86 min | -2.27 min | -0.40 min | -0.70 min | 6.25% | 2.58% | 0.38% |
| NYC Topup | 3.4M | 1.36 min | -2.63 min | -1.27 min | -1.10 min | 5.48% | 2.24% | 0.36% |
| ONT Topup | 2.4M | 2.06 min | -1.77 min | 0.29 min | -0.28 min | 6.39% | 2.86% | **0.56%** |
| BC Topup | 1.5M | 1.33 min | -1.93 min | -0.60 min | -0.82 min | 4.32% | 1.79% | 0.32% |
| SEA Topup | 380K | 2.11 min | -1.75 min | 0.36 min | **+0.02 min** | **8.69%** | **3.56%** | 0.51% |

### Individual Model Findings

1. **CA Topup (Best Performer)**
   - Lowest late rates across all thresholds
   - 2.79% >10min (vs 4.34% for order mode)
   - Same median lateness as order mode (-1.97 min)

2. **SEA Topup (Worst Performer)**
   - Only model with positive median lateness (+0.02 min)
   - Highest % >10min (8.69%) and % >15min (3.56%)
   - 2x the late rate of order mode

3. **ONT Topup (Second Worst)**
   - Highest % >30min (0.56%)
   - 6.39% >10min late
   - Positive average total lateness (+0.29 min)

4. **TimeMode (Middle of Pack)**
   - 6.25% >10min late
   - Median -0.70 min (still early, but less than order mode)

5. **NYC Topup & BC Topup (Moderate)**
   - Similar performance to order mode
   - BC Topup nearly matches order mode rates

---

## SQL Queries

### Pay Model Distribution

```sql
SELECT
    timebased_pay_model,
    COUNT(*) AS delivery_count
FROM edw.opex.fact_dx_fraud_pc_rolling_scores
WHERE assignment_created_at >= '2025-12-10'::date
  AND assignment_created_at <= '2026-01-07'::date
  AND DELIVERY_DEVIATION_SCORE IS NOT NULL
GROUP BY timebased_pay_model
ORDER BY delivery_count DESC;
```

### Order Mode vs TBPM Comparison

```sql
SELECT
    CASE
        WHEN timebased_pay_model = 'order mode' THEN 'Order Mode'
        ELSE 'Time-Based (TBPM)'
    END AS pay_model_group,
    COUNT(*) AS delivery_count,
    ROUND(AVG(EST_ACT_PICKUP_ERR_MINUTES), 2) AS avg_pickup_late,
    ROUND(AVG(EST_ACT_DROPOFF_ERR_MINUTES), 2) AS avg_dropoff_late,
    ROUND(AVG(EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES), 2) AS avg_total_late,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES), 2) AS median_total_late,
    ROUND(100.0 * SUM(CASE WHEN (EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES) > 10 THEN 1 ELSE 0 END) / COUNT(*), 2) AS pct_over_10min,
    ROUND(100.0 * SUM(CASE WHEN (EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES) > 15 THEN 1 ELSE 0 END) / COUNT(*), 2) AS pct_over_15min,
    ROUND(100.0 * SUM(CASE WHEN (EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES) > 30 THEN 1 ELSE 0 END) / COUNT(*), 2) AS pct_over_30min
FROM edw.opex.fact_dx_fraud_pc_rolling_scores
WHERE assignment_created_at >= '2025-12-10'::date
  AND assignment_created_at <= '2026-01-07'::date
  AND DELIVERY_DEVIATION_SCORE IS NOT NULL
GROUP BY 1
ORDER BY 1;
```

### Individual Pay Model Breakdown

```sql
SELECT
    timebased_pay_model AS pay_model,
    COUNT(*) AS delivery_count,
    ROUND(AVG(EST_ACT_PICKUP_ERR_MINUTES), 2) AS avg_pickup_late,
    ROUND(AVG(EST_ACT_DROPOFF_ERR_MINUTES), 2) AS avg_dropoff_late,
    ROUND(AVG(EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES), 2) AS avg_total_late,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES), 2) AS median_total_late,
    ROUND(100.0 * SUM(CASE WHEN (EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES) > 10 THEN 1 ELSE 0 END) / COUNT(*), 2) AS pct_over_10min,
    ROUND(100.0 * SUM(CASE WHEN (EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES) > 15 THEN 1 ELSE 0 END) / COUNT(*), 2) AS pct_over_15min,
    ROUND(100.0 * SUM(CASE WHEN (EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES) > 30 THEN 1 ELSE 0 END) / COUNT(*), 2) AS pct_over_30min
FROM edw.opex.fact_dx_fraud_pc_rolling_scores
WHERE assignment_created_at >= '2025-12-10'::date
  AND assignment_created_at <= '2026-01-07'::date
  AND DELIVERY_DEVIATION_SCORE IS NOT NULL
GROUP BY timebased_pay_model
ORDER BY delivery_count DESC;
```

---

*Analysis conducted January 8, 2026*
