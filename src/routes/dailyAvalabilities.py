from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

import schemas
from db.session import get_db
from services import availability_service
from utils.exceptions import RecordNotFoundError, DuplicateRecordError
from core.dependencies import (
    require_create,
    require_read,
    require_list
)
import logging
router = APIRouter(
    prefix="/availabilities",
    tags=["Availabilities"],
)

@router.post("/", response_model=schemas.DailyAvailability, status_code=status.HTTP_201_CREATED, summary="Create a new availability record")
def create_availability_endpoint(
    availability_in: schemas.DailyAvailabilityCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_create()),
):
    """
    Creates a new daily availability record for an employee.
    - Raises 404 if the employee does not exist or is inactive.
    - Raises 409 if an availability record for that employee and date already exists.
    - Requires 'nutripae-rh:create' permission.
    """
    logging.info(f"Creating availability: {availability_in}")
    try:
        return availability_service.create_availability(db=db, availability_in=availability_in)
    except (RecordNotFoundError, ValueError) as e:
        logging.error(f"Error creating availability: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DuplicateRecordError as e:
        logging.error(f"Error creating availability: {e}")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.get("/", response_model=List[schemas.DailyAvailabilityDetails], summary="Get detailed availabilities by date range")
def get_detailed_availabilities_endpoint(
    start_date: date,
    end_date: date,
    employee_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_list()),
):
    """
    Retrieves detailed availability records within a date range.
    - Optionally filters by a specific employee.
    - Requires 'nutripae-rh:list' permission.
    """
    logging.info(f"Getting detailed availabilities: {start_date}, {end_date}, {employee_id}")
    try:
        return availability_service.get_detailed_availabilities(
            db=db, start_date=start_date, end_date=end_date, employee_id=employee_id
        )
    except ValueError as e:
        logging.error(f"Error getting detailed availabilities: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/employee/{employee_id}", response_model=List[schemas.DailyAvailability], summary="Get all availabilities for an employee")
def get_availabilities_for_employee_endpoint(
    employee_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(require_read()),
):
    """
    Retrieves all availability records for a specific employee.
    - Raises 404 if the employee does not exist.
    - Requires 'nutripae-rh:read' permission.
    """
    try:
        return availability_service.get_availabilities_by_employee(db=db, employee_id=employee_id, skip=skip, limit=limit)
    except RecordNotFoundError as e:
        logging.error(f"Error getting availabilities for employee: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

# Aquí irían los endpoints para GET (por ID), PUT y DELETE para una disponibilidad específica,
# siguiendo el mismo patrón que el controlador de empleados.