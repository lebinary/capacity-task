# Capacity Task

## Quick Start

```bash
docker-compose up --build
```

Initial setup may take up to `10 minutes` depending on internet speed.

Access: http://localhost:8001/health

## Services

- PostgreSQL: 5433
- Redis: 6380
- FastAPI: 8001

## Common Commands

```bash
docker-compose logs -f backend
docker-compose exec backend alembic revision --autogenerate -m "msg"
docker-compose down -v
```

## Local Development

```bash
pip install -r requirements.txt
alembic upgrade head
python backend_app/main.py
```
