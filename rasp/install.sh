if [ -x "$(command -v docker)" ]; then
    echo "Docker is already installed"
    # command
else
    echo "Installing docker"
    curl -sSL https://get.docker.com | sh

fi

sudo systemctl enable docker
sudo systemctl start docker

docker build --tag=sensorbox