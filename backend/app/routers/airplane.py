from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.repositories.airplane import AirplaneRepository
from app.schemas.airplane import AirplaneCreate, AirplaneResponse, AirplaneWithAlerts
from app.services.airplane import AirplaneService

router = APIRouter(prefix="/airplanes", tags=["airplanes"])


def _service(session: AsyncSession = Depends(get_session)) -> AirplaneService:
    return AirplaneService(repo=AirplaneRepository(session))


def _with_alerts(airplane, service: AirplaneService) -> AirplaneWithAlerts:
    return AirplaneWithAlerts(
        **AirplaneResponse.model_validate(airplane).model_dump(),
        days_until_maintenance=service.days_until_maintenance(airplane),
        maintenance_alert=service.maintenance_alert(airplane),
    )


@router.get("/", response_model=list[AirplaneWithAlerts])
async def list_airplanes(service: AirplaneService = Depends(_service)):
    airplanes = await service.list_airplanes()
    return [_with_alerts(a, service) for a in airplanes]


@router.get("/{plate_number}", response_model=AirplaneWithAlerts)
async def get_airplane(
    plate_number: str, service: AirplaneService = Depends(_service)
):
    airplane = await service.get_airplane(plate_number)
    if airplane is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Airplane not found"
        )
    return _with_alerts(airplane, service)


@router.post(
    "/", response_model=AirplaneWithAlerts, status_code=status.HTTP_201_CREATED
)
async def create_airplane(
    data: AirplaneCreate, service: AirplaneService = Depends(_service)
):
    airplane = await service.create_airplane(data)
    return _with_alerts(airplane, service)
