# Servidor da calculadora gRPC: soma e multiplicação.
from concurrent import futures

import grpc
import servico_pb2
import servico_pb2_grpc


def criar_resultado(valor, context):
    # O contrato usa int32, mesmo que Python aceite inteiros maiores.
    if not -(2**31) <= valor <= 2**31 - 1:
        context.abort(grpc.StatusCode.OUT_OF_RANGE, "Resultado fora do limite de int32.")
    return servico_pb2.Resultado(valor=valor)


class CalculadoraServicer(servico_pb2_grpc.CalculadoraServicer):
    def Somar(self, request, context):
        return criar_resultado(request.a + request.b, context)

    def Multiplicar(self, request, context):
        return criar_resultado(request.a * request.b, context)


def main():
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servico_pb2_grpc.add_CalculadoraServicer_to_server(CalculadoraServicer(), servidor)
    servidor.add_insecure_port("127.0.0.1:50051")
    servidor.start()
    print("[servidor gRPC] ouvindo em 127.0.0.1:50051", flush=True)
    try:
        servidor.wait_for_termination()
    except KeyboardInterrupt:
        servidor.stop(grace=2).wait()


if __name__ == "__main__":
    main()
