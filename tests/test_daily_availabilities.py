import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from models import parametric, Employee, DailyAvailability
from datetime import date, timedelta

# --- Fixtures de Datos ---

@pytest.fixture(scope="function")
def parametric_data(db: Session):
    doc_type = parametric.DocumentType(name="DocType Test Avail")
    gender = parametric.Gender(name="Gender Test Avail")
    role = parametric.OperationalRole(name="Role Test Avail")
    status_disponible = parametric.AvailabilityStatus(name="Disponible")
    status_vacaciones = parametric.AvailabilityStatus(name="Vacaciones")
    db.add_all([doc_type, gender, role, status_disponible, status_vacaciones])
    db.commit()
    return doc_type.id, gender.id, role.id, status_disponible.id, status_vacaciones.id

@pytest.fixture
def sample_employee(db: Session, parametric_data):
    doc_type_id, gender_id, role_id, _, _ = parametric_data
    employee = Employee(
        document_number="555", full_name="Empleado Para Disponibilidad", 
        birth_date="1995-01-01", hire_date="2024-01-01",
        document_type_id=doc_type_id, gender_id=gender_id, operational_role_id=role_id
    )
    db.add(employee)
    db.commit()
    return employee

# --- Pruebas de Creación ---

def test_create_availability(client: TestClient, sample_employee, parametric_data):
    _, _, _, status_disponible_id, _ = parametric_data
    today = date.today()
    availability_data = {
        "employee_id": sample_employee.id,
        "date": today.isoformat(),
        "status_id": status_disponible_id,
        "notes": "Disponible para trabajar"
    }
    response = client.post("/availabilities/", json=availability_data)
    assert response.status_code == 201
    data = response.json()
    assert data["notes"] == "Disponible para trabajar"
    assert data["employee_id"] == sample_employee.id

def test_create_availability_for_past_date_fails(client: TestClient, sample_employee, parametric_data):
    _, _, _, status_disponible_id, _ = parametric_data
    past_date = (date.today() - timedelta(days=1)).isoformat()
    availability_data = {
        "employee_id": sample_employee.id,
        "date": past_date,
        "status_id": status_disponible_id
    }
    response = client.post("/availabilities/", json=availability_data)
    assert response.status_code == 404 # Error de negocio mapeado a 404
    assert "past date" in response.json()["detail"]

def test_create_duplicate_availability_fails(client: TestClient, sample_employee, parametric_data):
    _, _, _, status_disponible_id, _ = parametric_data
    today = date.today()
    availability_data = {
        "employee_id": sample_employee.id,
        "date": today.isoformat(),
        "status_id": status_disponible_id
    }
    # Primera creación (éxito)
    client.post("/availabilities/", json=availability_data)
    # Segunda creación (fallo)
    response = client.post("/availabilities/", json=availability_data)
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]

# --- Pruebas de Consulta ---

def test_get_availabilities_by_date_range(client: TestClient, sample_employee, parametric_data):
    doc_type_id, gender_id, role_id, status_disponible_id, status_vacaciones_id = parametric_data
    today = date.today()
    tomorrow = today + timedelta(days=1)

    # Crear datos de prueba
    client.post("/availabilities/", json={"employee_id": sample_employee.id, "date": today.isoformat(), "status_id": status_disponible_id})
    client.post("/availabilities/", json={"employee_id": sample_employee.id, "date": tomorrow.isoformat(), "status_id": status_vacaciones_id})

    # Test: Consultar rango que incluye ambos días
    response = client.get(f"/availabilities/?start_date={today.isoformat()}&end_date={tomorrow.isoformat()}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["employee"]["id"] == sample_employee.id
    assert data[1]["status"]["name"] == "Vacaciones"

def test_get_availabilities_for_specific_employee(client: TestClient, db: Session, parametric_data):
    doc_type_id, gender_id, role_id, status_disponible_id, _ = parametric_data
    # Crear dos empleados
    emp1 = Employee(document_number="666", full_name="Emp A", birth_date="1990-01-01", hire_date="2024-01-01", document_type_id=doc_type_id, gender_id=gender_id, operational_role_id=role_id)
    emp2 = Employee(document_number="777", full_name="Emp B", birth_date="1990-01-01", hire_date="2024-01-01", document_type_id=doc_type_id, gender_id=gender_id, operational_role_id=role_id)
    db.add_all([emp1, emp2])
    db.commit()

    today = date.today()
    client.post("/availabilities/", json={"employee_id": emp1.id, "date": today.isoformat(), "status_id": status_disponible_id})
    client.post("/availabilities/", json={"employee_id": emp2.id, "date": today.isoformat(), "status_id": status_disponible_id})

    # Test: Consultar solo para emp1
    response = client.get(f"/availabilities/?start_date={today.isoformat()}&end_date={today.isoformat()}&employee_id={emp1.id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["employee"]["id"] == emp1.id

def test_get_availabilities_invalid_date_range_fails(client: TestClient):
    today = date.today()
    yesterday = today - timedelta(days=1)
    response = client.get(f"/availabilities/?start_date={today.isoformat()}&end_date={yesterday.isoformat()}")
    assert response.status_code == 400
    assert "Start date cannot be after end date" in response.json()["detail"]
