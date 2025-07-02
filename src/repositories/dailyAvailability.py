from sqlalchemy.orm import Session, joinedload
from models import DailyAvailability, Employee
from schemas.dailyAvailability import DailyAvailabilityCreate, DailyAvailabilityUpdate
from .base import BaseRepository
from datetime import date
from typing import Optional

class DailyAvailabilityRepository(BaseRepository[DailyAvailability, DailyAvailabilityCreate, DailyAvailabilityUpdate]):
    
    def get_by_employee_and_date(self, db: Session, *, employee_id: int, target_date: date) -> DailyAvailability | None:
        return (
            db.query(DailyAvailability)
            .filter(DailyAvailability.employee_id == employee_id, DailyAvailability.date == target_date)
            .first()
        )

    def get_by_date_range(
        self, 
        db: Session, 
        *, 
        start_date: date, 
        end_date: date, 
        employee_id: Optional[int] = None
    ) -> list[DailyAvailability]:
        query = (
            db.query(DailyAvailability)
            .join(Employee)
            .options(joinedload(DailyAvailability.employee).joinedload(Employee.operational_role))
            .filter(DailyAvailability.date >= start_date, DailyAvailability.date <= end_date)
        )

        if employee_id:
            query = query.filter(DailyAvailability.employee_id == employee_id)

        return query.order_by(DailyAvailability.date, Employee.full_name).all()

availability_repo = DailyAvailabilityRepository(DailyAvailability)