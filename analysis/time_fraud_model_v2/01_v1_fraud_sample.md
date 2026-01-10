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

Query has been sent for golden review at https://docs.google.com/spreadsheets/d/1iLg5kikKGU0edBroapDXNunoxK32epSjtY4csMTZlSM/edit?gid=0#gid=0

## Query
```sql
SELECT DISTINCT
    entity_id AS delivery_id,
    JSON_EXTRACT_PATH_TEXT(FACT_RESULTS, 'dasher_id.output.value') AS dasher_id,
    DATE(iguazu_sent_at) AS iguazu_date
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

## Output
- **File:** `v1_fraud_sample.csv`
- **Count:** 100 deliveries
- **Date range:** Last 2 days (2026-01-08 to 2026-01-09)

## Sample Preview
| DELIVERY_ID | DASHER_ID | IGUAZU_DATE |
|-------------|-----------|-------------|
| 276470497415 | 11911262 | 2026-01-08 |
| 318488051028 | 26124532 | 2026-01-09 |
| 345358925004 | 46917363 | 2026-01-09 |
| 238532267221 | 16709378 | 2026-01-08 |
| 265396260385 | 32220546 | 2026-01-08 |
