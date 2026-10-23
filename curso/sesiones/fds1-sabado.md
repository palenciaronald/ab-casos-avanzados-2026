# Fin de semana 1 · Sábado — Caso, EDA y preprocesamiento

**Duración:** 4 horas · **Hito del día:** **H1** (ficha aprobada, EDA y preprocesamiento reproducible).

## Objetivos

Al terminar el sábado, cada grupo tiene:

1. Una **ficha de caso aprobada** por el instructor.
2. Un **EDA** que termina en decisiones escritas (mínimo 5, cada una justificada).
3. Un **preprocesamiento reproducible**: la limpieza como código, la partición por la unidad de
   análisis correcta y datos limpios listos para modelar.
4. La **sección del reporte** de caso y EDA.

## Cómo se organiza la sesión

El instructor muestra el ejemplo **en tres demos cortas de máximo 20 minutos**, cada una justo antes
de que los grupos trabajen esa etapa. Todas salen de `curso/diapositivas/demos/01-caso-eda-preproc.md`
y de los notebooks `01`, `02` y `03` de `ejemplo/notebooks/`. **No se programa en vivo:** se recorren
las decisiones de un notebook ya ejecutado.

> Si el grupo va muy adelantado, las tres demos se pueden dar seguidas (20 min en total, como una
> sola charla) y dedicar más tiempo al trabajo de grupos.

## Agenda

| Hora | Min | Bloque | Material |
|---|---|---|---|
| 0:00–0:10 | 10 | Apertura y estado de las fichas | `curso/evaluacion/ficha-de-caso.md` |
| 0:10–0:25 | 15 | **Demo A:** el caso de negocio | Secciones 1–3 (diap. 3–5) · `01_caso_negocio` |
| 0:25–0:50 | 25 | Trabajo de grupos: cerrar la ficha | — |
| 0:50–1:10 | 20 | **Demo B:** EDA | Secciones 4–8 (diap. 6–10) · `02_eda` |
| 1:10–1:55 | 45 | Trabajo de grupos: EDA | — |
| 1:55–2:05 | 10 | Descanso | — |
| 2:05–2:25 | 20 | **Demo C:** preprocesamiento y fuga | Secciones 9–13 (diap. 11–15) · `03_preprocesamiento` |
| 2:25–3:35 | 70 | Trabajo de grupos: limpieza, partición y pruebas | — |
| 3:35–3:50 | 15 | Puesta en común | — |
| 3:50–4:00 | 10 | Cierre: criterios de H1 y tarea autónoma | `specs/.../contracts/etapas.md` |

## Detalle por bloque

### 0:00 · Apertura y fichas (10 min)
- Devolver las fichas del viernes: **aprobadas**, **devueltas** (con observaciones concretas) o
  **pendientes**.
- Las devueltas se corrigen durante el bloque de las 0:25; ningún grupo avanza al EDA sin ficha
  aprobada.

### 0:10 · Demo A — el caso (15 min)
- Secciones 1–3 de la demo (diap. 3–5) y `01_caso_negocio`: pregunta de negocio ("quién decide, qué decide, con qué
  información"), **matriz de costos** y baseline sin modelo (siempre `Standard` cuesta 1,05;
  al azar, 1,62).
- Pedir a cada grupo que **traduzca su costo de equivocarse** a una matriz o, al menos, a dos frases.

### 0:25 · Trabajo de grupos — cerrar la ficha (25 min)
- El instructor aprueba las fichas pendientes en vivo, grupo por grupo.
- **Punto de control 1 (0:50):** todos los grupos tienen ficha aprobada o una fecha clara para
  cerrarla. Un grupo sin ficha aprobada se sienta con el instructor en el bloque siguiente.

### 0:50 · Demo B — EDA (20 min)
- Secciones 4–8 de la demo (diap. 6–10) y `02_eda`. Hilo: **cada hallazgo termina en una decisión escrita**
  (tabla de 10 decisiones de CreditSight en `ejemplo/reports/01_eda.md`).
- Puntos a subrayar: datos que llegan como texto → basura; salto brusco tras p95–p97 → corrupción;
  variables que **deberían** ser estables; vacío que significa algo ("sin préstamos").
- Preguntas para los grupos: *¿qué variable de su dataset debería ser estable y no lo es? ¿qué
  significa un vacío en su dataset?*

