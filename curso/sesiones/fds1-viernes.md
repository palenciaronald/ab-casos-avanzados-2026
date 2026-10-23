# Fin de semana 1 · Viernes — Nivelación, herramientas y elección de caso

**Duración:** 4 horas · **Entregable del día:** ficha de caso en **borrador** (una por grupo).

## Objetivos

Al terminar el viernes, cada estudiante:

1. Sabe en qué puntos del curso previo tiene vacíos (sin que se los reenseñemos).
2. Maneja el vocabulario del curso: pipeline, proyecto end-to-end, tracking, despliegue.
3. Tiene su entorno instalado y la conexión probada (o un plan B documentado).
4. Conoce la rúbrica y el kit de trabajo con Claude.
5. Pertenece a un grupo que ya tiene una ficha de caso en borrador.

> **Principio del curso.** No se repite lo que ya vieron. El diagnóstico sirve para **detectar
> vacíos y orientar**, no para dar clase.

## Agenda

| Hora | Min | Bloque | Material |
|---|---|---|---|
| 0:00–0:10 | 10 | Bienvenida: qué es el curso, tres fines de semana, entregables y hitos | Esta guía |
| 0:10–0:55 | 45 | **Diagnóstico** de lo visto en el curso previo | `curso/diapositivas/00-nivelacion/diagnostico.md` |
| 0:55–1:10 | 15 | Lectura de resultados y plan de apoyo (sin reenseñar) | — |
| 1:10–1:50 | 40 | **Nivelación** conceptual | `curso/diapositivas/00-nivelacion/nivelacion.md` |
| 1:50–2:00 | 10 | Descanso | — |
| 2:00–2:20 | 20 | **Tecnologías** del curso | `curso/diapositivas/00-nivelacion/tecnologias.md` |
| 2:20–2:55 | 35 | **Instalación guiada** + prueba de conexión | `curso/guias/instalacion.md` |
| 2:55–3:10 | 15 | **Publicar la rúbrica** y **presentar el kit** | `curso/evaluacion/rubrica.md`, `curso/kit-estudiante/` |
| 3:10–3:55 | 45 | **Formación de grupos** y elección de caso | `curso/evaluacion/criterios-dataset.md`, `curso/evaluacion/ficha-de-caso.md` |
| 3:55–4:00 | 5 | Cierre y tarea | — |

## Detalle por bloque

### 0:00 · Bienvenida (10 min)
- Calendario: tres fines de semana, 24 horas presenciales, trabajo autónomo entre ellos.
- Entregables del grupo: repositorio modular, notebooks, modelo final, reporte técnico, presentación
  de máximo 5 diapositivas y app desplegada. Exposición de máximo 10 minutos el último sábado.
- Hitos con fecha: H1 (cierre de este fin de semana), H2, H3 y H4 (`curso/evaluacion/hitos.md`).

### 0:10 · Diagnóstico (45 min)
- Se proyecta `diagnostico.md`: **12 preguntas**, cada una con su respuesta en la diapositiva
  siguiente. Los estudiantes responden primero por escrito y comparan después.
- **Regla del instructor:** se muestra la respuesta, se hace una aclaración de **un minuto** como
  máximo y se sigue. Si hay muchas fallas en un tema, se anota; no se detiene la sesión.
- Si el ritmo se atrasa, se recorta a las 8 preguntas más relevantes para el curso (fuga,
  validación por grupo, desbalance/umbral, calibración, pipeline).

### 0:55 · Lectura de resultados (15 min)
- Cada estudiante identifica sus 2–3 vacíos mayores con la tabla de lectura del diagnóstico.
- El instructor propone **apoyo fuera de clase** (el material del curso previo, la guía del kit),
  no clase extra. Los grupos se armarán después, y conviene que cada grupo tenga al menos una
  persona fuerte en cada tema que apareció como vacío frecuente.

### 1:10 · Nivelación (40 min)
- Se proyecta `nivelacion.md` (CreditSight como hilo conductor): pipeline, proyecto end-to-end,
  tracking de modelos y despliegue.
- La diapositiva de **tracking** parte del problema *"¿cuál de las 30 pruebas de ayer era la
  buena?"*. Pedir a los estudiantes que cuenten cómo lo resuelven hoy.
- Pregunta de cierre: *¿qué parte del proyecto les parece más difícil de hacer solos?* Anotar las
  respuestas: orientan las demos del fin de semana 2.

### 2:00 · Tecnologías (20 min)
- Se proyecta `tecnologias.md`: Python con `.venv`, Git y GitHub, VS Code con la extensión de Claude
  Code, Databricks Free Edition, MLflow y Streamlit.
