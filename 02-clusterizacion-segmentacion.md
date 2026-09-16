# Tema 1B: Clusterización — Segmentación de Clientes
## Fin de semana 1 (18–19 sep) — se dicta junto con Clasificación

## 1. Caso de negocio

Una empresa quiere entender los distintos perfiles de comportamiento de sus clientes para diseñar campañas de marketing y estrategias comerciales diferenciadas. El estudiante aplica clustering para identificar segmentos naturales en la base de clientes, sin usar una etiqueta objetivo (aprendizaje no supervisado).

## 2. Teoría a repasar (dentro del bloque de teoría del viernes, junto con clasificación)

- Diferencia entre aprendizaje supervisado y no supervisado
- K-Means: funcionamiento, método del codo (elbow method) y silhouette score para elegir K
- Importancia del escalado de variables antes de clusterizar (K-Means es sensible a la escala)
- Interpretación de clusters: perfilamiento (¿qué caracteriza a cada grupo?)
- Mención breve de alternativas (clustering jerárquico, DBSCAN) sin profundizar, dado el tiempo comprimido

## 3. Datasets

- **Viernes (demo del instructor):** [Mall Customer Segmentation](https://www.kaggle.com/datasets/vjchoudhary7/customer-segmentation-tutorial-in-python) — 200 filas, 5 columnas (género, edad, ingreso anual, spending score). Extremadamente simple, ideal para un caso corto y visual (se puede graficar en 2D).
- **Sábado (ejercicio del estudiante):** [Credit Card Dataset for Clustering](https://www.kaggle.com/datasets/arjunbhasin2013/ccdata) — ~8,950 filas, 18 variables de comportamiento financiero (balance, compras, cash advance, límite de crédito, frecuencia de pagos, etc.). Más rico, permite un perfilamiento de segmentos más interesante desde el negocio.

**Descarga:**
```bash
kaggle datasets download -d vjchoudhary7/customer-segmentation-tutorial-in-python -p ./data/02-clusterizacion --unzip
kaggle datasets download -d arjunbhasin2013/ccdata -p ./data/02-clusterizacion --unzip
```

## 4. Estructura del notebook demo (viernes) — versión corta, dado que comparte el día con clasificación

1. **Introducción** (Markdown) — planteamiento del caso
2. Carga y exploración rápida de datos
3. Selección de variables relevantes y escalado (`StandardScaler`)
4. Método del codo para elegir K
5. Entrenamiento de K-Means y asignación de clusters
6. Visualización de los clusters (scatter plot 2D con las variables más relevantes)
7. Perfilamiento: tabla resumen de medias por cluster + interpretación de negocio

## 5. Estructura de la plantilla (sábado)

Misma lógica de 7 secciones que el demo, pero:
- Sección 1 y 2 resueltas como ejemplo
- Celda de semilla personal (`np.random.seed(cedula)`), usada en el muestreo del dataset (`df.sample(frac=0.85, random_state=cedula)`) y en el `random_state` de `KMeans`
- Secciones 3 a 6: instrucción en Markdown + celda de código en blanco con comentario guía
- Sección 7 (perfilamiento): además de la tabla de medias, 2 preguntas abiertas en Markdown:
  - "Si tuvieras que nombrar cada cluster con una etiqueta de negocio (ej. 'clientes premium de bajo riesgo'), ¿cómo los llamarías y por qué?"
  - "¿Qué acción de negocio distinta recomendarías para cada segmento?"

**Nota de tiempo:** dado que este tema comparte sábado con clasificación, si el estudiante no alcanza a completar ambas plantillas, esta es la que puede quedar pendiente para entrega posterior, ya que su demo del viernes fue más corto.
