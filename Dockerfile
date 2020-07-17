ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

WORKDIR /src
COPY run.sh /
COPY read_influx.py ./
COPY test.py ./

WORKDIR /
RUN chmod a+x /run.sh
CMD [ "/run.sh" ]