from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field




class EquipmentModelCreate(BaseModel):

    manufacturer: str = Field(min_length=1, max_length=100)
    model_name: str = Field(min_length=1, max_length=100)
    description: str | None = None

class EquipmentModelResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    manufacturer: str = Field(min_length=1, max_length=100)
    model_name: str = Field(min_length=1, max_length=100)
    description: str | None = None
    created_at: datetime