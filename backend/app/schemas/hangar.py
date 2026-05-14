from pydantic import BaseModel


class HangarCreate(BaseModel):
    id: str
    name: str
    location: str | None = None


class HangarResponse(HangarCreate):
    model_config = {"from_attributes": True}
