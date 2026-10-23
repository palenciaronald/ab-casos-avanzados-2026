---
marp: true
theme: default
paginate: true
header: "Casos Avanzados · Maestría en Ingeniería Analítica"
footer: "Fin de semana 2 · Demo 2: variables y torneo de modelos"
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Demo 2 · Variables como hipótesis y torneo de modelos
## CreditSight: etapas 4 y 5

**Fin de semana 2 · ≤ 20 minutos**

Notebooks `04_features` y `05_torneo` del ejemplo

<!--
Duración total: 20 min. Distribución sugerida: variables 8 min (diapositivas 2-6), costo y decisión 4 min (7-8),
torneo 6 min (9-13), cierre 2 min (14). Notebooks ya ejecutados; no se programa en vivo.
-->

---

# Dos ideas para llevarse

1. **Cada variable nueva es una hipótesis**: se mide contra el ruido de la validación, no se añade porque "suena bien".
2. **El torneo elige finalistas, no un campeón.** La prueba final dice qué tan bueno es el modelo.

Todo se compara con **la misma validación**: 5 pliegues, **por cliente**.

<!--
Recordar de la demo 1: la partición por cliente. Aquí la validación cruzada también va por cliente.
-->

---

# Tres ideas de variables

| Idea | Por qué podría ayudar |
|---|---|
| **Razones financieras** (deuda/ingreso, cuota/sueldo...) | 1.000 de deuda pesa distinto con 20.000 que con 150.000 de ingreso |
| **Historial del mes anterior** | En un panel, lo previo suele predecir lo actual |
| **`Credit_Mix`** | Muy asociada al objetivo en el EDA |

Regla: una idea entra **solo si mejora el costo por más que el ruido entre pliegues**.

<!--
Notebook 04, tabla inicial. El historial usa solo meses anteriores (nunca el propio mes ni futuros: eso sería fuga);
el primer mes de cada cliente queda vacío y hay una verificación en el notebook.
-->

---

# Ver diferencia ≠ mejorar el modelo

Mediana por clase de `debt_to_income`: **Poor 0,063 · Standard 0,022 · Good 0,012**.

La variable **separa las clases a simple vista**. ¿Sirve?

> Un árbol puede estar **reconstruyendo esa razón** con las columnas originales. La única forma de saberlo es **medir**.

<!--
Notebook 04, tabla de medianas por clase. Esta es la trampa clásica: el gráfico convence, el experimento no.
-->

---

# El experimento

Mismo modelo (LightGBM, parámetros fijos) · 5 pliegues por cliente · solo cambia el conjunto de variables.

| Variante | Costo | ± pliegues |
|---|---|---|
| base, sin `Credit_Mix` | 0,4955 | 0,0086 |
| **base, con `Credit_Mix` (referencia)** | **0,4894** | 0,0075 |
| + razones financieras | 0,4896 | 0,0069 |
| + historial del mes anterior | 0,4842 | 0,0081 |
| + razones + historial | 0,4834 | 0,0088 |

<!--
Cifras exactas de ejemplo/reports/04_features_tabla.csv. Pedir que lean primero la columna ± pliegues antes de mirar las diferencias.
-->

---

# Cómo leer la tabla: mejora / ruido

| Idea | Mejora de costo | Mejora / ruido |
|---|---|---|
| razones financieras | −0,0001 | **−0,02** |
| historial del mes anterior | +0,0052 | **0,64** |
| razones + historial | +0,0061 | 0,69 |

Una mejora **menor que ~1 vez el ruido** puede desaparecer con otra partición.

**Resultado negativo honesto:** las razones y el historial **no aportan** de forma convincente.

<!--
Notebook 04. No es un fracaso: dos de tres ideas razonables no sirvieron, y eso es información.
En una prueba aparte con regresión logística el resultado fue el mismo: las razones no aportan.
-->

---

# `Credit_Mix`: aporta, con una condición

- En **costo** la mejora es pequeña (0,4955 → 0,4894; 0,7 veces el ruido).
- En **calidad de probabilidades** (log loss) mejora de **0,6953 a 0,6686**, varias veces el ruido.

| Decisión | Motivo |
|---|---|
| Razones: **descartar** | Sin mejora medible |
| Historial: **descartar** | Marginal; complica la app |
| `Credit_Mix`: **conservar, con condición** | Solo válida si **se conoce al momento de decidir** |

<!--
La condición es un supuesto de negocio, no un resultado técnico. Si el dato llegara después de calificar, sería una fuga.
Queda escrito en la ficha del modelo y la app permite dejarlo como "no sé".
-->

---

# La lección de fondo

