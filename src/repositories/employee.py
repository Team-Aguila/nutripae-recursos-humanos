from sqlalchemy.orm import Session
from models.employee import Employee
from schemas.employee import EmployeeCreate, EmployeeUpdate
from .base import BaseRepository

class EmployeeRepository(BaseRepository[Employee, EmployeeCreate, EmployeeUpdate]):
    
    # Aquí puedes añadir métodos específicos para el empleado
    def get_by_document_number(self, db: Session, *, document_number: str) -> Employee | None:
        return db.query(Employee).filter(Employee.document_number == document_number).first()
    
    def search_by_name(self, db: Session, *, keyword: str, skip: int = 0, limit: int = 100) -> list[Employee]:
        return (
            db.query(Employee)
            .filter(Employee.full_name.ilike(f"%{keyword}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )

# Creamos una instancia del repositorio que importaremos en los endpoints
employee_repo = EmployeeRepository(Employee)