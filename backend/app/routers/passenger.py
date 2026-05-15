from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.repositories.passenger import PassengerRepository
from app.schemas.passenger import PassengerCreate, PassengerResponse
from app.services.passenger import PassengerService

router = APIRouter(prefix="/passengers", tags=["passengers"])


def _service(session: AsyncSession = Depends(get_session)) -> PassengerService:
    return PassengerService(repo=PassengerRepository(session))


@router.get("/", response_model=list[PassengerResponse])
async def list_passengers(service: PassengerService = Depends(_service)):
    return await service.list_passengers()


@router.get("/{passenger_id}", response_model=PassengerResponse)
async def get_passenger(
    passenger_id: str, service: PassengerService = Depends(_service)
):
    passenger = await service.get_passenger(passenger_id)
    if passenger is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Passenger not found"
        )
    return passenger


@router.post("/", response_model=PassengerResponse, status_code=status.HTTP_201_CREATED)
async def create_passenger(
    data: PassengerCreate, service: PassengerService = Depends(_service)
):
    return await service.create_passenger(data)
