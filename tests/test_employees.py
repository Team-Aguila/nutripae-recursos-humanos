import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from models import parametric, Employee

# --- Fixtures de Datos Reutilizables ---

@pytest.fixture(scope="function")
def parametric_data(db: Session):
    """Crea datos paramétricos básicos una vez por módulo de prueba."""
    doc_type = parametric.DocumentType(name="Cédula de Ciudadanía (Test)")
    gender = parametric.Gender(name="Otro (Test)")
    role_a = parametric.OperationalRole(name="Rol A")
    role_b = parametric.OperationalRole(name="Rol B")
    db.add_all([doc_type, gender, role_a, role_b])
    db.commit()
    return doc_type.id, gender.id, role_a.id, role_b.id

@pytest.fixture
def sample_employees(db: Session, parametric_data):
    """Crea un conjunto de empleados de prueba para cada test."""
    doc_type_id, gender_id, role_a_id, role_b_id = parametric_data
    
    employees = [
        Employee(
            document_number="101", full_name="Juan Perez (A)", birth_date="1990-01-01",
            hire_date="2023-01-01", document_type_id=doc_type_id, gender_id=gender_id,
            operational_role_id=role_a_id, is_active=True
        ),
        Employee(
            document_number="102", full_name="Ana Gomez (B)", birth_date="1992-02-02",
            hire_date="2023-02-01", document_type_id=doc_type_id, gender_id=gender_id,
            operational_role_id=role_b_id, is_active=True
        ),
        Employee(
            document_number="103", full_name="Pedro Inactivo (A)", birth_date="1988-03-03",
            hire_date="2022-03-01", document_type_id=doc_type_id, gender_id=gender_id,
            operational_role_id=role_a_id, is_active=False
        )
    ]
    db.add_all(employees)
    db.commit()
    return employees

# --- Pruebas CRUD Básicas ---

def test_create_employee(client: TestClient, parametric_data):
    doc_type_id, gender_id, role_a_id, _ = parametric_data
    employee_data = {
        "document_number": "999",
        "full_name": "Nuevo Empleado",
        "birth_date": "1999-09-09",
        "hire_date": "2024-01-01",
        "document_type_id": doc_type_id,
        "gender_id": gender_id,
        "operational_role_id": role_a_id,
    }
    response = client.post("/employees/", json=employee_data)
    assert response.status_code == 201
    data = response.json()
    assert data["full_name"] == "Nuevo Empleado"
    assert data["is_active"] == True

def test_create_employee_duplicate_document_fails(client: TestClient, sample_employees):
    employee_data = {
        "document_number": "101", # Duplicado
        "full_name": "Empleado Duplicado",
        "birth_date": "1999-09-09",
        "hire_date": "2024-01-01",
        "document_type_id": sample_employees[0].document_type_id,
        "gender_id": sample_employees[0].gender_id,
        "operational_role_id": sample_employees[0].operational_role_id,
    }
    response = client.post("/employees/", json=employee_data)
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]

def test_get_employee_by_id(client: TestClient, sample_employees):
    employee_id = sample_employees[0].id
    response = client.get(f"/employees/{employee_id}")
    assert response.status_code == 200
    assert response.json()["id"] == employee_id

def test_get_employee_not_found_fails(client: TestClient):
    response = client.get("/employees/99999")
    assert response.status_code == 404

def test_update_employee(client: TestClient, sample_employees):
    employee_id = sample_employees[0].id
    update_data = {"full_name": "Juan Perez Actualizado"}
    response = client.put(f"/employees/{employee_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["full_name"] == "Juan Perez Actualizado"

def test_delete_employee(client: TestClient, sample_employees):
    employee_id = sample_employees[0].id
    response = client.delete(f"/employees/{employee_id}")
    assert response.status_code == 200
    # Verificar que ya no se puede encontrar
    response = client.get(f"/employees/{employee_id}")
    assert response.status_code == 404

# --- Pruebas de Listado, Filtros y Búsqueda ---

def test_get_all_employees_paginated(client: TestClient, sample_employees):
    response = client.get("/employees/?limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_filter_employees_by_role(client: TestClient, sample_employees, parametric_data):
    _, _, role_a_id, _ = parametric_data
    response = client.get(f"/employees/?role_id={role_a_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["full_name"] == "Juan Perez (A)"
    assert data[1]["full_name"] == "Pedro Inactivo (A)"

def test_filter_employees_by_active_status(client: TestClient, sample_employees):
    response = client.get("/employees/?is_active=false")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["full_name"] == "Pedro Inactivo (A)"

def test_search_employees_by_name_and_document(client: TestClient, sample_employees):
    # Búsqueda por nombre
    response = client.get("/employees/?search=Juan")
    assert response.status_code == 200
    assert len(response.json()) == 1
    # Búsqueda por documento
    response = client.get("/employees/?search=102")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["full_name"] == "Ana Gomez (B)"
