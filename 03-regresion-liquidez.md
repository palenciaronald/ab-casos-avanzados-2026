# Tema 3: Regresión — Modelo de Liquidez
## Fin de semana 3 (2–3 oct)

## 1. Caso de negocio

Un analista financiero quiere estimar el nivel de liquidez de una empresa (medido como un ratio continuo, ej. Current Ratio) a partir de otros indicadores financieros disponibles en sus estados financieros, para anticipar riesgos de liquidez sin depender únicamente del cálculo directo. El estudiante construye un modelo de regresión donde la variable objetivo es un ratio de liquidez y las features son otros ratios/indicadores financieros.

**Nota:** a diferencia de los otros temas, aquí no hay un dataset "de liquidez" con ese nombre — se usa el `current_ratio` / `Current Ratio` que ya viene calculado en ambas bases como variable objetivo (`y`), y el resto de columnas financieras como predictoras (`X`).

**Variables a excluir de las features en el dataset del sábado por ser casi-duplicadas del target** (fuga de información / colinealidad extrema): `Acid Test` (Quick Ratio), `Quick Assets/Current Liability`, `Cash/Current Liability`, `Current Liability to Current Assets`, `Current Liability to Assets`. Todas estas miden esencialmente lo mismo que el Current Ratio y dejarlas como predictoras haría el modelo trivial (R² artificialmente cercano a 1). Esto es justo un buen punto de teoría para el viernes: "cuidado con las variables que son una reformulación del target."

## 2. Teoría (viernes, ~2 h dedicadas)

Regresión es el aprendizaje supervisado para **variables continuas** — el
paralelo de clasificación. La teoría cubre **toda la familia de algoritmos**
usados para ese problema, no solo el lineal:

- Regresión lineal: supuestos (linealidad, homocedasticidad, normalidad de residuos, no multicolinealidad)
- Métricas de regresión: MAE, RMSE, R², MAPE — cuándo usar cada una
- Diagnóstico de residuos (gráfico de residuos vs. predichos, QQ-plot) — propio de la familia lineal
- Multicolinealidad: VIF (Variance Inflation Factor) y por qué importa con muchos ratios financieros correlacionados entre sí
- Regularización: Ridge y Lasso, y el trade-off sesgo-varianza
- **Modelos no lineales**: Árbol de decisión, Random Forest y **XGBoost** (gradient boosting) — la idea de cada uno, y por qué no necesitan escalado ni sufren de multicolinealidad de la misma forma que los lineales
- Interpretación: coeficientes (familia lineal) vs. importancia de variables (familia de árboles) — cuándo coinciden y cuándo no, y qué significa cuando no coinciden
- Trade-off explícito: precisión (los árboles suelen ganar) vs. interpretabilidad (los lineales son más fáciles de explicar)

## 3. Datasets

