# Tema 2: Regresión — Modelo de Liquidez
## Fin de semana 2 (25–26 sep)

## 1. Caso de negocio

Un analista financiero quiere estimar el nivel de liquidez de una empresa (medido como un ratio continuo, ej. Current Ratio) a partir de otros indicadores financieros disponibles en sus estados financieros, para anticipar riesgos de liquidez sin depender únicamente del cálculo directo. El estudiante construye un modelo de regresión donde la variable objetivo es un ratio de liquidez y las features son otros ratios/indicadores financieros.

**Nota:** a diferencia de los otros temas, aquí no hay un dataset "de liquidez" con ese nombre — se usa el `current_ratio` / `Current Ratio` que ya viene calculado en ambas bases como variable objetivo (`y`), y el resto de columnas financieras como predictoras (`X`).

**Variables a excluir de las features en el dataset del sábado por ser casi-duplicadas del target** (fuga de información / colinealidad extrema): `Acid Test` (Quick Ratio), `Quick Assets/Current Liability`, `Cash/Current Liability`, `Current Liability to Current Assets`, `Current Liability to Assets`. Todas estas miden esencialmente lo mismo que el Current Ratio y dejarlas como predictoras haría el modelo trivial (R² artificialmente cercano a 1). Esto es justo un buen punto de teoría para el viernes: "cuidado con las variables que son una reformulación del target."

## 2. Teoría a repasar el viernes (~1 hora)

- Regresión lineal: supuestos (linealidad, homocedasticidad, normalidad de residuos, no multicolinealidad)
- Métricas de regresión: MAE, RMSE, R², R² ajustado
- Diagnóstico de residuos (gráfico de residuos vs. predichos, QQ-plot)
- Multicolinealidad: VIF (Variance Inflation Factor) y por qué importa con muchos ratios financieros correlacionados entre sí
- Regularización (Ridge/Lasso) como mención — útil dado el alto número de variables en el dataset del sábado
- Interpretación de coeficientes en contexto financiero (¿qué significa el signo y la magnitud?)

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
5. Entrenamiento de regresión lineal (baseline) y comparación con un modelo regularizado (Ridge o Lasso)
6. Evaluación: MAE, RMSE, R², gráfico de residuos
7. Interpretación de coeficientes: ¿qué ratios explican mejor la liquidez?
8. Conclusión de negocio: ¿qué indicadores debería monitorear el analista financiero de cerca?

## 5. Estructura de la plantilla (sábado)

Misma estructura de 8 secciones que el demo, pero:
- Secciones 1 y 2 resueltas como ejemplo (incluyendo la explicación de cómo se define el target de liquidez en este dataset)
- Celda de semilla personal (`np.random.seed(cedula)`), usada en el muestreo del dataset y en el `random_state` del `train_test_split`
- Secciones 3 a 7: instrucción en Markdown + celda de código en blanco con comentario guía
- Sección 8 (conclusión): 2–3 preguntas abiertas en Markdown, ej.:
  - "¿Qué ratios muestran mayor riesgo de multicolinealidad, y cómo lo detectaste?"
  - "Si tuvieras que reducir el modelo a solo 3 variables por simplicidad operativa, ¿cuáles elegirías y por qué?"
