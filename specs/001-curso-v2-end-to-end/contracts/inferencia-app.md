# Contrato: inferencia y app

## Función de inferencia (`src/<paquete>/inference`)

- `predict(df: DataFrame) -> DataFrame`: recibe las columnas **crudas** que el usuario conoce al
  decidir (las que el modelo puede conocer al momento de predecir; nunca columnas posteriores).
- Salida mínima: clase predicha, probabilidad por clase (calibrada si la etapa 7 la calibró) y un
  indicador de confianza o de datos fuera de rango.
- Debe fallar con un mensaje claro ante columnas faltantes o valores inválidos; nunca devolver una
  predicción silenciosa con datos corruptos.

## Archivo del modelo

- `models/model.joblib`: pipeline completo (preprocesamiento + modelo) exportado desde la versión
  registrada en Databricks.
- `models/ficha_modelo.md`: datos de entrenamiento, métricas en prueba, límites y usos
  no recomendados, versión del registro y versión de las librerías.

## App (`app/streamlit_app.py`)

- Carga `models/model.joblib` desde el repo (no consulta Databricks).
- Formulario con los campos de entrada del contrato anterior, validados.
- Muestra predicción, probabilidades y una explicación comprensible para un no técnico.
- Incluye un aviso de uso responsable (qué decisión apoya y cuál no).
- Arranca con `streamlit run app/streamlit_app.py` en un entorno limpio con solo
  `requirements.txt`.
