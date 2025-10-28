import json
import logging
import os
from typing import Any, Optional

import redis.asyncio as redis

logger = logging.getLogger(__name__)


class CacheMemory:
    def __init__(self):
        redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
        self._client = redis.from_url(redis_url, decode_responses=True)
        logger.info(f"CacheMemory initialized with Redis at {redis_url}")

    async def ping(self) -> bool:
        try:
            await self._client.ping()
            return True
        except Exception as e:
            logger.error(f"Cache ping failed: {e}")
            return False

    async def get(self, key: str) -> Optional[str]:
        return await self._client.get(key)

    async def set(self, key: str, value: str, ttl: Optional[int] = None) -> None:
        await self._client.set(key, value, ex=ttl)

    async def get_json(self, key: str) -> Optional[Any]:
        value = await self._client.get(key)
        if value:
            return json.loads(value)
        return None

    async def set_json(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        await self._client.set(key, json.dumps(value), ex=ttl)

    async def delete(self, *keys: str) -> int:
        if not keys:
            return 0
        return await self._client.delete(*keys)

    async def close(self) -> None:
        await self._client.close()
        logger.info("CacheMemory connection closed")
