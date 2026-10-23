# Especificación del proyecto — CreditSight (ejemplo de referencia)

> **Esta es la plantilla `material-del-curso/kit/especificacion-proyecto.md` ya diligenciada** para el
> ejemplo del instructor. Úsenla como modelo del nivel de detalle esperado. Claude la lee antes de
> generar código: lo que está aquí manda sobre cualquier otra suposición.

## 1. Grupo

| Integrante | Rol (datos / modelado / app / negocio) |
|---|---|
| Instructor | Todos los roles (proyecto de referencia, no es de un grupo) |

Nombre de la "startup": **CreditSight**   Repositorio (público): este repositorio, carpeta `material-del-curso/ejemplo-creditsight/`

## 2. Caso de negocio

- **Pregunta de negocio** (una frase, que alguien sin formación técnica entienda):
  ¿Podemos clasificar a cada cliente como `Good`, `Standard` o `Poor` a partir de su perfil
  financiero y su historial de pagos, para **priorizar la revisión** del analista de riesgo y
  acelerar las aprobaciones de crédito?
- **¿Quién usará el resultado y qué decisión tomará con él?**
  El **analista de riesgo** de una fintech que ofrece líneas de crédito digitales. Decide si asigna
  **un límite alto, uno estándar o uno restringido**. Hoy revisa a mano el historial y tarda días.
  El modelo **no decide solo**: ordena la cola de trabajo y el analista conserva la decisión final.
- **¿Qué cuesta equivocarse?** (cuál error es peor y por qué):
  **Clasificar como `Good` o `Standard` a un cliente que es `Poor`** es el error **más caro**: se le
  asigna un límite que no podrá pagar y la fintech pierde capital. **Clasificar como `Poor` a un
  cliente que es `Good`** es menos grave: se le restringe el límite y se pierde un buen cliente, pero
  el analista revisa el caso y es recuperable. La matriz de costos usada está en la sección 4.

## 3. Datos

- **Fuente** (enlace de Kaggle, empresa, etc.):
  *Credit score classification* (Kaggle, autor Rohan Paris, 2022), archivo
  `credit_score_classification.csv`, en `data/01-clasificacion/` del repositorio del curso. Datos
  **sintéticos**.
- **Filas / columnas:** 100.000 filas × 28 columnas (25 al quitar los tres campos de datos personales).
- **Variable objetivo** (columna que queremos predecir o describir): `Credit_Score`, con tres clases:
  `Standard` (53,2 %), `Poor` (29,0 %) y `Good` (17,8 %).
- **Tipo de problema:** ☒ clasificación (multiclase y desbalanceada)  ☐ regresión  ☐ clusterización
- **¿Una misma entidad (cliente, paciente, empresa) aparece en varias filas?** ☐ no  ☒ sí → la partición
  será por: **cliente (`Customer_ID`)**. Hay 12.500 clientes × 8 meses; **la unidad de análisis es el
  cliente-mes**, y la etiqueta cambia entre meses en el 58 % de los clientes.
- **Datos personales o confidenciales presentes:** ☐ no  ☒ sí → se eliminarán/anonimizarán así:
  `Name`, `SSN` e `ID` se **eliminan al cargar los datos** (`load_raw`) y nunca llegan al modelo.
- **Licencia o permiso de uso de los datos:** **por confirmar** (campo de licencia de la página de
  Kaggle); pendiente de verificación por el instructor.

## 4. Métrica

- **Métrica principal:** **costo esperado por cliente-mes** con una matriz de costos de negocio
  (menor es mejor).
  **Por qué esa y no otra:** equivocarse no cuesta lo mismo en las dos direcciones, y la exactitud
  (accuracy) engaña: predecir siempre `Standard` ya acierta ~53 %.

  | real \ predicho | Poor | Standard | Good |
  |---|---|---|---|
  | **Poor** | 0 | 3 | 10 |
  | **Standard** | 1 | 0 | 3 |
  | **Good** | 2 | 1 | 0 |

