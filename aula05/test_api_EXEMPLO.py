# Os três testes solicitados na atividade. Execute: python -m pytest -v
from itertools import count

import pytest
from fastapi.testclient import TestClient
import app as modulo_app


@pytest.fixture
def cliente(monkeypatch):
    # Cada teste começa com dados próprios e não depende dos outros.
    monkeypatch.setattr(modulo_app, "tarefas", [])
    monkeypatch.setattr(modulo_app, "ids", count(1))
    with TestClient(modulo_app.app) as client:
        yield client


def test_criar_devolve_201(cliente):
    resposta = cliente.post("/tarefas", json={"titulo": "estudar SD"})
    assert resposta.status_code == 201
    assert resposta.json() == {"id": 1, "titulo": "estudar SD"}


def test_listar_devolve_200(cliente):
    criada = cliente.post("/tarefas", json={"titulo": "revisar REST"})
    assert criada.status_code == 201
    resposta = cliente.get("/tarefas")
    assert resposta.status_code == 200
    assert isinstance(resposta.json(), list)
    assert resposta.json() == [criada.json()]


def test_id_inexistente_devolve_404(cliente):
    resposta = cliente.get("/tarefas/9999")
    assert resposta.status_code == 404
    assert resposta.json() == {"detail": "tarefa não encontrada"}
