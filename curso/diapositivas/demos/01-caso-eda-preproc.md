---
marp: true
theme: default
paginate: true
header: "Casos Avanzados · Maestría en Ingeniería Analítica"
footer: "Fin de semana 1 · Sábado · Demo 1: caso, EDA y preprocesamiento"
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Demo 1 · Del caso de negocio a datos limpios
## CreditSight: caso, EDA y preprocesamiento

**Fin de semana 1 · Sábado · ≤ 20 minutos**

Notebooks `01`, `02` y `03` del ejemplo

<!--
Duración total: 20 min. Distribución sugerida: caso 4 min (diapositivas 2-3), EDA 6 min (4-8),
preprocesamiento 3 min (9-10), fuga por partición 5 min (11-13), cierre 2 min (14).
Abrir los tres notebooks ejecutados en VS Code; no se programa en vivo, se recorren las decisiones.
-->

---

# Lo que van a ver, y lo que NO

**Sí:** cómo se pasa de una pregunta de negocio a datos listos para modelar, y **por qué cada decisión**.

**No:** técnica de limpieza que ya conocen. Aquí importa el **criterio**.

| Etapa | Notebook | Entrega |
|---|---|---|
| Caso de negocio | `01_caso_negocio` | Ficha de caso |
| EDA | `02_eda` | Hallazgos → decisiones |
| Preprocesamiento | `03_preprocesamiento` | Datos limpios + partición por cliente |

<!--
Recordar el contrato: cada etapa deja un artefacto que consume la siguiente (specs/.../contracts/etapas.md).
-->

---

# 1 · La pregunta de negocio

**CreditSight** es una fintech de líneas de crédito digitales. Para cada cliente decide: **límite alto, estándar o restringido**.

> ¿Podemos clasificar a cada cliente como `Good`, `Standard` o `Poor` para **priorizar la revisión** del analista de riesgo y acelerar aprobaciones?

- Quien usa el resultado: el **analista de riesgo**, que decide.
- El modelo **no decide solo**: ordena la cola de trabajo.

<!--
Mostrar la ficha de caso real: ejemplo/reports/00_caso.md. Insistir en "quién decide, qué decide, con qué información".
Pedir a los estudiantes que piensen ya en SU caso: ¿quién usa el resultado?
-->

---

# 2 · Equivocarse no cuesta lo mismo

Matriz de costos (filas = real, columnas = decisión):

| | Poor | Standard | Good |
|---|---|---|---|
| **real Poor** | 0 | 3 | **10** |
| **real Standard** | 1 | 0 | 3 |
| **real Good** | 2 | 1 | 0 |

Aprobar a un `Poor` como `Good` cuesta **10**; rechazar a un `Good` como `Poor` cuesta **2**.

**Sin modelo:** siempre `Standard` cuesta **1,05** por cliente; al azar, **1,62**.

<!--
Son unidades relativas, no dólares. Lo que importa es la proporción. El 1,05 es el punto que cualquier modelo debe vencer.
Esta matriz decide la métrica del proyecto: costo esperado (menor es mejor). F1 macro y recall de Poor son controles.
-->

---

# 3 · Qué es una fila

`Customer_ID` + `Month`: ¿una fila es un cliente?

- **100.000 filas = 12.500 clientes × 8 meses** (enero a agosto).
- Una fila es un **cliente-mes**, no un cliente.
- La etiqueta cambia entre meses en el **58 %** de los clientes.

> Consecuencia que veremos al final de la demo: **cómo se parte el dato decide si la métrica es honesta.**

<!--
Notebook 02, sección 1 y sección 2 (objetivo). Distribución del objetivo: Standard 53,2 %, Poor 29,0 %, Good 17,8 %.
Predecir siempre Standard acierta el 53 %: por eso accuracy no sirve.
-->

---

# 4 · EDA: ¿qué tan sucios están los datos?

Columnas numéricas que llegaron como **texto**: casi siempre hay basura dentro.

- Números con guion bajo pegado: `'23_'`
- **Centinelas**: `'_'`, `'_______'`, `'!@9#%8'`
- `'__10000__'`: **4.305 filas** con exactamente el mismo valor en `Amount_invested_monthly`

> Un valor repetido tantas veces no es un dato: es un **marcador de "no disponible"**.

<!--
Notebook 02, sección 3. El EDA no es hacer gráficos: es descubrir qué decisiones hay que tomar.
Preguntar a la audiencia: ¿lo habrían detectado con describe()? (El tipo de dato texto ya era la pista).
-->

---

# 5 · EDA: valores imposibles

Los percentiles suben normal hasta ~p95–p97 y luego **se disparan**:

| Columna | p97 | p99 |
|---|---|---|
| `Num_Bank_Accounts` | 10 | 445 |
| `Interest_Rate` | 34 | 2.865 |
| `Age` | 55 | 4.112 |

Y hay negativos imposibles (edad −500, préstamos −100).

**Decisión:** fuera de un rango plausible → **vacío**, no se borra la fila.

<!--
Notebook 02, sección 4. El salto brusco es lo que distingue corrupción de cola natural.
Borrar el ~3 % de filas por una columna sería peor que imputar ese dato.
-->

---

# 6 · EDA: lo que debería ser estable

Edad, ocupación o ingreso **no cambian en 8 meses**. ¿Cuántos clientes muestran cambios?

- Crudo: ocupación **44,4 %**, ingreso **48,2 %**, `Credit_Mix` **83,8 %**.
- Solo con valores válidos: **0 %** en ocupación, ingreso, tasa, préstamos y `Credit_Mix`.

