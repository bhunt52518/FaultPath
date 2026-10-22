from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.equipment import EquipmentModelCreate, EquipmentModelResponse
from app.services.equipment_service import EquipmentModelService




router = APIRouter(prefix="/equipment", tags=["Equipment"])

@router.post("/models", response_model=EquipmentModelResponse, status_code=status.HTTP_201_CREATED)
def create_equipment(create_equipment_model: EquipmentModelCreate, session: Session=Depends(get_db)):
    service = EquipmentModelService(session)
    return service.create_equipment_model(
        create_equipment_model.manufacturer, create_equipment_model.model_name, create_equipment_model.description)

@router.get("/models/{model_id}", response_model=EquipmentModelResponse)
def get_equipment(model_id: int, session: Session=Depends(get_db)):
    service = EquipmentModelService(session)
    equipment = service.get_equipment_model(model_id)

    if equipment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipment Model Not Found")

    return equipment

@router.get("/models", response_model=list[EquipmentModelResponse])
def get_all_equipment(session: Session=Depends(get_db)):
    service = EquipmentModelService(session)
    return service.get_all_equipment_models()

    
