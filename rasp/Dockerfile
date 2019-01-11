FROM balenalib/rpi-raspbian:latest
ENTRYPOINT []

RUN apt-get -q update && \
	apt-get -qy install \
        python3 python3-pip \
        python-dev python-pip gcc make  

RUN pip3 install -r requirements.txt


COPY . /app
WORKDIR /app

RUN pip3 install  -r requirements.txt

EXPOSE 80

ENV NAME World

# Run app.py when the container launches
CMD ["python3", "light.py"]