from typing import Any, Dict

from sqlalchemy.ext.asyncio import AsyncSession

from backend_app.src.models import TripModel


class TripRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, trip_data: Dict[str, Any]) -> TripModel:
        trip = TripModel(**trip_data)
        self.db.add(trip)
        await self.db.flush()
        return trip
