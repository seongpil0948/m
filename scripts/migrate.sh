#!/usr/bin/env bash
cd /home/ubuntu/app

python manage.py makemigrations
python mange.py migrate
