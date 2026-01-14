# risk_core_checkpoint_evaluation_shadow_event

**Full Table Name:** `iguazu.server_events_production.RISK_CORE_CHECKPOINT_EVALUATION_SHADOW_EVENT`

**Description:** Realtime log table of all fraud checkpoints running in SHADOW mode. Used to test and validate checkpoint rules before they go live. Similar structure to the production checkpoint table but specifically for shadow evaluations.

## Schema

| Column Name | Data Type | Nullable | Description |
|-------------|-----------|----------|-------------|
| IGUAZU_UUID | VARCHAR | Y | Unique Iguazu identifier |
| IGUAZU_SENT_AT | TIMESTAMP_NTZ(9) | Y | Timestamp when sent to Iguazu |
| IGUAZU_INGEST_TIMESTAMP | TIMESTAMP_NTZ(9) | Y | Timestamp when ingested by Iguazu |
| IGUAZU_CUSTOM_ATTRIBUTES | VARIANT | Y | Custom attributes (JSON) |
| EVALUATION_ID | VARCHAR | Y | Unique identifier for the checkpoint evaluation |
| CHECKPOINT | VARCHAR | Y | Name of the fraud checkpoint being evaluated |
| MODE | VARCHAR | Y | Evaluation mode (use 'SHADOW' for shadow evaluations) |
| SEGMENT_USER_TYPE | VARCHAR | Y | Type of user segment |
| SEGMENT_USER_ID | VARCHAR | Y | User ID within the segment |
| ENTITY_TYPE | VARCHAR | Y | Type of entity being evaluated |
| ENTITY_ID | VARCHAR | Y | ID of the entity being evaluated |
| EXTRA_TRACKING_PROPS | VARCHAR | Y | Additional tracking properties (JSON) |
| FINAL_ACTION | VARCHAR | Y | Final action taken by the checkpoint |
| FINAL_ACTION_DETAILS | VARCHAR | Y | Details about the final action |
| ACTIONS | VARCHAR | Y | List of actions (JSON) |
| LABELS | VARCHAR | Y | Labels applied (JSON) |
| EXEMPTIONS | VARCHAR | Y | Exemptions applied (JSON) |
| BUILTIN_RESULTS | VARCHAR | Y | Results from built-in evaluations (JSON) |
| FACT_RESULTS | VARCHAR | Y | Results from fact evaluations (JSON) |
| RULE_RESULTS | VARCHAR | Y | Results from rule evaluations (JSON) |
| DELIVERY_ID | VARCHAR | Y | Associated delivery ID |
| LINK_ID | VARCHAR | Y | Associated link ID |
| STAGE_CHANGE_ID | VARCHAR | Y | Stage change identifier |
| EVALUATED_AT | TIMESTAMP_NTZ(9) | Y | Timestamp when evaluation occurred |
| EXPERIMENT_OVERRIDES | VARCHAR | Y | Experiment overrides (JSON) |

## Key Columns

- **IGUAZU_SENT_AT** - Primary timestamp column for time-based filtering
- **CHECKPOINT** - The fraud checkpoint name being evaluated
- **MODE** - Filter by 'SHADOW' to get shadow evaluations
- **FACT_RESULTS** - JSON containing all fact outputs
- **RULE_RESULTS** - JSON containing all rule outputs
- **FINAL_ACTION** - The resulting action from the checkpoint evaluation

## Usage Examples

### Accessing Facts and Rules from JSON (Shadow Mode)

```sql
SELECT
    DATE(iguazu_sent_at) AS active_date,
    JSON_EXTRACT_PATH_TEXT(FACT_RESULTS, 'fact_name.output') AS fact_name,
    JSON_EXTRACT_PATH_TEXT(RULE_RESULTS, 'rule_name.output') AS rule_name
FROM iguazu.server_events_production.RISK_CORE_CHECKPOINT_EVALUATION_SHADOW_EVENT
WHERE iguazu_sent_at >= DATEADD(day, -7, CURRENT_DATE())
AND mode = 'SHADOW'
```

### Basic Query with Date Filter

```sql
SELECT
    checkpoint,
    final_action,
    COUNT(*) AS evaluation_count
FROM iguazu.server_events_production.RISK_CORE_CHECKPOINT_EVALUATION_SHADOW_EVENT
WHERE iguazu_sent_at >= DATEADD(hour, -2, CURRENT_TIMESTAMP())
AND checkpoint = 'dx_order_problem'
AND mode = 'SHADOW'
GROUP BY 1, 2
ORDER BY 3 DESC
```
