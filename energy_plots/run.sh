#!/usr/bin/with-contenv bashio

echo ----
echo Files in workdir:
ls
echo ----
echo Files in app:
ls app
echo ----
echo Files in app:
ls configs
echo ----
echo Files in app:
ls plots
echo ----
echo 
echo starting script
python3 run_dashboard.py