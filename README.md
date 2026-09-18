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
├── data/                 # los 8 datasets (versionados; ~43 MB)
│   ├── 01-clasificacion/
│   ├── 02-clusterizacion/
│   ├── 03-regresion/
│   └── 04-nlp/
├── notebooks/            # notebooks demo (viernes) y plantilla (sábado)
│   ├── 01-clasificacion/ #   demo German Credit + plantilla Credit Score
│   ├── 02-clusterizacion/#   demo Mall Customers + plantilla Credit Card
│   ├── 03-regresion/     #   demo Financial Statements + plantilla Taiwan
│   └── 04-nlp/           #   demo PhraseBank + plantilla Financial Sentiment
├── ppts/                 # presentaciones de teoría (~2h por viernes, Marp/ISL, desde cero)
│   ├── 01-clasificacion/
│   ├── 02-clusterizacion/
│   ├── 03-regresion/
│   ├── 04-nlp/
│   └── README.md         #   cómo renderizar las PPTs
├── scripts/
│   └── download_data.sh  # descarga los 8 datasets vía Kaggle API
├── requirements.txt
├── data/README.md        # resumen de las 8 bases
└── README.md
```

Los `.md` de la raíz (`00-curso-general.md` y `01`–`04`) son el diseño
pedagógico de referencia de cada tema.

## Contenido del curso

Cada tema incluye un **notebook demo** (resuelto, ejecutado en vivo el viernes),
una **plantilla** (con secciones `# TODO:` que el estudiante completa el sábado)
y una **PPT de teoría** (~2 h, desde cero, basada en *An Introduction to Statistical
Learning*).

| FDS | Tema | Demo (viernes) | Plantilla (sábado) | Teoría (PPT) |
|-----|------|----------------|--------------------|--------------|
| 1 | Clasificación | `demo_viernes_german_credit.ipynb` | `plantilla_sabado_credit_score.ipynb` | `teoria_clasificacion.md` |
| 1 | Clusterización | `demo_viernes_mall_customers.ipynb` | `plantilla_sabado_credit_card.ipynb` | `teoria_clusterizacion.md` |
| 2 | Regresión | `demo_viernes_financial_statements.ipynb` | `plantilla_sabado_taiwan_bankruptcy.ipynb` | `teoria_regresion.md` |
| 3 | NLP | `demo_viernes_financial_phrasebank.ipynb` | `plantilla_sabado_financial_sentiment.ipynb` | `teoria_nlp_sentimientos.md` |

Los demos están **ejecutados y verificados** (con gráficos incrustados). Las
plantillas tienen las secciones 1–2 resueltas como ejemplo y el resto en `# TODO:`.
Ver `ppts/README.md` para renderizar las presentaciones.

## Setup

```bash
# 1. Entorno virtual (recomendado)
python3 -m venv .venv
source .venv/bin/activate

# 2. Dependencias
pip install -r requirements.txt

# 3. NLP: recursos de NLTK (solo Tema 4)
#    En macOS puede fallar por certificados SSL; el workaround va incluido:
python -c "import ssl, nltk; ssl._create_default_https_context = ssl._create_unverified_context; [nltk.download(r, quiet=True) for r in ['stopwords','wordnet','omw-1.4','punkt','punkt_tab']]"
```

Los notebooks del Tema 4 ya incluyen ese workaround SSL en su primera celda, así
que también funcionan si no ejecutas el comando anterior.

## Datasets

Los 8 datasets **ya vienen incluidos en este repo** (carpeta `data/`, ~43 MB),
así que al clonar tienes todo listo para ejecutar los notebooks. Ver
`data/README.md` para el detalle de cada base.

Si necesitas **regenerarlos** desde el origen (vienen de Kaggle, sin link
directo), tienes dos opciones:

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

## Cómo ejecutar los notebooks

```bash
source .venv/bin/activate
jupyter notebook          # o: jupyter lab
```

Abre el notebook del tema y, en la **primera celda**, reemplaza
`cedula = ...` por tu número de cédula antes de ejecutar (ver convención abajo).
Los demos ya vienen ejecutados; las plantillas se completan celda por celda.

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
