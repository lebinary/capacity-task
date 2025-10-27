from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from backend_app.src.database import Base


class Voyage(Base):
    __tablename__ = "voyages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_version_roundtrip = Column(String, nullable=False)
    origin_service_master = Column(String, nullable=False)
    dest_service_master = Column(String, nullable=False)
    corridor = Column(String, nullable=False, index=True)
    latest_origin_departure = Column(DateTime, nullable=False)
    week_start_date = Column(DateTime, nullable=False, index=True)
    week_no = Column(Integer, nullable=False)
    capacity_teu = Column(Integer, nullable=False)

    trips = relationship("Trip", back_populates="voyage")

    __table_args__ = (
        UniqueConstraint(
            "service_version_roundtrip",
            "origin_service_master",
            "dest_service_master",
            name="uq_voyage_composite"
        ),
        Index("ix_voyages_corridor_week", "corridor", "week_start_date"),
    )
