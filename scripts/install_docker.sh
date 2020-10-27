#!/bin/bash

echo "Install Docker"
sudo apt install docker.io -y
sudo apt install docker-compose -y
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
sudo service docker restart

cd ~/app
docker-compose up --build -d
