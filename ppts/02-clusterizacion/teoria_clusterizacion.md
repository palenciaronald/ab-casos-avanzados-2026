---
marp: true
theme: default
paginate: true
header: "Casos Avanzados · Maestría en Ingeniería Analítica"
footer: "Tema 2 — Clusterización · basado en *ISL* cap. 12"
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Clusterización
## Segmentación de Clientes

**Fin de semana 1 · Viernes · Repaso conceptual (~1 h)**

*Basado en An Introduction to Statistical Learning (ISL)*
Cap. 12 — Unsupervised Learning

---

# El caso de negocio

Una empresa quiere **entender los perfiles** de sus clientes para diseñar
campañas diferenciadas.

- Tenemos variables de comportamiento (ingreso, gasto, uso de productos)…
- …pero **no hay una etiqueta** que diga a qué grupo pertenece cada cliente.

> Objetivo: **descubrir estructura** en los datos sin una variable respuesta.
> Esto es **aprendizaje no supervisado**.

---

# Agenda (enfoque ISL)

1. Supervisado vs. **no supervisado** — *ISL §12.1*
2. El reto del aprendizaje no supervisado
3. **K-means:** idea y objetivo — *ISL §12.4.1*
4. El algoritmo y su naturaleza local
5. **Elegir K:** codo y silhouette
6. Estandarización y clustering jerárquico — *ISL §12.4.2*
7. Perfilamiento e interpretación de negocio
8. Demo en vivo

---

# 1. Aprendizaje no supervisado

ISL §12.1 — solo observamos las features $X_1, \dots, X_p$; **no hay $Y$**.

- No buscamos predecir, sino **descubrir patrones o subgrupos**.
- Dos grandes familias en ISL:
  - **PCA** — reducción de dimensión (§12.2)
  - **Clustering** — encontrar grupos homogéneos (§12.4)

> Es **más subjetivo**: no hay una respuesta "correcta" ni un error a minimizar
> de forma tan clara como en lo supervisado.

---

# 2. El reto de no tener etiqueta

ISL §12.1 — sin $Y$ verdadero:

- No podemos calcular *accuracy* ni RMSE.
- No hay validación cruzada directa contra la "verdad".
- La **evaluación es indirecta**: cohesión interna, separación, e
  **interpretabilidad de negocio**.

> El éxito se juzga por si los segmentos son **accionables**, no por una métrica
> única.

---

# 3. K-means — la idea

ISL §12.4.1 — partir las observaciones en **K grupos** sin solapamiento, tan
**homogéneos internamente** como sea posible.

Minimiza la **variación intra-cluster** total:

$$\min_{C_1,\dots,C_K} \sum_{k=1}^{K} W(C_k)$$

con la variación medida como distancia euclídea al cuadrado:

$$W(C_k) = \frac{1}{|C_k|} \sum_{i, i' \in C_k} \sum_{j=1}^{p} (x_{ij} - x_{i'j})^2$$

---

# 3. El algoritmo K-means

ISL §12.4.1 — iterativo:

1. Asignar aleatoriamente cada observación a uno de los K clusters.
2. **Repetir hasta converger:**
   a. Calcular el **centroide** de cada cluster.
   b. Reasignar cada observación al centroide **más cercano**.

- Garantiza reducir el objetivo en cada paso.
- Converge a un **óptimo local** → depende de la inicialización.

---

# 4. Naturaleza local → múltiples inicios

- Distintos arranques → distintas soluciones.
- **Solución:** correr el algoritmo varias veces (`n_init`) y quedarse con la de
  menor variación intra-cluster.
- Fijar `random_state` para **reproducibilidad**.

> En la práctica, `KMeans(n_init=10, random_state=...)`.

---

# 5. ¿Cuántos clusters? — Método del codo

No hay un K "verdadero"; lo elegimos con criterios:

- Graficar la **inercia** (variación intra-cluster) frente a K.
- Buscar el **"codo"**: el punto donde añadir clusters ya **no reduce mucho** la
  inercia.

$$\text{inercia} = \sum_{k} W(C_k)$$

---

# 5. ¿Cuántos clusters? — Silhouette

Complementa al codo midiendo **qué tan bien** está asignada cada observación:

$$s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}$$

- $a(i)$: distancia media a su propio cluster.
- $b(i)$: distancia media al cluster vecino más cercano.
- $s \in [-1, 1]$; **más alto = mejor** separación.

---

# 6. La escala importa

K-means usa **distancias** → variables en escalas grandes dominan.

- Un balance de miles pesaría más que una frecuencia entre 0 y 1.
- **Solución:** estandarizar (`StandardScaler`, media 0, desviación 1) antes de
  clusterizar.

> ISL insiste: la decisión de **escalar** cambia por completo los grupos
> resultantes (§12.4.2).

---

# 6. Alternativa: clustering jerárquico

ISL §12.4.2 — no exige fijar K de antemano.

- Construye un **dendrograma** (árbol de fusiones sucesivas).
- Se "corta" a la altura deseada para obtener K grupos.
- Depende de la **medida de enlace** (linkage) y de la distancia.

> Mención breve: útil cuando se quiere explorar la estructura a varias
> resoluciones. Hoy nos centramos en K-means.

---

# 7. Perfilamiento — dar sentido a los clusters

Encontrar los grupos es solo la mitad; hay que **interpretarlos**.

- Calcular la **media de cada variable por cluster**.
- Traducir a **etiquetas de negocio**: "premium de alto gasto",
  "potencial no explotado", "sensibles a promociones"…
- Definir una **acción distinta** por segmento.

> El valor está en la **interpretación accionable**, no en el algoritmo.

---

# Trampas comunes ⚠️

- **No estandarizar** cuando las escalas difieren.
- Tomar el primer K sin evaluar codo/silhouette.
- Un solo `n_init` → caer en un óptimo local pobre.
- Sobre-interpretar clusters que en realidad son ruido.
- Olvidar que **no hay respuesta única**: la validación es de negocio.

---

# Ahora: a la demo 🚀

En el notebook del viernes:

**Carga → Escalado → Elegir K (codo + silhouette) → K-means →
Visualización → Perfilamiento e interpretación**

- **Hoy (demo):** Mall Customers — 200 clientes, 2 variables clave (2D).
- **Sábado (tú):** Credit Card — 8.950 clientes, 17 variables de
  comportamiento (usarás PCA para visualizar).

---

<!-- _class: lead -->

# ¿Preguntas?

**Lecturas ISL recomendadas:**
cap. 12 — Unsupervised Learning (§12.1 introducción,
§12.4.1 K-means, §12.4.2 clustering jerárquico y escalado).
