from enum import Enum




class EquipmentStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    RETIRED = "RETIRED"

class AlarmSeverity(str, Enum):
    GENERAL = "GENERAL"
    WARNING = "WARNING"
    FAULT = "FAULT"