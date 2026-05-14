from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.flight import Flight
    from app.models.passenger import Passenger


class FlightPassenger(Base):
    __tablename__ = "flight_passengers"

    flight_id: Mapped[str] = mapped_column(
        ForeignKey("flights.flight_id"), primary_key=True
    )
    passenger_id: Mapped[str] = mapped_column(
        ForeignKey("passengers.passenger_id"), primary_key=True
    )
    status: Mapped[str] = mapped_column(String(20))  # Boarded | Cancelled

    flight: Mapped["Flight"] = relationship(back_populates="flight_passengers")
    passenger: Mapped["Passenger"] = relationship(back_populates="flight_passengers")
