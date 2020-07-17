#!/usr/bin/with-contenv bashio

CONFIG_PATH=/data/options.json
HOST=$(jq --raw-output ".host" $CONFIG_PATH)
PORT=$(jq --raw-output ".port" $CONFIG_PATH)
USERNAME=$(jq --raw-output ".username" $CONFIG_PATH)
PASSWORD=$(jq --raw-output ".password" $CONFIG_PATH)
DAILY_ELECTRICITY_USAGE=$(jq --raw-output ".daily_electricity_usage" $CONFIG_PATH)
DAILY_YIELD=$(jq --raw-output ".daily_yield" $CONFIG_PATH)

echo ----
echo Files in workdir:
ls
echo ----
echo "${DAILY_ELECTRICITY_USAGE}"
echo "${DAILY_YIELD}"
python3 src/test.py "${DAILY_ELECTRICITY_USAGE}" "${DAILY_YIELD}"

echo Start server...
nohup python3 -m http.server 8000 --directory ./src &

echo Run script...
python3 src/read_influx.py
