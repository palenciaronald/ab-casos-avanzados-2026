# Informe del EDA — CreditSight

Resultado del notebook `02_eda.ipynb`. Cada hallazgo termina en una decisión, y cada decisión está
implementada con pruebas en `src/creditsight/data/`.

## Qué son los datos

- 100.000 filas × 28 columnas (25 al quitar datos personales y quedarnos con lo útil para modelar).
- **12.500 clientes × 8 meses** (enero–agosto), panel balanceado: la unidad de análisis es el
  **cliente-mes**, no el cliente.
- Objetivo `Credit_Score`: `Standard` 53,2 %, `Poor` 29,0 %, `Good` 17,8 %. Predecir siempre
  `Standard` acierta el 53 %, por eso la exactitud no sirve como métrica.
- La etiqueta cambia entre meses en el **58 %** de los clientes (41,7 % tiene una sola etiqueta; 58,1 %,
  dos; 0,2 %, tres).

## Calidad de los datos

- **Números como texto con basura**: `'23_'`, centinelas (`'_'`, `'_______'`, `'!@9#%8'`) y el valor
  `'__10000__'` repetido 4.305 veces en `Amount_invested_monthly` (marcador de "no disponible").
- **Valores imposibles**: tras p95–p97 los percentiles se disparan (`Num_Bank_Accounts` de 10 a 445,
  `Interest_Rate` de 34 a 2.865, edades de 55 a 4.112), y hay negativos (edad −500, préstamos −100).
- **Variables estables que parecen cambiar**: al descartar los valores corruptos, ocupación, ingreso,
  tasa, número de préstamos y `Credit_Mix` dejan de variar dentro del cliente (de 44–84 % de clientes
  con "cambios" a 0 %). La **edad** sí cambia, pero es el cumpleaños (+1 exacto, 6.877 pasos); solo 5
  clientes tienen una edad corrupta dentro del rango.
- **`Type_of_Loan` vacío = sin préstamos** (coincide con `Num_of_Loan == 0` en las 95.652 filas con
  `Num_of_Loan` válido).
- **Antigüedad crediticia**: sube exactamente un mes por mes (72.373 de 72.373 diferencias); el 9 % de
  vacíos se puede reconstruir.
- **`Credit_Mix`**: muy asociado al objetivo (`Bad` → 60 % `Poor`; `Good` → 49 % `Good`) pero no es el
  objetivo disfrazado (con `Bad`, 38 % es `Standard`).

## Decisiones

| # | Hallazgo | Decisión |
|---|---|---|
| 1 | `Name`, `SSN`, `ID` son datos personales | Se eliminan al cargar |
| 2 | Unidad de análisis cliente-mes, 8 filas por cliente | Particiones y CV **por cliente** |
| 3 | Accuracy da 53 % sin modelo | Métrica = costo esperado; F1 macro y recall de `Poor` como controles |
| 4 | Centinelas y números con `_` sobrante | Centinelas → vacío; quitar `_` y convertir |
| 5 | Salto tras p95–p97 y negativos imposibles | Fuera de rango plausible → vacío, sin borrar filas |
| 6 | Variables estables varían solo por ruido | Reparar con el valor válido más frecuente del cliente |
| 7 | `Credit_Mix` constante por cliente | Reparar igual; medir su aporte con y sin ella |
| 8 | `Type_of_Loan` vacío = sin préstamos | Interpretar, no imputar |
| 9 | Antigüedad +1 mes por mes | Reconstruir, no imputar |
| 10 | Sueldo mensual ≈ ingreso anual / 12 | Rellenar vacíos con la mediana del cliente |

## Qué queda abierto

- Si `Credit_Mix` se conoce en el momento de decidir (¿es un dato de buró previo o posterior?). Se
  mide en la etapa 4 y se discute en el reporte.
- El 20 % de `Credit_Mix` perdido, el 7,6 % de `Payment_Behaviour` perdido y varios vacíos de
  columnas mensuales (2–9 %) se imputan **dentro del pipeline**, ajustados solo con entrenamiento.