- Para cada herramienta se dice **qué NO tienen que dominar**. Se recuerda que usarán Claude como
  asistente obligatorio (plan individual de pago si no lo tienen) y la sección de cuota en
  `curso/guias/desarrollo-con-ia.md`.

### 2:20 · Instalación guiada (35 min)
- Cada estudiante sigue `curso/guias/instalacion.md` en su equipo. El instructor y un apoyo
  circulan.
- **Meta mínima de la prueba:** crear el entorno, completar `.env` y ejecutar
  `python ejemplo/scripts/check_databricks.py` con resultado "OK".
- Anotar en una lista visible quién queda **pendiente** y por qué (ver plan B).

### 2:55 · Rúbrica y kit (15 min)
- **Rúbrica** (`curso/evaluacion/rubrica.md`): recorrerla criterio por criterio, sin entrar en
  detalle de ponderación (la fija el instructor). Subrayar la regla del curso: *cada integrante debe
  poder explicar el código que la IA generó*, y que habrá una pregunta oral.
- **Kit** (`curso/kit-estudiante/`): mostrar `CLAUDE.md`, la plantilla de especificación del
  proyecto, los prompts por etapa y la lista de revisión del código generado. Decir dónde se copia
  (al repositorio del grupo) y que la IA lo lee antes de generar nada.

### 3:10 · Grupos y caso (45 min)
1. **Formar grupos** (10 min) con roles sugeridos: datos, modelado, app y negocio. El tamaño y la
   cantidad los define el instructor ese día según la asistencia.
2. **Criterios de dataset** (10 min): se proyecta `criterios-dataset.md`. Recordar que **no** valen
   los datasets de clase ni los del curso previo, ni los del ejemplo, y que los datos del trabajo
   solo si no son confidenciales.
3. **Elegir y escribir la ficha** (25 min): cada grupo diligencia la plantilla de
   `curso/evaluacion/ficha-de-caso.md` con `status: borrador`. Tomar como modelo el ejemplo de
   CreditSight (`ejemplo/reports/00_caso.md`).
- El instructor recorre los grupos y filtra de inmediato: dataset trivial, objetivo ambiguo, sin
  costo de equivocarse definible.

### 3:55 · Cierre (5 min)
- **Tarea:** completar y corregir la ficha; dejar el repositorio del grupo creado (plantilla del
  kit copiada) y compartir el enlace.
- **Mañana:** la ficha se aprueba o se devuelve en la primera media hora.

## Plan B si la instalación falla

| Situación | Qué hacer |
|---|---|
| El equipo no deja instalar (equipo corporativo) | Trabajar **en pareja** con un compañero cuyo entorno funcione; la persona sin entorno participa en EDA y decisiones y avisa al instructor |
| Databricks no conecta (token, perfil, cuota) | Poner `MLFLOW_FORCE_LOCAL=1` en `.env`: el código usa MLflow local y el curso continúa; la conexión se arregla con calma antes del fin de semana 2 |
| El CLI de Databricks no está en el `PATH` | Cambiar a la **opción B** (host y token personal) del `.env.example`, que no requiere el CLI |
| Error de codificación en consola de Windows | Definir `PYTHONUTF8=1` en `.env` (está en la sección de errores comunes de la guía) |
| No tiene plan de Claude | Seguir la política de respaldo de `curso/guias/desarrollo-con-ia.md` y avisar al instructor hoy |
| Quedan más de 5 personas sin entorno al final del bloque | Dejar de instalar en grupo; el instructor abre una **sesión de apoyo** antes del sábado y se sigue con los grupos |

> **Criterio para no bloquear a todos:** la instalación nunca debe consumir más del bloque
> asignado. Lo que no se resuelva a las 2:55 pasa a apoyo individual.

## Entregable del día

- Ficha de caso en `borrador` por grupo (`reports/00_caso.md` del repo del grupo).
- Lista de pendientes de instalación con responsable.
- Lista de vacíos frecuentes detectados en el diagnóstico (insumo para el fin de semana 2).

## Lo que el instructor debe tener listo

- [ ] `diagnostico.md`, `nivelacion.md` y `tecnologias.md` revisados y exportados a HTML.
- [ ] Rúbrica publicada y accesible para todos.
- [ ] Kit disponible en un enlace (carpeta `curso/kit-estudiante/`).
- [ ] Un apoyo para la instalación (otra persona o un grupo avanzado).
- [ ] Ejemplo de CreditSight abierto (`ejemplo/reports/00_caso.md`).
