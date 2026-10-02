# Tema 2: Clusterización — Segmentación de Clientes
## Fin de semana 2 (25–26 sep)

## 1. Caso de negocio

Una empresa quiere entender los distintos perfiles de comportamiento de sus clientes para diseñar campañas de marketing y estrategias comerciales diferenciadas. El estudiante aplica clustering para identificar segmentos naturales en la base de clientes, sin usar una etiqueta objetivo (aprendizaje no supervisado).

## 2. Teoría (viernes, ~2 h dedicadas)

- Diferencia entre aprendizaje supervisado y no supervisado; el reto de no tener una etiqueta contra la cual validar.
- **K-Means**: funcionamiento, naturaleza iterativa y de óptimo local (`n_init`), sensibilidad a la escala.
- **Clustering jerárquico (aglomerativo)**: dendrograma, criterios de enlace (`linkage`: ward, complete, average), cómo "cortar" el árbol para obtener K grupos, ventajas frente a K-Means (no exige fijar K de antemano, es determinista).
- **DBSCAN**: clustering basado en densidad, parámetros `eps` y `min_samples`, capacidad de detectar outliers como "ruido" y de encontrar formas no convexas — el contraste más claro frente a K-Means/jerárquico.
- **Evaluación de calidad sin etiqueta** — métricas internas:
  - Método del **codo** (inercia) — específico de K-Means.
  - **Silhouette score** — aplica a cualquier algoritmo.
  - **Davies-Bouldin index** — más bajo es mejor (separación vs. compacidad).
  - **Calinski-Harabasz index** — más alto es mejor (dispersión entre/dentro de clusters).
  - Cuándo confiar en cada una y por qué ninguna sustituye la interpretación de negocio.
- Importancia del escalado de variables antes de clusterizar (los tres algoritmos usan distancias).
- Interpretación de clusters: perfilamiento (¿qué caracteriza a cada grupo?) y cómo comparar los resultados de los 3 algoritmos sobre el mismo problema.

## 3. Datasets

- **Viernes (demo del instructor):** [Mall Customer Segmentation](https://www.kaggle.com/datasets/vjchoudhary7/customer-segmentation-tutorial-in-python) — 200 filas, 5 columnas (género, edad, ingreso anual, spending score). Extremadamente simple, ideal para un caso corto y visual (se puede graficar en 2D) donde comparar los 3 algoritmos lado a lado.
- **Sábado (ejercicio del estudiante):** [Credit Card Dataset for Clustering](https://www.kaggle.com/datasets/arjunbhasin2013/ccdata) — ~8,950 filas, 18 variables de comportamiento financiero (balance, compras, cash advance, límite de crédito, frecuencia de pagos, etc.). Más rico, permite un perfilamiento de segmentos más interesante desde el negocio.

**Descarga:**
```bash
kaggle datasets download -d vjchoudhary7/customer-segmentation-tutorial-in-python -p ./data/02-clusterizacion --unzip
kaggle datasets download -d arjunbhasin2013/ccdata -p ./data/02-clusterizacion --unzip
```

## 4. Estructura del notebook demo (viernes)

1. **Introducción** (Markdown) — planteamiento del caso
2. Carga y exploración rápida de datos
3. Selección de variables relevantes y escalado (`StandardScaler`)
4. Elección de K para K-Means: método del codo + silhouette
5. Entrenamiento y comparación de los **3 algoritmos** (K-Means, jerárquico/Agglomerative, DBSCAN) sobre las mismas variables
6. Evaluación de calidad de cada algoritmo con las 4 métricas (silhouette, Davies-Bouldin, Calinski-Harabasz, + inercia donde aplique) en una tabla comparativa
7. Visualización de los clusters de cada algoritmo (scatter plot 2D)
8. Perfilamiento del algoritmo ganador: tabla resumen de medias por cluster + interpretación de negocio

## 5. Estructura de la plantilla (sábado)

Misma lógica que el demo, pero:
- Sección 1 y 2 resueltas como ejemplo
- Celda de semilla personal (`np.random.seed(cedula)`), usada en el muestreo del dataset (`df.sample(frac=0.85, random_state=cedula)`) y en el `random_state` de los algoritmos
- Secciones 3 en adelante: instrucción en Markdown + celda de código en blanco con comentario guía
- El estudiante entrena y compara **los 3 algoritmos** vistos en la demo (K-Means, jerárquico y DBSCAN), con las métricas de calidad, y elige uno para el perfilamiento — justificando la elección, no solo reportando el número
- **La descriptiva de los grupos (perfilamiento) es obligatoria** sin importar el algoritmo elegido: es el paso que le da sentido de negocio a todo el análisis
- **Los atípicos son obligatorios de inspeccionar, no solo de mencionar**: el estudiante debe sacar de la base las filas atípicas (ruido de DBSCAN, o el cluster más pequeño/extremo si usó K-Means/jerárquico), mirarlas con todas sus columnas, y para cada patrón decidir si parece un cliente real e inusual o un error de datos — con evidencia concreta, no una respuesta genérica
- Sección final de conclusión: mayoría de preguntas **de negocio** (imaginando que se las responde al área comercial, no a un técnico), con solo 2 preguntas técnicas breves al final. Preguntas de negocio, entre ellas:
  - "Bautiza cada cluster con un nombre de negocio" (pregunta central: si alguien del área comercial solo lee esta respuesta, debe entender quiénes son los segmentos)
  - "¿Cuál segmento es más valioso para el negocio y cuál representa mayor riesgo/costo?"
  - "¿Qué acción comercial distinta recomendarías para cada segmento?"
  - "Si solo hubiera presupuesto para una campaña este trimestre, ¿en qué segmento la invertirías primero?"
  - "¿Qué harías con los clientes marcados como ruido/atípicos desde el negocio?"
  - (técnicas, breves) "¿Con cuál algoritmo te quedaste y por qué?" y "¿Por qué fue imprescindible escalar?"
