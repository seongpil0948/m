#!/bin/bash

echo "Setting: ${DJANGO_SETTINGS_MODULE}"

echo "WORKDIR"
cd /app

echo "Migrate DB"
python manage.py migrate

echo "Install requirements"
pip install -r requirements

echo "Run Server..."
gunicorn m_back.wsgi:application --bind 0:8000 --env DJANGO_SETTINGS_MODULE='m_back.settings.deploy'