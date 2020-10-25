#!/bin/bash

echo "Starting docker-compose"
docker build -t porsche .
docker-compose up -d