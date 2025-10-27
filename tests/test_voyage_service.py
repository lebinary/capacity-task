import pytest
from datetime import datetime
from backend_app.src.services.voyage_service import VoyageService
from backend_app.src.models import Voyage, Trip
from sqlalchemy import select


@pytest.mark.asyncio
async def test_create_new_voyage_and_trip(test_db_session, make_trip_data, make_voyage_data):
    service = VoyageService(test_db_session)

    trip_data = make_trip_data()
    voyage_data = make_voyage_data()

    trip, voyage = await service.add_trip(trip_data, voyage_data)

    assert trip.id is not None
    assert voyage.id is not None
    assert trip.voyage_id == voyage.id
    assert voyage.capacity_teu == 24136

    result = await test_db_session.execute(select(Voyage))
    assert len(result.scalars().all()) == 1

    result = await test_db_session.execute(select(Trip))
    assert len(result.scalars().all()) == 1


@pytest.mark.asyncio
async def test_upsert_voyage_with_newer_departure(test_db_session, make_trip_data, make_voyage_data):
    service = VoyageService(test_db_session)

    dt1 = datetime(2024, 4, 18, 22, 0, 0)
    trip1 = make_trip_data(origin_at_utc=dt1)
    voyage1 = make_voyage_data(origin_at_utc=dt1)

    trip_result1, voyage_result1 = await service.add_trip(trip1, voyage1)
    voyage_id_before = voyage_result1.id

    dt2 = datetime(2024, 4, 25, 10, 0, 0)
    trip2 = make_trip_data(origin_at_utc=dt2, capacity=30000, dest_port="NLRTM")
    voyage2 = make_voyage_data(origin_at_utc=dt2, capacity=30000)

    trip, voyage = await service.add_trip(trip2, voyage2)

    assert voyage.id == voyage_id_before
    assert voyage.latest_origin_departure == dt2
    assert voyage.capacity_teu == 30000

    result = await test_db_session.execute(select(Voyage))
    assert len(result.scalars().all()) == 1

    result = await test_db_session.execute(select(Trip))
    assert len(result.scalars().all()) == 2


@pytest.mark.asyncio
async def test_upsert_voyage_with_older_departure(test_db_session, make_trip_data, make_voyage_data):
    service = VoyageService(test_db_session)

    dt1 = datetime(2024, 4, 25, 10, 0, 0)
    trip1 = make_trip_data(origin_at_utc=dt1, capacity=30000)
    voyage1 = make_voyage_data(origin_at_utc=dt1, capacity=30000)

    trip_result1, voyage_result1 = await service.add_trip(trip1, voyage1)
    voyage_id_before = voyage_result1.id

    dt2 = datetime(2024, 4, 18, 22, 0, 0)
    trip2 = make_trip_data(origin_at_utc=dt2, dest_port="NLRTM")
    voyage2 = make_voyage_data(origin_at_utc=dt2)

    trip, voyage = await service.add_trip(trip2, voyage2)

    assert voyage.id == voyage_id_before
    assert voyage.latest_origin_departure == dt1
    assert voyage.capacity_teu == 30000

    result = await test_db_session.execute(select(Voyage))
    voyages = result.scalars().all()
    assert len(voyages) == 1
    assert voyages[0].latest_origin_departure == dt1

    result = await test_db_session.execute(select(Trip))
    assert len(result.scalars().all()) == 2


@pytest.mark.asyncio
async def test_different_voyages_same_service_different_masters(test_db_session, make_trip_data, make_voyage_data):
    service = VoyageService(test_db_session)

    dt = datetime(2024, 4, 18, 22, 0, 0)

    trip1 = make_trip_data(origin_at_utc=dt)
    voyage1 = make_voyage_data(
        origin_at_utc=dt,
        service_master="THEA - FE3 || HL - FE3 | HMM - FE3"
    )

    await service.add_trip(trip1, voyage1)

    trip2 = make_trip_data(origin_at_utc=dt, capacity=15000)
    voyage2 = make_voyage_data(
        origin_at_utc=dt,
        capacity=15000,
        service_master="DIFFERENT - SERVICE"
    )

    await service.add_trip(trip2, voyage2)

    result = await test_db_session.execute(select(Voyage))
    assert len(result.scalars().all()) == 2

    result = await test_db_session.execute(select(Trip))
    assert len(result.scalars().all()) == 2


@pytest.mark.asyncio
async def test_get_rolling_average_capacity_empty_database(test_db_session, mock_redis):
    service = VoyageService(test_db_session)

    result = await service.get_rolling_average_capacity(
        date_from=datetime(2024, 1, 1),
        date_to=datetime(2024, 3, 31),
        redis_client=mock_redis
    )

    assert result == []
    mock_redis.get.assert_called_once()
    mock_redis.setex.assert_called_once()


@pytest.mark.asyncio
async def test_get_rolling_average_capacity_with_voyages(test_db_session, make_voyage_data, mock_redis):
    from backend_app.src.repositories.voyage_repository import VoyageRepository

    repo = VoyageRepository(test_db_session)

    await repo.create(make_voyage_data(
        origin_at_utc=datetime(2024, 1, 3),
        capacity=10000
    ))
    await repo.create(make_voyage_data(
        origin_at_utc=datetime(2024, 1, 4),
        capacity=15000,
        service_roundtrip="Different Service"
    ))

    await repo.create(make_voyage_data(
        origin_at_utc=datetime(2024, 1, 10),
        capacity=20000,
        service_roundtrip="Another Service"
    ))

    await test_db_session.commit()

    service = VoyageService(test_db_session)

    result = await service.get_rolling_average_capacity(
        date_from=datetime(2024, 1, 1),
        date_to=datetime(2024, 1, 31),
        redis_client=mock_redis
    )

    assert len(result) == 2
    assert result[0]["week_start_date"] == "2024-01-01"
    assert result[0]["offered_capacity_teu"] == 25000  # Week 1: avg(25000) = 25000
    assert result[1]["week_start_date"] == "2024-01-08"
    assert result[1]["offered_capacity_teu"] == 22500  # Week 2: avg(25000, 20000) = 22500


@pytest.mark.asyncio
async def test_get_rolling_average_capacity_date_filtering(test_db_session, make_voyage_data, mock_redis):
    from backend_app.src.repositories.voyage_repository import VoyageRepository

    repo = VoyageRepository(test_db_session)

    await repo.create(make_voyage_data(origin_at_utc=datetime(2024, 1, 1), capacity=10000))
    await repo.create(make_voyage_data(
        origin_at_utc=datetime(2024, 2, 1),
        capacity=20000,
        service_roundtrip="Feb Service"
    ))
    await repo.create(make_voyage_data(
        origin_at_utc=datetime(2024, 3, 1),
        capacity=30000,
        service_roundtrip="Mar Service"
    ))

    await test_db_session.commit()

    service = VoyageService(test_db_session)

    result = await service.get_rolling_average_capacity(
        date_from=datetime(2024, 2, 1),
        date_to=datetime(2024, 2, 29),
        redis_client=mock_redis
    )

    assert all("2024-02" in r["week_start_date"] or "2024-01-29" in r["week_start_date"] for r in result)
