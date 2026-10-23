# Desarrollo con IA para no desarrolladores

Esta guía te enseña a programar con Claude sin ser desarrollador. Funciona igual para el código
modular, las pruebas y la app. La regla del curso es una: **cada integrante debe poder explicar el
código que la IA generó.**

## 1. El flujo: pedir → revisar → probar → corregir

1. **Pedir.** Una tarea pequeña, con el archivo exacto, el resultado esperado y las restricciones.
2. **Revisar.** Lee lo que hizo. Usa `kit-estudiante/checklist-revision-ia.md`.
3. **Probar.** Ejecuta el comando que Claude te dio y compara con el resultado esperado.
4. **Corregir.** Si falla o no te convence, di exactamente qué falló. No repitas el pedido original.

Nunca pases a la tarea siguiente con una anterior sin probar.

## 2. Cómo pedir en pasos pequeños

| Pedido grande (mal) | Pasos pequeños (bien) |
|---|---|
| "Haz el modelo completo" | 1) "Dime en 5 viñetas el plan." 2) "Escribe solo la limpieza de `Age` en `cleaning.py`." 3) "Añade la prueba." 4) "Ahora la partición por cliente." |

Incluye siempre: **el archivo**, **qué debe hacer**, **cómo sabré que funcionó** y **qué no debe
tocar**. Si el resultado es largo, pide "solo la función que cambia".

## 3. Ejemplo con un error provocado

Imagina que pides: *"En `src/proyecto/data/cleaning.py`, convierte la columna `Age` a número."*
Claude escribe:

```python
def clean_age(df):
    df["Age"] = df["Age"].astype(int)
    return df
```

Al ejecutarla con los datos reales aparece:

```text
Traceback (most recent call last):
  File "src/proyecto/data/cleaning.py", line 3, in clean_age
    df["Age"] = df["Age"].astype(int)
ValueError: invalid literal for int() with base 10: '23_'
```

**Cómo leer el traceback** (de abajo hacia arriba):
1. **La última línea** dice qué pasó: `ValueError`, y un valor concreto, `'23_'`.
2. **La línea anterior** dice dónde: `cleaning.py`, línea 3.
3. Conclusión: hay valores con basura (`23_`) en `Age`. No es culpa tuya ni de Claude: los datos
   estaban sucios, y el EDA debía haberlo mostrado.

**Cómo corregir con un buen pedido:**

> "Al ejecutar `clean_age` falla con `ValueError: invalid literal for int() with base 10: '23_'`.
> Haz que quite los caracteres que no sean dígitos, convierta a número, ponga `NaN` si no se
> puede, y recorte edades fuera de 14–100. Añade una prueba con `'23_'`, `'-500'` y `'40'`."

Claude corrige; tú ejecutas `pytest` y confirmas que la prueba pasa. Fíjate en lo que hiciste:
**pegaste el error exacto**, **pediste el resultado esperado** y **pediste una prueba** para que no
vuelva a ocurrir.

## 4. Cómo leer un traceback (resumen)

- Lee **de abajo hacia arriba**.
- Última línea = **qué** falló. Línea de "File ..., line N" más cercana a tu código = **dónde**.
- Copia el mensaje completo a Claude; no lo parafrasees.
- Errores comunes: `ModuleNotFoundError` (falta instalar o estás en otro entorno),
  `KeyError` (la columna no existe o se llama distinto), `FileNotFoundError` (ruta equivocada) y
  `UnicodeEncodeError` en Windows (define `PYTHONUTF8=1` en `.env`).

## 5. Cuándo desconfiar de la IA

- **Resultados demasiado buenos:** una precisión casi perfecta suele ser fuga de información.
- **Afirma sin ejecutar:** "esto debería funcionar" no es una prueba. Ejecútalo.
- **Inventa:** funciones, librerías o columnas que no existen. Si da error al importar o no
  encuentra la columna, no insistas: pide que revise contra tus datos reales.
- **Cambia cosas que no pediste:** revisa `git diff` y rechaza lo que no entiendas.
- **Es seguro de sí mismo y se equivoca igual:** el tono no es evidencia.
- **Datos o secretos:** nunca pegues tokens ni datos personales en la conversación.

Cuando dudes, **pídele que te explique** el código línea por línea y que te diga qué podría
salir mal. Si no lo entiendes después, no lo uses.

## Cuota y respaldo

**Herramienta del curso:** Claude, usado desde VS Code con la extensión de Claude Code. El plan
individual de pago de nivel básico (Pro) incluye Claude Code, y su cuota es **compartida** con el
chat de Claude: lo que gastas en uno lo restas del otro.

**Cómo funcionan los límites (verifica los números en el Centro de ayuda de Anthropic; cambian):**
- Hay una ventana de uso de 5 horas que se renueva de forma móvil, y puede haber topes semanales.
- El número de mensajes depende del tamaño del mensaje, de los archivos adjuntos, de lo larga que
  sea la conversación y del modelo que uses.
- En Claude Code, el comando `/status` muestra tu uso frente al límite del plan.

**Cómo gastar poca cuota**
- Pide una cosa por vez y con el archivo exacto: *"En `src/data/cleaning.py`, convierte `Age` a número"*,
  no *"arregla mi proyecto"*.
- Abre una conversación nueva al cambiar de etapa; las conversaciones largas cuestan más.
- Deja las instrucciones fijas en `CLAUDE.md` (el kit lo trae) en lugar de repetirlas en cada mensaje.
- Revisa el resultado antes de pedir el siguiente cambio.

**Si te quedas sin cuota en plena clase**
1. Espera a que se renueve la ventana y avanza en lo que no necesita IA (leer resultados, escribir
   el reporte, ensayar la presentación).
2. Trabaja en pareja con alguien de tu grupo y turnen las tareas que más IA consumen. Cada uno
   debe poder explicar el código resultante (regla de la rúbrica).
3. Avisa al instructor. Como último recurso se acepta otra herramienta de IA pegando el
   contenido de `CLAUDE.md` al inicio de la conversación; no habrá penalización si lo comunicas.

**Si no puedes contratar el plan** (tarjeta, país, política de tu empresa): avisa al instructor el
primer viernes para acordar una alternativa antes de empezar.

*Fuentes consultadas para esta sección:* [Anthropic — uso del plan Pro](https://support.claude.com/en/articles/8324991-about-claude-s-pro-plan-usage)
y guías de terceros (cifras sin verificar con Anthropic).
