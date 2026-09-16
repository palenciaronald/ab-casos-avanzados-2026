# Tema 3: NLP — Análisis de Sentimientos
## Fin de semana 3 (2–3 oct)

## 1. Caso de negocio

Un equipo de inversión/research quiere clasificar automáticamente el sentimiento (positivo, negativo, neutral) de noticias y textos financieros, para incorporarlo como señal adicional en su análisis de mercado. El estudiante construye un clasificador de texto que predice el sentimiento de una oración o titular financiero.

## 2. Teoría a repasar el viernes (~1 hora)

- Pipeline de NLP clásico: tokenización, limpieza (stopwords, lowercasing, lematización/stemming)
- Representación de texto: Bag of Words vs. TF-IDF (repaso rápido, ya lo vieron en cursos previos)
- Modelos clásicos para clasificación de texto: regresión logística o Naive Bayes sobre TF-IDF como enfoque base y reproducible sin GPU
- Mención de embeddings y modelos preentrenados (ej. BERT/FinBERT) como siguiente nivel — sin implementarlo en el ejercicio si el tiempo/recursos no dan, pero sí mostrarlo conceptualmente en la demo si el tiempo alcanza
- Métricas para clasificación multiclase de texto: F1 macro (útil cuando las clases están desbalanceadas, como suele pasar con "neutral" siendo mayoritaria en noticias financieras)

## 3. Datasets

- **Viernes (demo del instructor):** [Financial PhraseBank](https://www.kaggle.com/datasets/ankurzing/sentiment-analysis-for-financial-news) — ~4,840 oraciones de noticias financieras, anotadas como positivo/neutral/negativo. Dataset pequeño, limpio y ampliamente usado como benchmark — ideal para mostrar el pipeline completo sin fricción.
- **Sábado (ejercicio del estudiante):** [Financial Sentiment Analysis (FiQA + PhraseBank combinado)](https://www.kaggle.com/datasets/sbhatti/financial-sentiment-analysis) — combina FiQA y Financial PhraseBank en un solo CSV, dataset más grande y con mayor variedad de estilos de texto (noticias + foros financieros), lo que da más textura al ejercicio.

**Descarga:**
```bash
kaggle datasets download -d ankurzing/sentiment-analysis-for-financial-news -p ./data/04-nlp --unzip
kaggle datasets download -d sbhatti/financial-sentiment-analysis -p ./data/04-nlp --unzip
```

## 4. Estructura del notebook demo (viernes)

1. **Introducción** (Markdown) — planteamiento del caso de negocio
2. Carga de datos y exploración: distribución de clases de sentimiento, longitud de textos
3. Preprocesamiento de texto: limpieza, tokenización, remoción de stopwords
4. Vectorización con TF-IDF
5. Entrenamiento de un clasificador (regresión logística o Naive Bayes) sobre el TF-IDF
6. Evaluación: reporte de clasificación, matriz de confusión, F1 macro
7. Análisis cualitativo: revisar algunos casos mal clasificados, ¿por qué se equivocó el modelo?
8. Conclusión de negocio: ¿qué tan confiable sería esta señal de sentimiento para apoyar decisiones de inversión?

## 5. Estructura de la plantilla (sábado)

Misma estructura de 8 secciones que el demo, pero:
- Secciones 1 y 2 resueltas como ejemplo
- Celda de semilla personal (`np.random.seed(cedula)`), usada en el muestreo del dataset y en el `train_test_split`
- Secciones 3 a 7: instrucción en Markdown + celda de código en blanco con comentario guía
- Sección 8 (conclusión): 2–3 preguntas abiertas en Markdown, ej.:
  - "¿En qué tipo de frases se equivoca más el modelo (ironía, negaciones, jerga financiera específica)?"
  - "¿Qué mejorarías del pipeline si tuvieras más tiempo (embeddings, más datos, balanceo de clases)?"

**Nota logística:** dado que este es el último fin de semana y no tiene siguiente sesión para recuperar tiempo, es el caso donde más se debe insistir en que el estudiante entregue el mismo sábado — el diseño de la plantilla (8 secciones, pero con 1 y 2 resueltas) está pensado para que sea completable dentro del bloque de práctica del sábado.
