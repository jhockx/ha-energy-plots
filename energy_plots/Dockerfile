ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

WORKDIR /
COPY run.sh /
COPY ./app ./app
COPY ./configs ./configs
COPY ./plots ./plots
COPY ./run_dashboard.py ./run_dashboard.py
COPY ./run.sh ./run.sh

EXPOSE 8099

RUN chmod a+x ./run.sh
CMD [ "./run.sh" ]