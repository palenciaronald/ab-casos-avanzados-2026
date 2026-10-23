# Prompts por etapa

Cómo usarlos: abre la conversación **dentro de tu proyecto** (Claude lee `CLAUDE.md` y
`especificacion-proyecto.md`). Cambia lo que está entre `<...>`. Pide una cosa por vez y revisa el
resultado con `checklist-revision-ia.md` antes de continuar.

## Prompts para gastar poca cuota

- **Ancla el archivo:** "En `src/proyecto/data/cleaning.py`, convierte la columna `<col>` a número."
- **Una etapa, una conversación:** abre una conversación nueva al cambiar de etapa.
- **Pide el plan antes del código:** "Dime en 5 viñetas qué harías para `<tarea>`. No escribas código todavía."
- **Pide solo el cambio:** "Muéstrame solo la función que cambia, no el archivo completo."
- **Resumen para retomar:** "Resume en 10 líneas lo decidido hasta ahora para pegarlo en una conversación nueva."

---

## 1. Caso de negocio
**Prompt:** "Ayúdame a completar la sección 2 de `especificacion-proyecto.md` con mi caso: `<describe el problema>`. Hazme 5 preguntas sobre quién decide y qué cuesta equivocarse antes de escribir nada."
**Qué esperar:** preguntas concretas y una ficha redactada para no técnicos, con la decisión y los costos de error.
**Cómo revisarlo:** ¿se entiende sin saber ML? ¿dice qué error es peor? ¿la métrica elegida refleja ese costo?

## 2. EDA
**Prompt:** "Lee `data/raw/<archivo>.csv`. Hazme un EDA en `notebooks/02_eda.ipynb`: forma, tipos, nulos, duplicados, valores raros en columnas numéricas, distribución del objetivo y si una entidad se repite en varias filas. Escribe los hallazgos en `reports/01_eda.md`."
**Qué esperar:** tablas y gráficos, y una lista de problemas de datos con cifras.
**Cómo revisarlo:** ¿los porcentajes se pueden reproducir? ¿detectó entidades repetidas? ¿hay al menos 5 decisiones justificadas?

## 3. Preprocesamiento
**Prompt:** "Con los hallazgos de `reports/01_eda.md`, escribe en `src/proyecto/data/cleaning.py` una función de limpieza y en `src/proyecto/data/split.py` la partición por `<unidad>`. Elimina `<columnas personales>`. Añade pruebas en `tests/`."
**Qué esperar:** funciones pequeñas, pruebas que pasan y una verificación de que ninguna entidad cae en dos particiones.
**Cómo revisarlo:** `pytest` en verde; la prueba de partición falla si mezclas entidades; `data/raw/` no cambió.

## 4. Feature engineering
**Prompt:** "En `src/proyecto/features/`, crea las variables `<ideas>` y el `ColumnTransformer` dentro de un `Pipeline`. Solo variables que se conozcan al momento de predecir. Explica cada una en `notebooks/04_features.ipynb`."
**Qué esperar:** tabla de variables con justificación y un pipeline que ajusta solo con entrenamiento.
**Cómo revisarlo:** ¿alguna variable usa información del futuro o del objetivo? ¿se ajusta el escalado solo con entrenamiento?

## 5. Torneo de modelos
**Prompt:** "En `notebooks/05_torneo.ipynb`, compara regresión logística (o lineal), un bosque y un modelo de boosting con validación cruzada **por `<unidad>`** y la métrica `<métrica>`. Incluye una línea base trivial. Pon el código reutilizable en `src/proyecto/models/`."
**Qué esperar:** tabla comparativa con media y desviación entre folds, y una recomendación de 1–2 finalistas.
**Cómo revisarlo:** ¿la validación es por grupo? ¿los modelos se comparan con los mismos folds? ¿la diferencia supera la desviación?