- **Viernes (demo del instructor):** [Financial Statements of Major Companies (2009-2023)](https://www.kaggle.com/datasets/rish59/financial-statements-of-major-companies2009-2023) — 161 filas (panel de empresas grandes conocidas, ej. Apple, Microsoft, a lo largo de varios años), con la columna **`current_ratio`** ya calculada, más `debt_equity_ratio`, `roe`, `roa`, `roi`, `net_profit_margin`, `revenue`, `ebitda`, `share_holder_equity`, entre otras. Dataset pequeño, limpio y con empresas reconocibles — ideal para una demo en vivo sin fricción.
- **Sábado (ejercicio del estudiante):** [Company Bankruptcy Prediction (Taiwan)](https://www.kaggle.com/datasets/fedesoriano/company-bankruptcy-prediction) — 6,819 filas, 95 ratios financieros, incluyendo la columna **`Current Ratio`** (confirmada, existe con ese nombre exacto) como target. Dataset mucho más grande y denso en variables, obligando al estudiante a hacer selección de variables y lidiar con colinealidad real.

**Descarga:**
```bash
kaggle datasets download -d rish59/financial-statements-of-major-companies2009-2023 -p ./data/03-regresion --unzip
kaggle datasets download -d fedesoriano/company-bankruptcy-prediction -p ./data/03-regresion --unzip
```

## 4. Estructura del notebook demo (viernes)

1. **Introducción** (Markdown) — planteamiento del caso y explicación de cómo se construye el target de liquidez
2. Carga de datos y exploración inicial
3. EDA: distribución del target, correlaciones entre ratios (heatmap)
4. Selección de variables predictoras y train/test split
5. Modelos lineales: Lineal (baseline) vs. Ridge/Lasso
6. Modelos no lineales: Árbol de decisión, Random Forest y **XGBoost**
7. Evaluación comparativa de los 6 modelos: MAE, RMSE, R², MAPE + diagnóstico de residuos del mejor lineal
8. Multicolinealidad: VIF (familia lineal)
9. Interpretación: coeficientes (lineal) vs. importancia de variables (árboles) — comparar qué cuenta cada familia
10. Conclusión de negocio: ¿qué indicadores debería monitorear el analista financiero, y qué modelo debería usar?

**Resultado real de la demo** (Financial Statements, n=137): los modelos lineales
apenas explican 5-7% de la varianza (R²), mientras que XGBoost explica ~76% —
evidencia de que la relación entre estos indicadores y la liquidez no es lineal.
Es el punto de teoría más fuerte del día: no asumir que lineal alcanza.

## 5. Estructura de la plantilla (sábado) — taller de ~4 h

A diferencia de la demo, **el estudiante hace el EDA completo** (obligatorio) y de él salen las decisiones de limpieza. Solo la carga de datos y la semilla vienen resueltas.

| # | Sección | Qué hace el estudiante |
|---|---|---|
| 2 | **EDA obligatorio** (2.1–2.9) | Calidad de datos; target (skew, p99); outliers del target y de los **predictores**; correlación **Pearson vs. Spearman**; pares casi duplicados; relación con `Bankrupt?`; detección de **fuga de información**; cuadro de hallazgos con decisiones |
| 3 | Preparación y split | Aplica las decisiones del EDA; experimento **sin vs. con `Winsorizer`** (se entrega la clase) |
| 4–5 | Baseline + lineales | `DummyRegressor`; Lineal, `RidgeCV`, `LassoCV` |
| 6 | No lineales | Árbol, Random Forest, XGBoost |
| 7 | Validación cruzada | 5-fold, media ± std del RMSE |
| 8 | Tuning | `RandomizedSearchCV` sobre XGBoost |
| 9 | Evaluación y errores | MAE/RMSE/R²/MAPE (MAPE solo con y>0), residuos, real vs. predicho, MAE por cuartil, top-10 errores |
| 10 | VIF | VIF completo + eliminación iterativa (VIF<10) y comparación de R² |
| 11 | Interpretación | Coeficientes, importancia por impureza e importancia por **permutación** |
| 12 | Auditoría de fuga residual | Ablación por grupos de ratios relacionados |
| 13 | Conclusión | 8 preguntas abiertas |

**Hallazgos reales del dataset (verificados con la solución del instructor, semilla 1020304050):**
- Target: media 4.7e5 vs. mediana 0.011; máximo 2.75e9; ~1% de filas sobre el p99 (0.0748).
- ~21 de 94 predictores tienen valores > 1000 (la mayoría de ratios está en [0,1]). Sin tratarlos, la regresión lineal da **R² ≈ −4.8** (con otras semillas varía de −7 a −7e15); con `Winsorizer` (p1–p99) da **R² ≈ 0.91**.
- Fuga de información: *Quick Ratio*, *Quick Assets/Current Liability* y *Cash/Current Liability* tienen Pearson ≈ 0 con el target pero **Spearman 0.67–0.88** (los extremos ocultan la relación); *Current Liability to Current Assets* tiene Spearman = −1.0. Con ellas XGBoost llega a R² 0.9995; sin ellas, 0.983.
- Fuga residual: los ratios se calculan unos de otros; quitando grupos por nombre (Equity → Liabilit/Debt → Working/Current/Cash) el R² de XGBoost cae 0.983 → 0.974 → 0.936 → 0.692.
- Lineal ≈ 0.91 vs. XGBoost ≈ 0.98: a diferencia de la demo (n=137), con ~5.700 filas los lineales **sí funcionan** una vez tratados los outliers; los árboles siguen ganando pero por menos margen.
- VIF: sin quitar constantes ni casi-duplicadas aparecen `inf`/`NaN`; tras limpiar, 34 de 75 variables tienen VIF > 10 y quedan 55 al reducir.
- Lasso: el target vale ~0.01, así que hay que usar `LassoCV` (un `alpha` fijo como 0.01 anula todos los coeficientes).

La solución completa del instructor está en `soluciones-instructor/03-regresion/solucion_taiwan_bankruptcy.ipynb` (no versionada).
