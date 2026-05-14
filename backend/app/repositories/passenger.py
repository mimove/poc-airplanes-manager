from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.passenger import Passenger


class PassengerRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self) -> list[Passenger]:
        result = await self.session.execute(select(Passenger))
        return list(result.scalars().all())

    async def get_by_id(self, passenger_id: str) -> Passenger | None:
        result = await self.session.execute(
            select(Passenger).where(Passenger.passenger_id == passenger_id)
        )
        return result.scalar_one_or_none()

    async def create(self, passenger: Passenger) -> Passenger:
        self.session.add(passenger)
        await self.session.commit()
        await self.session.refresh(passenger)
        return passenger
