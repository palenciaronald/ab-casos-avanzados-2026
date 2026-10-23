---
description: "Lista de tareas del curso v2: ejemplo de referencia, material de sesiones, kit del estudiante y evaluación"
---

# Tasks: Curso v2 — Laboratorios de Casos Avanzados (proyecto end-to-end tipo startup)

**Input**: `specs/001-curso-v2-end-to-end/` (plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md)

**Prerequisites**: plan.md, spec.md. Constitución v1.1.1.

**Tests**: se piden pruebas `pytest` solo para `src/` del ejemplo (plan: Testing) y la ejecución de notebooks en entorno limpio como prueba de reproducibilidad. No se piden pruebas para el material didáctico.

**Organization**: por historia de usuario (spec.md). La cadena del ejemplo (US1) es **secuencial**; el resto del material se puede producir en paralelo una vez cumplidos los contratos.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: se puede ejecutar en paralelo (archivos distintos, sin dependencias abiertas).
- **[Story]**: US1…US6 según la historia de spec.md.
- **Rutas**: todo vive en este repo (rama `v2`). `COURSE/` = raíz del repo (material del curso); `EXAMPLE/` = `ejemplo/` dentro del repo (proyecto CreditSight). Los estudiantes crean su propio repo; este es el del instructor.
- Todo texto para estudiantes en español; identificadores de código en inglés.

---

## Phase 1: Setup

**Purpose**: preparar la carpeta del ejemplo, el entorno compartido y los archivos de configuración del repo.

- [X] T001 Crear la carpeta `EXAMPLE/` (`ejemplo/`) dentro de este repo para el proyecto CreditSight; el remoto ya existe (`origin`, repo público `palenciaronald/ab-casos-avanzados-2026`); no hacer push sin confirmación del instructor
- [X] T002 [P] Crear el esqueleto de carpetas del ejemplo según `contracts/estructura-repo.md` en `EXAMPLE/` (`data/raw`, `data/processed`, `notebooks`, `src/creditsight/{data,features,models,tracking,inference}`, `tests`, `models`, `app`, `reports`, `presentacion`, `scripts`) con un `.gitkeep` donde esté vacío
- [X] T003 [P] Escribir `requirements.txt` **en la raíz del repo** (Streamlit lo busca en la raíz o junto al entrypoint) con versiones fijadas, Python 3.12: pandas, scikit-learn, xgboost, lightgbm, optuna, shap, mlflow, databricks-sdk, python-dotenv, streamlit, joblib, pytest, nbconvert, nbformat, ipykernel (tomar las versiones reales del `.venv` ya probado; reemplaza al `requirements.txt` de la v1, que sigue en la rama `v1`)
- [X] T004 [P] Verificar que el `.gitignore` de la raíz cubre `.env`, `.venv/`, `__pycache__/`, `.ipynb_checkpoints/` y los datos con licencia dudosa, y completar `.env.example` de la raíz con las dos formas de conectar: perfil (`PROFILE=<perfil de ~/.databrickscfg>`; URIs `databricks://<perfil>` y `databricks-uc://<perfil>`) y token (`DATABRICKS_HOST`, `DATABRICKS_TOKEN`), más `PYTHONUTF8=1`; sin secretos
- [X] T005 [P] Crear la estructura del curso en `COURSE/curso/{sesiones,diapositivas/00-nivelacion,diapositivas/demos,guias,kit-estudiante/plantilla-repo,evaluacion}` con un `README.md` de una línea por carpeta

---

## Phase 2: Foundational (bloquea todas las historias)

**Purpose**: scripts de verificación y los chequeos de riesgo del plan.

**⚠️ CRITICAL**: ninguna historia empieza antes de cerrar T006 y T007.

