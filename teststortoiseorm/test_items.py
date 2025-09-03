# tests/test_items.py
import pytest

@pytest.mark.asyncio
async def test_create_item(client):
    response = await client.post(
        "/items/",
        json={"name": "Phone", "description": "Smartphone", "price": 599.99, "tax": 10.0},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Phone"
    assert "id" in data

@pytest.mark.asyncio
async def test_list_items(client):
    response = await client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1  # At least the one created before

@pytest.mark.asyncio
async def test_get_item(client):
    response = await client.get("/items/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

@pytest.mark.asyncio
async def test_update_item(client):
    response = await client.put(
        "/items/1",
        json={"name": "Updated Phone", "description": "Latest model", "price": 699.99},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Phone"

@pytest.mark.asyncio
async def test_delete_item(client):
    response = await client.delete("/items/1")
    assert response.status_code == 200
