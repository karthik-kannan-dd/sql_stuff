# PRODDB.PUBLIC.DIMENSION_DELIVERIES

Table containing delivery-level data including completion status, dasher assignment, timestamps, financials, and metrics. This is a large table with 230+ columns.

## Key Columns for Geospoofing Analysis

| Column | Type | Description |
|--------|------|-------------|
| DELIVERY_ID | NUMBER | Unique numeric identifier for the delivery |
| DELIVERY_UUID | TEXT | UUID identifier (matches GPS table's DELIVERY_UUID) |
| DASHER_ID | NUMBER | ID of the dasher who completed the delivery |
| ACTUAL_DELIVERY_TIME | TIMESTAMP_NTZ | When the delivery was dropped off (NULL if not completed) |
| CANCELLED_AT | TIMESTAMP_NTZ | When delivery was cancelled (NULL if not cancelled) |
| ACTIVE_DATE | DATE | Date of the delivery (use for filtering - table is massive) |

## Column Categories

### Core Delivery Info
| Column | Type | Description |
|--------|------|-------------|
| DELIVERY_ID | NUMBER | Unique delivery identifier (primary key) |
| DELIVERY_UUID | TEXT | UUID identifier for the delivery |
| PUBLIC_ID | TEXT | Public-facing delivery ID |
| DELIVERY_RATING | NUMBER | Rating given to the delivery by the consumer |
| ACTIVE_DATE | DATE | Date of the delivery |
| BATCH_ID | NUMBER | ID if delivery was batched with others |
| PARENT_DELIVERY_ID | NUMBER | Parent delivery ID for sub-deliveries |

### Consumer Info
| Column | Type | Description |
|--------|------|-------------|
| CREATOR_ID | NUMBER | Consumer who created the order |
| IS_FIRST_ORDERCART | BOOLEAN | Whether this is a new user's first order |
| FIRST_CONSUMER_DELIVERY | NUMBER | First delivery indicator for consumer |
| IS_GROUP_ORDER | BOOLEAN | Whether this is a group order |
| IS_SUBSCRIBED_CONSUMER | BOOLEAN | Whether consumer has subscription (DashPass) |
| IS_SUBSCRIPTION_DISCOUNT_APPLIED | BOOLEAN | Whether subscription discount was applied |
| SUBSCRIPTION_PLAN_ID | NUMBER | Subscription plan identifier |

### Store/Business Info
| Column | Type | Description |
|--------|------|-------------|
| STORE_ID | NUMBER | Store identifier |
| BUSINESS_ID | NUMBER | Business identifier |
| STORE_NAME | TEXT | Name of the store |
| BUSINESS_NAME | TEXT | Name of the business |
| STORE_STARTING_POINT_ID | NUMBER | Store's starting point |
| MENU_ID | NUMBER | Menu identifier |

### Geographic Info
| Column | Type | Description |
|--------|------|-------------|
| REGION_ID | NUMBER | Region identifier |
| MARKET_ID | NUMBER | Market identifier |
| SUBMARKET_ID | NUMBER | Submarket identifier |
| SUBMARKET_NAME | TEXT | Submarket name |
| DISTRICT_ID | NUMBER | District identifier |
| TIMEZONE | TEXT | Delivery timezone |
| COUNTRY_ID | NUMBER | Country identifier |
| PICKUP_ADDRESS_ID | NUMBER | Pickup address ID |
| DELIVERY_ADDRESS_ID | NUMBER | Delivery address ID |

### Dasher Info
| Column | Type | Description |
|--------|------|-------------|
| DASHER_ID | NUMBER | ID of the dasher who completed the delivery |
| IS_FIRST_DASHER_DELIVERY | BOOLEAN | Whether this is dasher's first delivery |
| DASHER_STARTING_POINT_ID | NUMBER | Dasher's starting point |
| DELIVERY_VEHICLE_TYPE | TEXT | Type of vehicle used for delivery |
| DASHER_SCORE | NUMBER | Dasher's score |
| SHIFT_ID | NUMBER | Shift identifier |
| TENTATIVE_SHIFT_ID | NUMBER | Tentative shift ID |

### Timestamps (Key for Analysis)
| Column | Type | Description |
|--------|------|-------------|
| CREATED_AT | TIMESTAMP_NTZ | When the delivery was created |
| QUOTED_DELIVERY_TIME | TIMESTAMP_NTZ | Quoted delivery time to consumer |
| ESTIMATED_DELIVERY_TIME | TIMESTAMP_NTZ | Estimated delivery time |
| FIRST_ASSIGNMENT_MADE_TIME | TIMESTAMP_NTZ | When first dasher was assigned |
| DASHER_ASSIGNED_TIME | TIMESTAMP_NTZ | When current dasher was assigned |
| DASHER_CONFIRMED_TIME | TIMESTAMP_NTZ | When dasher confirmed assignment |
| STORE_CONFIRMED_TIME | TIMESTAMP_NTZ | When store confirmed order |
| DASHER_AT_STORE_TIME | TIMESTAMP_NTZ | When dasher arrived at store |
| DASHER_CONFIRMED_AT_STORE_TIME | TIMESTAMP_NTZ | When dasher confirmed at store |
| ACTUAL_PICKUP_TIME | TIMESTAMP_NTZ | When dasher picked up the order |
| STORE_ORDER_READY_TIME | TIMESTAMP_NTZ | When store marked order ready |
| ACTUAL_DELIVERY_TIME | TIMESTAMP_NTZ | When dasher dropped off the order |
| CANCELLED_AT | TIMESTAMP_NTZ | When delivery was cancelled (if applicable) |

### Local Time Variants
| Column | Type | Description |
|--------|------|-------------|
| ACTUAL_PICKUP_TIME_LOCAL | TIMESTAMP_NTZ | Pickup time in local timezone |
| ACTUAL_DELIVERY_TIME_LOCAL | TIMESTAMP_NTZ | Delivery time in local timezone |
| DASHER_ASSIGNED_TIME_LOCAL | TIMESTAMP_NTZ | Assignment time in local timezone |
| DASHER_AT_STORE_TIME_LOCAL | TIMESTAMP_NTZ | At store time in local timezone |
| DASHER_CONFIRMED_AT_STORE_TIME_LOCAL | TIMESTAMP_NTZ | Confirmed at store time in local timezone |

### Assignment Metrics
| Column | Type | Description |
|--------|------|-------------|
| NUM_ASSIGNS | NUMBER | Number of times the delivery was assigned |
| NUM_UNASSIGNS | NUMBER | Number of times the delivery was unassigned |
| MANUAL_UNASSIGNS | NUMBER | Manual unassignment count |
| DRIVER_DIDNT_RECEIVE_ASSIGNMENTS | NUMBER | Failed assignment receipts |
| DRIVER_MONITOR_UNASSIGNED | NUMBER | Monitor-triggered unassignments |
| UNASSIGNED_FOR_LATE_CHECK_IN | NUMBER | Late check-in unassignments |
| DRIVER_SELF_UNASSIGNEDS | NUMBER | Dasher self-unassignments |
| RENEGES | NUMBER | Renege count |
| DECLINES | NUMBER | Decline count |
| CONFIRMATIONS | NUMBER | Confirmation count |
| MANUALLY_ASSIGNED | BOOLEAN | Whether manually assigned |
| IS_PREASSIGNED | BOOLEAN | Whether preassigned |

### Duration Metrics
| Column | Type | Description |
|--------|------|-------------|
| CONFIRM_TO_DELIVER_DURATION | NUMBER | Time from confirm to delivery |
| D2R_DURATION | NUMBER | Dasher to restaurant duration |
| DASHER_WAIT_DURATION | NUMBER | Time dasher waited at store |
| R2C_DURATION | NUMBER | Restaurant to consumer duration |
| DIRECT_R2C_EST_DURATION | NUMBER | Direct R2C estimated duration |
| D2P_DURATION | NUMBER | Dasher to pickup duration |
| T2P_DURATION | NUMBER | Time to pickup duration |
| WAP_DURATION | NUMBER | Wait after pickup duration |
| D2C_DURATION | NUMBER | Dasher to consumer duration |
| DEMAND_CONCENTRATION_DURATION | NUMBER | Demand concentration time |
| DISTINCT_ACTIVE_DURATION | NUMBER | Distinct active time |
| PREDICTED_DELIVERY_DURATION | NUMBER | ML-predicted delivery duration |

### Financial - Fees
| Column | Type | Description |
|--------|------|-------------|
| FEE | NUMBER | Total fee |
| DELIVERY_FEE | NUMBER | Delivery fee charged |
| DRIVE_FEE | NUMBER | Drive fee |
| ALCOHOL_DELIVERY_FEE | NUMBER | Alcohol delivery fee |
| CORE_DELIVERY_FEE | NUMBER | Core delivery fee |
| FEE_BASERATE | NUMBER | Base rate fee |
| SERVICE_FEE | NUMBER | Service fee |
| SERVICE_FEE_NO_DSCNT | NUMBER | Service fee before discount |
| SMALL_ORDER_FEE | NUMBER | Small order fee |
| SOS_FEE | NUMBER | SOS fee |

### Financial - Order Value
| Column | Type | Description |
|--------|------|-------------|
| SUBTOTAL | NUMBER | Order subtotal |
| TAX | NUMBER | Tax amount |
| TAX_RATE | FLOAT | Tax rate |
| VALUE_OF_CONTENTS | NUMBER | Value of order contents |
| GOV | NUMBER | Gross order value |
| TIP | NUMBER | Total tip |
| PRE_TIP_AMOUNT | NUMBER | Pre-tip amount |
| DRIVE_POST_TIP_AMOUNT | NUMBER | Post-tip amount for Drive |

### Financial - Dasher Pay
| Column | Type | Description |
|--------|------|-------------|
| DASHER_BASE_PAY | NUMBER | Dasher's base pay |
| DASHER_DELIVERY_BOOST | NUMBER | Delivery boost pay |
| DELIVERY_PEAK_PAY | FLOAT | Peak pay amount |
| DELIVERY_SOS_AMOUNT | FLOAT | SOS pay amount |
| DELIVERY_SETUP_PAY | FLOAT | Setup pay |
| DASHER_PAY_OTHER | NUMBER | Other dasher pay |
| DASHER_CATCH_ALL | NUMBER | Catch-all dasher pay |
| DOORDASH_CONTRIBUTION_AMOUNT | NUMBER | DoorDash contribution |
| FAIR_VALUE_AMOUNT | NUMBER | Fair value pay |
| IS_ON_DYNAMIC_PAY_MODEL | BOOLEAN | On dynamic pay model |
| DASHER_PAY_TARGET_ID | NUMBER | Pay target ID |

### Financial - Commission & Costs
| Column | Type | Description |
|--------|------|-------------|
| COMMISSION | NUMBER | Commission amount |
| COMMISSION_RATE | FLOAT | Commission rate |
| ALCOHOL_COMMISSION_AMOUNT | NUMBER | Alcohol commission |
| CORE_COMMISSION_AMOUNT | NUMBER | Core commission |
| SUPPORT_COST | NUMBER | Support cost |
| ORDER_PLACER_COST | NUMBER | Order placer cost |
| REDELIVERY_COST | NUMBER | Redelivery cost |

### Financial - Refunds & Credits
| Column | Type | Description |
|--------|------|-------------|
| CONSUMER_REFUND | NUMBER | Consumer refund amount |
| STORE_REFUND | NUMBER | Store refund amount |
| STORE_CHARGE | NUMBER | Store charge |
| SUPPORT_CREDIT | NUMBER | Support credit |
| SUBSCRIPTION_CREDIT | NUMBER | Subscription credit |
| XCREDITS_ISSUED | NUMBER | X credits issued |
| GIFT_CODE_CREDIT | NUMBER | Gift code credit |
| DELIVERY_GIFT_CREDIT | NUMBER | Delivery gift credit |

### Order Flags
| Column | Type | Description |
|--------|------|-------------|
| IS_ASAP | BOOLEAN | Whether ASAP order |
| IS_REORDER | BOOLEAN | Whether reorder |
| IS_FROM_STORE_TO_US | BOOLEAN | Store to us flag |
| IS_AUTOMATED | BOOLEAN | Whether automated |
| IS_FRAUDULENT | BOOLEAN | Whether flagged as fraudulent |
| IS_PENDING_RESOLUTION | BOOLEAN | Pending resolution flag |
| IS_MISSING_INCORRECT | BOOLEAN | Missing/incorrect items flag |
| WAS_BATCHED | BOOLEAN | Whether batched |
| IS_PARTNER | BOOLEAN | Partner delivery |
| IS_COMMISSION_PARTNER | BOOLEAN | Commission partner |
| IS_DEPOT | BOOLEAN | Depot delivery |
| IS_CONSUMER_PICKUP | BOOLEAN | Consumer pickup |
| IS_TEST | BOOLEAN | Test delivery |
| IS_FILTERED | BOOLEAN | Filtered flag |
| IS_FILTERED_CORE | BOOLEAN | Core filtered flag |

### Platform & Protocol
| Column | Type | Description |
|--------|------|-------------|
| SUBMIT_PLATFORM | TEXT | Order submission platform |
| SOURCE | TEXT | Order source |
| DEVICE_TYPE | TEXT | Device type used |
| ORDER_PROTOCOL | TEXT | Order protocol |
| CONFIRM_PROTOCOL | TEXT | Confirmation protocol |
| PAYMENT_PROTOCOL | TEXT | Payment protocol |
| FLF | TEXT | FLF designation |
| BUSINESS_LINE | TEXT | Business line |
| FULFILLMENT_TYPE | TEXT | Fulfillment type |
| DELIVERY_LOCATION | TEXT | Delivery location type |

### Item Info
| Column | Type | Description |
|--------|------|-------------|
| ORDER_CART_ID | NUMBER | Order cart ID |
| STORE_ORDER_CART_ID | NUMBER | Store order cart ID |
| DISTINCT_ITEM_COUNT | NUMBER | Count of distinct items |
| TOTAL_ITEM_COUNT | NUMBER | Total item count |
| MAX_ORIGINAL_ITEM_PRICE | NUMBER | Max item price |
| MIN_ORIGINAL_ITEM_PRICE | NUMBER | Min item price |

## Example Queries

```sql
-- Get completed deliveries for a specific date range
SELECT
    DELIVERY_UUID,
    DASHER_ID,
    ACTUAL_DELIVERY_TIME
FROM PRODDB.PUBLIC.DIMENSION_DELIVERIES
WHERE ACTIVE_DATE >= DATEADD(day, -3, CURRENT_DATE())
  AND ACTUAL_DELIVERY_TIME IS NOT NULL;
```

```sql
-- Join with GPS data to filter for completing dasher only
SELECT
    gps.DELIVERY_UUID,
    gps.DASHER_ID,
    dd.ACTUAL_DELIVERY_TIME
FROM proddb.public.dimension_dasher_location_enhanced gps
INNER JOIN PRODDB.PUBLIC.DIMENSION_DELIVERIES dd
    ON gps.DELIVERY_UUID = dd.DELIVERY_UUID
    AND gps.DASHER_ID = dd.DASHER_ID
WHERE gps.TIME >= DATEADD(day, -3, CURRENT_TIMESTAMP())
  AND dd.ACTIVE_DATE >= DATEADD(day, -3, CURRENT_DATE())
  AND dd.ACTUAL_DELIVERY_TIME IS NOT NULL;
```

```sql
-- Analyze dasher assignment patterns
SELECT
    DELIVERY_UUID,
    DASHER_ID,
    NUM_ASSIGNS,
    NUM_UNASSIGNS,
    DRIVER_SELF_UNASSIGNEDS,
    RENEGES,
    DECLINES
FROM PRODDB.PUBLIC.DIMENSION_DELIVERIES
WHERE ACTIVE_DATE >= DATEADD(day, -7, CURRENT_DATE())
  AND NUM_UNASSIGNS > 0;
```

## Notes

- **Always filter by ACTIVE_DATE** when querying this table - it's very large (230+ columns, millions of rows)
- `ACTUAL_DELIVERY_TIME IS NOT NULL` indicates a completed delivery
- `DASHER_ID` is the dasher who completed the delivery (not intermediate dashers who may have been reassigned)
- Use `DELIVERY_UUID` to join with GPS data from `dimension_dasher_location_enhanced`
- `NUM_ASSIGNS` > 1 indicates the delivery was reassigned at least once
- Financial columns are useful for fraud analysis (e.g., unusually high tips, refunds)
- Duration metrics can help identify anomalous delivery patterns

