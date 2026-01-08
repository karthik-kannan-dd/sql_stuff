# SQL Analysis with Claude Code

A workflow for running SQL queries and documenting analysis using Claude Code as your AI-powered data analyst.

## Why This Approach?

Instead of context-switching between SQL clients, spreadsheets, and documentation, you can:
- Ask Claude to write and run queries against your data warehouse
- Get instant analysis and insights from query results
- Build up a searchable knowledge base of past analyses
- Reference previous findings in new investigations

## Prerequisites

1. **Claude Code** - Install from [claude.ai/claude-code](https://claude.ai/claude-code)
2. **Snowflake CLI** (`snow`) - Or your preferred database CLI tool
   ```bash
   # Install Snowflake CLI
   pip install snowflake-cli-labs

   # Configure connection
   snow connection add
   ```

## Setup

### 1. Create a CLAUDE.md file

This file tells Claude how to interact with your database. Create `CLAUDE.md` in your project root:

```markdown
# SQL Analysis Workspace

Use the `snow sql` command for all queries. Example:
snow sql -q "SELECT * FROM my_table LIMIT 10"

## Common Tables
- `schema.table_name` - Description of what this table contains

## Query Patterns
Include any useful patterns, JSON extraction syntax, or table relationships.
```

### 2. Organize Your Workspace

```
sql_analysis/
├── CLAUDE.md              # Instructions for Claude
├── table_schemas/         # Store DESCRIBE results here
│   └── my_table.md
├── project_a/             # Group related analyses
│   ├── 01_initial_exploration.md
│   └── 02_deep_dive.md
└── project_b/
    └── analysis.md
```

## Safety: Read-Only SQL Hook

When giving Claude access to your database, you probably want to ensure it can only run `SELECT` queries and not accidentally `DELETE` or `DROP` your tables.

The [`hooks/validate-snow-sql.sh`](hooks/validate-snow-sql.sh) script is a **PreToolUse hook** that intercepts all `snow sql` commands and blocks any containing dangerous keywords.

### Blocked Keywords

```
DELETE, UPDATE, TRUNCATE, DROP, ALTER, INSERT, GRANT, REVOKE, MERGE
```

### Installation

1. Copy the hook script to your Claude hooks directory:
   ```bash
   cp hooks/validate-snow-sql.sh ~/.claude/hooks/
   chmod +x ~/.claude/hooks/validate-snow-sql.sh
   ```

2. Add the hook to your project's `.claude/settings.local.json`:
   ```json
   {
     "permissions": {
       "allow": ["Bash(snow sql:*)"]
     },
     "hooks": {
       "PreToolUse": [
         {
           "matcher": "Bash",
           "hooks": [
             {
               "type": "command",
               "command": "~/.claude/hooks/validate-snow-sql.sh"
             }
           ]
         }
       ]
     }
   }
   ```

   See [`hooks/settings.example.json`](hooks/settings.example.json) for a full example.

### How It Works

1. Claude attempts to run a `snow sql` command
2. The hook receives the command as JSON via stdin
3. It checks if the SQL contains any dangerous keywords
4. If found, it returns `{"decision": "block", "reason": "..."}` to prevent execution
5. If safe, it exits silently and the command proceeds

### Example

```
You: Delete all records from the users table

Claude: [attempts to run: snow sql -q "DELETE FROM users"]

Hook: BLOCKED: This session only has SELECT (read-only) permissions.
      Commands containing DELETE, UPDATE, TRUNCATE, DROP, ALTER,
      INSERT, GRANT, REVOKE, or MERGE are not allowed.
```

## Workflow

### Running Queries

Ask Claude naturally:

```
"How many orders did we have last week?"

"Show me the top 10 customers by revenue"

"What's the distribution of order values?"
```

Claude will:
1. Write the SQL query
2. Execute it using your configured CLI tool
3. Present and analyze the results
4. Save findings to a markdown file

### Building Context

As you analyze, Claude remembers:
- Table schemas it has explored
- Previous query results in the current session
- Patterns documented in your markdown files

Reference past work:
```
"Using the same customer cohort from yesterday's analysis,
what's their retention rate?"
```

### Documenting Findings

Each analysis file should include:
- Query purpose and context
- The SQL query itself
- Results (or summary for large result sets)
- Insights and next steps

Example format:

```markdown
# Customer Churn Analysis

> **Date:** January 8, 2025
> **Table:** analytics.customers

## Query
\```sql
SELECT
    DATE_TRUNC('month', churned_at) as month,
    COUNT(*) as churned_customers
FROM analytics.customers
WHERE churned_at IS NOT NULL
GROUP BY 1
ORDER BY 1
\```

## Results
| month | churned_customers |
|-------|-------------------|
| 2024-11 | 145 |
| 2024-12 | 203 |

## Insights
December showed a 40% increase in churn...
```

## Tips

### Keep Table Schemas Handy
When you query a new table, ask Claude to `DESCRIBE` it and save the schema:
```
"Describe the orders table and save the schema"
```

### Use Numbered Files for Multi-Step Analysis
Prefix files with numbers to show progression:
- `01_initial_exploration.md`
- `02_hypothesis_testing.md`
- `03_final_results.md`

### Let Claude Iterate
Don't try to write the perfect query upfront. Start broad:
```
"Show me a sample of 10 rows from the events table"
```

Then refine:
```
"Now filter to just error events from the last 24 hours"
```

### Reference Previous Work
Claude can read your past analysis files:
```
"Look at the customer segments we defined in project_a/segmentation.md
and apply them to this new dataset"
```

## Building Dashboards

Once you've validated your analysis in markdown, you can ask Claude to turn it into an interactive dashboard.

### Example: Streamlit Dashboard

See [`lateness_analysis/tools/`](lateness_analysis/tools/) for a working example.

```
You: I want to build a dashboard to look up lateness for individual dashers

Claude: I'll create a Streamlit app that:
- Takes a dasher ID as input
- Queries Snowflake for their delivery history
- Shows summary stats and risk classification
- Displays charts for lateness distribution
- Lets you download the data as CSV

[creates app.py, queries.py, requirements.txt]
```

### Running Dashboards

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```

### Dashboard Features Claude Can Build

| Feature | Libraries |
|---------|-----------|
| Interactive filters | Streamlit sidebar widgets |
| Data tables | Pandas + Streamlit dataframes |
| Charts | Plotly, Altair, or Matplotlib |
| Database queries | Snowflake connector, SQLAlchemy |
| Export options | CSV/Excel download buttons |

### Tips for Dashboard Creation

1. **Start with the analysis** - Build your queries in markdown first, then convert to a dashboard
2. **Keep queries separate** - Put SQL logic in a `queries.py` file for easier testing
3. **Add caching** - Use `@st.cache_data` to avoid re-running expensive queries
4. **Include error handling** - Wrap database calls in try/except blocks

## Example Session

```
You: I want to understand why orders dropped last Tuesday

Claude: Let me check the order volumes around that date...
[runs query, shows results]

It looks like orders dropped 34% on Tuesday. Let me check
if there were any system issues...
[runs another query]

I found that payment processing had errors from 2-4pm.
Here's the breakdown by hour...

You: Save this analysis to outage_analysis/jan_7_investigation.md

Claude: [saves file with queries, results, and findings]
```

## License

MIT
