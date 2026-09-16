---
marp: true
theme: default
paginate: true
header: "Casos Avanzados · Maestría en Ingeniería Analítica"
footer: "Tema 3 — Regresión · basado en *ISL* caps. 3 y 6"
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Regresión
## Modelo de Liquidez

**Fin de semana 2 · Viernes · Repaso conceptual (~1 h)**

*Basado en An Introduction to Statistical Learning (ISL)*
Cap. 3 — Linear Regression · Cap. 6 — Model Selection & Regularization

---

# El caso de negocio

Un analista financiero quiere **estimar la liquidez** de una empresa
(el **Current Ratio**) a partir de otros indicadores.

- La variable respuesta $Y$ es **continua** → problema de **regresión**.
- Predictores $X$: rentabilidad, márgenes, endeudamiento, flujos de caja.

> Objetivo doble: **predecir** la liquidez y **entender qué indicadores** la
> explican (inferencia).

---

# Agenda (enfoque ISL)

1. El modelo lineal — *ISL §3.1–3.2*
2. Estimación por **mínimos cuadrados** y su interpretación
3. Métricas: RSE, $R^2$ — *ISL §3.1.3*
4. **Supuestos** y diagnóstico de residuos — *ISL §3.3.3*
5. **Multicolinealidad** y VIF — *ISL §3.3.3*
6. **Regularización:** Ridge y Lasso — *ISL §6.2*
7. Trade-off sesgo–varianza y selección — *ISL §6.1*
8. Demo en vivo

---

# 1. El modelo lineal

ISL §3.1 — asumimos una relación aproximadamente lineal:

$$Y = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + \dots + \beta_p X_p + \varepsilon$$

- $\beta_j$: efecto **promedio** sobre $Y$ de subir $X_j$ una unidad,
  **manteniendo lo demás constante**.
- $\varepsilon$: error irreducible.

> Simple, interpretable y sorprendentemente competitivo — el punto de partida
> de ISL.

---

# 2. Mínimos cuadrados (OLS)

ISL §3.1.1 — elegimos los coeficientes que **minimizan la suma de residuos al
cuadrado**:

$$\text{RSS} = \sum_{i=1}^{n} \left(y_i - \hat{y}_i\right)^2$$

- $\hat{y}_i = \hat{\beta}_0 + \hat{\beta}_1 x_{i1} + \dots$
- Solución cerrada; cada $\hat{\beta}_j$ tiene un **error estándar** para
  contrastes de hipótesis ($H_0: \beta_j = 0$).

---

# 3. ¿Qué tan bueno es el ajuste?

ISL §3.1.3 — dos medidas clave:

- **RSE** (Residual Standard Error): magnitud típica del error, en unidades de
  $Y$.
- **$R^2$**: proporción de la varianza de $Y$ explicada por el modelo,
  $R^2 \in [0, 1]$.

$$R^2 = 1 - \frac{\text{RSS}}{\text{TSS}}$$

También usaremos **MAE** y **RMSE** para evaluar en el conjunto de prueba.

---

# 4. Los supuestos del modelo lineal

ISL §3.3.3 — para que la inferencia sea válida:

1. **Linealidad** de la relación.
2. **Homocedasticidad:** varianza constante del error.
3. **Normalidad** aproximada de los residuos.
4. **Independencia** de los errores.
5. Ausencia de **multicolinealidad** severa.

> Violarlos no impide predecir, pero **invalida la interpretación** de los
> coeficientes.

---

# 4. Diagnóstico de residuos

ISL §3.3.3 — se revisa gráficamente:

- **Residuos vs. predichos:** deben ser una nube sin patrón alrededor de 0
  (patrón → no linealidad o heterocedasticidad).
- **QQ-plot:** los puntos sobre la diagonal → residuos ~ normales.

> El diagnóstico es tan importante como el $R^2$: un $R^2$ alto con residuos
> con patrón es sospechoso.

---

# 5. Multicolinealidad

