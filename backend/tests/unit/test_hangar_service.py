from unittest.mock import AsyncMock

import pytest

from app.models.hangar import Hangar
from app.schemas.hangar import HangarCreate
from app.services.hangar import HangarService


def make_hangar(**kwargs) -> Hangar:
    defaults = dict(id="H-01", name="Main Hangar", location="North side")
    defaults.update(kwargs)
    return Hangar(**defaults)


@pytest.fixture
def mock_repo():
    return AsyncMock()


@pytest.fixture
def service(mock_repo):
    return HangarService(repo=mock_repo)


async def test_list_hangars_returns_repo_results(service, mock_repo):
    expected = [make_hangar()]
    mock_repo.get_all.return_value = expected
    result = await service.list_hangars()
    assert result == expected


async def test_get_hangar_returns_none_when_not_found(service, mock_repo):
    mock_repo.get_by_id.return_value = None
    result = await service.get_hangar("UNKNOWN")
    assert result is None


async def test_create_hangar_delegates_to_repo(service, mock_repo):
    hangar = make_hangar()
    mock_repo.create.return_value = hangar
    data = HangarCreate(id="H-01", name="Main Hangar", location="North side")
    result = await service.create_hangar(data)
    assert result == hangar
    mock_repo.create.assert_called_once()
