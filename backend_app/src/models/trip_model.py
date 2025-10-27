from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend_app.src.database import Base


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
