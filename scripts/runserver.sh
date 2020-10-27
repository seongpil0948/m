#!/bin/bash

echo "Start with runserver"
cd /app
python manage.py runserver 0.0.0.0:8000 --settings='m_back.settings.deploy'