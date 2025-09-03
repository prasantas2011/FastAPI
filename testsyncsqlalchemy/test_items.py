import pytest

def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_create_item(client):
    # Example assuming your /items/ POST route exists
    response = client.post(
        "/items/",
        json={"name": "Phone", "description": "Smartphone", "price": 599.99, "tax": 50.0}
    )
    assert response.status_code == 200 or response.status_code == 201
    data = response.json()
    assert data["name"] == "Phone"
    assert "id" in data  # if your model returns id


def test_list_items(client):
    response = client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1  # At least the one created before

def test_get_item(client):
    response = client.get("/items/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

def test_update_item(client):
    response = client.put(
        "/items/1",
        json={"name": "Updated Phone", "description": "Latest model", "price": 699.99},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Phone"

def test_delete_item(client):
    response = client.delete("/items/1")
    assert response.status_code == 200