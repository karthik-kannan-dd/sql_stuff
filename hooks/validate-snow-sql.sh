#!/bin/bash

# Hook to validate snow sql commands - blocks DELETE, UPDATE, TRUNCATE, DROP, etc.
# Only allows SELECT (read-only) queries

# Read hook input from stdin
input=$(cat)

# Extract tool name and command using python
tool_name=$(echo "$input" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_name',''))" 2>/dev/null)
command=$(echo "$input" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('command',''))" 2>/dev/null)

# Only validate Bash commands that start with "snow sql"
if [[ "$tool_name" != "Bash" ]]; then
    exit 0
fi

if [[ ! "$command" =~ ^snow[[:space:]]+sql ]]; then
    exit 0
fi

# Convert to uppercase for case-insensitive matching
upper_command=$(echo "$command" | tr '[:lower:]' '[:upper:]')

# List of dangerous SQL keywords to block
dangerous_keywords="DELETE|UPDATE|TRUNCATE|DROP|ALTER|INSERT|GRANT|REVOKE|MERGE"

if echo "$upper_command" | grep -qE "\b($dangerous_keywords)\b"; then
    # Output JSON to block with clear message
    cat << 'EOF'
{
  "decision": "block",
  "reason": "BLOCKED: This session only has SELECT (read-only) permissions. Commands containing DELETE, UPDATE, TRUNCATE, DROP, ALTER, INSERT, GRANT, REVOKE, or MERGE are not allowed."
}
EOF
    exit 0
fi

# Allow the command
exit 0
