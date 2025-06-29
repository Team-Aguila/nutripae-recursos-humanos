from sqlalchemy.orm import Session
from datetime import date
from models import DailyAvailability
from schemas import DailyAvailabilityCreate, DailyAvailabilityUpdate
from repositories import availability_repo, employee_repo
from utils.exceptions import RecordNotFoundError, DuplicateRecordError

class DailyAvailabilityService:
    def get_availability(self, db: Session, availability_id: int) -> DailyAvailability:
        """
        Obtiene un registro de disponibilidad por su ID.
        Lanza RecordNotFoundError si no existe.
        """
        availability = availability_repo.get(db, id=availability_id)
        if not availability:
            raise RecordNotFoundError(f"Availability record with id {availability_id} not found.")
        return availability

    def get_availabilities_by_employee(
        self, db: Session, employee_id: int, skip: int = 0, limit: int = 100
    ) -> list[DailyAvailability]:
        """Obtiene todos los registros de disponibilidad para un empleado específico."""
        # Nota: Este método podría vivir en el repositorio para una consulta más optimizada.
        # Por ahora, lo mantenemos simple.
        employee = employee_repo.get(db, id=employee_id)
        if not employee:
            raise RecordNotFoundError(f"Employee with id {employee_id} not found.")
        return employee.availabilities[skip : skip + limit]

    def create_availability(self, db: Session, availability_in: DailyAvailabilityCreate) -> DailyAvailability:
        """
        Crea un nuevo registro de disponibilidad.
        Valida que el empleado exista y esté activo.
        Valida que no exista ya un registro para esa fecha y empleado.
        """
        # Regla de Negocio 1: Validar que el empleado exista y esté activo.
        employee = employee_repo.get(db, id=availability_in.employee_id)
        if not employee:
            raise RecordNotFoundError(f"Employee with id {availability_in.employee_id} not found.")
        if not employee.is_active:
            raise ValueError(f"Cannot register availability for inactive employee {employee.full_name}.")
            
        # Regla de Negocio 2: Evitar duplicados.
        existing_availability = availability_repo.get_by_employee_and_date(
            db, employee_id=availability_in.employee_id, target_date=availability_in.date
        )
        if existing_availability:
            raise DuplicateRecordError(f"Availability for this employee on {availability_in.date} already exists.")

        return availability_repo.create(db, obj_in=availability_in)

    def update_availability(
        self, db: Session, availability_id: int, availability_in: DailyAvailabilityUpdate
    ) -> DailyAvailability:
        """Actualiza un registro de disponibilidad."""
        db_availability = self.get_availability(db, availability_id)
        return availability_repo.update(db, db_obj=db_availability, obj_in=availability_in)

    def delete_availability(self, db: Session, availability_id: int) -> DailyAvailability:
        """Elimina un registro de disponibilidad."""
        self.get_availability(db, availability_id) # Valida que exista
        return availability_repo.remove(db, id=availability_id)


availability_service = DailyAvailabilityService()