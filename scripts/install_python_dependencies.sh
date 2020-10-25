#!/usr/bin/env bash
chown ubuntu:ubuntu /home/ubuntu/app
virtualenv /home/ubuntu/app/project-venv
chown ubuntu:ubuntu /home/ubuntu/app/project-venv
chown ubuntu:ubuntu /home/ubuntu/app/project-venv/*
source /home/ubuntu/app/project-venv/bin/activate
pip install -r /home/ubuntu/app/requirements.txt