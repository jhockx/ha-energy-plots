ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

WORKDIR /src
COPY run.sh /
COPY ./src/utils.py ./
COPY ./src/plot_electricity.py ./
COPY ./src/test.py ./

WORKDIR /
RUN chmod a+x /run.sh
CMD [ "/run.sh" ]