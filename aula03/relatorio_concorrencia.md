# Relatório de Teste de Carga - Concorrência

**Aluno:** Juan Carlos Oliveira Cunha  
**Curso:** Análise e Desenvolvimento de Sistemas (FAESA)  
**Disciplina:** Sistemas Distribuídos e Computação em Nuvem  

## 1. Resultados das Medições

### Servidor Single-Thread (Aula 2)
| Número de Clientes (N) | Tempo Total (ms) | Tempo Médio por Cliente (ms) |
| :--- | :--- | :--- |
| **10** | Falha (Conexão encerrada) | Falha (Conexão encerrada) |
| **50** | Falha (Conexão encerrada) | Falha (Conexão encerrada) |
| **100** | Falha (Conexão encerrada) | Falha (Conexão encerrada) |

### Servidor Multi-Thread (Aula 3)
| Número de Clientes (N) | Tempo Total (ms) | Tempo Médio por Cliente (ms) |
| :--- | :--- | :--- |
| **10** | 2.8 ms | 2.2 ms |
| **50** | 11.7 ms | 4.4 ms |
| **100** | 16.0 ms | 4.8 ms |

## 2. Análise de Desempenho

**Onde o servidor single-thread trava e por quê?**
O servidor da Aula 2 processa estritamente uma conexão por vez e, na implementação testada, não possui um loop para continuar ouvindo a porta. Quando o cliente A conecta, o servidor bloqueia para atendê-lo. Se os outros 99 clientes tentarem conectar simultaneamente, eles entram em uma fila do sistema operacional (backlog) que rapidamente estoura, resultando em múltiplas exceções de conexão recusada. O gargalo é de concorrência e I/O: o servidor não consegue lidar com novos clientes enquanto atende o atual, causando a quebra do serviço sob carga.

**Por que o servidor multi-thread resolve esse gargalo?**
No servidor multicliente da Aula 3, a thread principal existe apenas para executar o `accept()`. Assim que uma conexão chega, o socket é repassado para uma nova thread independente e a thread principal volta imediatamente a ouvir a porta 5000. Isso permite concorrência: enquanto uma thread está bloqueada esperando pacotes de um cliente (I/O), o sistema operacional alterna o contexto para outra thread que já tem pacotes prontos para processar. Dessa forma, as esperas de rede se sobrepõem no tempo, reduzindo brutalmente o tempo total necessário para processar N clientes em relação à abordagem sequencial e evitando a queda do servidor.