#!/bin/bash

echo "Starting web"
cd /app
./scripts/migrate.sh
./scripts/gunicorn.sh