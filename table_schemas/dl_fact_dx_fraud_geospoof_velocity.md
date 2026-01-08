# edw.opex.dl_fact_dx_fraud_geospoof_velocity

Geospoof velocity table for tracking delivery event location data and detecting potential location spoofing. Contains only 3 GPS pings per delivery, so not very suitable for detailed analysis use dimension_dasher_location_enhanced instead


## Columns

| Column | Type | Description |
|--------|------|-------------|
| DELIVERY_UUID | VARCHAR | DoorDash delivery UUID |
| DELIVERY_ID | NUMBER(38,0) | DoorDash delivery ID |
| DELIVERY_EVENT_ID | NUMBER(38,0) | Delivery event unique ID |
| SHIFT_ID | NUMBER(38,0) | Dasher shift ID |
| DASHER_ID | VARCHAR | DoorDash dasher ID |
| DELIVERY_EVENT_NAME | VARCHAR | Event name |
| CREATED_AT | TIMESTAMP_NTZ(9) | Event created at timestamp |
| AVG_LAT | FLOAT | Average dasher latitude collected between +-30 seconds windows from created at |
| AVG_LNG | FLOAT | Average dasher longitude collected between +-30 seconds windows from created at |
| AVG_ALTITUDE | FLOAT | Average dasher altitude collected between +-30 seconds windows from created at |
| AVG_H_ACCURACY | FLOAT | Average horizontal accuracy |
| AVG_V_ACCURACY | FLOAT | Average vertical accuracy |
| AVG_SPEED | FLOAT | Average dasher speed |
| PREV_LAT | FLOAT | Previous dasher latitude |
| PREV_LNG | FLOAT | Previous dasher longitude |
| PREV_ALT | FLOAT | Previous dasher altitude |
| PREV_DELIVERY_EVENT_NAME | VARCHAR | Previous dasher delivery event name |
| ADJ_DELIVERY_ID | NUMBER(38,0) | Previous delivery ID (same as DELIVERY_ID if within same delivery) |
| PREV_CREATED_AT | TIMESTAMP_NTZ(9) | Previous event created at timestamp |
| HORIZONTAL_DISTANCE_MILES | FLOAT | Distance between previous location and current location in miles |
| VERTICAL_DISTANCE_MILES | FLOAT | Distance between previous altitude and current altitude in miles |
| TIME_DIFF_HOURS | NUMBER(27,6) | Time difference in hours between current and previous event |
| HORIZONTAL_VELOCITY_MPH | FLOAT | Horizontal velocity in miles per hour |
| VERTICAL_VELOCITY_MPH | FLOAT | Vertical velocity in miles per hour |
| DEVICE_COUNT | NUMBER(38,0) | Dasher device count in last 1 minute of delivery |
| CREATED_DATE | DATE | Event created at date |
| ETL_CREATE_DATE_UTC | DATE | ETL created timestamp |
