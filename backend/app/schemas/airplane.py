from datetime import date

from pydantic import BaseModel


class AirplaneCreate(BaseModel):
    plate_number: str
    type: str
    last_maintenance_date: date
    next_maintenance_date: date
    capacity: int
    owner_id: str
    owner_name: str
    hangar_id: str
    fuel_capacity: int


class AirplaneResponse(AirplaneCreate):
    model_config = {"from_attributes": True}


class AirplaneWithAlerts(AirplaneResponse):
    days_until_maintenance: int
    maintenance_alert: bool
