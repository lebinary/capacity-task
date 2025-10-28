from datetime import datetime, timedelta
from typing import Dict, List

from sqlalchemy.ext.asyncio import AsyncSession

from backend_app.src.cache import CacheMemory
from backend_app.src.models import TripModel, VoyageModel
from backend_app.src.repositories import TripRepository, VoyageRepository
from backend_app.src.schemas import (
    TripSchemaCreate,
    VoyageSchemaCreate,
    VoyageSchemaUpdate,
    WeekInfo,
)


class VoyageService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.voyage_repo = VoyageRepository(db)
        self.trip_repo = TripRepository(db)

    async def add_trip_and_voyage(
        self, trip_data: TripSchemaCreate, voyage_data: VoyageSchemaCreate
    ) -> tuple[TripModel, VoyageModel]:
        voyage = await self.voyage_repo.find_by_composite_key(
            service_version_roundtrip=voyage_data.service_version_roundtrip,
            origin_service_master=voyage_data.origin_service_master,
            dest_service_master=voyage_data.dest_service_master,
        )

        if voyage:
            if voyage_data.latest_origin_departure > voyage.latest_origin_departure:
                update_data = VoyageSchemaUpdate(
                    latest_origin_departure=voyage_data.latest_origin_departure,
                    week_start_date=voyage_data.week_start_date,
                    week_no=voyage_data.week_no,
                    capacity_teu=voyage_data.capacity_teu,
                )
                voyage = await self.voyage_repo.update(voyage, update_data)
        else:
            voyage = await self.voyage_repo.create(voyage_data)

        trip_data_dict = trip_data.model_dump()
        trip_data_dict["voyage_id"] = voyage.id
        trip = await self.trip_repo.create(trip_data_dict)

        await self.db.commit()
        return trip, voyage

    async def get_rolling_average_capacity(
        self,
        date_from: datetime,
        date_to: datetime,
        cache: CacheMemory,
        corridor: str = "china_main-north_europe_main",
        n_weeks: int = 4,
    ) -> List[Dict]:
        cache_key = f"capacity:{corridor}:{date_from.date()}:{date_to.date()}:{n_weeks}"

        cached = await cache.get_json(cache_key)
        if cached:
            return cached

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

        await cache.set_json(cache_key, data, ttl=3600)

        return data

    @staticmethod
    def calculate_week_info(origin_at_utc: datetime) -> WeekInfo:
        week_start = origin_at_utc - timedelta(days=origin_at_utc.weekday())
        week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
        week_no = week_start.isocalendar()[1]
        return WeekInfo(week_start_date=week_start, week_no=week_no)
