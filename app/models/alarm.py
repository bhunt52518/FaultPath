from datetime import datetime, timezone
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.equipment import EquipmentModel

from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, UniqueConstraint, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import AlarmSeverity




class AlarmDefinition(Base):
    __tablename__ = "alarm_definitions"

    __table_args__ = (UniqueConstraint("equipment_model_id", "alarm_code", name="uq_equipment_alarm_code",),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    equipment_model_id: Mapped[int] = mapped_column(Integer, ForeignKey("equipment_models.id"), nullable=False)
    alarm_code: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    severity: Mapped[AlarmSeverity] = mapped_column(
        SQLEnum(AlarmSeverity, native_enum=False, create_constraint=True), nullable=False, default=AlarmSeverity.GENERAL)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    equipment_model: Mapped["EquipmentModel"] = relationship(back_populates="alarms")