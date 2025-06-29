from sqlalchemy.orm import Session
from models.dailyAvailability import DailyAvailability
from schemas.dailyAvailability import DailyAvailabilityCreate, DailyAvailabilityUpdate
from .base import BaseRepository
from datetime import date

class DailyAvailabilityRepository(BaseRepository[DailyAvailability, DailyAvailabilityCreate, DailyAvailabilityUpdate]):
    
    # Ejemplo de método específico
    def get_by_employee_and_date(self, db: Session, *, employee_id: int, target_date: date) -> DailyAvailability | None:
        return (
            db.query(DailyAvailability)
            .filter(DailyAvailability.employee_id == employee_id, DailyAvailability.date == target_date)
            .first()
        )

availability_repo = DailyAvailabilityRepository(DailyAvailability)