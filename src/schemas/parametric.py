
from pydantic import BaseModel, ConfigDict

class ParametricBase(BaseModel):
    name: str

class OperationalRoleBase(ParametricBase):
    description: str | None = None

class DocumentType(ParametricBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class Gender(ParametricBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class OperationalRole(OperationalRoleBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class AvailabilityStatus(ParametricBase):
    id: int
    model_config = ConfigDict(from_attributes=True)