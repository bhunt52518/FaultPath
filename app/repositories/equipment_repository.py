from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.equipment import EquipmentModel




class EquipmentModelRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_equipment_model(self, equipment_model: EquipmentModel) -> EquipmentModel:
        self.db.add(equipment_model)

        return equipment_model

    def get_by_id(self, model_id: int) -> EquipmentModel | None:
        return self.db.get(EquipmentModel, model_id)

    def get_all(self) -> list[EquipmentModel]:
        return self.db.scalars(select(EquipmentModel)).all()

    
