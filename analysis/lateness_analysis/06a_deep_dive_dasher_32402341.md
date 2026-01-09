# Dasher 32402341: Store Wait Time Validation

> **Analysis Date:** January 8, 2026
> **Data Source:** `edw.opex.fact_dx_fraud_pc_rolling_scores`, `edw.opex.fact_dx_fraud_assignment`, `proddb.public.dimension_deliveries`
> **Data Period:** December 10, 2025 - January 7, 2026 (28 days)
> **Subject:** Dasher 32402341 (Tier 2 Moderate Lateness)

---

## Context

Dasher 32402341 was identified in the Tier 2 moderate lateness analysis with:
- 40 deliveries
- Median pickup lateness: 26.18 min
- 72.5% of deliveries >15 min total late
- 45.0% of deliveries >30 min total late

The dasher claimed that stores in their area are always slow due to high traffic/busy conditions.

---

## Methodology

To validate this claim:
1. Selected 20 of the dasher's late deliveries (>15 min total late)
2. Identified the store for each delivery
3. Found the dasher's **actual store arrival time** for each delivery
4. Looked back 10, 30, and 60 minutes from that arrival time
5. Compared the dasher's wait time to other dashers who arrived at the same store during those windows

---

## Late Deliveries Analyzed

| Delivery ID | Store | Store Arrival Time | Dx Wait (min) |
|-------------|-------|-------------------|---------------|
| 271677428733 | Taco Heart (E Passyunk Ave) | 2025-12-20 15:13 | 49.6 |
| 274830094825 | Unit Su Vege | 2025-12-12 16:40 | 45.0 |
| 322657778797 | Dunkin' (300230) | 2025-12-12 18:46 | 48.6 |
| 260095048830 | IHOP (5501) | 2025-12-11 23:18 | 46.1 |
| 226674637347 | Chipotle - 1214 | 2025-12-18 21:37 | 43.4 |
| 227341054514 | Philip's Steaks | 2025-12-20 11:40 | 43.5 |
| 358224072139 | McDonald's (Broad & Diamond) | 2025-12-12 23:15 | 47.1 |
| 234124984842 | McDonald's (Columbus Blvd) | 2025-12-20 16:26 | 36.7 |
| 285956375966 | Popeyes (11086) | 2025-12-20 19:55 | 39.0 |
| 286566778075 | Taco man LLC | 2025-12-19 01:05 | 37.1 |
| 199731820589 | Castor & Aramingo | 2025-12-11 18:41 | 39.3 |
| 164464074005 | Chipotle (Walnut Street) | 2025-12-12 15:51 | 31.1 |
| 285724292641 | Raising Cane's - C0824 | 2025-12-13 00:14 | 45.0 |
| 163885800503 | Grays Ferry | 2025-12-20 10:54 | 31.8 |
| 221340567814 | Sunrise Breakfast | 2025-12-20 12:37 | 32.8 |
| 224794474223 | Taco Bell - 024243 | 2025-12-11 20:27 | 36.3 |
| 277131190215 | McDonald's (24th & Oregon) | 2025-12-18 23:03 | 30.7 |
| 345419926176 | Dunkin' (348933) | 2025-12-20 14:15 | 35.6 |
| 330863539712 | Petes Famous Pizza | 2025-12-20 18:54 | 34.9 |
| 318583334037 | Nifty Fifty's (Fishtown) | 2025-12-19 02:59 | 27.8 |

---

## Comparison: Dasher vs Other Dashers at Same Stores

Wait times for other dashers who arrived at the same store within 60 minutes **before** this dasher's arrival:

