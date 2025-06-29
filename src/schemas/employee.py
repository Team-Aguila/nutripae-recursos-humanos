
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import date, datetime

from .parametric import DocumentType, Gender, OperationalRole
from .dailyAvailability import DailyAvailability

class EmployeeBase(BaseModel):
    document_number: str
    full_name: str
    birth_date: date
    hire_date: date
    address: str | None = None
    phone_number: str | None = None
    personal_email: EmailStr | None = None
    emergency_contact_name: str | None = None
    emergency_contact_phone: str | None = None
    emergency_contact_relation: str | None = None
    
    document_type_id: int
    gender_id: int
    operational_role_id: int

class EmployeeCreate(EmployeeBase):
    # El path del documento es opcional durante la creación
    identity_document_path: str | None = None

class EmployeeUpdate(BaseModel):
    # En la actualización, todos los campos son opcionales
    document_number: str | None = None
    full_name: str | None = None
    birth_date: date | None = None
    hire_date: date | None = None
    address: str | None = None
    phone_number: str | None = None
    personal_email: EmailStr | None = None
    emergency_contact_name: str | None = None
    emergency_contact_phone: str | None = None
    emergency_contact_relation: str | None = None
    document_type_id: int | None = None
    gender_id: int | None = None
    operational_role_id: int | None = None
    identity_document_path: str | None = None
    is_active: bool | None = None
    termination_date: date | None = None
    reason_for_termination: str | None = None

class Employee(EmployeeBase):
    id: int
    is_active: bool
    identity_document_path: str | None = None
    termination_date: date | None = None
    reason_for_termination: str | None = None
    created_at: datetime
    updated_at: datetime

    # En lugar de los _id, devolvemos los objetos completos anidados
    document_type: DocumentType
    gender: Gender
    operational_role: OperationalRole
    
    # También podemos incluir las disponibilidades relacionadas
    availabilities: list[DailyAvailability] = []

    model_config = ConfigDict(from_attributes=True)