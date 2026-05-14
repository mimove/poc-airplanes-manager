from datetime import date
from unittest.mock import AsyncMock

import pytest

from app.models.passenger import Passenger
from app.schemas.passenger import PassengerCreate
from app.services.passenger import PassengerService


def make_passenger(**kwargs) -> Passenger:
    defaults = dict(
        passenger_id="P-1001",
        name="Ana García Martínez",
        national_id="12345678A",
        date_of_birth=date(1991, 5, 15),
    )
    defaults.update(kwargs)
    return Passenger(**defaults)


@pytest.fixture
def mock_repo():
    return AsyncMock()


@pytest.fixture
def service(mock_repo):
    return PassengerService(repo=mock_repo)


async def test_list_passengers_returns_repo_results(service, mock_repo):
    expected = [make_passenger()]
    mock_repo.get_all.return_value = expected
    result = await service.list_passengers()
    assert result == expected


async def test_get_passenger_returns_none_when_not_found(service, mock_repo):
    mock_repo.get_by_id.return_value = None
    result = await service.get_passenger("UNKNOWN")
    assert result is None


async def test_create_passenger_delegates_to_repo(service, mock_repo):
    passenger = make_passenger()
    mock_repo.create.return_value = passenger
    data = PassengerCreate(
        passenger_id="P-1001",
        name="Ana García Martínez",
        national_id="12345678A",
        date_of_birth=date(1991, 5, 15),
    )
    result = await service.create_passenger(data)
    assert result == passenger
    mock_repo.create.assert_called_once()
