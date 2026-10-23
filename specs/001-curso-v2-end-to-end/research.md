# Research — Curso v2 (Fase 0)

Formato: Decisión · Razón · Alternativas.

## D1. Versión de Python
- **Decisión**: Python 3.12 en `.venv` creado con `uv`; `requirements.txt` con versiones fijadas.
- **Razón**: Streamlit Community Cloud usa 3.12 por defecto; el equipo del instructor tiene 3.14,
  demasiado nuevo para algunas librerías científicas (p. ej. SHAP). Ya probado: `mlflow 3.17.1` con
  3.12.15 funciona.
- **Alternativas**: 3.14 local (riesgo de incompatibilidades); conda (más pesado para no
  desarrolladores).

## D2. Autenticación en Databricks
- **Decisión**: dos formas, ambas en `.env.example`: (a) **perfil**: `PROFILE=<perfil de ~/.databrickscfg>` con
  `mlflow.set_tracking_uri(f"databricks://{profile}")` y `set_registry_uri(f"databricks-uc://{profile}")`
  (patrón del instructor; dentro de Databricks se detecta con `DATABRICKS_RUNTIME_VERSION` y no hace falta);
  (b) **token**: `DATABRICKS_HOST` + `DATABRICKS_TOKEN`, más simple para estudiantes. `PYTHONUTF8=1` va en `.env`/guía para Windows.
- **Razón**: el CLI de Databricks no está en el `PATH` salvo por la extensión de VS Code; el token
  se configura en minutos. MLflow imprime un emoji que rompe la consola cp1252 sin `PYTHONUTF8=1`
  (verificado: el run se registra pero la salida lanza `UnicodeEncodeError`).
- **Alternativas**: OAuth por CLI para todos (instalación más frágil).

## D3. Tracking y registro
- **Decisión**: `mlflow` con `MLFLOW_TRACKING_URI=databricks` y `MLFLOW_REGISTRY_URI=databricks-uc`;
  modelos registrados como `<catalog>.<schema>.<nombre>`; en Free Edition el catálogo por defecto
  es `workspace` y el esquema `default`.
- **Razón**: probado desde el equipo del instructor: experimento + run + `log_model` con
  `registered_model_name="workspace.default.curso_v2_prueba"` → versión 1 creada.
- **Riesgo R1**: el workspace del instructor tiene catálogos `mlops_*`, así que no es
  representativo de una Free Edition. **Acción**: repetir las pruebas con una cuenta de estudiante
  nueva antes del curso. Model Serving y Databricks Apps: sin confirmar; opcionales.
- **Alternativas**: MLflow local (`mlflow ui`) como respaldo documentado (FR-008) si la cuota
  diaria de Free Edition se agota.

## D4. Unidad de análisis y partición del dataset (hallazgo)
- **Hechos verificados**: 100.000 filas = 12.500 clientes × 8 meses exactos. El `Credit_Score`
  cambia dentro del mismo cliente en el 58 % de los casos (constante solo en el 42 %). Distribución:
  Standard 53,2 %, Poor 29,0 %, Good 17,8 %.
- **Decisión**: la partición entrenamiento/validación/prueba y la validación cruzada MUST ser **por
  cliente** (`GroupKFold`/`StratifiedGroupKFold`), nunca por fila. El ejemplo MUST documentar la
  decisión de unidad de análisis (cliente-mes vs. cliente) y por qué.
- **Razón**: una partición por fila pone meses del mismo cliente en train y test y infla la
  métrica. Es un caso de fuga de nivel senior que los estudiantes no practicaron.
- **Alternativas**: agregar a un registro por cliente (pierde la dinámica mensual; se discute en el
  ejemplo como variante).

## D5. Calidad de datos y datos personales
- **Hechos verificados**: ~1–7 % de varias columnas numéricas llega como texto con basura
  (`Annual_Income` 7,0 %, `Age` 4,9 %, `Num_of_Loan` 4,8 %, `Amount_invested_monthly` 4,3 %…);
  `Occupation` con marcador de basura 7,1 %; `Credit_Mix` = `_` 20,2 %; `Payment_Behaviour`
  basura 7,6 %; `Age` fuera de 14–100 en 2,8 %; `Credit_History_Age` con formato "22 Years and 1
  Months" y 9 % de nulos.
- **Decisión**: `Name`, `SSN` y `ID` se eliminan al inicio y se explica por qué (datos personales,
  aunque sean sintéticos). La limpieza va en `src/creditsight/data/` como código testeado, no
  inline en notebooks.
- **Hipótesis a probar en el ejemplo (no afirmada)**: `Credit_Mix` podría ser casi una
  reformulación del objetivo; el ejemplo MUST medir su aporte con y sin ella.

## D6. La app no consulta Databricks
- **Decisión**: la app Streamlit carga el modelo final desde un archivo `.joblib` dentro del repo
  (más la ficha del modelo), no desde el registro de Databricks.
- **Razón**: Streamlit Community Cloud no tiene el login OAuth ni el token de Databricks, y no
  conviene poner credenciales en la nube; además la cuota de Free Edition no debe afectar a la
  app. El registro en Databricks sigue siendo el sistema de verdad del modelo (el archivo se
  exporta desde ahí en el paso de inferencia).
- **Alternativas**: leer del registro con un token en los *secrets* de Streamlit (acopla la app a
  la cuota y a una credencial personal).

## D7. Despliegue de la app
- **Decisión**: Streamlit Community Cloud desde este repo público de GitHub (`ejemplo/app/streamlit_app.py`
  como entrypoint), con `requirements.txt` en la raíz y Python 3.12 (opción "Advanced settings").