- [X] T006 Escribir `EXAMPLE/scripts/verify_stage.ps1` (y `verify_stage.sh`): crea un entorno limpio con `uv venv --python 3.12`, instala `requirements.txt`, fija `PYTHONUTF8=1`, ejecuta el notebook indicado con `jupyter nbconvert --execute` y falla si el código de salida no es 0 (research D13); verificar además que `npx @marp-team/marp-cli` exporta un `.md` de prueba a HTML
- [X] T007 [P] Escribir `EXAMPLE/scripts/check_databricks.py`: lee `.env`; si `PROFILE` existe usa `databricks://<PROFILE>` y `databricks-uc://<PROFILE>`, si no usa host y token; dentro de Databricks lo detecta con `is_databricks()` (variable `DATABRICKS_RUNTIME_VERSION`) y no configura nada; crea un experimento en `/Users/<usuario>/<nombre>`, registra un run con un parámetro y una métrica, registra un modelo de juguete en `workspace.default.<nombre>`; lee `.env` con `python-dotenv` (basado en las pruebas ya hechas, research D3)
- [ ] T008 Verificar la licencia del dataset de Kaggle de `data/01-clasificacion/credit_score_classification.csv` (ya está en `data/` del repo público; si no permite redistribuir, retirarlo del seguimiento y documentar la descarga) y anotar la decisión en `data/README.md` (research D8, riesgo R4)
- [ ] T009 [P] Ejecutar `EXAMPLE/scripts/check_databricks.py` con una cuenta **nueva** de Databricks Free Edition (no la del instructor) y anotar el resultado y los límites encontrados en `specs/001-curso-v2-end-to-end/research.md` bajo "Verificación R1"; incluir si Model Serving y Databricks Apps están disponibles
- [X] T010 [P] Verificar qué incluye hoy el plan individual básico de Claude (uso de Claude Code, límites por ventana) y redactar la política de respaldo (qué hacer sin cuota o sin tarjeta) en `COURSE/curso/guias/desarrollo-con-ia.md` sección "Cuota y respaldo" (research D12, riesgo R2)

**Checkpoint**: entorno y verificación listos; riesgos R1, R2 y R4 documentados; el instructor revisa y aprueba cada pieza antes de publicarla.

---

## Phase 3: User Story 1 — Ejemplo de referencia completo (Priority: P1) 🎯 MVP

**Goal**: CreditSight, de nivel senior, reproducible desde un entorno limpio, que cubre las 13 etapas de `contracts/etapas.md`.

**Independent Test**: una persona ajena clona el repo, sigue el README de `EXAMPLE/`, ejecuta las etapas en orden y llega a la app funcionando, al informe y a la presentación sin ayuda del autor (SC-001).

**Cadena secuencial** (cada tarea depende de la anterior; salvo indicación):

