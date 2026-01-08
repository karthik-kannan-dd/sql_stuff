# Worst Dashers by Median Total Lateness

> **Analysis Date:** January 7, 2026
> **Data Source:** `edw.opex.fact_dx_fraud_pc_rolling_scores`
> **Scope:** Dashers with 20+ TBPM deliveries in last 28 days and median total lateness >10 min
> **Lateness Metric:** Total Lateness = Pickup Lateness + Dropoff Lateness

---

## Summary

These dashers have the highest **median total lateness** - meaning half of their deliveries are at least this late. This identifies dashers with consistently egregious lateness patterns.

**25 dashers** have median total lateness >10 minutes with tier classifications.

---

## Top 25 Dashers by Median Total Lateness

| Dasher ID | Deliveries | Med Pickup | Med Dropoff | Med Total | % >10min | % >15min | % >30min | Tier |
|-----------|------------|------------|-------------|-----------|----------|----------|----------|------|
| **65023622** | 87 | -2.72 min | 102.32 min | **99.52 min** | 95.4% | 94.3% | 92.0% | **Tier 1** |
| **8026806** | 110 | -2.17 min | 101.46 min | **99.39 min** | 93.6% | 93.6% | 93.6% | **Tier 1** |
| **57134452** | 120 | -1.50 min | 96.12 min | **98.38 min** | 91.7% | 89.2% | 84.2% | **Tier 1** |
| **36963906** | 40 | -2.89 min | 99.78 min | **96.24 min** | 75.0% | 67.5% | 65.0% | **Tier 1** |
| **67706906** | 22 | 5.05 min | 46.74 min | **88.77 min** | 90.9% | 90.9% | 86.4% | **Tier 1** |
| **67482992** | 22 | 2.61 min | 69.76 min | **88.40 min** | 90.9% | 90.9% | 77.3% | **Tier 1** |
| **67754477** | 25 | 4.68 min | 51.18 min | **79.60 min** | 96.0% | 96.0% | 80.0% | **Tier 1** |
| **67482904** | 21 | 1.70 min | 42.35 min | **60.85 min** | 76.2% | 76.2% | 76.2% | **Tier 1** |
| **67086725** | 39 | 4.18 min | 45.83 min | **57.38 min** | 84.6% | 82.1% | 71.8% | **Tier 1** |
| **67433810** | 28 | 1.58 min | 45.54 min | **53.91 min** | 92.9% | 92.9% | 78.6% | **Tier 1** |
| **67086507** | 31 | 1.25 min | 48.78 min | **49.15 min** | 83.9% | 71.0% | 64.5% | **Tier 1** |
| **66919671** | 58 | **38.02 min** | -2.66 min | **36.63 min** | 74.1% | 70.7% | 58.6% | **Tier 1** |
| **53090914** | 62 | **46.95 min** | -11.48 min | **36.24 min** | 61.3% | 59.7% | 56.5% | **Tier 1** |
| **35560585** | 54 | 12.36 min | 16.79 min | **33.73 min** | 87.0% | 75.9% | 59.3% | **Tier 1** |
| **67268112** | 31 | **31.07 min** | -2.83 min | **28.45 min** | 87.1% | 80.6% | 45.2% | Tier 2 |
| **55114061** | 23 | 22.95 min | 1.27 min | **26.88 min** | 82.6% | 65.2% | 47.8% | Tier 2 |
| **29043870** | 20 | 13.30 min | 8.09 min | **26.17 min** | 75.0% | 75.0% | 35.0% | Tier 2 |
| **32402341** | 40 | 26.18 min | -0.55 min | **24.43 min** | 80.0% | 72.5% | 45.0% | Tier 2 |
| **32871454** | 125 | 18.62 min | 4.65 min | **23.95 min** | 80.8% | 70.4% | 31.2% | Tier 2 |
| **66405525** | 20 | 10.08 min | 7.63 min | **23.64 min** | 85.0% | 70.0% | 25.0% | Tier 2 |
| **47600977** | 25 | **40.28 min** | -18.18 min | **23.25 min** | 68.0% | 68.0% | 36.0% | Tier 2 |
| **29034610** | 111 | 19.00 min | -0.47 min | **22.48 min** | 68.5% | 62.2% | 35.1% | Tier 2 |
| **32584641** | 27 | 12.35 min | 2.00 min | **22.42 min** | 81.5% | 63.0% | 25.9% | Tier 2 |
| **1675750** | 41 | 27.22 min | -3.82 min | **21.93 min** | 70.7% | 65.9% | 31.7% | Tier 2 |
| **66394460** | 32 | 7.78 min | 9.65 min | **21.84 min** | 87.5% | 62.5% | 46.9% | Tier 2 |

