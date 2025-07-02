from sqlalchemy.orm import Session
from sqlalchemy import func
from .base import BaseRepository
from models.parametric import DocumentType, Gender, OperationalRole, AvailabilityStatus
from models.employee import Employee

# --- Repositorios para tablas paramétricas simples ---

class DocumentTypeRepository(BaseRepository[DocumentType, DocumentType, DocumentType]):
    pass

class GenderRepository(BaseRepository[Gender, Gender, Gender]):
    pass

class AvailabilityStatusRepository(BaseRepository[AvailabilityStatus, AvailabilityStatus, AvailabilityStatus]):
    pass

# --- Repositorio para Roles Operativos con lógica adicional ---

class OperationalRoleRepository(BaseRepository[OperationalRole, OperationalRole, OperationalRole]):
    def get_with_employee_count(self, db: Session) -> list:
        """Obtiene los roles y el número de empleados asociados a cada uno."""
        results = (
            db.query(
                OperationalRole,
                func.count(Employee.id).label("employee_count")
            )
            .outerjoin(Employee, Employee.operational_role_id == OperationalRole.id)
            .group_by(OperationalRole.id)
            .order_by(OperationalRole.name)
            .all()
        )
        # Mapeamos el resultado a un formato que el schema pueda entender
        roles_with_count = []
        for role, count in results:
            role.employee_count = count
            roles_with_count.append(role)
        return roles_with_count

# --- Instancias de los repositorios ---

document_type_repo = DocumentTypeRepository(DocumentType)
gender_repo = GenderRepository(Gender)
operational_role_repo = OperationalRoleRepository(OperationalRole)
availability_status_repo = AvailabilityStatusRepository(AvailabilityStatus)
