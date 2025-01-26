import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def prepare_database():
    response = client.get("/contacts/")
    contacts = response.json()
    for contact in contacts:
        client.delete(f"/contacts/{contact['id']}")

    response_1 = client.post(
        "/contacts/",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "phone": "123-456-7890",
            "birthday": "1990-01-01",
            "additional_info": "Test data"
        },
    )
    response_2 = client.post(
        "/contacts/",
        json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "janedoe@example.com",
            "phone": "987-654-3210",
            "birthday": "1992-05-10",
            "additional_info": "Test data"
        },
    )
    return {
        "first_contact_id": response_1.json()["id"],
        "second_contact_id": response_2.json()["id"],
    }

def test_create_contact():
    response = client.post(
        "/contacts/",
        json={
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice@example.com",
            "phone": "555-555-5555",
            "birthday": "1985-03-15",
            "additional_info": "New contact"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Alice"
    assert data["last_name"] == "Smith"

def test_read_contacts():
    response = client.get("/contacts/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_read_contact(prepare_database):
    first_contact_id = prepare_database["first_contact_id"]
    response = client.get(f"/contacts/{first_contact_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == first_contact_id

def test_update_contact(prepare_database):
    first_contact_id = prepare_database["first_contact_id"]
    response = client.put(
        f"/contacts/{first_contact_id}",
        json={
            "first_name": "Jane",
            "last_name": "Smith"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Jane"
    assert data["last_name"] == "Smith"

def test_delete_contact(prepare_database):
    first_contact_id = prepare_database["first_contact_id"]
    response = client.delete(f"/contacts/{first_contact_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Contact deleted successfully"

def test_search_contacts():
    response = client.get("/contacts/search/?query=Jane")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

def test_upcoming_birthdays():
    response = client.get("/contacts/birthdays/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)