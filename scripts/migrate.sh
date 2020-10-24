#!/usr/bin/env bash
cd /home/ec2-user/app
source /home/ec2-user/app/project-venv/bin/activate

python manage.py makemigrations
python mange.py migrate
