---
marp: true
theme: default
paginate: true
header: "Casos Avanzados · Maestría en Ingeniería Analítica"
footer: "Tema 1 — Clasificación · desde cero (~2 h) · basado en *ISL*"
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Clasificación
## Enseñar a una máquina a decidir "sí" o "no"

**Fin de semana 1 · Viernes · Clase teórica (~2 h)**

De cero: qué es aprender de los datos → cómo se construye y evalúa un modelo
*Basado en An Introduction to Statistical Learning (ISL)*

---

<!-- _class: lead -->
# Parte 1
## ¿Qué es la Inteligencia Artificial y el Machine Learning?

---

# La idea en una frase

**Machine Learning (ML):** enseñar a una computadora a **encontrar patrones en
datos** para tomar decisiones, **sin programarle las reglas una por una**.

- Programación clásica: *nosotros* escribimos las reglas.
- Machine Learning: le damos **ejemplos** y la máquina **deduce las reglas**.

> IA es el campo amplio; ML es la técnica más usada hoy; el *aprendizaje
> profundo* (redes neuronales) es una rama del ML.

---

# Un ejemplo cotidiano

¿Cómo aprendiste a distinguir un correo **spam** de uno normal?

- Nadie te dio una lista exacta de reglas.
- Viste **muchos ejemplos** y notaste patrones ("premio gratis", remitentes
  raros…).

**El ML hace lo mismo:** le mostramos miles de correos ya etiquetados
(spam / no spam) y aprende a clasificarlos solo.

---

# Programación clásica vs. Machine Learning

| | Entrada | Proceso | Salida |
|---|---|---|---|
| **Clásica** | datos + **reglas** | ejecuta | resultado |
| **ML** | datos + **resultados** | **aprende** | **reglas (modelo)** |

> En ML, el "programa" que queremos obtener se llama **modelo**, y se construye
> **entrenándolo** con datos.

---

# Los tres tipos de aprendizaje

- **Supervisado** — los datos traen la **respuesta correcta** (etiqueta).
  Ej.: correos marcados como spam / no spam. *(temas 1, 3 y 4)*
- **No supervisado** — **no hay respuesta**; buscamos estructura oculta.
  Ej.: agrupar clientes parecidos. *(tema de clusterización)*
- **Por refuerzo** — aprende por ensayo y error con recompensas.
  Ej.: un robot que aprende a caminar. *(fuera de este curso)*

> Hoy trabajamos **aprendizaje supervisado**.

---

# Vocabulario esencial (lo usaremos todo el curso)

- **Observación / fila:** un caso (un cliente).
- **Variable / *feature* / columna:** una característica (edad, ingreso).
- **Etiqueta / *target* / $Y$:** lo que queremos predecir (¿buen o mal pagador?).
- **Modelo:** la "fórmula" aprendida que va de las features a la predicción.

$$\underbrace{\text{features } X}_{\text{lo que sabemos}}
\;\longrightarrow\; \boxed{\text{modelo}} \;\longrightarrow\;
\underbrace{\text{predicción } \hat{Y}}_{\text{lo que estimamos}}$$

---

# Regresión vs. Clasificación

Según **qué tipo de respuesta** queremos:

- **Regresión:** predecir un **número** (¿cuánto valdrá la casa?). → Tema 3
- **Clasificación:** predecir una **categoría** (¿buen o mal pagador?). → **hoy**

> Hoy: **clasificación**. Enseñar a la máquina a poner cada caso en una
> **categoría**.

---

<!-- _class: lead -->
# Parte 2
## El problema de hoy: Score de Riesgo Crediticio

---

# El caso de negocio

Un **banco** recibe solicitudes de crédito y debe decidir a quién prestarle.

- De cada solicitante conocemos: edad, empleo, vivienda, cuentas, monto y
  duración del crédito…
- Queremos predecir: ¿será **buen pagador** (*good*) o **mal pagador** (*bad*)?

> Si acertamos, **reducimos la mora** y damos crédito con criterio.
> Este es un problema de **clasificación binaria** (dos categorías).

---

# ¿Cómo "aprende" el modelo aquí?

1. Tomamos **miles de créditos pasados** donde ya sabemos quién pagó y quién no.
2. El modelo estudia qué combinaciones de características se asociaron a
   **impago**.
3. Ante un **nuevo** solicitante, estima su probabilidad de ser mal pagador.

