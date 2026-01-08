# risk_checkpoint_evaluation_event_ice

**Full Table Name:** `iguazu.server_events_production.risk_checkpoint_evaluation_event_ice`

**Description:** Realtime log table of all fraud checkpoints and their various facts that were fed into the checkpoints and their corresponding results.

## Schema

| Column Name | Data Type | Nullable | Description |
|-------------|-----------|----------|-------------|
| EVALUATION_ID | VARCHAR | Y | Unique identifier for the checkpoint evaluation |
| CHECKPOINT | VARCHAR | Y | Name of the fraud checkpoint being evaluated |
| MODE | VARCHAR | Y | Evaluation mode |
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
| FACT_RESULTS | VARCHAR | Y | Results from fact evaluations (JSON) - see usage below |
| RULE_RESULTS | VARCHAR | Y | Results from rule evaluations (JSON) - see usage below |
| DELIVERY_ID | VARCHAR | Y | Associated delivery ID |
| LINK_ID | VARCHAR | Y | Associated link ID |
| _EVENT_NAME_ | VARCHAR | Y | Internal event name |
| _EVENT_TIME_ | NUMBER(19,0) | Y | Event timestamp (epoch) |
| _IDEMPOTENCY_KEY_ | VARCHAR | Y | Idempotency key for deduplication |
| _SOURCE_ | VARCHAR | Y | Event source |
| _ENTITY_NAME_ | VARCHAR | Y | Internal entity name |
| _ENTITY_ID_ | VARCHAR | Y | Internal entity ID |
| _CUSTOM_ATTRIBUTES_ | VARCHAR | Y | Custom attributes (JSON) |
| _EVENT_VERSION_ | NUMBER(10,0) | Y | Event schema version |
| _KAFKA_TIMESTAMP_ | NUMBER(19,0) | Y | Kafka message timestamp (epoch) |
| _KAFKA_PARTITION_ | NUMBER(10,0) | Y | Kafka partition |
| _KAFKA_OFFSET_ | NUMBER(19,0) | Y | Kafka offset |
| _KAFKA_TOPIC_ | VARCHAR | Y | Kafka topic name |
| IGUAZU_ID | VARCHAR | Y | Iguazu internal ID |
| IGUAZU_SENT_AT | TIMESTAMP_NTZ(6) | Y | Timestamp when sent to Iguazu |
| IGUAZU_OTHER_PROPERTIES | VARCHAR | Y | Other Iguazu properties (JSON) |
| _KAFKA_TIMESTAMP | TIMESTAMP_NTZ(6) | Y | Kafka timestamp (timestamp format) |
| IGUAZU_PARTITION_DATE | VARCHAR | Y | Partition date (for partitioning) |
| IGUAZU_PARTITION_HOUR | NUMBER(10,0) | N | Partition hour (for partitioning) |
| EVALUATED_AT | TIMESTAMP_NTZ(6) | Y | Timestamp when evaluation occurred |
| EXPERIMENT_OVERRIDES | VARCHAR | Y | Experiment overrides (JSON) |

## Key Columns

- **IGUAZU_SENT_AT** - Primary timestamp column for time-based filtering
- **CHECKPOINT** - The fraud checkpoint name being evaluated
- **FACT_RESULTS** - JSON containing all fact outputs
- **RULE_RESULTS** - JSON containing all rule outputs
- **FINAL_ACTION** - The resulting action from the checkpoint evaluation

## Usage Examples

### Accessing Facts and Rules from JSON

```sql
SELECT
    DATE(iguazu_sent_at) AS active_date,
    JSON_EXTRACT_PATH_TEXT(FACT_RESULTS, 'fact_name.output') AS fact_name,
    JSON_EXTRACT_PATH_TEXT(RULE_RESULTS, 'rule_name.output') AS rule_name
FROM iguazu.server_events_production.risk_checkpoint_evaluation_event_ice
WHERE iguazu_sent_at >= DATEADD(day, -7, CURRENT_DATE())
```

### Basic Query with Date Filter

```sql
SELECT
    final_action,
    COUNT(*) AS evaluation_count
FROM iguazu.server_events_production.risk_checkpoint_evaluation_event_ice
WHERE iguazu_sent_at >= DATEADD(day, -1, CURRENT_DATE())
AND checkpoint = '<checkpoint>'
GROUP BY 1, 2
ORDER BY 3 DESC
```
