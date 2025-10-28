#!/bin/bash
set -e

if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

export VITE_API_URL="${API_URL}"
export VITE_API_PORT="${API_PORT}"

if [ ! -d "frontend_app/node_modules" ]; then
    cd frontend_app && npm install && cd ..
fi

echo ""
echo "Frontend: ${API_URL}:${FRONTEND_PORT}"
echo ""

cd frontend_app && npm run dev
