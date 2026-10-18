from datetime import datetime, timezone
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.alarm import AlarmDefinition

from sqlalchemy import String, DateTime, Integer, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import EquipmentStatus
from app.models import alarm





class EquipmentModel(Base):
    __tablename__ = "equipment_models"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    manufacturer: Mapped[str] = mapped_column(String(100), nullable=False)
    model_name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),nullable=False)
    assets: Mapped[list["EquipmentAsset"]] = relationship(back_populates="equipment_model")
    alarms: Mapped[list["AlarmDefinition"]] = relationship(back_populates="equipment_model")

class EquipmentAsset(Base):
    __tablename__ = "equipment_assets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    equipment_model_id: Mapped[int] = mapped_column(Integer, ForeignKey("equipment_models.id"), nullable=False)
    asset_tag: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    serial_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    location: Mapped[str | None] = mapped_column(String(150), nullable=True)
    status: Mapped[EquipmentStatus] = mapped_column(
        SQLEnum(EquipmentStatus, native_enum=False, create_constraint=True), nullable=False, default=EquipmentStatus.ACTIVE)
    installed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    equipment_model: Mapped[EquipmentModel] = relationship(back_populates="assets")