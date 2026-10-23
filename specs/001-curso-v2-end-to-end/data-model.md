# Data Model — Curso v2 (Fase 1)

Entidades de la especificación, con campos y relaciones. Son registros de gestión del curso
(Markdown/CSV), no una base de datos.

## Grupo
- `group_id`, `name`, `members[]` (cada uno con `student_name`, `role` ∈ {datos, modelado, app,
  negocio}), `repo_url`, `app_url`, `case_id`.
- Relación: 1 Grupo → 1 Ficha de caso → N Hitos entregados → 1 Entregable final.
- Validación: ≥ 1 integrante por rol; `repo_url` público.

## Ficha de caso
- `case_id`, `business_question`, `dataset_source`, `dataset_rows`, `dataset_columns`,
  `target`, `problem_type` ∈ {clasificación, regresión, clusterización}, `primary_metric`,
  `business_cost_note`, `status` ∈ {borrador, devuelta, aprobada}, `reviewer_notes`.
- Estados: borrador → (devuelta → borrador)* → aprobada. Solo `aprobada` permite avanzar.
- Validación (criterios de dataset): volumen no trivial, mezcla de tipos de variable, objetivo
  definido, no coincide con los datasets de clase ni del ejemplo, sin datos confidenciales.

## Hito
- `milestone_id` ∈ {H1 caso+EDA+preprocesamiento, H2 modelo+tracking+repo modular, H3 app+
  presentación, H4 reporte final}, `due_date`, `acceptance_criteria[]`, `report_section`.
- Relación: pertenece a un fin de semana; cada Hito aporta una sección del reporte.

## Ejemplo de referencia (CreditSight)
- `stages[]` en orden: caso, EDA, preprocesamiento, features, torneo, optimización, validación,
  tracking, módulos, inferencia, app, reporte, presentación. Cada etapa: `inputs`, `outputs`,
  `verify_command` (ver `contracts/etapas.md`).

## Demo
- `demo_id`, `stage`, `source_notebook`, `duration_min` (≤ 20), `slides_file`.
- Relación: derivada de una etapa del ejemplo.

## Entregable final
- `repo`, `notebooks`, `model_ref` (nombre en el registro + archivo `.joblib`), `technical_report`,
  `executive_deck` (≤ 5 diapositivas), `app_url`.

## Rúbrica
- `criteria[]` con `name`, `weight` (la define el instructor), `levels[]`, `evidence`.
- Aplica a: hitos, entregables, exposición, aporte individual.

## Guía de desarrollo con IA / Kit del estudiante
- Kit: `CLAUDE.md`, `especificacion-proyecto.md`, `plantilla-repo/`, `prompts-por-etapa.md`,
  `checklist-revision-ia.md`, `.env.example`.
