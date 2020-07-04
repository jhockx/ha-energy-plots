FROM homeassistant/armv7-base-debian:latest

ENV LANG C.UTF-8

WORKDIR .
COPY . .
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-pandas
RUN rm -rf /var/lib/apt/lists/*

# RUN pip3 install pandas
RUN pip3 install influxdb
RUN pip3 install plotly

# Run the following command to build the image: docker build - < Dockerfile
# Run the following command to rename the image: docker tag local-image:tagname jhockx/ha-python:test
# Or: docker tag image-id jhockx/ha-python:test
# Run the following command to push to dockerhub: docker push jhockx/ha-python:test