### 1:10 · Trabajo de grupos — EDA (45 min)
- Cada grupo trabaja en `notebooks/02_eda.ipynb` de su repo, con el kit de prompts por etapa.
- **Punto de control 2 (1:45):** el instructor pasa por cada grupo y comprueba que tienen una lista
  de **al menos 3 decisiones** ya escritas con su motivo (las 5 completas se cierran en el bloque
  siguiente). Preguntar a un integrante distinto de quien escribió: *¿por qué esa decisión?*

### 2:05 · Demo C — preprocesamiento y fuga (20 min)
- Secciones 9–13 de la demo (diap. 11–15) y `03_preprocesamiento`. Hilo: de decisiones a **código con pruebas**
  (`src/<paquete>/data/`); el notebook solo orquesta.
- **Momento central (5 min):** la fuga por partición. Mismo modelo y datos; solo cambia cómo se parte:

  | Partición | Clientes en ambos lados | F1 macro | Costo esperado |
  |---|---|---|---|
  | Por fila (mal) | 10.449 | 0,734 | 0,65 |
  | Por cliente (bien) | 0 | 0,695 | 0,73 |

- Pregunta de transferencia: *¿cuál es su unidad de análisis? ¿qué se repite en sus filas?*

### 2:25 · Trabajo de grupos — limpieza, partición y pruebas (70 min)
- Cada grupo convierte sus decisiones del EDA en código en `src/<paquete>/data/` y crea al menos una
  prueba que verifica la **partición por su unidad de análisis**.
- Se pide a Claude con el kit, pero con la regla del curso: **revisar el resultado** con
  `kit-estudiante/checklist-revision-ia.md` (¿corre desde cero?, ¿filtra información?, ¿se entiende
  cada línea?).
- **Punto de control 3 (3:10):** cada grupo muestra (1) la limpieza corriendo de principio a fin,
  (2) cómo parte los datos y por qué, y (3) `pytest` en verde. Ningún grupo termina sin declarar su
  unidad de análisis por escrito.

### 3:35 · Puesta en común (15 min)
- Cada grupo dice en un minuto: **su unidad de análisis** y **un hallazgo que no esperaban**. El
  tiempo por grupo se ajusta a la cantidad de grupos del día.
- El instructor señala patrones: fugas posibles que vio, decisiones de imputación que conviene
  revisar.

### 3:50 · Cierre (10 min)
- Revisión de los criterios de **H1** (abajo) y qué falta por grupo.
- **Trabajo autónomo hasta el fin de semana 2:** cerrar lo pendiente de H1 y dejar el pipeline base
  (preprocesamiento + un modelo simple) para entrar directo al feature engineering y al torneo.

## Criterios de aceptación de H1

Tomados de `specs/001-curso-v2-end-to-end/contracts/etapas.md`:

- **Ficha aprobada.**
- **EDA con al menos 5 decisiones justificadas** (`reports/01_eda.md`).
- **Partición por la unidad correcta, documentada** y verificada con una prueba.
- **Limpieza reproducible por script**: corre de principio a fin desde el repositorio del grupo.

## Qué entrega cada grupo al terminar

| Entregable | Dónde |
|---|---|
| Ficha de caso aprobada | `reports/00_caso.md` |
| EDA con decisiones | `notebooks/02_eda.ipynb` y `reports/01_eda.md` |
| Limpieza y partición como código | `src/<paquete>/data/` + `tests/` |
| Datos limpios y partición | `data/processed/` (se regeneran con el notebook 03) |
| **Sección del reporte** de caso y EDA | `reports/` (primera parte del informe técnico) |

## Reglas de la sesión

- **La prueba no se toca:** se guarda la partición y no se vuelve a mirar hasta la etapa de
  validación final.
- **Decisiones antes que código:** primero la decisión con su motivo, luego el código.
- **Sin ficha aprobada no hay EDA.**
- **Cada integrante explica lo que generó la IA:** el instructor pregunta a quien no escribió el código.

## Lo que el instructor debe tener listo

- [ ] `01-caso-eda-preproc.md` exportado a HTML y los tres notebooks (`01`–`03`) ejecutados y abiertos.
- [ ] Fichas del viernes revisadas con observaciones concretas.
- [ ] Una lista de verificación por grupo con los tres puntos de control.
- [ ] `ejemplo/reports/00_caso.md` y `ejemplo/reports/01_eda.md` a mano como modelos.
