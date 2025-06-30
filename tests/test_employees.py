from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from models import parametric

def test_create_and_get_employee(client: TestClient, db: Session):
    # --------------------------------------------------------------------------
    # 1. Setup: Crear datos paramétricos necesarios en la DB de prueba
    # --------------------------------------------------------------------------
    # Se usa la sesión 'db' que viene de la fixture transaccional
    doc_type = parametric.DocumentType(name="Cédula de Ciudadanía (Test)")
    gender = parametric.Gender(name="Otro (Test)")
    role = parametric.OperationalRole(name="Tester")

    # Guardarlos en la base de datos (dentro de la transacción)
    db.add_all([doc_type, gender, role])
    db.commit()
    db.refresh(doc_type)
    db.refresh(gender)
    db.refresh(role)

    # --------------------------------------------------------------------------
    # 2. Test: Crear un empleado usando el endpoint de la API
    # --------------------------------------------------------------------------
    employee_data = {
        "document_number": "987654321",
        "full_name": "Maria Test",
        "birth_date": "1995-02-20",
        "hire_date": "2024-01-10",
        "document_type_id": doc_type.id,
        "gender_id": gender.id,
        "operational_role_id": role.id,
    }

    response = client.post("/employees/", json=employee_data)

    assert response.status_code == 201, response.text
    created_employee = response.json()
    assert created_employee["full_name"] == employee_data["full_name"]
    assert created_employee["document_number"] == employee_data["document_number"]

    # --------------------------------------------------------------------------
    # 3. Test: Obtener el empleado recién creado
    # --------------------------------------------------------------------------
    employee_id = created_employee["id"]
    response = client.get(f"/employees/{employee_id}")

    assert response.status_code == 200, response.text
    retrieved_employee = response.json()
    assert retrieved_employee["id"] == employee_id
    assert retrieved_employee["full_name"] == employee_data["full_name"]
    assert retrieved_employee["operational_role"]["id"] == role.id 