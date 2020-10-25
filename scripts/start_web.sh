#!/bin/bash

echo "Starting web"
./scripts/migrate.sh
./scripts/gunicorn.sh