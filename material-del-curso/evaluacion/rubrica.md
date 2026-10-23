# Rúbrica de evaluación

Se publica el **primer viernes**. Cada criterio es observable: dos evaluadores que lean la misma
evidencia deben asignar el mismo nivel. Si un criterio no se puede decidir con la evidencia
indicada, el nivel es el inferior.

**Niveles:** 3 = cumple por completo · 2 = cumple en parte · 1 = cumple mínimamente · 0 = no cumple o no hay evidencia.

**Ponderación (`weight`):** `PENDIENTE: instructor` en cada criterio. Entre paréntesis va una
propuesta que suma 100 %.

---

## A. Hitos (ver `hitos.md`)

### A1. Ficha de caso y datos (H1) — weight: PENDIENTE: instructor (propuesta 10 %)
| Nivel | Descripción | Evidencia |
|---|---|---|
| 3 | Ficha aprobada con pregunta de negocio, dataset, métrica, tipo de problema y costo del error; EDA con ≥ 5 decisiones justificadas por escrito; unidad de partición documentada; limpieza reproducible por script | `reports/00_caso.md`, `reports/01_eda.md`, `src/` de datos |
| 2 | Ficha aprobada y EDA con 3–4 decisiones justificadas; limpieza reproducible | idem |
| 1 | Ficha aprobada; EDA con < 3 decisiones o limpieza solo en notebook | idem |
| 0 | Sin ficha aprobada | — |

### A2. Modelado y tracking (H2) — weight: PENDIENTE: instructor (propuesta 20 %)
| Nivel | Descripción | Evidencia |
|---|---|---|
| 3 | ≥ 3 modelos comparados con la misma validación; ≥ 1 ejecución por candidato registrada; modelo final registrado con versión; la partición respeta la unidad de análisis; prueba abierta una sola vez | tabla del torneo, experimentos en Databricks (o MLflow local), registro, historial del repo |
| 2 | Cumple lo anterior salvo un punto (p. ej. una sola ejecución por candidato) | idem |
| 1 | 2 modelos comparados o modelo sin versión registrada | idem |
| 0 | Un solo modelo, o sin registro | — |

### A3. App y presentación (H3) — weight: PENDIENTE: instructor (propuesta 10 %)
| Nivel | Descripción | Evidencia |
|---|---|---|
| 3 | App accesible por enlace público, devuelve predicción del modelo final con datos válidos y error claro con datos inválidos; presentación ≤ 5 diapositivas | enlace probado por el evaluador, archivo de la presentación |
| 2 | App pública que funciona con datos válidos pero sin validar entradas; o presentación de 6–7 diapositivas | idem |
| 1 | **App no desplegada**: corre en local con evidencia (captura de pantalla con fecha y repo, o demostración en vivo) y el plan de despliegue escrito | idem + evidencia local |
| 0 | Sin app funcionando | — |

> **Penalización por app no desplegada:** el nivel máximo de A3 es 1. No afecta a los demás criterios.

### A4. Reporte técnico (H4) — weight: PENDIENTE: instructor (propuesta 15 %)
| Nivel | Descripción | Evidencia |
|---|---|---|
| 3 | `informe_tecnico.md` entregado en plazo con todas las secciones (caso, datos, features, torneo, optimización, validación, registro, despliegue); cada decisión con su motivo | informe, fecha del commit |
| 2 | Entregado en plazo con 6–7 secciones, o secciones sin motivos | idem |
| 1 | Entregado con ≤ 5 secciones, o fuera de plazo hasta 3 días | idem |
| 0 | No entregado, o más de 3 días de retraso | — |

---

## B. Entregables

### B1. Repositorio modular — weight: PENDIENTE: instructor (propuesta 15 %)
| Nivel | Descripción | Evidencia |
|---|---|---|
| 3 | Cumple `contracts/estructura-repo.md`; `src/` con lógica reusable; notebooks solo orquestan; `pytest` pasa; `requirements.txt` en la raíz; sin credenciales ni datos personales; un tercero lo reproduce desde el README | revisión del repo, ejecución del evaluador |
| 2 | Estructura correcta y `pytest` pasa, pero parte de la lógica vive en notebooks | idem |
| 1 | Estructura parcial o no se reproduce sin ayuda | idem |
| 0 | Sin estructura o con credenciales o datos personales en el repo (en este caso el criterio es 0 aunque lo demás cumpla) | — |

### B2. Modelo final y ficha — weight: PENDIENTE: instructor (propuesta 5 %)
| Nivel | Descripción | Evidencia |
|---|---|---|
| 3 | `models/model.joblib` carga y predice; `ficha_modelo.md` con datos, métricas en prueba, límites, usos no recomendados y versión del registro | archivos del repo |
| 2 | Modelo carga; ficha incompleta | idem |
| 1 | Modelo sin ficha | idem |
| 0 | Sin modelo exportado | — |

---

## C. Exposición (ver `guia-exposicion.md`) — weight: PENDIENTE: instructor (propuesta 15 %)

| Nivel | Descripción | Evidencia |
|---|---|---|
| 3 | Dura ≤ 10 min; cubre caso de negocio, demo de la app en vivo y resultados con su costo de negocio; responde las preguntas | cronómetro del evaluador |
| 2 | Cubre las tres partes pero se pasa hasta 1 minuto, o la demo no es en vivo | idem |
| 1 | Omite una de las tres partes o se pasa más de 1 minuto | idem |
| 0 | Omite dos o más partes, o se pasa más de 2 minutos | — |

---

## D. Aporte individual (ver `aporte-individual.md`) — weight: PENDIENTE: instructor (propuesta 10 %)

Se asigna **por integrante**, no por grupo.

| Nivel | Descripción | Evidencia |
|---|---|---|
| 3 | Commits propios en ≥ 3 de las 4 áreas del repo (datos, modelado, app, reporte); explica correctamente un fragmento de código generado con IA elegido por el evaluador | historial del repo, pregunta oral |
| 2 | Commits propios en 2 áreas; explica correctamente con una pista | idem |
| 1 | Commits propios en 1 área; explicación parcial | idem |
| 0 | Sin commits propios o no puede explicar nada de lo que presenta | — |

---

## Resumen de la propuesta de ponderación

| Criterio | Propuesta |
|---|---|
| A1 Caso y datos | 10 % |
| A2 Modelado y tracking | 20 % |
| A3 App y presentación | 10 % |
| A4 Reporte técnico | 15 % |
| B1 Repositorio modular | 15 % |
| B2 Modelo final y ficha | 5 % |
| C Exposición | 15 % |
| D Aporte individual | 10 % |
| **Total** | **100 %** |

La nota final de cada estudiante = suma ponderada de A1–C (nota del grupo) y D (individual).
La fórmula exacta la fija el instructor al aprobar los pesos.
