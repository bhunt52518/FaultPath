from sqlalchemy import inspect, select

from app.models.equipment import EquipmentModel
from app.repositories.equipment_repository import EquipmentModelRepository




def test_create_equipment_model(db_session):
    repository=EquipmentModelRepository(db_session)
    equipment_model = EquipmentModel(manufacturer="Delta", model_name="CNC Model A", description=None)

    created_equipment_model = repository.create_equipment_model(equipment_model)
    
    assert created_equipment_model is equipment_model

    state = inspect(created_equipment_model)

    assert state.pending is True

    db_session.commit()

    assert created_equipment_model.id is not None
    assert state.persistent is True

def test_get_equipment_model_by_id(db_session):
    repository=EquipmentModelRepository(db_session)
    equipment_model = EquipmentModel(manufacturer="Delta", model_name="CNC Model A", description=None)
    
    repository.create_equipment_model(equipment_model)
    db_session.commit()

    retrived_equipment_model = repository.get_by_id(equipment_model.id)

    assert retrived_equipment_model is not None
    assert retrived_equipment_model.id == equipment_model.id
    assert retrived_equipment_model.model_name == equipment_model.model_name
    assert retrived_equipment_model.manufacturer == equipment_model.manufacturer

def test_get_nonexistent_equipment_model_returns_none(db_session):
    repository=EquipmentModelRepository(db_session)

    retrived_equipment_model = repository.get_by_id(999)

    assert retrived_equipment_model is None

def test_get_all_equipment_models(db_session):
    repository=EquipmentModelRepository(db_session)
    equipment_model_a = EquipmentModel(manufacturer="Delta", model_name="CNC Model A", description=None)
    equipment_model_b = EquipmentModel(manufacturer="Delta", model_name="CNC Model B", description=None)
    equipment_model_c = EquipmentModel(manufacturer="Delta", model_name="CNC Model C", description=None)
    
    repository.create_equipment_model(equipment_model_a)
    repository.create_equipment_model(equipment_model_b)
    repository.create_equipment_model(equipment_model_c)
    db_session.commit()


    retrieved_equipment = repository.get_all()

    model_names = [model.model_name for model in retrieved_equipment]

    assert len(retrieved_equipment) == 3
    assert equipment_model_c.model_name in model_names
    assert equipment_model_b.model_name in model_names
    assert equipment_model_a.model_name in model_names

def test_get_all_equipment_models_empty(db_session):
    repository = EquipmentModelRepository(db_session)

    retieved_equipment = repository.get_all()

    assert retieved_equipment == []

