sudo apt-get update
sudo apt-get install python3-pip
if  [ ! -d "$DIRECTORY" ]; then
    mkdir venv
    python3.6 -m venv venv
  # Control will enter here if $DIRECTORY exists.
fi

pip3 install -r requirements.txt 