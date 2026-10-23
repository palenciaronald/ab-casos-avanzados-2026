# Guía de instalación

Tiempo estimado: 45–60 minutos. Hazla **antes del primer viernes**; en clase se resuelven los atascos.

Qué vas a dejar listo:
1. VS Code con la extensión de Claude Code.
2. `uv` y Python 3.12.
3. Tu repositorio propio (el de tu grupo) con el kit del curso.
4. El archivo `.env` con la conexión a Databricks.
5. Una prueba que confirma que todo funciona.

> No necesitas saber programar para instalar esto. Sigue los pasos en orden y, si algo falla,
> ve a la sección **Errores comunes** al final.

---

## 1. VS Code

- Descarga e instala **Visual Studio Code**: <https://code.visualstudio.com/>.
- Ábrelo una vez y cierra la pantalla de bienvenida.

## 2. Claude y la extensión de Claude Code

1. Crea una cuenta en <https://claude.ai> si no la tienes. El curso exige Claude con un plan de
   pago individual de nivel básico (ver `desarrollo-con-ia.md`, sección "Cuota y respaldo").
2. En VS Code abre **Extensiones** (`Ctrl+Shift+X` en Windows, `Cmd+Shift+X` en macOS), busca
   **Claude Code** (publicada por Anthropic) e instálala.
3. Abre el panel de Claude Code (icono en la barra lateral) e inicia sesión con tu cuenta.

## 3. Git

- **Windows:** descarga Git desde <https://git-scm.com/download/win> e instálalo con las opciones
  por defecto.
- **macOS:** abre la Terminal y escribe `git --version`; si no está instalado, el sistema ofrece
  instalarlo.

Comprueba: `git --version` debe mostrar un número de versión.

## 4. uv y Python 3.12

`uv` instala Python y los paquetes del curso por ti.

- **Windows (PowerShell):**
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
- **macOS (Terminal):**
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

Cierra y vuelve a abrir la terminal. Comprueba: `uv --version`.

El curso usa **Python 3.12** (no 3.13 ni 3.14: algunas librerías todavía no funcionan en ellas y
Streamlit Cloud usa 3.12 por defecto). `uv` lo descargará solo en el paso 6.

## 5. Tu repositorio y el kit del curso

El proyecto de tu grupo **nace de la rama `base`** del repositorio del curso: trae la plantilla
lista (`src/`, `notebooks/`, `tests/`, `CLAUDE.md`, `especificacion-proyecto.md`…) y el material de
consulta. **No se copian archivos a mano.**

1. Crea una cuenta en <https://github.com> (ver `git-github-basico.md`).
2. **Una persona del grupo** crea un repositorio **público y vacío** (sin README, sin `.gitignore`).
   Público es necesario para desplegar la app gratis.
3. Esa persona clona **solo la rama `base`** y la apunta al repositorio del grupo:

   ```bash
   git clone --branch base --single-branch https://github.com/palenciaronald/ab-casos-avanzados-2026.git mi-proyecto
   cd mi-proyecto
   git remote set-url origin https://github.com/TU-USUARIO/TU-REPOSITORIO.git
   git branch -M main
   git push -u origin main
   ```

4. **Los demás integrantes** clonan el repositorio **del grupo** (no el del curso) y lo abren en VS
   Code (la guía `git-github-basico.md` explica cómo).
5. La carpeta `material-del-curso/` es de **consulta**: se borra antes del hito H3
   (`git rm -r material-del-curso`). El detalle está en `LEEME-PRIMERO.md`.

## 6. Entorno de Python y paquetes

En la terminal de VS Code (`Ctrl+ñ` o menú *Terminal → Nueva terminal*), dentro de la carpeta de
tu repositorio:

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

Cuando termine, el nombre de la terminal empezará con `(.venv)`. Si VS Code pregunta si quieres
usar ese entorno para el proyecto, di que sí.

## 7. Conexión con Databricks (archivo `.env`)

