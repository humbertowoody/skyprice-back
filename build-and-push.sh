#!/bin/bash
# Script para construir las imágenes de Docker y subirlas a Docker Hub

# Definir la URL de la imagen en Docker Hub
DOCKER_URL="humbertowoody/skyprice-api"
printf "Docker URL: $DOCKER_URL\n"

# Construir la imagen base
docker buildx build --platform linux/arm64,linux/amd64  --cache-from $DOCKER_URL-builder:latest --cache-to=type=inline --progress plain -t $DOCKER_URL-builder:latest --target builder .

# Construir la imagen de ejecución
docker buildx build --platform linux/arm64,linux/amd64 --cache-from $DOCKER_URL-builder:latest --cache-from $DOCKER_URL:latest --cache-to=type=inline --progress plain -t $DOCKER_URL:latest --target run .

# Subir la imagen a Docker Hub
docker push $DOCKER_URL:latest
