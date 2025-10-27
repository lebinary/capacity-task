from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TripSchemaCreate(BaseModel):
    origin: str
    destination: str
    origin_port_code: str
    destination_port_code: str
    origin_at_utc: datetime
    offered_capacity_teu: int

    model_config = ConfigDict(from_attributes=True)


class TripSchemaResponse(BaseModel):
    id: int
    voyage_id: int
    origin: str
    destination: str
    origin_port_code: str
    destination_port_code: str
    origin_at_utc: datetime
    offered_capacity_teu: int

    model_config = ConfigDict(from_attributes=True)
