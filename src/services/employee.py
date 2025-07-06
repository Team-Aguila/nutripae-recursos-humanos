# app/services/employee.py

from sqlalchemy.orm import Session, joinedload
from models import Employee
from schemas import EmployeeCreate, EmployeeUpdate
from repositories import employee_repo
from utils.exceptions import RecordNotFoundError, DuplicateRecordError

class EmployeeService:
    def get_employee(self, db: Session, employee_id: int) -> Employee:
        """
        Obtiene un empleado por su ID.
        Lanza RecordNotFoundError si no existe.
        """
        employee = employee_repo.get(
            db, 
            id=employee_id,
            options=lambda query: query.options(
                joinedload(Employee.document_type),
                joinedload(Employee.gender),
                joinedload(Employee.operational_role)
            )
        )
        if not employee:
            raise RecordNotFoundError(f"Employee with id {employee_id} not found.")
        return employee

    from typing import Optional

    def get_all_employees(
        self, 
        db: Session, 
        search: Optional[str] = None,
        role_id: Optional[int] = None,
        is_active: Optional[bool] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> list[Employee]:
        """Obtiene una lista de todos los empleados con filtros opcionales."""
        return employee_repo.search_and_filter(
            db,
            search=search,
            role_id=role_id,
            is_active=is_active,
            skip=skip,
            limit=limit
        )

    def create_employee(self, db: Session, employee_in: EmployeeCreate) -> Employee:
        """
        Crea un nuevo empleado.
        Lanza DuplicateRecordError si el número de documento ya existe.
        """
        existing_employee = employee_repo.get_by_document_number(db, document_number=employee_in.document_number)
        if existing_employee:
            raise DuplicateRecordError(f"Employee with document number {employee_in.document_number} already exists.")
        
        # Aquí podrías añadir más lógica de negocio, como enviar un email de bienvenida, etc.
        
        return employee_repo.create(db, obj_in=employee_in)

    def update_employee(
        self, db: Session, employee_id: int, employee_in: EmployeeUpdate
    ) -> Employee:
        """
        Actualiza un empleado existente.
        Lanza RecordNotFoundError si el empleado no existe.
        """
        db_employee = self.get_employee(db, employee_id) # Reutiliza el método get para la validación
        
        # Aquí podrías añadir lógica compleja de actualización
        
        return employee_repo.update(db, db_obj=db_employee, obj_in=employee_in)

    def delete_employee(self, db: Session, employee_id: int) -> Employee:
        """
        Elimina un empleado por su ID.
        Lanza RecordNotFoundError si no existe.
        """
        # Le pasamos las opciones de carga a remove para que el objeto devuelto
        # tenga las relaciones y no cause un DetachedInstanceError.
        options = lambda query: query.options(
            joinedload(Employee.document_type),
            joinedload(Employee.gender),
            joinedload(Employee.operational_role)
        )
        
        deleted_employee = employee_repo.remove(db, id=employee_id, options=options)
        
        if not deleted_employee:
            raise RecordNotFoundError(f"Employee with id {employee_id} not found.")
            
        return deleted_employee

# Creamos una instancia del servicio para ser usada con inyección de dependencias
employee_service = EmployeeService()