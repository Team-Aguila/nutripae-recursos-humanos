# app/models/employee.py

from datetime import date
from sqlalchemy import (
    Column, Integer, String, Date, Boolean, ForeignKey, TIMESTAMP
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

from .base import Base # Importa la clase Base

class Employee(Base):
    __tablename__ = "employees"

    # --- Basic Identification ---
    id = Column(Integer, primary_key=True, index=True)
    document_number = Column(String(50), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    birth_date = Column(Date, nullable=False)
    
    # --- Foreign Keys to Parametric Tables ---
    document_type_id = Column(Integer, ForeignKey('document_types.id'), nullable=False)
    gender_id = Column(Integer, ForeignKey('genders.id'), nullable=False)
    operational_role_id = Column(Integer, ForeignKey('operational_roles.id'), nullable=False)
    
    # --- SQLAlchemy Relationships (for easy access in code) ---
    document_type = relationship("DocumentType")
    gender = relationship("Gender")
    operational_role = relationship("OperationalRole")
    
    # --- Identity Document File ---
    identity_document_path = Column(String(500), nullable=True)

    # --- Employment Data ---
    hire_date = Column(Date, nullable=False)
    
    # --- Optional Contact Info ---
    address = Column(String(255), nullable=True)
    phone_number = Column(String(50), nullable=True)
    personal_email = Column(String(100), nullable=True)
    
    # --- Optional Emergency Contact ---
    emergency_contact_name = Column(String(255), nullable=True)
    emergency_contact_phone = Column(String(50), nullable=True)
    emergency_contact_relation = Column(String(50), nullable=True)
    
    # --- Logical Delete & Auditing ---
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    termination_date = Column(Date, nullable=True)
    reason_for_termination = Column(String(500), nullable=True)
    
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'), onupdate=text('now()'))

    # --- Relationship to DailyAvailability ---
    availabilities = relationship("DailyAvailability", back_populates="employee", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Employee(id={self.id}, name='{self.full_name}')>"