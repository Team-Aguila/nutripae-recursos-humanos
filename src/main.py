from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from routes import employees, dailyAvalabilities, parametrics
from core.config import settings
from utils.telemetrics import PrometheusMiddleware, metrics, setting_otlp
import logging
import uvicorn

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="API de Recursos Humanos PAE",
        version="1.0.0",
        description="Backend para la gestión del personal y su disponibilidad.",
        routes=app.routes,
    )
    
    # Define the security scheme for JWT Bearer tokens
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter your JWT token obtained from the NutriPAE-AUTH service /auth/login endpoint"
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app = FastAPI(
    title=settings.APP_NAME,
    description="Backend para la gestión del personal y su disponibilidad.",
    version="1.0.0",
)

app.add_middleware(PrometheusMiddleware, app_name=settings.APP_NAME)
app.add_route("/metrics", metrics)
# Setting OpenTelemetry exporter
setting_otlp(app, settings.APP_NAME, settings.OTLP_GRPC_ENDPOINT)

class EndpointFilter(logging.Filter):
    # Uvicorn endpoint access log filter
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("GET /metrics") == -1


# Filter out /endpoint
logging.getLogger("uvicorn.access").addFilter(EndpointFilter())
# Set custom OpenAPI schema
app.openapi = custom_openapi

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las origenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los headers
)

# Incluimos los routers en la aplicación principal con prefijo de API
app.include_router(
    employees.router, 
    prefix=settings.API_PREFIX_STR,
    tags=["Employees"]
)
app.include_router(
    dailyAvalabilities.router, 
    prefix=settings.API_PREFIX_STR,
    tags=["Daily Availabilities"]
)
app.include_router(
    parametrics.router, 
    prefix=settings.API_PREFIX_STR,
    tags=["Parametrics"]
)

@app.get(f"{settings.API_PREFIX_STR}", tags=["Root"])
def api_root():
    return {
        "message": "Bienvenido a la API de Recursos Humanos del PAE",
        "description": "Gestión del personal y su disponibilidad",
        "version": "1.0.0",
        "docs_url": "/docs",
        "module_identifier": settings.MODULE_IDENTIFIER,
        "auth_service": settings.NUTRIPAE_AUTH_URL,
        "features": [
            "Gestión de Empleados",
            "Disponibilidad Diaria",
            "Datos Paramétricos",
            "Autenticación JWT",
            "Autorización Granular"
        ]
    }

@app.get("/", tags=["Root"])
def root():
    return {"status": "healthy", "service": "pae-recursos-humanos"}


if __name__ == "__main__":
    # update uvicorn access logger format
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"][
        "fmt"
    ] = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=log_config)