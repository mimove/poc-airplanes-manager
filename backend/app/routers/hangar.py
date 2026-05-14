from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.repositories.hangar import HangarRepository
from app.schemas.hangar import HangarCreate, HangarResponse
from app.services.hangar import HangarService

router = APIRouter(prefix="/hangars", tags=["hangars"])


def _service(session: AsyncSession = Depends(get_session)) -> HangarService:
    return HangarService(repo=HangarRepository(session))


@router.get("/", response_model=list[HangarResponse])
async def list_hangars(service: HangarService = Depends(_service)):
    return await service.list_hangars()


@router.get("/{hangar_id}", response_model=HangarResponse)
async def get_hangar(hangar_id: str, service: HangarService = Depends(_service)):
    hangar = await service.get_hangar(hangar_id)
    if hangar is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hangar not found"
        )
    return hangar


@router.post("/", response_model=HangarResponse, status_code=status.HTTP_201_CREATED)
async def create_hangar(data: HangarCreate, service: HangarService = Depends(_service)):
    return await service.create_hangar(data)
