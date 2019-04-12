FROM python:3.7-alpine3.9

ADD . /home/pseudo
WORKDIR /home/pseudo
RUN pip3 install click
RUN pip3 install .
WORKDIR /home
RUN rm -rf /home/pseudo

ENTRYPOINT ["pdc"]