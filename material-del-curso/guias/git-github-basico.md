# Git y GitHub: lo mínimo que necesitas

**Git** guarda el historial de tu proyecto en tu computador. **GitHub** es el sitio web donde se
sube una copia para compartirla y para desplegar la app. No necesitas más que lo de esta guía.

## Vocabulario en una línea
- **Repositorio (repo):** la carpeta de tu proyecto con su historial.
- **Commit:** una "foto" guardada de tus cambios, con un mensaje que explica qué cambió.
- **Push:** subir tus commits a GitHub. **Pull:** traer a tu computador lo que hay en GitHub.
- **Clone:** descargar un repo de GitHub a tu computador por primera vez.

## 1. Cuenta y repositorio público
1. Crea una cuenta en <https://github.com> (usa un nombre de usuario que puedas mostrar).
2. Botón **New repository**: nombre corto del proyecto, visibilidad **Public**, marca
   *Add a README file*. Público es necesario para desplegar tu app gratis en Streamlit.
3. Añade a tus compañeros: *Settings → Collaborators → Add people*.

## 2. Configurar Git (una sola vez)
En la terminal:
```
git config --global user.name "Tu Nombre"
git config --global user.email "tu-correo-de-github@ejemplo.com"
```

## 3. Clonar el repo
En GitHub: botón verde **Code**, copia la dirección HTTPS. En la terminal, en la carpeta donde
guardas tus proyectos:
```
git clone https://github.com/TU-USUARIO/TU-REPO.git
```
Abre la carpeta que se creó con VS Code. La primera vez que subas cambios, GitHub pedirá iniciar
sesión (se abre el navegador); acepta.

## 4. El ciclo diario: add, commit, push
```
git status                      # ¿qué cambió?
git add .                       # prepara todos los cambios
git commit -m "Describe lo que hiciste"
git push                        # sube a GitHub
```
- Haz commits **pequeños y frecuentes**, con un mensaje claro: "Limpia columna Age", no "cambios".
- La rúbrica mira los commits para ver el aporte de cada integrante: haz commits con **tu** cuenta.

## 5. Traer los cambios de tus compañeros
Antes de empezar a trabajar y antes de hacer `push`:
```
git pull
```

## 6. Qué NO subir nunca
- El archivo **`.env`** (contiene tu token). Ya está en `.gitignore`; confirma con `git status`
  que no aparece como archivo nuevo.
- Datos con información personal (nombres, documentos, correos reales).
- La carpeta `.venv/`.

Si subiste un secreto por error, **no basta con borrarlo**: avisa al instructor y genera un token
nuevo en Databricks de inmediato.

## 7. Conflictos: qué hacer
Un conflicto ocurre cuando tú y un compañero cambiaron las mismas líneas del mismo archivo. Al hacer
`git pull` Git avisa `CONFLICT` y marca el archivo así:
```
<<<<<<< HEAD
tu versión
=======
la versión de tu compañero
>>>>>>> origin/main
```
Pasos:
1. Abre el archivo en VS Code: muestra botones **Accept Current / Accept Incoming / Accept Both**.
   Decide con tu compañero cuál versión se queda (o ambas).
2. Borra las marcas `<<<<<<<`, `=======`, `>>>>>>>` si quedaron.
3. Guarda, y luego:
   ```
   git add .
   git commit -m "Resuelve conflicto en NOMBRE-DEL-ARCHIVO"
   git push
   ```

**Para evitarlos:** repártanse los archivos (cada quien trabaja en carpetas distintas según su rol),
haz `git pull` antes de empezar y sube con frecuencia. Los notebooks (`.ipynb`) generan conflictos
muy difíciles de leer: que **una sola persona** edite cada notebook a la vez.

## 8. Si algo sale mal
- Copia el mensaje de error completo y pégalo a Claude diciendo qué comando ejecutaste.
- Antes de usar comandos que borran historial (`reset --hard`, `push --force`), pregunta al
  instructor: pueden perder el trabajo de todo el grupo.
