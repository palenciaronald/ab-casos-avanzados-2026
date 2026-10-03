# Casos Avanzados de Machine Learning — Maestría en Ingeniería Analítica (2026)

Material del curso: presentaciones de teoría, datasets y notebooks de cada tema.
Cada tema tiene:

- una **presentación de teoría** (viernes),
- un **notebook demo** (resuelto en clase, el viernes),
- una **plantilla** con secciones `# TODO:` que **tú completas** (sábado) y entregas.

## Temas

| FDS | Tema | Demo (viernes) | Ejercicio (sábado) | Teoría |
|-----|------|----------------|--------------------|--------|
| 1 | Clasificación (score de riesgo) | German Credit | Credit Score Classification | `ppts/01-clasificacion/` |
| 2 | Clusterización (segmentación) | Mall Customers | Credit Card Clustering | `ppts/02-clusterizacion/` |
| 3 | Regresión (liquidez) | Financial Statements | Company Bankruptcy (Taiwan) | `ppts/03-regresion/` |

> El material del tema 4 (NLP) se agrega al repositorio cuando se dicte.

## Estructura

```
.
├── ppts/          # presentaciones: abre el .html en el navegador (el .md es la fuente)
├── notebooks/     # demo_viernes_*.ipynb y plantilla_sabado_*.ipynb por tema
├── data/          # datasets de cada tema (ver data/README.md)
├── INSTRUCCIONES_ENTREGA.md   # cómo nombrar y subir tus laboratorios
└── requirements.txt
```

## Cómo trabajar

**Opción A — Local**

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (en Mac/Linux: source .venv/bin/activate)
pip install -r requirements.txt
jupyter notebook
```

**Opción B — Google Colab:** sube la carpeta del repo a tu Drive (o clónalo) para que las
rutas relativas `../../data/...` de los notebooks funcionen.

En la **primera celda** de cada notebook reemplaza `cedula = ...` por tu número de
cédula completo antes de ejecutar: esa semilla personaliza tu muestra de datos y tus
resultados.

## Entrega de laboratorios

Lee `INSTRUCCIONES_ENTREGA.md`: copia la plantilla, renómbrala con el formato
indicado y súbela a la carpeta de Drive del curso.

## Referencia

*An Introduction to Statistical Learning* (James, Witten, Hastie, Tibshirani) — base
teórica del curso.
