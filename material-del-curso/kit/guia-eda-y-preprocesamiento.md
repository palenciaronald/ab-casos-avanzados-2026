# Guía de trabajo: EDA y preprocesamiento (clase 2 · hito H1)

Esta guía es para **tu dataset**, no para el de CreditSight. El ejemplo del instructor
(`material-del-curso/ejemplo-creditsight/notebooks/02_eda.ipynb`, `material-del-curso/ejemplo-creditsight/notebooks/03_preprocesamiento.ipynb` y
`material-del-curso/ejemplo-creditsight/reports/01_eda.md`) te muestra **cómo se razona**, pero sus cifras y sus decisiones no
valen para otros datos: cada hallazgo de tu EDA lo tienes que medir tú.

**Regla de oro del día:** el EDA no es "hacer gráficos". Es **descubrir qué decisiones hay que
tomar** antes de modelar. Cada hallazgo termina en una decisión escrita con su motivo, y cada
decisión termina en código con una prueba.

**Lo que se te pide para cerrar H1:** ficha aprobada · EDA con **al menos 5 decisiones
justificadas** · partición por la **unidad de análisis correcta**, verificada con una prueba ·
limpieza **reproducible por script**.

---

## 0. Antes de empezar

- Tu dataset está en `data/raw/`. **Ese archivo no se modifica nunca**: toda limpieza se hace en
  código y se guarda aparte en `data/processed/`.
- Si el dataset trae **datos personales** (nombres, documentos, teléfonos, correos), no los
  mires ni los imprimas: elimínalos al cargar (ver sección 4).
- Trabaja en `notebooks/02_eda.ipynb` (esqueleto en tu repo). Verifica tu entorno con
  `python scripts/verificar_entorno.py` si algo no corre.

---

## 1. Las cinco preguntas guía del EDA

### Pregunta 1 · ¿Cuál es la unidad de análisis? ¿Qué representa una fila?

Una fila puede ser un cliente, una transacción, un cliente en un mes, una empresa en un año. De la
respuesta depende **cómo se parte el dato** y cómo se valida el modelo.

```python
import pandas as pd

df = pd.read_csv("data/raw/<archivo>.csv")
print(df.shape)

# ¿Qué columna identifica a la entidad (cliente, paciente, empresa...)?
id_col = "<columna_id>"          # TODO: reemplázala por la tuya
print("filas:", len(df), "| entidades distintas:", df[id_col].nunique())
print(df.groupby(id_col).size().value_counts().head())   # ¿cuántas filas por entidad?
```

**Cómo interpretarlo.** Si `entidades distintas` es mucho menor que `filas`, **una entidad aparece
en varias filas**. Eso es lo más importante que puedes descubrir hoy: la partición será por esa
entidad (sección 4). Anota también si hay una columna de tiempo (mes, fecha): el panel puede tener
un orden.

### Pregunta 2 · ¿Cómo está el objetivo?

```python
target = "<columna_objetivo>"    # TODO

# Clasificación: proporciones de cada clase
print(df[target].value_counts(normalize=True))

# Regresión: forma de la distribución
print(df[target].describe(percentiles=[.01, .25, .5, .75, .99]))
df[target].hist(bins=50)

# ¿La etiqueta es de la entidad o de cada fila? (¿cambia dentro de la misma entidad?)
print(df.groupby(id_col)[target].nunique().value_counts(normalize=True))
```

**Cómo interpretarlo.** En clasificación, ¿qué porcentaje acierta predecir siempre la clase más
frecuente? Esa es tu **línea base** y dice si la exactitud sirve como métrica. Si la etiqueta
cambia dentro de la misma entidad, la etiqueta es de la **fila**, no de la entidad. Si el
objetivo tiene vacíos, decide qué hacer con esas filas.

### Pregunta 3 · ¿Qué tan sucios están los datos y de qué manera?

Hazlo con los chequeos concretos de la **sección 3**. Aquí solo un resumen rápido:

```python
print(df.dtypes.value_counts())                 # ¿tipos mezclados? (número guardado como texto)
print(df.isna().mean().sort_values(ascending=False).head(10))    # vacíos por columna
print("duplicados exactos:", df.duplicated().sum())
```

