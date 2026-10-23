# Checklist: revisar lo que generó la IA

Úsalo **antes de aceptar** cualquier cambio. Si respondes "no" a algo, corrige o pregunta antes de seguir.

## Funciona
- [ ] ¿Corre desde cero (reinicia el kernel y ejecuta todo, o crea un entorno nuevo)?
- [ ] ¿Pasan las pruebas (`pytest`)?
- [ ] ¿Obtuve el mismo resultado al repetirlo?

## Datos y modelo
- [ ] ¿Alguna información del conjunto de prueba (o del futuro) llega al entrenamiento?
- [ ] ¿La partición es por la unidad correcta (por cliente/entidad si se repite)?
- [ ] ¿El preprocesamiento está dentro de un `Pipeline` ajustado solo con entrenamiento?
- [ ] ¿El conjunto de prueba se abrió una sola vez y solo al final?
- [ ] ¿La métrica refleja el costo de equivocarse en mi caso?
- [ ] ¿Comparé contra una línea base trivial?

## Seguridad y privacidad
- [ ] ¿Hay tokens, contraseñas o el archivo `.env` en el código o en lo que voy a subir?
- [ ] ¿Quedaron nombres, documentos de identidad u otros datos personales en el repo?
- [ ] ¿`git status` muestra solo lo que quiero subir?

## Entendimiento
- [ ] ¿Entiendo qué hace cada función nueva?
- [ ] ¿Puedo explicar por qué se eligió este modelo / esta variable / este umbral?
- [ ] ¿Puedo explicarle esto a mi grupo y al instructor **sin mirar el código**?

## Respeta el proyecto
- [ ] ¿Cumple la estructura del repositorio y los nombres (identificadores en inglés)?
- [ ] ¿La lógica reutilizable está en `src/` y los notebooks solo orquestan?
- [ ] ¿Escribí la decisión y su motivo en `reports/`?

## Señales de que la IA se equivocó
- Números "demasiado buenos" (precisión casi perfecta): sospecha de fuga de información.
- Resultados sin que se haya ejecutado nada, o gráficos que no corresponden a tus datos.
- Librerías o funciones que no existen o que da error al importar.
- Cambios en archivos que no pediste.
