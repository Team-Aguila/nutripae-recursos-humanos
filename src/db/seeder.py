import logging
from datetime import date, timedelta
from faker import Faker
from sqlalchemy.orm import Session
from models import (
    Base,
    DocumentType,
    Gender,
    OperationalRole,
    AvailabilityStatus,
    Employee,
    DailyAvailability,
)

# Configuración básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar Faker para datos de prueba en español
fake = Faker("es_CO")


def seed_db(db: Session):
    """
    Función principal para poblar la base de datos con datos de prueba.
    """
    # La lógica de la sesión se maneja en el lanzador (sync_seeder.py)
    logger.info("Iniciando el proceso de siembra de la base de datos...")

    # 1. Sembrar Tablas Paramétricas
    logger.info("Sembrando tablas paramétricas...")
    doc_types = seed_parametric(
        db,
        DocumentType,
        [
            {"name": "Cédula de Ciudadanía (CC)"},
            {"name": "Cédula de Extranjería (CE)"},
            {"name": "Permiso por Protección Temporal (PPT)"},
        ],
    )
    genders = seed_parametric(db, Gender, [{"name": "Masculino"}, {"name": "Femenino"}, {"name": "Otro"}])
    roles = seed_parametric(
        db,
        OperationalRole,
        [
            {"name": "Manipulador de Alimentos", "description": "Encargado de la preparación y servicio de alimentos."},
            {"name": "Conductor", "description": "Responsable del transporte de insumos y alimentos."},
            {"name": "Auxiliar Logístico", "description": "Apoyo en bodega, cargue y descargue."},
            {"name": "Supervisor de Ruta", "description": "Coordina y verifica las entregas en las instituciones."},
        ],
    )
    statuses = seed_parametric(
        db,
        AvailabilityStatus,
        [
            {"name": "Disponible"},
            {"name": "Ausente por Enfermedad"},
            {"name": "Vacaciones"},
            {"name": "Permiso"},
            {"name": "Capacitación"},
            {"name": "Inactivo"},
        ],
    )
    logger.info("Tablas paramétricas sembradas con éxito.")

    # 2. Sembrar Empleados
    logger.info("Sembrando empleados de prueba...")
    seed_employees(db, doc_types, genders, roles)
    logger.info("Empleados sembrados con éxito.")

    # 3. Sembrar Disponibilidad Diaria
    logger.info("Sembrando disponibilidad diaria...")
    seed_daily_availability(db, statuses)
    logger.info("Disponibilidad diaria sembrada con éxito.")

    logger.info("¡Siembra de la base de datos completada exitosamente!")


def seed_parametric(db: Session, model, data):
    """Función genérica para poblar tablas paramétricas."""
    if db.query(model).count() == 0:
        instances = [model(**item) for item in data]
        db.add_all(instances)
        db.commit()
        logger.info(f"Se crearon {len(instances)} registros en la tabla {model.__tablename__}.")
        return instances
    else:
        logger.info(f"La tabla {model.__tablename__} ya contiene datos. No se realizaron cambios.")
        return db.query(model).all()


def seed_employees(db: Session, doc_types, genders, roles):
    """Puebla la tabla de empleados si está vacía."""
    if db.query(Employee).count() > 0:
        logger.info("La tabla de empleados ya contiene datos. No se realizaron cambios.")
        return

    employees_to_create = []
    for i in range(15):  # Crear 15 empleados de ejemplo
        doc_type = fake.random_element(elements=doc_types)
        gender = fake.random_element(elements=genders)
        role = fake.random_element(elements=roles)

        employee = Employee(
            document_number=str(fake.unique.random_number(digits=10)),
            full_name=fake.name(),
            birth_date=fake.date_of_birth(minimum_age=18, maximum_age=65),
            document_type_id=doc_type.id,
            gender_id=gender.id,
            operational_role_id=role.id,
            hire_date=fake.date_between(start_date="-5y", end_date="today"),
            address=fake.address(),
            phone_number=fake.phone_number(),
            personal_email=fake.email(),
            emergency_contact_name=fake.name(),
            emergency_contact_phone=fake.phone_number(),
            emergency_contact_relation="Familiar",
            is_active=fake.boolean(chance_of_getting_true=90),
        )
        if not employee.is_active:
            employee.termination_date = fake.date_between(start_date=employee.hire_date)
            employee.reason_for_termination = "Terminación de Contrato"
            
        employees_to_create.append(employee)

    db.add_all(employees_to_create)
    db.commit()


def seed_daily_availability(db: Session, statuses):
    """Puebla la disponibilidad diaria para los próximos días."""
    if db.query(DailyAvailability).count() > 0:
        logger.info("La tabla de disponibilidad diaria ya contiene datos. No se realizaron cambios.")
        return

    active_employees = db.query(Employee).filter(Employee.is_active == True).all()
    today = date.today()
    
    status_disponible = next((s for s in statuses if s.name == "Disponible"), None)
    
    availabilities_to_create = []
    for day_offset in range(7): # Para los próximos 7 días
        current_date = today + timedelta(days=day_offset)
        for emp in active_employees:
            status = fake.random_element(elements=statuses) if fake.random_int(min=1, max=10) > 8 else status_disponible
            
            if status and status.name == 'Inactivo':
                continue

            availability = DailyAvailability(
                employee_id=emp.id,
                date=current_date,
                status_id=status.id,
                notes=f"Nota de prueba para {emp.full_name}" if status.name != "Disponible" else ""
            )
            availabilities_to_create.append(availability)

    db.add_all(availabilities_to_create)
    db.commit()
