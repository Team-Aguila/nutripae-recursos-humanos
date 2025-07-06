
from datetime import date
from sqlalchemy import (
    Column, Integer, Date, Text, ForeignKey, UniqueConstraint, TIMESTAMP
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

from .base import Base

class DailyAvailability(Base):
    __tablename__ = "daily_availabilities"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    notes = Column(Text, nullable=True)
    
    # --- Foreign Keys ---
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    status_id = Column(Integer, ForeignKey("availability_statuses.id"), nullable=False)
    
    # --- SQLAlchemy Relationships ---
    employee = relationship("Employee", back_populates="availabilities")
    status = relationship("AvailabilityStatus")

    # --- Auditing ---
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'), onupdate=text('now()'))

    # --- Constraint ---
    __table_args__ = (UniqueConstraint('employee_id', 'date', name='_employee_date_uc'),)

    def __repr__(self):
        return f"<DailyAvailability(employee_id={self.employee_id}, date='{self.date}')>"