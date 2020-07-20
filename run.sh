#!/usr/bin/with-contenv bashio

CONFIG_PATH=/data/options.json
HOST="$(bashio::config 'host')"
PORT="$(bashio::config 'port')"
USERNAME="$(bashio::config 'username')"
PASSWORD="$(bashio::config 'password')"
DAILY_GAS_USAGE="$(bashio::config 'daily_gas_usage')"
DAILY_ELECTRICITY_USAGE="$(bashio::config 'daily_electricity_usage')"
DAILY_YIELD="$(bashio::config 'daily_yield')"
PREDICTED_SOLAR="$(bashio::config 'predicted_solar')"

echo ----
echo Files in workdir:
ls
echo ----

python3 ./src/test.py "${HOST}" "${PORT}" "${USERNAME}" "${PASSWORD}" "${DAILY_GAS_USAGE}"

echo Start server...
nohup python3 -m http.server 8000 --directory ./src &

echo Run electricity script...
python3 ./src/plot_electricity.py "${HOST}" "${PORT}" "${USERNAME}" "${PASSWORD}" "${DAILY_ELECTRICITY_USAGE}" "${DAILY_YIELD}" "${PREDICTED_SOLAR}" &

echo Run gas script...
python3 ./src/plot_gas.py "${HOST}" "${PORT}" "${USERNAME}" "${PASSWORD}" "${DAILY_GAS_USAGE}"
