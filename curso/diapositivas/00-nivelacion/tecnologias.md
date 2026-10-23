---
marp: true
theme: default
paginate: true
header: "Casos Avanzados · Maestría en Ingeniería Analítica"
footer: "Fin de semana 1 · Viernes · Tecnologías del curso"
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Las herramientas del curso
## Qué hace cada una y qué **no** tienen que dominar

**Fin de semana 1 · Viernes**

---

# El mapa de herramientas

| Herramienta | Para qué la usamos |
|---|---|
| **Python y `.venv`** | Correr el código del proyecto |
| **Git y GitHub** | Guardar y compartir el proyecto |
| **VS Code + Claude Code** | Escribir el proyecto con ayuda de IA |
| **Databricks Free Edition** | Guardar experimentos y modelos |
| **MLflow** | Registrar cada prueba (el *tracking*) |
| **Streamlit** | Construir y publicar la app |

**Idea clave:** no son seis cursos nuevos. Usarán **lo mínimo** de cada una, y la IA hará la
mayor parte del código.

---

# Python y el entorno virtual (`.venv`)

**Qué hace:** un entorno **aislado** donde viven las librerías del proyecto, con las versiones
exactas del archivo `requirements.txt`. Así el proyecto corre igual en tu computador y en la nube.

**Usarán:** crear el entorno, activarlo, instalar con `requirements.txt`.

**No tienen que dominar:** gestión de versiones de Python, empaquetado, nada de configuración avanzada.

> Versión del curso: **Python 3.12**. Si algo no corre, lo primero que se revisa es el entorno.

---

# Git y GitHub

**Qué hace:** Git guarda el **historial** de tu proyecto; GitHub lo aloja en internet para
compartirlo y para que la app se publique desde ahí.

**Usarán:** crear un repositorio **público** del grupo, `clone`, `add`, `commit`, `push`, `pull`.

**No tienen que dominar:** ramas complejas, `rebase`, resolver historiales enredados. Cada grupo
trabaja con **una sola rama**.

> Regla de oro: **nunca** suban el archivo `.env` ni datos personales. El `.gitignore` del kit ya lo evita.

---

# VS Code con la extensión de Claude Code

**Qué hace:** VS Code es el editor; la extensión de Claude Code le permite a Claude **leer tu
proyecto, escribir y corregir código**. Es la herramienta de IA **obligatoria** del curso.

**Usarán:** pedirle a Claude tareas pequeñas y concretas, revisar lo que hizo, ejecutar y corregir.
El archivo `CLAUDE.md` del kit le explica el curso a Claude desde el primer mensaje.

**No tienen que dominar:** programar desde cero. **Sí** tienen que **entender y poder explicar**
lo que la IA generó (se pregunta en la exposición).

> Requiere el plan individual de pago de nivel básico si no tienen cuenta. Hay una guía de cuota.

---

# Databricks Free Edition

**Qué hace:** un espacio en la nube, **gratuito**, donde se guardan los **experimentos** y el
**registro de modelos** del proyecto.

**Usarán:** crear su cuenta, conectarse desde el código con **perfil** o **token**, y mirar la
interfaz de experimentos.

**No tienen que dominar:** clústeres, notebooks en Databricks, SQL, permisos. Tiene **límites de
uso diario** y es **solo para uso no comercial**.

> Si se agota el uso del día, hay un **respaldo local** para no detenerse.

---

# MLflow

**Qué hace:** la librería que **registra cada prueba**: parámetros, métricas y resultado. Es el
*tracking* de hoy. Además guarda el **modelo final con versión**.

**Usarán:** unas pocas funciones, que ya vienen **escritas en el módulo del proyecto**. Abrir la
tabla de ejecuciones para comparar.

**No tienen que dominar:** montar servidores, almacenamiento, configuración interna.

```python
# La idea, sin detalles: cada prueba queda así
mlflow.log_param("max_depth", 6)
mlflow.log_metric("auc", 0.87)
```

---

# Streamlit

**Qué hace:** convierte un archivo de Python en una **página web** con formulario, botones y
resultados. Se publica **gratis** en *Streamlit Community Cloud* desde un repositorio público.

**Usarán:** un formulario con los datos de entrada, la predicción y una explicación sencilla.
Claude generará casi todo el código; ustedes lo **revisan y prueban**.

**No tienen que dominar:** HTML, CSS, JavaScript ni servidores.

> La app **carga el modelo desde un archivo** del repositorio. No consulta Databricks, para no
> poner credenciales en la nube.

---

# Cómo se conecta Databricks: dos opciones

Se configura en el archivo **`.env`** (se copia desde `.env.example`; **nunca se sube a Git**).

**Opción A — perfil** (si instalaron el CLI de Databricks):

```
PROFILE=nombre-de-tu-perfil
```

**Opción B — token personal** (la más simple):

```
DATABRICKS_HOST=https://TU-WORKSPACE.cloud.databricks.com
DATABRICKS_TOKEN=pega-aqui-tu-token-personal
```

En Windows añadan también `PYTHONUTF8=1` para evitar errores al imprimir en la consola.

---

# Comprobar que todo funciona

Con el entorno activado y el `.env` completo:

```
python ejemplo/scripts/check_databricks.py
```

Debe terminar con: **«OK: el seguimiento y el registro funcionan.»**

Si falla, **no lo resuelvan solos durante una hora**: anoten el mensaje de error y pídanle
ayuda a Claude o al instructor.

*La guía de instalación paso a paso está en `curso/guias/instalacion.md`.*

---

<!-- _class: lead -->
<!-- _paginate: false -->

# Resumen

Usarán **lo mínimo** de cada herramienta.
La IA escribe mucho código; ustedes **entienden, revisan y explican**.

Hoy: **instalación guiada** y comprobación de la conexión.
