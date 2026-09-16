---
marp: true
theme: default
paginate: true
header: "Casos Avanzados · Maestría en Ingeniería Analítica"
footer: "Tema 4 — NLP · marco de clasificación de *ISL* cap. 4 aplicado a texto"
---

<!-- _class: lead -->
<!-- _paginate: false -->

# NLP
## Análisis de Sentimientos Financieros

**Fin de semana 3 · Viernes · Repaso conceptual (~1 h)**

*Marco de clasificación de An Introduction to Statistical Learning (ISL, cap. 4)*
aplicado a datos de texto

---

# El caso de negocio

Un equipo de *research* quiere clasificar el **sentimiento** de noticias y
textos financieros (positivo / neutral / negativo) como **señal** para el
análisis de mercado.

- Entrada: una **oración o titular** financiero (texto libre).
- Salida: una **categoría** de sentimiento → problema de **clasificación
  multiclase**.

> La clave: convertir **texto** en features numéricas y luego aplicar un
> clasificador clásico (ISL cap. 4).

---

# Agenda

1. Del texto a una tarea de clasificación — *marco ISL §4*
2. Pipeline de NLP clásico: limpieza y tokenización
3. Representación: **Bag of Words** y **TF-IDF**
4. Clasificadores: **Naive Bayes** y **regresión logística** — *ISL §4.3*
5. Métricas multiclase: **F1 macro** y matriz de confusión — *ISL §4.4.2*
6. Análisis cualitativo de errores
7. Más allá: embeddings y modelos preentrenados
8. Demo en vivo

---

# 1. Texto como problema de clasificación

El marco de ISL (cap. 4) sigue vigente: predecir una clase $Y$ a partir de
features $X$.

- El reto extra: el texto **no es numérico**.
- **Estrategia:** transformar cada documento en un **vector** de features
  → luego aplicar los mismos clasificadores del cap. 4.

$$\text{texto} \;\longrightarrow\; \text{vector } X \;\longrightarrow\;
\hat{f}(X) \;\longrightarrow\; \text{sentimiento}$$

---

# 2. Pipeline de NLP clásico

Antes de vectorizar, **normalizamos** el texto:

- **Lowercasing:** "Growth" y "growth" → misma palabra.
- **Tokenización:** partir la frase en palabras (tokens).
- **Stopwords:** quitar palabras vacías ("the", "a", "of"…).
- **Lematización / stemming:** reducir a la raíz ("growing" → "grow").

> Menos ruido y menor dimensión → mejor señal para el clasificador.

---

# 3. Bag of Words (BoW)

Representación más simple: contar **cuántas veces** aparece cada palabra del
vocabulario en el documento.

- Cada documento = un vector de longitud = tamaño del vocabulario.
- Ignora el orden de las palabras ("bolsa" de palabras).
- Problema: da el **mismo peso** a palabras muy frecuentes y poco informativas.

---

# 3. TF-IDF

Pondera cada palabra por su **relevancia**: frecuente en el documento, pero rara
en el corpus.

$$\text{tfidf}(t, d) = \underbrace{\text{tf}(t, d)}_{\text{frecuencia en } d}
\times \underbrace{\log\frac{N}{\text{df}(t)}}_{\text{rareza en el corpus}}$$

- $\text{df}(t)$: nº de documentos que contienen el término $t$.
- Baja el peso de palabras ubicuas; realza las **distintivas**.

> TF-IDF + clasificador lineal es un baseline **fuerte y reproducible sin GPU**.

---

# 4. Clasificadores clásicos

Sobre la matriz TF-IDF aplicamos modelos del cap. 4 de ISL:

- **Naive Bayes (multinomial):** rápido, sólido en texto; asume independencia
  entre palabras dada la clase.
- **Regresión logística:** modela $\Pr(\text{clase} \mid X)$ con features
  TF-IDF; interpretable (peso de cada palabra).

> Ambos escalan bien a vocabularios grandes y dispersos.

---

# 4. Regresión logística en texto

ISL §4.3 — la misma logística, ahora con miles de features (una por palabra):

$$\log\!\left(\frac{p(X)}{1 - p(X)}\right) = \beta_0 + \sum_j \beta_j \, x_j$$

- $x_j$ = peso TF-IDF de la palabra $j$.
- Un $\beta_j$ grande y positivo → palabra asociada a sentimiento positivo.
- Extensión **multinomial** para las 3 clases (softmax).

---

# 5. Métricas para multiclase desbalanceada

En noticias financieras, "neutral" suele ser **mayoritaria** → el accuracy
engaña (igual que en el cap. 4).

- **F1 por clase:** balance de precision y recall.
- **F1 macro:** promedio **no ponderado** entre clases
  → trata igual a la clase minoritaria.
- **Matriz de confusión:** ver **qué clases se confunden** entre sí.

> Reportar **F1 macro** es lo apropiado con clases desbalanceadas.

---

# 6. Análisis cualitativo de errores

Más allá de las métricas, **leer los casos mal clasificados**:

- **Negaciones:** "not bad" mal interpretado.
- **Ironía / sarcasmo:** difícil para BoW/TF-IDF.
- **Jerga financiera** y tickers ($ESI, BK…).

> El análisis de errores guía las mejoras del pipeline mejor que una sola
> métrica.

---

# 7. Más allá del baseline

TF-IDF ignora **orden y contexto**. El siguiente nivel:

- **Word embeddings** (Word2Vec, GloVe): palabras como vectores densos con
  significado.
- **Modelos preentrenados** (BERT, **FinBERT**): capturan contexto; estado del
  arte en sentimiento financiero.

> Mención conceptual — requieren más cómputo. TF-IDF sigue siendo el baseline
> reproducible del curso.

---

# Trampas comunes ⚠️

- Reportar **solo accuracy** con "neutral" dominante.
- **Fuga de datos:** ajustar el TF-IDF sobre todo el corpus antes del split
  → vectorizar **dentro** del pipeline, solo con *train*.
- No limpiar el texto (ruido infla el vocabulario).
- Ignorar el desbalance de clases.

---

# Ahora: a la demo 🚀

En el notebook del viernes:

**Carga → Limpieza y tokenización → TF-IDF →
Naive Bayes / Logística → F1 macro + matriz de confusión →
Análisis de errores → Conclusión**

- **Hoy (demo):** Financial PhraseBank — frases de noticias, benchmark limpio.
- **Sábado (tú):** Financial Sentiment (FiQA + PhraseBank) — más volumen y
  estilos mixtos (noticias + foros).

---

<!-- _class: lead -->

# ¿Preguntas?

**Lecturas recomendadas:**
ISL cap. 4 — Classification (§4.3 regresión logística,
§4.4.2 métricas y matriz de confusión), como marco del clasificador
aplicado a features TF-IDF de texto.
