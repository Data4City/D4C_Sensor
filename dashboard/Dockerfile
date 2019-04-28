#!/bin/bash

FROM balenalib/rpi-raspbian:latest
ENTRYPOINT []


RUN apt-get update -y
RUN apt-get install -y python3 python-pip-whl python3-pip python3-setuptools python3.5-dev
RUN rm -rf /var/lib/apt/lists/*


COPY ./app /app
WORKDIR /app
RUN pip3 install wheel
RUN pip3 install -r /app/requirements.txt


CMD ["python3", "flask_helper.py"]