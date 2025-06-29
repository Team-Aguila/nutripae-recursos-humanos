from sqlalchemy import Column, Integer, String, Text
from .base import Base

class DocumentType(Base):
    __tablename__ = 'document_types'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<DocumentType(id={self.id}, name='{self.name}')>"

class Gender(Base):
    __tablename__ = 'genders'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<Gender(id={self.id}, name='{self.name}')>"

class OperationalRole(Base):
    __tablename__ = 'operational_roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    def __repr__(self):
        return f"<OperationalRole(id={self.id}, name='{self.name}')>"

class AvailabilityStatus(Base):
    __tablename__ = 'availability_statuses'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    
    def __repr__(self):
        return f"<AvailabilityStatus(id={self.id}, name='{self.name}')>"