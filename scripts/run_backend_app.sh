#!/bin/bash
set -e

if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

cleanup() {
    docker-compose down
    exit 0
}

trap cleanup INT TERM

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
fi

if [ "$BUILD_FLAG" = true ] || [ "$FIRST_RUN" = true ]; then
    docker-compose down -v
    docker-compose up --build -d

    until docker-compose exec -T db pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB" > /dev/null 2>&1; do
        sleep 5
    done

    docker-compose exec backend alembic upgrade head
    docker-compose exec backend python backend_app/etl/seed.py
else
    docker-compose up -d
fi

echo ""
echo "Backend API: ${API_URL}:${API_PORT}"
echo ""

docker-compose logs -f backend
