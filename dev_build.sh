#!/bin/sh
docker compose -f docker-compose.yml down
cd app/
tailwindcss -i ./static/src/main.css -o ./static/dist/main.css --minify
cd ..
docker compose -f docker-compose.yml up -d --build