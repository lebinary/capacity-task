from datetime import datetime
from typing import List, Optional

from sqlalchemy import and_, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from backend_app.src.models import Voyage


class VoyageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_by_composite_key(
        self,
        service_version_roundtrip: str,
        origin_service_master: str,
        dest_service_master: str,
    ) -> Optional[Voyage]:
        stmt = select(Voyage).where(
            and_(
                Voyage.service_version_roundtrip == service_version_roundtrip,
                Voyage.origin_service_master == origin_service_master,
                Voyage.dest_service_master == dest_service_master,
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

    async def get_rolling_average_capacity(
        self, date_from: datetime, date_to: datetime, corridor: str, n_weeks: int
    ) -> List[tuple]:
        query = text("""
            WITH weekly_capacity AS (
                SELECT
                    week_start_date,
                    week_no,
                    SUM(capacity_teu) as total_capacity_teu
                FROM voyages
                WHERE corridor = :corridor
                GROUP BY week_start_date, week_no
            ),
            rolling_avg AS (
                SELECT
                    week_start_date,
                    week_no,
                    ROUND(AVG(total_capacity_teu) OVER (
                        ORDER BY week_start_date
                        ROWS BETWEEN :n_weeks - 1 PRECEDING AND CURRENT ROW
                    ))::INTEGER as offered_capacity_teu
                FROM weekly_capacity
            )
            SELECT
                week_start_date,
                week_no,
                offered_capacity_teu
            FROM rolling_avg
            WHERE week_start_date >= :date_from
              AND week_start_date <= :date_to
            ORDER BY week_start_date
        """)

        result = await self.db.execute(
            query,
            {
                "corridor": corridor,
                "date_from": date_from,
                "date_to": date_to,
                "n_weeks": n_weeks,
            },
        )

        return result.fetchall()
