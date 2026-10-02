---
marp: true
theme: default
paginate: true
header: "Casos Avanzados · Maestría en Ingeniería Analítica"
footer: "Tema 3 — Regresión · clase teórica (~2 h) · basado en *ISL* caps. 3, 6 y 8"
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Regresión
## Una investigación: ¿qué modelo predice mejor la liquidez?

**Fin de semana 3 · Viernes · Clase teórica (~2 h)**

*Basado en An Introduction to Statistical Learning (ISL)*
Cap. 3 — Linear Regression · Cap. 6 — Regularization · Cap. 8 — Tree-Based Methods

---

# El caso de negocio

Un analista financiero quiere **estimar la liquidez** de una empresa
(el **Current Ratio**) a partir de otros indicadores.

- La variable respuesta $Y$ es **continua** → problema de **regresión**.
- Predictores $X$: rentabilidad, márgenes, endeudamiento, flujos de caja.

> Objetivo doble: **predecir** la liquidez y **entender qué indicadores** la
> explican (inferencia).

---

# Clasificación vs. regresión — el mismo problema, distinto tipo de $Y$

En el Tema 1 predecíamos una **categoría** (`good`/`bad`, `Poor`/`Standard`/`Good`).
Hoy predecimos un **número continuo** (el Current Ratio puede ser 0.88, 1.35,
2.4…).

- El *aprendizaje supervisado* es el mismo marco: hay un target $Y$ conocido
  en el train, y aprendemos una función $f$ que lo aproxima a partir de $X$.
- Lo que cambia es **cómo medimos el error** y, como consecuencia, **qué
  algoritmos y métricas aplican**.
- La buena noticia: **casi todos los algoritmos de clasificación que ya
  viste tienen una versión de regresión** — árboles, Random Forest,
  gradient boosting — cambia la función de pérdida, no la idea del algoritmo.

---

# La clase de hoy es una investigación, no un catálogo

En vez de una lista de "aquí hay 6 algoritmos", vamos a **construir un
modelo en vivo**, con datos reales de 137 empresas, y dejar que los
resultados guíen las decisiones — exactamente como pasa en un proyecto real:

1. Probamos lo obvio (regresión lineal).
2. Diagnosticamos por qué funciona peor de lo esperado.
3. Intentamos arreglarlo dentro de la familia lineal (regularización).
4. Vemos que **no alcanza**, y descubrimos por qué.
5. Cambiamos de familia de modelo (árboles) — y el resultado da un salto.
6. Pagamos el costo de ese salto: perdemos interpretabilidad directa, y
   aprendemos a recuperarla.

Todos los números que van a aparecer hoy son **reales**, del mismo dataset
que van a ver ejecutado en la demo.

---

<!-- _class: lead -->
# Acto 1
## Antes de 12 variables, un ejemplo con 1

---

# Empecemos simple: ROA vs. Current Ratio

Antes de meter las 12 variables del modelo completo, miremos **una sola**
relación real: rentabilidad sobre activos (ROA) vs. liquidez.

**Pregunta:** ¿una línea recta describe bien esta relación?

---

# ¿Una línea recta alcanza?

![width:620px center](img/toy_linea_vs_tendencia.png)

*Datos reales (137 empresas). La línea roja es el mejor ajuste lineal
posible. La línea oscura es la tendencia real suavizada: sube, llega a un
máximo alrededor de ROA≈12, y luego **baja**. Una línea recta no puede
hacer eso — por diseño, solo sabe subir o bajar, nunca las dos cosas.*

---

# Guardemos esta pista

- Con **una sola variable**, ya vemos que la relación real **no es
  lineal** — tiene forma de joroba, no de línea.
- Con **12 variables** relacionándose entre sí de formas parecidas, es
  razonable sospechar que el problema se mantiene o empeora.
- Vamos a construir el modelo lineal completo de todas formas — es el punto
  de partida estándar, y **necesitamos verlo fallar con números reales**
  para entender exactamente qué falla y por qué.

---

# Agenda de hoy

