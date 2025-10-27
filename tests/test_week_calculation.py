import pytest
from datetime import datetime
from backend_app.src.services.voyage_service import VoyageService


def test_calculate_week_info_monday():
    origin_at_utc = datetime(2024, 4, 15, 10, 30, 45)
    week_info = VoyageService.calculate_week_info(origin_at_utc)

    assert week_info["week_start_date"] == datetime(2024, 4, 15, 0, 0, 0)
    assert week_info["week_no"] == 16


def test_calculate_week_info_sunday():
    origin_at_utc = datetime(2024, 4, 21, 23, 59, 59)
    week_info = VoyageService.calculate_week_info(origin_at_utc)

    assert week_info["week_start_date"] == datetime(2024, 4, 15, 0, 0, 0)
    assert week_info["week_no"] == 16


def test_calculate_week_info_wednesday():
    origin_at_utc = datetime(2024, 4, 18, 22, 0, 0)
    week_info = VoyageService.calculate_week_info(origin_at_utc)

    assert week_info["week_start_date"] == datetime(2024, 4, 15, 0, 0, 0)
    assert week_info["week_no"] == 16


def test_calculate_week_info_year_boundary():
    origin_at_utc = datetime(2024, 1, 3, 12, 0, 0)
    week_info = VoyageService.calculate_week_info(origin_at_utc)

    assert week_info["week_start_date"] == datetime(2024, 1, 1, 0, 0, 0)
    assert week_info["week_no"] == 1


def test_calculate_week_info_different_week():
    origin_at_utc = datetime(2024, 4, 27, 5, 5, 0)
    week_info = VoyageService.calculate_week_info(origin_at_utc)

    assert week_info["week_start_date"] == datetime(2024, 4, 22, 0, 0, 0)
    assert week_info["week_no"] == 17