---

## Tier Classification (New Thresholds)

| Tier | Definition | Dashers in Top 25 |
|------|------------|-------------------|
| **Tier 1 (Egregious)** | >50% deliveries >30 min total late | 14 dashers |
| **Tier 2 (Moderate)** | >50% deliveries >15 min (excl Tier 1) | 11 dashers |
| **Tier 3 (Mild)** | >50% deliveries >10 min (excl Tier 1-2) | 0 in top 25 |

---

## Two Lateness Patterns

| Pattern | Description | Example Dashers |
|---------|-------------|-----------------|
| **Dropoff-Heavy** | Early/on-time pickup, very late dropoff | 65023622, 8026806, 57134452, 67482992 |
| **Pickup-Heavy** | Very late pickup, on-time or early dropoff | 66919671, 53090914, 67268112, 47600977 |

### Dropoff-Heavy Pattern (Most Common)
- Median pickup: -3 to +5 min (early or on-time)
- Median dropoff: 40-100 min late
- Example: Dasher 8026806 with 99.39 min median total lateness

### Pickup-Heavy Pattern (Hidden Abuse)
- Median pickup: 30-50 min late
- Median dropoff: -18 to +5 min (early or on-time)
- Example: Dasher 53090914 with 46.95 min median pickup, -11.48 min dropoff

---

## SQL Queries

### Find Dashers with Median Total Lateness >10 min (with Tier Classification)

```sql
WITH dasher_stats AS (
    SELECT
        dasher_id,
        COUNT(*) AS total_deliveries,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EST_ACT_PICKUP_ERR_MINUTES) AS median_pickup_min,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EST_ACT_DROPOFF_ERR_MINUTES) AS median_dropoff_min,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES) AS median_total_late_min,
        SUM(CASE WHEN (EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES) > 30 THEN 1 ELSE 0 END) AS count_over_30min,
        SUM(CASE WHEN (EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES) > 15 THEN 1 ELSE 0 END) AS count_over_15min,
        SUM(CASE WHEN (EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES) > 10 THEN 1 ELSE 0 END) AS count_over_10min
    FROM edw.opex.fact_dx_fraud_pc_rolling_scores
    WHERE timebased_pay_model NOT IN ('order mode')
      AND assignment_created_at >= dateadd(dd,-28,current_date())
      AND DELIVERY_DEVIATION_SCORE IS NOT NULL
    GROUP BY dasher_id
    HAVING COUNT(*) >= 20
)
SELECT
    dasher_id,
    total_deliveries,
    ROUND(median_pickup_min, 2) AS median_pickup_min,
    ROUND(median_dropoff_min, 2) AS median_dropoff_min,
    ROUND(median_total_late_min, 2) AS median_total_late_min,
    ROUND(100.0 * count_over_10min / total_deliveries, 1) AS pct_over_10min,
    ROUND(100.0 * count_over_15min / total_deliveries, 1) AS pct_over_15min,
    ROUND(100.0 * count_over_30min / total_deliveries, 1) AS pct_over_30min,
    CASE
        WHEN 100.0 * count_over_30min / total_deliveries > 50 THEN 'Tier 1 (Egregious)'
        WHEN 100.0 * count_over_15min / total_deliveries > 50 THEN 'Tier 2 (Moderate)'
        WHEN 100.0 * count_over_10min / total_deliveries > 50 THEN 'Tier 3 (Mild)'
        ELSE 'Normal'
    END AS tier
FROM dasher_stats
WHERE median_total_late_min > 10
ORDER BY median_total_late_min DESC
LIMIT 25;
```

### Get Sample Deliveries for Specific Dashers

```sql
SELECT
    dasher_id,
    delivery_id,
    assignment_created_at::date AS delivery_date,
    ROUND(EST_ACT_PICKUP_ERR_MINUTES, 2) AS pickup_late_min,
    ROUND(EST_ACT_DROPOFF_ERR_MINUTES, 2) AS dropoff_late_min,
    ROUND(EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES, 2) AS total_late_min
FROM edw.opex.fact_dx_fraud_pc_rolling_scores
WHERE dasher_id IN (65023622, 8026806, 57134452, 66919671, 53090914)
  AND timebased_pay_model NOT IN ('order mode')
  AND assignment_created_at >= dateadd(dd,-28,current_date())
QUALIFY ROW_NUMBER() OVER (PARTITION BY dasher_id ORDER BY assignment_created_at DESC) <= 10
ORDER BY dasher_id, assignment_created_at DESC;
```

---

*Analysis conducted January 7, 2026*
