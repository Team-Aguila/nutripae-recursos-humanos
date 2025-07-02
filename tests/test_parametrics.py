import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from models import parametric, Employee

@pytest.fixture
def setup_roles_and_employees(db: Session):
    """Crea roles y empleados para probar el conteo."""
    role_a = parametric.OperationalRole(name="Rol de Prueba A")
    role_b = parametric.OperationalRole(name="Rol de Prueba B")
    doc_type = parametric.DocumentType(name="DocType Parametric Test")
    gender = parametric.Gender(name="Gender Parametric Test")
    db.add_all([role_a, role_b, doc_type, gender])
    db.commit()

    # 2 empleados para Rol A, 1 para Rol B
    emp1 = Employee(document_number="801", full_name="Emp Rol A1", birth_date="1990-01-01", hire_date="2024-01-01", document_type_id=doc_type.id, gender_id=gender.id, operational_role_id=role_a.id)
    emp2 = Employee(document_number="802", full_name="Emp Rol A2", birth_date="1990-01-01", hire_date="2024-01-01", document_type_id=doc_type.id, gender_id=gender.id, operational_role_id=role_a.id)
    emp3 = Employee(document_number="803", full_name="Emp Rol B1", birth_date="1990-01-01", hire_date="2024-01-01", document_type_id=doc_type.id, gender_id=gender.id, operational_role_id=role_b.id)
    db.add_all([emp1, emp2, emp3])
    db.commit()

# --- Pruebas para Roles Operativos ---

def test_get_operational_roles_with_employee_count(client: TestClient, setup_roles_and_employees):
    response = client.get("/options/operational-roles")
    assert response.status_code == 200
    data = response.json()

    # Asumimos que pueden existir otros roles de otras pruebas, así que buscamos los nuestros
    role_a_data = next((r for r in data if r["name"] == "Rol de Prueba A"), None)
    role_b_data = next((r for r in data if r["name"] == "Rol de Prueba B"), None)

    assert role_a_data is not None
    assert role_b_data is not None

    assert role_a_data["employee_count"] == 2
    assert role_b_data["employee_count"] == 1

# --- Pruebas para otros datos paramétricos (casos simples) ---

def test_get_document_types(client: TestClient, db: Session):
    # Setup: Asegurarse de que hay al menos un tipo de documento
    if not db.query(parametric.DocumentType).first():
        db.add(parametric.DocumentType(name="Cédula de Ciudadanía"))
        db.commit()

    response = client.get("/options/document-types")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_get_genders(client: TestClient, db: Session):
    if not db.query(parametric.Gender).first():
        db.add(parametric.Gender(name="Femenino"))
        db.commit()

    response = client.get("/options/genders")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_get_availability_statuses(client: TestClient, db: Session):
    if not db.query(parametric.AvailabilityStatus).first():
        db.add(parametric.AvailabilityStatus(name="Incapacidad"))
        db.commit()

    response = client.get("/options/availability-statuses")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
