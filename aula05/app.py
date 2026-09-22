# Aula 5 — API REST de tarefas com CRUD completo.
# Execute: python -m uvicorn app:app --reload --port 8000
# Documentação: http://127.0.0.1:8000/docs
from itertools import count
from threading import Lock

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel

app = FastAPI(title="API de Tarefas")
tarefas = []  # Banco em memória: os dados desaparecem ao reiniciar.
ids = count(1)  # Evita IDs duplicados quando uma tarefa é removida.
trava = Lock()


class Tarefa(BaseModel):
    titulo: str


class TarefaResposta(Tarefa):
    id: int


ERRO_404 = {404: {"description": "Tarefa não encontrada"}}


def buscar_tarefa(tid: int):
    # Chamado pelas rotas enquanto a trava está adquirida.
    for tarefa in tarefas:
        if tarefa["id"] == tid:
            return tarefa
    raise HTTPException(status_code=404, detail="tarefa não encontrada")


@app.get("/tarefas", response_model=list[TarefaResposta])
def listar():
    with trava:
        return [tarefa.copy() for tarefa in tarefas]


@app.post("/tarefas", status_code=status.HTTP_201_CREATED, response_model=TarefaResposta)
def criar(tarefa: Tarefa):
    with trava:
        nova = {"id": next(ids), "titulo": tarefa.titulo}
        tarefas.append(nova)
        return nova.copy()


@app.get("/tarefas/{tid}", response_model=TarefaResposta, responses=ERRO_404)
def obter(tid: int):
    with trava:
        return buscar_tarefa(tid).copy()


@app.put("/tarefas/{tid}", response_model=TarefaResposta, responses=ERRO_404)
def atualizar(tid: int, tarefa: Tarefa):
    with trava:
        existente = buscar_tarefa(tid)
        existente["titulo"] = tarefa.titulo
        return existente.copy()  # 200: devolve a tarefa atualizada.


@app.delete(
    "/tarefas/{tid}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    responses=ERRO_404,
)
def remover(tid: int):
    with trava:
        existente = buscar_tarefa(tid)
        tarefas.remove(existente)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
