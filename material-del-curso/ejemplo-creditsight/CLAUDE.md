# Instrucciones permanentes para Claude (ejemplo de referencia: CreditSight)

Este archivo lo lees al inicio de cada conversación. Sigue estas reglas siempre.

> **Este es el `CLAUDE.md` del kit, adaptado al ejemplo del instructor.** El código de `material-del-curso/ejemplo-creditsight/src/`
> (paquete `creditsight`) es **el modelo a imitar** por los grupos: úsalo como referencia de
> estructura, estilo y nivel de detalle, no como algo que haya que copiar sin entender.

## Quién soy y qué hacemos

- Soy el instructor del curso de Maestría en Ingeniería Analítica. Construimos **CreditSight**, un
  proyecto de machine learning de principio a fin, como si fuera una startup: caso de negocio, EDA,
  preprocesamiento, features, torneo de modelos, optimización, validación, tracking en Databricks, app
  en Streamlit, reporte y presentación.
- Explica lo que haces, con palabras simples, antes y después de cambiar código: el material se usa
  para enseñar a personas que **son analistas, no desarrolladores**.
- El caso, el dataset, la métrica y el tipo de problema están en `material-del-curso/ejemplo-creditsight/especificacion-proyecto.md`.
  **Léelo antes de generar código** y avísame si algo del pedido lo contradice.

## Estructura del repositorio

El ejemplo vive dentro del repositorio del curso. La raíz del repositorio aporta `requirements.txt`,
`.env.example` y los datos en `data/`; el proyecto está en `material-del-curso/ejemplo-creditsight/`:

```text
requirements.txt  .env  .env.example  data/01-clasificacion/      # en la raíz del repo del curso
material-del-curso/ejemplo-creditsight/
├── README.md  CLAUDE.md  especificacion-proyecto.md
├── notebooks/       # 01_caso_negocio ... 09_inferencia; solo orquestan, sin lógica reutilizable
├── src/creditsight/ # data/ features/ models/ tracking/ inference/ config.py
├── tests/           # pytest
├── data_processed/  # train/test generados por el notebook 03 (no se versionan)
├── models/          # model.joblib, input_schema.json, ficha_modelo.md
├── app/streamlit_app.py
├── reports/         # una sección por etapa + informe_tecnico.md
├── presentacion/    # ejecutiva.md (máximo 5 diapositivas)
└── scripts/         # check_databricks.py, verify_stage.*
```

- La lógica reutilizable va en `material-del-curso/ejemplo-creditsight/src/creditsight/`; los notebooks importan de ahí, nunca al revés.
- Los datos originales (`data/01-clasificacion/`) **nunca se modifican**.
- En los repos de los grupos la estructura es la de `` (con
  `src/<paquete>/` en la raíz); aquí está anidada en `material-del-curso/ejemplo-creditsight/` por ser parte del repositorio del curso.

## Estilo

- **Textos, comentarios y documentación en español. Nombres de variables, funciones y archivos de
  código en inglés** (`clean_income`, no `limpiar_ingreso`).
- Cambios pequeños: una cosa por vez, en el archivo que te indico. No reescribas el proyecto entero.
- Si no estás seguro, pregunta antes de inventar.

## Reglas que no se negocian

1. **No inventes datos.** Si una columna, un valor o un resultado no existe, dilo. Nunca
   fabriques métricas ni resultados: toda cifra del ejemplo sale de un notebook ejecutado.
2. **No subas secretos ni datos personales.** `.env` está en `.gitignore`; no imprimas ni
   escribas tokens. `Name`, `SSN` e `ID` se eliminan al cargar los datos (`load_raw`).
3. **Parte los datos por la unidad correcta.** En CreditSight un mismo cliente aparece en 8 filas
   (cliente-mes): la partición entrenamiento/validación/prueba y la validación cruzada se hacen
   **por `Customer_ID`** (`GroupShuffleSplit`, `StratifiedGroupKFold`), no por fila.
4. **No uses el conjunto de prueba para decidir nada.** Se abre una sola vez, al final, en la
   etapa de validación (notebook 07). Elegir modelo, umbral o hiperparámetros se hace con validación.
5. **Todo preprocesamiento va dentro de un `Pipeline`** ajustado solo con entrenamiento, para
   evitar fuga de información.
6. **Cada decisión de datos se escribe con su motivo** en `material-del-curso/ejemplo-creditsight/reports/`, no solo en el código.
7. **El seguimiento de experimentos usa MLflow en Databricks.** Lee la conexión desde `.env`
   (`PROFILE` o `DATABRICKS_HOST` y `DATABRICKS_TOKEN`, y `EXPERIMENT_DIR` para la carpeta). Si no hay
   conexión, `material-del-curso/ejemplo-creditsight/src/creditsight/tracking/mlflow_utils.py` cae a MLflow local. Define
   `PYTHONUTF8=1` en Windows.
8. **La app NO consulta Databricks.** Carga `material-del-curso/ejemplo-creditsight/models/model.joblib` desde el repositorio. Valida
   las entradas del formulario y muestra un aviso de uso responsable.
9. **Pruebas.** Cada función de `material-del-curso/ejemplo-creditsight/src/` que limpia datos o transforma variables debe tener una
   prueba en `material-del-curso/ejemplo-creditsight/tests/`. Ejecútalas con `pytest material-del-curso/ejemplo-creditsight/tests` antes de dar el cambio por terminado.

## Cómo quiero que respondas

1. Resume en 2–3 frases qué vas a hacer y por qué.
2. Haz el cambio.
3. Dime cómo comprobar que funciona (el comando exacto) y qué resultado debería ver.
4. Si hay un riesgo (fuga de información, datos personales, métrica engañosa), avísame.
