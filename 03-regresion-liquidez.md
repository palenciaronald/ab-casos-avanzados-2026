# Tema 2: Regresión — Modelo de Liquidez
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

## 5. Estructura de la plantilla (sábado)

Misma estructura de 10 secciones que el demo, pero:
- Secciones 1 y 2 resueltas como ejemplo (incluyendo la explicación de cómo se define el target de liquidez en este dataset)
- Celda de semilla personal (`np.random.seed(cedula)`), usada en el muestreo del dataset y en el `random_state` del `train_test_split`
- Secciones 3 a 9: instrucción en Markdown + celda de código en blanco con comentario guía
- El estudiante entrena **los 6 modelos** (3 lineales + 3 no lineales), no solo el lineal
- Sección 9 (conclusión): 6 preguntas abiertas en Markdown, incluyendo comparar qué modelo ganó y por qué, y si el resultado (36× más filas que la demo) cambia la ventaja de los árboles sobre lo lineal