| Store | Dx Wait | n (10m) | Avg (10m) | n (30m) | Avg (30m) | n (60m) | Avg (60m) | Gap |
|-------|---------|---------|-----------|---------|-----------|---------|-----------|-----|
| Taco Heart | 49.6 | 3 | 3.7 | 3 | 3.7 | 8 | 4.1 | **+45.5** |
| McDonald's (Broad) | 47.1 | 2 | 8.8 | 6 | 7.2 | 9 | 7.7 | **+39.4** |
| IHOP | 46.1 | 0 | - | 1 | 3.0 | 1 | 3.0 | **+43.1** |
| Raising Cane's | 45.0 | 2 | 17.0 | 9 | 17.2 | 21 | 16.5 | **+28.5** |
| Chipotle - 1214 | 43.4 | 0 | - | 0 | - | 2 | 4.6 | **+38.8** |
| Castor & Aramingo | 39.3 | 0 | - | 0 | - | 1 | 5.6 | **+33.7** |
| Popeyes | 39.0 | 0 | - | 1 | 4.0 | 2 | 4.0 | **+35.0** |
| McDonald's (Columbus) | 36.7 | 0 | - | 0 | - | 2 | 18.2 | **+18.5** |
| Taco Bell | 36.3 | 0 | - | 0 | - | 2 | 1.8 | **+34.5** |
| Dunkin' (348933) | 35.6 | 0 | - | 0 | - | 1 | 1.3 | **+34.3** |
| Petes Famous Pizza | 34.9 | 1 | 3.4 | 1 | 3.4 | 1 | 3.4 | **+31.5** |
| Chipotle (Walnut) | 31.1 | 0 | - | 1 | 3.7 | 1 | 3.7 | **+27.4** |
| McDonald's (Oregon) | 30.7 | 1 | 1.9 | 2 | 4.2 | 4 | 3.3 | **+27.4** |
| Nifty Fifty's | 27.8 | 2 | 3.7 | 6 | 4.6 | 7 | 4.5 | **+23.3** |

---

## Key Findings

1. **Consistent gap across all stores**: For all 14 stores with comparison data, this dasher's wait time exceeded other dashers' average by 18-46 minutes.

2. **Stores are not universally slow**: Other dashers at the same stores around the same time had average wait times of 1-18 minutes, while this dasher waited 28-50 minutes.

3. **Even at slower stores, gap persists**: Raising Cane's had 21 other dashers arrive in the hour before this dasher, averaging 16.5 min wait (suggesting it may be a slower store). Yet this dasher waited 45 min - still 2.7x longer than peers.

4. **Pattern is dasher-specific**: The claim that "stores in the area are always busy" is not supported by the data. Other dashers servicing the same stores at similar times did not experience comparable delays.

---

## SQL Queries

### Get Late Deliveries with Store Arrival Times

```sql
SELECT
    pc.delivery_id,
    dd.store_id,
    dd.store_name,
    fa.DASHER_CONFIRMED_STORE_ARRIVAL_TIME AS store_arrival_time,
    fa.MX_ARRIVAL_TO_PICKUP_SECOND / 60.0 AS this_dasher_wait_min,
    pc.EST_ACT_PICKUP_ERR_MINUTES AS pickup_late_min
FROM edw.opex.fact_dx_fraud_pc_rolling_scores pc
JOIN proddb.public.dimension_deliveries dd ON pc.delivery_id = dd.delivery_id
JOIN edw.opex.fact_dx_fraud_assignment fa ON pc.delivery_id = fa.delivery_id AND fa.is_last_assignment = TRUE
WHERE pc.dasher_id = 32402341
  AND pc.timebased_pay_model NOT IN ('order mode')
  AND pc.assignment_created_at >= '2025-12-10'::date
  AND pc.assignment_created_at <= '2026-01-07'::date
  AND pc.DELIVERY_DEVIATION_SCORE IS NOT NULL
  AND (pc.EST_ACT_PICKUP_ERR_MINUTES + pc.EST_ACT_DROPOFF_ERR_MINUTES) > 15
  AND fa.DASHER_CONFIRMED_STORE_ARRIVAL_TIME IS NOT NULL
ORDER BY (pc.EST_ACT_PICKUP_ERR_MINUTES + pc.EST_ACT_DROPOFF_ERR_MINUTES) DESC
LIMIT 20;
```

