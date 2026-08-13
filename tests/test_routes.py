import pytest
from app import create_app
from app import storage


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    storage.reset_storage()
    with app.test_client() as client:
        yield client
    storage.reset_storage()


def test_get_empty_inventory(client):
    resp = client.get("/inventory")
    assert resp.status_code == 200
    assert resp.get_json() == []


def test_create_item(client):
    resp = client.post("/inventory", json={"name": "Milk", "price": 3.5, "quantity": 5})
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["name"] == "Milk"
    assert data["id"] == 1


def test_create_item_missing_fields(client):
    resp = client.post("/inventory", json={"name": "Milk"})
    assert resp.status_code == 400
    assert "errors" in resp.get_json()


def test_get_single_item(client):
    client.post("/inventory", json={"name": "Eggs", "price": 4.0, "quantity": 12})
    resp = client.get("/inventory/1")
    assert resp.status_code == 200
    assert resp.get_json()["name"] == "Eggs"


def test_get_single_item_not_found(client):
    resp = client.get("/inventory/999")
    assert resp.status_code == 404


def test_patch_item(client):
    client.post("/inventory", json={"name": "Bread", "price": 2.0, "quantity": 10})
    resp = client.patch("/inventory/1", json={"price": 2.5, "quantity": 8})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["price"] == 2.5
    assert data["quantity"] == 8


def test_patch_item_not_found(client):
    resp = client.patch("/inventory/999", json={"price": 1})
    assert resp.status_code == 404


def test_delete_item(client):
    client.post("/inventory", json={"name": "Butter", "price": 3.0, "quantity": 4})
    resp = client.delete("/inventory/1")
    assert resp.status_code == 200
    resp2 = client.get("/inventory/1")
    assert resp2.status_code == 404


def test_delete_item_not_found(client):
    resp = client.delete("/inventory/999")
    assert resp.status_code == 404


def test_lookup_missing_params(client):
    resp = client.get("/inventory/lookup")
    assert resp.status_code == 400
