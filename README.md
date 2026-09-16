# Laboratorio de Casos Avanzados — Maestría en Ingeniería Analítica (2026)

Curso 100% aplicado (24 h, 3 fines de semana). Cada tema tiene dos notebooks:
un **demo del viernes** (resuelto, ejecutado en vivo por el instructor) y una
**plantilla del sábado** (con secciones en blanco que el estudiante completa
como entrega).

## Calendario y temas

| FDS | Fechas | Tema | Demo (viernes) | Ejercicio (sábado) |
|-----|--------|------|----------------|--------------------|
| 1 | 18–19 sep | Clasificación (score de riesgo) | German Credit Data | Credit Score Classification |
| 1 | 18–19 sep | Clusterización (segmentación) | Mall Customer Segmentation | Credit Card Clustering |
| 2 | 25–26 sep | Regresión (liquidez) | Financial Statements 2009-2023 | Company Bankruptcy (Taiwan) |
| 3 | 2–3 oct | NLP (sentimientos) | Financial PhraseBank | Financial Sentiment (FiQA+PB) |

## Estructura del repositorio

```
.
├── data/                 # datasets (NO versionados — se descargan)
│   ├── 01-clasificacion/
│   ├── 02-clusterizacion/
│   ├── 03-regresion/
│   └── 04-nlp/
├── notebooks/            # notebooks demo (viernes) y plantilla (sábado)
│   ├── 01-clasificacion/
│   ├── 02-clusterizacion/
│   ├── 03-regresion/
│   └── 04-nlp/
├── ppts/                 # presentaciones de teoría (~1h por viernes)
│   ├── 01-clasificacion/
│   ├── 02-clusterizacion/
│   ├── 03-regresion/
│   └── 04-nlp/
├── scripts/
│   └── download_data.sh  # descarga los 8 datasets vía Kaggle API
├── requirements.txt
└── README.md
```

Los `.md` de la raíz (`00-curso-general.md` y `01`–`04`) son el diseño
pedagógico de referencia de cada tema.

## Setup

```bash
# 1. Entorno virtual (recomendado)
python3 -m venv .venv
source .venv/bin/activate

# 2. Dependencias
pip install -r requirements.txt

# 3. NLP: recursos de NLTK (solo Tema 4)
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"
```

## Descarga de datasets

Los datasets vienen de Kaggle y no se pueden bajar por link directo.

### Opción A — Kaggle API (automático)

Requiere credenciales de Kaggle:

1. En Kaggle: **Account → Create New API Token** (descarga `kaggle.json`).
2. Colócalo en `~/.kaggle/kaggle.json` y protégelo:
   ```bash
   mkdir -p ~/.kaggle && mv ~/Downloads/kaggle.json ~/.kaggle/
   chmod 600 ~/.kaggle/kaggle.json
   ```
3. Ejecuta el script:
   ```bash
   bash scripts/download_data.sh
   ```

### Opción B — Descarga manual

Entra a cada dataset de la tabla (logueado en Kaggle), dale **Download** y
ubica los CSV en la carpeta correspondiente de `data/<tema>/`. Las rutas
relativas de los notebooks esperan los archivos ahí.

## Convención de los notebooks

- **Semilla anti-copia:** la primera celda de código define
  `cedula = <número>` y `np.random.seed(cedula)`. Esa semilla alimenta el
  `random_state` de los splits/modelos y un muestreo
  `df.sample(frac=0.85, random_state=cedula)`, de modo que cada estudiante
  obtiene resultados ligeramente distintos sobre la misma base.
- **Plantilla del sábado:** secciones 1–2 resueltas como ejemplo; secciones
  intermedias con Markdown explicativo + celda de código en blanco con
  comentarios `# TODO:`; cierre con 2–3 preguntas abiertas de interpretación
  de negocio.

## Stack

Python 3.x · pandas · numpy · scikit-learn · matplotlib · seaborn ·
statsmodels (VIF) · nltk (NLP) · Jupyter. Todo corre en Colab o local sin GPU.
