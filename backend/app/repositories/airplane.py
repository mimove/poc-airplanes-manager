from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.airplane import Airplane


class AirplaneRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self) -> list[Airplane]:
        result = await self.session.execute(select(Airplane))
        return list(result.scalars().all())

    async def get_by_plate(self, plate_number: str) -> Airplane | None:
        result = await self.session.execute(
            select(Airplane).where(Airplane.plate_number == plate_number)
        )
        return result.scalar_one_or_none()

    async def create(self, airplane: Airplane) -> Airplane:
        self.session.add(airplane)
        await self.session.commit()
        await self.session.refresh(airplane)
        return airplane
