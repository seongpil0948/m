#!/bin/bash

echo "Start with gunicorn"
cd /app
gunicorn m_back.wsgi:application --bind 0:8000 --env DJANGO_SETTINGS_MODULE='m_back.settings.deploy'