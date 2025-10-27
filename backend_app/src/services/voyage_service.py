import json
from datetime import datetime, timedelta
from typing import Dict, List

import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession

from backend_app.src.repositories.trip_repository import TripRepository
from backend_app.src.repositories.voyage_repository import VoyageRepository


class VoyageService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.voyage_repo = VoyageRepository(db)
        self.trip_repo = TripRepository(db)

    async def add_trip(self, trip_data: dict, voyage_data: dict) -> tuple:
        voyage = await self.voyage_repo.find_by_composite_key(
            service_version_roundtrip=voyage_data["service_version_roundtrip"],
            origin_service_master=voyage_data["origin_service_master"],
            dest_service_master=voyage_data["dest_service_master"],
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

    async def get_rolling_average_capacity(
        self,
        date_from: datetime,
        date_to: datetime,
        redis_client: redis.Redis,
        corridor: str = "china_main-north_europe_main",
        n_weeks: int = 4,
    ) -> List[Dict]:
        cache_key = f"capacity:{corridor}:{date_from.date()}:{date_to.date()}:{n_weeks}"
        cached = await redis_client.get(cache_key)
        if cached:
            return json.loads(cached)

        rows = await self.voyage_repo.get_rolling_average_capacity(
            date_from=date_from, date_to=date_to, corridor=corridor, n_weeks=n_weeks
        )

        data = [
            {
                "week_start_date": row.week_start_date.strftime("%Y-%m-%d"),
                "week_no": row.week_no,
                "offered_capacity_teu": row.offered_capacity_teu,
            }
            for row in rows
        ]

        await redis_client.setex(
            cache_key,
            3600,
            json.dumps(data),
        )

        return data

    @staticmethod
    def calculate_week_info(origin_at_utc: datetime) -> dict:
        week_start = origin_at_utc - timedelta(days=origin_at_utc.weekday())
        week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
        week_no = week_start.isocalendar()[1]
        return {"week_start_date": week_start, "week_no": week_no}