## 6. Optimización con tracking
**Prompt:** "Con `src/proyecto/tracking/` conectado a Databricks por `.env`, optimiza el finalista con Optuna (máximo `<N>` pruebas) en `notebooks/06_optimizacion.ipynb`, registrando cada prueba como ejecución de MLflow con sus parámetros y métrica."
**Qué esperar:** un experimento en Databricks con una ejecución por prueba y la mejor combinación elegida.
**Cómo revisarlo:** abre el experimento en Databricks: ¿están todas las pruebas? ¿la mejora es real frente a la línea base o está dentro del ruido?

## 7. Validación e interpretación
**Prompt:** "En `notebooks/07_validacion_interpretacion.ipynb`, abre el conjunto de prueba **una sola vez** con el modelo optimizado. Muestra matriz de confusión con costos, umbral, calibración, importancia de variables (SHAP) y errores por segmento."
**Qué esperar:** métricas en prueba, gráficos y una lectura en lenguaje de negocio.
**Cómo revisarlo:** ¿se usó la prueba solo aquí? ¿el resultado cae cerca del de validación? ¿se discuten riesgos y límites?

## 8. Registro del modelo
**Prompt:** "En `notebooks/08_registro_modelo.ipynb`, registra el mejor modelo en Unity Catalog con firma y ejemplo de entrada, asigna versión y alias, y explica cómo recuperarlo."
**Qué esperar:** una versión del modelo en el registro de Databricks.
**Cómo revisarlo:** ¿aparece la versión en Databricks? ¿puedes cargarla y predecir con datos nuevos?

## 9. Módulos y pruebas
**Prompt:** "Mueve a `src/proyecto/` toda la lógica que siga en los notebooks, deja los notebooks solo como orquestadores y añade pruebas en `tests/`. No cambies los resultados."
**Qué esperar:** notebooks más cortos, `src/` completo, `pytest` en verde.
**Cómo revisarlo:** ejecuta todo desde cero; ¿dan las mismas métricas que antes?

## 10. Inferencia
**Prompt:** "En `src/proyecto/inference/predict.py`, crea `predict(df)` que reciba las columnas crudas y devuelva clase y probabilidades; falla con mensaje claro si faltan columnas. Exporta `models/model.joblib` y escribe `models/ficha_modelo.md`."
**Qué esperar:** una función probada, el archivo del modelo y la ficha con métricas y límites.
**Cómo revisarlo:** prueba con un caso conocido y con datos inválidos; ¿falla con claridad?

## 11. App
**Prompt:** "Crea `app/streamlit_app.py`: un formulario con las variables de entrada, validación, predicción y probabilidades, una explicación para no técnicos y un aviso de uso responsable. Debe cargar `models/model.joblib` del repositorio y no consultar Databricks."
**Qué esperar:** una app que arranca con `streamlit run app/streamlit_app.py`.
**Cómo revisarlo:** ¿acepta datos inválidos sin avisar? ¿la predicción coincide con la función `predict`? ¿funciona en un entorno limpio?

## 12. Informe técnico
**Prompt:** "Ensambla `reports/informe_tecnico.md` a partir de las secciones de `reports/`: caso, datos, preprocesamiento, features, torneo, optimización, validación, registro y despliegue. Escribe claro, sin inventar resultados que no estén en los archivos."
**Qué esperar:** un informe con todas las secciones y las cifras de los experimentos.
**Cómo revisarlo:** compara cada cifra con el experimento original; busca afirmaciones sin respaldo.

## 13. Presentación
**Prompt:** "En `presentacion/ejecutiva.md` (Marp), escribe **máximo 5 diapositivas**: problema, enfoque, resultado y costo de negocio, demo de la app, riesgos y siguientes pasos. Lenguaje sin jerga."
**Qué esperar:** cinco diapositivas claras, una idea por diapositiva.
**Cómo revisarlo:** ¿son 5 o menos? ¿un directivo entendería el resultado y el riesgo en 1 minuto?
