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
**Antes de pedir nada:** abre `guia-eda-y-preprocesamiento.md` y define tu **ID_COL** (la columna que identifica a la entidad) y tu **TARGET**.

**Prompt 1 (plan, sin código):** "Lee `especificacion-proyecto.md` y mira `data/raw/<archivo>.csv` sin imprimir columnas con datos personales. Dime en 5 viñetas qué revisarías en el EDA siguiendo las 5 preguntas de `kit-estudiante/guia-eda-y-preprocesamiento.md` (unidad de análisis, objetivo, suciedad, variables que deberían ser estables, sospecha de fuga). No escribas código todavía."

**Prompt 2 (una pregunta por vez):** "En `notebooks/02_eda.ipynb`, sección `<1, 2, 3, 4 o 5>`, completa la celda de código para mi dataset (ID_COL=`<columna>`, TARGET=`<columna>`). Usa pandas, muestra cifras y no cambies otras secciones. Dime cómo reproducir cada porcentaje."

**Prompt 3 (calidad de datos):** "Revisa mi dataset con los chequeos de la sección 3 de la guía: números guardados como texto, valores centinela, valores imposibles mirando los percentiles (p90, p95, p97, p99, máximo), vacíos y qué podrían significar, duplicados y categorías raras. Dame una tabla con la cifra de cada problema. No corrijas nada todavía."

**Prompt 4 (decisiones):** "Con estos hallazgos `<pega la tabla>`, ayúdame a redactar en `reports/01_eda.md` la tabla hallazgo → decisión → motivo. Cada fila debe tener una cifra. Dime si alguna decisión es vaga o no tiene motivo."

**Qué esperar:** tablas y gráficos con cifras, una lista de problemas de datos reproducible y **al menos 5 decisiones** escritas con su motivo.

**Cómo revisarlo (con la guía):**
- ¿Pude **reproducir** los porcentajes ejecutando la celda yo mismo?
- ¿Respondí la **pregunta 1** (unidad de análisis) por escrito y dije si una entidad se repite?
- ¿Cada decisión tiene **cifra, acción y motivo**? (una decisión sin motivo no cuenta)
- ¿Revisé **valores imposibles con percentiles** y no solo con `describe()`?
- ¿Claude **inventó** alguna columna o cifra? Si dudas, ejecuta `df.columns` y compara.
- ¿Imprimió **datos personales**? Si pasó, elimínalos de la salida del notebook antes de guardarlo.

## 3. Preprocesamiento
**Antes de pedir nada:** tu tabla de decisiones del EDA (`reports/01_eda.md`) es la entrada. Una decisión = una función = una prueba.

**Prompt 1 (una decisión):** "Del `reports/01_eda.md`, decisión número `<n>`: `<pega la decisión>`. Escribe en `src/proyecto/data/cleaning.py` una función pequeña que la implemente, con docstring en español. Añade una prueba en `tests/test_cleaning.py` con un ejemplo mínimo hecho a mano (el caso normal y el caso sucio). No toques otras funciones."

**Prompt 2 (la función que une todo):** "En `src/proyecto/data/cleaning.py`, crea `clean(df)` que aplique en orden las funciones ya escritas y devuelva un `DataFrame` con el **mismo número de filas** que la entrada. Elimina las columnas personales `<lista>` al cargar los datos. No modifiques nada de `data/raw/`."

**Prompt 3 (partición por la unidad de análisis):** "En `src/proyecto/data/split.py`, escribe `split_by_group(df, group_col, test_size, seed)` con `GroupShuffleSplit`, partiendo por `<unidad>`. Añade en `tests/test_split.py` una prueba con `assert` de que **ninguna entidad aparece en entrenamiento y prueba a la vez**. Después demuéstrame que esa prueba **falla** si se parte por fila con `train_test_split`."

**Prompt 4 (orquestar):** "En `notebooks/03_preprocesamiento.ipynb`, deja que el notebook solo **llame** a `clean` y `split_by_group`, muestre las comprobaciones y guarde `data/processed/train.joblib` y `test.joblib`. Sin lógica reutilizable dentro del notebook."

**Qué esperar:** funciones pequeñas con docstring, pruebas que pasan, la limpieza corriendo de principio a fin y una verificación de que ninguna entidad cae en dos particiones.

**Cómo revisarlo (con la guía y `checklist-revision-ia.md`):**
- `pytest -q` en **verde**.
- La prueba de partición **falla** si parto por fila (compruébalo: una prueba que no puede fallar no protege nada).
- `data/raw/` **no cambió** (`git status` no lo muestra modificado).
- ¿Hay alguna estadística de **todo el dataset** (media, mediana, categorías) calculada antes de partir? Eso va dentro del pipeline, no en la limpieza.
- ¿Puedo explicar **cada línea** de las funciones? Si no, pídele que la explique antes de aceptarla.
- ¿Los datos personales quedaron **fuera** del `DataFrame` limpio?

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
