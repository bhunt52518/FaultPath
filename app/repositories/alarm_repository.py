from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.alarm import AlarmDefinition




class AlarmDefinitionRepository:
    def __init__(self, db: Session):
        self.db = db 

    def create_alarm(self, alarm: AlarmDefinition) -> AlarmDefinition:
        self.db.add(alarm)

        return alarm

    def get_by_id(self, alarm_id: int) -> AlarmDefinition | None:
        return self.db.get(AlarmDefinition, alarm_id)

    def get_by_equipment_model(self, model_id: int) -> list[AlarmDefinition]:
        alarms_by_equipment = select(AlarmDefinition).where(AlarmDefinition.equipment_model_id == model_id)
         
        return self.db.scalars(alarms_by_equipment).all()