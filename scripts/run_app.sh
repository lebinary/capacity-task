#!/bin/bash
set -euxo pipefail

if [ -z "${DATABASE_URL:-}" ]; then
    echo "DATABASE_URL is not set. Please check your .env file."
    exit 1
fi

alembic upgrade head

python backend_app/main.py