- **Razón**: gratuito; la documentación oficial indica repos privados vía clave de despliegue,
  pero una fuente de terceros menciona un único repo privado en el plan gratuito (sin verificar
  oficialmente) → se usan repos públicos.
- **Alternativas**: Hugging Face Spaces (otra cuenta más); Databricks Apps (sin confirmar en
  Free Edition).

## D8. Redistribución del dataset
- **Decisión**: el CSV de 31 MB ya está en `data/` de este repo público; verificar la licencia de
  Kaggle. Si no permite redistribuir, retirarlo del seguimiento y documentar la descarga.
- **Razón**: el `.gitignore` de la v1 ya advierte revisar licencias antes de redistribuir.

## D9. Diapositivas
- **Decisión**: Markdown con Marp como fuente (`.md`), HTML versionado, PPTX/PDF bajo demanda; la
  presentación ejecutiva del ejemplo de ≤5 diapositivas se exporta a PPTX.
- **Razón**: coincide con la v1 (`ppts/README.md`); el diff es legible y los subagentes escriben
  Markdown.

## D10. Qué se hace con `specs/`, `.specify/` y `.claude/`
- **Decisión**: `.specify/` y `.claude/` siguen ignorados. Los estudiantes de esta edición siguen solo
  la rama `v2` (cada grupo trabaja en su propio repo, con una rama); `main` y `v1` quedan para el grupo
  anterior. Antes de compartir `v2` se decide si `specs/` queda visible (T065).
- **Razón**: `specs/` es útil como ejemplo de desarrollo guiado por especificaciones, pero incluye
  decisiones internas (riesgos, ponderación de rúbrica en borrador).

## D11. Retirada del material v1
- **Decisión**: los estudiantes de esta edición no usan nada de la v1, así que se borra en la rama `v2` durante la implementación, después de que exista el
  reemplazo: `ppts/`, `notebooks/`, `INSTRUCCIONES_ENTREGA.md`, `requirements.txt`. Se conservan
  `data/`, `HOJA_DE_RUTA.md` y `hoja-de-ruta/` (actualizar), y el README se reescribe. La v1 sigue
  íntegra en la rama `v1` y el tag `v1.0`.

## D12. Asistente de IA
- **Decisión**: Claude vía VS Code + extensión Claude Code; el kit usa `CLAUDE.md` como archivo de
  instrucciones; la guía incluye una sección de gasto de cuota (prompts específicos).
- **Riesgo R2**: los límites del plan básico pueden afectar los sábados de trabajo intenso.
  **Acción**: verificar qué incluye hoy el plan y qué hacer sin cuota (política de respaldo).

## D13. Verificación reproducible
- **Decisión**: cada etapa del ejemplo tiene un script `verify_stage` que crea un entorno limpio
  (`uv venv`), instala `requirements.txt` y ejecuta la etapa con `nbconvert`; las funciones de
  `src/` tienen pruebas `pytest`.
- **Razón**: SC-001 exige que una persona ajena reproduzca el ejemplo sin ayuda del autor.

## Riesgos abiertos
| ID | Riesgo | Mitigación |
|---|---|---|
| R1 | Free Edition de estudiante distinta del workspace del instructor | Probar con cuenta nueva antes del curso; respaldo con MLflow local |
| R2 | Cuota del plan básico de Claude | Guía de gasto; política de respaldo |
| R3 | Cuota diaria de Databricks con muchos grupos el mismo sábado | Optimización pesada con pocos trials; tracking local como respaldo |
| R4 | Licencia del dataset | Verificar antes de publicar el repo (el CSV ya está en `data/`) |
| R5 | Despliegue de la app en un viernes | Esqueleto de la app desde el FDS 2 |

## Verificación R1 (T009) — PENDIENTE
- No se pudo hacer desde el equipo del instructor: requiere una cuenta **nueva** de Databricks Free Edition.
- Acción del instructor: crear la cuenta (o pedir a un estudiante), completar `.env` según `.env.example`
  y ejecutar `python ejemplo/scripts/check_databricks.py`. Anotar aquí: ¿corre?, ¿catálogo/esquema por
  defecto?, límites de cuota, y si Model Serving y Databricks Apps están disponibles.
- Resultado en el workspace del instructor (no representativo): conexión por perfil OK, experimento OK,
  registro en `workspace.default.curso_v2_prueba` OK.

## Licencia del dataset (T008) — PENDIENTE
- Búsqueda web y lectura de la página de Kaggle (`parisrohan/credit-score-classification`) no devolvieron
  el campo de licencia; no se pudo confirmar.
- Acción del instructor: abrir la página del dataset en Kaggle y copiar aquí el campo **License**.
- Contexto: el CSV ya está en `data/01-clasificacion/` de este repo público (heredado de la v1).
  Si la licencia no permite redistribuir, retirarlo del seguimiento (`git rm --cached`) y documentar
  la descarga en `data/README.md`.

## Plan de Claude (T010) — HECHO con salvedad
- Fuentes: página de Anthropic sobre el uso del plan Pro y guías de terceros. El plan Pro incluye Claude
  Code; la cuota se comparte con el chat; hay ventana de 5 horas y posibles topes semanales. Las cifras
  exactas de mensajes varían y no se verificaron con Anthropic; la guía no las promete.
- Política de respaldo redactada en `curso/guias/desarrollo-con-ia.md` (sección "Cuota y respaldo").
