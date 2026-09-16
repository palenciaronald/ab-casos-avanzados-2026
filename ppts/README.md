# Presentaciones de teoría (~1 h por viernes)

Cada tema tiene una PPT de **repaso conceptual** para la primera hora del
viernes, **basada en el libro *An Introduction to Statistical Learning* (ISL)**
(James, Witten, Hastie & Tibshirani), con referencias a los capítulos.

| Tema | Archivo | Base ISL |
|---|---|---|
| 1 · Clasificación | `01-clasificacion/teoria_clasificacion.md` | caps. 2, 4, 8 |
| 2 · Clusterización | `02-clusterizacion/teoria_clusterizacion.md` | cap. 12 |
| 3 · Regresión | `03-regresion/teoria_regresion.md` | caps. 3, 6 |
| 4 · NLP (sentimientos) | `04-nlp/teoria_nlp_sentimientos.md` | cap. 4 (marco) |

## Formato

Están escritas en **Markdown con [Marp](https://marp.app/)**: cada `---` separa
una diapositiva y el encabezado `marp: true` activa el modo presentación. Las
fórmulas usan LaTeX (`$...$`).

## Cómo verlas / exportarlas

**Opción 1 — VS Code:** instala la extensión *Marp for VS Code* y abre el `.md`;
verás la vista previa como presentación y podrás exportar a PDF/HTML/PPTX.

**Opción 2 — Marp CLI** (requiere Node/npx):

```bash
# HTML (presentación en el navegador)
npx @marp-team/marp-cli teoria_clasificacion.md -o teoria_clasificacion.html --html

# PDF
npx @marp-team/marp-cli teoria_clasificacion.md -o teoria_clasificacion.pdf

# PowerPoint editable
npx @marp-team/marp-cli teoria_clasificacion.md -o teoria_clasificacion.pptx
```

> Los archivos generados (`.html`, `.pdf`, `.pptx`) **no se versionan**
> (ver `.gitignore`): se regeneran desde el `.md`.

## Estructura pedagógica de cada PPT

Portada → caso de negocio → agenda con referencias ISL → repaso conceptual
(con notación y fórmulas del libro) → métricas → trampas comunes →
puente a la demo del viernes → cierre con lecturas ISL recomendadas.
