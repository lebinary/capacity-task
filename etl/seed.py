import csv
import os
import sys
from datetime import datetime
import asyncio

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend_app.src.database import AsyncSessionLocal
from backend_app.src.services.voyage_service import VoyageDataService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_csv_row(row: dict) -> tuple[dict, dict]:
    origin_at_utc = datetime.strptime(row["ORIGIN_AT_UTC"], "%Y-%m-%d %H:%M:%S.%f")

    service_version_roundtrip = row["SERVICE_VERSION_AND_ROUNDTRIP_IDENTFIERS"]
    origin_service_master = row["ORIGIN_SERVICE_VERSION_AND_MASTER"]
    dest_service_master = row["DESTINATION_SERVICE_VERSION_AND_MASTER"]

    corridor = f"{row['ORIGIN']}-{row['DESTINATION']}"
    capacity_teu = int(row["OFFERED_CAPACITY_TEU"])

    week_info = VoyageDataService.calculate_week_info(origin_at_utc)

    trip_data = {
        "origin": row["ORIGIN"],
        "destination": row["DESTINATION"],
        "origin_port_code": row["ORIGIN_PORT_CODE"],
        "destination_port_code": row["DESTINATION_PORT_CODE"],
        "origin_at_utc": origin_at_utc,
        "offered_capacity_teu": capacity_teu
    }

    voyage_data = {
        "service_version_roundtrip": service_version_roundtrip,
        "origin_service_master": origin_service_master,
        "dest_service_master": dest_service_master,
        "corridor": corridor,
        "latest_origin_departure": origin_at_utc,
        "week_start_date": week_info["week_start_date"],
        "week_no": week_info["week_no"],
        "capacity_teu": capacity_teu
    }

    return trip_data, voyage_data


async def seed_database(csv_path: str):
    async with AsyncSessionLocal() as db:
        service = VoyageDataService(db)

        try:
            with open(csv_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                total_rows = 0

                for row in reader:
                    try:
                        trip_data, voyage_data = parse_csv_row(row)
                        await service.add_trip(trip_data, voyage_data)
                        total_rows += 1

                        if total_rows % 100 == 0:
                            logger.info(f"Processed {total_rows} rows")

                    except Exception as e:
                        logger.error(f"Error processing row {total_rows + 1}: {e}")
                        await db.rollback()
                        continue

                logger.info(f"Seeding complete. Total rows processed: {total_rows}")

        except Exception as e:
            logger.error(f"Fatal error during seeding: {e}")
            await db.rollback()
            raise


if __name__ == "__main__":
    csv_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "raw_data",
        "sailing_level_raw.csv"
    )

    if not os.path.exists(csv_path):
        logger.error(f"CSV file not found at: {csv_path}")
        sys.exit(1)

    logger.info(f"Starting database seed from: {csv_path}")
    asyncio.run(seed_database(csv_path))
