import pytest
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.models.equipment import EquipmentModel
from app.services.equipment_service import EquipmentModelService




def test_create_equipment_model_success(db_session):
    service=EquipmentModelService(db_session)
    created_equipment_model = service.create_equipment_model(manufacturer="Delta", model_name="CNC Model A", description=None)

    assert created_equipment_model.id is not None
    assert isinstance(created_equipment_model.created_at, datetime)

    new_equipment_model = db_session.get(EquipmentModel, created_equipment_model.id)

    assert new_equipment_model is not None
    assert new_equipment_model is created_equipment_model
    assert new_equipment_model.manufacturer == "Delta"
    assert new_equipment_model.model_name == "CNC Model A"

def test_create_equipment_model_rollback_on_failure(db_session):
    service = EquipmentModelService(db_session)

    with pytest.raises(IntegrityError):
        service.create_equipment_model(manufacturer=None, model_name="CNC Model A", description=None)

    equipment_models = db_session.scalars(select(EquipmentModel)).all()

    assert equipment_models == []

