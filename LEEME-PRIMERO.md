# Lee esto primero

Esta es la **base de tu proyecto**: una plantilla lista para usar y el material del curso. Está
pensada para que **cada grupo la clone una sola vez** y la convierta en su propio repositorio.

## Qué tienes aquí

| Dónde | Qué es |
|---|---|
| La **raíz** de este repositorio | La plantilla de tu proyecto: `src/`, `notebooks/`, `tests/`, `app/`, `reports/`, `scripts/`, `CLAUDE.md`, `especificacion-proyecto.md`, `.env.example`… **Esto es lo que vas a completar** |
| `material-del-curso/guias/` | Instalación, Git, trabajo con IA, Databricks, Streamlit y el montaje del proyecto |
| `material-del-curso/evaluacion/` | Rúbrica, hitos, criterios del dataset, ficha de caso, guía de exposición y aporte individual |
| `material-del-curso/kit/` | Prompts por etapa, checklist de revisión del código de IA y guía de EDA |
| `material-del-curso/presentaciones/` | Las presentaciones de cada clase, para abrir en el navegador |
| `material-del-curso/ejemplo-creditsight/` | El proyecto de ejemplo completo, **solo para consultar** (sus notebooks traen los resultados) |

## Cómo empezar (lo hace una persona por grupo)

1. En GitHub, crea un repositorio **público y vacío** para tu grupo (sin README ni `.gitignore`).
2. En tu equipo, clona **solo esta rama** con el nombre de tu proyecto y apúntala a tu repositorio:

   ```bash
   git clone --branch base --single-branch https://github.com/palenciaronald/ab-casos-avanzados-2026.git mi-proyecto
   cd mi-proyecto
   git remote set-url origin https://github.com/TU-USUARIO/TU-REPOSITORIO.git
   git branch -M main
   git push -u origin main
   ```

3. Los demás integrantes clonan **tu repositorio de grupo** (no este).
4. Sigue la guía `material-del-curso/guias/montaje-proyecto.md`.

> **Importante:** a partir del paso 2 tu repositorio es **tuyo**. Ya no recibe cambios de esta base.
> Si el instructor publica material nuevo, se vuelve a consultar aquí.

## Antes de la entrega

La carpeta `material-del-curso/` es de **consulta**. Antes del hito H3, bórrala de tu repositorio
(`git rm -r material-del-curso`) para que tu repo quede solo con **tu** proyecto. Esta guía
(`LEEME-PRIMERO.md`) también puedes borrarla.

## Lo que nunca debe subirse

Tu archivo `.env` (credenciales) y datos con datos personales o de licencia dudosa. La plantilla ya
trae un `.gitignore` que protege `.env`; el script `scripts/verificar_entorno.py` te avisa si algo falla.
