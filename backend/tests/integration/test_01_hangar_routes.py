import pytest


@pytest.mark.asyncio
async def test_health_endpoint(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_create_hangar(client):
    response = await client.post(
        "/hangars/",
        json={"id": "H-01", "name": "Main Hangar", "location": "North side"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["id"] == "H-01"
    assert body["name"] == "Main Hangar"


@pytest.mark.asyncio
async def test_list_hangars_contains_created(client):
    response = await client.get("/hangars/")
    assert response.status_code == 200
    ids = [h["id"] for h in response.json()]
    assert "H-01" in ids


@pytest.mark.asyncio
async def test_get_hangar_by_id(client):
    response = await client.get("/hangars/H-01")
    assert response.status_code == 200
    assert response.json()["id"] == "H-01"


@pytest.mark.asyncio
async def test_get_hangar_not_found(client):
    response = await client.get("/hangars/DOES-NOT-EXIST")
    assert response.status_code == 404
