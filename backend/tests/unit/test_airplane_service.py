from datetime import date, timedelta
from unittest.mock import AsyncMock

import pytest

from app.models.airplane import Airplane
from app.schemas.airplane import AirplaneCreate
from app.services.airplane import AirplaneService


def make_airplane(**kwargs) -> Airplane:
    defaults = dict(
        plate_number="EC-XYZ1",
        type="Cessna 208 Caravan",
        last_maintenance_date=date(2024, 4, 15),
        next_maintenance_date=date(2026, 4, 15),
        capacity=9,
        owner_id="O-12345",
        owner_name="Madrid Flying Club",
        hangar_id="H-01",
        fuel_capacity=700,
    )
    defaults.update(kwargs)
    return Airplane(**defaults)


@pytest.fixture
def mock_repo():
    return AsyncMock()


@pytest.fixture
def service(mock_repo):
    return AirplaneService(repo=mock_repo)


def test_days_until_maintenance_returns_correct_days(service):
    target = date.today() + timedelta(days=45)
    airplane = make_airplane(next_maintenance_date=target)
    assert service.days_until_maintenance(airplane) == 45


def test_maintenance_alert_true_when_less_than_100_days(service):
    airplane = make_airplane(next_maintenance_date=date.today() + timedelta(days=99))
    assert service.maintenance_alert(airplane) is True


def test_maintenance_alert_false_when_exactly_100_days(service):
    airplane = make_airplane(next_maintenance_date=date.today() + timedelta(days=100))
    assert service.maintenance_alert(airplane) is False


def test_maintenance_alert_false_when_more_than_100_days(service):
    airplane = make_airplane(next_maintenance_date=date.today() + timedelta(days=200))
    assert service.maintenance_alert(airplane) is False


async def test_list_airplanes_returns_repo_results(service, mock_repo):
    expected = [make_airplane()]
    mock_repo.get_all.return_value = expected
    result = await service.list_airplanes()
    assert result == expected
    mock_repo.get_all.assert_called_once()


async def test_get_airplane_returns_none_when_not_found(service, mock_repo):
    mock_repo.get_by_plate.return_value = None
    result = await service.get_airplane("UNKNOWN")
    assert result is None


async def test_create_airplane_delegates_to_repo(service, mock_repo):
    airplane = make_airplane()
    mock_repo.create.return_value = airplane
    data = AirplaneCreate(
        plate_number="EC-XYZ1",
        type="Cessna 208 Caravan",
        last_maintenance_date=date(2024, 4, 15),
        next_maintenance_date=date(2026, 4, 15),
        capacity=9,
        owner_id="O-12345",
        owner_name="Madrid Flying Club",
        hangar_id="H-01",
        fuel_capacity=700,
    )
    result = await service.create_airplane(data)
    assert result == airplane
    mock_repo.create.assert_called_once()
