# V1 Time Fraud Model - Fraud Sample

## Purpose
Sample of 100 deliveries adjudicated as fraud by the v1 time fraud model to serve as positive examples in the golden dataset.

## Definition
Cases where:
1. **ML model threshold triggered** (at least one):
   - `DeliveryCrossesTimeFraudMLModelThresholdOutsidePreconditionsRule`
   - `DeliveryCrossesTimeFraudMLModelThresholdRule`

2. **AND action taken** (at least one):
   - `BlockPayForTimeModeLabelToActionRule`
   - `BlockPayForTopUpLabelToActionRule`
   - `FlagEntityForTopUpLabelToActionRule`
   - `FlagEntityForTimeModeLabelToActionRule`

Query results have been sent for golden review at https://docs.google.com/spreadsheets/d/1iLg5kikKGU0edBroapDXNunoxK32epSjtY4csMTZlSM/edit?gid=0#gid=0

## Query
```sql
SELECT DISTINCT
    entity_id AS delivery_id,
    JSON_EXTRACT_PATH_TEXT(FACT_RESULTS, 'dasher_id.output.value') AS dasher_id,
    DATE(iguazu_sent_at) AS iguazu_date,
    ROUND((JSON_EXTRACT_PATH_TEXT(FACT_RESULTS, 'actual_pickup_time_in_epoch_seconds.output')::NUMBER
         - JSON_EXTRACT_PATH_TEXT(FACT_RESULTS, 'dx_facing_eta_pickup_in_epoch_seconds.output')::NUMBER) / 60.0, 2) AS pickup_lateness,
    ROUND((JSON_EXTRACT_PATH_TEXT(FACT_RESULTS, 'actual_dropoff_time_in_epoch_seconds.output')::NUMBER
         - JSON_EXTRACT_PATH_TEXT(FACT_RESULTS, 'dx_facing_eta_dropoff_in_epoch_seconds.output')::NUMBER) / 60.0, 2) AS dropoff_lateness,
    ROUND((JSON_EXTRACT_PATH_TEXT(FACT_RESULTS, 'actual_pickup_time_in_epoch_seconds.output')::NUMBER
         - JSON_EXTRACT_PATH_TEXT(FACT_RESULTS, 'dx_facing_eta_pickup_in_epoch_seconds.output')::NUMBER
         + JSON_EXTRACT_PATH_TEXT(FACT_RESULTS, 'actual_dropoff_time_in_epoch_seconds.output')::NUMBER
         - JSON_EXTRACT_PATH_TEXT(FACT_RESULTS, 'dx_facing_eta_dropoff_in_epoch_seconds.output')::NUMBER) / 60.0, 2) AS total_lateness
FROM iguazu.server_events_production.risk_checkpoint_evaluation_event_ice
WHERE checkpoint = 'dx_dropoff_delivery'
  AND iguazu_sent_at >= DATEADD(day, -2, CURRENT_DATE())
  AND (
    JSON_EXTRACT_PATH_TEXT(rule_results, 'DeliveryCrossesTimeFraudMLModelThresholdOutsidePreconditionsRule.output') IS NOT NULL
    OR JSON_EXTRACT_PATH_TEXT(rule_results, 'DeliveryCrossesTimeFraudMLModelThresholdRule.output') IS NOT NULL
  )
  AND (
    JSON_EXTRACT_PATH_TEXT(rule_results, 'BlockPayForTimeModeLabelToActionRule.output') IS NOT NULL
    OR JSON_EXTRACT_PATH_TEXT(rule_results, 'BlockPayForTopUpLabelToActionRule.output') IS NOT NULL
    OR JSON_EXTRACT_PATH_TEXT(rule_results, 'FlagEntityForTopUpLabelToActionRule.output') IS NOT NULL
    OR JSON_EXTRACT_PATH_TEXT(rule_results, 'FlagEntityForTimeModeLabelToActionRule.output') IS NOT NULL
  )
ORDER BY RANDOM()
LIMIT 100;
```

## Lateness Calculation
Lateness values are calculated using checkpoint facts (in minutes):
- **pickup_lateness** = `(actual_pickup_time_in_epoch_seconds - dx_facing_eta_pickup_in_epoch_seconds) / 60`
- **dropoff_lateness** = `(actual_dropoff_time_in_epoch_seconds - dx_facing_eta_dropoff_in_epoch_seconds) / 60`
- **total_lateness** = `pickup_lateness + dropoff_lateness`

Positive values = late, negative values = early.

## Output
- **File:** `v1_fraud_sample.csv`
- **Count:** 100 deliveries
- **Date range:** Last 2 days (2026-01-10 to 2026-01-12)

## Sample Preview
| DELIVERY_ID | DASHER_ID | IGUAZU_DATE | PICKUP_LATENESS | DROPOFF_LATENESS | TOTAL_LATENESS |
|-------------|-----------|-------------|-----------------|------------------|----------------|
| 189437704884 | 32119799 | 2026-01-10 | -1.23 | 11.25 | 10.02 |
| 271588294906 | 58574964 | 2026-01-11 | 21.83 | -2.75 | 19.08 |
| 268642984074 | 35117986 | 2026-01-10 | 2.53 | 7.47 | 10.00 |
| 247796947897 | 56763196 | 2026-01-11 | 16.22 | -1.58 | 14.63 |
| 311900352795 | 51668473 | 2026-01-11 | 9.48 | -1.67 | 7.82 |
