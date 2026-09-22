# Windows/PowerShell, com o ambiente virtual ativado: .\gerar_stubs.ps1
$ErrorActionPreference = "Stop"
Push-Location $PSScriptRoot
try {
    python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. servico.proto
    if ($LASTEXITCODE -ne 0) {
        throw "Falha ao gerar os stubs. Instale as dependencias de requirements.txt."
    }
    Write-Host "Stubs gerados: servico_pb2.py e servico_pb2_grpc.py"
} finally {
    Pop-Location
}
