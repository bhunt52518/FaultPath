from sqlalchemy.orm import Session

from app.models.equipment import EquipmentModel
from app.repositories.equipment_repository import EquipmentModelRepository




class EquipmentModelService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = EquipmentModelRepository(db)

    def create_equipment_model(self, manufacturer: str, model_name: str, description: str | None) -> EquipmentModel:
        equipment_model = EquipmentModel(manufacturer=manufacturer, model_name=model_name, description=description)

        try:
            created_equipment_model = self.repository.create_equipment_model(equipment_model)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
        
        return created_equipment_model

    def get_equipment_model(self, model_id: int) -> EquipmentModel | None:
        return self.repository.get_by_id(model_id)

    def get_all_equipment_models(self) -> list[EquipmentModel]:
        return self.repository.get_all()