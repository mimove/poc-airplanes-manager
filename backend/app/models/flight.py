from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.airplane import Airplane
    from app.models.flight_passenger import FlightPassenger


class Flight(Base):
    __tablename__ = "flights"

    flight_id: Mapped[str] = mapped_column(String(20), primary_key=True)
    plate_number: Mapped[str] = mapped_column(ForeignKey("airplanes.plate_number"))
    arrival_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    departure_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    fuel_consumption: Mapped[int] = mapped_column(Integer)
    occupied_seats: Mapped[int] = mapped_column(Integer)
    origin: Mapped[str] = mapped_column(String(100))
    destination: Mapped[str] = mapped_column(String(100))

    airplane: Mapped["Airplane"] = relationship(back_populates="flights")
    flight_passengers: Mapped[list["FlightPassenger"]] = relationship(
        back_populates="flight"
    )
