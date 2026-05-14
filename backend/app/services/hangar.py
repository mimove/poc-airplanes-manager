from app.models.hangar import Hangar
from app.repositories.hangar import HangarRepository
from app.schemas.hangar import HangarCreate


class HangarService:
    def __init__(self, repo: HangarRepository) -> None:
        self.repo = repo

    async def list_hangars(self) -> list[Hangar]:
        return await self.repo.get_all()

    async def get_hangar(self, hangar_id: str) -> Hangar | None:
        return await self.repo.get_by_id(hangar_id)

    async def create_hangar(self, data: HangarCreate) -> Hangar:
        hangar = Hangar(**data.model_dump())
        return await self.repo.create(hangar)
