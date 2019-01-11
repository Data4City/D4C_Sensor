FROM balenalib/rpi-raspbian:latest
ENTRYPOINT []

RUN apt-get -q update && \
	apt-get -qy install \
        	i2c-tools \
        python3 python3-pip \
        python-dev python-pip gcc make  

COPY requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt
COPY . /tmp/


EXPOSE 80

CMD ["python3","-u", "/tmp/light.py"]