from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from backend_app.src.database import get_db
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


def init_app(app):
    app.include_router(router)
    logger.info("Health check route registered at /health")
