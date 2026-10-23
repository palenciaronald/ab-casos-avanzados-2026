<#
Ejecuta un notebook del ejemplo desde un entorno limpio y falla si algo no corre.

Uso (desde la raíz del repo):
    ejemplo\scripts\verify_stage.ps1 ejemplo\notebooks\02_eda.ipynb
    ejemplo\scripts\verify_stage.ps1 ejemplo\notebooks\02_eda.ipynb -Reuse   # reutiliza .verify-venv

Requisitos: uv instalado. Crea .verify-venv (ignorado por Git) con Python 3.12.
#>
param(
    [Parameter(Mandatory = $true)][string]$Notebook,
    [switch]$Reuse
)

# No usar "Stop": PowerShell 5.1 trata como error lo que uv escribe en stderr; se revisa $LASTEXITCODE.
$ErrorActionPreference = "Continue"
$env:PYTHONUTF8 = "1"
$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$venv = Join-Path $root ".verify-venv"
$py = Join-Path $venv "Scripts\python.exe"

if (-not $Reuse -and (Test-Path $venv)) { Remove-Item -Recurse -Force $venv }
if (-not (Test-Path $py)) {
    uv venv --python 3.12 $venv
    if ($LASTEXITCODE -ne 0) { throw "No se pudo crear el entorno" }
    uv pip install --python $py -r (Join-Path $root "requirements.txt")
    if ($LASTEXITCODE -ne 0) { throw "No se pudo instalar requirements.txt" }
}

$nb = Resolve-Path $Notebook
$env:PYTHONPATH = Join-Path $root "ejemplo\src"
& $py -m nbconvert --to notebook --execute --output-dir (Join-Path $root ".verify-out") $nb
if ($LASTEXITCODE -ne 0) { throw "El notebook falló: $Notebook" }
Write-Host "OK: $Notebook se ejecutó sin errores."
