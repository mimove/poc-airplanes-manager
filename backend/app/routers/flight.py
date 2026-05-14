from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.repositories.flight import FlightRepository
from app.schemas.flight import (
    FlightCreate,
    FlightResponse,
    FlightWithAlerts,
    PassengerStatusItem,
)
from app.services.flight import FlightService

router = APIRouter(prefix="/flights", tags=["flights"])


def _service(session: AsyncSession = Depends(get_session)) -> FlightService:
    return FlightService(repo=FlightRepository(session))


def _with_alerts(flight, service: FlightService) -> FlightWithAlerts:
    return FlightWithAlerts(
        **FlightResponse.model_validate(flight).model_dump(),
        empty_seats=service.empty_seats(flight),
        empty_seats_alert=service.empty_seats_alert(flight),
        fuel_alert=service.fuel_alert(flight),
        passengers=[
            PassengerStatusItem(passenger_id=fp.passenger_id, status=fp.status)
            for fp in flight.flight_passengers
        ],
    )


@router.get("/", response_model=list[FlightWithAlerts])
async def list_flights(service: FlightService = Depends(_service)):
    flights = await service.list_flights()
    return [_with_alerts(f, service) for f in flights]


@router.get("/{flight_id}", response_model=FlightWithAlerts)
async def get_flight(flight_id: str, service: FlightService = Depends(_service)):
    flight = await service.get_flight(flight_id)
    if flight is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Flight not found"
        )
    return _with_alerts(flight, service)


@router.post("/", response_model=FlightWithAlerts, status_code=status.HTTP_201_CREATED)
async def create_flight(data: FlightCreate, service: FlightService = Depends(_service)):
    flight = await service.create_flight(data)
    return _with_alerts(flight, service)
