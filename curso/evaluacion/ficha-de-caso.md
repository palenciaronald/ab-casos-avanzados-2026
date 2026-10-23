# Ficha de caso

Cada grupo entrega **una ficha** el primer viernes. El instructor la aprueba o la devuelve con
observaciones concretas (criterios en `criterios-dataset.md`). **Solo una ficha aprobada permite
avanzar.** Se guarda en el repo del grupo como `reports/00_caso.md`.

## Campos

| Campo | Qué escribir |
|---|---|
| `case_id` | Identificador corto del caso, en minúsculas y con guiones (ej. `creditsight`) |
| `business_question` | La pregunta de negocio en 2–3 frases: quién decide, qué decide y con qué información |
| `dataset_source` | Nombre y enlace del dataset, y su licencia |
| `dataset_rows` | Número de filas |
| `dataset_columns` | Número de columnas |
| `target` | Columna que se predice (o "no hay: se agrupa", si es clusterización) |
| `problem_type` | `clasificación`, `regresión` o `clusterización` |
| `primary_metric` | Métrica principal y por qué es la que importa para el negocio |
| `business_cost_note` | Qué cuesta equivocarse en cada dirección, en términos del negocio |
| `status` | `borrador` → (`devuelta` → `borrador`)* → `aprobada` |
| `reviewer_notes` | Observaciones del instructor (las llena el instructor) |

**Estados.** Una ficha nace en `borrador`. Si el instructor la devuelve queda en `devuelta` con
sus notas; el grupo la corrige y vuelve a `borrador`. Solo cuando está `aprobada` el grupo sigue
con el EDA.

## Plantilla para copiar

```markdown
# Ficha de caso

- **case_id:**
- **business_question:**
- **dataset_source:**
- **dataset_rows:**
- **dataset_columns:**
- **target:**
- **problem_type:**
- **primary_metric:**
- **business_cost_note:**
- **status:** borrador
- **reviewer_notes:**
```

---

## Ejemplo diligenciado: CreditSight

# Ficha de caso

- **case_id:** `creditsight`

- **business_question:** *CreditSight* es una fintech que ofrece líneas de crédito digitales y
  debe decidir, para cada cliente, si le asigna **un límite alto, uno estándar o uno restringido**.
  Hoy el analista de riesgo revisa a mano el historial de crédito y tarda días. Queremos un modelo
  que clasifique a cada cliente en `Good`, `Standard` o `Poor` a partir de su perfil financiero y
  su historial de pagos, para **priorizar la revisión** del analista y acelerar las aprobaciones.
  La persona que usa el resultado es el analista de riesgo, que conserva la decisión final.

- **dataset_source:** *Credit score classification* (Kaggle, autor Rohan Paris, 2022), archivo
  `credit_score_classification.csv`. Datos sintéticos. **Licencia: por confirmar por el
  instructor** (ver `specs/001-curso-v2-end-to-end/research.md`).

- **dataset_rows:** 100.000

- **dataset_columns:** 28 (incluye 3 con datos personales sintéticos: `Name`, `SSN`, `ID`)

- **target:** `Credit_Score`, con tres clases: `Standard` (53,2 %), `Poor` (29,0 %) y `Good` (17,8 %).
  Unidad de análisis: **cliente-mes** (12.500 clientes × 8 meses). Un mismo cliente aparece en 8
  filas y su etiqueta cambia entre meses en el 58 % de los casos; por eso la partición para validar
  se hace **por cliente**, nunca por fila.

- **problem_type:** clasificación multiclase (desbalanceada)

- **primary_metric:** **Costo esperado por cliente-mes** con una matriz de costos de negocio (menor
  es mejor), porque equivocarse no cuesta lo mismo en las dos direcciones. Como controles se reportan
  **F1 macro** (ninguna clase puede ignorarse) y **recall de la clase `Poor`** (la que más cuesta no
  detectar). La exactitud (accuracy) no se usa: la clase mayoritaria sola ya da ~53 %.

- **business_cost_note:** Equivocarse no cuesta lo mismo en las dos direcciones.
  - **Clasificar como `Good` o `Standard` a un cliente que es `Poor`** (falso negativo de riesgo):
    se le asigna un límite que no podrá pagar y la fintech pierde capital. Es el error **más caro**.
  - **Clasificar como `Poor` a un cliente que es `Good`** (falso positivo): se le restringe el límite
    y se pierde un buen cliente y sus ingresos futuros, pero el daño es menor y recuperable porque
    el analista revisa el caso.
  - Matriz de costos usada (filas = clase real, columnas = clase predicha, en unidades de costo):

    | real \ predicho | Poor | Standard | Good |
    |---|---|---|---|
    | **Poor** | 0 | 3 | 10 |
    | **Standard** | 1 | 0 | 3 |
    | **Good** | 2 | 1 | 0 |

  - Por eso la decisión final no es la clase más probable sino la de **menor costo esperado**, y el
    modelo no decide solo: prioriza la cola del analista.

- **status:** aprobada (ejemplo del instructor)

- **reviewer_notes:** Caso de referencia. Puntos que el instructor señala en el ejemplo: (1) partir
  por cliente para evitar fuga entre meses; (2) eliminar `Name`, `SSN` y `ID` por ser datos personales;
  (3) medir el modelo con y sin `Credit_Mix`, porque podría reflejar casi directamente el objetivo
  (hipótesis a probar, no afirmada); (4) limpiar valores basura en columnas numéricas que llegan como
  texto.
