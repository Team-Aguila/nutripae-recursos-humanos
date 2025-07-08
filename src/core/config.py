import os
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Variables de entorno para la base de datos
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DB_HOST: str = "localhost" # Default to localhost for local development
    DB_HOST_PORT: int = 5432

    # URL de la base de datos (construida a partir de las variables anteriores)
    DATABASE_URL: str | None = None

    @field_validator("DATABASE_URL", mode='before')
    @classmethod
    def assemble_db_connection(cls, v: str | None, values) -> any:
        if isinstance(v, str):
            return v
        
        data = values.data
        return f"postgresql+psycopg2://{data.get('POSTGRES_USER')}:{data.get('POSTGRES_PASSWORD')}@{data.get('DB_HOST')}:{data.get('DB_HOST_PORT')}/{data.get('POSTGRES_DB')}"

    API_PREFIX_STR: str = "/api/v1"
    MODULE_IDENTIFIER: str = "nutripae-rh"

    # Configuración del servicio de autenticación
    NUTRIPAE_AUTH_HOST: str
    NUTRIPAE_AUTH_PORT: int
    NUTRIPAE_AUTH_PREFIX_STR: str = "/api/v1"
    NUTRIPAE_AUTH_URL: str | None = None
    
    
    
    def assemble_nutripae_auth_url(cls, v: str | None, values) -> any:
        if isinstance(v, str):
            return v
        
        data = values.data
        return f"http://{data.get('NUTRIPAE_AUTH_HOST')}:{data.get('NUTRIPAE_AUTH_PORT')}{data.get('NUTRIPAE_AUTH_PREFIX_STR')}"

    model_config = SettingsConfigDict(
        env_file=f".env",
        extra="ignore"
    )

# Instancia global de la configuración
settings = Settings()