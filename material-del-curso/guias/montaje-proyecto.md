# Montaje del proyecto del grupo (clase 2 · ~50 minutos)

Al terminar esta guía, tu grupo tiene **un repositorio propio, listo para trabajar**: estructura del
curso, entorno de Python, conexión con Databricks (o su respaldo local), la **especificación** del
proyecto llena y un primer *commit* en GitHub.

**Parte de:** una **ficha de caso aprobada** y la instalación del viernes (VS Code, Git, `uv`,
Claude y las cuentas de GitHub y Databricks). Si algo de eso falta, resuélvelo con
`instalacion.md` antes de seguir.

> **Regla de oro:** no avances de un paso al siguiente sin comprobar su casilla de verificación.
> Un paso mal hecho aquí cuesta mucho más tiempo en las clases siguientes.

## Cómo repartirse el trabajo (3–4 personas)

Varios pasos se pueden hacer a la vez. Una propuesta:

| Persona | Pasos |
|---|---|
| **Datos** | 9 (dataset) y 7 (sección 3 de la especificación) |
| **Modelado** | 5 y 6 (`.env` y carpeta de Databricks) |
| **App** | 1 al 4 (repo vacío, clonar la base, nombre del paquete, entorno) |
| **Negocio** | 7 (secciones 1, 2, 4, 5 y 6 de la especificación) y 8 |

Al final, **todos** ejecutan el paso 10 en su propio equipo.

## Tiempos orientativos

| Paso | Qué | Min |
|---|---|---|
| 1 | Repositorio vacío en GitHub | 3 |
| 2 | Clonar la base y apuntarla a tu repo | 7 |
| 3 | Nombre del paquete | 3 |
| 4 | Entorno y paquetes | 7 |
| 5 | Archivo `.env` | 5 |
| 6 | Carpeta de Databricks | 5 |
| 7 | Especificación del proyecto | 10 |
| 8 | Revisar `CLAUDE.md` | 2 |
| 9 | Dataset en `data/raw/` | 3 |
| 10 | Verificar el entorno | 3 |
| 11 | Primer commit y push | 2 |

---

## Paso 1 · Repositorio vacío en GitHub (lo hace **una** persona)

1. En GitHub: **New repository**. Pónle el **nombre del proyecto** (por ejemplo `creditsight`) y
   márcalo como **Public**. **Público** es obligatorio: sin eso no se puede desplegar la app gratis.
2. **No** marques *Add a README file*, ni `.gitignore`, ni licencia: el repositorio debe quedar
   **vacío**. Se va a llenar con la base del curso, y si ya tiene un README el primer `push` se rechaza.
3. Copia su URL (termina en `.git`) y compártela con el grupo.

✔ **Comprobación:** GitHub muestra la página *Quick setup* de un repositorio **vacío**.

## Paso 2 · Clonar la base y apuntarla a tu repositorio

El proyecto **nace de la rama `base`** del repositorio del curso: su raíz es la plantilla (con
`CLAUDE.md`, `especificacion-proyecto.md`, `scripts/`, `src/proyecto/`…) y trae además la carpeta
`material-del-curso/` para consultar. **No hay que copiar nada a mano.**

**La persona del paso 1** (en la carpeta donde guardas tus proyectos; el comando es igual en Windows
PowerShell y en macOS Terminal):

```bash
git clone --branch base --single-branch https://github.com/palenciaronald/ab-casos-avanzados-2026.git mi-proyecto
cd mi-proyecto
git remote set-url origin https://github.com/TU-USUARIO/TU-REPOSITORIO.git
git branch -M main
git push -u origin main
```

- `mi-proyecto` es el nombre de la carpeta en tu equipo: cámbialo si quieres.
- `--single-branch` descarga solo la base, sin el resto del repositorio del curso.
- `remote set-url` hace que tu carpeta deje de apuntar al curso y empiece a apuntar a **tu** repo.
- Cambia `TU-USUARIO/TU-REPOSITORIO` por la URL del paso 1.

Después, ábrelo en VS Code:

```bash
code .
```

Si no tienes el comando `code`, abre la carpeta desde VS Code: *Archivo → Abrir carpeta*.

**Los demás integrantes** clonan el repositorio **del grupo** (no el del curso):