**Acto 2 — El modelo lineal completo**: ajuste, métricas, primer resultado real.
**Acto 3 — El diagnóstico**: supuestos, residuos, VIF, y el marco de
sesgo vs. varianza.
**Acto 4 — El intento de arreglo**: regularización (Ridge/Lasso) — ¿ayuda?
**Acto 5 — El giro**: árboles, Random Forest, XGBoost.
**Acto 6 — El costo del giro**: coeficientes vs. importancia de variables,
y cómo recuperar interpretabilidad con un *Partial Dependence Plot*.

---

<!-- _class: lead -->
# Acto 2
## El modelo lineal completo

---

# 1. El modelo lineal

ISL §3.1 — asumimos una relación aproximadamente lineal:

$$Y = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + \dots + \beta_p X_p + \varepsilon$$

- $\beta_j$: efecto **promedio** sobre $Y$ de subir $X_j$ una unidad,
  **manteniendo lo demás constante**.
- $\varepsilon$: error irreducible.

> Simple, interpretable y sorprendentemente competitivo en muchos problemas
> — el punto de partida de ISL. Hoy vamos a ver un caso donde **no** lo es.

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

También usaremos **MAE**, **RMSE** y **MAPE** para evaluar en el conjunto de
prueba — y para comparar de forma justa contra los modelos no lineales.

---

# Las métricas de regresión, en una tabla

| Métrica | Qué mide | Ventaja | Cuidado con |
|---|---|---|---|
| **MAE** | Error absoluto promedio | Fácil de interpretar, robusta a outliers | Pesa todos los errores igual |
| **RMSE** | Raíz del error cuadrático promedio | Penaliza más los errores **grandes** | Sensible a outliers |
| **R²** | % de varianza explicada | Comparable entre problemas, intuitivo | No dice nada sobre la magnitud del error |
| **MAPE** | Error porcentual promedio | Interpretable en % — ideal para negocio | Explota si $Y$ tiene valores cerca de 0 |

> RMSE y MAE casi siempre se reportan juntas (si RMSE ≫ MAE, hay errores
> grandes puntuales). MAPE es la más fácil de explicarle a negocio — y
> aquí es segura porque el Current Ratio nunca es cercano a 0.

---

# Intento 1: el modelo lineal completo

Ajustamos con las **12 variables** financieras (Revenue, EBITDA, ROA, ROE,
Debt/Equity, etc.) sobre 137 empresas (102 en train, 35 en test).

| | R² en train | R² en test |
|---|---|---|
| **Lineal** | **0.43** | **0.05** |

- En **train**, el modelo explica un 43% de la varianza — no es
  espectacular, pero es razonable.
- En **test**, cae a **5%** — prácticamente no generaliza. Es casi lo mismo
  que predecir siempre el promedio.

> Hay una brecha enorme entre train y test (0.43 → 0.05). Eso **no es
> normal**, y es la primera pista real que vamos a investigar.

---

<!-- _class: lead -->
# Acto 3
## El diagnóstico

---

# 4. Los supuestos del modelo lineal

ISL §3.3.3 — para que la inferencia sea válida:

1. **Linealidad** de la relación.
2. **Homocedasticidad:** varianza constante del error.
3. **Normalidad** aproximada de los residuos.
4. **Independencia** de los errores.
5. Ausencia de **multicolinealidad** severa.

> Violarlos no impide predecir, pero **invalida la interpretación** de los
> coeficientes — y, como vamos a ver, puede estar detrás de la brecha
> train/test que acabamos de encontrar.

---

# 4. Diagnóstico de residuos

ISL §3.3.3 — se revisa gráficamente:

- **Residuos vs. predichos:** deben ser una nube sin patrón alrededor de 0
  (patrón → no linealidad o heterocedasticidad).
- **QQ-plot:** los puntos sobre la diagonal → residuos ~ normales.

> El diagnóstico es tan importante como el $R^2$: un $R^2$ alto con residuos
> con patrón es sospechoso — y un $R^2$ bajo con residuos con patrón
> confirma que algo estructural está mal, no solo ruido.

