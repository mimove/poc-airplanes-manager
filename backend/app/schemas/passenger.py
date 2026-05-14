from datetime import date

from pydantic import BaseModel


class PassengerCreate(BaseModel):
    passenger_id: str
    name: str
    national_id: str
    date_of_birth: date


class PassengerResponse(PassengerCreate):
    model_config = {"from_attributes": True}