ISL §3.3.3 — cuando dos o más predictores están muy correlacionados entre sí.

- Infla la varianza de los $\hat{\beta}_j$ → coeficientes **inestables** y
  difíciles de interpretar.
- Frecuente con **ratios financieros** (se mueven juntos).

Se mide con el **VIF (Variance Inflation Factor):**

$$\text{VIF}(\hat{\beta}_j) = \frac{1}{1 - R^2_{X_j \mid X_{-j}}}$$

> Regla práctica: **VIF > 5–10** indica un problema.

---

# 5. ⚠️ Fuga de información

Un peligro relacionado pero distinto: incluir como predictor una variable que es
**una reformulación del target**.

- Ej.: predecir *Current Ratio* usando *Quick Ratio* o
  *Cash/Current Liability*.
- El $R^2$ se dispara artificialmente hacia 1… pero el modelo **no aprende
  nada útil**: solo ve una copia de $Y$.

> Regla: **excluir** variables casi-idénticas al target. (Punto clave del
> ejercicio del sábado.)

---

# 6. Regularización — ¿por qué?

ISL §6.2 — con muchos predictores (y colinealidad), OLS **sobreajusta**.

Idea: penalizar el tamaño de los coeficientes para **reducir varianza** a cambio
de un poco de sesgo (trade-off sesgo–varianza, §6.1).

- Encoge los $\hat{\beta}_j$ hacia 0.
- Mejora la **generalización** en test.

---

# 6. Ridge vs. Lasso

ISL §6.2 — dos penalizaciones distintas:

**Ridge** (penalización $\ell_2$):
$$\min \; \text{RSS} + \lambda \sum_{j=1}^{p} \beta_j^2$$

**Lasso** (penalización $\ell_1$):
$$\min \; \text{RSS} + \lambda \sum_{j=1}^{p} |\beta_j|$$

- Ridge encoge pero **mantiene** todas las variables.
- Lasso puede llevar coeficientes a **exactamente 0** → **selección de
  variables**.

---

# 6. Elegir $\lambda$

ISL §6.2 — el hiperparámetro $\lambda$ controla la fuerza de la penalización:

- $\lambda = 0$ → OLS (sin regularizar).
- $\lambda \to \infty$ → todos los coeficientes hacia 0.
- Se elige por **validación cruzada**.

> Importante: **escalar** los predictores antes de Ridge/Lasso — la
> penalización depende de la escala.

---

# 7. Sesgo–varianza y selección de modelo

ISL §6.1 — con muchos predictores conviene **reducir** el modelo:

- **Selección de subconjuntos** (forward/backward).
- **Regularización** (Ridge/Lasso).
- Preferir el modelo más **parsimonioso** que generalice bien.

> Un modelo más simple es más **robusto** y más fácil de explicar al negocio.

---

# Trampas comunes ⚠️

- Reportar $R^2$ sin revisar los **residuos**.
- Dejar variables que son una **copia del target** (fuga → $R^2 \approx 1$).
- No **escalar** antes de Ridge/Lasso.
- Ignorar el **VIF** con muchos ratios correlacionados.
- Interpretar coeficientes con multicolinealidad severa.

---

# Ahora: a la demo 🚀

En el notebook del viernes:

**Carga → EDA y correlaciones → Lineal vs. Ridge/Lasso →
MAE / RMSE / $R^2$ → Residuos + VIF → Interpretación de coeficientes**

- **Hoy (demo):** Financial Statements — 161 empresas reconocibles.
- **Sábado (tú):** Taiwan Bankruptcy — 6.819 empresas, 95 ratios;
  excluir variables casi-duplicadas del target y domar la colinealidad.

---

<!-- _class: lead -->

# ¿Preguntas?

**Lecturas ISL recomendadas:**
cap. 3 — Linear Regression (§3.1–3.3, VIF en §3.3.3),
cap. 6 — Linear Model Selection & Regularization (§6.1–6.2, Ridge/Lasso).
