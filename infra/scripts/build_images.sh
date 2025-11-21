#!/bin/bash
# Script to build KALDRA Docker images
# Placeholder - basic implementation

set -e

echo "Building KALDRA Docker images..."

docker build -f infra/docker/Dockerfile.core -t kaldra-core:dev .
docker build -f infra/docker/Dockerfile.api -t kaldra-api:dev .

echo "KALDRA Docker images built successfully."
