#!/usr/bin/env bash
# Ejecuta un notebook del ejemplo desde un entorno limpio y falla si algo no corre.
#
# Uso (desde la raíz del repo):
#   ejemplo/scripts/verify_stage.sh ejemplo/notebooks/02_eda.ipynb
#   ejemplo/scripts/verify_stage.sh ejemplo/notebooks/02_eda.ipynb --reuse
#
# Requisitos: uv instalado. Crea .verify-venv (ignorado por Git) con Python 3.12.
set -euo pipefail

NOTEBOOK="${1:?Indica el notebook a ejecutar}"
REUSE="${2:-}"
export PYTHONUTF8=1
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
VENV="$ROOT/.verify-venv"

if [ "$REUSE" != "--reuse" ] && [ -d "$VENV" ]; then rm -rf "$VENV"; fi
if [ ! -d "$VENV" ]; then
  uv venv --python 3.12 "$VENV"
  PY="$VENV/bin/python"; [ -x "$PY" ] || PY="$VENV/Scripts/python.exe"
  uv pip install --python "$PY" -r "$ROOT/requirements.txt"
fi
PY="$VENV/bin/python"; [ -x "$PY" ] || PY="$VENV/Scripts/python.exe"

export PYTHONPATH="$ROOT/ejemplo/src"
"$PY" -m nbconvert --to notebook --execute --output-dir "$ROOT/.verify-out" "$NOTEBOOK"
echo "OK: $NOTEBOOK se ejecutó sin errores."