### Compare Wait Times with Other Dashers (Lookback from Store Arrival)

```sql
WITH late_deliveries AS (
    SELECT
        pc.delivery_id,
        dd.store_id,
        dd.store_name,
        fa.DASHER_CONFIRMED_STORE_ARRIVAL_TIME AS store_arrival_time,
        fa.MX_ARRIVAL_TO_PICKUP_SECOND / 60.0 AS this_dasher_wait_min
    FROM edw.opex.fact_dx_fraud_pc_rolling_scores pc
    JOIN proddb.public.dimension_deliveries dd ON pc.delivery_id = dd.delivery_id
    JOIN edw.opex.fact_dx_fraud_assignment fa ON pc.delivery_id = fa.delivery_id AND fa.is_last_assignment = TRUE
    WHERE pc.dasher_id = 32402341
      AND pc.timebased_pay_model NOT IN ('order mode')
      AND pc.assignment_created_at >= '2025-12-10'::date
      AND pc.assignment_created_at <= '2026-01-07'::date
      AND pc.DELIVERY_DEVIATION_SCORE IS NOT NULL
      AND (pc.EST_ACT_PICKUP_ERR_MINUTES + pc.EST_ACT_DROPOFF_ERR_MINUTES) > 15
      AND fa.DASHER_CONFIRMED_STORE_ARRIVAL_TIME IS NOT NULL
    ORDER BY (pc.EST_ACT_PICKUP_ERR_MINUTES + pc.EST_ACT_DROPOFF_ERR_MINUTES) DESC
    LIMIT 20
),
other_dashers AS (
    SELECT
        ld.delivery_id AS target_delivery_id,
        ld.store_id,
        ld.store_name,
        ld.store_arrival_time AS target_arrival_time,
        ld.this_dasher_wait_min,
        fa2.MX_ARRIVAL_TO_PICKUP_SECOND / 60.0 AS other_wait_min,
        DATEDIFF('minute', fa2.DASHER_CONFIRMED_STORE_ARRIVAL_TIME, ld.store_arrival_time) AS minutes_before
    FROM late_deliveries ld
    JOIN proddb.public.dimension_deliveries dd2
        ON dd2.store_id = ld.store_id
        AND dd2.active_date >= '2025-12-10'::date
        AND dd2.active_date <= '2026-01-07'::date
    JOIN edw.opex.fact_dx_fraud_assignment fa2
        ON fa2.delivery_id = dd2.delivery_id
        AND fa2.is_last_assignment = TRUE
    WHERE fa2.dasher_id != 32402341
      AND fa2.DASHER_CONFIRMED_STORE_ARRIVAL_TIME IS NOT NULL
      AND fa2.MX_ARRIVAL_TO_PICKUP_SECOND IS NOT NULL
      AND fa2.DASHER_CONFIRMED_STORE_ARRIVAL_TIME >= DATEADD('minute', -60, ld.store_arrival_time)
      AND fa2.DASHER_CONFIRMED_STORE_ARRIVAL_TIME <= ld.store_arrival_time
)
SELECT
    SUBSTR(store_name, 1, 20) AS store,
    ROUND(this_dasher_wait_min, 1) AS dx_wait,
    COUNT(CASE WHEN minutes_before <= 10 THEN 1 END) AS n_10m,
    ROUND(AVG(CASE WHEN minutes_before <= 10 THEN other_wait_min END), 1) AS avg_10m,
    COUNT(CASE WHEN minutes_before <= 30 THEN 1 END) AS n_30m,
    ROUND(AVG(CASE WHEN minutes_before <= 30 THEN other_wait_min END), 1) AS avg_30m,
    COUNT(*) AS n_60m,
    ROUND(AVG(other_wait_min), 1) AS avg_60m
FROM other_dashers
GROUP BY target_delivery_id, store_name, this_dasher_wait_min
ORDER BY this_dasher_wait_min DESC;
```

---

*Analysis conducted January 8, 2026*
