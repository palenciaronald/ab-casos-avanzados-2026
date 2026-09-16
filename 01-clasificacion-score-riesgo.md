# Tema 1A: Clasificación — Score de Riesgo
## Fin de semana 1 (18–19 sep) — se dicta junto con Clusterización

## 1. Caso de negocio

Una entidad financiera necesita clasificar a sus solicitantes de crédito según su nivel de riesgo (bueno/malo pagador, o categorías de score) para apoyar la decisión de otorgamiento de crédito. El estudiante construye un modelo de clasificación que, a partir de información financiera y demográfica del solicitante, predice su categoría de riesgo.

## 2. Teoría a repasar el viernes (~1 hora, nivel refresco)

- Formulación del problema de clasificación binaria/multiclase
- Métricas: accuracy, precision, recall, F1, matriz de confusión, ROC-AUC — y por qué el accuracy solo, no basta en datasets desbalanceados
- Modelos a repasar: regresión logística, árboles de decisión, random forest (al menos uno de ensamble)
- Manejo de desbalance de clases (undersampling/oversampling, class_weight)
- Importancia de variables / interpretabilidad (coeficientes, feature importance)

## 3. Datasets

- **Viernes (demo del instructor):** [German Credit Data (with Risk)](https://www.kaggle.com/datasets/kabure/german-credit-data-with-risk) — 1,000 registros, 10 variables (edad, sexo, trabajo, vivienda, cuentas de ahorro/corriente, monto y duración del crédito, propósito) más la columna target **`Risk`** (good/bad). Ojo: la versión `uciml/german-credit` de Kaggle NO trae la columna target — hay que usar específicamente esta versión de `kabure`, que sí la incluye. Dataset pequeño y limpio, ideal para explicar el pipeline completo sin fricción de limpieza de datos (aunque tiene algunos NA en "Saving accounts" y "Checking account" que vale la pena mostrar cómo tratar).
- **Sábado (ejercicio del estudiante):** [Credit Score Classification Dataset](https://www.kaggle.com/datasets/parisrohan/credit-score-classification) — ~100,000 filas, 28 variables, target multiclase (Poor/Standard/Good). Más grande y con más limpieza necesaria (valores atípicos, columnas mixtas texto/número), lo que exige más trabajo de preprocesamiento por parte del estudiante.

**Descarga:**
```bash
kaggle datasets download -d kabure/german-credit-data-with-risk -p ./data/01-clasificacion --unzip
kaggle datasets download -d parisrohan/credit-score-classification -p ./data/01-clasificacion --unzip
```

## 4. Estructura del notebook demo (viernes)

1. **Introducción** (Markdown) — planteamiento del caso de negocio
2. Carga de datos y exploración inicial (`.head()`, `.info()`, `.describe()`)
3. Análisis exploratorio (EDA): distribución del target, correlaciones, variables categóricas vs. target
4. Preprocesamiento: encoding de categóricas, escalado si aplica, train/test split
5. Entrenamiento de al menos 2 modelos (ej. regresión logística como baseline, random forest como modelo principal)
6. Evaluación: matriz de confusión, reporte de clasificación, curva ROC
7. Interpretación: importancia de variables, ¿qué features pesan más en el riesgo?
8. Conclusión de negocio: ¿qué recomendaría el modelo al área de crédito?

## 5. Estructura de la plantilla (sábado)

Misma estructura de 8 secciones que el demo, pero:
- Secciones 1 y 2 (introducción y carga de datos) ya resueltas como ejemplo de formato
- Celda de semilla personal al inicio (`cedula = ...`, `np.random.seed(cedula)`), usada en el `train_test_split` y en un muestreo del dataset completo (ej. `df.sample(frac=0.85, random_state=cedula)`)
- Secciones 3 a 7: celdas Markdown con la pregunta/instrucción de qué hacer, y celda de código en blanco con comentario guía (ej. `# TODO: entrena un RandomForestClassifier con los datos de entrenamiento`)
- Sección 8 (conclusión de negocio): 2–3 preguntas abiertas en Markdown para que el estudiante responda en texto, ej.:
  - "¿Qué variables tienen mayor peso en la predicción del riesgo, y tiene sentido desde el negocio?"
  - "Si el banco quisiera reducir falsos negativos (aprobar a alguien que no paga), ¿qué ajustarías del modelo?"
