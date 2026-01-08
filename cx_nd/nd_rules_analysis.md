# ND Rules Analysis - order_problem checkpoint

Analysis of delivery_ids where ND-related rules evaluated to non-null values in the `order_problem` checkpoint over the last 7 days.

## Rules Analyzed
- `NDCostMLV2HighThresholdExperimentRule`
- `HighNDScoreforHighRises`

## Results

| ACTIVE_DATE | NDCostMLV2HighThreshold | HighNDScoreforHighRises | Either Rule (Union) |
|-------------|-------------------------|-------------------------|---------------------|
| 2025-12-26  | 1,279                   | 250                     | 1,529               |
| 2025-12-27  | 1,541                   | 305                     | 1,846               |
| 2025-12-28  | 1,636                   | 289                     | 1,925               |
| 2025-12-29  | 1,590                   | 292                     | 1,882               |
| 2025-12-30  | 1,508                   | 284                     | 1,792               |
| 2025-12-31  | 1,565                   | 272                     | 1,837               |
| 2026-01-01  | 1,517                   | 269                     | 1,786               |
| 2026-01-02  | 1,562                   | 304                     | 1,866               |

**Totals (7 days):**
- NDCostMLV2HighThreshold: ~12,198
- HighNDScoreforHighRises: ~2,265
- **Either Rule (no double-count): ~14,463**

## Key Insight
The overlap between the two rules is minimal (~0), meaning they capture mostly distinct delivery populations.

## Total Checkpoint Volume

Total distinct delivery_ids going through `order_problem` checkpoint daily:

| ACTIVE_DATE | TOTAL_DELIVERIES |
|-------------|------------------|
| 2025-12-26  | 388,019          |
| 2025-12-27  | 396,071          |
| 2025-12-28  | 400,067          |
| 2025-12-29  | 390,429          |
| 2025-12-30  | 392,602          |
| 2025-12-31  | 427,416          |
| 2026-01-01  | 500,402          |
| 2026-01-02  | 412,431          |

**~390k-500k deliveries/day** go through the checkpoint. The rules analyzed hit ~1,800/day, representing roughly **0.4-0.5%** of total volume.

## Query

```sql
SELECT
    DATE(iguazu_sent_at) as active_date,
    COUNT(DISTINCT CASE WHEN JSON_EXTRACT_PATH_TEXT(RULE_RESULTS, 'NDCostMLV2HighThresholdExperimentRule.output') IS NOT NULL THEN entity_id END) as ndcost_mlv2_high_threshold,
    COUNT(DISTINCT CASE WHEN JSON_EXTRACT_PATH_TEXT(RULE_RESULTS, 'HighNDScoreforHighRises.output') IS NOT NULL THEN entity_id END) as high_nd_score_high_rises,
    COUNT(DISTINCT CASE WHEN
        JSON_EXTRACT_PATH_TEXT(RULE_RESULTS, 'NDCostMLV2HighThresholdExperimentRule.output') IS NOT NULL
        OR JSON_EXTRACT_PATH_TEXT(RULE_RESULTS, 'HighNDScoreforHighRises.output') IS NOT NULL
    THEN entity_id END) as either_rule
FROM iguazu.server_events_production.risk_checkpoint_evaluation_event_ice
WHERE iguazu_sent_at >= DATEADD(day, -7, CURRENT_DATE())
AND checkpoint = 'order_problem'
GROUP BY 1
ORDER BY 1
```

### Total Checkpoint Volume Query

```sql
SELECT
    DATE(iguazu_sent_at) as active_date,
    COUNT(DISTINCT entity_id) as total_deliveries
FROM iguazu.server_events_production.risk_checkpoint_evaluation_event_ice
WHERE iguazu_sent_at >= DATEADD(day, -7, CURRENT_DATE())
AND checkpoint = 'order_problem'
GROUP BY 1
ORDER BY 1
```
