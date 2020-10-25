#!/usr/bin/env bash

cd /home/ubuntu/app/

gunicorn m_back.wsgi:application --bind 0:8000 --env DJANGO_SETTINGS_MODULE='m_back.settings.deploy'
