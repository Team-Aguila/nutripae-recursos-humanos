# PAE Recursos Humanos API

Backend para la gestión del personal y su disponibilidad en el sistema PAE (Programa de Alimentación Escolar).

## Características

- ✅ **Gestión de Empleados**: CRUD completo de empleados
- ✅ **Disponibilidad Diaria**: Gestión de disponibilidad del personal
- ✅ **Datos Paramétricos**: Tipos de documento, géneros, roles operacionales
- ✅ **Autenticación JWT**: Integración con el módulo NutriPAE-AUTH
- ✅ **Autorización Delegada**: Sin lógica de auth, solo especifica permisos
- ✅ **API REST**: Endpoints RESTful con documentación Swagger
- ✅ **Base de Datos**: PostgreSQL con Alembic para migraciones

## Autenticación y Autorización

Este módulo **NO contiene lógica de autenticación**. Se integra completamente con el servicio `pae-auth` de forma transparente:

### Arquitectura de Seguridad

1. **Sin lógica JWT**: Este módulo no conoce la estructura de tokens JWT
2. **Sin mapeo de permisos**: No contiene lógica de conversión acción→permiso
3. **Solo especifica permisos**: Cada endpoint declara qué permiso necesita
4. **Delegación completa**: El servicio `pae-auth` maneja toda la validación

### Permisos Requeridos

Cada endpoint especifica directamente el permiso que necesita:

- `nutripae-rh:create` - Crear empleados y disponibilidades
- `nutripae-rh:read` - Leer información específica
- `nutripae-rh:list` - Listar empleados y disponibilidades  
- `nutripae-rh:update` - Actualizar información
- `nutripae-rh:delete` - Eliminar registros

### Flujo de Autenticación Simplificado

1. **Cliente envía token**: Include `Authorization: Bearer <token>` en el request
2. **Módulo especifica permiso**: Cada endpoint declara qué permiso necesita
3. **Delegación al servicio auth**: Se envía token + permiso al servicio `pae-auth`
4. **Respuesta binaria**: El servicio auth responde SÍ/NO autorizado
5. **Ejecución**: Si autorizado, ejecuta el endpoint; sino, retorna 403

### Configuración de Swagger

La documentación incluye soporte para JWT Bearer tokens. En `/docs`:
1. Haz clic en "Authorize" 
2. Ingresa tu token JWT (sin "Bearer ")
3. Todos los requests incluirán automáticamente el token

## Requisitos

- Python 3.10+
- PostgreSQL
- Servicio NutriPAE-AUTH ejecutándose y accesible

## Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# Database Configuration
POSTGRES_USER=pae_user
POSTGRES_PASSWORD=pae_password
POSTGRES_DB=pae_recursos_humanos
DB_HOST=localhost
DB_HOST_PORT=5432

# Authentication Service Configuration
NUTRIPAE_AUTH_HOST=localhost
NUTRIPAE_AUTH_PORT=8001
NUTRIPAE_AUTH_PREFIX_STR=/api/v1
```

**Nota**: No se requieren variables JWT (SECRET_KEY, ALGORITHM) ya que este módulo no maneja tokens directamente.

## Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <repo-url>
   cd pae-recursos-humanos
   ```

2. **Instalar dependencias**
   ```bash
   poetry install
   ```

3. **Configurar variables de entorno**
   ```bash
   cp .env.example .env
   # Editar .env con tus configuraciones
   ```

4. **Ejecutar migraciones**
   ```bash
   poetry run poe db-migrate
   ```

5. **Iniciar el servidor**
   ```bash
   poetry run poe dev
   ```

La API estará disponible en `http://localhost:8000`

## Documentación de la API

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Desarrollo

### Comandos útiles

```bash
# Servidor de desarrollo
poetry run poe dev

# Ejecutar tests
poetry run poe test

# Generar migración
poetry run poe db-generate -m "descripción del cambio"

# Aplicar migraciones
poetry run poe db-migrate
```

### Estructura del Proyecto

```
src/
├── core/
│   ├── config.py           # Configuración de la aplicación (sin JWT)
│   └── dependencies.py     # Middleware minimalista de auth
├── routes/
│   ├── employees.py        # Rutas de empleados
│   ├── dailyAvailabilities.py # Rutas de disponibilidad
│   └── parametrics.py      # Rutas de datos paramétricos
├── services/              # Lógica de negocio
├── repositories/          # Acceso a datos
├── models/               # Modelos de base de datos
├── schemas/              # Schemas Pydantic
└── main.py              # Punto de entrada

```

### Principios de Diseño

- **Separación de responsabilidades**: Sin lógica de autenticación
- **Declarativo**: Cada endpoint especifica claramente sus permisos
- **Delegación**: Toda validación se delega al servicio especializado
- **Simplicidad**: Código mínimo y enfocado en la funcionalidad de negocio

## Integración con otros Módulos

Este módulo se integra con:

- **pae-auth**: Autenticación y autorización (DEPENDENCIA CRÍTICA)
- **pae-inventarios**: (futuro) Gestión de inventarios
- **pae-menu**: (futuro) Planificación de menús

## Contribución

1. Crear una rama para tu feature
2. Realizar los cambios
3. Ejecutar tests
4. Crear un Pull Request

## Licencia

[MIT License](LICENSE)

# Modulo de Recursos Humanos

Este repositorio usa el branchnig model git-flow por lo tanto, para crear una nueva feature hay que usar el comando:

```bash
git flow feature start feature-name
```

Una vez se hayan commitieado los cambios, se debe hacer:

```bash
git flow feature finish
```

Para generar las migraciones con alembic, hay que ejecutar el comando:

```bash
poetry run alembic revision --autogenerate  
```

luego para correr las migraciones, hay que ejecutar el commando:

```bash
poetry run alembic upgrade head  
```

# Gestión de Ambientes con Docker

Este proyecto utiliza Docker y Docker Compose para gestionar de forma aislada los ambientes de desarrollo, testing y producción.

## Prerrequisitos

* Tener instalado [Docker](https://www.docker.com/get-started).
* Tener instalado [Docker Compose](https://docs.docker.com/compose/install/).

## Configuración Inicial

Antes de levantar cualquier ambiente, es necesario crear los archivos de entorno correspondientes. El proyecto buscará los siguientes archivos:

* `.env.development`: Para el ambiente de desarrollo.
* `.env.test`: Para el ambiente de pruebas.

Puedes usar los archivos `.env.example` como plantilla para crearlos.

## Estructura de Archivos

Para que los comandos funcionen correctamente, se espera la siguiente estructura de archivos en la raíz del proyecto:

## Entorno de Desarrollo

Utilizado para el desarrollo diario. Incluye *hot-reloading* para que los cambios en el código se reflejen al instante sin necesidad de reconstruir la imagen.

**1. Levantar el ambiente:**

```bash
cd compose/dev &&
docker-compose up --build -d &&
cd ../..
```


**2. Detener el ambiente:**

```bash
cd compose/dev &&
docker-compose down -v --remove-orphans &&
cd ../..
```

## Entorno de Pruebas 

**1. Lanzar las pruebas:**

```bash
cd compose/test && 
docker compose up --build --abort-on-container-exit --exit-code-from api-test &&
docker compose down -v --remove-orphans &&
cd ../..

```