---

# 5. Multicolinealidad — sospechoso #1

ISL §3.3.3 — cuando dos o más predictores están muy correlacionados entre sí.

- Infla la **varianza** de los $\hat{\beta}_j$ → coeficientes **inestables**:
  cambian mucho si cambian ligeramente los datos de entrenamiento.
- Un modelo con coeficientes inestables **ajusta bien el train** (encuentra
  *algún* balance de coeficientes que funciona ahí) pero **generaliza mal**
  — exactamente el patrón que acabamos de ver.
- Frecuente con **ratios financieros** (se mueven juntos: más ingresos,
  más utilidad, más EBITDA…).

Se mide con el **VIF (Variance Inflation Factor):**

$$\text{VIF}(\hat{\beta}_j) = \frac{1}{1 - R^2_{X_j \mid X_{-j}}}$$

> Regla práctica: **VIF > 5–10** indica un problema.

---

# El VIF, con datos reales

| Variable | VIF |
|---|---|
| EBITDA | **30.1** |
| Net Income | **24.2** |
| Gross Profit | **20.6** |
| Revenue | **15.3** |
| Net Profit Margin | 5.0 |
| Cash Flow from Operating | 4.5 |
| ROA | 4.1 |
| Number of Employees | 4.1 |
| Share Holder Equity | 3.6 |
| Debt/Equity Ratio | 2.5 |
| ROE | 1.8 |
| ROI | 1.1 |

**Confirmado:** 4 variables con VIF muy por encima de 10. `EBITDA`, `Net
Income`, `Gross Profit` y `Revenue` son, en el fondo, **la misma señal**
(tamaño/rentabilidad de la empresa) medida 4 veces.

---

# 5. ⚠️ Fuga de información (un peligro relacionado, pero distinto)

Incluir como predictor una variable que es **una reformulación del target**.

- Ej.: predecir *Current Ratio* usando *Quick Ratio* o
  *Cash/Current Liability*.
- El $R^2$ se dispara artificialmente hacia 1… pero el modelo **no aprende
  nada útil**: solo ve una copia de $Y$.

> No es nuestro problema hoy (ya lo evitamos), pero **sí** es el punto
> clave del ejercicio del sábado con el dataset de Taiwan.

---

# Dos sospechosos: sesgo y varianza

Toda la brecha train/test que estamos investigando se explica con **uno de
dos problemas** (o ambos):

- **Alto sesgo (underfitting):** el modelo es **demasiado simple** para la
  relación real — ni siquiera en train le va bien.
- **Alta varianza (overfitting):** el modelo es **demasiado sensible** a los
  datos de entrenamiento específicos — le va muy bien en train, pero no
  generaliza porque memorizó ruido en vez de señal.

---

# El diagnóstico, ilustrado

![width:560px center](img/sesgo_varianza_esquema.png)

*A la izquierda, el modelo es tan simple que ni el train le sale bien (alto
sesgo). A la derecha, el modelo es tan flexible que memoriza el train pero
falla en test (alta varianza). El punto óptimo minimiza el error en test,
no en train.*

---

# ¿Qué dice nuestro caso?

| | R² train | R² test | Brecha |
|---|---|---|---|
| **Lineal** | 0.43 | 0.05 | **0.37** |

- Train **no** es bajo (0.43) → **no** parece un problema de sesgo puro.
- La brecha es enorme (0.37) → **sí** parece alta varianza.
- Y ya tenemos al sospechoso: **multicolinealidad severa** (VIF hasta 30)
  infla la varianza de los coeficientes en una muestra de solo 102 filas.

> **Hipótesis de trabajo:** si el problema es varianza por
> multicolinealidad, la **regularización** (que existe exactamente para
> esto) debería ayudar bastante. Vamos a probarlo.

---

<!-- _class: lead -->
# Acto 4
## El intento de arreglo: regularización

---

# 6. Regularización — ¿por qué?

ISL §6.2 — con muchos predictores correlacionados, OLS produce coeficientes
de **alta varianza**.

