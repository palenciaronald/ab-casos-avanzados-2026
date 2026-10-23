# Databricks y MLflow: registrar tus experimentos y tu modelo

Esta guía te lleva de cero a tener tus experimentos y tu modelo guardados en Databricks. No
necesitas ser desarrollador: son pasos de configuración y un script de comprobación.

> **La regla que ordena todo:** el **tracking** guarda *ejecuciones* (cada prueba, con sus
> parámetros y métricas). El **registro** guarda *versiones del modelo* (el modelo que eliges
> entre todas esas pruebas). Pruebas muchas, registras pocas.

## 1. Crear tu cuenta en Databricks Free Edition

1. Busca "Databricks Free Edition" en la documentación oficial de Databricks y sigue el enlace de
   registro. Puedes entrar con correo y código de un solo uso, con Google o con Microsoft.
2. Al terminar tendrás un *workspace* (tu espacio de trabajo) con una dirección parecida a
   `https://dbc-xxxxxxxx-xxxx.cloud.databricks.com`. **Guárdala**: es tu `DATABRICKS_HOST`.

Dos cosas que debes saber desde el principio (verifícalas en la documentación oficial, pueden
cambiar):

- Free Edition es para **aprender y practicar, no para uso comercial**. No subas datos de tu
  empresa ni de clientes reales.
- Tiene **límites de uso diario**. Si se agotan, ves el apartado 8: el proyecto sigue funcionando.

## 2. Generar un token personal

El token es como una contraseña que permite a tu computador hablar con tu workspace.

1. Dentro de Databricks, abre el menú de tu usuario (arriba a la derecha) → **Settings**.
2. Busca **Developer** → **Access tokens** → **Manage** → **Generate new token**.
3. Ponle un nombre (por ejemplo `curso-v2`) y una duración corta.
4. **Copia el token ahora**: no se vuelve a mostrar completo.

> **Trátalo como una contraseña.** No lo pegues en el chat de Claude, no lo escribas en un
> notebook y no lo subas a GitHub. Solo va en el archivo `.env`, que Git ignora.

Los nombres exactos de los menús pueden variar; si no los encuentras, busca "personal access
token" en la documentación oficial de Databricks.

## 3. Completar el archivo `.env`

En la raíz de tu proyecto copia `.env.example` como `.env` (mismo nombre, sin `.example`) y completa
**una** de estas dos opciones.

**Opción A: perfil** (si instalaste el CLI de Databricks y ya hiciste login).

```text
PYTHONUTF8=1
PROFILE=nombre-de-tu-perfil
```

`nombre-de-tu-perfil` es el nombre que aparece entre corchetes `[...]` en el archivo
`~/.databrickscfg` (en Windows, `C:\Users\TU_USUARIO\.databrickscfg`).

**Opción B: token** (más simple, no necesita el CLI; es la que recomendamos si dudas).

```text
PYTHONUTF8=1
DATABRICKS_HOST=https://TU-WORKSPACE.cloud.databricks.com
DATABRICKS_TOKEN=pega-aqui-tu-token-personal
MLFLOW_TRACKING_URI=databricks
MLFLOW_REGISTRY_URI=databricks-uc
```

`PYTHONUTF8=1` evita un error típico de Windows (`UnicodeEncodeError`) al imprimir símbolos en la
consola. Déjalo siempre.

## 4. Comprobar la conexión

Con el entorno activado y desde la raíz del repo:

```bash
python scripts/check_databricks.py
```

El script crea un experimento, registra una ejecución con un parámetro y una métrica, y registra un
modelo de juguete. Si todo va bien, termina con:

```text
OK: el seguimiento y el registro funcionan.
```

Si falla, mira el mensaje: casi siempre es un `.env` incompleto, un token vencido o el host mal
escrito. Pega el mensaje completo a Claude y pídele que te ayude a leerlo (ver la guía de
desarrollo con IA).

## 5. Leer la interfaz de experimentos

1. En Databricks, en el menú lateral, entra a **Experiments**.
2. Abre el experimento del script (el nombre empieza por `/Users/tu-correo/...`).
3. Verás una tabla con una fila por **ejecución** (*run*). Cada una guarda:
   - **Parámetros**: lo que elegiste (por ejemplo, la profundidad de un árbol).
   - **Métricas**: el resultado (por ejemplo, el costo o el F1).
   - **Etiquetas** y **artefactos**: notas y archivos asociados.
