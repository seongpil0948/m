#!/usr/bin/env bash
cd /home/ubuntu/app
source /home/ubuntu/app/project-venv/bin/activate

python manage.py makemigrations
python mange.py migrate
