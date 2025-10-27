from datetime import datetime

from pydantic import BaseModel, ConfigDict


class VoyageSchemaCreate(BaseModel):
    service_version_roundtrip: str
    origin_service_master: str
    dest_service_master: str
    corridor: str
    latest_origin_departure: datetime
    week_start_date: datetime
    week_no: int
    capacity_teu: int

    model_config = ConfigDict(from_attributes=True)


class VoyageSchemaUpdate(BaseModel):
    latest_origin_departure: datetime
    week_start_date: datetime
    week_no: int
    capacity_teu: int

    model_config = ConfigDict(from_attributes=True)


class WeekInfo(BaseModel):
    week_start_date: datetime
    week_no: int


class CapacityRow(BaseModel):
    week_start_date: datetime
    week_no: int
    offered_capacity_teu: int

    model_config = ConfigDict(from_attributes=True)
