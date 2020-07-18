ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

WORKDIR /src
COPY run.sh /
COPY utils.py ./
COPY plot_electricity.py ./
COPY test.py ./

WORKDIR /
RUN chmod a+x /run.sh
CMD [ "/run.sh" ]