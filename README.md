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
* `.env.prod`: Para el ambiente de producción.

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
cd ..

```