1. Crea una cuenta gratuita en <https://www.databricks.com/learn/free-edition>
   (Databricks Free Edition) y entra a tu espacio de trabajo.
2. Copia `.env.example` como `.env` (**nunca** subas `.env` a GitHub; ya está en `.gitignore`).
3. Elige **una** de las dos opciones y completa el `.env` (son las mismas A y B del archivo `.env.example`):

   **Opción A — perfil del CLI de Databricks:** si instalaste el CLI y ya iniciaste sesión, pon en `.env`
   `PROFILE=` seguido del nombre de la sección `[...]` de tu archivo `~/.databrickscfg`. Necesita el CLI en
   el `PATH`; si no lo tienes, usa la opción B.

   **Opción B — token personal (más simple, recomendada si no instalaste el CLI):**
   en Databricks: tu avatar → *Settings → Developer → Access tokens → Generate new token*.
   Copia el token (solo se muestra una vez) y completa:
   ```
   PYTHONUTF8=1
   DATABRICKS_HOST=https://TU-WORKSPACE.cloud.databricks.com
   DATABRICKS_TOKEN=pega-aqui-tu-token
   MLFLOW_TRACKING_URI=databricks
   MLFLOW_REGISTRY_URI=databricks-uc
   ```
   (comenta con `#` la línea `PROFILE=` y descomenta las de la opción B).

4. `PYTHONUTF8=1` evita un error de caracteres en la consola de Windows (ver errores comunes).

## 8. Prueba final

Con el entorno activado y el `.env` completo, en la raíz del repositorio:

```
python scripts/check_databricks.py
```

(Si copiaste el script a tu repo, usa la ruta donde lo dejaste.) Debe imprimir la conexión, tu
usuario y terminar con **`OK: el seguimiento y el registro funcionan.`** Verás un experimento y un
modelo de prueba en tu Databricks.

Si lo logras, ya puedes trabajar. Si no, anota el mensaje de error completo y revisa abajo.

---

## Errores comunes

### `UnicodeEncodeError: 'charmap' codec can't encode character ...` (Windows)
La consola de Windows usa la codificación cp1252 y MLflow imprime un emoji. El experimento **sí se
registró**; solo falla la impresión. Solución: asegúrate de tener `PYTHONUTF8=1` en `.env`, o
ejecuta antes en PowerShell: `$env:PYTHONUTF8 = "1"`.

### PowerShell muestra un error rojo ("NativeCommandError") justo después de `uv venv`
En Windows PowerShell 5.1, lo que `uv` escribe en su salida de mensajes (por ejemplo
`Using CPython 3.12...`) aparece como error aunque no lo sea. Revisa si el entorno se creó
(`.venv` existe) y continúa. Si un script falla solo por eso, ejecuta los comandos uno por uno.

### `databricks: command not found` / `'databricks' no se reconoce como comando`
El CLI de Databricks no está en el `PATH` (la extensión de VS Code de Databricks lo trae en una
carpeta interna, pero no lo expone). No lo necesitas si usas la **Opción A (token)**. Si prefieres
la Opción B, instala el CLI desde la documentación oficial de Databricks y vuelve a iniciar sesión.

### `uv` no se reconoce tras instalarlo
Cierra todas las terminales y abre una nueva (o reinicia VS Code). Si persiste, reinicia el equipo.

### `Invalid access token` / error 401 o 403
El token está mal copiado, expiró o el `DATABRICKS_HOST` no es el de tu espacio de trabajo. Genera
un token nuevo y revisa que el host empiece con `https://` y no termine en `/`.

### Python 3.13 o 3.14 en lugar de 3.12
Borra la carpeta `.venv` y crea el entorno otra vez con `uv venv --python 3.12`.

### Se me agotó la cuota de Databricks
Free Edition tiene cuota diaria de cómputo. Si se agota, espera al día siguiente o usa MLflow
local como respaldo (la guía `databricks-mlflow.md` lo explica).
