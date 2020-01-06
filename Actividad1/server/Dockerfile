FROM python:latest
RUN apt-get update
RUN apt-get install -y python3
RUN cd /usr/local/bin

RUN python -m pip install grpcio
RUN python -m pip install grpcio-tools

ADD server.py /server/

WORKDIR /server/