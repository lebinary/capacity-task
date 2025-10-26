#!/bin/bash
set -e

echo "Running tests..."
docker-compose exec backend pytest -v
