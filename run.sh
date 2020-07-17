#!/usr/bin/with-contenv bashio

CONFIG_PATH=/data/options.json
DAILY_ELECTRICITY_USAGE=$(jq --raw-output ".daily_electricity_usage" $CONFIG_PATH)

echo ----
echo Files in workdir:
ls
echo ----

python3 src/test.py DAILY_ELECTRICITY_USAGE

echo Start server...
nohup python3 -m http.server 8000 --directory ./src &

echo Run script...
python3 src/read_influx.py
