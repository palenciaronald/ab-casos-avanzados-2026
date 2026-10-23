# Contrato: estructura obligatoria del repositorio del grupo

La plantilla del kit (`kit-estudiante/plantilla-repo/`) y el repo del ejemplo cumplen este
contrato; la rúbrica lo verifica.

```text
<proyecto>/
├── README.md              # qué hace, cómo ejecutar, enlace a la app
├── CLAUDE.md              # instrucciones para Claude (viene del kit)
├── especificacion-proyecto.md
├── requirements.txt       # en la RAÍZ (requisito de Streamlit Community Cloud)
├── .env.example           # sin secretos; .env real está en .gitignore
├── .gitignore             # incluye .env, .venv/, datos con PII, __pycache__/
├── data/
│   ├── raw/               # intocable
│   └── processed/
├── notebooks/             # numerados por etapa; solo orquestan, no contienen lógica reusable
├── src/<paquete>/         # data/ features/ models/ tracking/ inference/
├── tests/                 # pytest
├── models/                # model.joblib + ficha_modelo.md
├── app/streamlit_app.py
├── reports/               # secciones por hito + informe_tecnico.md
└── presentacion/          # ejecutiva.md (≤ 5 diapositivas)
```

## Reglas

- No hay credenciales ni datos personales en el repo.
- `src/` no importa de `notebooks/`; los notebooks importan de `src/`.
- `requirements.txt` fija versiones y declara Python 3.12.
- El repo es público para poder desplegar en Streamlit Community Cloud.
