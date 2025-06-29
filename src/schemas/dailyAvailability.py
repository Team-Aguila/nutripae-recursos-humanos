from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional

# Importamos el esquema de lectura de la tabla paramétrica
from .parametric import AvailabilityStatus

class DailyAvailabilityBase(BaseModel):
    date: date
    status_id: int
    notes: str | None = None

class DailyAvailabilityCreate(DailyAvailabilityBase):
    employee_id: int

class DailyAvailabilityUpdate(BaseModel):
    date: Optional[date] = None
    status_id: Optional[int] = None
    notes: Optional[str] = None

class DailyAvailability(DailyAvailabilityBase):
    # Esquema de lectura
    id: int
    employee_id: int
    created_at: datetime
    updated_at: datetime
    
    # Devolvemos el objeto anidado para el estado
    status: AvailabilityStatus

    model_config = ConfigDict(from_attributes=True)