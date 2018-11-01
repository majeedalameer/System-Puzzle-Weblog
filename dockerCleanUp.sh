#!/bin/bash

# Stop all running containers
docker stop $(docker ps -aq)

# Remove all containers
docker rm $(docker ps -aq)

# Remove all images
docker image rm system-puzzle-weblog_ingestion
docker image rm system-puzzle-weblog_processing
docker image rm system-puzzle-weblog_flaskapp
