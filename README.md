# Nombre del proyecto

> Una frase: qué problema de negocio resuelve este proyecto y para quién.

**App desplegada:** _enlace público de Streamlit (se completa en el tercer fin de semana)_

## Qué contiene
Estructura obligatoria del curso. Cada carpeta tiene un propósito:

| Carpeta | Contenido |
|---|---|
| `data/raw/` | Datos originales, intocables |
| `data/processed/` | Datos limpios generados por el código |
| `notebooks/` | Un notebook por etapa; solo orquestan |
| `src/proyecto/` | Código reutilizable (data, features, models, tracking, inference) |
| `tests/` | Pruebas con `pytest` |
| `models/` | `model.joblib` y `ficha_modelo.md` |
| `app/` | `streamlit_app.py` |
| `reports/` | Una sección por hito e `informe_tecnico.md` |
| `presentacion/` | `ejecutiva.md` (máximo 5 diapositivas) |

## Cómo ejecutarlo
```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/Scripts/python.exe -r requirements.txt   # en Mac/Linux: .venv/bin/python
cp .env.example .env     # completa PROFILE o DATABRICKS_HOST y DATABRICKS_TOKEN
python scripts/check_databricks.py
pytest
streamlit run app/streamlit_app.py
```

## De dónde viene este repositorio
Nació de la rama `base` del repositorio del curso (ver `LEEME-PRIMERO.md`): una persona del grupo la clonó con
`git clone --branch base --single-branch …`, la apuntó a este repo con `git remote set-url origin …` y hizo `push`. Los demás integrantes
clonan **este** repositorio. Para arrancar, sigue `material-del-curso/guias/montaje-proyecto.md`.

## Equipo
| Integrante | Rol |
|---|---|
| | |

Especificación del proyecto: [`especificacion-proyecto.md`](especificacion-proyecto.md)
