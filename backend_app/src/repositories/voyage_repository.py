from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select
from backend_app.src.models import Voyage
from datetime import datetime
from typing import Optional


class VoyageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_by_composite_key(
        self,
        service_version_roundtrip: str,
        origin_service_master: str,
        dest_service_master: str
    ) -> Optional[Voyage]:
        stmt = select(Voyage).where(
            and_(
                Voyage.service_version_roundtrip == service_version_roundtrip,
                Voyage.origin_service_master == origin_service_master,
                Voyage.dest_service_master == dest_service_master
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def create(self, voyage_data: dict) -> Voyage:
        voyage = Voyage(**voyage_data)
        self.db.add(voyage)
        await self.db.flush()
        return voyage

    async def update(self, voyage: Voyage, voyage_data: dict) -> Voyage:
        for key, value in voyage_data.items():
            setattr(voyage, key, value)
        await self.db.flush()
        return voyage