- [X] T011 [US1] Escribir `EXAMPLE/notebooks/01_caso_negocio.ipynb` y `EXAMPLE/reports/00_caso.md`: ficha de caso de CreditSight (pregunta de negocio sobre decisión de crédito con costos asimétricos de equivocarse, métrica principal justificada, tipo de problema = clasificación, riesgos éticos) en el formato de `COURSE/curso/evaluacion/ficha-de-caso.md` (depende de T034)
- [X] T012 [US1] Escribir `EXAMPLE/notebooks/02_eda.ipynb` y `EXAMPLE/reports/01_eda.md`: documentar que son 100000 filas = 12500 clientes × 8 meses y que el objetivo cambia dentro del mismo cliente en el 58 % de los casos; distribución del objetivo (Standard 53,2 %, Poor 29,0 %, Good 17,8 %); cuantificar la basura por columna (research D5); ≥ 5 decisiones de datos justificadas
- [X] T013 [US1] Implementar `EXAMPLE/src/creditsight/data/cleaning.py`: eliminar `Name`, `SSN`, `ID` (datos personales); convertir a numérico `Age`, `Annual_Income`, `Num_of_Loan`, `Num_of_Delayed_Payment`, `Outstanding_Debt`, `Changed_Credit_Limit`, `Amount_invested_monthly`, `Monthly_Balance`; tratar marcadores de basura en `Occupation`, `Credit_Mix`, `Payment_Behaviour`; recortar `Age` fuera de 14–100; convertir `Credit_History_Age` ("22 Years and 1 Months") a meses
- [X] T014 [US1] Implementar `EXAMPLE/src/creditsight/data/split.py`: partición entrenamiento/validación/prueba **por `Customer_ID`** con `StratifiedGroupKFold`/`GroupShuffleSplit`; la prueba queda cerrada hasta la etapa 7; función que verifica que ningún cliente aparece en dos particiones
- [X] T015 [US1] Escribir `EXAMPLE/notebooks/03_preprocesamiento.ipynb` que orquesta T013 y T014 y deja `EXAMPLE/data/processed/`; incluir una demostración corta de la fuga: métrica con partición por fila vs. por cliente
- [X] T016 [US1] Implementar `EXAMPLE/src/creditsight/features/` (agregados por cliente-mes si son legítimos, razones de deuda e ingreso, tratamiento de `Credit_Mix`) y el `ColumnTransformer` en `features/pipeline.py`; escribir `EXAMPLE/notebooks/04_features.ipynb` con la tabla de variables y su justificación; medir el modelo **con y sin `Credit_Mix`** (hipótesis de research D5)
- [X] T017 [US1] Escribir `EXAMPLE/notebooks/05_torneo.ipynb` y `EXAMPLE/reports/05_torneo.md`: ≥ 4 candidatos (regresión logística, bosque, XGBoost/LightGBM y un baseline) con validación cruzada **por grupo**, métricas apropiadas al desbalance y al costo de negocio, tabla comparativa con dispersión entre folds; el código reutilizable va en `EXAMPLE/src/creditsight/models/`, no inline; registrar cada candidato en MLflow es recomendable pero opcional
- [X] T018 [US1] Implementar `EXAMPLE/src/creditsight/tracking/mlflow_utils.py` antes de la optimización: configurar la conexión desde `.env` (`PROFILE` → `databricks://<perfil>` y `databricks-uc://<perfil>`, o host y token; `is_databricks()` dentro de Databricks), función para abrir un experimento, registrar parámetros, métricas y artefactos de cada ejecución, y respaldo con MLflow local si se agota la cuota; probarlo con `EXAMPLE/scripts/check_databricks.py`
- [ ] T019 [US1] Escribir `EXAMPLE/notebooks/06_optimizacion.ipynb`: Optuna sobre 1–2 finalistas, **registrando cada trial como ejecución en MLflow con `mlflow_utils` (T018)**, con espacio de búsqueda justificado, número de trials acotado para respetar la cuota de Databricks (riesgo R3), y evidencia de que la mejora sobrevive a la validación anidada o a un conjunto separado
- [ ] T020 [US1] Escribir `EXAMPLE/notebooks/07_validacion_interpretacion.ipynb` y `EXAMPLE/reports/07_validacion.md`: abrir la prueba **una sola vez**; matriz de confusión con costos, umbral de decisión, calibración, SHAP global y por cliente, análisis de errores por segmento, riesgos de equidad
- [ ] T021 [US1] Escribir `EXAMPLE/notebooks/08_registro_modelo.ipynb`: elegir la mejor ejecución de la optimización, registrar el modelo final en Unity Catalog con firma y ejemplo de entrada, asignar versión y alias, documentar cómo recuperarlo; explicar qué diferencia hay entre tracking (ejecuciones) y registro (versiones del modelo)
- [ ] T022 [US1] Completar y probar los módulos de `EXAMPLE/src/creditsight/models/` (entrenamiento, evaluación) que se vienen escribiendo desde las etapas anteriores y escribir `EXAMPLE/tests/test_cleaning.py`, `test_split.py` (aserción: ningún cliente en dos particiones), `test_features.py`, `test_inference.py`; `pytest` MUST pasar; los notebooks solo orquestan
- [ ] T023 [US1] Implementar `EXAMPLE/src/creditsight/inference/predict.py` según `contracts/inferencia-app.md` (columnas crudas de entrada, clase, probabilidades, indicador de confianza, errores claros) y exportar `EXAMPLE/models/model.joblib` desde la versión registrada; escribir `EXAMPLE/notebooks/09_inferencia.ipynb` y `EXAMPLE/models/ficha_modelo.md`
- [ ] T024 [US1] Implementar `EXAMPLE/app/streamlit_app.py` según `contracts/inferencia-app.md`: formulario validado, predicción, probabilidades, explicación comprensible para no técnicos y aviso de uso responsable; carga `models/model.joblib` sin consultar Databricks (research D6)
- [ ] T025 [US1] Desplegar la app en Streamlit Community Cloud desde este repo público (rama `v2`), entrypoint `ejemplo/app/streamlit_app.py`, Python 3.12, `requirements.txt` en la raíz; anotar el enlace público en `EXAMPLE/README.md` (requiere la confirmación del instructor antes de publicar)
- [ ] T026 [US1] Escribir `EXAMPLE/reports/informe_tecnico.md` ensamblando las secciones de cada etapa (caso, EDA, datos, features, torneo, optimización, validación, tracking, despliegue) en lenguaje claro
- [ ] T027 [US1] Escribir `EXAMPLE/presentacion/ejecutiva.md` (Marp, **máximo 5 diapositivas**: problema, enfoque, resultado y costo de negocio, demo de la app, riesgos y siguientes pasos) y exportar a PPTX
- [ ] T028 [US1] Escribir `EXAMPLE/README.md` (qué es CreditSight, cómo reproducir de principio a fin, enlace a la app, estructura) y ejecutar `verify_stage` sobre cada notebook 01–09 desde un entorno limpio, anotando el tiempo total (meta: < 30 min de cómputo)