La mejora grande del proyecto vino de **entender y limpiar los datos** (etapas 2 y 3), no de inventar columnas.

Un modelo con **menos variables** es más fácil de explicar, desplegar y mantener.

> Pregunta para su caso: ¿qué idea de variable van a **medir** antes de incluirla?

<!--
Conexión con la demo 1. El código de las variables descartadas se conserva (documenta la prueba) pero el pipeline las deja apagadas.
-->

---

# El costo esperado y la regla de decisión

La matriz de costos de la etapa 1 se convierte en **la forma de decidir**:

- Opción A: elegir la **clase más probable**.
- Opción B: elegir la clase de **menor costo esperado**: $\arg\min_j \sum_i p_i \, C(i,j)$.

Con probabilidades útiles, B **reduce el costo de todos los modelos**.

<!--
Notebook 05, columna "costo (clase más probable)" frente a "costo". Ejemplo con LightGBM: 0,7722 eligiendo la clase más probable
frente a 0,4894 con la regla de menor costo; las cifras de cada modelo están en la diapositiva siguiente.
-->

---

# El torneo: cinco candidatos, la misma validación

| Modelo | Costo | ± | Costo (más probable) | Recall Poor | s/ajuste |
|---|---|---|---|---|---|
| **random forest** | **0,4820** | 0,0077 | 0,7869 | 0,8237 | 12 |
| lightgbm | 0,4894 | 0,0075 | 0,7722 | 0,8075 | 6 |
| xgboost | 0,4900 | 0,0080 | 0,7760 | 0,8072 | 11 |
| regresión logística | 0,5528 | 0,0139 | 0,9252 | 0,7743 | 4 |
| baseline (clase más frecuente) | 1,0494 | 0,0003 | 1,0494 | 0,0000 | 1 |

<!--
Cifras exactas de ejemplo/reports/05_torneo_tabla.csv. El baseline no mejora con la regla de decisión: no tiene probabilidades que explotar.
-->

---

# ¿La diferencia entre los mejores es real?

Todos se evaluaron **en los mismos pliegues**: comparamos de a pares.

| Mejor | Contra | Dif. media de costo | Gana en | Dif. / ruido |
|---|---|---|---|---|
| random forest | lightgbm | 0,0075 | **5 de 5** | 1,44 |
| random forest | xgboost | 0,0080 | **5 de 5** | 2,24 |
| lightgbm | xgboost | 0,0005 | 2 de 5 | **0,17** |

LightGBM y XGBoost **empatan**; random forest gana de forma **consistente**, aunque por poco.

<!--
Notebook 05, comparación pareada. Una diferencia que gana en todos los pliegues y es varias veces el ruido es consistente;
una que gana en 2 de 5 con ruido mayor que la diferencia es un empate práctico.
-->

---

# ¿Cuánto vale en dinero?

Con **100.000 decisiones al mes** (unidades relativas de costo):

| Modelo | Costo mensual | Extra vs. el mejor |
|---|---|---|
| random forest | 48.196 | 0 |
| lightgbm | 48.945 | 749 |
| xgboost | 48.997 | 801 |
| regresión logística | 55.285 | **7.089** |
| baseline | 104.938 | 56.741 |

La regresión logística es la **referencia interpretable**: ese es el **precio** de explicarla mejor. Decisión de **negocio**, no solo técnica.

<!--
Cifras del notebook 05 (tabla de dinero). Si el regulador exige un modelo explicable, esas 7.089 unidades mensuales son el costo de cumplirlo.
-->

---

# Advertencia sobre la métrica

Random forest logra el menor costo siendo el **más conservador**:

- **Mayor recall de `Poor`** (0,8237)
- **Menor F1 macro** (0,5002)

Para esta matriz de costos es lo correcto: prefiere marcar de más a un cliente riesgoso (error barato) que dejar pasar a uno riesgoso (error caro).

Pero implica **más casos para el analista**: un efecto que el costo no ve y que se mide en la validación.

<!--
Compare con lightgbm: F1 macro 0,5442 y recall de Poor 0,8075. La carga de revisión del analista se mide en el notebook 07.
-->

---

<!-- _class: lead -->

# Decisión del torneo

**Finalistas para optimizar: random forest y LightGBM.**

XGBoost queda fuera: empata con LightGBM y tarda más en ajustar.

> **El torneo elige finalistas, no un campeón definitivo.** La optimización puede cambiar el orden y solo la prueba final (etapa 7) dice qué tan bueno es el modelo.

**Para su caso:** ¿qué modelo es su baseline? ¿cuál es su métrica de negocio?

<!--
Cierre. Siguiente: notebook 06, optimización con seguimiento en MLflow (cada ensayo queda registrado).
-->
