from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import employees, dailyAvalabilities, parametrics

# Aquí podrías tener configuraciones de CORS, etc.

app = FastAPI(
    title="API de Recursos Humanos PAE",
    description="Backend para la gestión del personal y su disponibilidad.",
    version="1.0.0",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las origenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los headers
)

# Incluimos los routers en la aplicación principal
app.include_router(employees.router)
app.include_router(dailyAvalabilities.router)
app.include_router(parametrics.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bienvenido a la API de Recursos Humanos del PAE"}