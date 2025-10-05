#!/bin/bash

URL="http://127.0.0.1:8000/job"
DATA='{"command": "yes > /dev/null &"}'

for i in {1..3}
do
  echo "Submitting job #$i..."
  curl -X POST "$URL" \
       -H "Content-Type: application/json" \
       -d "$DATA" | jq .
  sleep 1  # Optional delay between requests
done

