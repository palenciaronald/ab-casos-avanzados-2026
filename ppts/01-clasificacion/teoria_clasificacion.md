---
marp: true
theme: default
paginate: true
header: "Casos Avanzados · Maestría en Ingeniería Analítica"
footer: "Tema 1 — Clasificación · basado en *ISL* caps. 2, 4 y 8"
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Clasificación
## Score de Riesgo Crediticio

**Fin de semana 1 · Viernes · Repaso conceptual (~1 h)**

*Basado en An Introduction to Statistical Learning (ISL)*
James, Witten, Hastie & Tibshirani — caps. 2, 4 y 8

---

# El caso de negocio

Una **entidad financiera** debe decidir a quién otorgar crédito.

- Cada solicitante trae variables **demográficas** (edad, empleo, vivienda) y
  **financieras** (cuentas, monto, duración).
- Buscamos una función $\hat{f}(X)$ que prediga la clase
  $Y \in \{\text{good}, \text{bad}\}$.

> **Valor:** decisiones de crédito basadas en evidencia, menor mora,
> criterios homogéneos entre analistas.

---

# Agenda (enfoque ISL)

1. Aprendizaje supervisado y el marco $Y = f(X) + \varepsilon$ — *ISL §2.1*
2. El **clasificador de Bayes** como ideal teórico — *ISL §2.2.3*
3. **Regresión logística** y log-odds — *ISL §4.3*
4. Métricas: matriz de confusión, ROC, AUC — *ISL §4.4.2*
5. **Árboles y Random Forest** — *ISL §8.1, §8.2*
6. Trade-off **sesgo–varianza** e interpretabilidad — *ISL §2.2*
7. Demo en vivo

---

# 1. El marco del aprendizaje estadístico

ISL §2.1 — asumimos que existe una relación

$$Y = f(X) + \varepsilon$$

- $f$ es la información sistemática que $X$ aporta sobre $Y$.
- Estimamos $\hat{f}$ para **predecir** (y en parte **inferir**).
- En **clasificación**, $Y$ es cualitativa: predecir la *categoría*.

> Distinguir **predicción** (¿acierta?) de **inferencia** (¿qué variables
> importan y cómo?) — ambas nos interesan en banca.

---

# 2. El clasificador de Bayes (ideal)

ISL §2.2.3 — el clasificador que **minimiza el error** asigna cada observación a
la clase más probable dado $X$:

$$\Pr(Y = j \mid X = x_0)$$

- Su tasa de error (**Bayes error rate**) es el mínimo teórico irreducible.
- **No es alcanzable** en la práctica: no conocemos la distribución real.
- Los métodos (logística, KNN, árboles) **estiman** esa probabilidad.

---

# 3. Regresión logística

ISL §4.3 — modela **la probabilidad** de la clase, no la clase directamente:

$$p(X) = \frac{e^{\beta_0 + \beta_1 X_1 + \dots + \beta_p X_p}}
{1 + e^{\beta_0 + \beta_1 X_1 + \dots + \beta_p X_p}}$$

Equivale a un modelo lineal en el **log-odds** (logit):

$$\log\!\left(\frac{p(X)}{1 - p(X)}\right) = \beta_0 + \beta_1 X_1 + \dots$$

Se ajusta por **máxima verosimilitud**.

---

# 3. Interpretar los coeficientes

- Un aumento unitario en $X_j$ cambia el **log-odds** en $\beta_j$.
- $e^{\beta_j}$ es el **odds ratio**: cuánto se multiplican las probabilidades
  relativas.
- El **signo** indica dirección del efecto sobre el riesgo.

> Esta interpretabilidad es la razón por la que la logística sigue siendo el
> *baseline* estándar en scoring crediticio.

---

# 4. Evaluación — la matriz de confusión

ISL §4.4.2 — con clases desbalanceadas el *accuracy* global engaña.

|              | Pred. good | Pred. bad |
|--------------|:----------:|:---------:|
| **Real good**|     TN     |    FP     |
| **Real bad** |   **FN**   |    TP     |

- **Sensibilidad (recall):** TP / (TP + FN) — % de malos pagadores detectados.
- **Especificidad:** TN / (TN + FP).
- El **Falso Negativo** (aprobar a quien no paga) es el error costoso.

---

# 4. Curva ROC y AUC

ISL §4.4.2 — la ROC traza **sensibilidad vs. (1 − especificidad)** al variar el
umbral de decisión.

- **AUC** (área bajo la curva) resume el desempeño en un número.
- AUC = 1 → perfecto; AUC = 0.5 → azar.
- Ventaja: **independiente del umbral** y del desbalance.

> Permite comparar modelos sin fijar todavía el punto de corte de negocio.

---

# 5. Árboles de decisión

ISL §8.1 — dividen el espacio de predictores en regiones mediante reglas
simples (*if–then*).

- **Interpretables** y visualizables.
- Capturan **interacciones** y no linealidades sin transformaciones.
- Pero un árbol único tiene **alta varianza** (sobreajusta).

$$\text{clasifica según la clase mayoritaria de cada región terminal}$$

---

# 5. Random Forest

ISL §8.2 — combina **muchos árboles** para reducir la varianza.

- **Bagging:** entrena cada árbol en una muestra bootstrap.
- En cada división considera solo un **subconjunto aleatorio** de predictores
  → decorrelaciona los árboles.
- Predicción = **voto mayoritario** de los árboles.
- Da **importancia de variables** (reducción de impureza / Gini).

> Más preciso que un árbol; menos interpretable → ver importancia de variables.

---

# 6. Desbalance de clases

70% *good* vs. 30% *bad*: el modelo tiende a la clase mayoritaria.

- `class_weight="balanced"` — pondera más los errores en la clase rara.
- Re-muestreo (over/under-sampling, SMOTE).
- **Ajustar el umbral** de probabilidad según el costo de negocio
  (relación con la ROC).

> En banca, subir la sensibilidad a *bad* suele valer más que el accuracy.

---

# 6. Sesgo, varianza e interpretabilidad

ISL §2.2 — dos ejes centrales del libro:

- **Trade-off sesgo–varianza:** modelos flexibles ↓ sesgo pero ↑ varianza.
- **Flexibilidad vs. interpretabilidad:** logística (interpretable) ↔
  Random Forest (flexible, "caja negra").

> La elección **depende del objetivo**: ¿explicar la decisión de crédito o
> maximizar el acierto?

---

# Trampas comunes ⚠️

- Reportar **solo accuracy** en datos desbalanceados.
- **Data leakage:** escalar/imputar usando información del test
  → todo dentro de un `Pipeline`.
- No **estratificar** el train/test split.
- Interpretar coeficientes como **causalidad**.

---

# Ahora: a la demo 🚀

Recorreremos el pipeline completo en el notebook del viernes:

**Carga → EDA → Preprocesamiento → Logística + Random Forest →
Matriz de confusión, ROC-AUC → Importancia de variables → Conclusión**

- **Hoy (demo):** German Credit Data — 1.000 clientes, target `Risk` (binaria).
- **Sábado (tú):** Credit Score Classification — 100.000 filas, 3 clases,
  datos "sucios".

---

<!-- _class: lead -->

# ¿Preguntas?

**Lecturas ISL recomendadas:**
cap. 2 (aprendizaje estadístico), cap. 4 (clasificación, logística),
cap. 8 (árboles, bagging, random forest).
