# Instrucciones permanentes para Claude (proyecto del curso)

Este archivo lo lees al inicio de cada conversación. Sigue estas reglas siempre.

## Quién soy y qué hacemos

- Soy estudiante de la Maestría en Ingeniería Analítica. **Soy analista, no desarrollador.**
  Explica lo que haces, con palabras simples, antes y después de cambiar código.
- Trabajo en un grupo. Estamos construyendo un proyecto de machine learning de principio a fin,
  como si fuera una startup: caso de negocio, EDA, preprocesamiento, features, torneo de modelos,
  optimización, validación, tracking en Databricks, app en Streamlit, reporte y presentación.
- El caso, el dataset, la métrica y el tipo de problema están en `especificacion-proyecto.md`.
  **Léelo antes de generar código** y avísame si algo del pedido lo contradice.

## Estructura obligatoria del repositorio

```text
README.md  CLAUDE.md  especificacion-proyecto.md  requirements.txt  .env.example  .gitignore
data/raw/        # datos originales: NUNCA se modifican
data/processed/
notebooks/       # numerados por etapa; solo orquestan, sin lógica reutilizable
src/proyecto/    # data/ features/ models/ tracking/ inference/
tests/           # pytest
models/          # model.joblib + ficha_modelo.md
app/streamlit_app.py
reports/         # una sección por hito + informe_tecnico.md
presentacion/    # ejecutiva.md (máximo 5 diapositivas)
scripts/
```

- La lógica reutilizable va en `src/`; los notebooks importan de `src/`, nunca al revés.
- `requirements.txt` está en la raíz, con versiones fijadas y Python 3.12.

## Estilo

- **Textos, comentarios y documentación en español. Nombres de variables, funciones y archivos de
  código en inglés** (`clean_income`, no `limpiar_ingreso`).
- Cambios pequeños: una cosa por vez, en el archivo que te indico. No reescribas el proyecto entero.
- Si no estás seguro, pregunta antes de inventar.

## Reglas que no se negocian

1. **No inventes datos.** Si una columna, un valor o un resultado no existe, dilo. Nunca
   fabriques métricas ni resultados.
2. **No subas secretos ni datos personales.** `.env` está en `.gitignore`; no imprimas ni
   escribas tokens. Elimina o anonimiza nombres, documentos de identidad y similares.
3. **Parte los datos por la unidad correcta.** Si un mismo cliente, paciente o empresa aparece en
   varias filas, la partición entrenamiento/validación/prueba y la validación cruzada se hacen
   **por grupo** (`GroupKFold`, `StratifiedGroupKFold`, `GroupShuffleSplit`), no por fila.
4. **No uses el conjunto de prueba para decidir nada.** Se abre una sola vez, al final, en la
   etapa de validación. Elegir modelo, umbral o hiperparámetros se hace con validación.
5. **Todo preprocesamiento va dentro de un `Pipeline`** ajustado solo con entrenamiento, para
   evitar fuga de información.
6. **Cada decisión de datos se escribe con su motivo** en `reports/`, no solo en el código.
7. **El seguimiento de experimentos usa MLflow en Databricks.** Lee la conexión desde `.env`
   (`PROFILE` o `DATABRICKS_HOST` y `DATABRICKS_TOKEN`). Define `PYTHONUTF8=1` en Windows.
8. **La app NO consulta Databricks.** Carga `models/model.joblib` desde el repositorio. Valida
   las entradas del formulario y muestra un aviso de uso responsable.
9. **Pruebas.** Cada función de `src/` que limpia datos o transforma variables debe tener una
   prueba en `tests/`. Ejecútalas con `pytest` antes de darme el cambio por terminado.

## Cómo quiero que respondas

1. Resume en 2–3 frases qué vas a hacer y por qué.
2. Haz el cambio.
3. Dime cómo comprobar que funciona (el comando exacto) y qué resultado debería ver.
4. Si hay un riesgo (fuga de información, datos personales, métrica engañosa), avísame.
