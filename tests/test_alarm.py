import pytest
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.models.equipment import EquipmentModel
from app.models.alarm import AlarmDefinition
from app.models.enums import AlarmSeverity




def test_multiple_alarms_per_equipment_model(db_session):
    cnc_machine = EquipmentModel(manufacturer="Delta", model_name="CNC Model A", description=None)
    alarm_1 = AlarmDefinition(alarm_code="MOTOR-001", title="Motor Drive Fault", severity=AlarmSeverity.FAULT, equipment_model=cnc_machine)
    alarm_2 = AlarmDefinition(alarm_code="TEMP-001", title="Temperature Warning", severity=AlarmSeverity.WARNING, equipment_model=cnc_machine)

    db_session.add(cnc_machine)
    db_session.commit()
    model = db_session.get(EquipmentModel, cnc_machine.id)

    assert model is not None
    assert model.created_at is not None
    assert isinstance(alarm_1.created_at, datetime)
    assert isinstance(alarm_2.created_at, datetime)
    assert len(model.alarms) == 2
    assert alarm_1.equipment_model_id == cnc_machine.id
    assert alarm_2.equipment_model_id == cnc_machine.id

def test_duplicate_alarm_code_same_model_rejected(db_session):
    cnc_machine = EquipmentModel(manufacturer="Delta", model_name="CNC Model A", description=None)
    alarm_1 = AlarmDefinition(alarm_code="MOTOR-001", title="Motor Drive Fault", severity=AlarmSeverity.FAULT, equipment_model=cnc_machine)
    alarm_2 = AlarmDefinition(alarm_code="MOTOR-001", title="Temperature Warning", severity=AlarmSeverity.WARNING, equipment_model=cnc_machine)

    db_session.add(cnc_machine)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

    alarms = db_session.scalars(select(AlarmDefinition)).all()

    assert alarms == []

def test_same_alarm_code_different_models_allowed(db_session):
    cnc_model_a = EquipmentModel(manufacturer="Delta", model_name="CNC Model A", description=None)
    cnc_model_b = EquipmentModel(manufacturer="Delta", model_name="CNC Model B", description=None)
    alarm_1 = AlarmDefinition(alarm_code="MOTOR-001", title="Motor Drive Fault", severity=AlarmSeverity.FAULT, equipment_model=cnc_model_a)
    alarm_2 = AlarmDefinition(alarm_code="MOTOR-001", title="Motor Drive Fault", severity=AlarmSeverity.FAULT, equipment_model=cnc_model_b)

    db_session.add_all([cnc_model_a, cnc_model_b])
    db_session.commit()

    alarms = db_session.scalars(select(AlarmDefinition)).all()

    assert len(alarms) == 2
    assert alarms[0].alarm_code == alarms[1].alarm_code
    assert alarms[0].equipment_model_id != alarms[1].equipment_model_id

def test_invalid_alarm_severity_rejected(db_session):
    cnc_machine = EquipmentModel(manufacturer="Delta", model_name="CNC Model A", description=None)
    alarm_1 = AlarmDefinition(alarm_code="MOTOR-001", title="Motor Drive Fault", severity="CRITICAL", equipment_model=cnc_machine)

    db_session.add(cnc_machine)
    with pytest.raises(IntegrityError):    
        db_session.commit()
    db_session.rollback()

    alarms = db_session.scalars(select(AlarmDefinition)).all()
    assert alarms == []



