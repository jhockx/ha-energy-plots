#!/usr/bin/with-contenv bashio

echo ----
echo Files in workdir:
ls
echo ----

echo Start server...
nohup python3 -m http.server 8000 &

echo Run script...
python3 read_influx.py
