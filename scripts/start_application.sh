#!/usr/bin/env bash

cd /home/ubuntu/app/
source /home/ubuntu/app/project-venv/bin/activate

gunicorn m_back.wsgi:application --bind 0:8000 --env DJANGO_SETTINGS_MODULE='m_back.settings.deploy'
