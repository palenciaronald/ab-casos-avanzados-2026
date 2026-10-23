# Hitos del proyecto

Cuatro hitos: tres presenciales (uno por fin de semana) y la entrega final del reporte. Cada hito
aporta una sección del informe técnico, de modo que el reporte se construye de forma incremental.

| Hito | Fecha límite | Fin de semana | Sección del reporte que aporta |
|---|---|---|---|
| **H1** Caso, EDA y preprocesamiento | cierre del FDS 1 (sábado) | 1 | Caso de negocio; datos y limpieza |
| **H2** Modelo, tracking y repo modular | cierre del FDS 2 (sábado) | 2 | Features; torneo; optimización; validación; registro del modelo |
| **H3** App y presentación | viernes del FDS 3 | 3 | Despliegue; resumen ejecutivo |
| **H4** Reporte técnico final | 8 días tras la última clase | — | Informe completo ensamblado (todas las secciones) |

---

## H1 — Cierre del FDS 1

**Criterios de aceptación** (de `specs/001-curso-v2-end-to-end/contracts/etapas.md`):
- Ficha aprobada.
- EDA con ≥ 5 decisiones justificadas.
- Partición por la unidad correcta documentada.
- Limpieza reproducible por script.

**Entregan:** `reports/00_caso.md`, `reports/01_eda.md`, código de limpieza y partición en `src/`.

## H2 — Cierre del FDS 2

**Criterios de aceptación:**
- ≥ 3 modelos comparados con la misma validación.
- ≥ 1 experimento por candidato registrado.
- Modelo final registrado con versión.
- `src/` con pruebas.
- App local que carga el modelo.

**Entregan:** `reports/05_torneo.md`, `reports/07_validacion.md`, experimentos y modelo registrados en
Databricks (o MLflow local si se agotó la cuota), `src/` con `pytest` verde, esqueleto de la app.

## H3 — Viernes del FDS 3

**Criterios de aceptación:**
- App accesible por enlace público.
- Presentación ≤ 5 diapositivas.
- Ensayo de 10 minutos cronometrado.

**Entregan:** enlace de la app, `presentacion/ejecutiva.md` (o su exportación), registro del tiempo
del ensayo. Si la app no se desplegó, se aplica la penalización de la rúbrica (criterio A3, nivel máximo 1).

## H4 — 8 días tras la última clase

**Criterios de aceptación:** informe técnico completo con todas las secciones (caso, datos, features,
torneo, optimización, validación, registro, despliegue), con cada decisión justificada.

**Entrega:** `reports/informe_tecnico.md` en el repo del grupo.

---

## Reglas comunes
- Ninguna etapa usa el conjunto de prueba para decidir; se abre una sola vez, en la validación.
- Cada decisión de datos queda escrita con su motivo, no solo el código.
- Los cambios de datos y de unidad de análisis se documentan en el informe.
- El instructor revisa cada hito y responde con "aprobado" o "devuelto" y observaciones concretas.
