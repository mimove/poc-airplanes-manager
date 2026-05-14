from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.flight import Flight
    from app.models.hangar import Hangar


class Airplane(Base):
    __tablename__ = "airplanes"

    plate_number: Mapped[str] = mapped_column(String(20), primary_key=True)
    type: Mapped[str] = mapped_column(String(100))
    last_maintenance_date: Mapped[date] = mapped_column(Date)
    next_maintenance_date: Mapped[date] = mapped_column(Date)
    capacity: Mapped[int] = mapped_column(Integer)
    owner_id: Mapped[str] = mapped_column(String(20))
    owner_name: Mapped[str] = mapped_column(String(100))
    hangar_id: Mapped[str] = mapped_column(ForeignKey("hangars.id"))
    fuel_capacity: Mapped[int] = mapped_column(Integer)

    hangar: Mapped["Hangar"] = relationship(back_populates="airplanes")
    flights: Mapped[list["Flight"]] = relationship(back_populates="airplane")
