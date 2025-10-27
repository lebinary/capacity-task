import os
from datetime import datetime
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from backend_app.src.database import Base
from backend_app.src.services.voyage_service import VoyageService

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
if not TEST_DATABASE_URL:
    raise ValueError("TEST_DATABASE_URL environment variable is not set")


@pytest_asyncio.fixture(scope="function")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()


async def get_test_db(engine):
    async_session = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as db:
        try:
            yield db
        except:
            await db.rollback()
            raise
        finally:
            await db.close()


@pytest_asyncio.fixture(scope="function")
async def test_db_session(test_engine):
    async for session in get_test_db(test_engine):
        yield session


@pytest.fixture
def make_trip_data():
    def _make(
        origin_at_utc=None, capacity=24136, origin_port="CNYTN", dest_port="DEHAM"
    ):
        return {
            "origin": "china_main",
            "destination": "north_europe_main",
            "origin_port_code": origin_port,
            "destination_port_code": dest_port,
            "origin_at_utc": origin_at_utc or datetime(2024, 4, 18, 22, 0, 0),
            "offered_capacity_teu": capacity,
        }

    return _make


@pytest.fixture
def make_voyage_data():
    def _make(
        origin_at_utc=None,
        capacity=24136,
        service_roundtrip="ONE INSPIRATION | 27442.000000000 | v16-s14 | v16-s14 | 2 - 2",
        service_master="THEA - FE3 || HL - FE3 | HMM - FE3 | ONE - FE3 | YML - FE3",
    ):
        dt = origin_at_utc or datetime(2024, 4, 18, 22, 0, 0)
        week_info = VoyageService.calculate_week_info(dt)

        return {
            "service_version_roundtrip": service_roundtrip,
            "origin_service_master": service_master,
            "dest_service_master": service_master,
            "corridor": "china_main-north_europe_main",
            "latest_origin_departure": dt,
            "week_start_date": week_info["week_start_date"],
            "week_no": week_info["week_no"],
            "capacity_teu": capacity,
        }

    return _make


@pytest.fixture
def mock_redis():
    mock = AsyncMock()
    mock.get.return_value = None
    mock.setex.return_value = True
    return mock


@pytest_asyncio.fixture
async def refresh_materialized_view(test_db_session):
    async def _refresh():
        try:
            await test_db_session.execute(
                text("REFRESH MATERIALIZED VIEW CONCURRENTLY weekly_capacity_rolling")
            )
            await test_db_session.commit()
        except Exception:
            pass

    return _refresh
