# Física 1 — LCC, FaMAF (UNC)

Repositorio personal de estudio de **Física 1**, cursada 2026. Reúne el material de la cátedra y, sobre todo, **un apunte teórico propio** que se va escribiendo tema por tema a lo largo de la cursada.

A diferencia de mis otros repos de materias, este no se organiza solo alrededor de los parciales: el centro es el apunte. Los parciales son el calendario; el apunte es el producto.

---

## El apunte

Vive en [`sintesis/fisica-1/`](./sintesis/fisica-1). Es **un solo documento LaTeX** (clase `book`) que acumula un capítulo por tema, en el orden lógico de la materia y no en el orden en que se escribieron.

| Cap. | Tema | Guía | Páginas |
|---|---|---|---|
| **1** | Cinemática en una dimensión | 1 | 3–24 |
| **2** | Dinámica I: las tres leyes de Newton | 2 | 25–37 |
| **3** | Dinámica II: rozamiento y sistemas acoplados | 2 | 38–54 |

Cada capítulo sigue la misma estructura: motivación · marco teórico en bloques, cada uno con su chequeo de comprensión · ejemplos resueltos con andamiaje decreciente · errores comunes · ejercicios en dos niveles.

**El capítulo 1 construye derivada e integral desde cero**, motivadas por la pregunta física, siguiendo el camino del apunte de la cátedra. Es la parte que más costó y la que más rinde: sin eso, la mitad del Práctico 1 no se puede hacer.

### Los resultados de los ejercicios no están en el PDF

Están en los scripts de verificación que acompañan al apunte:

```
sintesis/fisica-1/verificacion-cinematica-1d.py
sintesis/fisica-1/verificacion-dinamica-1.py
sintesis/fisica-1/verificacion-dinamica-2.py
```

Corren con `python <archivo>` y no necesitan nada más que `sympy`. Cada uno resuelve los ejercicios de su capítulo de forma independiente e imprime el razonamiento, no solo el número. Tenerlos separados es deliberado: para ver un resultado hay que ir a buscarlo, que es mejor que tenerlo al lado del enunciado.

### Compilar

```bash
cd sintesis/fisica-1
pdflatex fisica-1.tex && pdflatex fisica-1.tex   # dos pasadas, por el índice
```

---

## Material de la cátedra

| Carpeta | Qué hay |
|---|---|
| [`bibliografia/apunte-catedra/`](./bibliografia/apunte-catedra) | *Introducción a la Física* — Wolfenson, Trincavelli y Serra (FaMAF, 2ª ed. 2021). El texto de los propios docentes. Cubre toda la cinemática y construye el cálculo desde cero |
| [`bibliografia/bibliografia-extra/`](./bibliografia/bibliografia-extra) | Serway & Jewett, *Física para Ciencias e Ingeniería* vol. 2 |
| [`parcial-1/practicos/`](./parcial-1/practicos) | Las 4 guías de prácticos (0 a 3). La 3 es la versión 2025; la de este año todavía no salió |
| [`examenes-viejos/`](./examenes-viejos) | 17 parciales (2009–2025) y 9 finales (2008–2026) |
| [`plantillas/`](./plantillas) | La plantilla LaTeX `resumen-teorico`, compartida con mis otros repos |
| `Cronograma Tentativo Cursado .pdf` | El cronograma oficial de la cursada |

### Un detalle del cronograma que conviene saber

La columna *"Prácticos: Guía N"* del cronograma **no dice qué guía corresponde al tema de esa clase**: dice qué guía se resuelve en la sesión de práctico de ese día, que va **una atrás** de la teórica. Por eso la Clase 2 (Cinemática 1D) figura como "Guía 0" cuando en realidad es la Guía 1, y la Clase 7 (Energía I) figura como "Guía 2" cuando es la 3. El mapeo real sale de los prácticos:

| Práctico | Tema |
|---|---|
| 0 | Magnitudes, unidades y vectores |
| 1 | Cinemática 1D y 2D |
| 2 | Dinámica (incluye gravitación y MAS) |
| 3 | Trabajo, energía y colisiones |

---

## Estado

**Parcial I: 24 de septiembre de 2026** — Guías 0 a 3.

Cobertura del apunte sobre los prácticos:

| Práctico | Resolvibles | Falta |
|---|---|---|
| 0 — Magnitudes y vectores | 0 / 16 | todo |
| 1 — Cinemática | **7 / 15** | 2D, tiro de proyectil y circular |
| 2 — Dinámica | **11 / 19** | circular con fuerzas, MAS, gravitación |
| 3 — Trabajo y energía | 0 / 12 | todo |

Un ejercicio del Práctico 2 (el 12, resortes en serie y paralelo) no lo cubre ninguna de las fuentes disponibles.

### Material de repaso

- [`flashcards/fisica-1.tsv`](./flashcards) — 86 tarjetas, importables en Anki (tipo de nota "Básica", separador Tab). Etiquetadas por familia: `cinematica-1d`, `dinamica-newtoniana`, `calculo-diferencial`, `calculo-integral`, más el examen al que pertenecen. Las de cálculo se pueden repasar sueltas.
- [`mapas-mentales/fisica-1/parcial-i.pdf`](./mapas-mentales/fisica-1) — mapa de los 33 conceptos ya cubiertos, en dos paneles.

### Carpetas por examen

`parcial-1/`, `parcial-2/` y `final/` siguen la misma convención:

| | |
|---|---|
| `practicos/` | consignas oficiales de la cátedra |
| `soluciones/` | resoluciones propias |
| `preparacion/` | plan de estudio, formulario y material de repaso |

`final/` no tiene `practicos/`: se rinde sobre el material de toda la cursada.

---

## Cómo se escribe el apunte

Con [**syntheca**](https://github.com/PedroMVillar/syntheca), un plugin propio para Claude Code que orquesta un pipeline de agentes: concilia las fuentes, calibra el nivel contra una ficha de perfil, imita el formato de ejercicios de la cátedra, redacta, verifica los resultados por código de forma independiente, y recién entonces pasa por un control de calidad que puede rechazar el borrador.

**La infraestructura de ese pipeline no está versionada acá** — está en el `.gitignore`. Concretamente quedan afuera `skills/` (las fuentes ingeridas, el banco de ejercicios y la ficha de perfil), `scripts/`, `mapa-estudio.json` y `_inbox/`. Lo que sí se versiona es el producto: el apunte, las flashcards, los mapas mentales y los scripts de verificación.

También quedan fuera del repo los dos PDF de bibliografía que superan los 50 MB (Alonso & Finn, y Serway vol. 1). Siguen en disco, pero no se versionan.

---

## Política de versionado

Dos reglas conviven, explicadas en [`.gitignore`](./.gitignore):

- **Material de parciales** — solo quedan los PDF finales; el `.tex` que los produjo no se versiona.
- **El apunte** (`sintesis/`, `mapas-mentales/`) — acá el `.tex` **sí** se versiona. Es el activo principal del repo y su fuente no es recuperable.

Los auxiliares de compilación (`.aux`, `.log`, `.toc`, `.out`) y los `outputs/` de previews están ignorados.

---

> **Aviso.** Los exámenes escaneados de `examenes-viejos/` son copias de alumnos y llevan **nombre, DNI y nota** manuscritos en la carátula. Este repositorio está pensado para ser **privado**; no hacerlo público sin antes revisar ese material.

---

*Licenciatura en Ciencias de la Computación — FaMAF, Universidad Nacional de Córdoba.*
