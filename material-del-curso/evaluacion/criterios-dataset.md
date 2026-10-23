# Criterios para elegir el dataset de tu proyecto

El instructor **aprueba el caso** el primer fin de semana según estos criterios (ver
`ficha-de-caso.md`). Un dataset débil hace sufrir al grupo las dos semanas siguientes: elige con
cuidado.

Eres libre de usar un dataset de Kaggle, de otra fuente abierta o de tu trabajo (si no es
confidencial). Kaggle es la recomendación del instructor, pero no es obligatorio.

## Criterios obligatorios

| # | Criterio | Qué se revisa |
|---|---|---|
| 1 | **Volumen suficiente** | **Mínimo 50.000 filas; lo recomendado es 100.000 o más**, y ~10 columnas útiles o más. Sin pasarse mucho de ahí: el cómputo del taller (portátiles y la cuota diaria de Databricks Free) no soporta datasets enormes. Más importante que el número: que haya señal suficiente para comparar modelos con validación cruzada |
| 2 | **Mezcla de tipos de variable** | Numéricas **y** categóricas (idealmente alguna de alta cardinalidad, fecha o texto corto). Un dataset solo de números ya limpios no ejercita el preprocesamiento |
| 3 | **Algo de suciedad real** | Valores faltantes, formatos inconsistentes, atípicos. Un dataset de "juguete" ya limpio no sirve para un caso avanzado |
| 4 | **Objetivo definido** | Debes poder decir en una frase qué predices o qué agrupas y quién usaría el resultado. Si es clasificación/regresión, el objetivo es una columna clara; si es clusterización, hay una decisión de negocio que dependa de los grupos |
| 5 | **Unidad de análisis clara** | Qué es una fila (un cliente, una transacción, un cliente-mes). Si un mismo cliente aparece en varias filas, debes saberlo y partir los datos por cliente |
| 6 | **Decisión de negocio con costo** | Debe haber una acción real y un costo de equivocarse (por ejemplo, rechazar a un buen cliente vs. aprobar a uno que no paga) |
| 7 | **No repetido** | No coincide con los datasets de clase ni con el del ejemplo (lista abajo) |
| 8 | **Sin datos personales sin anonimizar** | Nada de nombres, documentos o contactos reales. Si hay columnas así, se eliminan al inicio |
| 9 | **Sin información confidencial** | Si viene de tu trabajo, tienes permiso explícito por escrito para usarlo en un repo **público** |
| 10 | **Licencia revisada** | Debes poder redistribuirlo o, si no, el repo explica cómo descargarlo sin incluirlo |
| 11 | **Sin fuga evidente del objetivo** | Ninguna columna debe contener la respuesta (o conocerse solo después de ocurrido el hecho que predices) |

## Datasets que NO se pueden usar

**De este curso (clase y ejemplo):**
German Credit, Credit Score Classification (es el del ejemplo CreditSight), Mall Customers,
Credit Card (clusterización), Financial Statements, Taiwan Bankruptcy, y los de NLP de sentimientos
financieros.

**Del curso previo de IA:**
insurance (seguro médico), iris, telco churn, hoteles (reservas de playa en Portugal), Ames Housing,
wine, dígitos (digits), auto MPG y winter activities (turistas de invierno).

Si dudas de si un dataset es "el mismo" con otro nombre, pregunta al instructor.

## Dónde buscar
- **Kaggle** (<https://www.kaggle.com/datasets>): filtra por *tabular*, tamaño mediano y usabilidad
  alta; abre la pestaña de licencia y la de discusión (ahí aparecen los problemas conocidos).
- **UCI Machine Learning Repository**, **datos abiertos de tu gobierno**, **Hugging Face Datasets**.
- **Tu trabajo:** solo con permiso por escrito y anonimizado.

## Ejemplos de rechazo (y por qué)

| Dataset propuesto | Motivo del rechazo | Alternativa |
|---|---|---|
| Titanic | Demasiado conocido, ~900 filas, ya limpio | Un dataset de aseguradora o riesgo con más filas |
| Iris, wine, digits | Son del curso previo; sin suciedad ni dilema de negocio | Cualquier tabla con decisión de negocio |
| Una encuesta de 5.000 filas | Por debajo del mínimo de 50.000 filas para una validación cruzada seria | Una fuente con 50.000 filas o más |
| Un dataset de varios millones de filas | Demasiado grande para portátiles y para la cuota gratuita de Databricks | Una muestra de ~100.000 filas (documentando cómo se muestreó) |
| Base de clientes de mi empresa con nombres y teléfonos | Datos personales y confidenciales en un repo público | Versión anonimizada con permiso escrito, o un dataset abierto equivalente |
| Dataset donde una columna dice "resultado final" del mismo caso que predigo | Fuga del objetivo | Quitar la columna o elegir otro objetivo |
| Datos de precios de una acción para "predecir mañana" | Serie de tiempo: el curso no cubre la validación temporal adecuada | Un problema tabular sin dependencia temporal fuerte |
| Imágenes o audio | El curso es de datos tabulares | Una tabla con características |
| Dataset de Kaggle con licencia que prohíbe redistribuir | No puedes subirlo al repo público | Documentar la descarga, o elegir otro |

## Lista rápida antes de presentar tu propuesta
- [ ] Puedo decir la pregunta de negocio en una frase.
- [ ] Tiene **al menos 50.000 filas** (lo ideal: 100.000 o más).
- [ ] Sé qué es una fila y si hay filas del mismo cliente repetidas.
- [ ] Hay suciedad real y mezcla de tipos de variable.
- [ ] Hay un costo asimétrico de equivocarme.
- [ ] No está en la lista prohibida.
- [ ] No tiene datos personales ni confidenciales; revisé la licencia.
- [ ] Ninguna columna contiene la respuesta.
