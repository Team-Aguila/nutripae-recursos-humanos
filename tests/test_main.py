from fastapi.testclient import TestClient


def test_read_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenido a la API de Recursos Humanos del PAE"} 