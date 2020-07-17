#!/usr/bin/with-contenv bashio

CONFIG_PATH=/data/options.json
HOST="$(bashio::config 'host')"
PORT="$(bashio::config 'port')"
USERNAME="$(bashio::config 'username')"
PASSWORD="$(bashio::config 'password')"
DAILY_ELECTRICITY_USAGE="$(bashio::config 'daily_electricity_usage')"
DAILY_YIELD="$(bashio::config 'daily_yield')"

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
