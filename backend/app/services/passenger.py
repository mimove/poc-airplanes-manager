from app.models.passenger import Passenger
from app.repositories.passenger import PassengerRepository
from app.schemas.passenger import PassengerCreate


class PassengerService:
    def __init__(self, repo: PassengerRepository) -> None:
        self.repo = repo

    async def list_passengers(self) -> list[Passenger]:
        return await self.repo.get_all()

    async def get_passenger(self, passenger_id: str) -> Passenger | None:
        return await self.repo.get_by_id(passenger_id)

    async def create_passenger(self, data: PassengerCreate) -> Passenger:
        passenger = Passenger(**data.model_dump())
        return await self.repo.create(passenger)
