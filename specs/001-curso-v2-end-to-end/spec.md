# Feature Specification: Curso v2 — Laboratorios de Casos Avanzados (proyecto end-to-end tipo startup)

**Feature Branch**: `v2` (rama de trabajo existente; no se crea rama nueva)

**Created**: 2026-10-18

**Status**: Draft

**Input**: User description: "Diseñar y producir todo el material del instructor y de los estudiantes para tres fines de semana (viernes y sábado, 4 h cada día), con un proyecto end-to-end por grupo tratado como startup, sobre estudiantes que ya cursaron un curso previo de IA pero no son desarrolladores y no vieron tracking de experimentos ni despliegue."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - El instructor dispone de un ejemplo de referencia completo (Priority: P1)

El instructor necesita un proyecto de ejemplo, de nivel senior de ciencia de datos, que recorra
todas las etapas del curso sobre el dataset de clasificación Credit Score, para tener de dónde
sacar las demos y para que los grupos tengan un estándar que imitar.

**Why this priority**: Es la base de todo el curso. Sin el ejemplo no hay demos, ni criterio de
evaluación, ni plantilla de entregables. Además puede producirse y validarse sin esperar a los
estudiantes.

**Independent Test**: Una persona ajena ejecuta el ejemplo desde cero en un entorno limpio, sigue
las etapas en orden y llega a una app funcionando y a un reporte técnico y una presentación
completos, sin intervención del autor.

**Acceptance Scenarios**:

1. **Given** el repositorio recién clonado y un entorno limpio, **When** se ejecutan las etapas
   del ejemplo en orden, **Then** cada etapa corre sin errores y deja el insumo de la siguiente.
2. **Given** el ejemplo terminado, **When** se revisa contra la lista de etapas del curso (caso
   de negocio, EDA, preprocesamiento, feature engineering, torneo, optimización, validación,
   tracking, código modular, modelo final, inferencia, app, reporte, presentación), **Then**
   ninguna etapa falta.
3. **Given** la presentación ejecutiva del ejemplo, **When** se cuentan sus diapositivas,
   **Then** son cinco o menos y explican el caso, la decisión de negocio y el resultado sin
   jerga técnica.

---

### User Story 2 - Un grupo avanza del caso de negocio al modelo en el primer fin de semana (Priority: P1)

Los estudiantes forman grupos, eligen un caso de negocio con un dataset de su elección y, con
demos cortas del instructor sobre el ejemplo, producen la ficha del caso, el EDA y el
preprocesamiento de su propio proyecto.

**Why this priority**: Es el primer hito y condiciona todo lo posterior: un caso débil arruina
los dos fines de semana siguientes.

**Independent Test**: Al cierre del primer sábado, cada grupo tiene una ficha de caso aprobada
por el instructor, un EDA de su dataset y un preprocesamiento reproducible.

**Acceptance Scenarios**:

1. **Given** el primer viernes, **When** el grupo presenta su caso, **Then** el instructor lo
   aprueba o lo devuelve con observaciones concretas según criterios publicados de dataset
   (volumen, mezcla de tipos de variable, objetivo definido, no repetir los datasets de clase).
2. **Given** un caso aprobado, **When** el grupo termina el primer sábado, **Then** entrega EDA y
   preprocesamiento con la sección correspondiente del reporte.
3. **Given** un estudiante que no recuerda los conceptos del curso previo, **When** consulta la
   nivelación del primer viernes, **Then** encuentra explicados pipeline, proyecto end-to-end,
   tracking de modelos y despliegue en lenguaje no técnico.

---

### User Story 3 - Un grupo modela, optimiza y registra su modelo (Priority: P2)

En el segundo fin de semana el grupo hace feature engineering, el torneo de modelos, la
optimización, la validación y la interpretación, registra sus experimentos y su modelo en la
plataforma de seguimiento y deja su código modular, con un esqueleto de la app.

**Why this priority**: Es el núcleo técnico y el tema nuevo (tracking, registro) que el curso
previo no cubrió, pero depende de que el primer hito esté cumplido.

**Independent Test**: Al cierre del segundo sábado, cada grupo muestra experimentos registrados
y comparables, un modelo final registrado, un repositorio con código modular y una app local
que carga el modelo.

