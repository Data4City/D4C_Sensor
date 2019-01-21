FROM balenalib/rpi-raspbian:latest
ENTRYPOINT []


RUN apt-get update \
	&& apt-get install -y curl \
	&& rm -rf /var/lib/apt/lists/*


RUN apt-get update
RUN apt-get install -y redis-server


EXPOSE 6379
CMD ["redis-server", "--protected-mode no"]


RUN apt-get update && \
	apt-get -y install \
        	i2c-tools \
                libatlas-base-dev \
                libasound-dev \
                libportaudio-dev  \
        python3 python3-pip

COPY requirements.txt /data/
RUN pip3 install -r /data/requirements.txt
COPY . /data/


EXPOSE 80

CMD ["python3","-u", "/tmp/main.py"]