```bash
git clone https://github.com/TU-USUARIO/TU-REPOSITORIO.git
cd TU-REPOSITORIO
code .
```

> Desde que haces el `push`, tu repositorio es **tuyo** y ya no recibe cambios de la base.
> `material-del-curso/` es de consulta: **se borra antes del hito H3** con
> `git rm -r material-del-curso`. Lo mismo vale para `LEEME-PRIMERO.md`.

✔ **Comprobación:** en la raíz de tu repo existen `LEEME-PRIMERO.md`, `CLAUDE.md`,
`especificacion-proyecto.md`, `requirements.txt`, `.gitignore`, `.env.example`, la carpeta
`material-del-curso/` y las carpetas `data/`, `notebooks/`, `src/`, `tests/`, `models/`, `app/`,
`reports/`, `presentacion/` y `scripts/`. En GitHub ves esos mismos archivos.

## Paso 3 · Poner nombre a tu paquete

El código de tu proyecto vive en `src/<nombre>/`. La plantilla trae el nombre genérico `proyecto`:
cámbialo por el de tu proyecto.

**Reglas del nombre:** minúsculas, **sin espacios, sin guiones y sin tildes**, y en inglés si puedes
(`creditsight`, `churnwatch`, `loanrisk`).

- **Windows (PowerShell):** `Rename-Item src\proyecto creditsight`
- **macOS (Terminal):** `mv src/proyecto src/creditsight`

Después, en VS Code usa *Buscar y reemplazar en archivos* (`Ctrl+Shift+H`, en Mac `Cmd+Shift+H`)
para cambiar `src/proyecto/` por `src/<tu-nombre>/` en `CLAUDE.md` y en `README.md`.

✔ **Comprobación:** existe `src/<tu-nombre>/__init__.py` y ya no existe `src/proyecto/`.

## Paso 4 · Entorno de Python y paquetes

En la terminal de VS Code, dentro de tu repo:

- **Windows (PowerShell):**
  ```powershell
  uv venv --python 3.12
  .venv\Scripts\activate
  uv pip install -r requirements.txt
  ```
- **macOS (Terminal):**
  ```bash
  uv venv --python 3.12
  source .venv/bin/activate
  uv pip install -r requirements.txt
  ```

La terminal debe empezar con `(.venv)`. Si VS Code pregunta si quieres usar ese entorno, di que sí.

> En PowerShell puede salir un texto rojo justo después de `uv venv`. Es un falso error de Windows
> PowerShell: revisa que exista la carpeta `.venv` y sigue.

✔ **Comprobación:** `python --version` muestra `Python 3.12.x` y la instalación termina sin errores.

## Paso 5 · El archivo `.env`

El `.env` guarda **tus** credenciales. Nunca se sube a GitHub (ya está en `.gitignore`).

1. Cópialo desde la plantilla:
   - **Windows:** `Copy-Item .env.example .env`
   - **macOS:** `cp .env.example .env`
2. Ábrelo y elige **una** de las dos formas de conectar a Databricks:

   **Opción A — perfil del CLI de Databricks** (si ya iniciaste sesión con el CLI): deja
   `PROFILE=` con el nombre de la sección `[...]` de tu archivo `~/.databrickscfg`.

   **Opción B — token personal** (más simple si no instalaste el CLI): comenta la línea `PROFILE=`
   con `#`, descomenta las líneas de la Opción B y complétalas:
   ```
   DATABRICKS_HOST=https://TU-WORKSPACE.cloud.databricks.com
   DATABRICKS_TOKEN=<tu token personal>
   MLFLOW_TRACKING_URI=databricks
   MLFLOW_REGISTRY_URI=databricks-uc
   ```
   El token se genera en Databricks: tu avatar → *Settings → Developer → Access tokens*.

3. Deja `PYTHONUTF8=1`: evita un error de caracteres en la consola de Windows.
4. Añade **al final** del archivo la carpeta de experimentos (la creas en el paso 6):
   ```
   EXPERIMENT_DIR=/Users/<tu-correo>/<nombre-de-tu-carpeta>
   ```

> El `.env.example` de la plantilla puede no traer la línea `EXPERIMENT_DIR`; añádela a mano.
> No uses comillas ni espacios alrededor del `=`.

