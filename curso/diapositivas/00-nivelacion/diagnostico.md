---
marp: true
theme: default
paginate: true
header: "Casos Avanzados · Maestría en Ingeniería Analítica"
footer: "Fin de semana 1 · Viernes · Diagnóstico (45 min, sin nota)"
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Diagnóstico de lo visto en el curso anterior
## 45 minutos · sin nota · solo para orientar

**Fin de semana 1 · Viernes**

*No es un examen ni una clase de repaso. Sirve para saber dónde hay vacíos.*

---

# Cómo funciona

- **12 preguntas cortas.** Respondan solos, en una hoja, en unos **15 minutos**.
- Luego **revisamos las respuestas** (≈ 20 minutos). Quien falle una pregunta **no recibe
  explicación larga**: se le indica qué buscar y dónde.
- Los últimos minutos: quien tenga **varios vacíos** recibe material de apoyo del curso anterior.

**Objetivo:** que ninguno llegue al fin de semana 2 sin un concepto que necesitará.

*No reenseñamos: detectamos y orientamos.*

---

# Pregunta 1 · Pipeline

**¿Por qué se pone el escalado y el modelo dentro del mismo pipeline en lugar de escalar los
datos antes y luego entrenar?**

---

# Respuesta 1

Porque el escalado **aprende** de los datos (medias, desviaciones). Dentro del pipeline se ajusta
**solo con el conjunto de entrenamiento** de cada partición; fuera de él, esas cifras se calculan
con todos los datos y **filtran información** hacia la validación.

*Palabra clave: fuga de información.*

---

# Pregunta 2 · Validación cruzada

**¿Qué ventaja tiene la validación cruzada sobre una sola partición entrenamiento/validación?
¿Qué información extra te da, además del promedio?**

---

# Respuesta 2

Usa **todos los datos** para evaluar y reduce el azar de una sola partición. Además da la
**dispersión entre folds**: si la diferencia entre dos modelos es menor que esa dispersión, no es
un hallazgo confiable.

---

# Pregunta 3 · Fuga de información

**Tienes varias filas por cliente (por ejemplo, un registro por mes). Haces una partición
aleatoria por fila y tu métrica sale muy alta. ¿Qué sospechas y cómo lo corriges?**

---

# Respuesta 3

Sospecho **fuga entre particiones**: el mismo cliente aparece en entrenamiento y en prueba, y el
modelo lo reconoce. Se corrige particionando **por cliente** (por grupo), no por fila.

---

# Pregunta 4 · Métricas con desbalance

**Una clase es el 5 % de los casos. Un modelo que siempre responde «no» tiene 95 % de exactitud.
¿Qué métricas miras en su lugar y por qué?**

---

# Respuesta 4

La **exactitud engaña**. Se miran **precision, recall, F1** de la clase rara, la matriz de
confusión y curvas **ROC / precision-recall**. Se elige según el **costo** de cada tipo de error.

---

# Pregunta 5 · Umbral

**Un clasificador entrega probabilidades. ¿Por qué el umbral de 0,5 no siempre es el correcto?
¿Quién debería decidir el umbral?**

---

# Respuesta 5

Porque los errores **no cuestan lo mismo**: el umbral es una decisión de **negocio**, no del
modelo. Se mueve según el equilibrio entre falsos positivos y falsos negativos que la
organización acepte.

---

# Pregunta 6 · Ensambles

**¿En qué se diferencian, en una frase, un bosque aleatorio (*bagging*) y un modelo de
*boosting*?**

---

# Respuesta 6

El **bosque** entrena muchos árboles **independientes** y promedia sus respuestas (reduce
varianza). El **boosting** entrena árboles **en secuencia**, cada uno corrigiendo los errores del
anterior (reduce sesgo).

---

# Pregunta 7 · Optimización de hiperparámetros

**Optimizaste hiperparámetros con validación cruzada y la métrica mejoró 0,3 puntos. ¿Cómo
compruebas que la mejora es real y no un efecto de haber probado muchas combinaciones?**

---

# Respuesta 7

Se mide con una **validación independiente de la búsqueda** (validación cruzada anidada o un
conjunto separado) y se compara con la **dispersión entre folds**. Una mejora menor que esa
dispersión no se considera hallazgo.

---

# Pregunta 8 · Conjunto de prueba

**¿Cuántas veces se puede usar el conjunto de prueba para tomar decisiones sobre el modelo?
¿Por qué?**

---

# Respuesta 8

**Una sola vez, al final.** Si se usa para elegir, deja de medir cómo generaliza el modelo,
porque ya quedó ajustado a él.

---

# Pregunta 9 · SHAP

**¿Qué responde un valor SHAP de una variable para un cliente concreto? ¿Qué cuidado debes
tener cuando dos variables están muy correlacionadas?**

---

# Respuesta 9

Responde **cuánto empujó esa variable** la predicción de ese cliente, hacia arriba o hacia abajo,
respecto a un valor de referencia. Con variables **correlacionadas** el aporte se **reparte** entre
ellas y puede engañar: no se interpreta como causa.

---

# Pregunta 10 · Calibración

**Tu modelo dice «80 % de probabilidad de impago». ¿Qué significa que esté bien calibrado y
cómo lo compruebas?**

---

# Respuesta 10

Que de los casos con 80 % predicho, **alrededor del 80 % ocurre de verdad**. Se comprueba con
una **curva de calibración** y el **puntaje de Brier**; si falla, se corrige con una calibración
posterior.

---

# Pregunta 11 · Deriva

**Pasan seis meses y el modelo en producción empeora aunque nadie lo tocó. ¿Qué puede haber
pasado y qué se mide para detectarlo?**

---

# Respuesta 11

Los datos cambiaron (**deriva**): la población o las variables ya no se parecen a las del
entrenamiento. Se detecta comparando distribuciones, por ejemplo con el **índice de
estabilidad poblacional (PSI)**.

---

# Pregunta 12 · Tipo de problema

**Tienes clientes sin ninguna etiqueta y quieres segmentarlos. ¿Cómo sabes si los grupos que
encontraste son buenos, si no hay «respuesta correcta»?**

---

# Respuesta 12

Se evalúa con **estabilidad** (¿salen los mismos grupos con otra muestra?), métricas internas
como la silueta y, sobre todo, **perfilando** los segmentos: ¿tienen sentido y son
accionables para el negocio?

---

# Cómo leer tus resultados

| Aciertos | Qué hacer |
|---|---|
| **10–12** | Vas bien. Sigue con el curso. |
| **7–9** | Repasa solo los temas que fallaste, con tus notas del curso anterior. |
| **0–6** | Habla con el instructor hoy: te sugerimos qué repasar antes del fin de semana 2. |

**Recuerda:** el diagnóstico **no tiene nota**. Un vacío detectado hoy es un problema evitado el
fin de semana 2.

---

<!-- _class: lead -->
<!-- _paginate: false -->

# Siguiente

**Tecnologías del curso** e instalación guiada.
