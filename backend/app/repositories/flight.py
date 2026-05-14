from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.flight import Flight
from app.models.flight_passenger import FlightPassenger


class FlightRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self) -> list[Flight]:
        result = await self.session.execute(
            select(Flight).options(
                selectinload(Flight.airplane),
                selectinload(Flight.flight_passengers),
            )
        )
        return list(result.scalars().all())

    async def get_by_id(self, flight_id: str) -> Flight | None:
        result = await self.session.execute(
            select(Flight)
            .where(Flight.flight_id == flight_id)
            .options(
                selectinload(Flight.airplane),
                selectinload(Flight.flight_passengers),
            )
        )
        return result.scalar_one_or_none()

    async def create(self, flight: Flight, passengers: list[FlightPassenger]) -> Flight:
        self.session.add(flight)
        for fp in passengers:
            self.session.add(fp)
        await self.session.commit()
        await self.session.refresh(flight)
        return flight