### Pregunta 4 · ¿Qué variables deberían ser estables y no lo son?

Edad, ocupación, ingreso o la categoría de un cliente **no cambian de un mes al siguiente**. Si en
tus datos cambian, el cambio puede ser ruido o corrupción, y eso se puede reparar con el valor
válido más frecuente **de esa misma entidad**.

```python
# Solo aplica si una entidad aparece en varias filas
candidates = ["<col_1>", "<col_2>", "<col_3>"]    # TODO: variables que deberían ser constantes por entidad
changes = {c: df.groupby(id_col)[c].nunique().gt(1).mean() for c in candidates}
pd.Series(changes, name="% de entidades con más de un valor").sort_values(ascending=False)
```

**Cómo interpretarlo.** Un porcentaje alto no siempre es ruido. Mira **cómo** cambia: si sube
exactamente +1 podría ser la edad (cumpleaños) y es real; si aparece un valor imposible entre
valores normales es corrupción. **No repares nada hasta entender el porqué.**

### Pregunta 5 · ¿Hay algo que suene a fuga de información?

Una **fuga** es una columna que contiene la respuesta o que solo se conoce *después* del hecho que
predices. Cualquier modelo con una fuga parece excelente y en producción no sirve.

```python
# 1) Columnas casi idénticas al objetivo (clasificación)
for c in df.select_dtypes(exclude="number").columns:
    if df[c].nunique() < 30 and c != target:
        print(c, "->", round(pd.crosstab(df[c], df[target], normalize="index").max(axis=1).mean(), 2))

# 2) Columnas numéricas muy correlacionadas con un objetivo numérico
print(df.select_dtypes("number").corrwith(df[target]).abs().sort_values(ascending=False).head(5))
```

**Cómo interpretarlo.** Pregunta de negocio, no de estadística: *¿esta columna ya se conoce en el
momento en que alguien tiene que decidir?* Si la respuesta es "no" o "no sé", es una sospecha de
fuga. No la descartes por intuición: **mídela** con y sin esa columna en la etapa de variables.

---

## 2. Tabla de decisiones: hallazgo → decisión → motivo

Es el **entregable del EDA** (`reports/01_eda.md`). Necesitas **al menos 5 filas**; una fila sin
motivo no cuenta.

| # | Hallazgo (con la cifra que lo prueba) | Decisión | Motivo |
|---|---|---|---|
| 1 | Ej.: "La columna X llega como texto y el N % de sus valores tiene un carácter extra" | Quitar el carácter y convertir a número | Sin eso no se puede calcular ni modelar la columna |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |

**Una decisión buena tiene tres cosas:** una **cifra** que prueba el hallazgo, una acción
**concreta** y un **motivo** que otra persona pueda discutir. "Limpiar los datos" no es una
decisión; "convertir `X` a número y marcar como vacío todo lo que no lo sea porque el 4 % de sus
valores llega como texto" sí lo es.

---

## 3. Chequeos concretos de calidad de datos

Haz **todos** estos chequeos en tu dataset; cada uno puede darte una decisión.

### 3.1 Números guardados como texto
```python
obj_cols = df.select_dtypes(include="object").columns
for c in obj_cols:
    converted = pd.to_numeric(df[c], errors="coerce")
    share_numeric = converted.notna().mean()
    if 0.5 < share_numeric < 1:        # casi todo parece número, pero no del todo
        print(c, "->", round(1 - share_numeric, 3), "no se puede convertir")
        print("   ejemplos:", df.loc[converted.isna() & df[c].notna(), c].value_counts().head(3).to_dict())
```

### 3.2 Valores centinela
Un valor **repetido muchas veces** que no tiene sentido (`-1`, `9999`, `"?"`, `"N/A"`, `"_"`)
suele significar "no disponible".
```python
for c in df.columns:
    top = df[c].value_counts(dropna=False).head(1)
    if top.iloc[0] / len(df) > 0.03 and df[c].nunique() > 20:
        print(c, "->", top.index[0], f"({top.iloc[0] / len(df):.1%})")   # ¿un valor sospechosamente frecuente?
```

