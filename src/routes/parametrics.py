from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

import schemas
from db.session import get_db
from services import (
    document_type_service,
    gender_service,
    operational_role_service,
    availability_status_service,
)

router = APIRouter(
    prefix="/options",
    tags=["Options"],
)

@router.get("/document-types", response_model=List[schemas.DocumentType], summary="Get all available document types")
def get_document_types_endpoint(db: Session = Depends(get_db)):
    return document_type_service.get_all(db=db)

@router.get("/genders", response_model=List[schemas.Gender], summary="Get all available genders")
def get_genders_endpoint(db: Session = Depends(get_db)):
    return gender_service.get_all(db=db)

@router.get("/operational-roles", response_model=List[schemas.OperationalRole], summary="Get all available operational roles")
def get_operational_roles_endpoint(db: Session = Depends(get_db)):
    return operational_role_service.get_all(db=db)

@router.get("/availability-statuses", response_model=List[schemas.AvailabilityStatus], summary="Get all available availability statuses")
def get_availability_statuses_endpoint(db: Session = Depends(get_db)):
    return availability_status_service.get_all(db=db)