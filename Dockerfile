FROM python:3.11-slim

WORKDIR /app

RUN pip install poetry

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && poetry install --no-root --only main

COPY . .

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]