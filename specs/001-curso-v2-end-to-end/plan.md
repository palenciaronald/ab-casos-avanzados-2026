# Implementation Plan: Curso v2 — Laboratorios de Casos Avanzados (proyecto end-to-end tipo startup)

**Branch**: `v2` (rama de trabajo; el directorio de spec es `001-curso-v2-end-to-end`) | **Date**: 2026-10-18 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/001-curso-v2-end-to-end/spec.md`

## Summary

Producir el material completo de un curso de tres fines de semana en el que cada grupo construye
un proyecto de ML end-to-end tratado como startup. El instructor construye primero un **ejemplo
de referencia de nivel senior** (CreditSight, sobre `credit_score_classification.csv`) en una
carpeta `ejemplo/` de este mismo repositorio público; de ese ejemplo se derivan las demos, la plantilla de repo y los
criterios de la rúbrica. Este repositorio del curso contiene las diapositivas, planes de sesión,
guías, el **kit del estudiante** (instrucciones para Claude, plantilla de especificación,
plantilla de repo, prompts y checklist de revisión) y la evaluación. Tracking y registro en
Databricks Free Edition con MLflow; app en Streamlit Community Cloud; Claude (VS Code + extensión)
como asistente obligatorio.

## Technical Context

**Language/Version**: Python 3.12 (entorno `.venv` creado con `uv`); Markdown para el material.

**Primary Dependencies**: pandas, scikit-learn, xgboost, lightgbm, optuna, shap, mlflow,
databricks-sdk, python-dotenv, streamlit, joblib, pytest, nbconvert/nbformat. Diapositivas:
Marp (fuente `.md`, salida HTML/PPTX bajo demanda), como en la v1.

**Storage**: archivos (CSV en `data/`, modelo `.joblib`, informes `.md`). Tracking y registro en
Databricks (experimentos y Unity Catalog); la app **no** consulta Databricks (ver research D6).

**Testing**: `pytest` sobre `src/` del ejemplo; ejecución de notebooks con `nbconvert` desde un
entorno limpio (`uv venv` + `requirements.txt`) como prueba de reproducibilidad por etapa.

**Target Platform**: Windows/macOS de estudiantes (VS Code); Streamlit Community Cloud para la app;
Databricks Free Edition para tracking.

**Project Type**: producto educativo (material de curso) + repositorio de ejemplo de ciencia de
datos con app web, en un solo repositorio. Cada grupo crea su propio repo.

**Performance Goals**: el ejemplo completo corre en un portátil sin GPU en menos de 30 min de
cómputo total; cada notebook de demo corre en menos de 5 min.

**Constraints**: Free Edition (solo serverless, cuota diaria, sin uso comercial); plan básico de
Claude (límites de uso por ventana); estudiantes no desarrolladores; consola Windows requiere
`PYTHONUTF8=1`; material en español, identificadores en inglés.

**Scale/Scope**: 3 fines de semana × 8 h; ≈ 12 demos cortas; 1 ejemplo completo; 5 guías; 1 kit;
1 rúbrica. Número de grupos desconocido (no condiciona el diseño).

## Constitution Check

*GATE: pasa antes de Phase 0; se re-evalúa tras Phase 1.*

| Principio | Estado | Nota |
|---|---|---|
| I. Proyecto end-to-end por grupo, tipo startup | PASS | Hitos por fin de semana; ficha de caso aprobada el 1.º sábado |
| II. No repetir lo visto | PASS | Única excepción: nivelación del 1.er viernes (permitida); el resto exige pipelines sin plantilla |
| III. Tres fines de semana con hitos | PASS | Ver `contracts/etapas.md` y plan de sesión |
| IV. Entregables verificables | PASS | Rúbrica + criterios de aceptación por hito + pregunta oral sobre código de IA |
| V. Exposición acotada | PASS | 10 min + preguntas; viernes final = app y presentación |
| VI. Material de estudiantes versionable; del instructor no | PASS con acción | El ejemplo vive en este repo público (`ejemplo/`); es un modelo, no una "solución de laboratorio". `curso_Leo_IA/`, `.env`, `.venv/`, `.specify/`, `.claude/` ya ignorados. Acción: decidir antes de compartir `v2` si `specs/` queda visible (ver D10) |
| VII. Ejemplo senior con subagentes | PASS | Ver "Reparto en subagentes" |
| VIII. Desarrollo asistido por IA | PASS | Kit con `CLAUDE.md`, guía y checklist |
| Restricciones (Claude, Streamlit, Databricks Free, español) | PASS | Verificación en cuenta de estudiante real pendiente (riesgo R1) |

**Post-Phase 1**: sin violaciones nuevas. Complejidad adicional justificada abajo.

## Project Structure

### Documentation (this feature)

```text
specs/001-curso-v2-end-to-end/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── etapas.md             # entradas/salidas de cada etapa del ejemplo y de cada hito
│   ├── estructura-repo.md    # layout obligatorio del repo del grupo (plantilla)
│   └── inferencia-app.md     # contrato de entrada/salida del modelo y de la app
├── checklists/requirements.md
└── tasks.md                  # lo crea /speckit-tasks
```

### Repositorio del curso (este repo, rama `v2`)

```text
README.md                      # nuevo: qué es el curso v2, cómo usar el repo
curso/
├── sesiones/                  # plan por día: objetivos, tiempos, demo, entregable
│   ├── fds1-viernes.md  fds1-sabado.md
│   ├── fds2-viernes.md  fds2-sabado.md
│   └── fds3-viernes.md  fds3-sabado.md
├── diapositivas/
│   ├── 00-nivelacion/         # pipeline, end-to-end, tracking, despliegue, tecnologías
│   └── demos/                 # una por etapa, derivada del ejemplo (md fuente + html)
├── guias/                     # instalacion.md, desarrollo-con-ia.md, databricks-mlflow.md,
│                              # streamlit-despliegue.md, git-github-basico.md
├── kit-estudiante/            # se copia al proyecto del grupo
│   ├── CLAUDE.md
│   ├── especificacion-proyecto.md
│   ├── prompts-por-etapa.md
│   ├── checklist-revision-ia.md
│   ├── .env.example
│   └── plantilla-repo/        # ver contracts/estructura-repo.md
└── evaluacion/                # rubrica.md, hitos.md, criterios-dataset.md, ficha-de-caso.md
data/                          # se conserva (datasets v1; el de Credit Score es el del ejemplo)
HOJA_DE_RUTA.md  hoja-de-ruta/ # se conservan (post-curso; actualizar menciones a MLflow/Databricks)
specs/  .specify/  .claude/    # instrucciones del instructor (ver D10)
```

Material v1 que se **retira** en implementación (queda en rama `v1` / tag `v1.0`): `ppts/`,
`notebooks/`, `INSTRUCCIONES_ENTREGA.md`, `requirements.txt` (se reemplaza por el del curso v2).

### Proyecto de ejemplo (`ejemplo/`, dentro de este repo)

```text
ejemplo/
├── README.md  CLAUDE.md
├── notebooks/                 # 01_caso_negocio  02_eda  03_preprocesamiento  04_features
│                              # 05_torneo  06_optimizacion  07_validacion_interpretacion
│                              # 08_registro_modelo  09_inferencia
├── src/creditsight/           # data/ features/ models/ tracking/ inference/ config.py
├── app/streamlit_app.py       # entrypoint de Streamlit Community Cloud
├── models/                    # modelo final .joblib + ficha del modelo
├── reports/                   # informe_tecnico.md (secciones por hito) + figuras
├── presentacion/              # ejecutiva.md (≤5 diapositivas, Marp)
├── tests/                     # pytest sobre src/
└── scripts/                   # verify_stage.* y check_databricks.py
```

`requirements.txt` y `.env.example` están en la **raíz del repo**; los datos en `data/` (raíz).

**Structure Decision**: un solo repositorio público. El material del curso y el ejemplo conviven;
el ejemplo sirve de modelo y de fuente de la plantilla de repo del grupo, y su app se despliega en
Streamlit Community Cloud desde este repo (el entrypoint puede estar en una subcarpeta). Los
estudiantes crean sus propios repos con la plantilla del kit.

## Reparto en subagentes

Cada pieza = un agente con entradas y salidas definidas en `contracts/`. El instructor revisa y
aprueba cada pieza (constitución, Flujo y puertas de calidad).

| Ola | Piezas | Dependencia | Paralelo |
|---|---|---|---|
| 0 | Entorno (`.venv`, paquetes), carpeta `ejemplo/` (esqueleto), contratos | ninguna | no (lo hace el instructor + asistente) |
| 1 | A: nivelación (diapositivas) · B: guía de desarrollo con IA · C: kit del estudiante · D: rúbrica, hitos, criterios de dataset, ficha de caso · E: guías de instalación/Databricks/Streamlit/Git | contratos de la Ola 0 | **sí**, 5 agentes |
| 2 | Cadena del ejemplo, en serie: caso → EDA → preprocesamiento → features → torneo → optimización → validación e interpretación → registro del modelo → módulos y tests → inferencia → app → informe técnico → presentación | cada etapa consume la salida de la anterior (`contracts/etapas.md`) | no (dependencias) |
| 3 | Demos y planes de sesión (uno por día), derivados del ejemplo; README del curso | Ola 2 completa | sí, por día |
| 4 | Verificación: ejecutar cada etapa en entorno limpio; aplicar la rúbrica al ejemplo con dos pasadas independientes; retirar material v1 | Olas 1–3 | verificaciones en paralelo |

## Complexity Tracking

| Decisión | Por qué se necesita | Alternativa más simple descartada porque |
|---|---|---|
| Cadena en serie para el ejemplo | Cada etapa depende de los artefactos de la anterior | Agentes en paralelo producirían etapas inconsistentes entre sí |
