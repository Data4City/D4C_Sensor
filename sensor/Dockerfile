#!/bin/bash

FROM balenalib/rpi-raspbian:latest
ENTRYPOINT []


RUN apt-get update -y
RUN apt-get install -y python3 python-pip-whl python3-pip python3-setuptools curl python3.5-dev
RUN apt-get -y install i2c-tools
RUN apt-get -y install libatlas-base-dev libasound-dev libportaudio-dev
RUN apt-get -y install libc-dev

RUN rm -rf /var/lib/apt/lists/*

COPY . /app
WORKDIR /app
RUN pip3 install wheel
RUN pip3 install -r /app/requirements.txt

CMD ["python3","-u", "main.py"]