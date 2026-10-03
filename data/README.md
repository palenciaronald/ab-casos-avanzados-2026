# Datasets del curso — resumen por tema

> **Nota:** los datasets **están versionados en este repo**, así que
> al clonar ya tienes todo listo para ejecutar los notebooks. Son datasets de
> Kaggle (enlaces en cada tema).

## Cómo funcionan las "dos bases por tema" (no son train/test)

Cada tema tiene **dos bases distintas**, una por rol de la sesión:

- **Base del viernes (demo):** el caso que el instructor resuelve en vivo.
- **Base del sábado (ejercicio):** un caso **diferente**, del mismo dominio y
  técnica, que el estudiante resuelve solo como entrega.

**No son un par train/test del mismo problema.** El split train/test se hace
*dentro* de cada notebook, sobre una sola base, con la semilla de la cédula
(`train_test_split(..., random_state=cedula)`). Por eso, si un dataset de Kaggle
trae un `test.csv` sin la columna target, ese archivo no se usa: cada notebook
parte su propia base internamente.

La base del sábado es siempre **más grande y/o más sucia** que la del viernes,
para que el estudiante aplique con fricción real lo que vio en la demo
(limpieza, escalado, selección de variables).

---

## Tema 1 — Clasificación (predecir una categoría)

### Viernes · `data/01-clasificacion/german_credit_data.csv`
- **Filas × columnas:** 1000 × 11 (incluye columna índice).
- **Problema:** clasificar solicitantes de crédito como buen/mal pagador.
  Clasificación **binaria**.
- **Target:** `Risk` (good / bad).
- **Features:** Age, Sex, Job, Housing, Saving accounts, Checking account,
  Credit amount, Duration, Purpose.
- **Notas:** pequeño y limpio, ideal para la demo. Tiene `NA` en
  *Saving accounts* y *Checking account* → buena oportunidad para mostrar
  tratamiento de nulos.

### Sábado · `data/01-clasificacion/credit_score_classification.csv`
- **Filas × columnas:** 100000 × 28.
- **Problema:** clasificar el score crediticio en 3 niveles. Clasificación
  **multiclase**.
- **Target:** `Credit_Score` (Poor / Standard / Good).
- **Features:** 27 variables (ingreso anual, salario mensual, nº de cuentas y
  tarjetas, tasa de interés, nº de préstamos, retrasos de pago, deuda pendiente,
  utilización de crédito, historial, comportamiento de pago, balance, etc.).
- **Notas:** grande y **sucio a propósito** (valores atípicos, columnas mixtas
  texto/número) → exige preprocesamiento fuerte del estudiante.

**Diferencia clave:** binaria y limpia (viernes) → multiclase, grande y sucia (sábado).

---

## Tema 2 — Clusterización (segmentar sin etiqueta)

### Viernes · `data/02-clusterizacion/Mall_Customers.csv`
- **Filas × columnas:** 200 × 5.
- **Problema:** segmentar clientes de un centro comercial por comportamiento de
  gasto. Aprendizaje **no supervisado** (sin target).
- **Variables:** CustomerID, Genre, Age, Annual Income (k$), Spending Score (1-100).
- **Notas:** mínima fricción; se puede graficar en 2D (ingreso vs. gasto),
  ideal para explicar K-Means y el método del codo visualmente.

### Sábado · `data/02-clusterizacion/CC_GENERAL.csv`
- **Filas × columnas:** 8950 × 18.
- **Problema:** segmentar tarjetahabientes por comportamiento financiero.
  No supervisado (sin target).
- **Variables:** 17 de comportamiento (BALANCE, PURCHASES, ONEOFF_PURCHASES,
  INSTALLMENTS_PURCHASES, CASH_ADVANCE, frecuencias, CREDIT_LIMIT, PAYMENTS,
  MINIMUM_PAYMENTS, PRC_FULL_PAYMENT, TENURE, etc.) + `CUST_ID`.
- **Notas:** más rica; tiene `NA` en *MINIMUM_PAYMENTS* y *CREDIT_LIMIT*
  (imputar), y **exige escalado** antes de clusterizar.

**Diferencia clave:** 2 variables visualizables (viernes) → 17 variables de comportamiento con NA y escalado obligatorio (sábado).

---

## Tema 3 — Regresión (predecir un número continuo)

### Viernes · `data/03-regresion/financial_statements.csv`
- **Filas × columnas:** 161 × 23.
- **Problema:** estimar la liquidez (`Current Ratio`) de empresas grandes a
  partir de otros indicadores financieros.
- **Target:** `Current Ratio`.
- **Features:** Revenue, Gross Profit, Net Income, EBITDA, Share Holder Equity,
  flujos de caja, Debt/Equity Ratio, ROE, ROA, ROI, Net Profit Margin, etc.
  (panel de empresas reconocibles como AAPL por año).
- **Notas:** pequeño y limpio. El header trae un BOM y espacios en algunos
  nombres de columna (p. ej. `Company `) → limpiar nombres al cargar.

### Sábado · `data/03-regresion/taiwan_bankruptcy.csv`
- **Filas × columnas:** 6819 × 96.
- **Problema:** mismo target de liquidez (`Current Ratio`), pero con 95 ratios
  financieros como predictores.
- **Target:** `Current Ratio`.
- **Notas:** mucho más grande y denso → exige **selección de variables** y
  manejo de **multicolinealidad** (VIF).
- **⚠️ CRÍTICO — variables a EXCLUIR de las features** (son casi-duplicadas del
  target y producen fuga de información / R² artificialmente ≈ 1):
  `Quick Ratio`, `Quick Assets/Current Liability`, `Cash/Current Liability`,
  `Current Liability to Assets`, `Current Liability to Current Assets`.
  (Confirmadas presentes en el archivo.)

**Diferencia clave:** pocas variables limpias (viernes) → 95 ratios con colinealidad real y trampa de fuga de información (sábado).

---

## Tabla resumen

| Tema | Rol | Archivo | Filas | Cols | Target | Tipo de problema |
|---|---|---|---|---|---|---|
| 1 Clasificación | Viernes | german_credit_data.csv | 1 000 | 11 | `Risk` | Binaria |
| 1 Clasificación | Sábado | credit_score_classification.csv | 100 000 | 28 | `Credit_Score` | Multiclase |
| 2 Clusterización | Viernes | Mall_Customers.csv | 200 | 5 | — | No supervisado |
| 2 Clusterización | Sábado | CC_GENERAL.csv | 8 950 | 18 | — | No supervisado |
| 3 Regresión | Viernes | financial_statements.csv | 161 | 23 | `Current Ratio` | Regresión |
| 3 Regresión | Sábado | taiwan_bankruptcy.csv | 6 819 | 96 | `Current Ratio` | Regresión |
