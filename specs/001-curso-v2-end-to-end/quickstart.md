# Quickstart — validar el entorno y el camino end-to-end

Guía de validación; no contiene la implementación.

## 1. Entorno (instructor)

```powershell
uv venv --python 3.12 .venv
uv pip install --python .venv\Scripts\python.exe -r requirements.txt   # el del curso v2 (por crear)
$env:PYTHONUTF8 = "1"
```
Esperado: `python -c "import mlflow, streamlit, sklearn"` sin errores con Python 3.12.

## 2. Tracking y registro (Databricks)

1. Copiar `.env.example` a `.env` y completar `DATABRICKS_HOST` y `DATABRICKS_TOKEN`
   (o usar el perfil OAuth del CLI en la máquina del instructor).
2. Ejecutar el script de comprobación del kit: crea un experimento, registra un run y registra un
   modelo de juguete en `workspace.default.<nombre>`.
3. Esperado: el run aparece en la interfaz de experimentos y el modelo tiene la versión 1.
   Ya verificado desde el equipo del instructor (ver research D3); **pendiente** repetirlo con una
   cuenta de estudiante de Free Edition (R1).

## 3. Una etapa del ejemplo

```powershell
scripts\verify_stage 02_eda     # entorno limpio + nbconvert --execute
```
Esperado: termina con código 0 y deja `reports/01_eda.md`.

## 4. App

```powershell
streamlit run app\streamlit_app.py
```
Esperado: formulario visible, predicción coherente para un caso de prueba conocido, error claro
con datos inválidos. Despliegue: conectar el repo público en Streamlit Community Cloud con
Python 3.12 y `requirements.txt` en la raíz; esperado: enlace público funcional.

## 5. Reproducción por una persona ajena (SC-001)

Alguien que no escribió el ejemplo clona el repo, sigue el README y llega a la app funcionando sin
ayuda. Cronometrar y anotar cada punto donde se atasca.
