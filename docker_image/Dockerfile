FROM homeassistant/armv7-base-debian:latest

ENV LANG C.UTF-8

WORKDIR .
COPY . .
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-pandas
RUN rm -rf /var/lib/apt/lists/*

RUN pip3 install numpy
RUN pip3 install influxdb
RUN pip3 install plotly
RUN pip3 install pytz

RUN pip3 install dash
RUN pip3 install dash-bootstrap-components
RUN pip3 install flask
RUN pip3 install hypercorn

# Run the following command to build and tag the image: docker build -t jhockx/ha-python:0.2 - < Dockerfile
# Run the following command to rename the image: docker tag local-image:tagname jhockx/ha-python:0.2
# Run the following command to push to dockerhub: docker push jhockx/ha-python:0.2