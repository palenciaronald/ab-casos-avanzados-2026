# De tu app local a Streamlit Community Cloud

Esta guía te lleva de una app que corre en tu computador a un **enlace público** que puedes
compartir en la exposición. Streamlit Community Cloud tiene una versión gratuita; verifica en la
documentación oficial las condiciones vigentes.

## 1. Antes de empezar: qué debe cumplir tu repo

| Requisito | Por qué |
|---|---|
| Repo **público** en GitHub | Streamlit lo lee desde GitHub. Con repos públicos no hay configuraciones extra |
| `requirements.txt` en la **raíz** del repo | Ahí lee Streamlit las librerías que debe instalar |
| `models/model.joblib` **dentro** del repo | La app carga el modelo desde este archivo |
| Tu app corre en local sin errores | Si no corre en tu computador, no correrá en la nube |
| Sin `.env` ni datos personales en el repo | Todo lo que subas a un repo público lo puede ver cualquiera |

Comprueba primero en local, desde la raíz del repo:

```bash
streamlit run app/streamlit_app.py
```

En el repo del ejemplo la ruta es `ejemplo/app/streamlit_app.py`.

## 2. Por qué la app NO consulta Databricks

Tu app en la nube **no tiene** tu token ni tu login de Databricks, y **no debes ponerlos allí**:
si pones credenciales en un repo público o en una app compartida, cualquiera las puede usar. Además,
tu app no debe depender de la cuota diaria de Databricks.

Por eso el flujo es:

1. Registras el modelo final en Databricks (es el registro oficial: la fuente de verdad).
2. Exportas esa versión a un archivo `models/model.joblib`.
3. Subes ese archivo al repo junto con una ficha del modelo (`models/ficha_modelo.md`).
4. La app carga `models/model.joblib`. No hace ninguna llamada a Databricks.

## 3. El archivo `requirements.txt`

Va en la **raíz** del repo y debe listar todas las librerías que usa la app, con versiones fijadas
(`nombre==versión`). Usa las mismas versiones con las que entrenaste, sobre todo `scikit-learn`,
`lightgbm`, `xgboost`, `pandas` y `joblib`: un modelo guardado con una versión puede fallar con otra.

Para ver las versiones que tienes instaladas:

```bash
pip freeze
```

Copia solo las que tu app necesita, no toda la lista. Si no estás seguro, pídele a Claude:
"revisa `app/streamlit_app.py` y `src/` y dime qué librerías necesito en `requirements.txt`".

## 4. Tamaño de archivos

- GitHub avisa o rechaza archivos muy grandes (consulta los límites vigentes en su documentación).
- Si tu `model.joblib` es grande, prueba un modelo más pequeño (menos árboles) o guarda solo lo que
  la app necesita. No subas los datos de entrenamiento: la app no los necesita.
- Revisa el tamaño antes de subir: `ls -lh models/` (macOS/Linux) o mira las propiedades del archivo
  en Windows.

## 5. Subir los archivos a GitHub

Con lo que aprendiste en la guía de Git:

```bash
git add app/ models/ src/ requirements.txt
git commit -m "App lista para desplegar"
git push
```

Después entra a tu repo en GitHub desde el navegador y comprueba que **sí aparecen**
`models/model.joblib`, `requirements.txt` y la app.

> **Si `model.joblib` no aparece en GitHub**, lo más probable es que tu `.gitignore` lo esté
> ignorando. Mira el apartado 8, "Errores comunes".

## 6. Crear la app en Streamlit Community Cloud

1. Entra a Streamlit Community Cloud (busca "Streamlit Community Cloud" en su documentación
   oficial) e inicia sesión con tu cuenta de GitHub. Autoriza el acceso a tus repos.
2. Pulsa **Create app** (o **New app**) y elige el repo, la rama y el archivo principal.
3. **Entrypoint** (la ruta del archivo de la app dentro del repo):
   - En el repo de tu grupo: `app/streamlit_app.py`.
   - En el repo del ejemplo: `ejemplo/app/streamlit_app.py`.