✔ **Comprobación:** `.env` existe, no tiene textos de ejemplo (`nombre-de-tu-perfil`, `pega-aqui…`) y
en VS Code aparece **en gris** (señal de que Git lo ignora).

## Paso 6 · Una carpeta de Databricks para el grupo

Los experimentos de tu proyecto deben quedar ordenados en **una carpeta propia**.

1. En Databricks abre **Workspace** (menú de la izquierda).
2. Entra a tu carpeta personal (`Users → <tu correo>`) y crea una carpeta nueva
   (*Create → Folder*, o el menú con los tres puntos). Nómbrala `curso_<nombre-del-proyecto>`.
3. Copia su **ruta completa** (suele mostrarse al pasar el cursor o en el menú de la carpeta;
   si no la ves, verifica en tu cuenta cómo copiarla): tendrá la forma
   `/Users/<tu-correo>/curso_<nombre-del-proyecto>`.
4. Pégala en `.env` como `EXPERIMENT_DIR=...` (paso 5.4).

> **Acuerden en el grupo qué cuenta de Databricks se usa para el seguimiento** (por ejemplo, la de
> quien tiene el rol de *modelado*). Cada integrante puede trabajar en local con
> `MLFLOW_FORCE_LOCAL=1` en su `.env`: el código funciona igual y los resultados no se pierden.

Prueba la conexión (crea un experimento y un modelo de prueba en tu espacio):

```bash
python scripts/check_databricks.py
```

✔ **Comprobación:** imprime la conexión y la línea **`OK: el seguimiento y el registro funcionan.`**
Si no lo logras ahora, **no te detengas**: sigue con `MLFLOW_FORCE_LOCAL=1` y arréglalo después con la
tabla de errores del final.

## Paso 7 · Llenar la especificación del proyecto

`especificacion-proyecto.md` es el documento que **Claude lee antes de generar código**: lo que
escribas aquí manda sobre cualquier otra suposición. Se llena **a partir de tu ficha de caso
aprobada**, sección por sección:

| Sección de la especificación | De dónde sale |
|---|---|
| **1. Grupo** | Integrantes y su rol (datos, modelado, app, negocio), nombre de la startup y enlace del repo |
| **2. Caso de negocio** | `business_question` y `business_cost_note` de la ficha |
| **3. Datos** | `dataset_source`, `dataset_rows`, `dataset_columns`, `target`, `problem_type`. **Aquí se declara la unidad de análisis**: ¿una misma entidad aparece en varias filas? Si sí, la partición será **por esa entidad** |
| **4. Métrica** | `primary_metric` de la ficha, por qué esa, métricas secundarias y la **línea base** (qué obtiene una regla trivial) |
| **5. Riesgos** | Fuga de información posible, sesgos, calidad de los datos, límites del modelo |
| **6. Entregables y fechas** | Las fechas de H1 a H4 (cierre del fin de semana 1, 2, viernes del 3 y 8 días después) |
| **7. Decisiones** | Se deja vacía: se llena durante el EDA, una fila por decisión con su motivo |

Puedes pedirle ayuda a Claude, **sin dejar que invente**:

> *"Lee `reports/00_caso.md` (mi ficha) y propón el texto de las secciones 2, 3 y 4 de
> `especificacion-proyecto.md`. Usa solo lo que dice la ficha. Si falta algo, déjalo marcado con
> «FALTA» y dime qué necesito decidir."*

✔ **Comprobación:** secciones 1 a 6 completas, sin `_______________` ni filas vacías. Todos los
integrantes la han leído.

## Paso 8 · Revisar `CLAUDE.md`

`CLAUDE.md` son las reglas permanentes de Claude para tu proyecto. **No lo reescribas:** solo
asegúrate de que la ruta del paquete sea la tuya (`src/<tu-nombre>/`, paso 3) y que no quede ninguna
mención a `proyecto`.

✔ **Comprobación:** abre `CLAUDE.md`, busca `proyecto` (Ctrl+F) y no hay referencias a `src/proyecto/`.

## Paso 9 · El dataset en `data/raw/`

1. Descarga el archivo del dataset aprobado (desde Kaggle u otra fuente) y guárdalo en `data/raw/`.
2. **Los datos originales nunca se modifican.** La limpieza se hace por código y escribe en
   `data/processed/`.