### 3.3 Valores imposibles (con percentiles)
Mira dónde los percentiles **se disparan**: un salto brusco tras el p95–p97 indica corrupción,
no una cola natural. También busca **negativos imposibles** (edades, cantidades).
```python
num = df.select_dtypes("number")
print(num.quantile([0.5, 0.9, 0.95, 0.97, 0.99, 1.0]).T.round(2))
print("negativos:", (num < 0).sum()[lambda s: s > 0])
```
Con ese salto fijas un **rango plausible** por columna (y lo que sale del rango pasa a vacío; no
se borra la fila).

### 3.4 Constancia por entidad
Ver pregunta 4. Resultado esperado: qué columnas deberían ser constantes y no lo son.

### 3.5 Vacíos que significan algo
No todo vacío es un dato perdido. A veces significa **"no aplica"** (sin préstamos → tipo de
préstamo vacío). Cruza el vacío con otra columna para entenderlo antes de imputar.
```python
print(pd.crosstab(df["<col_con_vacios>"].isna(), df["<col_relacionada>"]))
```

### 3.6 Duplicados
```python
print("filas duplicadas:", df.duplicated().sum())
print("entidades con filas idénticas:", df.duplicated(subset=[id_col, "<col_tiempo>"]).sum())  # si hay tiempo
```

### 3.7 Fechas y tiempo
¿Las fechas se leen como texto? Conviértelas con `pd.to_datetime(..., errors="coerce")` y mira el
rango (¿fechas del futuro? ¿años imposibles?). Si hay orden temporal, **nunca** uses información
de fechas posteriores a la fila que predices.

### 3.8 Categorías raras y de alta cardinalidad
```python
for c in df.select_dtypes(include="object").columns:
    n = df[c].nunique()
    rare = (df[c].value_counts(normalize=True) < 0.01).sum()
    print(f"{c}: {n} categorías, {rare} con menos de 1 % de las filas")
```
Muchas categorías raras: se agrupan en "otras" dentro del pipeline (no a mano).

### 3.9 Columnas de identidad y datos personales (PII)
Busca columnas con nombres, documentos, teléfonos, correos, direcciones, **identificadores
únicos** (un `id` distinto en cada fila no aporta señal y puede inducir memorización). Esas
columnas **se eliminan al cargar los datos**, antes de cualquier análisis que las imprima.

---

## 4. De la decisión al código

Cada decisión de la tabla se convierte en **una función pequeña en `src/<paquete>/data/`** y en
**al menos una prueba en `tests/`**. El notebook solo orquesta: llama a las funciones y muestra
resultados.

### 4.1 Una decisión como función
```python
# src/<paquete>/data/cleaning.py
import pandas as pd

SENTINELS = {"?", "N/A", "9999"}          # TODO: los tuyos, según el EDA

def to_number(series: pd.Series) -> pd.Series:
    """Convierte texto con basura en número; lo que no se pueda convertir queda vacío."""
    return pd.to_numeric(series.astype("string").str.strip("_"), errors="coerce")
```

### 4.2 La prueba de esa función
```python
# tests/test_cleaning.py
import pandas as pd
from <paquete>.data.cleaning import to_number

def test_to_number_strips_junk_and_keeps_missing():
    result = to_number(pd.Series(["23_", "40", "abc"]))
    assert result.iloc[0] == 23 and result.iloc[1] == 40
    assert pd.isna(result.iloc[2])
```
Regla práctica: **una prueba por decisión**, con un ejemplo mínimo hecho a mano (el caso normal y
el caso sucio).

### 4.3 La partición por la unidad de análisis (la prueba más importante)
Si una entidad aparece en varias filas, **todas sus filas van al mismo lado** de la partición:
```python
# src/<paquete>/data/split.py
from sklearn.model_selection import GroupShuffleSplit

def split_by_group(df, group_col, test_size=0.2, seed=42):
    """Separa entrenamiento y prueba sin repartir ninguna entidad entre los dos lados."""
    splitter = GroupShuffleSplit(n_splits=1, test_size=test_size, random_state=seed)
    train_idx, test_idx = next(splitter.split(df, groups=df[group_col]))
    return df.iloc[train_idx].reset_index(drop=True), df.iloc[test_idx].reset_index(drop=True)
```
```python
# tests/test_split.py
import pandas as pd
from <paquete>.data.split import split_by_group

def test_no_entity_in_two_partitions():
    df = pd.DataFrame({"id_entity": list("AABBCCDDEE"), "x": range(10)})   # 5 entidades x 2 filas
    train, test = split_by_group(df, group_col="id_entity", test_size=0.4)
    assert set(train["id_entity"]).isdisjoint(set(test["id_entity"]))      # ninguna entidad en los dos lados
    assert len(train) + len(test) == len(df)                               # no se pierde ninguna fila
```
**Esa prueba debe fallar si alguien parte por fila.** Compruébalo: cambia temporalmente
`GroupShuffleSplit` por `train_test_split` y mira que falle. Si no falla, la prueba no protege nada.

