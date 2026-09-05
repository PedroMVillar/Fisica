# Parcial 1

*— Temas por definir. Se completan al cargar el cronograma con `/cargar-programa fisica-1`.*

**Estado:** sin cursar.

## Peso por tema

| Bloque | Práctico | Peso |
|---|---|---|
| *— pendiente* | | |

## Contenido de esta carpeta

- [`practicos/`](./practicos) — consignas oficiales de la cátedra. Se van subiendo durante la cursada.
- [`soluciones/`](./soluciones) — resoluciones propias de esos prácticos, un ejercicio por hoja, con la plantilla `resumen-teorico`.
  - `practico-1-cinematica.pdf` — **Práctico 1 completo (15/15)**. Resuelto con NotebookLM (cuaderno *Fisica 1*, respuestas crudas en `soluciones/input/EjNTp1.md`, prompts en `input/prompts/`) y pasado en limpio. Los números están verificados aparte con `verificacion-practico-1.py` (sympy).
  - `practico-2-dinamica.pdf` — **Práctico 2 completo (19/19)**, mismo flujo (respuestas crudas en `input/EjNTp2.md`, verificación en `verificacion-practico-2.py`). Las figuras de la guía (planos inclinados, poleas, resortes, cono) están redibujadas en TikZ junto con los diagramas de cuerpo aislado.
  - Práctico 3 — pendiente (cuando salga la versión 2026).
  - **Parciales viejos resueltos** (mismo flujo, un problema por hoja, `verificacion-parcial-1-<año>.py` con sympy):
    - `parcial-1-2025.pdf` — 25/09/2025 (3 problemas: pelota con viento, loma + choque elástico + resorte, bloques apilados con polea).
- [`preparacion/`](./preparacion) — plan de estudio, formulario y material de repaso.

## Relación con el apunte

La teoría de estos temas **no vive acá**: vive en el apunte general, en [`sintesis/`](../sintesis), generado con `/generar-sintesis "<tema>" --materia fisica-1`. Esta carpeta es para la práctica y para el material específico de rendir este parcial.

Los parciales viejos de años anteriores están en [`examenes-viejos/parciales/`](../examenes-viejos/parciales).
