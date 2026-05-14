from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.hangar import Hangar


class HangarRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self) -> list[Hangar]:
        result = await self.session.execute(select(Hangar))
        return list(result.scalars().all())

    async def get_by_id(self, hangar_id: str) -> Hangar | None:
        result = await self.session.execute(
            select(Hangar).where(Hangar.id == hangar_id)
        )
        return result.scalar_one_or_none()

    async def create(self, hangar: Hangar) -> Hangar:
        self.session.add(hangar)
        await self.session.commit()
        await self.session.refresh(hangar)
        return hangar
