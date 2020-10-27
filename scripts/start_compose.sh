#!/bin/bash

echo "Starting docker-compose"
cd /app
docker build -t porsche .
docker-compose up -d