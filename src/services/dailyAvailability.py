from sqlalchemy.orm import Session
from datetime import date
from models import DailyAvailability
from schemas import DailyAvailabilityCreate, DailyAvailabilityUpdate
from repositories import availability_repo, employee_repo
from utils.exceptions import RecordNotFoundError, DuplicateRecordError
import logging
class DailyAvailabilityService:
    def get_availability(self, db: Session, availability_id: int) -> DailyAvailability:
        """
        Obtiene un registro de disponibilidad por su ID.
        Lanza RecordNotFoundError si no existe.
        """
        logging.info(f"Getting availability: {availability_id}")
        availability = availability_repo.get(db, id=availability_id)
        if not availability:
            logging.error(f"Availability record with id {availability_id} not found.")
            raise RecordNotFoundError(f"Availability record with id {availability_id} not found.")
        return availability

    def get_availabilities_by_employee(
        self, db: Session, employee_id: int, skip: int = 0, limit: int = 100
    ) -> list[DailyAvailability]:
        """Obtiene todos los registros de disponibilidad para un empleado específico."""
        # Nota: Este método podría vivir en el repositorio para una consulta más optimizada.
        # Por ahora, lo mantenemos simple.
        logging.info(f"Getting availabilities by employee: {employee_id}, {skip}, {limit}")
        employee = employee_repo.get(db, id=employee_id)
        if not employee:
            logging.error(f"Employee with id {employee_id} not found.")
            raise RecordNotFoundError(f"Employee with id {employee_id} not found.")
        return employee.availabilities[skip : skip + limit]

    def create_availability(self, db: Session, availability_in: DailyAvailabilityCreate) -> DailyAvailability:
        """
        Crea un nuevo registro de disponibilidad.
        Valida que el empleado exista y esté activo.
        Valida que no exista ya un registro para esa fecha y empleado.
        """
        # Regla de Negocio 1: Validar que el empleado exista y esté activo.
        logging.info(f"Creating availability: {availability_in}")
        employee = employee_repo.get(db, id=availability_in.employee_id)
        if not employee:
            logging.error(f"Employee with id {availability_in.employee_id} not found.")
            raise RecordNotFoundError(f"Employee with id {availability_in.employee_id} not found.")
        if not employee.is_active:
            logging.error(f"Cannot register availability for inactive employee {employee.full_name}.")
            raise ValueError(f"Cannot register availability for inactive employee {employee.full_name}.")

        # Regla de Negocio 2: Validar que la fecha no sea en el pasado.
        if availability_in.date < date.today():
            logging.error(f"Cannot register availability for a past date: {availability_in.date}")
            raise ValueError("Cannot register availability for a past date.")
            
        # Regla de Negocio 3: Evitar duplicados.
        existing_availability = availability_repo.get_by_employee_and_date(
            db, employee_id=availability_in.employee_id, target_date=availability_in.date
        )
        if existing_availability:
            logging.error(f"Availability for this employee on {availability_in.date} already exists.")
            raise DuplicateRecordError(f"Availability for this employee on {availability_in.date} already exists.")

        return availability_repo.create(db, obj_in=availability_in)

    def update_availability(
        self, db: Session, availability_id: int, availability_in: DailyAvailabilityUpdate
    ) -> DailyAvailability:
        """Actualiza un registro de disponibilidad."""
        logging.info(f"Updating availability: {availability_id}")
        db_availability = self.get_availability(db, availability_id)
        return availability_repo.update(db, db_obj=db_availability, obj_in=availability_in)

    from typing import Optional

    def get_detailed_availabilities(
        self, 
        db: Session, 
        start_date: date, 
        end_date: date, 
        employee_id: Optional[int] = None
    ) -> list[DailyAvailability]:
        """Obtiene una lista detallada de disponibilidades por rango de fecha y opcionalmente por empleado."""
        logging.info(f"Getting detailed availabilities: {start_date}, {end_date}, {employee_id}")
        if start_date > end_date:
            logging.error(f"Start date cannot be after end date: {start_date}, {end_date}")
            raise ValueError("Start date cannot be after end date.")
        return availability_repo.get_by_date_range(
            db, start_date=start_date, end_date=end_date, employee_id=employee_id
        )


availability_service = DailyAvailabilityService()