**Acceptance Scenarios**:

1. **Given** el preprocesamiento del primer hito, **When** el grupo completa el torneo y la
   optimización, **Then** los experimentos quedan registrados con parámetros y métricas y
   permiten comparar los candidatos.
2. **Given** el modelo elegido, **When** se registra, **Then** puede recuperarse desde el
   registro y usarse para predecir sobre datos nuevos.
3. **Given** el código del grupo, **When** otra persona lo revisa, **Then** está separado en
   módulos con una estructura reconocible y los notebooks solo orquestan.

---

### User Story 4 - Un grupo despliega su app y defiende el producto (Priority: P2)

En el tercer fin de semana el grupo despliega su app de forma pública y gratuita, termina la
presentación ejecutiva y la expone en un máximo de 10 minutos.

**Why this priority**: Es el entregable visible y el cierre del end-to-end, pero depende de los
dos hitos anteriores.

**Independent Test**: El último sábado, el grupo abre su app desplegada desde un enlace público,
la usa en vivo durante la exposición y responde preguntas.

**Acceptance Scenarios**:

1. **Given** el modelo registrado y el esqueleto de la app, **When** el grupo despliega, **Then**
   la app es accesible por enlace público y devuelve predicciones del modelo final.
2. **Given** la exposición de un grupo, **When** transcurren 10 minutos, **Then** se cortó o
   terminó, y cubrió caso de negocio, demo de la app y resultados.
3. **Given** un estudiante del grupo, **When** el instructor le pregunta por una parte del
   código generada con IA, **Then** puede explicar qué hace y por qué está ahí.

---

### User Story 5 - Un estudiante no desarrollador programa con ayuda de IA (Priority: P2)

Un estudiante sin experiencia de desarrollo usa una guía de trabajo con herramientas de IA para
construir el código modular y la app, aprendiendo a pedir, revisar, probar y corregir.

**Why this priority**: Es la condición que hace viable el despliegue para un grupo sin
desarrolladores y se aplica desde el primer viernes.

**Independent Test**: Un estudiante sin experiencia previa, siguiendo solo la guía, pone en
marcha una app mínima y localiza y corrige un error provocado a propósito.

**Acceptance Scenarios**:

1. **Given** la guía, **When** un estudiante sigue sus pasos, **Then** obtiene una app mínima
   funcionando con su modelo.
2. **Given** el kit inicial copiado a un proyecto vacío, **When** el estudiante pide a su asistente
   de IA crear la estructura del proyecto, **Then** el resultado respeta la estructura exigida por
   la rúbrica sin que el estudiante la haya descrito.
3. **Given** código generado por IA con un fallo, **When** el estudiante aplica el método de
   revisión de la guía, **Then** identifica el fallo y lo corrige o lo reporta con precisión.

---

### User Story 6 - El instructor evalúa con una rúbrica conocida desde el inicio (Priority: P3)

El instructor dispone de una rúbrica, hitos con criterios de aceptación y una forma de verificar
el aporte individual dentro de cada grupo, y se la entrega a los estudiantes el primer día.

**Why this priority**: Da transparencia y evita que el trabajo del grupo recaiga en una sola
persona, pero puede terminarse en paralelo al contenido.

**Independent Test**: Un evaluador aplica la rúbrica al ejemplo de referencia y obtiene la
calificación máxima esperada; aplicada a un entregable incompleto, señala qué falta.

**Acceptance Scenarios**:

1. **Given** la rúbrica, **When** se revisa contra los entregables, **Then** cada entregable y
   cada hito tienen criterios de aceptación explícitos.
2. **Given** un grupo, **When** se evalúa el aporte individual, **Then** hay evidencia
   verificable por integrante.

---

### Edge Cases

- Un grupo elige un dataset trivial, muy pequeño o sin objetivo claro: el instructor lo devuelve
  con criterios publicados y propone alternativas.
- Un grupo propone datos de su trabajo que podrían ser confidenciales: no se aceptan sin una
  confirmación explícita de que pueden compartirse.
- Un grupo elige clusterización, donde no hay etiqueta con qué validar: se exige perfilado de
  negocio y evaluación de estabilidad como sustituto.
