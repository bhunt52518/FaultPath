from sqlalchemy import inspect, select

from app.models.alarm import AlarmDefinition
from app.models.equipment import EquipmentModel
from app.models.enums import AlarmSeverity
from app.repositories.alarm_repository import AlarmDefinitionRepository
from app.repositories.equipment_repository import EquipmentModelRepository





def test_create_alarm(db_session):
    repository = AlarmDefinitionRepository(db_session)

    equipment_model_a = EquipmentModel(manufacturer="Delta", model_name="CNC Model A", description="Test Equipment")
    motor_alarm = AlarmDefinition(
        equipment_model=equipment_model_a,alarm_code="MOTOR-001", title="Motor Alarm", severity=AlarmSeverity.FAULT,
        description="Test Alarm")

    created_alarm = repository.create_alarm(motor_alarm)
    db_session.commit()

    assert created_alarm.id is not None
    assert created_alarm.equipment_model_id is not None
    assert created_alarm.equipment_model_id == equipment_model_a.id
    assert created_alarm.equipment_model is equipment_model_a

def test_get_alarm_by_id(db_session):
    repository = AlarmDefinitionRepository(db_session)
    equipment_model_a = EquipmentModel(manufacturer="Delta", model_name="CNC Model A", description="Test Equipment")
    motor_alarm = AlarmDefinition(
        equipment_model=equipment_model_a,alarm_code="MOTOR-001", title="Motor Alarm", severity=AlarmSeverity.FAULT,
        description="Test Alarm")

    created_alarm = repository.create_alarm(motor_alarm)
    db_session.commit()

    retrieved_alarm = repository.get_by_id(created_alarm.id)

    assert retrieved_alarm is not None
    assert retrieved_alarm.id == created_alarm.id
    assert retrieved_alarm.equipment_model is equipment_model_a
    assert retrieved_alarm.alarm_code == "MOTOR-001"
    assert retrieved_alarm.title == "Motor Alarm"

def test_get_alarms_by_equipment_model(db_session):
    repository = AlarmDefinitionRepository(db_session)
    equipment_model_a = EquipmentModel(manufacturer="Delta", model_name="CNC Model A", description="Test Equipment")
    equipment_model_b = EquipmentModel(manufacturer="Delta", model_name="CNC Model B", description="Test Equipment")
    motor_alarm = AlarmDefinition(
        equipment_model=equipment_model_a,alarm_code="MOTOR-001", title="Motor Alarm", severity=AlarmSeverity.FAULT,
        description="Test Alarm")
    temp_alarm = AlarmDefinition(
        equipment_model=equipment_model_a,alarm_code="Temp-001", title="Temp Alarm", severity=AlarmSeverity.FAULT,
        description="Test Alarm")
    press_alarm = AlarmDefinition(
        equipment_model=equipment_model_b,alarm_code="PRESS-001", title="Pressure Alarm", severity=AlarmSeverity.FAULT,
        description="Test Alarm")

    alarm_a = repository.create_alarm(motor_alarm)
    alarm_b = repository.create_alarm(temp_alarm)
    alarm_c = repository.create_alarm(press_alarm)
    db_session.commit()

    created_alarms = [alarm_a, alarm_b]
    created_ids = {alarm.id for alarm in created_alarms}

    retrieved_alarms = repository.get_by_equipment_model(equipment_model_a.id)
    retrieved_alarm_codes = [code.alarm_code for code in retrieved_alarms]
    retireved_ids = {alarm.id for alarm in retrieved_alarms}

    assert len(retrieved_alarms) == 2
    assert motor_alarm.alarm_code in retrieved_alarm_codes
    assert temp_alarm.alarm_code in retrieved_alarm_codes
    assert retireved_ids == created_ids
    assert all(
        alarm.equipment_model_id == equipment_model_a.id
        for alarm in retrieved_alarms)
    
def test_get_alarms_by_equipment_model_empty(db_session):
    alarm_repository = AlarmDefinitionRepository(db_session)
    equipment_repository = EquipmentModelRepository(db_session)
    equipment_model_a = EquipmentModel(manufacturer="Delta", model_name="CNC Model A", description="Test Equipment")

    created_equipment = equipment_repository.create_equipment_model(equipment_model_a)
    db_session.commit()

    retrieved_alarms =  alarm_repository.get_by_equipment_model(created_equipment.id)

    assert retrieved_alarms == []