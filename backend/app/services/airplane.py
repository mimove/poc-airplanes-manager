from datetime import date

from app.models.airplane import Airplane
from app.repositories.airplane import AirplaneRepository
from app.schemas.airplane import AirplaneCreate

_MAINTENANCE_ALERT_DAYS = 100


class AirplaneService:
    def __init__(self, repo: AirplaneRepository) -> None:
        self.repo = repo

    async def list_airplanes(self) -> list[Airplane]:
        return await self.repo.get_all()

    async def get_airplane(self, plate_number: str) -> Airplane | None:
        return await self.repo.get_by_plate(plate_number)

    async def create_airplane(self, data: AirplaneCreate) -> Airplane:
        airplane = Airplane(**data.model_dump())
        return await self.repo.create(airplane)

    def days_until_maintenance(self, airplane: Airplane) -> int:
        return (airplane.next_maintenance_date - date.today()).days

    def maintenance_alert(self, airplane: Airplane) -> bool:
        return self.days_until_maintenance(airplane) < _MAINTENANCE_ALERT_DAYS
