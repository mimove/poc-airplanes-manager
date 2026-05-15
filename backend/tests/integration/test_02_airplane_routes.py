import pytest


@pytest.mark.asyncio
async def test_create_airplane(client):
    response = await client.post(
        "/airplanes/",
        json={
            "plate_number": "EC-XYZ1",
            "type": "Cessna 208 Caravan",
            "last_maintenance_date": "2024-04-15",
            "next_maintenance_date": "2026-04-15",
            "capacity": 9,
            "owner_id": "O-12345",
            "owner_name": "Madrid Flying Club",
            "hangar_id": "H-01",
            "fuel_capacity": 700,
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["plate_number"] == "EC-XYZ1"
    assert "maintenance_alert" in body
    assert "days_until_maintenance" in body


@pytest.mark.asyncio
async def test_list_airplanes_includes_alerts(client):
    response = await client.get("/airplanes/")
    assert response.status_code == 200
    airplanes = response.json()
    assert len(airplanes) >= 1
    for a in airplanes:
        assert "maintenance_alert" in a
        assert "days_until_maintenance" in a


@pytest.mark.asyncio
async def test_get_airplane_by_plate(client):
    response = await client.get("/airplanes/EC-XYZ1")
    assert response.status_code == 200
    assert response.json()["plate_number"] == "EC-XYZ1"


@pytest.mark.asyncio
async def test_get_airplane_not_found(client):
    response = await client.get("/airplanes/EC-NOPE")
    assert response.status_code == 404
