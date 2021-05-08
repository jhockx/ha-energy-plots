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
gunicorn run_dashboard:server -b 0.0.0.0:8050