from sqlalchemy.orm import Session
from .base import BaseRepository
from models.parametric import DocumentType, Gender, OperationalRole, AvailabilityStatus

# Creamos un repositorio genérico para las tablas paramétricas simples
class ParametricRepository(BaseRepository):
    pass

# Creamos una instancia para cada tabla paramétrica
document_type_repo = ParametricRepository(DocumentType)
gender_repo = ParametricRepository(Gender)
operational_role_repo = ParametricRepository(OperationalRole)
availability_status_repo = ParametricRepository(AvailabilityStatus)

class DocumentTypeRepository(BaseRepository[DocumentType, DocumentType, DocumentType]):
    pass