**Checkpoint**: el ejemplo es reproducible; una persona ajena lo valida (T069); el instructor revisa y aprueba cada pieza antes de publicarla.

---

## Phase 4: User Story 2 — Primer fin de semana del grupo (Priority: P1)

**Goal**: nivelación, formación de grupos y ficha de caso aprobada, más EDA y preprocesamiento en el sábado.

**Independent Test**: al cierre del primer sábado, cada grupo tiene ficha aprobada, EDA y preprocesamiento reproducible (SC-002).

- [X] T029 [P] [US2] Escribir `COURSE/curso/diapositivas/00-nivelacion/nivelacion.md` (Marp): qué es un pipeline, qué es un proyecto end-to-end, qué es el tracking de modelos, qué es desplegar un modelo; lenguaje no técnico, sin reenseñar técnica de modelado (FR-002); usar CreditSight como hilo conductor; la diapositiva de tracking parte del problema ("¿cuál de las 30 pruebas de ayer era la buena?") y explica para qué sirve: comparar, reproducir, auditar y entregar
- [X] T030 [P] [US2] Escribir `COURSE/curso/diapositivas/00-nivelacion/tecnologias.md` (Marp): Python y `.venv`, Git y GitHub, VS Code con la extensión de Claude Code, Databricks Free Edition, MLflow, Streamlit; para cada una, qué hace y qué NO tiene que dominar el estudiante
- [X] T031 [P] [US2] Escribir `COURSE/curso/guias/instalacion.md`: paso a paso en Windows y macOS (VS Code, extensión de Claude, `uv`, Python 3.12, clonar la plantilla, crear `.env` desde `.env.example`, `PYTHONUTF8=1`, comprobar con el script de T007); incluir los errores comunes (consola cp1252)
- [X] T032 [P] [US2] Escribir `COURSE/curso/guias/git-github-basico.md`: crear cuenta, repo público, `clone`, `add`, `commit`, `push`, `pull` y qué hacer ante un conflicto; solo lo imprescindible, con capturas descritas paso a paso
- [X] T033 [P] [US2] Escribir `COURSE/curso/evaluacion/criterios-dataset.md`: volumen mínimo, mezcla de tipos de variable, objetivo definido, no coincidir con los datasets de clase ni del ejemplo, sin datos confidenciales ni personales sin anonimizar; incluir dónde buscar (Kaggle) y casos de rechazo
- [X] T034 [P] [US2] Escribir `COURSE/curso/evaluacion/ficha-de-caso.md` con los campos de `data-model.md` (`business_question`, `dataset_source`, `dataset_rows`, `dataset_columns`, `target`, `problem_type`, `primary_metric`, `business_cost_note`, `status`: borrador → devuelta → aprobada) y un ejemplo diligenciado con CreditSight
- [X] T035 [US2] Escribir `COURSE/curso/sesiones/fds1-viernes.md`: tiempos de las 4 h (diagnóstico corto de 45 min de lo visto con Leo, nivelación, tecnologías, instalación guiada, formación de grupos, elección de caso), entregable del día y criterio de aceptación de la ficha; incluir dos bloques con tiempo: publicar la rúbrica y presentar el kit de especificaciones (`kit-estudiante/`) (depende de T029–T034)
- [X] T036 [US2] Escribir `COURSE/curso/sesiones/fds1-sabado.md`: demo de levantamiento del caso, EDA y preprocesamiento sobre CreditSight (≤ 20 min cada una), trabajo de grupos con apoyo del instructor, cierre con criterios de H1 de `contracts/etapas.md` (depende de T012–T015)
- [X] T037 [P] [US2] Escribir `COURSE/curso/diapositivas/demos/01-caso-eda-preproc.md` (Marp): demo ≤ 20 minutos derivada de los notebooks 01–03 del ejemplo, con la fuga por partición como momento central
- [X] T038 [P] [US2] Escribir un diagnóstico de 45 minutos de lo visto en el curso previo en `COURSE/curso/diapositivas/00-nivelacion/diagnostico.md`: 10–12 preguntas cortas (pipeline, validación cruzada, fuga, métricas por desbalance) con respuestas, solo para detectar vacíos y orientar, **sin reenseñar** (el principio II de la constitución prohíbe repetir lo visto)

