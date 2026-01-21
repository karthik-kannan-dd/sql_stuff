# Labeled Time Fraud Tables

Human-labeled tables for time fraud model evaluation, stored in the `karthikkannan` schema.

## Schema

All tables share the same schema:

| Column | Type | Description |
|--------|------|-------------|
| DELIVERY_ID | NUMBER | Delivery identifier |
| DASHER_ID | NUMBER | Dasher identifier |
| IS_FRAUD | NUMBER | 1 = Fraud, 0 = Not Fraud, NULL = Maybe/TBD |

## Tables

### Review Tables (single delivery CVs)

| Table | Rows | Fraud | Not Fraud | NULL |
|-------|------|-------|-----------|------|
| `karthikkannan.time_fraud_test_2025_01_12` | 370 | 291 | 77 | 2 |
| `karthikkannan.time_fraud_test_2025_01_05` | 370 | 272 | 94 | 4 |

### Batch Tables (batch delivery CVs)

| Table | Rows | Fraud | Not Fraud | NULL |
|-------|------|-------|-----------|------|
| `karthikkannan.time_fraud_batch_2025_01_12` | 112 | 82 | 28 | 2 |
| `karthikkannan.time_fraud_batch_2025_01_05` | 112 | 73 | 37 | 2 |

## Access

All tables have SELECT granted to PUBLIC.
