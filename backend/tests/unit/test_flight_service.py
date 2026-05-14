from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest

from app.models.airplane import Airplane
from app.models.flight import Flight
from app.services.flight import FlightService


def make_airplane(capacity=9, fuel_capacity=700) -> Airplane:
    a = Airplane(
        plate_number="EC-XYZ1",
        type="Cessna 208 Caravan",
        last_maintenance_date=None,
        next_maintenance_date=None,
        capacity=capacity,
        owner_id="O-12345",
        owner_name="Madrid Flying Club",
        hangar_id="H-01",
        fuel_capacity=fuel_capacity,
    )
    return a


def make_flight(occupied_seats=7, fuel_consumption=350, airplane=None) -> Flight:
    f = Flight(
        flight_id="FL-2025-001",
        plate_number="EC-XYZ1",
        arrival_time=datetime(2026, 3, 1, 9, 30, tzinfo=timezone.utc),
        departure_time=datetime(2026, 3, 1, 14, 45, tzinfo=timezone.utc),
        fuel_consumption=fuel_consumption,
        occupied_seats=occupied_seats,
        origin="Valencia",
        destination="Paris",
    )
    f.airplane = airplane or make_airplane()
    f.flight_passengers = []
    return f


@pytest.fixture
def mock_repo():
    return AsyncMock()


@pytest.fixture
def service(mock_repo):
    return FlightService(repo=mock_repo)


def test_empty_seats_calculation(service):
    airplane = make_airplane(capacity=9)
    flight = make_flight(occupied_seats=7, airplane=airplane)
    assert service.empty_seats(flight) == 2


def test_empty_seats_alert_true_when_empty_exceeds_10_percent(service):
    # capacity=9, occupied=7, empty=2, 2/9=22% > 10%
    airplane = make_airplane(capacity=9)
    flight = make_flight(occupied_seats=7, airplane=airplane)
    assert service.empty_seats_alert(flight) is True


def test_empty_seats_alert_false_when_full(service):
    airplane = make_airplane(capacity=9)
    flight = make_flight(occupied_seats=9, airplane=airplane)
    assert service.empty_seats_alert(flight) is False


def test_fuel_alert_true_when_consumption_exceeds_10_percent_capacity(service):
    # fuel_capacity=700, consumption=350, 350 > 70 → alert
    airplane = make_airplane(fuel_capacity=700)
    flight = make_flight(fuel_consumption=350, airplane=airplane)
    assert service.fuel_alert(flight) is True


def test_fuel_alert_false_when_consumption_below_10_percent_capacity(service):
    # fuel_capacity=700, consumption=50, 50 < 70 → no alert
    airplane = make_airplane(fuel_capacity=700)
    flight = make_flight(fuel_consumption=50, airplane=airplane)
    assert service.fuel_alert(flight) is False


async def test_list_flights_returns_repo_results(service, mock_repo):
    expected = [make_flight()]
    mock_repo.get_all.return_value = expected
    result = await service.list_flights()
    assert result == expected


async def test_get_flight_returns_none_when_not_found(service, mock_repo):
    mock_repo.get_by_id.return_value = None
    result = await service.get_flight("UNKNOWN")
    assert result is None