**Checkpoint**: material del FDS 1 listo; el instructor revisa y aprueba cada pieza antes de publicarla.

---

## Phase 5: User Story 5 — Desarrollo asistido por IA para no desarrolladores (Priority: P2)

**Goal**: guía y kit que permiten a un estudiante sin experiencia programar con Claude.

**Independent Test**: un estudiante sin experiencia previa, siguiendo solo la guía, pone en marcha una app mínima en menos de 60 minutos y corrige un error provocado a propósito (SC-006).

- [X] T039 [P] [US5] Escribir `COURSE/curso/kit-estudiante/CLAUDE.md`: contexto del curso, estructura obligatoria de `contracts/estructura-repo.md`, estilo (español en textos, inglés en identificadores), "explica lo que haces: soy analista, no desarrollador", no inventar datos, no subir `.env` ni datos personales, partición por unidad correcta, no usar la prueba para decidir
- [X] T040 [P] [US5] Escribir `COURSE/curso/kit-estudiante/especificacion-proyecto.md`: plantilla que el grupo diligencia (caso, dataset, métrica, tipo de problema, entregables, riesgos) y que Claude lee antes de generar código
- [X] T041 [P] [US5] Escribir `COURSE/curso/kit-estudiante/prompts-por-etapa.md`: un bloque por etapa de `contracts/etapas.md` (EDA, preprocesamiento, features, torneo, optimización, validación, tracking, módulos, inferencia, app, reporte, presentación) con el prompt probado, qué esperar y cómo revisarlo; incluir prompts de ahorro de cuota
- [X] T042 [P] [US5] Escribir `COURSE/curso/kit-estudiante/checklist-revision-ia.md`: ¿corre desde cero?, ¿filtra información entre particiones?, ¿entiendo cada línea?, ¿hay credenciales o datos personales?, ¿se abrió la prueba una sola vez?, ¿puedo explicarlo oralmente?
- [X] T043 [US5] Crear `COURSE/curso/kit-estudiante/plantilla-repo/` copiando de `EXAMPLE/` la estructura vacía de `contracts/estructura-repo.md` (carpetas con `.gitkeep`, `README.md`, `.gitignore`, `.env.example`, `requirements.txt` base, `scripts/check_databricks.py`) para que cada grupo cree **su propio repo** (depende de T002–T004, T007)
- [X] T044 [US5] Escribir `COURSE/curso/guias/desarrollo-con-ia.md`: flujo pedir → revisar → probar → corregir con un ejemplo de error provocado, cómo pedir en pasos pequeños, cómo leer un traceback, cuándo desconfiar, y la política de respaldo de T010
- [ ] T045 [US5] Validar el kit con una persona sin experiencia de desarrollo: copiar el kit a un proyecto vacío, pedir a Claude crear la estructura y poner en marcha una app mínima; cronometrar y anotar atascos en `specs/001-curso-v2-end-to-end/research.md` bajo "Validación del kit"; corregir los archivos T039–T044 según lo encontrado

**Checkpoint**: kit validado con un usuario real; el instructor revisa y aprueba cada pieza antes de publicarla.

---

## Phase 6: User Story 3 — Modelado, optimización y tracking del grupo (Priority: P2)

**Goal**: material del segundo fin de semana.

**Independent Test**: al cierre del segundo sábado, cada grupo muestra experimentos registrados, modelo final registrado, repo modular y app local (SC-003).

