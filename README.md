# Capacity Task

## Quick Start

```bash
./scripts/run_app.sh
```

First run automatically builds, migrates, and seeds. Takes up to `10 minutes`.

Access: http://localhost:8001/health

## Services

- PostgreSQL: 5433
- Redis: 6380
- FastAPI: 8001

## Testing

```bash
./scripts/run_tests.sh
```

## Common Commands

```bash
./scripts/run_app.sh --build
docker-compose logs -f backend
docker-compose exec backend alembic revision --autogenerate -m "msg"
docker-compose down -v
```
