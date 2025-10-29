# Capacity Task

**Time to Complete: ~15 hours**

## Prerequisites

Before starting, verify you have:

- **Node.js**: 20.19+ or 22.12+
- **Docker**: Latest version
- **Docker Compose**: Latest version

Check versions:
```bash
node --version
docker --version
docker-compose --version
```

## First-Time Setup

### Step 1: Create Environment File

```bash
cp .env.example .env
```

The `.env` file contains configuration for:
- PostgreSQL (port 5433)
- Redis (port 6380)
- Backend API (port 8001)
- Frontend (port 3001)

### Step 2: Start Backend (Terminal 1)

```bash
./scripts/run_backend_app.sh
```

**First run will automatically:**
1. Build Docker images (backend, postgres, redis)
2. Wait for database health check
3. Run `alembic upgrade head` to create database tables
4. Run `python backend_app/etl/seed.py` to load CSV data into database

**This takes ~10 minutes on first run.**

Backend API: http://localhost:8001
Health check: http://localhost:8001/health

### Step 3: Start Frontend (Terminal 2)

**IMPORTANT: Open a new terminal window**

```bash
./scripts/run_frontend_app.sh
```

First run will automatically:
1. Install npm dependencies if `node_modules` doesn't exist
2. Start Vite dev server

Frontend: http://localhost:3001

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

### Rebuild Backend
```bash
./scripts/run_backend_app.sh --build
```

### View Logs
```bash
docker-compose logs -f backend
```

### Create Database Migration
```bash
docker-compose exec backend alembic revision --autogenerate -m "description"
```

### Stop Services
```bash
docker-compose down
```

### Clean Start (removes all data)
```bash
docker-compose down -v                # Remove containers and volumes
docker rmi capacity_backend           # Remove backend image
rm -rf frontend_app/node_modules      # Remove node modules
# Then run setup steps again
```
