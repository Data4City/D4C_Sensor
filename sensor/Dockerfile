#!/bin/bash

FROM balenalib/rpi-raspbian:latest
ENTRYPOINT []


RUN apt-get update -y
RUN apt-get install -y python3 python-pip-whl python3-pip python3-setuptools curl python3.5-dev
RUN apt-get -y install i2c-tools libatlas-base-dev libasound-dev libportaudio-dev
RUN rm -rf /var/lib/apt/lists/*


COPY sensor /data/
RUN pip3 install wheel
RUN pip3 install -r /data/requirements.txt
COPY .. /data/

ARG param
CMD ["python3","-u", "/data/main.py", "$param"]