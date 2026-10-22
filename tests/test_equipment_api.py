import pytest

from fastapi.testclient import TestClient
from sqlalchemy import select

from app.models.equipment import EquipmentModel
from app.main import app
from app.db.session import get_db
from app.schemas.equipment import EquipmentModelResponse




@pytest.fixture
def client(db_session):

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

def test_create_equipment_model_api(client):

    response = client.post(
        "/equipment/models",
        json={
            "manufacturer": "Delta",
            "model_name": "CNC Model A",
            "description": "Test Equipment"
        }
    )

    assert response.status_code == 201
    assert isinstance(response.json()["id"], int)
    assert response.json()["manufacturer"] == "Delta"
    assert response.json()["model_name"] == "CNC Model A"
    assert response.json()["description"] == "Test Equipment"
    assert response.json()["created_at"] is not None

def test_create_equipment_model_missing_model_name(client, db_session):

    response = client.post(
        "/equipment/models",
        json={
            "manufacturer": "Delta",
            "model_name": "",
            "description": "Test Equipment"
        }
    )

    assert response.status_code == 422

    models = db_session.scalars(select(EquipmentModel)).all()
    assert models == []

def test_get_equipment_model_success(client):
    response = client.post(
        "/equipment/models",
        json={
            "manufacturer": "Delta",
            "model_name": "CNC Model A",
            "description": "Test Equipment"
        }
    )

    assert response.status_code == 201

    data = response.json()
    model_id = data["id"]

    get_response = client.get(f"/equipment/models/{model_id}")

    assert get_response.status_code == 200
    assert get_response.json()["id"] == response.json()["id"]
    assert get_response.json()["manufacturer"] == "Delta"
    assert get_response.json()["model_name"] == "CNC Model A"
    assert get_response.json()["description"] == "Test Equipment"

def test_get_equipment_model_not_found(client):
    get_response = client.get("/equipment/models/9999")

    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Equipment Model Not Found"

def test_get_equipment_model_invalid_id(client):
    get_response = client.get("/equipment/models/abc")

    assert get_response.status_code == 422

def test_get_all_equipment_models_api(client):
    response_1 = client.post(
            "/equipment/models",
            json={
                "manufacturer": "Delta",
                "model_name": "CNC Model A",
                "description": "Test Equipment"
            }
        )

    assert response_1.status_code == 201
    
    response_2 = client.post(
            "/equipment/models",
            json={
                "manufacturer": "First",
                "model_name": "Drill Press",
                "description": "Test Equipment"
            }
        )

    assert response_2.status_code == 201
    
    response_3 = client.post(
            "/equipment/models",
            json={
                "manufacturer": "Third",
                "model_name": "Planner",
                "description": "Test Equipment"
            }
        )

    assert response_3.status_code == 201
    
    get_response = client.get("/equipment/models")

    created_models = [response_1.json(), response_2.json(), response_3.json()]
    retrieved_models = get_response.json()

    created_ids = {model["id"] for model in created_models}

    model_names = [model["model_name"] for model in retrieved_models]
    retrieved_ids = {model["id"] for model in retrieved_models}

    assert get_response.status_code == 200
    assert len(retrieved_models) == 3
    assert created_ids == retrieved_ids
    assert "CNC Model A" in model_names
    assert "Drill Press" in model_names
    assert "Planner" in model_names
    
def test_get_all_equipment_models_empty_api(client):
    get_response = client.get("/equipment/models")

    assert get_response.status_code == 200
    assert get_response.json() == []

