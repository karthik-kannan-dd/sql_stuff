# Introduction
This is a directory where we run sql queries and store their results so that i can reference and query them back later.

Each file must be an MD file, containing sql queries and their results. You can multiple sql queries in a single file. Name the files appropriately so we know what we're doing in the files so we can reference them. 

Use the snowflake tool `snow` for all your querying. It should be configured correctly for your use, if not raise a flag.

Once you do analysis, restrict yourself to talking about the results and insights. Do not give recommendations or opine about the nature of deliveries, unless explicitly asked. For example: Do not talk about what could be causing the fraud, or how to address it. 

# Table Schemas
Table schemas will be present in the table_schemas folder. If you find that one doesn't exist for a table we're querying, describe it first and add the schema to the corresponding MD file.  Reference the table schema while querying it to verify if you're using the right columns. 

# Useful Abbrevatiations
Mx = Merchant
Dx = Dasher
Cx = Consumer
Comms = Consumer

# Model Scores
You can access the model scores from 

# Important
- When querying large tables like dimension_deliveries ALWAYS restrict by date. If you don't know what dates to restrict by, ask. 
- Queries often take long, this is because we're competing with other folks in th ecompany, and queries can sometime be queued for a while. Only restart them if they take more than 10 monitues




