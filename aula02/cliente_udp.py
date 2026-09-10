# cliente_udp.py — CASA da Aula 2: eco em UDP (cliente)
# Em UDP NAO ha connect(): o endereco vai em cada sendto().
import socket

HOST, PORT = "127.0.0.1", 5001
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # SOCK_DGRAM = UDP
s.settimeout(5)                                        # UDP pode perder: use tempo-limite

mensagem = "oi via UDP"
# Envia a mensagem em bytes junto com o endereco do servidor.
s.sendto(mensagem.encode(), (HOST, PORT))
# Recebe o eco e o endereco de quem respondeu.
eco, endereco = s.recvfrom(1024)
print("eco:", eco.decode())

s.close()
