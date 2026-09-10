# carga.py — CASA da Aula 3: teste de carga do servidor multicliente.
import socket
import threading
import time

HOST, PORT = "127.0.0.1", 5000
N = 100                       # experimente depois com 10, 50, 100
MENSAGENS = 5

tempos = []                  # cada cliente anota aqui quanto levou

def um_cliente(i):
    t0 = time.perf_counter()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    for _ in range(MENSAGENS):
        s.sendall(b"ola")
        s.recv(1024)
    s.close()
    tempos.append(time.perf_counter() - t0)

# TODO 1: crie N objetos threading.Thread, cada um com target=um_cliente e args=(i,)
threads = []
for i in range(N):
    t = threading.Thread(target=um_cliente, args=(i,))
    threads.append(t)

inicio = time.perf_counter()

# TODO 2: start() em todas as threads
for t in threads:
    t.start()

# TODO 3: join() em todas as threads (esperar terminarem) antes de medir o total
for t in threads:
    t.join()

total = time.perf_counter() - inicio

media = sum(tempos) / len(tempos) if tempos else 0
print(f"N={N} clientes | tempo total: {total * 1000:.1f} ms | "
      f"media por cliente: {media * 1000:.1f} ms")
print("Repita com N=10, 50, 100 e anote no relatorio_concorrencia.md.")