- La plataforma de seguimiento gratuita no permite alguna función prometida: el curso tiene una
  alternativa documentada que mantiene el objetivo de aprendizaje.
- La app no logra desplegarse a tiempo: el grupo entrega la app corriendo en local con evidencia
  y un plan de despliegue, con una penalización definida en la rúbrica.
- Un estudiante no cursó todas las sesiones del curso previo: la nivelación del primer viernes
  y los materiales de apoyo le permiten ponerse al día.
- Un integrante no aporta al grupo: la evidencia individual lo hace visible.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El curso MUST organizarse en tres fines de semana (viernes y sábado, 4 horas cada
  día) y cada día MUST tener un plan de sesión con objetivos, tiempos y entregable.
- **FR-002**: El primer viernes MUST incluir una nivelación conceptual (pipeline, proyecto
  end-to-end, tracking de modelos, despliegue) y una introducción a las tecnologías del curso,
  sin reenseñar la técnica de modelado del curso previo.
- **FR-003**: El primer viernes MUST incluir la formación de grupos y la elección del caso de
  negocio, con un dataset libre (recomendación: Kaggle; también datos propios no confidenciales).
- **FR-004**: El curso MUST publicar criterios de aceptación de datasets y un formato de ficha de
  caso (pregunta de negocio, dataset, métrica, tipo de problema), y el instructor MUST aprobar
  cada caso antes de que el grupo avance.
- **FR-005**: El instructor MUST contar con un ejemplo de referencia completo sobre el dataset
  Credit Score que cubra todas las etapas del curso, incluida la inferencia, la app, el reporte
  técnico y la presentación ejecutiva.
- **FR-006**: Cada etapa del ejemplo de referencia MUST ser reproducible desde un entorno limpio
  siguiendo instrucciones escritas.
- **FR-007**: El curso MUST proveer demos cortas derivadas del ejemplo, una por etapa, que los
  grupos aplican a su propio caso.
- **FR-008**: El curso MUST cubrir tracking y registro de modelos en la plataforma gratuita
  indicada, con una guía paso a paso y una alternativa documentada si alguna función no está
  disponible.
- **FR-009**: El curso MUST proveer una plantilla de repositorio modular para el grupo y MUST
  mostrar cómo pasar de notebooks a módulos.
- **FR-010**: El curso MUST proveer una guía de desarrollo asistido por IA para no
  desarrolladores (cómo pedir, revisar, probar y corregir) y MUST exigir que cada integrante
  explique el código generado por IA.
- **FR-011**: Cada grupo MUST entregar: repositorio modular, notebooks, modelo final, reporte
  técnico, presentación ejecutiva de cinco diapositivas o menos y app desplegada de forma
  pública y gratuita.
- **FR-012**: El reporte técnico MUST construirse por secciones, una por hito, con una versión
  final entregable hasta 8 días después de la última clase.
- **FR-013**: El curso MUST definir hitos con fecha y criterios de aceptación para cada fin de
  semana y para el trabajo autónomo entre ellos.
- **FR-014**: El último sábado MUST dedicarse a exposiciones de máximo 10 minutos por grupo, con
  preguntas, y el último viernes MUST dedicarse a la app, la presentación y el ensayo.
- **FR-015**: El curso MUST proveer una rúbrica de evaluación, publicada el primer día, que
  incluya evidencia verificable del aporte individual por integrante.
- **FR-016**: El material del instructor, las soluciones, el contrato, los trabajos de
  estudiantes y el material de terceros (el del curso previo) MUST permanecer fuera del
  repositorio versionado.
- **FR-017**: El curso MUST decidir y documentar qué material de la versión anterior se conserva
  (datos, README) y qué se reemplaza (presentaciones, notebooks de demo y plantillas), sin
  perder la versión anterior.
- **FR-018**: Las capacidades reales de la plataforma de seguimiento gratuita MUST verificarse y
  documentarse antes del primer fin de semana.
- **FR-019**: Todo el material para estudiantes MUST estar en español.
- **FR-020**: El curso MUST entregar a los estudiantes un kit inicial de especificaciones
  generales para trabajar con IA (instrucciones permanentes para el asistente, plantilla de
  especificación del proyecto, estructura de repositorio vacía, prompts por etapa y lista de
  revisión del código generado) y MUST explicarlo el primer viernes, de modo que el asistente
  conozca el contexto del curso y la estructura exigida por la rúbrica.

