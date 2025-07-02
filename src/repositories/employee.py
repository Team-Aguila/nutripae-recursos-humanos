from sqlalchemy.orm import Session
from typing import Optional
from models.employee import Employee
from schemas.employee import EmployeeCreate, EmployeeUpdate
from .base import BaseRepository

class EmployeeRepository(BaseRepository[Employee, EmployeeCreate, EmployeeUpdate]):
    
    def get_by_document_number(self, db: Session, *, document_number: str) -> Employee | None:
        return db.query(Employee).filter(Employee.document_number == document_number).first()
    
    def search_and_filter(
        self, 
        db: Session, 
        *, 
        search: Optional[str] = None,
        role_id: Optional[int] = None,
        is_active: Optional[bool] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> list[Employee]:
        query = db.query(Employee)
        
        if search:
            query = query.filter(
                (Employee.full_name.ilike(f"%{search}%")) |
                (Employee.document_number.ilike(f"%{search}%"))
            )
        
        if role_id is not None:
            query = query.filter(Employee.operational_role_id == role_id)
            
        if is_active is not None:
            query = query.filter(Employee.is_active == is_active)
            
        return query.offset(skip).limit(limit).all()

# Creamos una instancia del repositorio que importaremos en los endpoints
employee_repo = EmployeeRepository(Employee)