- **Métricas secundarias:** **F1 macro** (ninguna clase puede ignorarse) y **recall de `Poor`** (la
  clase que más cuesta no detectar). Regla de decisión: no se elige la clase más probable sino la de
  **menor costo esperado**.
- **Línea base** (qué resultado obtiene una regla simple o un modelo trivial): **siempre `Standard`**
  cuesta **1,05** por cliente-mes; adivinar al azar según las proporciones, **1,62**. Todo modelo debe
  ganarles con holgura.

## 5. Riesgos

- **Fuga de información posible:** partir los datos **por fila** pone meses del mismo cliente en
  entrenamiento y en prueba y **infla la métrica**. Se parte siempre por cliente. Además, `Credit_Mix`
  está muy asociada al objetivo (`Bad` → 60 % `Poor`): se mide el modelo **con y sin** ella y se asume
  que **se conoce al momento de decidir**.
- **Sesgos o equidad:** la **edad** y la **ocupación** son variables del modelo; su uso en crédito real
  suele estar regulado. Se revisa el error por segmento y se declara en la ficha del modelo.
- **Datos faltantes o de mala calidad:** números guardados como texto con basura (`'23_'`), valores
  centinela (`'_'`, `'__10000__'`, `'!@9#%8'`), valores imposibles (edad −500, tasas de miles de por
  ciento) y vacíos en `Credit_Mix` (20 %) y `Payment_Behaviour` (7,6 %).
- **Límites de lo que el modelo puede decir:** datos **sintéticos**; apoya una priorización, no
  reemplaza una decisión de crédito; no se evaluó estabilidad en el tiempo ni deriva.

## 6. Entregables y fechas

| Hito | Contenido | Fecha |
|---|---|---|
| H1 | Ficha aprobada, EDA y preprocesamiento reproducible | Cierre del FDS 1 (sábado) |
| H2 | Torneo, optimización con tracking, modelo registrado, repo modular, app local | Cierre del FDS 2 (sábado) |
| H3 | App desplegada y presentación (≤ 5 diapositivas) | Viernes del FDS 3 |
| H4 | Informe técnico final (hasta 8 días tras la última clase) | 8 días tras la última clase |

## 7. Decisiones tomadas (agréguenlas a medida que avancen)

Las diez decisiones del EDA (`reports/01_eda.md`, notebook `02_eda`):

| Fecha | Decisión | Motivo |
|---|---|---|
| EDA (FDS 1) | Se eliminan `Name`, `SSN` e `ID` al cargar | Son datos personales (sintéticos, pero se tratan como reales) |
| EDA (FDS 1) | Particiones y validación cruzada **por cliente** | La unidad de análisis es el cliente-mes: 8 filas por cliente |
| EDA (FDS 1) | Métrica = costo esperado; F1 macro y recall de `Poor` como controles | Accuracy da 53 % sin modelo y los errores cuestan distinto |
| EDA (FDS 1) | Los centinelas pasan a vacío; se quita el `_` sobrante y se convierte a número | Centinelas y números con `_` sobrante en varias columnas |
| EDA (FDS 1) | Valores fuera de un rango plausible pasan a vacío, sin borrar filas | Salto brusco tras p95–p97 y negativos imposibles |
| EDA (FDS 1) | Variables estables se reparan con el valor válido más frecuente **del propio cliente** | Variaban entre meses solo por ruido; no cruza particiones |
| EDA (FDS 1) | `Credit_Mix` se repara igual y se mide con y sin ella | Es constante por cliente (los `_` eran perdidos) |
| EDA (FDS 1) | `Type_of_Loan` vacío se interpreta como "sin préstamos", no se imputa | Coincide con `Num_of_Loan == 0` en las 95.652 filas con `Num_of_Loan` válido |
| EDA (FDS 1) | La antigüedad crediticia se reconstruye, no se imputa | Sube exactamente 1 mes por mes (72.373 de 72.373 diferencias) |
| EDA (FDS 1) | El sueldo mensual vacío se rellena con la mediana del cliente | Es casi el ingreso anual / 12 |
