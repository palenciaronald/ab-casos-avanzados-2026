# Laboratorio de Casos Avanzados — Casos Prácticos
## Documento general del curso (para construcción con Kiro)

## 1. Contexto

Curso para la **Maestría en Ingeniería Analítica** de una universidad externa (coordina Leandro Ariza). La audiencia **no tiene formación previa en Inteligencia Artificial ni Machine Learning**, por lo que la teoría se dicta **desde cero**: primero la intuición (con analogías) y luego la formalización. El curso combina esos fundamentos con un enfoque 100% aplicado.

**Intensidad:** 24 horas totales, repartidas en 3 fines de semana (viernes + sábado cada uno).

**Fechas:**
| Fin de semana | Fechas | Tema(s) |
|---|---|---|
| 1 | 18–19 sep | Clasificación (Score de riesgo) + Clusterización (Segmentación de clientes) |
| 2 | 25–26 sep | Regresión (Modelo de liquidez) |
| 3 | 2–3 oct | NLP (Análisis de sentimientos) |

## 2. Dinámica de cada fin de semana

**Viernes — el instructor ejecuta:**
1. ~2 horas de teoría (PPT desde cero, para audiencia sin ML previo — intuición con analogías primero, luego la formalización; basada en *An Introduction to Statistical Learning*)
2. Resto de la sesión: práctica — el instructor desarrolla el caso de negocio completo en vivo, de principio a fin, en un notebook demo, explicando decisiones en cada paso

**Sábado — el estudiante ejecuta:**
1. 30–50 minutos: el instructor presenta el nuevo caso de negocio (variación del tema, mismo dominio pero distinto planteamiento/dataset)
2. Resto de la sesión: el estudiante trabaja solo sobre una plantilla de notebook, con el instructor presente resolviendo dudas
3. Idealmente el trabajo queda entregado el mismo sábado; si no alcanza, se puede entregar hasta el siguiente fin de semana

**Excepción — Fin de semana 1 (dos temas):** el viernes se explican y ejecutan ambos casos (clasificación y clusterización); el sábado, tras la explicación del nuevo caso, el estudiante intenta completar ambas plantillas si el tiempo alcanza.

## 3. Personalización con semilla (anti-copia, sin duplicar datasets)

En vez de tener un dataset distinto por estudiante, cada notebook (demo y plantilla) usa **una sola base de datos por rol** (una para el viernes, otra para el sábado), y la primera celda de código genera una semilla personal:

```python
cedula = 1020304050  # cada estudiante reemplaza por su número de cédula completo
np.random.seed(cedula)
```

Esa semilla se usa para:
- El `random_state` de cualquier train/test split
- Un muestreo (`.sample(frac=0.8, random_state=cedula)` o similar) que le da a cada estudiante un subconjunto ligeramente distinto de la base general

Esto asegura que los resultados numéricos (métricas, clusters, coeficientes) varíen entre estudiantes sin necesitar múltiples datasets.

## 4. Estructura y evaluación de las plantillas del sábado

- Las plantillas combinan **celdas Markdown con encabezados grandes y explicación del paso** (amigable, guiado) con **celdas de código en blanco con comentarios** indicando qué hacer (ej. `# Cargar el dataset y mostrar las primeras filas`, `# Entrenar un modelo de regresión logística con los datos de entrenamiento`).
- No hay rúbrica de puntaje separada: **el notebook mismo es el criterio de evaluación** — el estudiante completa el script paso a paso siguiendo las instrucciones en Markdown, y esa ejecución completa es la entrega.
- Cada plantilla termina con una sección de "Conclusiones" en Markdown donde el estudiante responde brevemente 2–3 preguntas de interpretación de negocio sobre sus resultados.

## 5. Datasets por tema (todos de Kaggle, 2 por tema: demo del viernes + ejercicio del sábado)