3. **No se sube a GitHub.** La plantilla ya lo evita con esta línea del `.gitignore`:
   `data/raw/*`. Quítala **solo** si la licencia permite redistribuir **y** no hay datos
   personales. En tu `README.md` anota **de dónde se descarga** el dataset para que otra persona
   pueda reproducirlo.

✔ **Comprobación:** el archivo está en `data/raw/` y `git status` **no** lo lista.

## Paso 10 · Verificar el entorno

Con el entorno activado, en la raíz del repo:

```bash
python scripts/verificar_entorno.py
```

El script **no cambia nada**: revisa Python, paquetes, `.env`, conexión, estructura, especificación,
Git y datos, y marca cada línea:

| Marca | Significado |
|---|---|
| **OK** | Todo bien |
| **AVISO** | Funciona, pero conviene revisarlo; no bloquea |
| **FALTA** | Hay que arreglarlo antes de seguir |

**Qué hacer con lo que sale con más frecuencia** (los textos son los que imprime el script):

| Lo que verás | Qué hacer |
|---|---|
| `FALTA  Paquetes sin instalar: …` | `uv pip install -r requirements.txt` (con el entorno activado) |
| `FALTA  No existe el archivo .env` | Copia `.env.example` como `.env` (paso 5) |
| `FALTA  .env NO está en .gitignore` | Añade una línea `.env` al `.gitignore`: si lo subes, expones tus credenciales |
| `FALTA  Estructura del repo incompleta: …` | Revisa que clonaste la rama `base` completa (paso 2); el mensaje dice qué falta |
| `FALTA  No hay ningún paquete dentro de src/` | Debe existir `src/<nombre>/__init__.py` (paso 3) |
| `FALTA  La carpeta no es un repositorio de Git` | Clona el repo del grupo (paso 2) o ejecuta `git init` |
| `AVISO  Python 3.x: el curso usa 3.12` | Borra `.venv` y crea el entorno con `uv venv --python 3.12` |
| `AVISO  No parece que el entorno virtual esté activado` | Actívalo (paso 4) |
| `AVISO  .env todavía tiene valores de ejemplo` | Reemplaza los textos de ejemplo por tus datos |
| `AVISO  Databricks sin configurar: se usará MLflow local` | Normal si aún no conectas; el curso sigue igual |
| `AVISO  No conecta con Databricks (…)` | Revisa token, perfil o CLI en el PATH (tabla de errores) |
| `AVISO  No definiste EXPERIMENT_DIR …` | Crea la carpeta (paso 6) y pon su ruta en `.env` |
| `AVISO  especificacion-proyecto.md tiene N campos en blanco` | Termina el paso 7 |
| `AVISO  El repositorio no tiene remoto (origin)` | `git remote add origin <url-del-repo-del-grupo>` (si ya existe, `git remote set-url origin <url>`) |
| `AVISO  data/raw está vacía` | Paso 9 |

✔ **Comprobación:** `Resumen: … 0 por arreglar`. Los avisos de Databricks no bloquean si usas el
respaldo local.

## Paso 11 · Primer commit y push

```bash
git status
git add .
git commit -m "Montaje inicial del proyecto"
git push
```

**Antes del `git add .`, mira la lista de `git status`.** Debe haber archivos de la plantilla, tu
`especificacion-proyecto.md` y tu `CLAUDE.md`. **No debe aparecer**:

| No se sube | Por qué |
|---|---|
| `.env` | Contiene tus credenciales |
| `.venv/` | Es tu entorno local, pesa mucho |
| Archivos de `data/raw/` con licencia dudosa o datos personales | El repo es **público** |
| `kaggle.json` o cualquier token | Credenciales |

> Si ves `.env` en la lista, **no hagas commit**: vuelve al paso 5 y revisa el `.gitignore`. Si ya
> lo subiste, avisa al instructor y **genera un token nuevo** en Databricks: el anterior quedó
> expuesto.

✔ **Comprobación:** en GitHub ves tus carpetas y archivos, y **no** ves `.env`.

---

## Listo cuando…

