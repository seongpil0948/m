#!/usr/bin/env bash
sudo chown ubuntu:ubuntu /home/ubuntu/app
virtualenv /home/ubuntu/app/project-venv
sudo chown ubuntu:ubuntu /home/ubuntu/app/project-venv
sudo chown ubuntu:ubuntu /home/ubuntu/app/project-venv/*
sudo source /home/ubuntu/app/project-venv/bin/activate
pip install -r /home/ubuntu/app/requirements.txt