- [X] T046 [P] [US3] Escribir `COURSE/curso/diapositivas/demos/02-features-torneo.md` (Marp, ≤ 20 min): derivada de los notebooks 04 y 05 del ejemplo; foco en validación cruzada por grupo y en el costo de negocio de la métrica
- [ ] T047 [P] [US3] Escribir `COURSE/curso/diapositivas/demos/03-optimizacion-validacion.md` (Marp, ≤ 20 min): notebooks 06 y 07; foco en optimización honesta con cuota limitada, prueba abierta una sola vez, calibración y SHAP
- [ ] T048 [P] [US3] Escribir `COURSE/curso/diapositivas/demos/04-tracking-modulos.md` (Marp, ≤ 20 min): notebooks 08, `src/` y pruebas; de notebook a módulo
- [X] T049 [P] [US3] Escribir `COURSE/curso/guias/databricks-mlflow.md`: crear cuenta en Free Edition, generar el token personal, completar `.env`, ejecutar `check_databricks.py`, leer la interfaz de experimentos, registrar un modelo, qué hacer si se agota la cuota (MLflow local), uso no comercial
- [ ] T050 [US3] Escribir `COURSE/curso/sesiones/fds2-viernes.md`: tiempos de las 4 h (feature engineering, torneo, optimización con tracking en MLflow, con demo corta y trabajo de grupos), entregable del día (depende de T046, T047)
- [ ] T051 [US3] Escribir `COURSE/curso/sesiones/fds2-sabado.md`: validación, registro del modelo, modularización y esqueleto de la app Streamlit; cierre con criterios de H2 de `contracts/etapas.md` (depende de T048, T049)

**Checkpoint**: material del FDS 2 listo; el instructor revisa y aprueba cada pieza antes de publicarla.

---

## Phase 7: User Story 4 — Despliegue y exposición (Priority: P2)

**Goal**: material del tercer fin de semana.

**Independent Test**: el último sábado, el grupo abre su app desplegada por enlace público, la usa en vivo y responde preguntas (SC-004, SC-005).

- [X] T052 [P] [US4] Escribir `COURSE/curso/guias/streamlit-despliegue.md`: de la app local a Streamlit Community Cloud (repo público, `requirements.txt` en la raíz, Python 3.12, `models/model.joblib` dentro del repo, errores comunes de despliegue)
- [ ] T053 [P] [US4] Escribir `COURSE/curso/diapositivas/demos/05-despliegue-presentacion.md` (Marp, ≤ 20 min): despliegue de la app y estructura de una presentación ejecutiva de **máximo 5 diapositivas**, usando `EXAMPLE/presentacion/ejecutiva.md` como modelo
- [X] T054 [P] [US4] Escribir `COURSE/curso/evaluacion/guia-exposicion.md`: formato de 10 minutos (caso 2, app 4, resultados 3, cierre 1) más preguntas, cronometraje y qué se evalúa
- [ ] T055 [US4] Escribir `COURSE/curso/sesiones/fds3-viernes.md`: tiempos de las 4 h (despliegue, presentación, ensayo cronometrado), criterios de H3 (depende de T052, T053)
- [ ] T056 [US4] Escribir `COURSE/curso/sesiones/fds3-sabado.md`: orden de exposiciones, tiempos por grupo, preguntas sobre código generado con IA (SC-007), cierre y entrega del reporte final en 8 días (H4) (depende de T054)

**Checkpoint**: material del FDS 3 listo; el instructor revisa y aprueba cada pieza antes de publicarla.

---

## Phase 8: User Story 6 — Rúbrica y evaluación (Priority: P3)

**Goal**: evaluación transparente, publicada el primer día.

**Independent Test**: dos evaluadores aplican la rúbrica al ejemplo de referencia y coinciden en ≥ 90 % de los criterios (SC-009).

- [X] T057 [US6] Escribir `COURSE/curso/evaluacion/rubrica.md`: criterios de hitos, entregables, exposición y aporte individual, con niveles y evidencia por criterio; dejar la ponderación (`weight`) marcada para que el instructor la fije
- [X] T058 [P] [US6] Escribir `COURSE/curso/evaluacion/hitos.md`: H1–H4 con fecha, criterios de aceptación de `contracts/etapas.md` y la sección del reporte que aporta cada uno
- [X] T059 [P] [US6] Escribir `COURSE/curso/evaluacion/aporte-individual.md`: cómo se verifica el aporte de cada integrante (roles, commits del repo, pregunta oral sobre el código de IA)
- [ ] T060 [US6] Aplicar la rúbrica al ejemplo con dos pasadas independientes (dos agentes sin acceso a la otra evaluación) y registrar la coincidencia en `specs/001-curso-v2-end-to-end/research.md` bajo "Validación de la rúbrica"; ajustar los criterios ambiguos

**Checkpoint**: rúbrica validada; el instructor revisa y aprueba cada pieza antes de publicarla.

---

## Phase 9: Polish & cross-cutting

