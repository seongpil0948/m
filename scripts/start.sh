#!/bin/bash

echo "Setting: ${DJANGO_SETTINGS_MODULE}"

# Migrate DB
echo "Migrate DB"
python manage.py migrate

echo "Docker-Compose Up"
docker-compose up -d