La diferencia entre meses era **ruido**. Eso habilita reparar con **el valor válido más frecuente del propio cliente** (no mira otros clientes, no hay fuga).

<!--
Notebook 02, sección 5. Excepción honesta: la edad sube exactamente +1 (cumpleaños, 6.877 pasos mensuales); es variación real, no ruido.
Solo 5 clientes tienen una edad corrupta que sigue dentro del rango (95 en un mes y 24 en los demás).
-->

---

# 7 · EDA: dos columnas que no son lo que parecen

- **`Type_of_Loan` vacío = sin préstamos.** Coincide con `Num_of_Loan == 0` en las 95.652 filas donde `Num_of_Loan` es válido. No se imputa: se **interpreta**.
- **Antigüedad crediticia:** sube **exactamente un mes por mes** (72.373 de 72.373 diferencias). Los vacíos (9 %) se **reconstruyen**, no se imputan.

> Entender el dato permite reparar mejor que cualquier imputación estadística.

<!--
Notebook 02, sección 6. Mensaje de fondo: antes de imputar, pregunten qué significa el vacío.
-->

---

# 8 · EDA → diez decisiones escritas

| # | Hallazgo | Decisión |
|---|---|---|
| 1 | Datos personales | Eliminar `Name`, `SSN`, `ID` |
| 2 | Cliente-mes | Particiones **por cliente** |
| 3 | Accuracy = 53 % sin modelo | Métrica = costo esperado |
| 4–5 | Centinelas e imposibles | → vacío |
| 6–7 | Estables con ruido | Valor del propio cliente |
| 8–9 | Préstamos y antigüedad | Interpretar y reconstruir |
| 10 | Sueldo ≈ ingreso / 12 | Mediana del cliente |

<!--
Mostrar ejemplo/reports/01_eda.md. El criterio de H1 pide ≥ 5 decisiones justificadas en el EDA de cada grupo.
Cada fila se convierte en código con pruebas en src/creditsight/data/.
-->

---

# 9 · Preprocesamiento: de decisiones a código

El notebook **solo orquesta**; la lógica vive en `src/creditsight/data/` con pruebas.

```text
raw  ──load_raw()──►  sin datos personales  ──clean()──►  datos limpios
                                                        ──split_by_customer()──► train / test
```

- 100.000 filas antes y después: **no se pierde ninguna fila**.
- Las decisiones se **verifican**: si algo no se cumple, el notebook falla.

<!--
Notebook 03. Mostrar la tabla de verificación (todo True) y mencionar pytest ejemplo/tests.
Por qué código y no celdas sueltas: la limpieza debe correr igual al entrenar, validar y predecir.
-->

---

# 10 · Lo que sigue vacío está bien

La limpieza **no inventa datos**: solo repara lo que se deduce con seguridad.

El resto se **imputa dentro del pipeline**, con estadísticas calculadas **solo con el entrenamiento**.

> Imputar antes de partir sería otra forma de fuga.

<!--
Notebook 03, sección "Lo que queda vacío". Conecta con lo visto en el curso previo sobre pipelines: el imputador se ajusta con train.
-->

---

<!-- _class: lead -->

# 11 · El momento central
## ¿Partimos por fila o por cliente?

Mismo modelo, mismos datos. **Solo cambia cómo se parte.**

<!--
Tomarse 5 minutos aquí. Pedir a la audiencia que predigan: ¿cuál de las dos particiones dará mejor métrica?
-->

---

# 12 · El experimento de la fuga

| Partición | Clientes en ambos lados | F1 macro | Costo esperado |
|---|---|---|---|
| Por fila (mal) | **10.449** | **0,734** | **0,65** |
| Por cliente (bien) | 0 | 0,695 | 0,73 |

Por fila el modelo **parece mejor**: ~4 puntos más de F1 y menos costo.

**Esa ventaja es falsa**: el modelo ya vio a los clientes de la prueba, con otros meses.

<!--
Cifras exactas del notebook 03 ejecutado: F1 0,734 vs 0,695; costo 0,65 vs 0,73; 10.449 clientes compartidos.
Es una fuga sin un solo error de código: el pipeline funciona, las métricas se ven bien y todo está mal.
Matiz honesto: con un modelo rápido y moderado la brecha es de unos 4 puntos; no la exageren.
-->

---

# 13 · La regla del curso

> **La partición respeta la unidad de análisis, y se verifica con una prueba automática, no a ojo.**

- En producción llegan clientes **nuevos**: el rendimiento real es el de la fila de abajo.
- `tests/test_split.py`: *ningún cliente aparece en dos particiones*.
- Partimos **una sola vez**: 10.000 clientes para entrenar y 2.500 de prueba, **cerrada hasta la etapa 7**.

**Para su caso:** ¿cuál es SU unidad de análisis? ¿Qué se repite en sus filas?

<!--
Pregunta de transferencia: cualquier dataset con entidades repetidas (pacientes, productos, tiendas, sensores) tiene el mismo riesgo.
Distribución del objetivo en train/test: Standard 0,532/0,529; Poor 0,291/0,286; Good 0,177/0,185.
-->

---

<!-- _class: lead -->

# 14 · Lo que se llevan

1. Un caso de negocio con **costo de equivocarse**.
2. Un EDA que termina en **decisiones escritas**.
3. Una limpieza **como código con pruebas**.
4. Una partición **por la unidad correcta**.

**Ahora, a su caso.** Entregable de hoy: ficha aprobada, EDA y preprocesamiento reproducible.

<!--
Cerrar y pasar al trabajo de grupos. Criterios de H1 en specs/.../contracts/etapas.md.
-->
