#!/usr/bin/env bash

cd /home/ec2-user/app/
source /home/ec2-user/app/project-venv/bin/activate

gunicorn m_back.wsgi:application --bind 0:8000 --env DJANGO_SETTINGS_MODULE='m_back.settings.deploy'
