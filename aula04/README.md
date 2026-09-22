# Calculadora gRPC — ampliação do contrato

Atividade da Aula 4 de Sistemas Distribuídos e Computação em Nuvem.

## Objetivo e implementação

O projeto permite executar duas operações em um servidor a partir de um cliente Python: `Somar` e `Multiplicar`. Ambas recebem a mensagem `Operandos`, com os inteiros `a` e `b`, e retornam `Resultado`, com o campo `valor`.

Foi acrescentado `Multiplicar` ao contrato original, implementado o cálculo no servidor e atualizado o cliente para chamar e conferir as duas operações. O endereço original foi mantido: `127.0.0.1:50051`. O servidor usa um pool de dez threads. Este exemplo é executado localmente e usa um canal sem TLS.

## Arquivos

| Arquivo | Função |
| --- | --- |
| `servico.proto` | Define o serviço, os dois métodos e as mensagens. |
| `servidor_grpc.py` | Implementa as operações e inicia o servidor. |
| `cliente_grpc.py` | Chama os dois métodos e confere os resultados. |
| `servico_pb2.py` | Classes de mensagens geradas automaticamente. |
| `servico_pb2_grpc.py` | Stub do cliente e registro do serviço gerados automaticamente. |
| `gerar_stubs.ps1` | Facilita a geração no PowerShell. |
| `requirements.txt` | Versões das dependências usadas no projeto. |

Copie os arquivos para a mesma pasta do projeto, substituindo os arquivos de mesmo nome. Os arquivos gerados já acompanham a entrega; o comando abaixo permite reproduzi-los. Não os edite manualmente.

## Executar no macOS ou Linux

É necessário Python 3.10 ou superior. No terminal, entre na pasta dos arquivos e execute:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. servico.proto
python servidor_grpc.py
```

Mantenha esse terminal aberto. Abra outro terminal na mesma pasta:

```bash
source .venv/bin/activate
python cliente_grpc.py
```

## Executar no Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. servico.proto
python servidor_grpc.py
```

Para gerar os stubs, também é possível usar ` .\gerar_stubs.ps1` com o ambiente ativado. Em outro terminal, na mesma pasta:

```powershell
.\.venv\Scripts\Activate.ps1
python cliente_grpc.py
```

## Resultado esperado

```text
2 + 3 = 5
2 * 3 = 6
Conferência concluída: os dois resultados estão corretos.
```

O cliente encerra com erro se o resultado divergir do esperado ou se a chamada falhar. Cada chamada tem limite de cinco segundos. Para encerrar o servidor, pressione `Ctrl+C` no primeiro terminal.

## O que acontece quando o contrato muda?

O `.proto` define a interface compartilhada. Os arquivos gerados traduzem essa definição para Python. Alterar somente o `.proto` não atualiza automaticamente o código que cliente e servidor importam.

### Renomear um campo

Se `int32 a = 1` virar `int32 primeiro = 1`, os novos objetos Python usarão `primeiro`. É necessário ajustar `Operandos(a=2, ...)` e `request.a` nos códigos que adotarem a nova definição.

Preservar número e tipo mantém a compatibilidade binária dessa renomeação: no tráfego Protobuf, o campo é identificado pelo número, não pelo nome. A API Python muda, e formatos baseados em nomes, como JSON, também podem ser afetados.

### Trocar um tipo

Trocar `int32` por `string` no mesmo campo é incompatível no formato binário. Regenerar os arquivos não torna versões incompatíveis interoperáveis. É necessário adaptar o código e coordenar a mudança; uma alternativa é criar um novo campo com outro número. Algumas trocas numéricas têm compatibilidade condicional, mas podem causar perda de informação. Números removidos não devem ser reutilizados.

### Por que atualizar os dois lados?

Para os dois lados adotarem o contrato ampliado, devem usar código gerado a partir da definição atualizada. O stub antigo do cliente não expõe `Multiplicar`; um servidor antigo não registra esse método e retorna `UNIMPLEMENTED` ao receber a chamada. Mesmo com arquivos novos, é necessário implementar a operação no servidor.

Nesta atividade, regeneramos os dois arquivos, disponibilizamos as versões atualizadas ao cliente e ao servidor e reiniciamos os processos. Em uma implantação separada, cada lado pode gerar seu código ou receber os arquivos gerados pela construção do projeto.

Uma extensão compatível não obriga todos os clientes antigos a atualizar imediatamente: um cliente que usa apenas `Somar` pode continuar funcionando. A atualização é necessária para adotar a nova interface.

## Limites dos cálculos

Os campos continuam sendo `int32`, como no projeto original. Se a soma ou o produto ultrapassar o intervalo de -2.147.483.648 a 2.147.483.647, o servidor retorna `OUT_OF_RANGE`.

## Referências

- [Documentação oficial do gRPC para Python](https://grpc.io/docs/languages/python/quickstart/)
- [Guia oficial de Protocol Buffers — proto3](https://protobuf.dev/programming-guides/proto3/)
