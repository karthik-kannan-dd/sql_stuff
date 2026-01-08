# Introduction
This is a directory where we run sql queries and store their results so that i can reference and query them back later.

Each file must be an MD file, containing sql queries and their results. You can multiple sql queries in a single file. Name the files appropriately so we know what we're doing in the files so we can reference them. 

Use the snowflake tool `snow` for all your querying. It should be configured correctly for your use, if not raise a flag.

# Common Tables
Table schemas will be present in the table_schemas folder. If you find that one doesn't exist for a table we're querying, describe it first and add the schema to the corresponding MD file.  You can reference the table schema while querying it to verify if you're using the right columns. 


- iguazu.server_events_production.risk_checkpoint_evaluation_event_ice is a relatime log table of all of our fraud checkpoints and their various facts that were fed into the checkpoints and their corresponding results. Facts are stored as json in FACT_RESULTS and rules are stored RULE_RESULTS
You can access facts and rules like so. 
```sql
select 
    date(iguazu_sent_at) as active_date,
    JSON_EXTRACT_PATH_TEXT(FACT_RESULTS, 'fact_name.output') as fact_name,
    JSON_EXTRACT_PATH_TEXT(RULE_RESULTS, 'rule_name.output') as rule_name
```



