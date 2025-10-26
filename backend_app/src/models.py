from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, Index
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


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, autoincrement=True)
    voyage_id = Column(Integer, ForeignKey("voyages.id"), nullable=False, index=True)
    origin = Column(String, nullable=False, index=True)
    destination = Column(String, nullable=False)
    origin_port_code = Column(String, nullable=False)
    destination_port_code = Column(String, nullable=False)
    origin_at_utc = Column(DateTime, nullable=False)
    offered_capacity_teu = Column(Integer, nullable=False)

    voyage = relationship("Voyage", back_populates="trips")
