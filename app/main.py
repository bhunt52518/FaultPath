from fastapi import FastAPI
from app.api.equipment import router as equipment_router




app = FastAPI(title="FaultPath")

app.include_router(equipment_router)