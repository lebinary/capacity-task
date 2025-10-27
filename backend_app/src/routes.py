from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from backend_app.src.database import get_db, get_redis
from backend_app.src.services.voyage_service import VoyageService
from datetime import datetime
import redis.asyncio as redis
import os
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    health_status = {
        "status": "healthy",
        "database": "disconnected",
        "redis": "disconnected",
        "last_etl_run": None
    }

    try:
        await db.execute(text("SELECT 1"))
        health_status["database"] = "connected"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        health_status["database"] = "error"
        health_status["status"] = "unhealthy"

    try:
        redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
        r = redis.from_url(redis_url)
        await r.ping()
        health_status["redis"] = "connected"

        last_etl = await r.get("last_etl_run")
        if last_etl:
            health_status["last_etl_run"] = last_etl.decode('utf-8')
        await r.close()
    except Exception as e:
        logger.error(f"Redis health check failed: {e}")
        health_status["redis"] = "error"

    return health_status


@router.get("/capacity")
async def get_capacity(
    date_from: str = Query(..., description="Start date in YYYY-MM-DD format"),
    date_to: str = Query(..., description="End date in YYYY-MM-DD format"),
    corridor: str = Query("china_main-north_europe_main", description="Shipping corridor"),
    n_weeks: int = Query(4, description="Rolling average window size"),
    db: AsyncSession = Depends(get_db),
    redis: redis.Redis = Depends(get_redis)
):
    try:
        date_from_dt = datetime.strptime(date_from, "%Y-%m-%d")
        date_to_dt = datetime.strptime(date_to, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    if date_from_dt > date_to_dt:
        raise HTTPException(status_code=400, detail="date_from must be before or equal to date_to")

    service = VoyageService(db)
    results = await service.get_rolling_average_capacity(
        date_from=date_from_dt,
        date_to=date_to_dt,
        redis_client=redis,
        corridor=corridor,
        n_weeks=n_weeks
    )

    return results


def init_app(app):
    app.include_router(router)
    logger.info("Health check route registered at /health")