- [ ] **1.** Tengo un repositorio **público** en GitHub, creado desde la rama `base` (la estructura de la plantilla está en la raíz), y **todos** clonamos el repo **del grupo**.
- [ ] **2.** El paquete de `src/` tiene el **nombre de mi proyecto** y `CLAUDE.md` ya no menciona `proyecto`.
- [ ] **3.** Tengo un entorno con **Python 3.12** y `requirements.txt` instalado.
- [ ] **4.** Mi `.env` está completo y **fuera de Git**.
- [ ] **5.** La conexión con Databricks funciona (`check_databricks.py` termina en **OK**) **o** el grupo acordó usar MLflow local, y **tengo definida** mi carpeta de experimentos.
- [ ] **6.** `especificacion-proyecto.md` está completa (secciones 1 a 6) y todos la leímos.
- [ ] **7.** El dataset está en `data/raw/`, **sin modificar** y sin subirse a GitHub.
- [ ] **8.** `verificar_entorno.py` termina con **0 por arreglar** y mi primer **commit está en GitHub**.

## Errores comunes

| Síntoma | Causa y solución |
|---|---|
| **Error 401 / `Invalid access token` / `Credential was not sent…`** al conectar con Databricks | Token mal copiado o vencido, o `DATABRICKS_HOST` que no es el de tu espacio. Genera un token nuevo; el host debe empezar con `https://` y **no** terminar en `/`. Mientras tanto usa `MLFLOW_FORCE_LOCAL=1` |
| **`databricks: command not found`** o `'databricks' no se reconoce` (el perfil no funciona) | El CLI de Databricks no está en el `PATH`. No lo necesitas si usas la **Opción B (token)**: comenta `PROFILE=` y completa host y token |
| **`UnicodeEncodeError: 'charmap' codec can't encode character …`** (Windows) | La consola usa cp1252. El experimento **sí** se registró. Asegura `PYTHONUTF8=1` en `.env`, o ejecuta antes `$env:PYTHONUTF8 = "1"` en PowerShell |
| **`error: remote origin already exists`** | Usaste `git remote add origin` en una carpeta clonada de la base: ya tiene un `origin` (el del curso). Usa `git remote set-url origin <url-del-repo-del-grupo>` |
| **`git push` rechazado al apuntar al repo del grupo** (`rejected`, `fetch first`, `refusing to merge unrelated histories`) | El repo del grupo **no estaba vacío** (tiene un README u otro archivo creado por GitHub). Si no tiene nada que quieras conservar, usa `git push -u origin main --force` **una sola vez, solo en ese primer push** y solo si el repo es nuevo; si sí tiene algo valioso, `git pull origin main --allow-unrelated-histories`, resuelve conflictos y `git push -u origin main`. Lo más simple: crea un repo **nuevo y vacío** |
| **Hice `git clone` del repo del curso sin `--branch base`** | Tienes la rama equivocada (`main` es el curso anterior). Borra la carpeta y repite el comando del paso 2 con `--branch base --single-branch` |
| **`git push` rechazado** (`rejected`, `non-fast-forward`, `fetch first`) | Alguien subió cambios antes que tú. Ejecuta `git pull --rebase` y luego `git push`. Si pide credenciales, inicia sesión en GitHub desde VS Code (*Cuentas*) |
| **`git push` pide usuario y contraseña** | GitHub ya no acepta contraseña: inicia sesión desde VS Code o usa un token personal de GitHub |
| **Falla `uv pip install -r requirements.txt`** | Casi siempre es Python 3.13 o 3.14: borra `.venv` y crea el entorno con `uv venv --python 3.12`. Si es un error de red, repite el comando |
| **`ModuleNotFoundError`** al ejecutar un script | No está activado el entorno `.venv` (la terminal no empieza con `(.venv)`) o falta instalar paquetes: paso 4 |
| **`.env` aparece en `git status`** | El `.gitignore` no lo cubre: añade la línea `.env`, ejecuta `git rm --cached .env` si ya estaba rastreado y **no hagas commit** hasta que desaparezca |
| **`uv` no se reconoce** | Cierra todas las terminales y abre una nueva; si persiste, reinicia VS Code o el equipo |

Más ayuda: `instalacion.md` (errores de instalación), `databricks-mlflow.md` (conexión y cuota) y
`git-github-basico.md` (Git).
