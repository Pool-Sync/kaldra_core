#!/bin/bash
# Script to start KALDRA development environment
# Placeholder - basic implementation

set -e

echo "Starting KALDRA development environment..."

docker compose -f infra/docker/docker-compose.dev.yml up --build

echo "KALDRA development environment started."
