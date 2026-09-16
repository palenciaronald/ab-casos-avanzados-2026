#!/usr/bin/env bash
# Descarga los 8 datasets del curso desde Kaggle a data/<tema>/
# Requisitos:
#   1. pip install kaggle   (o pip install -r requirements.txt)
#   2. Credenciales en ~/.kaggle/kaggle.json  (chmod 600)
#      Se obtienen en Kaggle > Account > Create New API Token
#
# Uso:  bash scripts/download_data.sh

set -euo pipefail

# Ubicarse en la raíz del proyecto (carpeta padre de este script)
cd "$(dirname "$0")/.."

if ! command -v kaggle >/dev/null 2>&1; then
  echo "ERROR: 'kaggle' no está instalado. Ejecuta: pip install -r requirements.txt" >&2
  exit 1
fi

if [ ! -f "${HOME}/.kaggle/kaggle.json" ]; then
  echo "ERROR: falta ~/.kaggle/kaggle.json (credenciales de Kaggle)." >&2
  echo "       Descárgalo desde Kaggle > Account > Create New API Token y colócalo ahí." >&2
  echo "       Luego: chmod 600 ~/.kaggle/kaggle.json" >&2
  exit 1
fi

echo "==> Tema 1: Clasificación (score de riesgo)"
kaggle datasets download -d kabure/german-credit-data-with-risk        -p ./data/01-clasificacion  --unzip
kaggle datasets download -d parisrohan/credit-score-classification     -p ./data/01-clasificacion  --unzip

echo "==> Tema 1: Clusterización (segmentación)"
kaggle datasets download -d vjchoudhary7/customer-segmentation-tutorial-in-python -p ./data/02-clusterizacion --unzip
kaggle datasets download -d arjunbhasin2013/ccdata                     -p ./data/02-clusterizacion --unzip

echo "==> Tema 2: Regresión (liquidez)"
kaggle datasets download -d rish59/financial-statements-of-major-companies2009-2023 -p ./data/03-regresion --unzip
kaggle datasets download -d fedesoriano/company-bankruptcy-prediction  -p ./data/03-regresion     --unzip

echo "==> Tema 3: NLP (sentimientos)"
kaggle datasets download -d ankurzing/sentiment-analysis-for-financial-news -p ./data/04-nlp       --unzip
kaggle datasets download -d sbhatti/financial-sentiment-analysis       -p ./data/04-nlp           --unzip

echo ""
echo "Descarga completa. Archivos en data/<tema>/:"
find data -type f ! -name ".gitkeep" | sort