Idea: penalizar el tamaño de los coeficientes para **reducir varianza** a
cambio de un poco de sesgo (trade-off sesgo–varianza).

- Encoge los $\hat{\beta}_j$ hacia 0.
- Coeficientes más chicos y estables → menos sensibles al ruido del train
  → mejor generalización esperada.

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

# Resultado real — ¿ayudó?

| | R² train | R² test | Brecha |
|---|---|---|---|
| Lineal | 0.43 | 0.05 | 0.37 |
| Ridge | 0.42 | **0.06** | 0.36 |
| Lasso | 0.42 | **0.07** | 0.35 |

- La brecha se redujo… **casi nada**. R² en test pasó de 0.05 a 0.07.
- La regularización sí hizo lo que promete (coeficientes más chicos, un
  poco más estables) — pero el techo del modelo **casi no se movió**.

> **La hipótesis de "solo es varianza" era incompleta.** Regularizar reduce
> varianza, pero no puede arreglar un problema de **forma equivocada** —
> y recordemos el Acto 1: la relación real (ROA) tenía forma de joroba, no
> de línea. Eso es **sesgo estructural**, y ningún $\lambda$ lo arregla.

---

<!-- _class: lead -->
# Acto 5
## El giro: modelos no lineales

---

# Cuando lo lineal no alcanza

La regresión lineal asume que el efecto de cada $X_j$ sobre $Y$ es
**constante** (no cambia según el valor de otras variables) y **aditivo**
(los efectos se suman). Vimos en el Acto 1 que, al menos para ROA, **eso ya
es falso** con una sola variable.

Necesitamos una familia de modelos que **no** asuma eso.

---

# 7. Árbol de decisión para regresión

ISL §8.1 — en vez de una ecuación, un árbol **parte el espacio de
predictores en regiones** y predice el **promedio de $Y$** dentro de cada
región.

- Cada split busca la pregunta (`¿ROA > 5?`) que **más reduce el error**
  (RSS) dentro de los dos grupos resultantes.
- Se repite recursivamente, creando regiones cada vez más pequeñas y
  homogéneas.
- Captura no linealidades e interacciones **automáticamente** — sin que
  nosotros tengamos que especificar la forma de la curva.

$$\hat{y} = \text{promedio de } y_i \text{ en la región que contiene a } x$$

---

# Un árbol individual, con datos reales

![width:560px center](img/toy_arbol_sobreajuste.png)

*El árbol sigue la forma general de la tendencia (a diferencia de la línea
recta) — pero también **memoriza un solo punto atípico** a la derecha,
creando un salto que no representa un patrón real. Esto es varianza,
otra vez, con otro algoritmo.*

---

# Resultado real — un árbol

| | R² train | R² test | Brecha |
|---|---|---|---|
| Lineal | 0.43 | 0.05 | 0.37 |
| Ridge / Lasso | 0.42 | 0.06–0.07 | ~0.35 |
| **Árbol** | **0.89** | **0.46** | **0.43** |

- El test **mejora muchísimo** (0.07 → 0.46): capturar la no linealidad
  vale la pena — confirma que el sesgo estructural era el problema
  dominante.
- Pero la brecha train/test **sigue siendo grande** (0.43): un solo árbol
  tiene **alta varianza** — es sensible a los datos específicos de train
  (como vimos con el punto atípico de la imagen).

> Arreglamos el sesgo, pero heredamos un problema de varianza nuevo.

---

# 8. Random Forest — arreglando la varianza, otra vez

ISL §8.2 — la solución al sobreajuste de un solo árbol: **promediar muchos
árboles distintos**.

- Cada árbol se entrena sobre una **submuestra aleatoria** de filas
  (*bagging*) y considera solo un **subconjunto aleatorio de variables** en
  cada split.
- La predicción final es el **promedio** de todos los árboles.
- Un árbol individual memoriza *su* punto atípico; promediar cientos de
  árboles (cada uno con una muestra distinta) **cancela ese ruido**.

> Misma lógica de sesgo-varianza del Acto 3, aplicada con árboles en vez de
> con $\lambda$: reducimos varianza promediando, no penalizando.

