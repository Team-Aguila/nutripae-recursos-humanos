# app/exceptions.py

class RecordNotFoundError(Exception):
    """Se lanza cuando un registro no se encuentra en la base de datos."""
    pass

class DuplicateRecordError(Exception):
    """Se lanza cuando se intenta crear un registro que viola una restricción de unicidad."""
    pass
