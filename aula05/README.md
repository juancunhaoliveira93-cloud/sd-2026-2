# Aula 5 — API REST de tarefas com CRUD completo

## O que foi implementado

O projeto original foi ampliado com atualização do título por PUT e remoção por DELETE. Buscar, atualizar ou excluir um ID inexistente retorna 404. Os dois TODOs do arquivo de testes foram preenchidos e o teste de criação foi mantido e aprimorado.

| Método | Rota | Resultado de sucesso |
| --- | --- | --- |
| POST | `/tarefas` | 201 — tarefa criada |
| GET | `/tarefas` | 200 — lista de tarefas |
| GET | `/tarefas/{tid}` | 200 — tarefa encontrada |
| PUT | `/tarefas/{tid}` | 200 — tarefa atualizada |
| DELETE | `/tarefas/{tid}` | 204 — remoção sem corpo na resposta |

`tid` é o ID da tarefa. Foi mantido o nome usado no arquivo original; corresponde ao `{id}` do enunciado. Exemplo: `/tarefas/1`.

POST e PUT recebem JSON no formato:

```json
{"titulo": "Estudar sistemas distribuídos"}
```

A resposta de erro para um ID inexistente é:

```json
{"detail": "tarefa não encontrada"}
```

Corpos sem o campo obrigatório `titulo` e IDs que não são inteiros são rejeitados pela validação com status 422.

## Arquivos para copiar

- `app.py`: substitua o original pela API completa.
- `test_api_EXEMPLO.py`: substitua o original pelos três testes completos.
- `requirements.txt`: dependências com as versões utilizadas na verificação.
- `README.md`: instruções de execução e conferência.

Mantenha os quatro arquivos na mesma pasta da atividade da Aula 5. Caso seu projeto já tenha um requirements.txt com outras dependências, incorpore estas dependências sem remover as demais.

## Preparação no Mac ou Linux

Use Python 3.10 ou superior. Abra um terminal na pasta da atividade:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Preparação no Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Executar os três testes

Com o ambiente ativado:

```bash
python -m pytest test_api_EXEMPLO.py -v
```

Os testes usam o TestClient e não exigem iniciar o Uvicorn. Cada teste usa dados isolados, sem depender da ordem de execução. São verificados criação (201), listagem (200) e busca por ID inexistente (404). O resultado esperado é `3 passed`.

## Iniciar a API e conferir /docs

```bash
python -m uvicorn app:app --reload --port 8000
```

Abra http://127.0.0.1:8000/docs no navegador. A documentação Swagger UI é gerada automaticamente com base nas rotas e nos modelos declarados. Não foi necessário criar uma página de documentação manualmente.

1. Confira as cinco operações, incluindo PUT e DELETE.
2. Em POST `/tarefas`, clique em **Try it out**, informe um título no JSON e clique em **Execute**. Confira 201 e anote o ID retornado.
3. Em PUT `/tarefas/{tid}`, informe esse ID e outro título. Confira 200 e o título atualizado.
4. Faça GET pelo mesmo ID e confirme a alteração.
5. Faça DELETE pelo ID. Confira 204, sem corpo na resposta.
6. Busque, atualize ou tente excluir novamente esse ID: o resultado deve ser 404.

O esquema das rotas também pode ser consultado em http://127.0.0.1:8000/openapi.json. Para encerrar o servidor, pressione Ctrl+C.

## Armazenamento da atividade

As tarefas ficam apenas na memória, como no exemplo fornecido. Reiniciar o servidor ou recarregar o código apaga os dados. Execute com um único processo: não use múltiplos workers para compartilhar essa lista.

Foi usado um contador para os IDs: calcular `len(tarefas) + 1` poderia gerar um ID já existente depois de uma exclusão. Uma trava protege o acesso à lista durante as operações concorrentes do mesmo processo.

## Referências

- https://fastapi.tiangolo.com/tutorial/testing/
- https://fastapi.tiangolo.com/tutorial/response-status-code/
