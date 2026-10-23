---
marp: true
theme: default
paginate: true
header: "Casos Avanzados · Maestría en Ingeniería Analítica"
footer: "Fin de semana 1 · Viernes · Nivelación conceptual"
---

<!-- _class: lead -->
<!-- _paginate: false -->

# De un modelo en un notebook a un producto
## Nivelación conceptual

**Fin de semana 1 · Viernes**

Hilo conductor: **CreditSight**, una startup que decide si aprueba un crédito.

---

# Qué vamos a hacer en este curso

Ya saben **construir** un modelo. Lo que no han hecho todavía es **llevarlo a la calle**.

- Cada grupo monta **una startup**: un caso de negocio, un modelo y una app que alguien puede usar.
- Hoy no repetimos técnica. Hoy ponemos **cuatro palabras** sobre la mesa:
  1. pipeline
  2. proyecto end-to-end
  3. tracking de modelos
  4. despliegue

*Si entienden estas cuatro, el resto del curso es ponerlas en práctica.*

---

# El ejemplo que nos acompaña: CreditSight

> **CreditSight** es una fintech. Cada día recibe solicitudes de crédito y tiene que decidir:
> **¿le doy el crédito a esta persona, sí o no?**

- Equivocarse en un sentido **cuesta dinero**: se presta a quien no paga.
- Equivocarse en el otro **también**: se pierde un buen cliente.
- Un modelo ayuda a decidir **mejor y más rápido**, pero no decide solo.

*Todo lo que sigue lo vamos a explicar con este caso.*

---

# 1. ¿Qué es un pipeline?

Una **receta escrita que siempre se ejecuta igual**, de los datos crudos a la predicción.

```
datos crudos → limpiar → transformar → modelo → predicción
```

- Sin pipeline: cada vez que alguien usa el modelo, repite los pasos **a mano**… y se equivoca.
- Con pipeline: la **misma receta** corre hoy, mañana y dentro de la app.

**En CreditSight:** cuando un cliente llena el formulario, sus datos pasan por **exactamente
los mismos pasos** con los que se entrenó el modelo.

*Ya lo usaron en el curso anterior. Aquí lo importante es **por qué**: sin él, no hay producto.*

---

# 2. ¿Qué es un proyecto end-to-end?

Un proyecto que cubre **todo el camino**, desde la pregunta de negocio hasta alguien usando el resultado.

| Etapa | Pregunta que responde |
|---|---|
| Caso de negocio | ¿Qué decisión mejora esto y cuánto cuesta equivocarse? |
| Datos y modelo | ¿Con qué datos y qué modelo? |
| Validación | ¿Cuánto puedo confiar en el resultado? |
| Registro | ¿Qué versión es la buena y cómo la recupero? |
| App | ¿Cómo la usa una persona que no programa? |
| Reporte y exposición | ¿Cómo lo explico a quien decide? |

**Un modelo con buena métrica pero sin las otras filas no es un producto.**

---

# El camino completo del curso

```
caso → datos → modelo → optimización → validación → registro → app → reporte
 FDS 1  FDS 1    FDS 2     FDS 2         FDS 2       FDS 2    FDS 3   FDS 3
```

- **Fin de semana 1:** el caso de negocio, entender los datos y prepararlos.
- **Fin de semana 2:** modelar, optimizar, validar y registrar.
- **Fin de semana 3:** desplegar la app, presentar y exponer.

Cada fin de semana termina con un **hito entregable**. No hay sorpresas al final.

---

# 3. Tracking de modelos: el problema

> Es lunes. Tu jefe pregunta:
> **«¿Cuál de las 30 pruebas de ayer era la buena?»**

- ¿Con qué parámetros se hizo?
- ¿Qué métrica dio?
- ¿Con qué versión de los datos y del código?
- ¿Puedes **repetirla** y obtener lo mismo?

Si la respuesta es «déjame revisar mis notebooks…», **tienes un problema**.
En riesgo crediticio ese problema se llama **no poder defender una decisión**.

---

# 3. Tracking de modelos: para qué sirve

**Tracking** = un cuaderno de laboratorio automático. Cada prueba (*run*) guarda sus parámetros,
sus métricas y su resultado.

1. **Comparar:** una tabla ordenada te dice cuál prueba fue la mejor y por qué.
2. **Reproducir:** otra persona, o tú en seis meses, recupera el mismo resultado.
3. **Auditar:** cuando preguntan «¿por qué elegiste este modelo?», la respuesta está registrada.
4. **Entregar:** el modelo elegido pasa a un **registro** con versión; así sabes qué versión usa la app.

*Con pocas pruebas parece un lujo. Con treinta, es lo que te salva.*

---

# 4. Desplegar un modelo

Un modelo dentro de tu computadora **no ayuda a nadie**. Desplegar es **ponerlo donde otros lo usen**.

- Una **app** con un formulario: la persona escribe los datos y recibe la respuesta.
- Un **enlace público**: cualquiera lo abre desde su navegador.
- Un modelo guardado en **un archivo**: la app lo carga y predice.

**En CreditSight:** el analista de crédito abre la app, ingresa los datos del solicitante y ve
la **recomendación, la probabilidad y por qué**.

*Una buena app también dice **cuándo no confiar**: datos fuera de rango, casos raros.*

---

# Lo que cambia respecto al curso anterior

| Antes | Ahora |
|---|---|
| Un notebook con un buen resultado | Un producto que otra persona usa |
| «Mi mejor prueba fue esta» | «Esta es la versión registrada, y así se obtuvo» |
| La métrica era el final | La métrica es **un criterio de negocio** |
| Trabajo individual | **Grupo** con roles y un caso propio |

**Y una condición:** programarán **con ayuda de IA** (Claude). Lo que genere la IA lo deben
**entender y poder explicar**.

---

# Lo que sigue hoy

1. **Diagnóstico corto** de lo visto en el curso anterior (sin nota, para orientar).
2. **Tecnologías** que vamos a usar y cómo instalarlas.
3. **Formación de grupos** y búsqueda del caso de negocio.
4. **Publicamos la rúbrica** y presentamos el **kit de especificaciones** para trabajar con IA.

**Entregable de hoy:** una **ficha de caso** de su grupo (pregunta de negocio, dataset, métrica,
tipo de problema), que el instructor aprueba antes de avanzar.

---

<!-- _class: lead -->
<!-- _paginate: false -->

# Resumen

**Pipeline** → la receta que siempre corre igual
**End-to-end** → de la pregunta de negocio a alguien usando el resultado
**Tracking** → no perder el rastro de lo que probaste
**Despliegue** → poner el modelo donde otros lo usen

*Ahora, el diagnóstico.*
