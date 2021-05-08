FROM homeassistant/armv7-base-debian:latest

ENV LANG C.UTF-8

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-pandas
RUN apt-get install -y gunicorn3
RUN rm -rf /var/lib/apt/lists/*

RUN pip3 install numpy
RUN pip3 install influxdb
RUN pip3 install plotly
RUN pip3 install pytz

RUN pip3 install dash
RUN pip3 install dash-bootstrap-components
RUN pip3 install flask
RUN pip3 install gunicorn