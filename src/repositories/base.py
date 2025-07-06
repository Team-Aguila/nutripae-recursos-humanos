from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union, Callable

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session, Query
from models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        Repositorio base con operaciones CRUD genéricas.
        :param model: El modelo de SQLAlchemy
        """
        self.model = model

    def get(self, db: Session, id: Any, *, options: Optional[Callable[[Query], Query]] = None) -> Optional[ModelType]:
        query = db.query(self.model)
        if options:
            query = options(query)
        return query.filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> list[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        # Pydantic v2 usa model_dump() en lugar de dict()
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)  # Desempaqueta el diccionario
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any]
    ) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            # Pydantic v2 usa model_dump() con exclude_unset=True
            update_data = obj_in.model_dump(exclude_unset=True)
        
        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int, options: Optional[Callable[[Query], Query]] = None) -> Optional[ModelType]:
        # Usamos get para poder aplicar las mismas opciones de carga
        obj = self.get(db, id, options=options)
        if obj:
            db.delete(obj)
            db.commit()
        return obj