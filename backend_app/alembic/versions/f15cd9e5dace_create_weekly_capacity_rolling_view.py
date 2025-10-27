"""create_weekly_capacity_rolling_view

Revision ID: f15cd9e5dace
Revises: 6f3e87163450
Create Date: 2025-10-27 12:28:16.158436

"""

from typing import Sequence, Union

from alembic import op

revision: str = "f15cd9e5dace"
down_revision: Union[str, None] = "6f3e87163450"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE MATERIALIZED VIEW weekly_capacity_rolling AS
        WITH weekly_capacity AS (
            SELECT
                corridor,
                week_start_date,
                week_no,
                SUM(capacity_teu) as total_capacity_teu
            FROM voyages
            GROUP BY corridor, week_start_date, week_no
        ),
        rolling_4week AS (
            SELECT
                corridor,
                week_start_date,
                week_no,
                total_capacity_teu,
                ROUND(AVG(total_capacity_teu) OVER (
                    PARTITION BY corridor
                    ORDER BY week_start_date
                    ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
                ))::INTEGER as offered_capacity_teu_4week
            FROM weekly_capacity
        ),
        rolling_8week AS (
            SELECT
                corridor,
                week_start_date,
                week_no,
                total_capacity_teu,
                offered_capacity_teu_4week,
                ROUND(AVG(total_capacity_teu) OVER (
                    PARTITION BY corridor
                    ORDER BY week_start_date
                    ROWS BETWEEN 7 PRECEDING AND CURRENT ROW
                ))::INTEGER as offered_capacity_teu_8week
            FROM rolling_4week
        )
        SELECT
            corridor,
            week_start_date,
            week_no,
            total_capacity_teu,
            offered_capacity_teu_4week,
            offered_capacity_teu_8week
        FROM rolling_8week
    """)

    op.execute("""
        CREATE UNIQUE INDEX idx_weekly_capacity_rolling_pk
        ON weekly_capacity_rolling (corridor, week_start_date, week_no)
    """)


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS idx_weekly_capacity_rolling_pk")

    op.execute("DROP MATERIALIZED VIEW IF EXISTS weekly_capacity_rolling")
