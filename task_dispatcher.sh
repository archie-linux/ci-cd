#!/bin/bash

URL="http://127.0.0.1:8000/job"
DATA='{"command": "pytest -v"}'

for i in {1..5}
do
  echo "Submitting job #$i..."
  curl -X POST "$URL" \
       -H "Content-Type: application/json" \
       -d "$DATA" | jq .
  sleep 1  # Optional delay between requests
done

