# Execute em outro terminal, com o servidor funcionando.
import grpc
import servico_pb2
import servico_pb2_grpc


def main():
    with grpc.insecure_channel("127.0.0.1:50051") as canal:
        stub = servico_pb2_grpc.CalculadoraStub(canal)
        operandos = servico_pb2.Operandos(a=2, b=3)
        try:
            soma = stub.Somar(operandos, timeout=5)
            produto = stub.Multiplicar(operandos, timeout=5)
        except grpc.RpcError as erro:
            print(f"Erro gRPC: {erro.code().name} - {erro.details()}")
            raise SystemExit(1)

        print("2 + 3 =", soma.valor)
        print("2 * 3 =", produto.valor)
        if soma.valor != 5 or produto.valor != 6:
            raise SystemExit("Falha: os resultados não correspondem ao esperado.")
        print("Conferência concluída: os dois resultados estão corretos.")


if __name__ == "__main__":
    main()
