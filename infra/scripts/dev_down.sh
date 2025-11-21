#!/bin/bash
# Script to stop KALDRA development environment
# Placeholder - basic implementation

set -e

echo "Stopping KALDRA development environment..."

docker compose -f infra/docker/docker-compose.dev.yml down

echo "KALDRA development environment stopped."
