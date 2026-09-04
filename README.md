# Física 1

Apuntes, prácticos y preparación de exámenes de **Física 1** (LCC — FAMAF, UNC). Repositorio personal de estudio.

A diferencia de mis otros repos de materias, este no se organiza solo alrededor de los parciales: el objetivo central es construir **un apunte teórico propio de toda la materia**, generado con [syntheca](https://github.com/PedroMVillar/syntheca) a partir de la bibliografía real de la cátedra y calibrado a mi perfil académico. Los parciales son la estructura de cursada; el apunte es el producto.

## Exámenes

| | Temas | Prácticos | Soluciones propias | Preparación |
|---|---|---|---|---|
| **[Parcial 1](./parcial-1)** | *— por definir con el cronograma* | — | — | — |
| **[Parcial 2](./parcial-2)** | *— por definir con el cronograma* | — | — | — |
| **[Final](./final)** | *— toda la materia* | — | — | — |

Los prácticos se van subiendo a lo largo de la cursada, por parcial.

## Bibliografía general

Vive en [`bibliografia/`](./bibliografia):

- **Apunte de cátedra** — el texto de referencia del curso.
- **Bibliografía extra** — Serway & Jewett, *Física para Ciencias e Ingeniería* (vols. 1 y 2); Alonso & Finn, *Física vol. 2 — Campos y Ondas*.

Los PDFs son la fuente de consulta humana. Para que syntheca pueda usarlos hay que **ingestarlos** con `/nueva-fuente`, lo que crea una skill por libro en `skills/fuentes/`.

## Exámenes viejos

[`examenes-viejos/`](./examenes-viejos) guarda parciales y finales de años anteriores. Tienen doble uso: consulta directa, y carga a syntheca con `/nuevo-banco-ejercicios` para que los ejercicios generados imiten el formato real de la cátedra.

## El apunte teórico — syntheca

Este repo **es** el workspace de syntheca: el plugin resuelve todas sus rutas relativas a esta carpeta.

| Ruta | Qué es |
|---|---|
| `skills/perfil-academico/SKILL.md` | Mi ficha de lector (4 dimensiones, 12 campos). Calibra cada síntesis. Ya está completa. |
| `skills/fuentes/` | Una skill por libro ingestado. Nunca se fusionan entre sí. |
| `skills/banco-ejercicios/` | Los TPs/parciales/finales reales, para calibrar el formato de los ejercicios. |
| `skills/herramientas/` | Opcional — simulador o lenguaje de la cátedra. Probablemente vacía en Física. |
| `sintesis/` | **El apunte.** LaTeX clase `book`: cada tema es un capítulo nuevo del mismo documento. |
| `flashcards/` | `.tsv` importable a Anki, se generan solas al cerrar cada síntesis. |
| `mapas-mentales/` | Mapa vivo por examen programado. |
| `examenes-prueba/` | Exámenes de práctica generados. |
| `mapa-estudio.json` | Estado acumulado: qué se generó, qué falta, qué conceptos ya salieron. |
| `_inbox/` | Zona de descarga para ingestar material en lote. |

### Orden de arranque

1. `/cargar-programa fisica-1` — pegando el cronograma. Llena `temas_pendientes` y los exámenes programados.
2. `/nueva-fuente bibliografia/apunte-catedra/apunte-catedra-fisica-1.pdf` — y después la complementaria que haga falta. **Un comando por libro.**
3. `/nuevo-banco-ejercicios <archivos> fisica-1 --tipo parcial` — agrupando varios del mismo tipo en una corrida, y cada `--tipo` por separado.
4. `/generar-sintesis "<tema>" --materia fisica-1 --fuentes <a,b>` — el primer capítulo.

> El perfil ya está cargado, así que `/setup-perfil` solo hace falta si algo cambió (`--edit`).

## Convención de carpetas de examen

La misma estructura se repite en cada `parcial-N/` (y en `final/`, sin `practicos/`):

| Carpeta | Qué contiene |
|---|---|
| `practicos/` | Consignas oficiales de los trabajos prácticos de la cátedra |
| `soluciones/` | Resoluciones propias de esos prácticos |
| `preparacion/` | Plan de estudio, formulario y demás material de repaso |

## Política de versionado

Dos reglas conviven, y están explicadas en [`.gitignore`](./.gitignore):

- **Material de parciales** — solo quedan los PDFs finales; el `.tex` que los produjo no se versiona (mismo criterio que uso en Lógica).
- **Apunte de syntheca** (`sintesis/`, `mapas-mentales/`, `examenes-prueba/`) — acá el `.tex` **sí** se versiona. Es el activo principal del repo y su fuente no es recuperable.

La plantilla LaTeX de los resúmenes de parcial (`resumen-teorico`) vive en [`plantillas/`](./plantillas); la del apunte la trae el propio plugin.

<details>
<summary>Árbol completo del repositorio</summary>

```
Fisica 1/
├── bibliografia/
│   ├── apunte-catedra/
│   │   └── apunte-catedra-fisica-1.pdf
│   └── bibliografia-extra/
│       ├── serway-jewett-fisica-vol1.pdf
│       ├── serway-jewett-fisica-vol2.pdf
│       └── alonso-finn-campos-y-ondas-vol2.pdf
├── plantillas/
│   ├── resumen-teorico.cls
│   └── resumen-teorico.sty
├── examenes-viejos/
│   ├── parciales/
│   └── finales/
├── parcial-1/
│   ├── README.md
│   ├── practicos/
│   ├── soluciones/
│   └── preparacion/
├── parcial-2/          (idéntico a parcial-1)
├── final/
│   ├── README.md
│   ├── preparacion/
│   └── soluciones/
│
└── ── workspace syntheca ──
    ├── mapa-estudio.json
    ├── _inbox/
    ├── skills/
    │   ├── perfil-academico/SKILL.md
    │   ├── fuentes/
    │   ├── banco-ejercicios/
    │   └── herramientas/
    ├── sintesis/
    ├── flashcards/
    ├── mapas-mentales/
    └── examenes-prueba/
```

</details>

---

*Materia: Física 1 — Licenciatura en Ciencias de la Computación, FAMAF (UNC).*