- [ ] T061 Retirar el material v1 de la rama `v2` (los estudiantes de esta edición solo siguen `v2` y no usan nada de la v1) cuando existan sus reemplazos: borrar `COURSE/ppts/`, `COURSE/notebooks/` y `COURSE/INSTRUCCIONES_ENTREGA.md` (quedan en la rama `v1` y el tag `v1.0`; el `requirements.txt` de la raíz ya lo reemplazó T003); conservar `COURSE/data/`, `COURSE/HOJA_DE_RUTA.md`, `COURSE/hoja-de-ruta/` (research D11)
- [ ] T062 Reescribir `COURSE/README.md`: qué es el curso v2, estructura de carpetas, calendario de los tres fines de semana, cómo usar el kit y dónde está el ejemplo (`ejemplo/`)
- [ ] T063 [P] Actualizar `COURSE/HOJA_DE_RUTA.md` y `COURSE/hoja-de-ruta/hoja_de_ruta.html` para que MLflow y Databricks aparezcan como cubiertos en el curso y se ajusten los siguientes pasos
- [ ] T064 [P] Reescribir `COURSE/data/README.md` con los datasets conservados y su uso en el curso v2
- [ ] T065 Revisar que el `.gitignore` del repo cubre `.env`, `.venv/`, `curso_Leo_IA/`, `contrato/`, `soluciones-instructor/`, `material-instructor/`, trabajos de estudiantes y datos personales (constitución VI); ejecutar `git status` y `git ls-files` para comprobar que nada ignorado está versionado
- [ ] T066 Antes de compartir `v2` con los estudiantes: (a) decidir si `specs/` se queda visible en `v2` (sirve como ejemplo de desarrollo guiado por especificaciones, pero muestra decisiones internas del instructor) o se retira de la rama; (b) fijar `v2` como rama por defecto del repo en GitHub o indicar `git clone -b v2`; (c) `main` y `v1` quedan para el grupo anterior y no se tocan; (d) subir `v2` solo con confirmación del instructor
- [ ] T067 Ejecutar `quickstart.md` completo en un entorno limpio, corregir los pasos que fallen y exportar todas las diapositivas `COURSE/curso/diapositivas/**/*.md` a HTML con Marp
- [ ] T068 Repasar la constitución v1.1.1 contra el material producido (principios I–VIII) y revisar cada plan de sesión contra el listado de lo visto en el curso previo (SC-008: nada repetido salvo la nivelación) y anotar cualquier desviación en `specs/001-curso-v2-end-to-end/research.md` bajo "Revisión final"
- [ ] T069 Pedir a una persona que no escribió el ejemplo que lo reproduzca desde el README en un entorno limpio, cronometrando cada atasco (SC-001), y corregir `EXAMPLE/README.md` y los scripts según el resultado

---

## Dependencies & Execution Order

- **Phase 1 → Phase 2 → historias.** T006 y T007 bloquean todo lo demás.
- **US1 es una cadena en serie** (T011 → T028). T011 depende además de la ficha de caso de T034 (el formato); lanzar T034 antes de T011.
- **US5 (T039–T044) y US6 (T057–T059) y las guías de US2/US4 (T029–T034, T052, T054)** no dependen de US1 y se pueden producir en paralelo, una vez cumplidos los contratos.
- **Las demos y planes de sesión** de US2/US3/US4 dependen de las etapas del ejemplo que reflejan (T036 ← T012–T015; T046 ← T016–T017; T047 ← T019–T020; T048 ← T021–T022; T053 ← T027).
- **Polish** al final; T061 solo cuando exista el reemplazo.

## Parallel Example: ola de materiales independientes (tras Phase 2)

Cinco agentes simultáneos: (A) T029, T030, T038 · (B) T044, T039 · (C) T040, T041, T042 · (D) T033, T034, T057 · (E) T031, T032, T049, T052.

## Implementation Strategy

1. **MVP = US1**: Phases 1, 2 y 3 dan el ejemplo reproducible. Se puede enseñar con solo eso, aunque con menos soporte para los grupos.
2. Añadir US2 y US5 para poder dar el primer fin de semana.
3. Añadir US3 antes del segundo fin de semana y US4 antes del tercero (cada uno se puede terminar mientras avanza el curso).
4. US6 (rúbrica) debe estar lista antes del primer viernes, porque la rúbrica se publica ese día (constitución IV).
5. Cada pieza producida por un subagente la revisa y aprueba el instructor antes de publicarse.
