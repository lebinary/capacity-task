from datetime import datetime
from typing import List, Optional

from sqlalchemy import and_, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from backend_app.src.models import VoyageModel
from backend_app.src.schemas import CapacityRow, VoyageSchemaCreate, VoyageSchemaUpdate


class VoyageRepository:
    MATERIALIZED_VIEW_COLUMNS = {
        4: "offered_capacity_teu_4week",
        8: "offered_capacity_teu_8week",
    }

    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_by_composite_key(
        self,
        service_version_roundtrip: str,
        origin_service_master: str,
        dest_service_master: str,
    ) -> Optional[VoyageModel]:
        stmt = select(VoyageModel).where(
            and_(
                VoyageModel.service_version_roundtrip == service_version_roundtrip,
                VoyageModel.origin_service_master == origin_service_master,
                VoyageModel.dest_service_master == dest_service_master,
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def create(self, voyage_data: VoyageSchemaCreate) -> VoyageModel:
        voyage = VoyageModel(**voyage_data.model_dump())
        self.db.add(voyage)
        await self.db.flush()
        return voyage

    async def update(self, voyage: VoyageModel, voyage_data: VoyageSchemaUpdate) -> VoyageModel:
        voyage.latest_origin_departure = voyage_data.latest_origin_departure
        voyage.week_start_date = voyage_data.week_start_date
        voyage.week_no = voyage_data.week_no
        voyage.capacity_teu = voyage_data.capacity_teu
        await self.db.flush()
        return voyage

    async def _get_capacity_from_materialized_view(
        self, date_from: datetime, date_to: datetime, corridor: str, n_weeks: int
    ) -> List[tuple]:
        if n_weeks not in self.MATERIALIZED_VIEW_COLUMNS:
            return []

        column = self.MATERIALIZED_VIEW_COLUMNS[n_weeks]

        query = text(f"""
            SELECT
                week_start_date,
                week_no,
                {column} as offered_capacity_teu
            FROM weekly_capacity_rolling
            WHERE corridor = :corridor
              AND week_start_date >= :date_from
              AND week_start_date <= :date_to
            ORDER BY week_start_date
        """)

        try:
            result = await self.db.execute(
                query,
                {
                    "corridor": corridor,
                    "date_from": date_from,
                    "date_to": date_to,
                },
            )
            return result.fetchall()
        except Exception:
            await self.db.rollback()
            return []

    async def _get_capacity_from_cte(
        self, date_from: datetime, date_to: datetime, corridor: str, n_weeks: int
    ) -> List[tuple]:
        query = text(f"""
            WITH weekly_capacity AS (
                SELECT
                    week_start_date,
                    week_no,
                    SUM(capacity_teu) as total_capacity_teu
                FROM {VoyageModel.__tablename__}
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

    async def get_rolling_average_capacity(
        self, date_from: datetime, date_to: datetime, corridor: str, n_weeks: int
    ) -> List[CapacityRow]:
        rows = await self._get_capacity_from_materialized_view(
            date_from, date_to, corridor, n_weeks
        )

        if rows:
            return [
                CapacityRow(
                    week_start_date=row.week_start_date,
                    week_no=row.week_no,
                    offered_capacity_teu=row.offered_capacity_teu,
                )
                for row in rows
            ]

        rows = await self._get_capacity_from_cte(date_from, date_to, corridor, n_weeks)
        return [
            CapacityRow(
                week_start_date=row.week_start_date,
                week_no=row.week_no,
                offered_capacity_teu=row.offered_capacity_teu,
            )
            for row in rows
        ]