---

# Resultado real — Random Forest

| | R² train | R² test | Brecha |
|---|---|---|---|
| Árbol | 0.89 | 0.46 | 0.43 |
| **Random Forest** | **0.94** | **0.72** | **0.22** |

La brecha se **reduce a la mitad** y el test **casi se duplica**. Promediar
árboles funcionó exactamente como predice la teoría.

---

# 9. Gradient Boosting — la idea

ISL §8.2 — en vez de promediar árboles **independientes** (Random Forest),
*boosting* los entrena **secuencialmente**: cada árbol nuevo corrige los
**errores del conjunto anterior**.

1. Empieza con una predicción simple (el promedio de $Y$).
2. Calcula los **residuos** (dónde se equivoca el modelo actual).
3. Entrena un árbol **pequeño** para predecir esos residuos.
4. Suma esa predicción (escalada por una tasa de aprendizaje) al modelo.
5. Repite muchas veces.

> Cada árbol es débil por sí solo, pero la **suma secuencial** de árboles
> que corrigen errores previos produce un modelo muy potente.

---

# 9. XGBoost

**XGBoost** (*eXtreme Gradient Boosting*) es la implementación de gradient
boosting más usada en la práctica para datos tabulares.

- Mismo principio que el boosting genérico, con **regularización
  incorporada** (evita que los árboles individuales crezcan demasiado).
- Hiperparámetros clave: `n_estimators`, `learning_rate`, `max_depth`.
- `learning_rate` bajo + más árboles suele generalizar mejor que
  `learning_rate` alto + pocos árboles — el trade-off sesgo-varianza, otra vez.

> `HistGradientBoostingRegressor` (ya en scikit-learn) es una alternativa
> sin instalar nada adicional, con una idea muy similar.

---

# El resultado completo — las 6 filas

| Modelo | R² train | R² test | Brecha |
|---|---|---|---|
| Lineal | 0.43 | 0.05 | 0.37 |
| Ridge | 0.42 | 0.06 | 0.36 |
| Lasso | 0.42 | 0.07 | 0.35 |
| Árbol | 0.89 | 0.46 | 0.43 |
| Random Forest | 0.94 | 0.72 | 0.22 |
| **XGBoost** | **1.00** | **0.76** | 0.24 |

**XGBoost gana**, con el mejor test (0.76) — a pesar de tener el ajuste a
train casi perfecto (1.00). La brecha por sí sola no es lo que importa: lo
que importa es **cuánto generaliza**, y XGBoost generaliza mejor que todo
lo demás a pesar de memorizar el train casi a la perfección.

---

# Lineal vs. árboles — la tabla que resume todo

| | Modelos lineales (Lineal/Ridge/Lasso) | Árboles (RF/XGBoost) |
|---|---|---|
| Captura no linealidad | No (por diseño) | Sí, automáticamente |
| Necesita escalar | Sí (Ridge/Lasso) | No |
| Sufre por multicolinealidad | Sí (VIF, coeficientes inestables) | Mucho menos |
| Interpretación | Coeficiente = efecto directo | Importancia = "cuánto usa" la variable, no dirección |
| Con pocos datos | Un solo árbol sobreajusta mucho | Ensambles (RF/XGBoost) compensan promediando |
| Con muchos datos | No mejora tanto | Suele **ganar por mucho** |

---

<!-- _class: lead -->
# Acto 6
## El costo del giro: interpretabilidad

---

# 10. Interpretar: coeficientes vs. importancia de variables

- **Coeficiente lineal**: dirección (signo) y magnitud del efecto,
  manteniendo lo demás constante. Directamente interpretable — *si* el
  modelo es confiable (residuos ok, VIF bajo). El nuestro no cumplía eso.
- **Importancia de variables** (árboles): cuánto **reduce el error** una
  variable al usarse en los splits, sumado sobre todos los árboles. No dice
  la dirección del efecto, solo cuánto "pesa".

