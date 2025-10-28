from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from backend_app.src.cache import CacheMemory
from backend_app.src.database import AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as db:
        try:
            yield db
        except Exception:
            await db.rollback()
            raise
        finally:
            await db.close()


async def get_cache() -> AsyncGenerator[CacheMemory, None]:
    cache = CacheMemory()
    try:
        yield cache
    finally:
        await cache.close()
