from sqlalchemy.ext.asyncio import AsyncSession
from backend_app.src.repositories.voyage_repository import VoyageRepository
from backend_app.src.repositories.trip_repository import TripRepository
from datetime import datetime, timedelta


class VoyageDataService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.voyage_repo = VoyageRepository(db)
        self.trip_repo = TripRepository(db)

    async def add_trip(self, trip_data: dict, voyage_data: dict) -> tuple:
        voyage = await self.voyage_repo.find_by_composite_key(
            service_version_roundtrip=voyage_data["service_version_roundtrip"],
            origin_service_master=voyage_data["origin_service_master"],
            dest_service_master=voyage_data["dest_service_master"]
        )

        if voyage:
            if voyage_data["latest_origin_departure"] > voyage.latest_origin_departure:
                voyage = await self.voyage_repo.update(voyage, voyage_data)
        else:
            voyage = await self.voyage_repo.create(voyage_data)

        trip_data["voyage_id"] = voyage.id
        trip = await self.trip_repo.create(trip_data)

        await self.db.commit()
        return trip, voyage

    @staticmethod
    def calculate_week_info(origin_at_utc: datetime) -> dict:
        week_start = origin_at_utc - timedelta(days=origin_at_utc.weekday())
        week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
        week_no = week_start.isocalendar()[1]
        return {
            "week_start_date": week_start,
            "week_no": week_no
        }
