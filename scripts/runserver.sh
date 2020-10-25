#!/bin/bash

echo "Start with runserver"
python manage.py runserver 0.0.0.0:8000 --settings='m_back.settings.deploy'