4. Abre **Advanced settings** y elige **Python 3.12**, la misma versión con la que trabajaste.
5. Pulsa **Deploy**. La primera vez tarda unos minutos porque instala las librerías.

Los nombres exactos de los botones pueden cambiar; guíate por la documentación oficial.

## 7. Compartir el enlace

Cuando termine, Streamlit te da una dirección pública. Cópiala y:

- Pégala en el `README.md` de tu repo.
- Ponla en la diapositiva de la app de tu presentación.
- Ábrela en una ventana privada del navegador para comprobar que la ve alguien sin tu sesión.

Las apps pueden "dormirse" si no se usan durante un tiempo (verifica en la documentación oficial
las condiciones vigentes). **Ábrela unos minutos antes de tu exposición** para que esté despierta.

## 8. Errores comunes de despliegue

| Síntoma | Causa probable | Qué hacer |
|---|---|---|
| `ModuleNotFoundError: No module named ...` | Falta una librería en `requirements.txt` | Añádela, haz commit y push; la app se reconstruye |
| Error de instalación al desplegar | Versión inexistente o incompatible con Python 3.12 | Revisa el nombre y la versión en `requirements.txt` |
| `FileNotFoundError: models/model.joblib` | Ruta relativa mal armada, o el archivo no se subió | Ver los dos puntos siguientes |
| El archivo existe en tu computador, no en GitHub | Tu `.gitignore` lo ignora (por ejemplo `*.joblib` o `models/`) | Quita esa regla del `.gitignore` solo para ese archivo y vuelve a hacer `git add` |
| La ruta funciona en local y falla en la nube | La app usa una ruta del computador o depende de desde dónde se ejecuta | Arma la ruta a partir de la ubicación del archivo (`Path(__file__)`), no de la carpeta de trabajo |
| `InconsistentVersionWarning` o error al cargar el modelo | El modelo se guardó con otra versión de scikit-learn o lightgbm | Usa en `requirements.txt` las mismas versiones del entrenamiento |
| Funciona en local y no en la nube, sin otra pista | Distinta versión de Python | Elige Python 3.12 en Advanced settings |
| La app pide un token o falla al conectar | Está intentando consultar Databricks | Quita esa llamada: la app solo carga `model.joblib` |

La regla de oro: **si falla, copia el mensaje completo a Claude** y dile exactamente en qué paso
estabas (ver la guía de desarrollo con IA).

## 9. Ver los registros (logs)

1. Abre tu app en Streamlit Community Cloud.
2. En la esquina inferior derecha de la app desplegada (o en el panel de administración de la app)
   busca la opción de **registros** o **logs**.
3. Léelos de abajo hacia arriba: la última línea suele decir qué falló.

Si no encuentras la opción, busca "app logs" en la documentación oficial de Streamlit.

## 10. Reiniciar la app

- **Reinicio simple:** en el panel de administración de la app, usa **Reboot** (o equivalente).
- **Reconstrucción por cambios:** cada vez que haces `git push` al repo, la app se vuelve a
  desplegar sola. Espera a que termine antes de probar.
- Si cambiaste `requirements.txt` o el modelo, confirma que el `push` se vio en GitHub antes de
  reiniciar.

## 11. Lista de verificación antes de la exposición

- [ ] El enlace abre en una ventana privada y muestra el formulario.
- [ ] Un caso de prueba conocido da una predicción coherente.
- [ ] Un dato inválido muestra un mensaje claro, no un error.
- [ ] No hay token, `.env` ni datos personales en el repo.
- [ ] Abriste la app 10 minutos antes y está despierta.
- [ ] Tienes un plan B: la app corriendo en local y capturas de pantalla.

## 12. Qué NO tienes que dominar

- Servidores, contenedores o Docker.
- Cómo funciona la nube por dentro.
- Streamlit más allá de lo que Claude y el ejemplo del curso te muestran: formulario, botón y
  resultado.