> Cuando una variable es importante en **ambas** familias, es una señal
> robusta. Cuando solo aparece en los árboles, sospecha de una relación no
> lineal o una interacción que el modelo lineal no puede ver.

---

# El caso de `Number of Employees`

En XGBoost, `Number of Employees` es la variable **más importante** — pero
en el modelo lineal tenía un coeficiente chico y una correlación simple de
apenas -0.19. ¿Contradicción, o exactamente lo que esperaríamos después de
todo lo que vimos hoy?

**Herramienta para responder esto: el *Partial Dependence Plot* (PDP)** —
grafica cómo cambia la predicción del modelo al mover **una variable**,
promediando sobre todas las demás. Es el equivalente, para un modelo de
árboles, de "leer un coeficiente".

---

# El PDP, con el modelo real de hoy

![width:560px center](img/pdp_xgboost_employees.png)

*Exactamente el patrón que sospechábamos: un **efecto umbral**. Para
empresas muy pequeñas, XGBoost predice liquidez alta; ese efecto cae
fuerte y se estabiliza una vez la empresa supera cierto tamaño. Una línea
recta no puede representar esta forma — por eso el coeficiente lineal de
esta variable era casi irrelevante, mientras que para XGBoost es la más
importante de todas.*

---

# Cerrando el círculo

- **Acto 1** mostró, con una variable, que la relación no era lineal.
- **Acto 6** lo confirma, con la variable más importante del mejor modelo:
  otra vez, un efecto no lineal (esta vez un umbral, no una joroba) que el
  modelo lineal no podía ver.
- La historia completa: el modelo lineal fallaba por **dos razones a la
  vez** — varianza por multicolinealidad (parcialmente arreglable con
  regularización) y **sesgo estructural** por forma incorrecta (solo
  arreglable cambiando de familia de modelo).

---

# Trampas comunes ⚠️

- Reportar $R^2$ sin revisar los **residuos** ni el **train vs. test**.
- Dejar variables que son una **copia del target** (fuga → $R^2 \approx 1$).
- No **escalar** antes de Ridge/Lasso.
- Ignorar el **VIF** con muchos ratios correlacionados.
- Asumir que la brecha train/test siempre significa lo mismo — a veces es
  varianza, a veces esconde también un problema de sesgo (como hoy).
- Quedarse solo con modelos lineales **sin probar alternativas no
  lineales** — la diferencia puede ser enorme.
- Usar árboles/XGBoost con **muy pocos datos** y esperar que generalicen
  igual de bien que con datasets grandes.
- Comparar RMSE de una familia contra R² de otra en vez de las mismas
  métricas para todos los modelos.
- Leer un PDP como si las variables fueran independientes — con predictores
  muy correlacionados (como los nuestros, recuerda el VIF), el PDP puede
  mostrar combinaciones de valores que casi no existen en los datos reales.

---

# Ahora: a la demo 🚀

En el notebook del viernes, vas a ver **exactamente esta investigación**,
ejecutada en vivo, celda por celda:

**Carga → EDA → Modelos lineales → Diagnóstico (residuos, VIF) →
Regularización → Modelos no lineales → Evaluación comparativa (train/test,
MAE, RMSE, R², MAPE) → Coeficientes vs. importancia de variables**

- **Hoy (demo):** Financial Statements — 161 empresas. Ya conoces el final:
  los árboles ganan por mucho.
- **Sábado (tú):** Taiwan Bankruptcy — 6.819 empresas, 95 ratios. Pregunta
  abierta: con 36× más datos, ¿la ventaja de los árboles se mantiene, crece,
  o se reduce? Vas a excluir variables casi-duplicadas del target y domar
  la colinealidad tú mismo.

---

<!-- _class: lead -->

# ¿Preguntas?

**Lecturas ISL recomendadas:**
cap. 3 — Linear Regression (§3.1–3.3, VIF en §3.3.3),
cap. 6 — Linear Model Selection & Regularization (§6.1–6.2, Ridge/Lasso),
cap. 8 — Tree-Based Methods (§8.1 árboles, §8.2 bagging/random forests/boosting).
