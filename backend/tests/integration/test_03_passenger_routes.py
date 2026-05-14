import pytest


@pytest.mark.asyncio
async def test_create_passenger(client):
    response = await client.post(
        "/passengers/",
        json={
            "passenger_id": "P-1001",
            "name": "Ana García Martínez",
            "national_id": "12345678A",
            "date_of_birth": "1991-05-15",
        },
    )
    assert response.status_code == 201
    assert response.json()["passenger_id"] == "P-1001"


@pytest.mark.asyncio
async def test_list_passengers_contains_created(client):
    response = await client.get("/passengers/")
    assert response.status_code == 200
    ids = [p["passenger_id"] for p in response.json()]
    assert "P-1001" in ids


@pytest.mark.asyncio
async def test_get_passenger_by_id(client):
    response = await client.get("/passengers/P-1001")
    assert response.status_code == 200
    assert response.json()["name"] == "Ana García Martínez"


@pytest.mark.asyncio
async def test_get_passenger_not_found(client):
    response = await client.get("/passengers/P-NOPE")
    assert response.status_code == 404
