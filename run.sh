#!/usr/bin/with-contenv bashio

echo ----
echo Files in workdir:
ls
echo ----

python3 read_influx.py

echo ----
echo Files in workdir:
ls
echo ----

echo Start server...
python3 -m http.server 8000
