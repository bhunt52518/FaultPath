import pytest

from datetime import datetime

from sqlalchemy import create_engine, select, text, event
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.base import Base
from app.models.equipment import EquipmentModel, EquipmentAsset
from app.models.enums import EquipmentStatus




def test_equipment_model_has_multiple_assets(db_session):
    cnc_machine = EquipmentModel(manufacturer="Delta", model_name="L2000", description=None)
    cnc_asset_1 = EquipmentAsset(
        asset_tag="CNC01", serial_number=None, location=None,
        status=EquipmentStatus.ACTIVE, installed_at=None, equipment_model=cnc_machine)
    cnc_asset_2 = EquipmentAsset(
            asset_tag="CNC02", serial_number=None, location=None,
            status=EquipmentStatus.ACTIVE,installed_at=None, equipment_model=cnc_machine)

    db_session.add(cnc_machine)
    db_session.commit()
    model = db_session.get(EquipmentModel, cnc_machine.id)

    assert model.created_at is not None
    assert isinstance(model.created_at, datetime)
    assert len(model.assets) == 2
    assert cnc_asset_1.equipment_model_id == cnc_machine.id
    assert cnc_asset_2.equipment_model_id == cnc_machine.id

def test_dupilcate_asset_tag_rejected(db_session):
    cnc_machine = EquipmentModel(manufacturer="Delta", model_name="L2000", description=None)
    cnc_asset_1 = EquipmentAsset(
        asset_tag="CNC01", serial_number=None, location=None,
        status=EquipmentStatus.ACTIVE, installed_at=None, equipment_model=cnc_machine)
    cnc_asset_2 = EquipmentAsset(
            asset_tag="CNC01", serial_number=None, location=None,
            status=EquipmentStatus.ACTIVE,installed_at=None, equipment_model=cnc_machine)

    
    db_session.add(cnc_machine)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()
    assets = db_session.scalars(select(EquipmentAsset)).all()

    assert assets == []



def test_invalid_equipment_status_rejected(db_session):
    cnc_machine = EquipmentModel(manufacturer="Delta", model_name="L2000", description=None)
    cnc_asset_1 = EquipmentAsset(
        asset_tag="CNC01", serial_number=None, location=None,
        status="Working", installed_at=None, equipment_model=cnc_machine)

    db_session.add(cnc_machine)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()
    assets = db_session.scalars(select(EquipmentAsset)).all()

    assert assets == []

def test_foreign_key_enforcement(db_session):
    result = db_session.execute(text("PRAGMA foreign_keys"))
    forgein_keys_enabled = result.scalar_one()

    assert forgein_keys_enabled == 1

def test_asset_requires_valid_equipment_model(db_session):
    cnc_asset_1 = EquipmentAsset(
        equipment_model_id=999, asset_tag="CNC01", serial_number=None, location=None,
        status=EquipmentStatus.ACTIVE, installed_at=None)

    db_session.add(cnc_asset_1)
    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()
    assets = db_session.scalars(select(EquipmentAsset)).all()

    assert assets == []





    