> La calidad depende de **aprender el patrón real**, no de memorizar los casos
> vistos (volveremos a esto: *sobreajuste*).

---

# El marco formal (ISL §2.1)

Suponemos que existe una relación entre las features y la respuesta:

$$Y = f(X) + \varepsilon$$

- $f$ = el patrón real (desconocido) que relaciona $X$ con $Y$.
- $\varepsilon$ = azar / cosas que no medimos (**error irreducible**).
- El modelo produce una **estimación** $\hat{f}$ de ese patrón.

> No buscamos la perfección: buscamos **capturar el patrón** lo mejor posible.

---

# El clasificador ideal: Bayes (ISL §2.2.3)

Si conociéramos las probabilidades reales, la mejor decisión sería:

> asignar cada caso a la **clase más probable** dado lo que sabemos de él.

- Ese clasificador ideal tiene el **mínimo error posible** (error de Bayes).
- **No es alcanzable** (no conocemos la realidad exacta).
- Todos los métodos (logística, árboles…) **intentan aproximarlo**.

---

<!-- _class: lead -->
# Parte 3
## Cómo entrenamos y evaluamos con honestidad

---

# Train / Test: la regla de oro

Si evaluamos el modelo con los **mismos** datos con que aprendió, nos engañamos
(es como corregir un examen con las respuestas a la vista).

- **Train (entrenamiento):** el modelo aprende aquí (p. ej. 75%).
- **Test (prueba):** medimos el desempeño con datos **nunca vistos** (25%).

> Solo el desempeño en **test** dice si el modelo **generaliza**.

---

# Sobreajuste (overfitting) — el error nº 1

- **Sobreajuste:** el modelo **memoriza** el train (incluido el ruido) y falla
  con datos nuevos.
- **Subajuste:** el modelo es demasiado simple y no capta el patrón.

> Analogía: estudiar memorizando las preguntas del año pasado (sobreajuste) vs.
> entender la materia (generaliza).

Buscamos el punto medio → **trade-off sesgo–varianza** (ISL §2.2).

---

# Sesgo y varianza — intuición

- **Sesgo alto:** el modelo simplifica de más → se equivoca sistemáticamente.
- **Varianza alta:** el modelo cambia mucho con pequeños cambios en los datos →
  inestable.

> Un buen modelo equilibra ambos: ni demasiado simple, ni demasiado complejo.
> Es el hilo conductor de ISL.

---

<!-- _class: lead -->
# Parte 4
## Los modelos de clasificación que usaremos

---

# Modelo 1: Regresión Logística (ISL §4.3)

En vez de decir directamente "good/bad", estima **la probabilidad** de la clase:

$$p(X) = \frac{e^{\beta_0 + \beta_1 X_1 + \dots + \beta_p X_p}}
{1 + e^{\beta_0 + \beta_1 X_1 + \dots}}$$

- Da un número entre **0 y 1** (probabilidad de ser mal pagador).
- Si $p(X) > 0.5$ → clasifica como *bad* (el umbral se puede ajustar).

> Es el **punto de partida** clásico: simple e **interpretable**.

---

# ¿Por qué "logística"? — intuición

Una recta puede dar valores absurdos (−3, 1.8…) para una probabilidad.

- La función **logística** aplasta cualquier número al rango **[0, 1]**.
- Así la salida **siempre** es una probabilidad válida.

$$\text{cualquier valor} \;\xrightarrow{\text{logística}}\; \text{entre 0 y 1}$$

> Y el "peso" $\beta_j$ de cada variable nos dice **cómo influye** en el riesgo.

---

# Modelo 2: Árbol de decisión (ISL §8.1)

Una serie de preguntas **sí/no** encadenadas, como un diagrama de flujo:

```
¿Monto > 5000?
├── sí → ¿Duración > 24 meses? → ...
└── no → probablemente good
```

- Muy **fácil de interpretar** y visualizar.
- Pero un solo árbol es **inestable** (cambia mucho con los datos → varianza
  alta).

---

# Modelo 3: Random Forest (ISL §8.2)

Idea: **muchos árboles votan** y se promedia → más estable y preciso.

- Cada árbol se entrena con una muestra distinta de los datos.
- Cada división mira solo **algunas** variables al azar (los "decorrelaciona").
- Predicción final = **voto mayoritario** de todos los árboles.

