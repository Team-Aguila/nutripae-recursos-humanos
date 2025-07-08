from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import logging
import schemas
from db.session import get_db
from services import (
    document_type_service,
    gender_service,
    operational_role_service,
    availability_status_service,
)
from core.dependencies import require_read

router = APIRouter(
    prefix="/options",
    tags=["Options"],
)

@router.get("/document-types", response_model=List[schemas.DocumentType], summary="Get all available document types")
def get_document_types_endpoint(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_read()),
):
    logging.info(f"Getting document types")
    """
    Get all available document types.
    - Requires 'nutripae-rh:read' permission.
    """
    return document_type_service.get_all(db=db)

@router.get("/genders", response_model=List[schemas.Gender], summary="Get all available genders")
def get_genders_endpoint(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_read()),
):
    logging.info(f"Getting genders")
    """
    Get all available genders.
    - Requires 'nutripae-rh:read' permission.
    """
    return gender_service.get_all(db=db)

@router.get("/operational-roles", response_model=List[schemas.OperationalRoleWithCount], summary="Get all available operational roles with employee count")
def get_operational_roles_endpoint(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_read()),
):
    logging.info(f"Getting operational roles")
    """
    Get all available operational roles with employee count.
    - Requires 'nutripae-rh:read' permission.
    """
    return operational_role_service.get_all_with_count(db=db)

@router.get("/availability-statuses", response_model=List[schemas.AvailabilityStatus], summary="Get all available availability statuses")
def get_availability_statuses_endpoint(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_read()),
):
    logging.info(f"Getting availability statuses")
    """
    Get all available availability statuses.
    - Requires 'nutripae-rh:read' permission.
    """
    return availability_status_service.get_all(db=db)