from sqlalchemy.orm import Session
from repositories.base import BaseRepository
from utils.exceptions import RecordNotFoundError
from repositories import (
    document_type_repo,
    gender_repo,
    operational_role_repo,
    availability_status_repo
)
from typing import Type

class ParametricService:
    def __init__(self, repository: BaseRepository):
        """
        Servicio genérico para manejar tablas paramétricas.
        :param repository: Una instancia de un repositorio para una tabla paramétrica.
        """
        self.repository = repository

    def get_all(self, db: Session) -> list:
        """Obtiene todos los registros de una tabla paramétrica."""
        return self.repository.get_multi(db, limit=200) # Aumentamos el límite para tablas de opciones

    def get_by_id(self, db: Session, id: int):
        """Obtiene un registro por su ID."""
        record = self.repository.get(db, id=id)
        if not record:
            raise RecordNotFoundError(f"Record with id {id} not found in {self.repository.model.__tablename__}.")
        return record

# --- Creamos una instancia del servicio para cada tabla paramétrica ---
# Le pasamos a cada servicio el repositorio correspondiente.

document_type_service = ParametricService(document_type_repo)
gender_service = ParametricService(gender_repo)
operational_role_service = ParametricService(operational_role_repo)
availability_status_service = ParametricService(availability_status_repo)