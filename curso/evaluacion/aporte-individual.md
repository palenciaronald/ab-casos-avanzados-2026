# Aporte individual

El proyecto es de grupo, pero la nota de aporte (criterio D de la rúbrica) es **individual** y se
basa en evidencia que cualquiera puede verificar.

## Roles

Cada integrante tiene un rol principal y apoya en los demás. Se declaran el primer sábado en
`especificacion-proyecto.md`.

| Rol | Responsabilidad principal | Área del repo |
|---|---|---|
| Datos | EDA, limpieza, partición, features | `src/.../data`, `src/.../features`, `reports/00_caso.md`, `reports/01_eda.md` |
| Modelado | Torneo, optimización, validación, registro | `src/.../models`, `src/.../tracking`, `reports/05_torneo.md`, `reports/07_validacion.md` |
| App | Inferencia, app, despliegue | `src/.../inference`, `app/`, `models/` |
| Negocio | Caso, métrica, informe, presentación | `reports/informe_tecnico.md`, `presentacion/` |

Un grupo con menos de cuatro integrantes reparte los roles; ninguna área puede quedar sin responsable.

## Evidencia 1 — Historial del repositorio

- Cada integrante hace **commits con su propia cuenta** de GitHub.
- El evaluador cuenta en qué áreas tiene commits propios (datos, modelado, app, reporte).
- Un commit cuenta si cambia contenido, no solo formato o nombres de archivo.
- Código generado por Claude y confirmado por el integrante **sí cuenta**, siempre que pueda explicarlo (evidencia 2).

## Evidencia 2 — Pregunta oral sobre código generado con IA

En la exposición o en una revisión corta, el evaluador elige un fragmento del proyecto escrito con
ayuda de IA (no uno que el integrante prefiera) y pregunta:
1. ¿Qué hace este fragmento?
2. ¿Por qué está aquí y no de otra forma?
3. ¿Qué pasaría si cambiara esta línea? (el evaluador señala una)

Criterio de respuesta correcta: describe el propósito real, identifica la entrada y la salida, y
anticipa una consecuencia plausible. Se permite una pista; con pista, el nivel baja de 3 a 2.

## Cómo se detecta que un integrante no aportó

Señales objetivas, no opiniones:
- Sin commits propios en todo el proyecto, o solo en archivos de configuración.
- No puede explicar el fragmento elegido ni con pista.
- Su rol declarado no tiene ningún commit suyo en la parte del repo correspondiente.
- Un único integrante concentra más del 70 % de los commits de contenido (señal para revisar, no
  sanción automática: el evaluador pregunta a ambas partes).

## Qué hace el grupo si hay un problema
- Avisar al instructor antes del cierre del FDS 2, para reasignar tareas.
- Quien no aporte recibe nota individual baja en el criterio D, sin afectar la nota del grupo en
  los criterios A–C.
