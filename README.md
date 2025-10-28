# Capacity Task

## Requirements

- **Node.js**: 20.19+ or 22.12+
- **Docker**: Latest version
- **Docker Compose**: Latest version

## Setup

1. Create environment file:
```bash
cp .env.example .env
```

## Quick Start

**IMPORTANT: Requires 2 terminals**

### Terminal 1 - Backend:
```bash
./scripts/run_backend_app.sh
```

First run automatically builds, migrates, and seeds. Takes up to 10 minutes.

Backend API: Configured via API_URL and API_PORT in .env
Health check: {API_URL}:{API_PORT}/health

### Terminal 2 - Frontend:
```bash
./scripts/run_frontend_app.sh
```

Frontend: Configured via API_URL and FRONTEND_PORT in .env

## Services

- PostgreSQL: 5433
- Redis: 6380
- Backend API: 8001
- Frontend: 3001

## Testing

```bash
./scripts/run_tests.sh
```

## Common Commands

```bash
./scripts/run_backend_app.sh --build
docker-compose logs -f backend
docker-compose exec backend alembic revision --autogenerate -m "msg"
docker-compose down -v
```
