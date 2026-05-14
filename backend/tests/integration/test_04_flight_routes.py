import pytest


@pytest.mark.asyncio
async def test_create_flight(client):
    response = await client.post(
        "/flights/",
        json={
            "flight_id": "FL-2025-001",
            "plate_number": "EC-XYZ1",
            "arrival_time": "2026-03-01T09:30:00Z",
            "departure_time": "2026-03-01T14:45:00Z",
            "fuel_consumption": 350,
            "occupied_seats": 7,
            "origin": "Valencia",
            "destination": "Paris",
            "passengers": [{"passenger_id": "P-1001", "status": "Boarded"}],
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["flight_id"] == "FL-2025-001"
    assert "empty_seats" in body
    assert "empty_seats_alert" in body
    assert "fuel_alert" in body
    assert body["empty_seats"] == 2  # capacity=9, occupied=7


@pytest.mark.asyncio
async def test_list_flights_includes_alerts(client):
    response = await client.get("/flights/")
    assert response.status_code == 200
    flights = response.json()
    assert len(flights) >= 1
    for f in flights:
        assert "empty_seats_alert" in f
        assert "fuel_alert" in f


@pytest.mark.asyncio
async def test_get_flight_by_id(client):
    response = await client.get("/flights/FL-2025-001")
    assert response.status_code == 200
    body = response.json()
    assert body["flight_id"] == "FL-2025-001"
    assert len(body["passengers"]) == 1
    assert body["passengers"][0]["status"] == "Boarded"


@pytest.mark.asyncio
async def test_get_flight_not_found(client):
    response = await client.get("/flights/FL-NOPE")
    assert response.status_code == 404
