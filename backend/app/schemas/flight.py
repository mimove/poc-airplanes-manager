from datetime import datetime

from pydantic import BaseModel


class PassengerStatusItem(BaseModel):
    passenger_id: str
    status: str


class FlightCreate(BaseModel):
    flight_id: str
    plate_number: str
    arrival_time: datetime
    departure_time: datetime
    fuel_consumption: int
    occupied_seats: int
    origin: str
    destination: str
    passengers: list[PassengerStatusItem] = []


class FlightResponse(BaseModel):
    flight_id: str
    plate_number: str
    arrival_time: datetime
    departure_time: datetime
    fuel_consumption: int
    occupied_seats: int
    origin: str
    destination: str

    model_config = {"from_attributes": True}


class FlightWithAlerts(FlightResponse):
    empty_seats: int
    empty_seats_alert: bool
    fuel_alert: bool
    passengers: list[PassengerStatusItem] = []
