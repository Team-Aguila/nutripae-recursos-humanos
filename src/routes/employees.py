from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from typing import List, Optional

import schemas
from db.session import get_db
from services import employee_service
from utils.exceptions import RecordNotFoundError, DuplicateRecordError
from core.dependencies import (
    require_create,
    require_read,
    require_update,
    require_delete,
    require_list
)
import logging
router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
)

@router.post("/", response_model=schemas.Employee, status_code=status.HTTP_201_CREATED, summary="Create a new employee")
def create_employee_endpoint(
    employee_in: schemas.EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_create()),
):
    """
    Creates a new employee in the system.
    - **document_number**: Must be unique.
    - Raises a 409 Conflict error if the document number already exists.
    - Requires 'nutripae-rh:create' permission.
    """
    logging.info(f"Creating employee: {employee_in}")
    try:
        return employee_service.create_employee(db=db, employee_in=employee_in)
    except DuplicateRecordError as e:
        logging.error(f"Error creating employee: {e}")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.get("/", response_model=List[schemas.Employee], summary="Get a list of all employees with filters")
def read_employees_endpoint(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    search: Optional[str] = Query(None, description="Search by name or document number"),
    role_id: Optional[int] = Query(None, description="Filter by operational role ID"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    current_user: dict = Depends(require_list()),
):
    """
    Retrieves a paginated list of employees. 
    It can be filtered by name, document, role, and active status.
    - Requires 'nutripae-rh:list' permission.
    """
    logging.info(f"Getting employees: {search}, {role_id}, {is_active}, {skip}, {limit}")
    return employee_service.get_all_employees(
        db=db, 
        search=search, 
        role_id=role_id, 
        is_active=is_active, 
        skip=skip, 
        limit=limit
    )

@router.get("/{employee_id}", response_model=schemas.Employee, summary="Get an employee by ID")
def read_employee_endpoint(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_read()),
):
    """
    Retrieves a single employee by their unique ID.
    - Raises a 404 Not Found error if the employee does not exist.
    - Requires 'nutripae-rh:read' permission.
    """
    try:
        return employee_service.get_employee(db=db, employee_id=employee_id)
    except RecordNotFoundError as e:
        logging.error(f"Error getting employee: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/{employee_id}", response_model=schemas.Employee, summary="Update an employee")
def update_employee_endpoint(
    employee_id: int,
    employee_in: schemas.EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_update()),
):
    """
    Updates an existing employee's information.
    - Raises a 404 Not Found error if the employee does not exist.
    - Requires 'nutripae-rh:update' permission.
    """
    logging.info(f"Updating employee: {employee_id}")
    try:
        return employee_service.update_employee(db=db, employee_id=employee_id, employee_in=employee_in)
    except RecordNotFoundError as e:
        logging.error(f"Error updating employee: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{employee_id}", response_model=schemas.Employee, summary="Delete an employee")
def delete_employee_endpoint(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_delete()),
):
    """
    Deletes an employee from the system.
    - Raises a 404 Not Found error if the employee does not exist.
    - Returns the deleted employee's data upon success.
    - Requires 'nutripae-rh:delete' permission.
    """
    logging.info(f"Deleting employee: {employee_id}")
    try:
        return employee_service.delete_employee(db=db, employee_id=employee_id)
    except RecordNotFoundError as e:
        logging.error(f"Error deleting employee: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))