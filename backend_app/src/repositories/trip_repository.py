from sqlalchemy.ext.asyncio import AsyncSession
from backend_app.src.models import Trip


class TripRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, trip_data: dict) -> Trip:
        trip = Trip(**trip_data)
        self.db.add(trip)
        await self.db.flush()
        return trip