### Key Entities

- **Grupo**: equipo de estudiantes con un caso, integrantes con rol y evidencia de aporte
  individual.
- **Ficha de caso**: pregunta de negocio, dataset, métrica, tipo de problema y estado de
  aprobación.
- **Hito**: entregable con fecha y criterios de aceptación, asociado a un fin de semana.
- **Ejemplo de referencia**: proyecto completo del instructor del que derivan las demos.
- **Demo**: pieza corta por etapa, derivada del ejemplo de referencia.
- **Entregable final**: conjunto de repositorio, notebooks, modelo, reporte, presentación y app.
- **Rúbrica**: criterios de evaluación de hitos, entregables, exposición y aporte individual.
- **Guía de desarrollo con IA**: método para pedir, revisar, probar y corregir código asistido.
- **Kit del estudiante**: carpeta con instrucciones para la IA, plantilla de especificación, estructura de repositorio, prompts por etapa y lista de revisión.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Una persona ajena reproduce el ejemplo de referencia de principio a fin en un
  entorno limpio, sin ayuda del autor, y llega a la app funcionando.
- **SC-002**: Al cierre del primer sábado, el 100 % de los grupos tiene una ficha de caso
  aprobada, un EDA y un preprocesamiento reproducible.
- **SC-003**: Al cierre del segundo sábado, al menos el 90 % de los grupos tiene experimentos
  registrados y comparables, un modelo final registrado y un repositorio modular.
- **SC-004**: Al finalizar el tercer fin de semana, al menos el 90 % de los grupos expone con su
  app accesible por enlace público.
- **SC-005**: El 100 % de las exposiciones respeta el máximo de 10 minutos y cubre caso de
  negocio, demo de la app y resultados.
- **SC-006**: Un estudiante sin experiencia de desarrollo sigue la guía y pone en marcha una app
  mínima funcionando en menos de 60 minutos.
- **SC-007**: Cada estudiante responde correctamente al menos una pregunta del instructor sobre
  una parte del código generada con IA en su proyecto.
- **SC-008**: Las 8 horas de cada fin de semana tienen un plan con objetivo, tiempos y
  entregable, y ninguna sesión repite contenido del curso previo salvo la nivelación conceptual
  del primer viernes.
- **SC-009**: La rúbrica se aplica al ejemplo de referencia sin ambigüedad: dos evaluadores
  independientes asignan la misma calificación por criterio en al menos el 90 % de los casos.

## Assumptions

- El número de grupos y de estudiantes se conoce el primer viernes y no condiciona el diseño del
  material, aunque sí el tiempo de exposición del último sábado.
- Los estudiantes dominan el contenido técnico del curso previo (pipelines, validación cruzada,
  ensambles, tuning, métricas, SHAP, calibración, deriva, segmentación) y no son
  desarrolladores de software.
- Los estudiantes conocen algo de la plataforma de seguimiento gratuita, aunque no su uso para
  tracking y registro.
- Entre fines de semana hay trabajo autónomo de grupo (aproximadamente una semana cada vez).
- La app se despliega con la herramienta gratuita definida en la constitución del curso; esa
  herramienta y la plataforma de seguimiento gratuita se mantienen disponibles durante el curso.
- Todos los estudiantes trabajan con el asistente de IA Claude (el instructor lo exige); quien no
  lo tenga contrata el plan de pago individual de nivel básico, que se asume asumible porque
  todos trabajan. Tienen además una cuenta en la plataforma de seguimiento gratuita y un
  repositorio donde alojar su proyecto.
- El kit del estudiante (FR-020) se escribe pensando en Claude, con sus instrucciones
  permanentes en el archivo que esa herramienta lee por defecto.
- El dataset del ejemplo de referencia ya está en el repositorio y su licencia permite
  redistribuirlo; los datasets de los grupos los eligen ellos.
- La versión anterior del curso queda congelada en su propia rama y etiqueta y no se modifica.
- La creación de la rúbrica incluye el peso relativo de cada criterio; la ponderación concreta
  la decide el instructor al revisar el borrador.