Si **no** hay entidades repetidas, partir por fila es válido: dilo por escrito en `reports/01_eda.md`
("cada fila es una entidad independiente porque ...").

### 4.4 Reglas del preprocesamiento
- Datos crudos → función de limpieza → datos limpios en `data/processed/`. Se regeneran con el
  notebook 03: **no se versionan**.
- La prueba (test) se guarda y **no se vuelve a mirar** hasta la etapa de validación final.
- Lo que depende de los datos de entrenamiento (medias, medianas, categorías) **va dentro del
  pipeline**, no en la limpieza: así no se filtra información (etapa 4).
- Corre `pytest` antes de dar algo por terminado.

---

## 5. Las 8 preguntas que el instructor hará en los puntos de control

Prepáralas con tu grupo; **las responderá la persona que no escribió el código**.

1. ¿Cuál es la **unidad de análisis** de tu dataset y cómo lo sabes?
2. ¿Qué **porcentaje** acierta la línea base y qué te dice eso de la métrica?
3. ¿Qué columna de tus datos **debería ser estable y no lo es**, y qué decidiste?
4. ¿Qué significa un **vacío** en tu dataset? ¿Es "no aplica", "no se anotó" o "perdido"?
5. ¿Cuál es tu decisión más importante del EDA y **qué cifra la respalda**?
6. ¿Cómo **parte tu código los datos** y qué prueba lo demuestra? ¿Qué pasa si parto por fila?
7. ¿Hay alguna columna que **solo se conozca después** de la decisión que quieres apoyar?
8. ¿Qué **datos personales** traía el dataset y cómo los eliminaste? ¿Dónde está la prueba?

---

## 6. Trampas comunes

| Trampa | Por qué falla | Qué hacer |
|---|---|---|
| Limpiar en el notebook "a mano" | No se reproduce ni se prueba | Función en `src/` + prueba |
| Modificar `data/raw/` | Pierdes el original | Guardar siempre en `data/processed/` |
| Partir por fila cuando hay entidades repetidas | Fuga: el modelo "reconoce" a la entidad | Partición por entidad + prueba |
| Imputar con la media global antes de partir | Fuga con datos de la prueba | Imputar **dentro** del pipeline |
| Borrar filas con valores raros | Pierdes datos y sesgas la muestra | Marcar como vacío e imputar luego |
| Decidir sin cifra | La decisión no se puede discutir | "N % de la columna X ..." |
| Pegar el resultado de Claude sin ejecutarlo | Puede inventar columnas o cifras | Ejecuta y compara con tus propios cálculos |
| Mirar la prueba "solo un momento" | Deja de medir generalización | No se toca hasta la etapa 7 |
| Imprimir datos personales en el notebook | Quedan guardados en el archivo | Eliminar PII al cargar |
| Copiar las decisiones de CreditSight | Son de otro dataset | Úsalo para ver **cómo** razonar, no **qué** decidir |

---

## Referencias del ejemplo

- `material-del-curso/ejemplo-creditsight/notebooks/02_eda.ipynb` · `material-del-curso/ejemplo-creditsight/reports/01_eda.md`: preguntas, hallazgos y tabla de
  decisiones de un panel de crédito.
- `material-del-curso/ejemplo-creditsight/notebooks/03_preprocesamiento.ipynb` · `material-del-curso/ejemplo-creditsight/src/creditsight/data/`: de las
  decisiones a código con pruebas, y la demostración de la fuga por partición.
- `material-del-curso/kit/checklist-revision-ia.md`: cómo revisar lo que genere Claude.
