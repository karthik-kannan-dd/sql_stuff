# Dasher Lateness Analysis: L50 Sum Score Deep Dive

> **Analysis Date:** December 30, 2025
> **Data Source:** `edw.opex.fact_dx_fraud_pc_rolling_scores`
> **Scope:** Top 10 dashers by L50 TBPM Sum Score (last 28 days)
> **Lateness Metric:** Total Lateness = Pickup Lateness + Dropoff Lateness

---

## Executive Summary

Analysis of the top 10 dashers ranked by `DELIVERY_DEVIATION_SCORE_SUM_L50_TBPM` reveals a critical insight: **high aggregate scores are predominantly driven by single extreme outlier deliveries rather than consistent lateness patterns**.

Using **Total Lateness** (pickup + dropoff) as the primary metric captures the full picture of time abuse, since TBPM dashers get paid by time and can delay either pickup or dropoff to maximize compensation.

---

## Top 10 Dashers by L50 Sum Score

| Rank | Dasher ID | L50 Sum Score | Max Score | Median Score | Outliers (100+) | Med Pickup | Med Dropoff | Med Total Late | 60+ Total Late |
|------|-----------|---------------|-----------|--------------|-----------------|------------|-------------|----------------|----------------|
| 1 | **58542935** | 1,775.63 | 1,758.37 | 0.39 | 1 | 2.08 min | 1.30 min | 4.11 min | 1 |
| 2 | **43769019** | 1,075.97 | 0.64 | 0.02 | 0 | 0.23 min | -3.37 min | -2.50 min | 0 |
| 3 | **65349905** | 438.88 | 427.70 | 0.21 | 1 | 1.29 min | -0.94 min | 0.15 min | 1 |
| 4 | **32236153** | 327.88 | 324.72 | 0.02 | 1 | 0.63 min | -2.13 min | -2.17 min | 1 |
| 5 | **8026806** | 290.65 | 13.32 | 5.42 | 0 | -2.27 min | 101.08 min | **98.03 min** | **45** |
| 6 | **65023622** | 257.13 | 20.44 | 5.37 | 0 | -2.48 min | 101.26 min | **99.11 min** | **42** |
| 7 | **57134452** | 232.67 | 15.96 | 5.36 | 0 | -1.78 min | 96.76 min | **96.44 min** | **36** |
| 8 | **4118462** | 231.48 | 29.38 | 3.01 | 0 | **41.82 min** | 7.23 min | **49.04 min** | **21** |
| 9 | **23305229** | 231.23 | 223.87 | 0.19 | 1 | 1.04 min | -1.48 min | 0.29 min | 1 |
| 10 | **64252667** | 179.43 | 6.73 | 4.60 | 0 | 1.04 min | 77.39 min | **80.85 min** | **30** |

---

## Classification: Three Distinct Dasher Categories

### Category 1: Outlier-Driven High Scores (4 dashers)

These dashers have high L50 sum scores driven almost entirely by a **single extreme outlier delivery**.

| Dasher ID | L50 Sum | Max Single Score | % of Sum from Max | Pattern |
|-----------|---------|------------------|-------------------|---------|
| 58542935 | 1,775.63 | 1,758.37 | **99.0%** | Single delivery ~19.8 days late |
| 65349905 | 438.88 | 427.70 | **97.5%** | Single extreme outlier |
| 32236153 | 327.88 | 324.72 | **99.0%** | Single extreme outlier |
| 23305229 | 231.23 | 223.87 | **96.8%** | Single extreme outlier |

**Characteristics:**
- Median deviation score near 0 (0.02 - 0.39)
- Only 1 delivery out of 50 with score > 100
- Median total lateness is near 0 or negative (on time!)
- Only 1 delivery out of 50 is 60+ minutes total late
- **Root cause:** Likely data anomalies (unclosed deliveries, system errors)

### Category 2: Consistently Late - Dropoff Heavy (4 dashers)

These dashers exhibit **persistent lateness across all deliveries** with no extreme outliers. They arrive early to pickup but are extremely late to dropoff.

| Dasher ID | L50 Sum | Max Score | Median Score | Med Pickup | Med Dropoff | Med Total | 60+ Total Late |
|-----------|---------|-----------|--------------|------------|-------------|-----------|----------------|
| 8026806 | 290.65 | 13.32 | 5.42 | **-2.27 min** | 101.08 min | **98.03 min** | **45 of 50** |
| 65023622 | 257.13 | 20.44 | 5.37 | **-2.48 min** | 101.26 min | **99.11 min** | **42 of 50** |
| 57134452 | 232.67 | 15.96 | 5.36 | **-1.78 min** | 96.76 min | **96.44 min** | **36 of 50** |
| 64252667 | 179.43 | 6.73 | 4.60 | 1.04 min | 77.39 min | **80.85 min** | **30 of 50** |

**Characteristics:**
- NO extreme outliers (max single score only 6-20)
- Median deviation score 4.6-5.4 (consistently elevated)
- **Early to pickup** (negative pickup lateness) - food is ready, they pick it up
- **Very late to dropoff** (77-101 minutes)
- Median total lateness: **80-99 minutes**
- **Root cause:** Consistent TBPM time abuse pattern

