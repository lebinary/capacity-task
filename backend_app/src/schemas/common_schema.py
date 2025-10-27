from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    database: str
    redis: str
    last_etl_run: str | None
