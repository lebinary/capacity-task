#!/bin/bash
set -e

# Load environment variables
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

trap 'echo "Shutting down..."; docker-compose down; exit 0' INT TERM

BUILD_FLAG=false

for arg in "$@"; do
    if [ "$arg" == "--build" ]; then
        BUILD_FLAG=true
    fi
done

if docker images | grep -q "capacity_backend"; then
    FIRST_RUN=false
else
    FIRST_RUN=true
    echo "First run detected, will build and seed..."
fi

if [ "$BUILD_FLAG" = true ] || [ "$FIRST_RUN" = true ]; then
    echo "Building from scratch..."
    docker-compose down -v
    docker-compose up --build -d

    until docker-compose exec -T db pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB" > /dev/null 2>&1; do
        echo "Waiting for database to be ready..."
        sleep 5
    done

    echo "Running migrations..."
    docker-compose exec backend alembic upgrade head

    echo "Seeding database..."
    docker-compose exec backend python backend_app/etl/seed.py

    echo "Build complete. Showing logs..."
    docker-compose logs -f backend
else
    echo "Starting services..."
    docker-compose up
fi