### Category 3: Pickup-Heavy Lateness (1 dasher) - NEW PATTERN

| Dasher ID | L50 Sum | Max Score | Med Pickup | Med Dropoff | Med Total | 60+ Total Late |
|-----------|---------|-----------|------------|-------------|-----------|----------------|
| 4118462 | 231.48 | 29.38 | **41.82 min** | 7.23 min | **49.04 min** | **21 of 50** |

**This dasher shows a different pattern:**
- Very late to **pickup** (~42 min) but relatively on-time to dropoff (~7 min)
- Suggests holding orders at the restaurant level, then delivering promptly

### Category 4: Requires Investigation (1 dasher)

| Dasher ID | L50 Sum | Notes |
|-----------|---------|-------|
| 43769019 | 1,075.97 | Max score only 0.64 but sum is 1,076 - potential data issue |

---

## Recommendations

### 1. Implement Outlier Filtering
When ranking dashers by lateness, exclude or cap extreme single-delivery scores (e.g., scores > 100) to surface consistently late dashers.

### 2. Use Total Lateness as Primary Metric
Use **Total Lateness = Pickup + Dropoff** to capture lateness patterns.

### 3. Flag Data Quality Issues
Deliveries showing 15-28 days lateness are data anomalies that should be excluded.

### 4. Investigate Both Patterns
- **Dropoff-Heavy:** Early pickup, very late dropoff (classic multi-apping)
- **Pickup-Heavy:** Late pickup, normal dropoff (holding at restaurant)

---

## Appendix: SQL Query

```sql
-- L50 Deep Dive with TOTAL LATENESS (pickup + dropoff)
WITH percentile_calc AS (
    SELECT percentile_cont(0.99) within group (order by max_score) AS threshold
    FROM (
        SELECT dasher_id, max(DELIVERY_DEVIATION_SCORE_sum_L50_TBPM) AS max_score
        FROM edw.opex.fact_dx_fraud_pc_rolling_scores
        WHERE timebased_pay_model NOT IN ('order mode')
        AND assignment_created_at >= dateadd(dd,-28,current_date())
        GROUP BY 1
    )
),
top10_dashers AS (
    SELECT dasher_id, DELIVERY_DEVIATION_SCORE_sum_L50_TBPM, assignment_created_at
    FROM edw.opex.fact_dx_fraud_pc_rolling_scores a
    CROSS JOIN percentile_calc b
    WHERE a.timebased_pay_model NOT IN ('order mode')
    AND a.assignment_created_at >= dateadd(dd,-28,current_date())
    AND a.DELIVERY_DEVIATION_SCORE_sum_L50_TBPM > b.threshold
    QUALIFY ROW_NUMBER() over(PARTITION BY a.dasher_id ORDER BY a.assignment_created_at DESC) = 1
    ORDER BY DELIVERY_DEVIATION_SCORE_sum_L50_TBPM DESC
    LIMIT 10
),
l50_deliveries AS (
    SELECT
        a.dasher_id,
        a.DELIVERY_DEVIATION_SCORE_sum_L50_TBPM AS l50_sum_score,
        b.DELIVERY_DEVIATION_SCORE AS deviation_score,
        b.EST_ACT_PICKUP_ERR_MINUTES AS pickup_late_min,
        b.EST_ACT_DROPOFF_ERR_MINUTES AS dropoff_late_min,
        (b.EST_ACT_PICKUP_ERR_MINUTES + b.EST_ACT_DROPOFF_ERR_MINUTES) AS total_late_min,
        row_number() over(PARTITION BY a.dasher_id ORDER BY b.assignment_created_at DESC) AS L50_idx
    FROM top10_dashers a
    LEFT JOIN edw.opex.fact_dx_fraud_pc_rolling_scores b
        ON a.dasher_id = b.dasher_id
        AND b.assignment_created_at < a.assignment_created_at
        AND b.timebased_pay_model NOT IN ('order mode')
    QUALIFY L50_idx <= 50
)
SELECT
    dasher_id,
    ROUND(l50_sum_score, 2) AS l50_sum_score,
    COUNT(*) AS deliveries_in_l50,
    ROUND(MAX(deviation_score), 2) AS max_deviation_score,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY deviation_score), 2) AS median_deviation_score,
    SUM(CASE WHEN deviation_score > 100 THEN 1 ELSE 0 END) AS outliers_100plus,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY pickup_late_min), 2) AS median_pickup_late_min,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY dropoff_late_min), 2) AS median_dropoff_late_min,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY total_late_min), 2) AS median_total_late_min,
    SUM(CASE WHEN total_late_min > 60 THEN 1 ELSE 0 END) AS deliveries_60plus_total_late,
    SUM(CASE WHEN total_late_min > 30 THEN 1 ELSE 0 END) AS deliveries_30plus_total_late
FROM l50_deliveries
GROUP BY dasher_id, l50_sum_score
ORDER BY l50_sum_score DESC;
```

---

*Analysis conducted December 30, 2025*