| Tema | Demo (viernes) | Ejercicio (sábado) |
|---|---|---|
| Clasificación | [German Credit Data (with Risk)](https://www.kaggle.com/datasets/kabure/german-credit-data-with-risk) | [Credit Score Classification Dataset](https://www.kaggle.com/datasets/parisrohan/credit-score-classification) |
| Clusterización | [Mall Customer Segmentation](https://www.kaggle.com/datasets/vjchoudhary7/customer-segmentation-tutorial-in-python) | [Credit Card Dataset for Clustering](https://www.kaggle.com/datasets/arjunbhasin2013/ccdata) |
| Regresión | [Financial Statements of Major Companies (2009-2023)](https://www.kaggle.com/datasets/rish59/financial-statements-of-major-companies2009-2023) | [Company Bankruptcy Prediction (Taiwan)](https://www.kaggle.com/datasets/fedesoriano/company-bankruptcy-prediction) |
| NLP | [Financial PhraseBank](https://www.kaggle.com/datasets/ankurzing/sentiment-analysis-for-financial-news) | [Financial Sentiment Analysis (FiQA + PhraseBank)](https://www.kaggle.com/datasets/sbhatti/financial-sentiment-analysis) |

Ver el `.md` de cada tema para el detalle del caso de negocio, la teoría a repasar, y la estructura exacta de cada notebook.

## 6. Descarga de los datasets

Todos los links de la tabla anterior apuntan a la **página de Kaggle** del dataset, no a un archivo descargable directo (Kaggle no lo permite sin pasar por su sistema de autenticación). Para obtener los CSV hay dos rutas:

**Opción A — Kiro descarga vía Kaggle API** (requiere que el entorno donde corre Kiro tenga configurado `kaggle.json` con las credenciales de la cuenta de Kaggle):

```bash
pip install kaggle
# colocar kaggle.json en ~/.kaggle/kaggle.json (o la ruta que use el entorno)

kaggle datasets download -d kabure/german-credit-data-with-risk -p ./data/01-clasificacion --unzip
kaggle datasets download -d parisrohan/credit-score-classification -p ./data/01-clasificacion --unzip

kaggle datasets download -d vjchoudhary7/customer-segmentation-tutorial-in-python -p ./data/02-clusterizacion --unzip
kaggle datasets download -d arjunbhasin2013/ccdata -p ./data/02-clusterizacion --unzip

kaggle datasets download -d rish59/financial-statements-of-major-companies2009-2023 -p ./data/03-regresion --unzip
kaggle datasets download -d fedesoriano/company-bankruptcy-prediction -p ./data/03-regresion --unzip

kaggle datasets download -d ankurzing/sentiment-analysis-for-financial-news -p ./data/04-nlp --unzip
kaggle datasets download -d sbhatti/financial-sentiment-analysis -p ./data/04-nlp --unzip
```

**Opción B — Descarga manual:** entrar a cada uno de los 8 links de la tabla (logueado en Kaggle), darle "Download", y ubicar los CSV en la misma estructura de carpetas (`data/01-clasificacion/`, `data/02-clusterizacion/`, `data/03-regresion/`, `data/04-nlp/`) para que las rutas relativas de los notebooks coincidan.

Cualquiera de las dos rutas deja los archivos en la estructura que los notebooks van a esperar: dentro de `data/<carpeta-del-tema>/`, un CSV para el viernes y otro para el sábado.

## 7. Stack técnico esperado

- Python 3.x, Jupyter Notebook
- Librerías estándar: `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`
- NLP: `nltk` o `spaCy` para preprocesamiento; `scikit-learn` (TF-IDF + clasificador clásico) como enfoque base — ver detalle en el .md de NLP
- Sin dependencias de infraestructura pesada (todo debe correr en Google Colab o Jupyter local sin GPU)

## 8. Archivos de este set

1. `00-curso-general.md` (este documento)
2. `01-clasificacion-score-riesgo.md`
3. `02-clusterizacion-segmentacion.md`
4. `03-regresion-liquidez.md`
5. `04-nlp-sentimientos.md`