4. Selecciona varias ejecuciones y usa **Compare** para verlas lado a lado. Ordena por una métrica
   para ver cuál fue la mejor.

Esto responde la pregunta de siempre: *"¿cuál de las 30 pruebas de ayer era la buena?"*

## 6. Ver y registrar un modelo en Unity Catalog

El **registro de modelos** vive en Unity Catalog y guarda **versiones** de un modelo: versión 1,
versión 2, etc., cada una con su historia (qué ejecución la produjo).

- El nombre completo tiene tres partes: `catalogo.esquema.modelo`. En Free Edition lo habitual es
  `workspace.default.<nombre>`, **pero verifica en tu cuenta** qué catálogo y esquema tienes.
- Para ver tus modelos, en el menú lateral abre **Models** (o explora el catálogo y busca el
  esquema).
- El script de comprobación ya registró un modelo de prueba. Ábrelo y verás la **versión 1**, la
  ejecución que la creó y su firma (qué entradas espera).
- Si tu catálogo o esquema son otros, cámbialos en `.env` con `UC_CATALOG` y `UC_SCHEMA`; el módulo
  `material-del-curso/ejemplo-creditsight/src/creditsight/tracking/mlflow_utils.py` los usa para armar el nombre.

| | **Tracking** | **Registro** |
|---|---|---|
| Qué guarda | Ejecuciones (cada prueba) | Versiones de un modelo |
| Cuántas hay | Muchas (decenas o cientos) | Pocas |
| Para qué sirve | Comparar y reproducir pruebas | Saber qué modelo se entrega y cuál versión |
| Cuándo | Mientras experimentas | Cuando eliges el modelo final |

## 7. Qué se registra en el proyecto

Durante el curso sigues este orden:

1. **Optimización**: cada ensayo queda como ejecución (tracking).
2. **Modelo final**: eliges el mejor, lo registras y obtienes una versión.
3. **App**: no consulta Databricks. Usas `models/model.joblib`, un archivo exportado desde esa
   versión (ver la guía de despliegue en Streamlit).

## 8. Si se agota la cuota diaria

Free Edition tiene límites diarios de uso (verifica los detalles en tu cuenta). Si se agotan,
tus datos no se borran, pero no puedes seguir registrando hasta que se renueven.

El proyecto **no se detiene**: el módulo `material-del-curso/ejemplo-creditsight/src/creditsight/tracking/mlflow_utils.py` intenta
conectarse a Databricks y, si no puede, **cae solo a un MLflow local** que guarda todo en una base
SQLite (`material-del-curso/ejemplo-creditsight/mlflow_local.db`). Tus notebooks corren igual y verás en pantalla que quedó en
`local`.

Para ver ese MLflow local, desde la raíz del repo:

```bash
mlflow ui --backend-store-uri sqlite:///ejemplo/mlflow_local.db
```

Abre en el navegador la dirección que imprime (normalmente `http://127.0.0.1:5000`). La interfaz es
muy parecida a la de Databricks.

Si prefieres trabajar siempre en local (por ejemplo, para ahorrar cuota), agrega
`MLFLOW_FORCE_LOCAL=1` a tu `.env`.

## 9. Errores comunes

| Síntoma | Causa probable | Qué hacer |
|---|---|---|
| `UnicodeEncodeError` al terminar un run | Consola de Windows sin UTF-8 | Pon `PYTHONUTF8=1` en `.env` |
| El notebook dice `local` y esperabas Databricks | `.env` vacío, token vencido o sin red | Revisa `.env` y vuelve a correr `check_databricks.py` |
| `databricks` no se reconoce como comando | El CLI no está en el `PATH` | Usa la opción B (token) |
| No encuentras el modelo | Catálogo o esquema distintos | Busca en **Models** o revisa `UC_CATALOG` y `UC_SCHEMA` |
| El token deja de funcionar | Venció | Genera uno nuevo y actualiza `.env` |

## 10. Qué NO tienes que dominar

- Crear clústeres, jobs o bases de datos.
- Escribir código dentro de Databricks: tu código vive en tu repo y se ejecuta en tu computador.
- Model Serving ni Databricks Apps: no son parte del curso. Si tu cuenta los ofrece, son opcionales
  (verifica en tu cuenta qué incluye).
