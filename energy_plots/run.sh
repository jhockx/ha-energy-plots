#!/usr/bin/with-contenv bashio

CONFIG_PATH=/data/options.json
HOST="$(bashio::config 'host')"
PORT="$(bashio::config 'port')"
USERNAME="$(bashio::config 'username')"
PASSWORD="$(bashio::config 'password')"
DAILY_GAS_USAGE="$(bashio::config 'daily_gas_usage')"
DAILY_ELECTRICITY_USAGE="$(bashio::config 'daily_electricity_usage')"
DAILY_YIELD="$(bashio::config 'daily_yield')"
DAILY_GAS_USAGE_MONTHLY_AVG="$(bashio::config 'daily_gas_usage_monthly_avg')"
DAILY_ELECTRICITY_USAGE_MONTHLY_AVG="$(bashio::config 'daily_electricity_usage_monthly_avg')"
DAILY_YIELD_MONTHLY_AVG="$(bashio::config 'daily_yield_monthly_avg')"
PREDICTED_SOLAR="$(bashio::config 'predicted_solar')"

echo ----
echo Files in workdir:
ls
echo ----

echo Start server...
nohup python3 -m http.server 8000 --directory ./src &

echo Run electricity script...
python3 ./src/plot_electricity.py "${HOST}" "${PORT}" "${USERNAME}" "${PASSWORD}" "${DAILY_ELECTRICITY_USAGE}" "${DAILY_YIELD}" "${DAILY_ELECTRICITY_USAGE_MONTHLY_AVG}" "${DAILY_YIELD_MONTHLY_AVG}" "${PREDICTED_SOLAR}" &

echo Run gas script...
python3 ./src/plot_gas.py "${HOST}" "${PORT}" "${USERNAME}" "${PASSWORD}" "${DAILY_GAS_USAGE}" "${DAILY_GAS_USAGE_MONTHLY_AVG}"
