#!/usr/bin/env bash
chown ec2-user:ec2-user /home/ec2-user/app
virtualenv /home/ec2-user/app/project-venv
chown ec2-user:ec2-user /home/ec2-user/app/project-venv
chown ec2-user:ec2-user /home/ec2-user/app/project-venv/*
source /home/ec2-user/app/project-venv/bin/activate
pip install -r /home/ec2-user/app/requirements.txt