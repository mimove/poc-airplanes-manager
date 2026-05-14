from app.models.flight import Flight
from app.models.flight_passenger import FlightPassenger
from app.repositories.flight import FlightRepository
from app.schemas.flight import FlightCreate

_EMPTY_SEATS_ALERT_RATIO = 0.10
_FUEL_ALERT_RATIO = 0.10


class FlightService:
    def __init__(self, repo: FlightRepository) -> None:
        self.repo = repo

    async def list_flights(self) -> list[Flight]:
        return await self.repo.get_all()

    async def get_flight(self, flight_id: str) -> Flight | None:
        return await self.repo.get_by_id(flight_id)

    async def create_flight(self, data: FlightCreate) -> Flight:
        flight_data = data.model_dump(exclude={"passengers"})
        flight = Flight(**flight_data)
        passengers = [
            FlightPassenger(
                flight_id=data.flight_id,
                passenger_id=p.passenger_id,
                status=p.status,
            )
            for p in data.passengers
        ]
        return await self.repo.create(flight, passengers)

    def empty_seats(self, flight: Flight) -> int:
        return flight.airplane.capacity - flight.occupied_seats

    def empty_seats_alert(self, flight: Flight) -> bool:
        threshold = flight.airplane.capacity * _EMPTY_SEATS_ALERT_RATIO
        return self.empty_seats(flight) > threshold

    def fuel_alert(self, flight: Flight) -> bool:
        threshold = flight.airplane.fuel_capacity * _FUEL_ALERT_RATIO
        return flight.fuel_consumption > threshold
