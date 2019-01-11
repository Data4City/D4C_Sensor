curl -sSL https://get.docker.com | sh
sudo systemctl enable docker
sudo systemctl start docker

docker build --tag=sensorbox