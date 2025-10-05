#!/bin/bash

# Check if a command argument is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 \"command\""
    echo "Example: $0 \"yes > /dev/null &\""
    exit 1
fi

URL="http://127.0.0.1:8000/job"
COMMAND="$1"
DATA="{\"command\": \"$COMMAND\"}"

for i in {1..5}
do
  echo "Submitting job #$i..."
  curl -X POST "$URL" \
       -H "Content-Type: application/json" \
       -d "$DATA" | jq .
  sleep 1
done
