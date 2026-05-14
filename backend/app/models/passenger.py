from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.flight_passenger import FlightPassenger


class Passenger(Base):
    __tablename__ = "passengers"

    passenger_id: Mapped[str] = mapped_column(String(20), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    national_id: Mapped[str] = mapped_column(String(20), unique=True)
    date_of_birth: Mapped[date] = mapped_column(Date)

    flight_passengers: Mapped[list["FlightPassenger"]] = relationship(
        back_populates="passenger"
    )