> "La sabiduría de la multitud": muchos modelos simples combinados superan a uno
> solo. Además, nos dice qué variables son **más importantes**.

---

<!-- _class: lead -->
# Parte 5
## ¿Cómo sabemos si el modelo es bueno?

---

# Por qué el "accuracy" solo engaña

Si el 70% de los clientes son *good*, un modelo que **siempre diga "good"**
acierta el 70%… ¡y nunca detecta a un mal pagador!

- **Accuracy** = % de aciertos totales → insuficiente con clases desbalanceadas.
- Necesitamos métricas que miren **cada clase por separado**.

---

# La matriz de confusión (ISL §4.4.2)

Cuenta los aciertos y errores de cada tipo:

|              | Pred. good | Pred. bad |
|--------------|:----------:|:---------:|
| **Real good**| ✅ TN | ❌ FP (falsa alarma) |
| **Real bad** | ❌ **FN** | ✅ TP |

- **Falso Negativo (FN):** dijimos "good" pero **no pagó** → el error **caro**
  para el banco.

---

# Precision, Recall y F1 — en palabras

- **Precision:** de los que predije *bad*, ¿cuántos lo eran de verdad?
  *(¿cuánta de mi alarma es real?)*
- **Recall (sensibilidad):** de los *bad* reales, ¿cuántos detecté?
  *(¿cuántos malos se me escaparon?)*
- **F1:** un balance entre precision y recall (un solo número).

> En banca solemos priorizar **recall de la clase *bad*** (no dejar pasar malos
> pagadores).

---

# La curva ROC y el AUC (ISL §4.4.2)

El modelo da una **probabilidad**; el **umbral** para decidir (0.5, 0.3…) lo
elegimos nosotros.

- La **curva ROC** muestra el desempeño para **todos** los umbrales.
- El **AUC** (área bajo la curva) lo resume: **1 = perfecto, 0.5 = azar**.

> Ventaja: compara modelos **sin fijar** todavía el punto de corte de negocio.

---

# Desbalance de clases — cómo tratarlo

Cuando una clase es rara (30% *bad*), el modelo tiende a ignorarla. Opciones:

- `class_weight="balanced"` → penaliza más equivocarse en la clase rara.
- **Re-muestreo** (crear/replicar ejemplos de la clase minoritaria, p. ej. SMOTE).
- **Bajar el umbral** de decisión (marcar *bad* con menos "sospecha").

> Hoy usaremos `class_weight="balanced"` en el notebook.

---

# Interpretabilidad — clave en banca

Un comité de crédito debe poder **explicar** por qué niega un préstamo (y la ley
a veces lo exige).

- **Logística:** el signo y tamaño de cada $\beta_j$.
- **Random Forest:** la **importancia de variables**.

> Trade-off: modelos más potentes suelen ser **menos explicables**
> (flexibilidad ↔ interpretabilidad, ISL §2.2).

---

# Trampas comunes ⚠️

- Reportar **solo accuracy** con clases desbalanceadas.
- **Fuga de datos:** preparar los datos usando información del test
  → todo dentro de un `Pipeline`, ajustando solo con train.
- No **estratificar** el train/test (perder la proporción de clases).
- Confundir **correlación con causalidad** al interpretar.

---

# Resumen de la clase

- ML = aprender **patrones de los datos** en vez de programar reglas.
- **Clasificación** = predecir una **categoría**; hoy binaria (good/bad).
- Separamos **train/test** para medir con honestidad y evitar **sobreajuste**.
- Modelos: **Logística** (interpretable), **Árbol**, **Random Forest** (potente).
- Evaluamos con **matriz de confusión, precision/recall/F1 y ROC-AUC**, no solo
  accuracy.

---

# Ahora: a la demo 🚀

Recorreremos el pipeline completo en el notebook del viernes:

**Carga → Explorar datos → Preparar → Logística + Random Forest →
Matriz de confusión, ROC-AUC → Importancia de variables → Conclusión**

- **Hoy (demo):** German Credit — 1.000 clientes, target `Risk` (binaria).
- **Sábado (tú):** Credit Score — 100.000 filas, 3 clases, datos "sucios".

---

<!-- _class: lead -->

# ¿Preguntas?

**Para profundizar (ISL):**
cap. 2 (aprendizaje estadístico, train/test, sesgo–varianza),
cap. 4 (clasificación, regresión logística, ROC),
cap. 8 (árboles, random forest).
