# Plataforma de Física 1 — Notas de ejemplo y Guía 2 · Plan de implementación

> **Para trabajadores agénticos:** SUB-SKILL REQUERIDA: usar superpowers:subagent-driven-development (recomendada) o superpowers:executing-plans para implementar este plan tarea por tarea. Los pasos usan sintaxis de casilla (`- [ ]`) para seguimiento.

**Objetivo:** ordenar el índice por tema, sumar dos notas de ejemplo con animaciones que cierran los dos huecos que quedaron de la Guía 1, y escribir los tres ensayos que cubren la Guía 2 completa.

**Arquitectura:** el plan anterior dejó tres ensayos y un motor maduro. Éste agrega **un tipo de página nuevo** —la nota de ejemplo, que resuelve un solo ejercicio a la vista en lugar de construir un concepto—, paga la deuda de estilos antes de escribir cinco páginas más, y le da al motor lo que un diagrama de fuerzas necesita: marco rotado, cuerpos rectangulares y las primitivas de descomposición.

**Stack:** ES modules vanilla, canvas 2D, `node --test` de Node 22, GitHub Pages desde `/docs`.

**Spec:** `plataforma/brief.md`

**Autoridad de diseño:** `plataforma/diseno/Tiro parabolico.dc.html`

## Dos decisiones del dueño, tomadas antes de escribir este plan

**Colores en un diagrama de cuerpo aislado.** Un diagrama lleva peso, normal, rozamiento
y tensión a la vez, y la paleta tiene un solo rojo para "fuerza". La decisión es:
**rojo para cada fuerza que actúa sobre el cuerpo, azul para la resultante de todas
ellas**. Distingue lo que empuja de lo que resulta, que es el salto conceptual del tema,
y no agrega ningún color nuevo.

Esto **acota** la regla global "azul para cinemática, rojo para aceleración y fuerza",
no la reemplaza: la aceleración sigue en rojo, como está hoy en los ensayos de tiro y de
circular, que no se tocan. Si un widget necesitara mostrar la resultante y la
aceleración a la vez —son la misma flecha salvo el factor de la masa— hay que
preguntarle al dueño antes, porque ahí las dos reglas se cruzan.

**Orden del índice.** Por tema, no por orden de construcción: 1 derivada e integral,
2 tiro parabólico, 3 movimiento circular, 4 cuerpo aislado, 5 sistemas acoplados,
6 fuerzas que dependen de la posición, 7 energía. Los conceptos básicos de cinemática en
una dimensión van primero.

La portada de hoy lista seis ensayos y el sexto es `Energía`. Este plan **intercala uno**:
la Guía 2 no termina en las cuerdas y las poleas —tiene resortes, gravitación y
movimiento armónico simple, que son el mismo tema visto tres veces: una fuerza que
depende de dónde está el cuerpo—. Sin ese ensayo, "Guía 2 entera" sería mentira. Así que
el ensayo 6 pasa a ser `Fuerzas que dependen de la posición` y `Energía`, que es de la
Guía 3 y no se escribe acá, pasa a ser el 7.

## Global Constraints

Aplican a todas las tareas.

- **Cero dependencias de runtime** salvo KaTeX por CDN. Nada de `npm install`.
- **Cero build.** Lo que está en el repositorio es lo que sirve el navegador.
- **Los tokens de color son exactamente estos**, y no se inventa ninguno:
  claro `--paper:#fbfaf7` `--band:#f2f0ea` `--ink:#16151a` `--dim:#6a6760`
  `--rule:#dcd8ce` `--blue:#1b4fd4` `--blue-soft:#8aa3e6` `--red:#c02a24`
  `--graph:#8e8a80`; oscuro `--paper:#131316` `--band:#191a1e` `--ink:#eceae4`
  `--dim:#948f86` `--rule:#2e2f35` `--blue:#7aa2ff` `--blue-soft:#3f5694`
  `--red:#ef5f52` `--graph:#6f6c66`. Nunca se escriben literales hex en JS.
- **Reparto semántico:** azul para cinemática y velocidad; rojo para aceleración y para
  cada fuerza que actúa; **azul para la resultante de las fuerzas**; `--graph` para la
  trayectoria.
- **Tipografías:** Source Serif 4 para el contenido, JetBrains Mono para la interfaz.
- **Grilla:** columna de texto `max-width:680px` con `padding:0 24px`, widget
  `max-width:880px` dentro de una franja a todo el ancho.
- **Canvas:** `width:100%`, `aspect-ratio:16/8`, `touch-action:none`.
- **Ningún widget se anima solo al cargar.**
- **Ningún número aparece sin respaldo** en un `verificacion-*.py` del repositorio.
- **Todo widget lleva su frase de "qué mirar"** en su encabezado, en `--dim`.
- **Las rutas se verifican sirviendo `docs/` como raíz**, que es lo que hace GitHub
  Pages. Servir el repositorio entero esconde enlaces rotos: así se escapó un defecto
  crítico en el plan anterior.
- **Al comparar bitmaps**, usar `.superpowers/sdd/2026-09-11-plataforma-guia-1/comparar-bitmaps.mjs`,
  que lanza un proceso de Chrome nuevo por medición. Reusar el proceso da falsos
  "idéntico" aunque el código haya cambiado.
- Nombres en español. Las pruebas corren con `node --test "test/**/*.test.js"` desde la
  raíz del worktree.
- **Los scripts de verificación viven en el repositorio de al lado.** Son
  `../Ejercicios-prácticos/parcial-1/soluciones/verificacion-practico-*.py`, y tres tareas
  de este plan —10, 11 y 15— les agregan bloques. Esos cambios van con su **propio
  commit**, en ese repositorio, y no entran en los commits de la plataforma. Es la única
  escritura fuera de este worktree que el plan autoriza: cualquier otra, se pregunta.

## Estructura de archivos

**Motor, modificados:**

| Archivo | Qué cambia |
|---|---|
| `docs/motor/dibujo.js` | recibe `acotarFlecha` y `marcaDeTope`, hoy atrapadas en un ensayo; suma `bloque`, `suelo`, `arco` y `componentes` |
| `docs/motor/lienzo.js` | acepta `angulo`, para el marco rotado del plano inclinado |
| `docs/motor/widget.js` | `panelesApilados` admite rango horizontal propio por panel |

**Estilos:**

| Archivo | Qué cambia |
|---|---|
| `docs/estilos/base.css` | recibe las ocho clases que hoy son 391 atributos `style` repetidos |

**Páginas nuevas:**

| Archivo | Qué es |
|---|---|
| `docs/ejemplos/la-tierra.html` | nota de ejemplo del ejercicio 12 de la Guía 1 |
| `docs/ejemplos/auto-y-camion.html` | nota de ejemplo del ejercicio 5 de la Guía 1 |
| `docs/ensayos/cuerpo-aislado.html` | ensayo 4, tres widgets, Guía 2 |
| `docs/ensayos/sistemas-acoplados.html` | ensayo 5, dos widgets, Guía 2 |
| `docs/ensayos/fuerzas-de-posicion.html` | ensayo 6, dos widgets, Guía 2 |

**Pruebas:** se extienden `test/dibujo.test.js`, `test/lienzo.test.js` y
`test/widget.test.js`.

## Las dieciséis tareas

| Fase | Tareas | Qué deja |
|---|---|---|
| A — preparar el terreno | 1, 2 | índice por tema, sección de ejemplos, ocho clases de estilo |
| B — las dos notas de ejemplo | 3, 4, 5 | el motor que las notas necesitan, `la-tierra.html`, `auto-y-camion.html` |
| C — el motor de fuerzas | 6, 7, 8 | marco rotado, bloques y suelo, arco y componentes |
| D — ensayo 4 | 9, 10, 11 | `cuerpo-aislado.html`, tres widgets |
| E — ensayo 5 | 12, 13 | `sistemas-acoplados.html`, dos widgets |
| F — ensayo 6 | 14, 15 | `fuerzas-de-posicion.html`, dos widgets |
| G — cerrar | 16 | navegación, portada, README, recorrido completo |

## Qué cubre de la Guía 2, ejercicio por ejercicio

La tabla existe para que la frase "cubre la Guía 2 entera" se pueda auditar en lugar de
creer. Los diecinueve ejercicios del práctico 2 aparecen todos; siete tienen widget y el
resto está tratado en prosa, con sus números, dentro del ensayo que le corresponde.

| Ej. | Tema | Dónde |
|---|---|---|
| 1 | plano inclinado con dos cuerdas | ensayo 4, widget 1 |
| 2, 3 | cuerda sin masa / con masa | ensayo 5, prosa de la sección 01 |
| 4 | plano inclinado + cuerpo colgando | ensayo 5, widget 1 |
| 5 | bloques en contacto | ensayo 5, prosa de la sección 02 |
| 6 | tensión máxima de un hilo | ensayo 4, "Cuatro variantes del mismo dibujo" |
| 7 | tres bloques y dos cuerdas | ensayo 5, widget 2 |
| 8 | rozamiento estático contra una pared | ensayo 4, "Cuatro variantes del mismo dibujo" |
| 9 | ángulo óptimo para arrastrar | ensayo 4, widget 2 |
| 10 | dos bloques atados con rozamientos distintos | ensayo 4, "Cuatro variantes del mismo dibujo" |
| 11 | dinamómetro | ensayo 6, prosa de la sección 01 |
| 12 | resortes en paralelo | ensayo 6, prosa de la sección 01 |
| 13 | círculo vertical, tensión en función del ángulo | ensayo 4, "Cinco variantes del mismo dibujo" |
| 14 | resorte como fuerza centrípeta | ensayo 6, prosa de la sección 01 |
| 15 | punto de fuerza nula Tierra-Luna | ensayo 6, widget 2 |
| 16 | triángulo equilátero de masas | ensayo 6, prosa de la sección 02 |
| 17 | movimiento armónico simple | ensayo 6, widget 1 |
| 18 | péndulo cónico | ensayo 4, widget 3 |
| 19 | un bloque sobre otro, con polea | ensayo 4, "Cuatro variantes del mismo dibujo" |

Lo que este plan **no** hace: la Guía 3 —trabajo, energía, cantidad de movimiento—, que
es el ensayo 7 y queda sin enlace en la portada; y la portada misma, que la diseña el
dueño.

## Qué es una nota de ejemplo

Es un tipo de página nuevo y conviene tener clara la diferencia antes de escribir una.

Un **ensayo** construye un concepto: cuatro widgets, cada uno con su sección, y un
cierre con reglas operativas. Se lee para entender.

Una **nota de ejemplo** resuelve **un** ejercicio a la vista: el enunciado, una
animación que lo hace evidente, el razonamiento en pasos, y el resultado. Se lee para
ver cómo se hace. Tiene **un solo widget**, y ese widget tiene que ser muy bueno,
porque es toda la página.

Estructura, que las dos notas comparten:

1. Encabezado igual al de los ensayos, con el kicker diciendo `EJEMPLO · FÍSICA 1`.
2. El enunciado del ejercicio, citado, en un bloque con borde izquierdo —el mismo que
   los ensayos usan para las fórmulas.
3. Un párrafo que dice qué tiene de difícil o de contraintuitivo.
4. La franja del widget.
5. El razonamiento en pasos numerados, cada uno con el número que sale del script de
   verificación.
6. El resultado, y una frase sobre qué se lleva el lector.
7. El pie, igual al de los ensayos.

---

## Fase A — preparar el terreno

### Tarea 1: El índice por tema y la sección de ejemplos

**Archivos:**
- Modificar: `docs/index.html`

**Interfaces:**
- Consume: nada.
- Produce: la portada ordenada por tema y con una sección de ejemplos vacía, lista para
  que las tareas 4 y 5 le agreguen sus enlaces.

- [ ] **Paso 1: reordenar la lista de ensayos**

Hoy la portada lista los ensayos en el orden en que se fueron construyendo —2, 1, 3, 4,
5, 6— con una línea que lo explica. Pasa a orden temático: **1, 2, 3, 4, 5, 6, 7**, o sea
derivada e integral primero, después tiro parabólico, después movimiento circular, y los
que no existen todavía al final.

Además hay uno más que antes: entre `Sistemas acoplados` y `Energía` se intercala
`Fuerzas que dependen de la posición`, así que `Energía` pasa de ser el ensayo 6 a ser el
7. Las cuatro filas sin enlace quedan:

- `ENSAYO 4` — `Diagrama de cuerpo aislado`
- `ENSAYO 5` — `Sistemas acoplados`
- `ENSAYO 6` — `Fuerzas que dependen de la posición`
- `ENSAYO 7` — `Energía`

Borrá la línea que promete el orden de construcción y reemplazala por una que describa
el orden nuevo, en el mismo estilo y con los mismos valores tipográficos:

```html
<p style="font:400 15px/1.55 'Source Serif 4',Georgia,serif;color:var(--dim);margin:10px 0 0;max-width:36em;text-wrap:pretty">Ordenados por tema: primero el cálculo que la cinemática necesita, después los movimientos, después las fuerzas.</p>
```

Los tres ensayos que existen conservan su enlace; los otros cuatro siguen como `<span>`
en `--dim`, sin enlace. Copiá la fila nueva de las que ya están: misma estructura, mismos
valores tipográficos, `color:var(--dim)` en las dos partes.

- [ ] **Paso 2: agregar la sección de ejemplos**

Después de la lista de ensayos, un segundo bloque con el mismo `<h2>` de sección que usa
`LOS ENSAYOS`, que diga `EJEMPLOS RESUELTOS`, su línea de bajada, y la lista vacía por
ahora. Copiá la estructura del bloque de ensayos tal cual: mismo `<h2>`, mismo párrafo
de bajada, mismas filas.

La bajada:

```html
<p style="font:400 15px/1.55 'Source Serif 4',Georgia,serif;color:var(--dim);margin:10px 0 0;max-width:36em;text-wrap:pretty">Un ejercicio del práctico, resuelto a la vista. Para cuando el concepto ya se entiende y lo que falta es ver cómo se usa.</p>
```

Las dos filas van con la misma forma que las de los ensayos, pero el rótulo mono de la
izquierda dice `EJEMPLO 1` y `EJEMPLO 2` en vez de `ENSAYO N`. Por ahora van **sin
enlace**, como `<span>` en `--dim`, porque las páginas no existen: las tareas 4 y 5 las
enlazan.

- `EJEMPLO 1` — `La Tierra que cae`
- `EJEMPLO 2` — `El auto y el camión`

- [ ] **Paso 3: verificar**

Servir `docs/` como raíz y mirar la portada a 1280 y a 390 px:

```bash
cd docs && python -m http.server 8080 --bind 127.0.0.1
```

Comprobar que el orden sea 1, 2, 3, 4, 5, 6, 7; que los tres enlaces existentes sigan
resolviendo; que la sección nueva se lea con el mismo peso visual que la de ensayos; y
que no haya desborde horizontal a 390 px —usá `Emulation.setDeviceMetricsOverride`,
porque `--window-size` ignora anchos menores a unos 526 px en esta máquina—.

- [ ] **Paso 4: commit**

```bash
git add docs/index.html
git commit -m "feat(plataforma): indice por tema y seccion de ejemplos resueltos"
```

---

### Tarea 2: Las ocho clases de estilo

Los tres ensayos y la portada tienen **391 atributos `style`** con sólo **62 valores
distintos**: el 84 % son repeticiones. `base.css` tiene 25 líneas. Con cuatro páginas
nuevas por venir, esto se paga ahora o se paga cuatro veces más caro después. Y hay una
razón mejor que el ahorro: con clases, un `touch-action:none` olvidado en una página
nueva es **imposible** en vez de invisible.

**Archivos:**
- Modificar: `docs/estilos/base.css`, `docs/index.html`,
  `docs/ensayos/tiro-parabolico.html`, `docs/ensayos/derivada-integral.html`,
  `docs/ensayos/movimiento-circular.html`

**Interfaces:**
- Consume: nada.
- Produce: ocho clases que las cuatro páginas nuevas van a usar desde el principio:
  `.columna`, `.banda`, `.marco-widget`, `.encabezado-widget`, `.boton`,
  `.boton-primario`, `.control`, `.lecturas`.

- [ ] **Paso 1: capturar la referencia antes de tocar nada**

Este refactor no puede cambiar **nada** a la vista, y los canvas no alcanzan para
probarlo: un cambio de CSS puede correr el layout sin tocar un solo píxel de canvas.
Hacen falta las dos medidas.

Con `docs/` servido como raíz, para cada una de las cuatro páginas y a 1280 y 390 px,
guardá fuera del repositorio: el hash del bitmap de cada canvas —con
`.superpowers/sdd/2026-09-11-plataforma-guia-1/comparar-bitmaps.mjs`— y, por el
protocolo DevTools, el `getBoundingClientRect` y el `getComputedStyle` completo de
**todos** los elementos del `<body>`:

```js
// dentro de Runtime.evaluate
[...document.querySelectorAll('body *')].map(el => {
  const r = el.getBoundingClientRect();
  const cs = getComputedStyle(el);
  const props = {};
  for (const p of cs) props[p] = cs.getPropertyValue(p);
  return { tag: el.tagName, id: el.id, rect: [r.x, r.y, r.width, r.height], props };
})
```

- [ ] **Paso 2: escribir las ocho clases en `base.css`**

Cada declaración se copia **textual** del atributo `style` que reemplaza. No es una
oportunidad para mejorar valores: si el resultado difiere en un píxel, el refactor está
mal.

```css
/* Las ocho clases salen de contar los atributos `style` de las cuatro paginas: 391
   atributos con 62 valores distintos. Cada declaracion de aca es una copia textual del
   atributo que reemplaza -- este archivo no decide nada de diseno, solo deja de repetir
   lo que el archivo de diseno ya decidio. */

.columna { max-width: 680px; margin: 0 auto; padding: 0 24px; display: flex; flex-direction: column; gap: 0; }
.columna-final { padding-bottom: 80px; }

.banda { width: 100%; background: var(--band); border-top: 1px solid var(--rule); border-bottom: 1px solid var(--rule); padding: 26px 20px 28px; margin: 30px 0 0; display: flex; justify-content: center; }
.marco-widget { width: 100%; max-width: 880px; display: flex; flex-direction: column; gap: 14px; }

.encabezado-widget { display: flex; align-items: baseline; gap: 10px; flex-wrap: wrap; }

.boton { font-size: 11px; letter-spacing: .08em; text-transform: uppercase; color: var(--dim); background: transparent; border: 1px solid var(--rule); border-radius: 2px; padding: 9px 13px; cursor: pointer; }
.boton-primario { font-size: 11px; letter-spacing: .08em; text-transform: uppercase; color: var(--paper); background: var(--blue); border: none; border-radius: 2px; padding: 9px 16px; cursor: pointer; }

.control { display: flex; flex-direction: column; gap: 5px; }

.lecturas { display: flex; flex-wrap: wrap; gap: 0 26px; border-top: 1px solid var(--rule); padding-top: 12px; font: 400 12px/1.5 'JetBrains Mono', monospace; color: var(--dim); }

canvas { width: 100%; aspect-ratio: 16/8; display: block; touch-action: none; }
```

La regla de `canvas` es la que convierte un olvido en imposible: hoy los doce canvas
repiten esas cuatro declaraciones a mano.

- [ ] **Paso 3: aplicarlas a las cuatro páginas**

Reemplazá el atributo `style` por la clase **sólo donde el valor coincida exactamente**.
Donde un elemento tenga la clase más algo propio —un `flex:1 1 200px` en un control, un
`accent-color:var(--red)` en un slider— dejá la clase y conservá lo propio en el
atributo.

Tres cosas que **no** se tocan en esta tarea: el script bloqueante del `<head>`, los
estilos de tipografía del contenido —los `<p>` y `<h2>`, que varían de bloque a bloque—,
y el `<canvas>` de cada widget salvo para sacarle las cuatro declaraciones que ahora
vienen de la regla de elemento.

- [ ] **Paso 4: verificar que no se movió nada**

Repetí las dos mediciones del paso 1 y compará.

- Los hashes de los doce canvas: **idénticos**, con el control negativo corrido.
- El volcado de rectángulos y estilos computados: **idéntico**, elemento por elemento.
  Esta es la medida que importa: es la única que detecta un layout corrido.

Si alguna difiere, **paralo y decilo** con el elemento y la propiedad que cambió. Una
diferencia acá significa que una clase no es copia textual del atributo que reemplazó.

- [ ] **Paso 5: commit**

```bash
git add docs/estilos/base.css docs/index.html docs/ensayos
git commit -m "refactor(plataforma): ocho clases en vez de 391 atributos style"
```

---

## Fase B — las dos notas de ejemplo

### Tarea 3: Lo que el motor le debe a las dos notas

Tres piezas: dos que ya existen pero viven atrapadas dentro de un ensayo, y una
ampliación chica.

**Archivos:**
- Modificar: `docs/motor/dibujo.js`, `docs/motor/widget.js`,
  `docs/ensayos/movimiento-circular.html`
- Prueba: `test/dibujo.test.js`, `test/widget.test.js`

**Interfaces:**
- Consume: `crearLienzo` con `margen`.
- Produce:
  - `acotarFlecha(dx, dy, tope)` → `[dx, dy, acotada]`, exportada de `dibujo.js`.
  - `marcaDeTope(ctx, x, y, dx, dy, { color })`, exportada de `dibujo.js`.
  - `panelesApilados({ lienzo, margen, hueco, paneles })` donde cada panel puede traer
    su propio `xMin`/`xMax`; si no los trae, hereda los del lienzo de afuera.

- [ ] **Paso 1: escribir las pruebas que fallan**

Al final de `test/dibujo.test.js`:

```js
test('acotarFlecha deja pasar una flecha mas corta que el tope', () => {
  const [dx, dy, acotada] = acotarFlecha(30, 40, 100);
  assert.equal(dx, 30);
  assert.equal(dy, 40);
  assert.equal(acotada, false);
});

test('acotarFlecha recorta al tope y avisa, conservando la direccion', () => {
  const [dx, dy, acotada] = acotarFlecha(300, 400, 100);   // largo 500
  assert.ok(Math.abs(Math.hypot(dx, dy) - 100) < 1e-9);
  assert.ok(Math.abs(dx / dy - 300 / 400) < 1e-12, 'la direccion no cambia');
  assert.equal(acotada, true);
});

test('marcaDeTope dibuja dos trazos perpendiculares a la flecha', () => {
  const c = ctxFalso();
  marcaDeTope(c, 100, 100, 50, 0, { color: '#000' });
  // Dos trazos: dos moveTo y dos lineTo, y los dos verticales porque la flecha es
  // horizontal -- misma x en cada par, distinta y.
  const moves = c.ops.filter(o => o[0] === 'moveTo');
  const lines = c.ops.filter(o => o[0] === 'lineTo');
  assert.equal(moves.length, 2);
  assert.equal(lines.length, 2);
  for (let i = 0; i < 2; i++) {
    assert.ok(Math.abs(moves[i][1] - lines[i][1]) < 1e-9, 'trazo vertical');
    assert.ok(Math.abs(moves[i][2] - lines[i][2]) > 1, 'con largo');
  }
});
```

Al final de `test/widget.test.js`:

```js
test('panelesApilados hereda el rango horizontal del lienzo de afuera', () => {
  const l = crearLienzo({ ancho: 800, alto: 400, xMin: 0, xMax: 10, yMin: 0, yMax: 2,
    margen: { L: 0, R: 0, T: 0, B: 0 } });
  const capas = panelesApilados({
    lienzo: l, margen: { L: 0, R: 0, T: 0, B: 0 }, hueco: 0,
    paneles: [{ yMin: 0, yMax: 1 }, { yMin: -5, yMax: 5 }],
  });
  for (const { lp } of capas) {
    assert.equal(lp.xMin, 0);
    assert.equal(lp.xMax, 10);
  }
});

test('un panel puede pedir su propio rango horizontal', () => {
  const l = crearLienzo({ ancho: 800, alto: 400, xMin: 0, xMax: 10, yMin: 0, yMax: 2,
    margen: { L: 0, R: 0, T: 0, B: 0 } });
  const capas = panelesApilados({
    lienzo: l, margen: { L: 0, R: 0, T: 0, B: 0 }, hueco: 0,
    paneles: [
      { yMin: 0, yMax: 1, xMin: -40, xMax: 60 },   // la ruta, en metros
      { yMin: 0, yMax: 50 },                        // el grafico, en segundos
    ],
  });
  assert.equal(capas[0].lp.xMin, -40);
  assert.equal(capas[0].lp.xMax, 60);
  assert.equal(capas[1].lp.xMin, 0);
  assert.equal(capas[1].lp.xMax, 10);
});
```

- [ ] **Paso 2: correrlas y verificar que fallan**

Ejecutar: `node --test test/dibujo.test.js test/widget.test.js`
Esperado: FALLAN las cinco; ni las dos funciones ni la opción existen.

- [ ] **Paso 3: mudar las dos funciones a `dibujo.js`**

Copialas **tal cual están** en `docs/ensayos/movimiento-circular.html`, incluidos sus
comentarios, que explican por qué la marca no es sutil. El único cambio es la firma de
`marcaDeTope`, que pasa a recibir el color en un objeto de opciones como el resto de las
primitivas del módulo, y que usa `exigirColor`.

```js
// Acota el largo dibujado de una flecha sin tocar su direccion, y avisa si la acoto.
// Hace falta cuando dos magnitudes del mismo dibujo tienen escalas muy distintas: en
// el widget de aceleraciones la normal llega a 600 mientras la tangencial vale 6, y
// sin acotar la flecha larga se va del canvas. La escala se deja fija a proposito --
// normalizar al valor del momento borraria que la magnitud crece.
export function acotarFlecha(dx, dy, tope) {
  const largo = Math.hypot(dx, dy);
  if (largo <= tope) return [dx, dy, false];
  const f = tope / largo;
  return [dx * f, dy * f, true];
}

// La marca de una flecha que llego a su tope: dos trazos cortos perpendiculares a la
// punta, la misma convencion que el quiebre de un eje partido. No es sutil a
// proposito -- tiene que quedar claro que la magnitud real sigue creciendo aunque el
// dibujo ya no.
export function marcaDeTope(ctx, x, y, dx, dy, { color } = {}) {
  exigirColor(color, 'marcaDeTope');
  const angulo = Math.atan2(dy, dx);
  const nx = -Math.sin(angulo), ny = Math.cos(angulo);
  ctx.strokeStyle = color;
  ctx.lineWidth = 1.4;
  for (const d of [-3, 3]) {
    ctx.beginPath();
    ctx.moveTo(x + Math.cos(angulo) * d - nx * 5, y + Math.sin(angulo) * d - ny * 5);
    ctx.lineTo(x + Math.cos(angulo) * d + nx * 5, y + Math.sin(angulo) * d + ny * 5);
    ctx.stroke();
  }
}
```

Borralas del ensayo, importalas del módulo, y adaptá las cuatro llamadas a
`marcaDeTope` a la firma nueva.

- [ ] **Paso 4: el rango horizontal por panel**

En `panelesApilados`, que cada panel pueda traer el suyo:

```js
        // Cada panel hereda el rango horizontal del lienzo de afuera, que es lo que
        // hace que una columna vertical signifique lo mismo en todos. Un panel puede
        // pedir el suyo cuando de verdad mide otra cosa: en la nota del auto y el
        // camion, la franja de arriba es la ruta en metros y la de abajo el grafico
        // de posicion contra tiempo en segundos.
        xMin: panel.xMin ?? lienzo.xMin,
        xMax: panel.xMax ?? lienzo.xMax,
```

- [ ] **Paso 5: verificar que el ensayo de circular no se movió**

El paso 3 le cambió el código a un ensayo terminado y aprobado. Comprobá con
`comparar-bitmaps.mjs` que sus cuatro canvas dan idénticos, con el control negativo
corrido. Si alguno cambia, **paralo y decilo**.

- [ ] **Paso 6: correr la suite y commitear**

```bash
node --test "test/**/*.test.js"
git add docs/motor/dibujo.js docs/motor/widget.js docs/ensayos/movimiento-circular.html test
git commit -m "feat(motor): acotar flechas y rango horizontal por panel"
```

---

### Tarea 4: La nota "La Tierra que cae"

Es el ejercicio 12 de la Guía 1: la Tierra gira alrededor del Sol a 30 km/s sobre un
radio de 150 millones de kilómetros. ¿Cuál es su aceleración? La respuesta es
`6.0 × 10⁻³ m/s²` y suena a nada.

**Lo que la nota tiene que hacer ver:** que esos 6 milímetros por segundo cuadrado son
exactamente lo que hace falta. En **un segundo** la Tierra avanza **30 km** por la
tangente y se aparta de ella **3 milímetros**. Esos 3 mm son la diferencia entre una
órbita y salir disparada en línea recta.

**Archivos:**
- Crear: `docs/ejemplos/la-tierra.html`
- Modificar: `docs/index.html`

**Interfaces:**
- Consume: `crearPagina`, `crearWidget` con `escalaUniforme: false`, `crearEscena`,
  `crearCircular`, y de `dibujo.js` `eje`, `curva`, `cuerpo`, `punteado`, `texto`,
  `vectorPx`, `acotarFlecha`, `marcaDeTope`; de `controles.js` `deslizador` y `boton`.
- Produce: la primera nota de ejemplo, y el patrón que la Tarea 5 espeja.

- [ ] **Paso 1: el esqueleto de la nota**

Copiá la estructura de `docs/ensayos/movimiento-circular.html` —script de tema en el
`<head>`, barra de progreso, encabezado, pie— con las clases de la Tarea 2, y cambiá:

- kicker: `EJEMPLO · FÍSICA 1`
- `<h1>`: `La Tierra que cae`
- bajada: `Seis milímetros por segundo cuadrado alcanzan para no salir despedida.`
- pie: `Apunte cap. 2, pp. 25–47 · práctico 1, ej. 12`, con el enlace a
  `../recursos/practico_1_2026.pdf`.

El enunciado citado va en el bloque de borde izquierdo que los ensayos usan para las
fórmulas:

```html
<div style="border-left:2px solid var(--rule);padding:4px 0 4px 20px;margin:24px 0 0">
  <p style="font:400 18px/1.7 'Source Serif 4',Georgia,serif;margin:0">La Tierra gira alrededor del Sol en una órbita aproximadamente circular con una velocidad constante de 30 km/s. ¿Cuál es la aceleración de la Tierra respecto al Sol? Considere el radio de la órbita terrestre igual a 150 × 10⁶ km.</p>
</div>
```

Y un párrafo que diga qué tiene de raro: que la cuenta es de una línea —`a = v²/R`— y da
un número tan chico que parece un error, y que lo que cuesta no es calcularlo sino
creerle.

- [ ] **Paso 2: la física, que es de tres líneas**

```js
const R = 1.5e11;          // 150 millones de km, en metros
const V = 3.0e4;           // 30 km/s, en metros por segundo
const OMEGA = V / R;       // rad/s
const A_C = V * V / R;     // 6.0e-3 m/s^2, el numero del ejercicio
```

Ese `A_C` tiene que dar `6.0e-3`: es el valor que imprime
`parcial-1/soluciones/verificacion-practico-1.py` para el ejercicio 12. Corré el script
y confirmalo antes de escribirlo en la prosa.

- [ ] **Paso 3: el widget**

La idea del dibujo: la Tierra arranca en `(R, 0)` y gira. Se dibujan **dos** caminos
desde ese punto — el real, que es el arco de la órbita, y el que habría seguido **sin
gravedad**, que es la tangente— y el segmento rojo que los separa. Ese segmento es lo
que cayó.

El control es el **tiempo de viaje**: de un segundo a tres meses, en escala logarítmica.
El encuadre se ajusta solo al triángulo que forman los tres puntos, así que a un segundo
se ve una recta y a un mes se ve la curva.

```js
function widgetLaTierra(pagina) {
  const T_EJERCICIO = 1;                    // un segundo: la escala del enunciado
  const T_MAXIMO = 90 * 24 * 3600;          // tres meses
  let t = T_EJERCICIO;

  const real = s => [R * Math.cos(OMEGA * s), R * Math.sin(OMEGA * s)];
  const recto = s => [R, V * s];            // sin gravedad, sigue la tangente
  const caida = s => {
    const [rx, ry] = real(s), [tx, ty] = recto(s);
    return Math.hypot(rx - tx, ry - ty);
  };

  const canvas = document.getElementById('w1-cv');
  const widget = crearWidget({
    pagina, canvas,
    margen: { L: 74, R: 30, T: 30, B: 42 },
    // Escala independiente por eje: la separacion de la tangente y el arco recorrido
    // difieren en siete ordenes de magnitud al segundo de viaje. Con escala uniforme
    // el dibujo seria una raya vertical. La lectura de "exageracion" dice cuanto se
    // estiro el eje horizontal, para que el estiramiento sea un dato y no una trampa.
    escalaUniforme: false,
    encuadre: () => {
      const puntos = [[R, 0], real(t), recto(t)];
      const xs = puntos.map(p => p[0]), ys = puntos.map(p => p[1]);
      const x0 = Math.min(...xs), x1 = Math.max(...xs);
      const y0 = Math.min(...ys), y1 = Math.max(...ys);
      const aireX = Math.max((x1 - x0) * 0.35, 1e-4);
      const aireY = Math.max((y1 - y0) * 0.12, 1e-4);
      return { xMin: x0 - aireX, xMax: x1 + aireX, yMin: y0 - aireY, yMax: y1 + aireY };
    },
    dibujar: pintar,
  });

  function pintar(ctx, l) {
    const p = pagina.paleta();

    // El Sol, cuando entra en el encuadre. Casi nunca entra: a un segundo de viaje el
    // encuadre mide centimetros y el Sol esta a 150 millones de kilometros.
    if (l.xMin <= 0 && 0 <= l.xMax && l.yMin <= 0 && 0 <= l.yMax) {
      cuerpo(ctx, l, [0, 0], { radio: 7, color: p.ink });
      texto(ctx, 'Sol', ...desplazar(l.p([0, 0]), 12, -8), { color: p.dim, px: 10, peso: 400 });
    }

    // El camino sin gravedad: la tangente, punteada.
    punteado(ctx, ...l.p([R, 0]), ...l.p(recto(t)), { color: p.rule, guiones: [4, 5] });
    texto(ctx, 'sin gravedad', ...desplazar(l.p(recto(t)), 8, -6),
      { color: p.dim, px: 10, peso: 400 });

    // El camino real: el arco de la orbita.
    curva(ctx, l, real, 0, t, { color: p.graph, grosor: 1.9 });

    // Lo que cayo: el segmento rojo entre los dos extremos. Es el ejercicio entero.
    const [ax, ay] = l.p(recto(t)), [bx, by] = l.p(real(t));
    vectorPx(ctx, ax, ay, bx, by, { color: p.red, grosor: 2, punta: 8 });

    cuerpo(ctx, l, [R, 0], { radio: 4, color: p.dim });
    cuerpo(ctx, l, real(t), { radio: 5.5, color: p.blue });

    const exageracion = l.escala.x / l.escala.y;
    leer('w1-t', formatearTiempo(t));
    leer('w1-arco', formatearLargo(V * t));
    leer('w1-caida', formatearLargo(caida(t)));
    leer('w1-exag', exageracion >= 1.05 ? '× ' + formatearGrande(exageracion) : 'sin exagerar');
  }
```

Tres ayudantes de formato, porque la nota recorre catorce órdenes de magnitud y un
`toFixed` no sirve: `formatearTiempo` pasa de segundos a minutos, horas, días o meses
según el tamaño; `formatearLargo` de milímetros a metros o kilómetros; `formatearGrande`
escribe un factor grande como `10 millones` en vez de `10000000`. Escribilos arriba del
widget, cortos, y comentá que existen porque la nota va de milímetros a mil millones de
kilómetros.

`desplazar([x, y], dx, dy)` devuelve `[x + dx, y + dy]`: es para no repetir la aritmética
en cada rótulo.

- [ ] **Paso 4: los controles y el encabezado**

Encabezado del widget: `SIMULACIÓN`, nombre `La caída que no se ve`, y la frase de qué
mirar: `— empezá en un segundo y mirá la última lectura.`

Un slider logarítmico de tiempo, un botón de preset que vuelve al segundo del enunciado,
y cuatro lecturas: tiempo de viaje, arco recorrido, separación de la recta, y exageración
del eje horizontal.

```js
  const aLog = v => T_EJERCICIO * Math.pow(T_MAXIMO / T_EJERCICIO, v);
  deslizador({
    entrada: document.getElementById('w1-t-slider'),
    salida: document.getElementById('w1-t-out'),
    formato: v => formatearTiempo(aLog(v)), pagina,
    alCambiar: v => { t = aLog(v); widget.repintar(); },
  });
  boton({
    elemento: document.getElementById('w1-un-segundo'), pagina,
    alApretar: () => {
      t = T_EJERCICIO;
      document.getElementById('w1-t-slider').value = '0';
      document.getElementById('w1-t-out').textContent = formatearTiempo(t);
      widget.repintar();
    },
  });
```

El slider va de `0` a `1` con paso `0.001` y valor inicial `0`, y la conversión
logarítmica la hace `aLog`. El botón dice `Un segundo`.

**El widget no anima.** No tiene reloj: el tiempo es lo que el lector mueve.

- [ ] **Paso 5: el razonamiento en pasos**

Después de la franja, la resolución. Cuatro pasos numerados, con la lista ordenada que
usan los cierres de los ensayos:

1. En un movimiento circular uniforme la aceleración apunta al centro y vale `v²/R`. No
   hay que derivar nada: es la fórmula del capítulo.
2. Pasar las unidades antes de dividir. `30 km/s = 3 × 10⁴ m/s` y
   `150 × 10⁶ km = 1.5 × 10¹¹ m`. La mitad de los errores de este ejercicio son de acá.
3. `a = (3 × 10⁴)² / 1.5 × 10¹¹ = 9 × 10⁸ / 1.5 × 10¹¹ = 6.0 × 10⁻³ m/s²`.
4. Chequear que el número tenga sentido: seis milímetros por segundo cuadrado. En un
   segundo eso desvía a la Tierra **3 milímetros** de la recta que traía —el segmento
   rojo del dibujo—, mientras avanza **30 kilómetros**. Uno en diez millones.

Y un párrafo de cierre que diga lo que la nota vino a decir: que la aceleración no mide
cuánto se mueve algo, mide cuánto **cambia** su movimiento; que el Sol no tiene que
tironear fuerte porque no tiene apuro, tiene que tironear **siempre**; y que moviendo el
control hasta un mes esos milímetros por segundo se vuelven veinte mil millones de
metros de desvío, que es lo que cierra la órbita.

**Ningún número de esos pasos que no salga del script de verificación**, salvo los del
enunciado y los 3 mm, que se derivan de `½ a t²` con `t = 1 s` y hay que dejarlos
comprobados en el informe.

- [ ] **Paso 6: enlazar desde la portada**

En `docs/index.html`, la fila `EJEMPLO 1` pasa de `<span>` a `<a href="ejemplos/la-tierra.html">`,
con el mismo tratamiento que los ensayos enlazados.

- [ ] **Paso 7: verificar en el navegador**

Servir `docs/` como raíz. Comprobar, a 1280 y a 390 px con
`Emulation.setDeviceMetricsOverride` y el caché desactivado:

- Que al cargar, con el preset del segundo, la separación lea `3.0 mm` y el arco `30 km`.
- Que la exageración lea unas diez millones de veces ahí, y que baje a `sin exagerar`
  cuando el tiempo llega a semanas.
- Que el Sol aparezca en el encuadre recién cuando el arco es una fracción apreciable de
  la órbita, y no antes.
- Que no anime solo, que el tema repinte, que no desborde, y que el enlace del pie
  resuelva sirviendo desde `docs/`.

- [ ] **Paso 8: correr la suite y commitear**

```bash
node --test "test/**/*.test.js"
git add docs/ejemplos/la-tierra.html docs/index.html
git commit -m "feat(plataforma): nota de ejemplo la Tierra que cae"
```

---

### Tarea 5: La nota "El auto y el camión"

Es el ejercicio 5 de la Guía 1, y es uno de los dos que se quedaron sin widget en el
plan anterior. Un auto y un camión arrancan en el mismo instante, el auto a cierta
distancia atrás. El camión acelera a `1.2 m/s²`, el auto a `1.8 m/s²`. El auto lo alcanza
cuando el camión recorrió 45 m.

**Lo que la nota tiene que hacer ver:** que el alcance es **el cruce de dos curvas**. En
el gráfico de posición contra tiempo, las dos parábolas se acercan y se tocan en un
punto, y ese punto es la respuesta. Deja de ser un sistema de ecuaciones y pasa a ser
algo que se ve venir.

**Archivos:**
- Crear: `docs/ejemplos/auto-y-camion.html`
- Modificar: `docs/index.html`

**Interfaces:**
- Consume: `crearPagina`, `crearWidget`, `crearEscena`, `panelesApilados` **con rango
  horizontal por panel**, y de `dibujo.js` `eje`, `curva`, `cuerpo`, `punteado`, `texto`;
  de `controles.js` `deslizador`, `boton`, `rotuloReproducir`.
- Produce: la segunda nota de ejemplo.

- [ ] **Paso 1: el esqueleto**

Igual que la nota anterior, con el kicker `EJEMPLO · FÍSICA 1`, el `<h1>`
`El auto y el camión`, y la bajada
`Alcanzar a alguien es cruzarse con su curva.` El pie:
`Apunte cap. 1, pp. 3–24 · práctico 1, ej. 5`.

El enunciado citado, en el bloque de borde izquierdo:

```html
<p style="font:400 18px/1.7 'Source Serif 4',Georgia,serif;margin:0">Un automóvil y un camión parten en el mismo instante, encontrándose inicialmente el auto a cierta distancia detrás del camión. Este último tiene una aceleración constante de 1.2 m/s², mientras que el auto acelera a 1.8 m/s². El auto alcanza al camión cuando éste ha recorrido 45 metros. ¿Cuánto tiempo tarda? ¿Cuál era la distancia inicial? ¿Con qué velocidad va cada uno al encontrarse?</p>
```

Y un párrafo sobre qué lo hace incómodo: que el enunciado da el dato del final —los
45 m— y pregunta por el principio, así que hay que leerlo al revés.

- [ ] **Paso 2: la física**

```js
const A_AUTO = 1.8, A_CAMION = 1.2;        // m/s^2
let d0 = 22.5;                              // distancia inicial, en metros

// Las dos posiciones. El auto arranca en 0 y el camion d0 metros adelante.
const xAuto = s => 0.5 * A_AUTO * s * s;
const xCamion = s => d0 + 0.5 * A_CAMION * s * s;

// El encuentro sale de igualarlas: 1/2 (a_auto - a_camion) t^2 = d0. Depende solo de
// la DIFERENCIA de aceleraciones, que es la lectura que conviene que el lector note.
const tEncuentro = () => Math.sqrt(2 * d0 / (A_AUTO - A_CAMION));
```

Con `d0 = 22.5` eso da `t = 8.660 s`, y el camión habrá recorrido
`½ · 1.2 · 8.66² = 45 m`, que es el dato del enunciado. Las velocidades en el encuentro
son `15.59` y `10.39 m/s`. Los cuatro números salen de
`parcial-1/soluciones/verificacion-practico-1.py`; corré el script y contrastalos.

- [ ] **Paso 3: el widget, en dos franjas**

La de arriba es la ruta, en **metros**; la de abajo es el gráfico de posición contra
tiempo, en **segundos**. Son dos magnitudes distintas en el eje horizontal, y por eso
esta tarea necesita el rango por panel que agregó la Tarea 3.

```js
  const MARGEN = { L: 62, R: 24, T: 20, B: 34 };
  const HUECO_ROTULO = COLGADO_ROTULO_EJE + 8;
  const canvas = document.getElementById('w1-cv');

  const widget = crearWidget({
    pagina, canvas, margen: MARGEN,
    escalaUniforme: false,
    altoMin: 2 * (95 + HUECO_ROTULO) + MARGEN.T + MARGEN.B,
    encuadre: () => ({ xMin: 0, xMax: tEncuentro() * 1.25, yMin: 0, yMax: 2 }),
    dibujar: pintar,
  });

  const capas = l => panelesApilados({
    lienzo: l, margen: MARGEN, hueco: HUECO_ROTULO,
    paneles: [
      // La ruta: el eje horizontal son METROS, no segundos. Va de un poco antes del
      // auto hasta un poco despues de donde se encuentran.
      { yMin: 0, yMax: 1, xMin: -8, xMax: xAuto(tEncuentro()) * 1.25 },
      // El grafico: el eje horizontal son SEGUNDOS, heredados del lienzo de afuera.
      { yMin: 0, yMax: xAuto(tEncuentro()) * 1.25 },
    ],
  });
```

El dibujo de cada franja:

```js
  function pintar(ctx, l) {
    const p = pagina.paleta();
    const t = escena.t, tEnc = tEncuentro();
    const [ruta, grafico] = capas(l);

    // --- la ruta ---
    eje(ctx, ruta.lp, { color: p.rule, colorTexto: p.dim, etiquetaX: 'x [m]', marcasY: false });
    cuerpo(ctx, ruta.lp, [xAuto(t), 0.35], { radio: 7, color: p.blue });
    cuerpo(ctx, ruta.lp, [xCamion(t), 0.35], { radio: 9, color: p.red });
    texto(ctx, 'auto', ...desplazar(ruta.lp.p([xAuto(t), 0.35]), 0, -16),
      { color: p.blue, alineacion: 'center' });
    texto(ctx, 'camión', ...desplazar(ruta.lp.p([xCamion(t), 0.35]), 0, -18),
      { color: p.red, alineacion: 'center' });

    // La distancia entre los dos, dibujada como el segmento que se achica. Es la
    // lectura que el parrafo pide mirar.
    if (xCamion(t) - xAuto(t) > 0.5) {
      punteado(ctx, ...ruta.lp.p([xAuto(t), 0.62]), ...ruta.lp.p([xCamion(t), 0.62]),
        { color: p.dim });
    }

    // --- el grafico ---
    eje(ctx, grafico.lp, { color: p.rule, colorTexto: p.dim,
      etiquetaX: 't [s]', etiquetaY: 'x [m]' });
    curva(ctx, grafico.lp, s => [s, xAuto(s)], 0, l.xMax, { color: p.blue, grosor: 1.9 });
    curva(ctx, grafico.lp, s => [s, xCamion(s)], 0, l.xMax, { color: p.red, grosor: 1.9 });

    // El cruce: el punto donde las dos curvas se tocan, marcado desde el principio.
    // Que este ahi antes de que los autos lleguen es el punto de la nota -- la
    // respuesta se ve venir.
    punteado(ctx, ...grafico.lp.p([tEnc, 0]), ...grafico.lp.p([tEnc, xAuto(tEnc)]),
      { color: p.rule });
    cuerpo(ctx, grafico.lp, [tEnc, xAuto(tEnc)], { radio: 5, color: p.ink });
    texto(ctx, 'se alcanzan', ...desplazar(grafico.lp.p([tEnc, xAuto(tEnc)]), 10, -8),
      { color: p.ink });

    cuerpo(ctx, grafico.lp, [t, xAuto(t)], { radio: 4, color: p.blue });
    cuerpo(ctx, grafico.lp, [t, xCamion(t)], { radio: 4, color: p.red });

    leer('w1-t', t.toFixed(2) + ' s');
    leer('w1-sep', Math.max(0, xCamion(t) - xAuto(t)).toFixed(1) + ' m');
    leer('w1-tenc', tEnc.toFixed(2) + ' s');
    leer('w1-camion', (0.5 * A_CAMION * tEnc * tEnc).toFixed(1) + ' m');
  }
```

Las cuatro lecturas: tiempo, **distancia entre ellos**, instante del encuentro, y cuánto
habrá recorrido el camión para entonces —que con la distancia inicial del enunciado da
los 45 m del dato—.

- [ ] **Paso 4: los controles**

Reproducir y reiniciar como los ensayos, con `rotuloReproducir`; un slider de distancia
inicial de 5 a 60 m, paso 0.5, valor 22.5; y un botón `El del ejercicio` que la devuelve
a 22.5.

La escena dura `tEncuentro() * 1.25`, recalculada al mover el slider, con velocidad 0.6.
El estado de reposo es `0.35 · duracion`, como todos los widgets del proyecto.

Que mover el slider **no** reinicie la reproducción: sólo recalcula la duración y el
encuadre, igual que hacen los widgets de tiro.

- [ ] **Paso 5: el razonamiento en pasos**

1. Escribir las dos posiciones desde el mismo origen y el mismo reloj. El auto en `0`,
   el camión en `d₀`. Ése es todo el trabajo: el resto es álgebra.
2. Alcanzar significa **estar en el mismo lugar al mismo tiempo**, o sea igualar las dos.
   Queda `½ (a_auto − a_camión) t² = d₀`: el encuentro depende sólo de la **diferencia**
   de aceleraciones, no de cuánto acelera cada uno.
3. El enunciado no da `d₀`, da que el camión recorrió 45 m. De ahí sale el tiempo
   primero: `45 = ½ · 1.2 · t²`, o sea `t = 8.66 s`.
4. Con el tiempo, el resto cae solo. El auto recorrió `½ · 1.8 · 8.66² = 67.5 m`, así que
   la distancia inicial era `67.5 − 45 = 22.5 m`. Y las velocidades son `a · t`:
   `15.59 m/s` el auto y `10.39 m/s` el camión.

Cierre: que el gráfico de abajo tiene la respuesta dibujada desde el primer instante —el
cruce está ahí antes de que los autos lleguen—, y que por eso conviene dibujarlo antes de
despejar: se ve si hay encuentro, cuándo, y si la cuenta dio cualquier cosa.

- [ ] **Paso 6: enlazar desde la portada**

La fila `EJEMPLO 2` pasa a `<a href="ejemplos/auto-y-camion.html">`.

- [ ] **Paso 7: verificar en el navegador**

Sirviendo `docs/` como raíz, a 1280 y a 390 px:

- Con la distancia del enunciado, que `instante del encuentro` lea `8.66 s` y
  `recorrido del camión` lea `45.0 m`.
- Que al reproducir, la separación baje hasta `0.0 m` **exactamente** cuando los dos
  puntos del gráfico se tocan en la marca del cruce.
- Que moviendo la distancia inicial el cruce se corra y las dos lecturas lo sigan.
- Que las dos franjas tengan ejes horizontales **distintos** —metros arriba, segundos
  abajo— y que cada uno esté rotulado.
- Que no anime solo, que el tema repinte, que no desborde, y que el enlace del pie
  resuelva.

- [ ] **Paso 8: correr la suite y commitear**

```bash
node --test "test/**/*.test.js"
git add docs/ejemplos/auto-y-camion.html docs/index.html
git commit -m "feat(plataforma): nota de ejemplo el auto y el camion"
```

---

## Fase C — el motor para diagramas de fuerzas

Las tres tareas que siguen no agregan ninguna página: agregan al motor las cuatro cosas
que un diagrama de cuerpo aislado necesita y que hoy no existen. Se hacen antes de los
ensayos 4 y 5 para que esos ensayos sean, como los tres anteriores, casi puro contenido.

### Tarea 6: El marco rotado

Un plano inclinado se piensa con los ejes **girados**: uno a lo largo del plano y otro
perpendicular a él. Hoy `crearLienzo` es un mapeo alineado a los ejes de la pantalla.
Girar el contexto con `ctx.rotate` parece la salida fácil, pero rompe `l.p()` y, peor,
rompe `arrastrable`, que vuelve de píxeles a unidades físicas con `l.ux`/`l.uy` y no
sabe nada de la transformación del contexto. La rotación tiene que vivir en el lienzo.

**Archivos:**
- Modificar: `docs/motor/lienzo.js`
- Modificar: `docs/motor/arrastre.js`
- Prueba: `test/lienzo.test.js`, `test/arrastre.test.js`

**Interfaces:**
- Consume: `crearLienzo` tal como quedó en la Guía 1 — `{ ancho, alto, xMin, xMax, yMin,
  yMax, margen }` → `{ px, py, p, ux, uy, escala, ... }`.
- Produce: `crearLienzo({ ..., angulo = 0 })`. Las coordenadas que reciben `px`, `py` y
  `p`, y las que devuelven `ux` y `uy`, son las del **marco girado**. `ux` y `uy` pasan a
  aceptar la segunda coordenada del píxel —`ux(vx, vy = 0)`, `uy(vy, vx = 0)`—, igual que
  `px(x, y = 0)` y `py(y, x = 0)` ya lo hacen. Se agregan dos ayudantes de dirección:
  `aMarco([X, Y])` pasa un vector del mundo al marco, y `aMundo([x, y])` al revés; los
  dos son sólo dirección, sin traslación, que es lo que hace falta para una fuerza.
  Con `angulo = 0` todo el módulo se comporta **exactamente** como antes.

- [ ] **Paso 1: escribir las pruebas que fallan**

Agregalas a `test/lienzo.test.js`, después de las que ya están.

```js
test('sin angulo el lienzo se comporta igual que siempre', () => {
  const l = crearLienzo({ ancho: 200, alto: 100, xMin: 0, xMax: 10, yMin: 0, yMax: 5 });
  assert.equal(l.px(0), 0);
  assert.equal(l.px(10), 200);
  assert.equal(l.py(0), 100);
  assert.equal(l.ux(0), 0);
  assert.equal(l.uy(100), 0);
  assert.deepEqual(l.aMarco([1, 0]), [1, 0]);
  assert.deepEqual(l.aMundo([0, 1]), [0, 1]);
});

test('con angulo, avanzar sobre el eje x del marco sube en pantalla', () => {
  // 30 grados: el eje x del marco apunta 30 grados por encima de la horizontal, asi que
  // un punto en (10, 0) del marco tiene que quedar a la derecha y mas arriba del origen.
  const l = crearLienzo({
    ancho: 400, alto: 400, xMin: -10, xMax: 10, yMin: -10, yMax: 10,
    angulo: Math.PI / 6,
  });
  const [x0, y0] = l.p([0, 0]);
  const [x1, y1] = l.p([10, 0]);
  assert.ok(x1 > x0, 'avanza a la derecha');
  assert.ok(y1 < y0, 'y sube, porque en pantalla la y crece hacia abajo');
});

test('ux y uy invierten a p tambien con angulo', () => {
  const l = crearLienzo({
    ancho: 320, alto: 180, xMin: -4, xMax: 12, yMin: -2, yMax: 9,
    margen: { L: 31, R: 17, T: 13, B: 23 }, angulo: 0.37,
  });
  for (const punto of [[-4, -2], [0, 0], [3.7, 4.25], [12, 9]]) {
    const [vx, vy] = l.p(punto);
    assert.ok(Math.abs(l.ux(vx, vy) - punto[0]) < 1e-9, `x vuelve para ${punto}`);
    assert.ok(Math.abs(l.uy(vy, vx) - punto[1]) < 1e-9, `y vuelve para ${punto}`);
  }
});

test('aMarco y aMundo son inversas y conservan el largo', () => {
  const l = crearLienzo({
    ancho: 100, alto: 100, xMin: 0, xMax: 1, yMin: 0, yMax: 1, angulo: 0.8,
  });
  for (const v of [[1, 0], [0, 1], [3, -4]]) {
    const ida = l.aMarco(v);
    const vuelta = l.aMundo(ida);
    assert.ok(Math.abs(Math.hypot(...ida) - Math.hypot(...v)) < 1e-12, 'conserva el largo');
    assert.ok(Math.abs(vuelta[0] - v[0]) < 1e-12, 'vuelve x');
    assert.ok(Math.abs(vuelta[1] - v[1]) < 1e-12, 'vuelve y');
  }
});

test('el peso, que en el mundo apunta abajo, en un marco inclinado tiene dos componentes', () => {
  // Es la descomposicion que resuelve todo plano inclinado, y la razon de ser del marco
  // girado: el peso vale (0, -1) en el mundo y en el marco vale (-sen a, -cos a).
  const alfa = Math.PI / 6;
  const l = crearLienzo({
    ancho: 100, alto: 100, xMin: 0, xMax: 1, yMin: 0, yMax: 1, angulo: alfa,
  });
  const [aLoLargo, perpendicular] = l.aMarco([0, -1]);
  assert.ok(Math.abs(aLoLargo + Math.sin(alfa)) < 1e-12, 'tira hacia abajo del plano');
  assert.ok(Math.abs(perpendicular + Math.cos(alfa)) < 1e-12, 'y aprieta contra el plano');
});
```

- [ ] **Paso 2: correrlas y verificar que fallan**

Ejecutar: `node --test test/lienzo.test.js`
Esperado: FALLAN las cuatro últimas (`l.aMarco is not a function`). La primera PASA: fija
el comportamiento de hoy, y tiene que seguir pasando cuando termines.

- [ ] **Paso 3: implementar**

La rotación se aplica **antes** del mapeo a píxeles: un punto del marco se lleva al
mundo, y el mundo se mapea como siempre.

```js
export function crearLienzo({ ancho, alto, xMin, xMax, yMin, yMax, margen, angulo = 0 }) {
  const m = { L: 0, R: 0, T: 0, B: 0, ...(margen || {}) };
  const kx = (ancho - m.L - m.R) / (xMax - xMin);
  const ky = (alto - m.T - m.B) / (yMax - yMin);
  const cos = Math.cos(angulo), sen = Math.sin(angulo);

  // Del marco girado al mundo y del mundo al marco. Son solo direccion: no hay
  // traslacion, porque los dos marcos comparten el origen. Es justo lo que necesita una
  // fuerza -- el peso apunta abajo en el mundo, y sobre un plano inclinado hay que
  // leerlo en el marco del plano.
  const aMundo = ([x, y]) => [x * cos - y * sen, x * sen + y * cos];
  const aMarco = ([X, Y]) => [X * cos + Y * sen, -X * sen + Y * cos];

  // El mapeo de un punto del marco a pixeles. Con angulo distinto de cero un punto NO se
  // puede mapear eje por eje: cada pixel depende de las dos coordenadas. Por eso `p` es
  // la forma correcta, y `px`/`py` toman la coordenada que les falta como segundo
  // argumento, igual que ya lo hacian.
  const aPixel = ([x, y]) => {
    const [X, Y] = aMundo([x, y]);
    return [m.L + (X - xMin) * kx, alto - m.B - (Y - yMin) * ky];
  };
  // Y la vuelta: de pixeles a coordenadas del marco.
  const aUnidades = (vx, vy) =>
    aMarco([(vx - m.L) / kx + xMin, (alto - m.B - vy) / ky + yMin]);

  return {
    ancho, alto, xMin, xMax, yMin, yMax, margen: m, angulo,
    aMundo, aMarco,
    p: aPixel,
    px: (x, y = 0) => aPixel([x, y])[0],
    py: (y, x = 0) => aPixel([x, y])[1],
    ux: (vx, vy = 0) => aUnidades(vx, vy)[0],
    uy: (vy, vx = 0) => aUnidades(vx, vy)[1],
    escala: { x: kx, y: ky },
  };
}
```

Con `angulo = 0` sale `cos = 1` y `sen = 0`, así que `aMundo` y `aMarco` son la
identidad, `aPixel` se reduce al mapeo de siempre, y `ux(vx)` y `uy(vy)` devuelven
exactamente lo que devolvían. Eso es lo que fija la primera prueba, y es lo que permite
que las decenas de llamadas ya escritas sigan andando sin tocarlas.

- [ ] **Paso 4: correr las pruebas del lienzo**

Ejecutar: `node --test test/lienzo.test.js`
Esperado: PASAN todas, incluidas las que ya estaban.

- [ ] **Paso 5: adaptar `arrastrable` y probarlo con un lienzo inclinado**

`docs/motor/arrastre.js` convierte el píxel del puntero con `l.ux(x)` y `l.uy(y)` por
separado. Con ángulo eso da mal: hay que pasarle las dos coordenadas. Cambialo a
`l.ux(x, y)` y `l.uy(y, x)` —con ángulo cero devuelven exactamente lo mismo que hoy— y
agregá esta prueba a `test/arrastre.test.js`:

```js
test('con un lienzo inclinado, el punto que llega al callback es el del marco', () => {
  const alfa = Math.PI / 6;
  const l = crearLienzo({
    ancho: 400, alto: 400, xMin: -10, xMax: 10, yMin: -10, yMax: 10, angulo: alfa,
  });
  const esperado = [6, 2];
  const [vx, vy] = l.p(esperado);
  let visto = null;
  const canvas = canvasFalso({ ancho: 400, alto: 400 });
  arrastrable({ canvas, lienzo: () => l, alArrastrar: q => { visto = q; } });
  canvas.disparar('pointerdown', { offsetX: vx, offsetY: vy });
  assert.ok(Math.abs(visto[0] - esperado[0]) < 1e-6, 'x en el marco');
  assert.ok(Math.abs(visto[1] - esperado[1]) < 1e-6, 'y en el marco');
});
```

Mirá cómo las pruebas que ya están en `test/arrastre.test.js` fabrican su canvas falso y
disparan eventos, y usá el mismo ayudante en vez de escribir uno nuevo; `canvasFalso` y
`disparar` de arriba son nombres provisorios.

- [ ] **Paso 6: verificar que con ángulo cero no se movió un solo píxel**

Tocaste el mapeo que usan los tres ensayos terminados. La única evidencia válida es
comparar el resultado. Corré `comparar-bitmaps.mjs` sobre los doce canvas de
`tiro-parabolico.html`, `derivada-integral.html` y `movimiento-circular.html`, contra el
árbol del commit anterior, con el control negativo corrido. **Proceso de Chrome fresco y
perfil descartable por medición**, y el servidor con raíz en `docs/`. Si algún canvas
cambia, **paralo y decilo** con la diferencia medida.

- [ ] **Paso 7: correr la suite entera y commitear**

```bash
node --test "test/**/*.test.js"
git add docs/motor/lienzo.js docs/motor/arrastre.js test/lienzo.test.js test/arrastre.test.js
git commit -m "feat(motor): marco rotado en el lienzo"
```

---
### Tarea 7: Bloques y suelo

Hasta ahora todo lo que se dibujó fue un punto: `cuerpo` hace un círculo. Un diagrama de
cuerpo aislado necesita un **bloque**, y necesita un suelo que pueda estar inclinado.

**Archivos:**
- Modificar: `docs/motor/dibujo.js`, `docs/ensayos/tiro-parabolico.html`
- Prueba: `test/dibujo.test.js`

**Interfaces:**
- Produce:
  - `bloque(ctx, l, centro, { ancho, alto, color, borde, angulo = 0 })` — rectángulo
    centrado en un punto del marco, con medidas en unidades físicas.
  - `suelo(ctx, l, { color, desde, hasta, y = 0 })` — la línea con rayitas. Se muda desde
    el ensayo de tiro, generalizada: hoy vive ahí y **supone que el encuadre arranca en
    cero**, lo que un plano inclinado rompe.

- [ ] **Paso 1: escribir las pruebas que fallan**

```js
test('bloque dibuja un rectangulo cerrado de cuatro esquinas', () => {
  const l = crearLienzo({ ancho: 200, alto: 200, xMin: 0, xMax: 10, yMin: 0, yMax: 10 });
  const c = ctxFalso();
  bloque(c, l, [5, 5], { ancho: 2, alto: 1, color: '#000' });
  const nombres = c.ops.map(o => o[0]);
  assert.equal(c.ops.filter(o => o[0] === 'moveTo').length, 1);
  assert.equal(c.ops.filter(o => o[0] === 'lineTo').length, 3);
  assert.ok(nombres.includes('closePath'));
  assert.ok(nombres.includes('fill'));
});

test('el bloque queda centrado en el punto que se le da', () => {
  const l = crearLienzo({ ancho: 200, alto: 200, xMin: 0, xMax: 10, yMin: 0, yMax: 10 });
  const c = ctxFalso();
  bloque(c, l, [5, 5], { ancho: 2, alto: 1, color: '#000' });
  const xs = c.ops.filter(o => o[0] === 'moveTo' || o[0] === 'lineTo').map(o => o[1]);
  const ys = c.ops.filter(o => o[0] === 'moveTo' || o[0] === 'lineTo').map(o => o[2]);
  const cx = (Math.min(...xs) + Math.max(...xs)) / 2;
  const cy = (Math.min(...ys) + Math.max(...ys)) / 2;
  assert.ok(Math.abs(cx - l.p([5, 5])[0]) < 1e-9);
  assert.ok(Math.abs(cy - l.p([5, 5])[1]) < 1e-9);
});

test('con borde, el bloque ademas se contornea', () => {
  const l = crearLienzo({ ancho: 200, alto: 200, xMin: 0, xMax: 10, yMin: 0, yMax: 10 });
  const c = ctxFalso();
  bloque(c, l, [5, 5], { ancho: 2, alto: 1, color: '#000', borde: '#f00' });
  assert.ok(c.ops.some(o => o[0] === 'stroke'));
});

test('suelo dibuja la linea y sus rayitas dentro del rango pedido', () => {
  const l = crearLienzo({ ancho: 400, alto: 200, xMin: -5, xMax: 15, yMin: 0, yMax: 10 });
  const c = ctxFalso();
  suelo(c, l, { color: '#000', desde: 0, hasta: 10 });
  const xs = c.ops.filter(o => o[0] === 'moveTo').map(o => o[1]);
  assert.ok(Math.min(...xs) >= l.p([0, 0])[0] - 1e-9, 'no arranca antes');
  assert.ok(Math.max(...xs) <= l.p([10, 0])[0] + 1e-9, 'no termina despues');
  assert.ok(xs.length > 3, 'hay rayitas, no solo la linea');
});

test('suelo puede ir a una altura distinta de cero', () => {
  const l = crearLienzo({ ancho: 400, alto: 200, xMin: 0, xMax: 10, yMin: 0, yMax: 10 });
  const c = ctxFalso();
  suelo(c, l, { color: '#000', desde: 0, hasta: 10, y: 4 });
  const ys = c.ops.filter(o => o[0] === 'moveTo').map(o => o[2]);
  assert.ok(Math.abs(Math.max(...ys) - l.p([0, 4])[1]) < 1e-9);
});
```

- [ ] **Paso 2: correrlas y verificar que fallan**

Ejecutar: `node --test test/dibujo.test.js`
Esperado: FALLAN las cinco.

- [ ] **Paso 3: implementar**

```js
// Un rectangulo con medidas en unidades fisicas, centrado en un punto del marco. Las
// cuatro esquinas se calculan en el marco y se mapean una por una con `l.p`, en vez de
// rotar el contexto: asi el bloque queda consistente con el lienzo inclinado y con lo
// que `arrastrable` devuelve, que es lo que se rompe cuando uno gira el contexto a mano.
export function bloque(ctx, l, centro, { ancho, alto, color, borde, angulo = 0 } = {}) {
  exigirColor(color, 'bloque');
  const [cx, cy] = centro;
  const cos = Math.cos(angulo), sen = Math.sin(angulo);
  const esquinas = [[-1, -1], [1, -1], [1, 1], [-1, 1]].map(([sx, sy]) => {
    const dx = (sx * ancho) / 2, dy = (sy * alto) / 2;
    return l.p([cx + dx * cos - dy * sen, cy + dx * sen + dy * cos]);
  });
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.moveTo(esquinas[0][0], esquinas[0][1]);
  for (let i = 1; i < 4; i++) ctx.lineTo(esquinas[i][0], esquinas[i][1]);
  ctx.closePath();
  ctx.fill();
  if (borde) {
    ctx.strokeStyle = borde;
    ctx.lineWidth = 1.2;
    ctx.stroke();
  }
}

// La linea del suelo con sus rayitas. Viene del ensayo de tiro parabolico, donde estaba
// escrita suponiendo que el encuadre arranca en cero; aca el rango es explicito, que es
// lo que un plano inclinado necesita. Las rayitas se dibujan en el marco del lienzo, asi
// que sobre un lienzo inclinado salen perpendiculares al plano, como corresponde.
export function suelo(ctx, l, { color, desde, hasta, y = 0 } = {}) {
  exigirColor(color, 'suelo');
  const [x0, y0] = l.p([desde, y]);
  const [x1, y1] = l.p([hasta, y]);
  ctx.strokeStyle = color;
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(x0, y0);
  ctx.lineTo(x1, y1);
  ctx.stroke();
  const largo = Math.hypot(x1 - x0, y1 - y0);
  const ux = (x1 - x0) / largo, uy = (y1 - y0) / largo;
  ctx.globalAlpha = 0.5;
  for (let d = 0; d < largo; d += 9) {
    ctx.beginPath();
    ctx.moveTo(x0 + ux * d, y0 + uy * d);
    ctx.lineTo(x0 + ux * (d - 6) + uy * 6, y0 + uy * (d - 6) - ux * 6);
    ctx.stroke();
  }
  ctx.globalAlpha = 1;
}
```

- [ ] **Paso 4: sacar la copia del ensayo de tiro**

`docs/ensayos/tiro-parabolico.html` tiene su propio `suelo` local. Borralo, importá el
del módulo, y adaptá la llamada al rango explícito: el ensayo lo usa de `l.xMin` a
`l.xMax` con `y = 0`.

- [ ] **Paso 5: verificar que el ensayo de tiro no se movió**

Es la prueba de que la generalización es fiel. `comparar-bitmaps.mjs` sobre sus cuatro
canvas, con el control negativo. Si alguno cambia, **paralo y decilo** con la diferencia.

- [ ] **Paso 6: correr la suite y commitear**

```bash
node --test "test/**/*.test.js"
git add docs/motor/dibujo.js docs/ensayos/tiro-parabolico.html test/dibujo.test.js
git commit -m "feat(motor): bloques rectangulares y suelo con rango explicito"
```

---

### Tarea 8: Arco de ángulo y descomposición

Las dos cosas que todo diagrama de fuerzas dibuja y que hoy están escritas a mano dentro
de un ensayo: el arquito que marca un ángulo con su letra, y el rectángulo punteado que
muestra en qué se descompone un vector.

**Archivos:**
- Modificar: `docs/motor/dibujo.js`
- Prueba: `test/dibujo.test.js`

**Interfaces:**
- Produce:
  - `arco(ctx, l, centro, { radio, desde, hasta, color, rotulo, colorTexto })` — el arco
    entre dos ángulos, en píxeles de radio, con su rótulo en la bisectriz.
  - `componentes(ctx, l, desde, hasta, { color, guiones = [3, 4] })` — las dos líneas
    punteadas que cierran el rectángulo entre el origen del vector y su punta, en los
    ejes del marco. Es lo que hace ver que una fuerza oblicua **son** dos fuerzas.

- [ ] **Paso 1: escribir las pruebas que fallan**

```js
test('arco traza un arco y escribe su rotulo', () => {
  const l = crearLienzo({ ancho: 200, alto: 200, xMin: -5, xMax: 5, yMin: -5, yMax: 5 });
  const c = ctxFalso();
  arco(c, l, [0, 0], { radio: 30, desde: 0, hasta: Math.PI / 3,
    color: '#000', rotulo: 'α', colorTexto: '#666' });
  assert.equal(c.ops.filter(o => o[0] === 'arc').length, 1);
  const t = c.ops.find(o => o[0] === 'fillText');
  assert.equal(t[1], 'α');
});

test('el rotulo del arco cae en la bisectriz, del lado de afuera', () => {
  const l = crearLienzo({ ancho: 200, alto: 200, xMin: -5, xMax: 5, yMin: -5, yMax: 5 });
  const c = ctxFalso();
  arco(c, l, [0, 0], { radio: 30, desde: 0, hasta: Math.PI / 2,
    color: '#000', rotulo: 'α', colorTexto: '#666' });
  const [ox, oy] = l.p([0, 0]);
  const t = c.ops.find(o => o[0] === 'fillText');
  // Bisectriz de 0 a 90 grados: 45. En pantalla la y crece hacia abajo, asi que el
  // rotulo queda a la derecha y arriba del centro.
  assert.ok(t[2] > ox, 'a la derecha');
  assert.ok(t[3] < oy, 'arriba');
  assert.ok(Math.hypot(t[2] - ox, t[3] - oy) > 30, 'afuera del arco');
});

test('arco sin rotulo no escribe nada', () => {
  const l = crearLienzo({ ancho: 200, alto: 200, xMin: -5, xMax: 5, yMin: -5, yMax: 5 });
  const c = ctxFalso();
  arco(c, l, [0, 0], { radio: 30, desde: 0, hasta: 1, color: '#000' });
  assert.equal(c.ops.filter(o => o[0] === 'fillText').length, 0);
});

test('componentes cierra el rectangulo con dos punteadas', () => {
  const l = crearLienzo({ ancho: 200, alto: 200, xMin: 0, xMax: 10, yMin: 0, yMax: 10 });
  const c = ctxFalso();
  componentes(c, l, [2, 2], [6, 5], { color: '#000' });
  // Dos segmentos: cada uno es un moveTo y un lineTo.
  assert.equal(c.ops.filter(o => o[0] === 'moveTo').length, 2);
  assert.equal(c.ops.filter(o => o[0] === 'lineTo').length, 2);
  const dashes = c.ops.filter(o => o[0] === 'setLineDash').map(o => o[1]);
  assert.deepEqual(dashes.at(-1), [], 'limpia los guiones al salir');
});

test('las dos punteadas pasan por las esquinas del rectangulo', () => {
  const l = crearLienzo({ ancho: 200, alto: 200, xMin: 0, xMax: 10, yMin: 0, yMax: 10 });
  const c = ctxFalso();
  componentes(c, l, [2, 2], [6, 5], { color: '#000' });
  const puntos = c.ops.filter(o => o[0] === 'moveTo' || o[0] === 'lineTo')
    .map(o => [o[1], o[2]]);
  const esquinaA = l.p([6, 2]), esquinaB = l.p([2, 5]);
  const cerca = (a, b) => Math.hypot(a[0] - b[0], a[1] - b[1]) < 1e-9;
  assert.ok(puntos.some(q => cerca(q, esquinaA)), 'la esquina de abajo');
  assert.ok(puntos.some(q => cerca(q, esquinaB)), 'la esquina del costado');
});
```

- [ ] **Paso 2: correrlas y verificar que fallan**

Ejecutar: `node --test test/dibujo.test.js`
Esperado: FALLAN las cinco.

- [ ] **Paso 3: implementar**

El arco sale del que el ensayo de tiro dibuja a mano para el ángulo del vector inicial;
mirá ahí los valores de grosor y de desplazamiento del rótulo antes de escribirlos.

```js
// El arquito que marca un angulo, con su letra en la bisectriz. El radio va en pixeles
// y no en unidades fisicas a proposito: un angulo no tiene tamaño fisico, y si el radio
// se escalara con el encuadre el arco cambiaria de tamaño al mover un slider.
export function arco(ctx, l, centro, { radio, desde, hasta, color, rotulo, colorTexto } = {}) {
  exigirColor(color, 'arco');
  const [ox, oy] = l.p(centro);
  ctx.strokeStyle = color;
  ctx.lineWidth = 1.2;
  ctx.beginPath();
  // En pantalla la y crece hacia abajo, asi que un angulo que en la fisica va en
  // sentido antihorario se dibuja con los signos cambiados.
  ctx.arc(ox, oy, radio, -desde, -hasta, true);
  ctx.stroke();
  if (!rotulo) return;
  exigirColor(colorTexto, 'arco (colorTexto)');
  const medio = (desde + hasta) / 2;
  texto(ctx, rotulo, ox + Math.cos(medio) * (radio + 13), oy - Math.sin(medio) * (radio + 13) + 4,
    { color: colorTexto, alineacion: 'center' });
}

// Las dos punteadas que cierran el rectangulo entre el origen de un vector y su punta,
// en los ejes del marco. Es lo que hace ver que una fuerza oblicua no es una cosa nueva:
// son dos fuerzas, una por eje. Sobre un lienzo inclinado los ejes son los del plano,
// que es exactamente como se resuelve un plano inclinado.
export function componentes(ctx, l, desde, hasta, { color, guiones = [3, 4] } = {}) {
  exigirColor(color, 'componentes');
  const [x0, y0] = desde, [x1, y1] = hasta;
  ctx.strokeStyle = color;
  ctx.lineWidth = 1;
  ctx.setLineDash(guiones);
  for (const [a, b] of [[[x1, y0], [x1, y1]], [[x0, y1], [x1, y1]]]) {
    ctx.beginPath();
    ctx.moveTo(...l.p(a));
    ctx.lineTo(...l.p(b));
    ctx.stroke();
  }
  ctx.setLineDash([]);
}
```

- [ ] **Paso 4: actualizar el contrato de estado del módulo**

El comentario de cabecera de `dibujo.js` enumera qué deja puesto cada primitiva. Sumá
las cuatro nuevas —`bloque`, `suelo`, `arco`, `componentes`— con lo que cada una toca:
`suelo` deja `globalAlpha` en 1, `componentes` limpia los guiones, `arco` deja lo que
deje `texto` si hay rótulo.

- [ ] **Paso 5: correr la suite y commitear**

```bash
node --test "test/**/*.test.js"
git add docs/motor/dibujo.js test/dibujo.test.js
git commit -m "feat(motor): arco de angulo y descomposicion en componentes"
```

---

## Fase D — Ensayo 4: Diagrama de cuerpo aislado

Es el ensayo que abre la Guía 2, y el salto conceptual más grande del cuatrimestre:
hasta acá el movimiento estaba dado y se lo describía; de acá en adelante el movimiento
es la **consecuencia** de las fuerzas, y para encontrarlo hay que aislar un cuerpo y
dibujar todo lo que lo toca.

Los tres widgets atacan los tres errores clásicos del tema, en orden:

1. dibujar fuerzas que no existen —la "fuerza del movimiento"— y olvidar las que sí;
2. creer que la normal vale siempre *mg*;
3. creer que la fuerza centrípeta es una fuerza aparte que se suma a las demás.

Todos los números salen de `parcial-1/soluciones/verificacion-practico-2.py` del
repositorio `Ejercicios-prácticos`, que está al lado de éste en el mismo directorio
padre. Corrélo con `python verificacion-practico-2.py` y tené su salida a la vista
mientras escribís: **ningún número se escribe de memoria**.

---

### Tarea 9: La página y el widget 1 — el diagrama que se endereza

**Archivos:**
- Crear: `docs/ensayos/cuerpo-aislado.html`
- Modificar: `docs/motor/widget.js` (una línea, ver Paso 2)

**Interfaces:**
- Consume: `crearPagina`, `crearWidget`, `crearEscena`, `conectarTema`, `deslizador`,
  `casilla`, `boton`; de `dibujo.js`: `eje`, `vector`, `vectorPx`, `bloque`, `suelo`,
  `arco`, `componentes`, `texto`, `punteado`; de `lienzo.js`, el `angulo` de la Tarea 6.
- Produce: la página con su encabezado, su sección 01 y su primer widget. Las tareas 10
  y 11 le agregan las secciones 02 y 03 y el cierre.

**El ejercicio (Guía 2, ej. 1).** Un bloque A de 100 kg apoyado en un plano liso
inclinado 30°. Una cuerda AB, paralela al plano, lo sostiene tirando hacia arriba con
tensión *P*. Otra cuerda AC, horizontal, pasa por una polea y cuelga un cuerpo Q de
10 kg, así que tira del bloque hacia afuera del plano con *T_C* = 98,0 N. El bloque está
en equilibrio.

Con el eje *u* a lo largo del plano hacia arriba y el eje *n* perpendicular saliente:

```
P = m_A g sen α + T_C cos α        N = m_A g cos α − T_C sen α
```

Con α = 30°: **T_C = 98,0 N, P = 574,9 N, N = 799,7 N** (y el cuerpo que tira de AB
pesaría 58,7 kg). Verificado en el bloque "Ej 1" del script.

- [ ] **Paso 1: armar el esqueleto de la página**

Copiá `docs/ensayos/movimiento-circular.html` a `docs/ensayos/cuerpo-aislado.html` y
vaciale el contenido, dejando **exactamente**: el script bloqueante del tema en el
`<head>`, los `<link>` de fuentes y de `base.css`, la barra de progreso `#tp-prog`, el
encabezado con el kicker y el botón de tema, el `<h1>`, la bajada, la regla, y el pie con
sus dos enlaces. Usá ya las clases de la Tarea 2 —`.columna`, `.banda`, `.marco-widget`,
`.encabezado-widget`, `.boton`, `.boton-primario`, `.control`, `.lecturas`— en vez de
repetir atributos `style`.

Lo que cambia respecto del original:

- kicker: `Ensayo 4 · Física 1`
- `<title>`: `Diagrama de cuerpo aislado · Física 1`
- `<h1>`: `Diagrama de cuerpo aislado`
- bajada: `Antes de escribir una sola ecuación hay que decidir qué cuerpo se mira y qué lo toca.`
- pie, enlaces de navegación: a la izquierda `Ensayo 3 · Movimiento circular`
  (`movimiento-circular.html`), a la derecha `Portada` (`../index.html`).
- pie, línea de fuentes: `Apunte cap. 3 · <a href="../recursos/resumen-cuerpo-aislado.pdf">hoja resumen</a> · <a href="../recursos/Practico 2_2026.pdf">práctico 2, ej. 1 a 8</a>`

Los dos PDF **tienen que existir en `docs/recursos/`**. Fijate cuáles hay; si falta
alguno, copialo desde `Ejercicios-prácticos` —`parcial-1/practicos/Practico 2_2026.pdf`
y la hoja resumen de cuerpo aislado de `parcial-1/preparacion/`— y agregalo al commit.
Éste es el defecto que se escapó entero en el plan anterior: **verificá los enlaces con
`docs/` servido como raíz**, no con el repositorio.

Dos párrafos de introducción, antes de la sección 01, con el mismo `<p>` que usa el
ensayo de circular. El primero: por qué "aislar" es una decisión y no un trámite — el
diagrama no describe la escena, describe **un** cuerpo, y todo lo que no sea ese cuerpo
aparece sólo por lo que le hace. El segundo: el error de dibujar una flecha "hacia donde
va" — la velocidad no es una fuerza, y en este ensayo no se dibuja ni una sola vez.

- [ ] **Paso 2: que `crearWidget` sepa de ángulos**

La Tarea 6 le dio `angulo` a `crearLienzo`, pero `crearWidget` no lo reenvía: en
`docs/motor/widget.js` destructura `{ xMin = 0, xMax, yMin = 0, yMax }` del resultado de
`encuadre()` y arma el lienzo con esos cuatro. Sumá `angulo = 0` a la destructuración y
pasalo en las **dos** llamadas a `crearLienzo` que hay en la función (la de escala
uniforme y la de escala libre).

Agregá la prueba a `test/widget.test.js`:

```js
test('crearWidget reenvia el angulo del encuadre al lienzo', () => {
  const { widget } = montarWidget({
    encuadre: () => ({ xMin: -1, xMax: 1, yMin: -1, yMax: 1, angulo: 0.5 }),
  });
  assert.equal(widget.lienzo().angulo, 0.5);
});

test('sin angulo en el encuadre, el lienzo queda en cero', () => {
  const { widget } = montarWidget({
    encuadre: () => ({ xMin: -1, xMax: 1, yMin: -1, yMax: 1 }),
  });
  assert.equal(widget.lienzo().angulo, 0);
});
```

`montarWidget` es el ayudante que las pruebas de ese archivo ya usan para fabricar un
canvas falso y una página falsa; mirá cómo lo llaman las que están y seguí esa forma.
Corré `node --test test/widget.test.js`: la primera prueba tiene que FALLAR antes del
cambio (`undefined !== 0.5`) y PASAR después.

- [ ] **Paso 3: la sección 01 y su franja**

`<h2>` de sección: `01 · Cuatro flechas y ninguna más`. Un párrafo antes de la franja que
enumere las cuatro fuerzas del ejercicio y diga en voz alta cuál es el truco de la
casilla: los ejes se pueden **elegir**, y elegirlos a lo largo del plano no es una maña
de cuentas, es mirar el problema desde donde es fácil.

La franja, con la estructura de `.banda` > `.marco-widget`:

- `.encabezado-widget`: `Simulación 1` · `El diagrama que se endereza` ·
  `— la resultante vale cero, y sale de sumar las cuatro flechas.`
- `<canvas id="w1-cv">`
- controles: un deslizador de inclinación (`w1-alfa`, `min="0" max="45" step="1"
  value="30"`, salida `w1-alfa-out` en grados) y una casilla
  (`w1-ejes`, `El plano es el suelo`).
- `.lecturas`: `α`, `T_AB` (`w1-P`), `N` (`w1-N`), `resultante` (`w1-res`).

La lectura de la resultante va en `--blue`, las otras dos en `--ink`. Es la lectura que
el párrafo de abajo manda mirar, así que **tiene que salir de sumar los cuatro vectores
en el código**, no de escribir `0.00`. Si alguien rompiera el modelo, esa lectura se
tiene que mover.

- [ ] **Paso 4: la física y el dibujo del widget 1**

```js
/* ---------- widget 1: el diagrama que se endereza ---------- */

// Guia 2, ej. 1. Bloque A de 100 kg en un plano liso que sube hacia la derecha. La
// cuerda AB va paralela al plano tirando hacia arriba; la cuerda AC es horizontal y tira
// hacia la izquierda con la tension de un cuerpo Q de 10 kg colgado de una polea.
// Verificado en el bloque "Ej 1" de verificacion-practico-2.py:
//   alfa = 30 grados  ->  T_C = 98.0 N,  P = 574.9 N,  N = 799.7 N
const G = 9.8;
const M_A = 100;      // kg, el bloque
const M_Q = 10;       // kg, el cuerpo que cuelga de la cuerda horizontal
const T_C = M_Q * G;  // 98.0 N

// Las cuatro fuerzas, en el marco del plano: x a lo largo hacia arriba, y perpendicular
// saliente. El peso vale (0, -M_A*G) en el mundo, y `l.aMarco` lo trae a este marco --
// esa es exactamente la descomposicion que la casilla hace visible.
function fuerzas(alfa) {
  const sen = Math.sin(alfa), cos = Math.cos(alfa);
  const P = M_A * G * sen + T_C * cos;   // tension de AB, a lo largo del plano
  const N = M_A * G * cos - T_C * sen;   // normal del plano
  return {
    P, N,
    // nombre, vector en el marco del plano, y letra del rotulo
    lista: [
      ['peso',    [-M_A * G * sen, -M_A * G * cos], 'P'],
      ['normal',  [0, N],                           'N'],
      ['AB',      [P, 0],                           'T'],
      ['AC',      [-T_C * cos, T_C * sen],          'Q'],
    ],
  };
}
```

El dibujo. El encuadre es **un cuadrado centrado en el bloque**: al girar el marco, un
punto conserva su distancia al origen, así que un cuadrado centrado en el origen que
contenga todo el dibujo lo sigue conteniendo a cualquier ángulo. Poné el origen del
lienzo en el bloque y elegí el semilado como la distancia del bloque al punto más lejano
que dibujes —la punta del plano— redondeada para arriba; dejá la cuenta escrita en un
comentario, no un número suelto.

La escala de las flechas es **píxeles por newton**, y se deriva dentro de `pintar`, no se
elige: la flecha más larga posible es el peso, `M_A * G = 980 N`, y tiene que caber en el
semialto del área útil.

```js
  function pintar(ctx, l) {
    const p = pagina.paleta();
    const { P, N, lista } = fuerzas(alfa);
    // La flecha mas larga es el peso: 980 N. Se le da el 80% del semialto util, y de ahi
    // sale cuantos pixeles vale un newton. Nada de constantes magicas.
    const semialto = (l.alto - l.margen.T - l.margen.B) / 2;
    const K_FUERZA = (0.8 * semialto) / (M_A * G);
    const O = [0, 0];              // el bloque, en el origen del marco del plano
    const [ox, oy] = l.p(O);

    // El plano y el bloque, dibujados en el marco: en el marco el plano SIEMPRE es
    // horizontal, y lo que gira es el lienzo. Por eso el mismo codigo sirve con la
    // casilla marcada y sin marcar.
    suelo(ctx, l, { color: p.rule, desde: -LADO, hasta: LADO, y: -ALTO_BLOQUE / 2 });
    bloque(ctx, l, O, { ancho: ANCHO_BLOQUE, alto: ALTO_BLOQUE, color: p.band, borde: p.ink });

    // Sin la casilla, el angulo del plano se marca con un arquito rotulado entre la
    // horizontal de la pantalla y la linea del plano. Con la casilla marcada el plano YA
    // es la horizontal, asi que el arco no tiene nada que marcar y no se dibuja.
    if (!verEjes) {
      arco(ctx, l, [-LADO * 0.8, -ALTO_BLOQUE / 2],
        { radio: 34, desde: 0, hasta: alfa, color: p.rule, rotulo: 'α', colorTexto: p.dim });
    }

    // Los ejes del marco solo cuando la casilla esta marcada: sin marcar, los ejes que
    // valen son los de la pantalla y dibujar los del plano confundiria.
    if (verEjes) {
      eje(ctx, l, { color: p.rule, colorTexto: p.dim, etiquetaX: 'u', etiquetaY: 'n' });
      // La descomposicion del peso: las dos punteadas que cierran el rectangulo entre
      // el bloque y la punta de la flecha del peso. Es la unica fuerza que no esta sobre
      // un eje, y es la que el alumno tiene que aprender a partir.
      const [wx, wy] = lista[0][1];
      // `componentes` trabaja en unidades del marco, y las flechas estan en pixeles:
      // hay que traer la punta de vuelta a unidades. Con `escalaUniforme: true` las dos
      // escalas son iguales, pero se divide por la que corresponde a cada eje igual,
      // para que no dependa de eso.
      componentes(ctx, l, O, [wx * K_FUERZA / l.escala.x, wy * K_FUERZA / l.escala.y],
        { color: p.dim });
    }

    // Las cuatro fuerzas, en rojo, con largo en pixeles.
    for (const [, [fx, fy], rotulo] of lista) {
      vectorPx(ctx, ox, oy, ox + fx * K_FUERZA, oy - fy * K_FUERZA,
        { color: p.red, grosor: 2, punta: 9, rotulo });
    }

    // La resultante, en azul. Se suma en el codigo: es la lectura que el parrafo manda
    // mirar, y tiene que moverse si alguien rompe el modelo.
    const rx = lista.reduce((s, f) => s + f[1][0], 0);
    const ry = lista.reduce((s, f) => s + f[1][1], 0);
    const modulo = Math.hypot(rx, ry);
    if (modulo * K_FUERZA > 1) {
      vectorPx(ctx, ox, oy, ox + rx * K_FUERZA, oy - ry * K_FUERZA,
        { color: p.blue, grosor: 2.6, punta: 11, rotulo: 'R' });
    }

    leer('w1-alfa', (alfa * 180 / Math.PI).toFixed(0) + '°');
    leer('w1-P', P.toFixed(1) + ' N');
    leer('w1-N', N.toFixed(1) + ' N');
    // El signo del cero: la cancelacion deja a veces un -1e-13 que toFixed imprimiria
    // como "-0.0". Mismo retoque que usa el widget 1 del ensayo de circular.
    const res = modulo.toFixed(1);
    leer('w1-res', (res === '-0.0' ? '0.0' : res) + ' N');
  }
```

Los tres largos del dibujo —`LADO`, `ANCHO_BLOQUE`, `ALTO_BLOQUE`— son unidades del
marco, no newtons. Elegilos para que el bloque se vea y el plano llegue a los bordes, y
**escribí en un comentario de dónde sale cada uno**. Un cuarto, `K_FUERZA`, ya queda
derivado arriba.

- [ ] **Paso 5: el widget y los controles**

Éste es el punto fino de la tarea, así que leelo dos veces antes de escribir código.

**El dibujo se hace siempre en el marco del plano**, donde el plano es horizontal: `suelo`
va sobre una recta de `y` constante, el bloque está en el origen, y las cuatro fuerzas
son las que devuelve `fuerzas()`, que ya están expresadas en ese marco. Ese código no
cambia nunca.

Lo que cambia es **el ángulo del lienzo**, o sea desde dónde se mira ese marco:

- casilla **sin** marcar: `angulo: alfa`. El eje *x* del marco sale inclinado hacia arriba
  en la pantalla, así que el plano se ve inclinado y el peso —que en el marco vale
  `(−mg sen α, −mg cos α)`— cae apuntando derecho hacia abajo de la pantalla, como tiene
  que ser. Es la vista natural.
- casilla marcada: `angulo: 0`. El marco y la pantalla coinciden, el plano queda
  horizontal, y el peso aparece oblicuo — que es exactamente lo que uno ve cuando gira la
  cabeza para resolver un plano inclinado.

No hay dos dibujos: hay uno solo, visto desde dos lugares. Si te encontrás escribiendo un
`if` que cambia las fuerzas según la casilla, está mal.

```js
  const widget = crearWidget({
    pagina, canvas: el('w1-cv'),
    margen: { L: 40, R: 40, T: 26, B: 26 },
    // Cuadrado y centrado: al girar el marco, la distancia al origen no cambia, asi que
    // un cuadrado centrado en el bloque contiene el dibujo a cualquier angulo. Con
    // escala uniforme, ademas, el bloque no se deforma al girar.
    centrar: true,
    encuadre: () => ({
      xMin: -LADO, xMax: LADO, yMin: -LADO, yMax: LADO,
      // Sin la casilla se mira el marco del plano desde afuera y el plano se ve
      // inclinado; con la casilla el marco y la pantalla coinciden y el plano se
      // endereza. El dibujo de adentro es el mismo en los dos casos.
      angulo: verEjes ? 0 : alfa,
    }),
    dibujar: pintar,
  });

  deslizador({
    entrada: el('w1-alfa'), salida: el('w1-alfa-out'), pagina,
    formato: v => v.toFixed(0) + '°',
    alCambiar: v => { alfa = v * Math.PI / 180; widget.repintar(); },
  });
  casilla({
    entrada: el('w1-ejes'), pagina,
    alCambiar: v => { verEjes = v; widget.repintar(); },
  });
```

Este widget **no tiene escena**: no hay nada que evolucione en el tiempo, así que no
lleva ni `crearEscena`, ni botón de reproducir, ni de reiniciar. Que el widget no se
anime solo al cargar es, acá, gratis.

Mirá la firma real de `casilla` en `docs/motor/controles.js` antes de escribir la
llamada; los nombres de arriba son los que usan los ensayos que ya existen, pero
confirmalos.

- [ ] **Paso 6: el párrafo de cierre de la sección**

Después de la franja, dos párrafos. El primero: que la resultante dé cero no es un
resultado del dibujo, es el **dato** —el bloque está en equilibrio— y de ahí salen las
dos incógnitas; con α = 30° dan *T_AB* = 574,9 N y *N* = 799,7 N, los dos números del
ejercicio 1. El segundo: mirá qué le pasa a *N* al mover el ángulo. No vale *mg*, y no
sólo porque el plano esté inclinado: la cuerda horizontal también le saca carga. La
normal es lo que el plano tiene que hacer para que el bloque no se hunda, y eso depende
de todo lo demás — es el error más caro del tema.

- [ ] **Paso 7: verificar**

Con `docs/` servido como raíz, y proceso de Chrome fresco:

1. A 1280 y a 390 px (con `Emulation.setDeviceMetricsOverride`), en los dos temas: la
   página entra sin desborde horizontal y el canvas no se corta.
2. Con α = 30° y la casilla sin marcar, las lecturas dicen `574.9 N`, `799.7 N` y
   `0.0 N`. Compará contra la salida del script.
3. Sin la casilla, el plano tiene que **verse inclinado** y la flecha del peso tiene que
   apuntar derecho hacia abajo de la pantalla. Comprobá las dos cosas mirando el canvas:
   si el peso sale oblicuo con la casilla sin marcar, tenés el ángulo al revés.
4. Marcá la casilla: el dibujo gira, el plano queda horizontal, el peso queda oblicuo,
   aparecen los ejes *u* y *n* y las dos punteadas. Las tres lecturas **no cambian** — es
   el mismo problema visto de otra manera, y si cambian, el marco rotado está mal.
5. Movelo a α = 0: *T_AB* tiene que dar 98,0 N (queda sólo la cuerda horizontal) y *N*
   tiene que dar 980,0 N. A α = 45°: `P = 100*9.8*sen45 + 98*cos45` y
   `N = 980*cos45 − 98*sen45`; calculalos a mano y compará con lo que muestra.
6. A α = 0 y α = 45°, con y sin casilla, nada se sale del canvas: es la razón por la que
   el encuadre es un cuadrado centrado en el bloque, y hay que comprobarla, no suponerla.
7. Ningún error en la consola.

- [ ] **Paso 8: commit**

```bash
node --test "test/**/*.test.js"
git add docs/ensayos/cuerpo-aislado.html docs/motor/widget.js test/widget.test.js docs/recursos
git commit -m "feat(ensayos): cuerpo aislado, el diagrama que se endereza"
```

---

### Tarea 10: Widget 2 — el ángulo óptimo

El rozamiento y la normal están **acoplados**: tirar de la caja hacia arriba la alivia,
pero desperdicia fuerza horizontal. Hay un ángulo que saca lo mejor de los dos, y no
depende ni de la masa ni de la fuerza: `tan θ = μ`.

**Archivos:**
- Modificar: `docs/ensayos/cuerpo-aislado.html`
- Modificar: `../Ejercicios-prácticos/parcial-1/soluciones/verificacion-practico-2.py`

**Interfaces:**
- Consume: lo mismo que la Tarea 9, más `curva` y `panelesApilados` de `widget.js`.
- Produce: la sección 02 de la página.

**El ejercicio (Guía 2, ej. 9).** Se arrastra una caja por un piso con rozamiento
tirando de una cuerda que forma un ángulo θ con la horizontal. ¿Qué θ da la aceleración
más grande? El script lo resuelve simbólicamente:

```
a(θ) = ( F cos θ − μ (m g − F sen θ) ) / m        da/dθ = 0  ⟺  tan θ = μ
```

y con μ = 0,4 da **θ = 21,8°**.

- [ ] **Paso 1: poner números al ejercicio, en el script**

El ejercicio es simbólico y el widget necesita valores concretos para mostrar lecturas.
La regla del proyecto es que ningún número aparece sin respaldo, así que los valores
entran **en el script de verificación**, no en el HTML. Agregá al bloque "Ej 9" de
`verificacion-practico-2.py`, después de lo que ya está:

```python
# Caso concreto que usa el widget del ensayo 4 (m = 10 kg, F = 40 N, mu = 0.4).
m9, F9, mu9 = 10, 40, Rational(4, 10)
a9c = lambda t: float((F9 * cos(t) - mu9 * (m9 * g - F9 * sin(t))) / m9)
th9 = atan(mu9)
print(f"  concreto: theta* = {float(deg(th9)):.1f} grados   a(theta*) = {a9c(th9):.3f} m/s^2")
print(f"            a(0) = {a9c(rad(0)):.3f}   a(45) = {a9c(rad(45)):.3f}   N(theta*) = {float(m9*g - F9*sin(th9)):.2f} N")
```

Corrélo y **copiá los números que imprime**. Con *F* = 40 N la cuerda nunca levanta la
caja (40 N contra 98 N de peso), así que el modelo vale en todo el rango del deslizador.
Este cambio va en el repositorio `Ejercicios-prácticos`, con su propio commit; anotá en
tu informe que quedó ahí, porque no entra en el commit de la plataforma.

- [ ] **Paso 2: la sección 02 y su franja**

`<h2>`: `02 · La normal no es el peso`. El párrafo previo: casi todo el mundo escribe
`N = mg` sin pensarlo, y casi siempre está mal. Acá se ve por qué de la peor manera
posible para esa costumbre: la normal cambia mientras tirás, el rozamiento cambia con
ella, y el resultado tiene un máximo que no está donde la intuición lo pone.

La franja:

- `.encabezado-widget`: `Simulación 2` · `El ángulo óptimo` ·
  `— tirar derecho no es lo mejor, y el mejor ángulo no depende de cuánto tires.`
- `<canvas id="w2-cv">`
- controles: deslizador de ángulo (`w2-theta`, `min="0" max="60" step="1" value="0"`,
  salida en grados) y deslizador de fuerza (`w2-F`, `min="20" max="60" step="1"
  value="40"`, salida en N).
- `.lecturas`: `θ`, `N` (`w2-N`), `rozamiento` (`w2-f`), `a` (`w2-a`), y
  `mejor θ` (`w2-opt`), este último en `--blue`.

El deslizador de fuerza está para probar la afirmación del encabezado: el máximo se
queda quieto en 21,8° mientras *F* se mueve. Es la lectura `w2-opt`, y **se calcula**,
no se escribe: `Math.atan(MU) * 180 / Math.PI`.

- [ ] **Paso 3: el widget 2**

Dos paneles apilados con `panelesApilados`: arriba la escena —la caja, el piso, la
cuerda, las cuatro fuerzas y la resultante—, abajo el gráfico de *a* contra θ con el
punto actual y el máximo marcados. El panel de abajo necesita **su propio rango
horizontal** (0 a 60 grados, mientras el de arriba está en metros): es exactamente lo
que la Tarea 3 le agregó a `panelesApilados`, y es el primer uso real de esa capacidad.

```js
/* ---------- widget 2: el angulo optimo ---------- */

// Guia 2, ej. 9, con los valores concretos del bloque "Ej 9" de
// verificacion-practico-2.py: m = 10 kg, F = 40 N, mu = 0.4.
//   theta* = 21.8 grados,  a(theta*) = 0.388 m/s^2,  a(0) = 0.080,  a(45) = 0.039
// (copia los valores exactos que imprime el script, no los de este comentario si no
//  coinciden: el script manda.)
const M2 = 10, MU = 0.4;
const THETA_OPT = Math.atan(MU);      // no se escribe 21.8: se calcula

function estado2(theta, F) {
  const N = M2 * G - F * Math.sin(theta);
  const f = MU * N;                       // la caja ya se mueve: rozamiento dinamico
  const a = (F * Math.cos(theta) - f) / M2;
  return { N, f, a };
}
```

En el panel de arriba las cuatro fuerzas van en rojo —peso, normal, la tensión de la
cuerda a ángulo θ, y el rozamiento apuntando hacia atrás— y la resultante en azul, que
queda **horizontal**, porque en vertical no hay aceleración. Escalá las flechas igual que
en el widget 1: la más larga posible es el peso, `M2 * G = 98 N`, y de ahí sale los
píxeles por newton.

En el panel de abajo, `curva` de `t => estado2(t, F).a` entre 0 y 60° (en radianes en el
modelo, en grados en el eje), un `punteado` vertical en el θ actual, y un `cuerpo`
pequeño en el máximo. El eje horizontal va rotulado `θ` y el vertical `a`.

Que el máximo de la curva **no se mueva** al cambiar *F* es el punto entero del widget.

- [ ] **Paso 4: los párrafos de cierre**

Tres cosas, una por párrafo o juntas en dos:

1. Por qué hay un máximo: subir la cuerda cambia dos cosas a la vez y en sentidos
   contrarios — pierde `F(1 − cos θ)` de tirón horizontal y gana `μ F sen θ` de
   rozamiento ahorrado. Al principio el ahorro gana; pasado cierto punto, la pérdida.
2. Que el ángulo óptimo cumpla `tan θ = μ` y no dependa ni de *m* ni de *F* es el
   resultado del ejercicio 9, y es más fuerte de lo que parece: **el mejor ángulo es una
   propiedad del par de superficies**, no de cuánto empujes.
3. Con μ = 0,4 sale 21,8°, y la diferencia contra tirar derecho es grande: con *F* = 40 N,
   la aceleración pasa de *a*(0°) a *a*(21,8°) (poné los dos números que imprime el
   script). Casi cinco veces, por levantar la cuerda veintipico de grados.

- [ ] **Paso 5: verificar**

1. Con θ = 0 y *F* = 40: las lecturas de *N*, rozamiento y *a* contra la salida del
   script. Con θ = 22° (el paso del deslizador es 1°, así que 21,8° no es alcanzable):
   *a* tiene que dar el máximo o a un pelo.
2. Mové *F* de 20 a 60: `mejor θ` se queda en `21.8°` y el punto del máximo en el
   gráfico **no se corre horizontalmente**. Capturá el canvas en *F* = 20 y en *F* = 60 y
   comprobá que la abscisa del máximo es la misma.
3. El panel de abajo llega a 60° en su eje horizontal mientras el de arriba sigue en
   metros: es el rango por panel de la Tarea 3. Si el de abajo hereda el rango del de
   arriba, está mal.
4. 1280 y 390 px, los dos temas, consola limpia.

- [ ] **Paso 6: commit**

```bash
node --test "test/**/*.test.js"
git add docs/ensayos/cuerpo-aislado.html
git commit -m "feat(ensayos): cuerpo aislado, el angulo optimo"
```

Y en el otro repositorio:

```bash
cd ../Ejercicios-prácticos
git add parcial-1/soluciones/verificacion-practico-2.py
git commit -m "test(verificacion): caso concreto del ejercicio 9 para el ensayo 4"
```

---

### Tarea 11: Widget 3 — la resultante apunta al centro, y el cierre

El tercer error: creer que "la fuerza centrípeta" es una fuerza más que hay que agregar
al diagrama. No lo es. El diagrama lleva las fuerzas de siempre —peso, tensión, normal—
y lo que pasa es que **su resultante** apunta al centro. Nada nuevo entra al dibujo.

**Archivos:**
- Modificar: `docs/ensayos/cuerpo-aislado.html`

**Interfaces:**
- Consume: lo mismo que las tareas 9 y 10, más `crearEscena` y `rotuloReproducir`.
- Produce: la página terminada, con sus tres secciones y su cierre.

**El ejercicio (Guía 2, ej. 18).** Un cuerpo de 0,12 kg apoyado en la cara interior de un
cono, atado al vértice por un hilo de 0,5 m que forma 60° con el eje vertical. El
conjunto gira a 10 rpm. Con *r* = *l* sen α:

```
T cos α + N sen α = m g              T sen α − N cos α = m ω² r
```

El script da: **ω = 1,0472 rad/s, r = 0,4330 m, v = 0,4534 m/s, T = 0,6373 N,
N = 0,9900 N**, y la velocidad a la que el cuerpo se despega del cono —donde *N* llega a
cero— **ω = 6,261 rad/s = 59,8 rpm**.

- [ ] **Paso 1: la sección 03 y su franja**

`<h2>`: `03 · La resultante apunta al centro`. Párrafo previo: en el diagrama de un
cuerpo que gira no hay ninguna flecha nueva. Están las tres de siempre; lo que cambia es
que ya no se cancelan, y lo que sobra apunta al centro y vale *m ω² r*. Decilo explícito:
si alguna vez dibujaste una flecha llamada "fuerza centrípeta" **además** de las otras,
contaste dos veces la misma cosa.

La franja:

- `.encabezado-widget`: `Simulación 3` · `El cuerpo en el cono` ·
  `— la flecha azul es horizontal y apunta al eje, siempre.`
- `<canvas id="w3-cv">`
- controles: `Reproducir` (`w3-play`, `.boton-primario`), `Reiniciar` (`w3-reset`,
  `.boton`), y un deslizador de revoluciones por minuto (`w3-rpm`, `min="0" max="59.8"
  step="0.1" value="10"`, salida en rpm).
- `.lecturas`: `ω` (`w3-omega`), `r` (`w3-r`), `T` (`w3-T`), `N` (`w3-N`) en `--red`, y
  `resultante` (`w3-res`) en `--blue`.

El tope del deslizador **es** 59,8 rpm y no es un número redondo por casualidad: es
donde *N* llega a cero. Calculalo, no lo escribas:
`Math.sqrt(G / (L * Math.cos(ALFA))) * 60 / (2 * Math.PI)`, y usalo para poner el `max`
del input desde JS al cargar la página, redondeado a un decimal. Un párrafo tiene que
decir por qué el deslizador se termina ahí.

- [ ] **Paso 2: la física**

```js
/* ---------- widget 3: el cuerpo en el cono ---------- */

// Guia 2, ej. 18. Cuerpo de 0.12 kg en la cara interior de un cono, atado al vertice por
// un hilo de 0.5 m que forma 60 grados con el eje. Verificado en el bloque "Ej 18":
//   10 rpm -> omega = 1.0472 rad/s, r = 0.4330 m, v = 0.4534 m/s, T = 0.6373 N, N = 0.9900 N
//   N = 0  -> omega = sqrt(g/(l cos a)) = 6.261 rad/s = 59.8 rpm
const M3 = 0.12, L3 = 0.5, ALFA3 = 60 * Math.PI / 180;
const R3 = L3 * Math.sin(ALFA3);
const RPM_TOPE = Math.sqrt(G / (L3 * Math.cos(ALFA3))) * 60 / (2 * Math.PI);

// Las dos ecuaciones del cuerpo aislado, resueltas para T y N. El eje vertical no
// acelera; el horizontal acelera hacia el eje del cono con m omega^2 r.
function estado3(omega) {
  const sen = Math.sin(ALFA3), cos = Math.cos(ALFA3);
  const ac = omega * omega * R3;            // aceleracion centripeta
  const T = M3 * (G * cos + ac * sen);
  const N = M3 * (G * sen - ac * cos);
  return { T, N, ac, r: R3, v: omega * R3 };
}
```

Comprobá a mano, antes de seguir, que `estado3(1.0472)` da `T = 0.6373` y `N = 0.9900`.
Si no da, la resolución del sistema está mal y todo lo que sigue miente.

- [ ] **Paso 3: el dibujo**

Vista **de frente**, en el plano que contiene el eje del cono y el cuerpo: se ven las dos
paredes del cono como dos rectas que salen del vértice, el hilo, y el cuerpo apoyado. El
cuerpo va y viene de un lado al otro del eje mientras gira —es la proyección de un
movimiento circular sobre el plano de la pantalla—, así que la escena **sí** tiene
`crearEscena`, con `duracion` igual al período `2π/ω` y `alCambiar` que reetiqueta el
botón con `rotuloReproducir`.

Cuando el cuerpo está del lado derecho, las tres fuerzas se dibujan en rojo desde él:

- el peso, `(0, −M3*G)`, hacia abajo;
- la tensión, de módulo *T*, a lo largo del hilo hacia el vértice;
- la normal del cono, de módulo *N*, perpendicular a la pared, apuntando **hacia arriba
  y hacia afuera del eje**. El cono tiene el vértice arriba y se abre hacia abajo, y el
  cuerpo está apoyado en su cara interior: la pared lo empuja hacia el interior del
  cono, que es hacia arriba y lejos del eje. Si te sale apuntando hacia el eje, tenés el
  signo al revés, y el widget entero va a mentir — comprobalo contra las dos ecuaciones,
  donde *N* aporta `+N sen α` en vertical y `−N cos α` del lado centrípeto.

Y la resultante en azul, sumando las tres, que tiene que salir horizontal apuntando al
eje. Sumala en el código, como en el widget 1: la lectura `w3-res` es la prueba.

La escala de flechas, otra vez derivada. Acá la más larga no es el peso: es la tensión
en el tope del deslizador, porque *T* crece con ω² mientras el peso no se mueve. Evaluá
`estado3(2 * Math.PI * RPM_TOPE / 60).T` una vez al armar el widget y usá **ese** módulo
para calcular los píxeles por newton; dejá la cuenta escrita. Así ninguna flecha se sale
del canvas en ninguna posición del deslizador, que es la razón de derivarla en vez de
elegirla.

Un detalle que hace la mitad del trabajo pedagógico: cuando el cuerpo cruza al lado
izquierdo, las tres flechas se dan vuelta en horizontal y la azul sigue apuntando al eje.
Que el lector vea la flecha azul cambiar de sentido mientras el cuerpo pasa de un lado al
otro es lo que convierte "apunta al centro" en algo visto y no leído.

- [ ] **Paso 4: los párrafos de cierre de la sección**

1. Los números a 10 rpm, los del ejercicio: *r* = 0,433 m, *v* = 0,453 m/s,
   *T* = 0,637 N, *N* = 0,990 N.
2. Subí las revoluciones: *T* crece y *N* **baja**. El cono aprieta cada vez menos,
   porque el hilo se va haciendo cargo de la vuelta él solo. A 59,8 rpm *N* llega a cero:
   de ahí para arriba el cuerpo se despega y el cono deja de tocarlo. El deslizador se
   frena ahí porque pasado ese punto estas ecuaciones ya no describen nada.
3. Repetí la idea central: en ningún momento se dibujó una flecha llamada "centrípeta".
   Las flechas son las tres de siempre; "centrípeta" es un adjetivo de la **resultante**,
   no un nombre de fuerza.

- [ ] **Paso 5: los cuatro ejercicios que no tienen widget**

Cinco ejercicios del práctico 2 caen en este ensayo y no llegan a widget, porque son
variantes de lo que las tres simulaciones ya muestran. No por eso quedan afuera: van en
un bloque de prosa antes del cierre, con `<h2>` `Cinco variantes del mismo dibujo`, un
párrafo por cada uno, con sus números del script. Un ensayo que dice cubrir un tema y
deja cinco ejercicios sin mencionar no lo cubre.

1. **Ej. 6 — el límite de la cuerda.** Una bola de 10 kg colgando de un hilo que aguanta
   500 N. Si se la acelera, la tensión crece; el hilo se corta cuando la aceleración llega
   a `a = √(T² − (mg)²)/m = 49,03 m/s²`, y en ese instante el hilo forma 78,7° con la
   vertical. Es el widget 1 sin plano: las mismas dos ecuaciones, con la incógnita del
   otro lado.
2. **Ej. 8 — el rozamiento estático no tiene fórmula.** Un bloque de 5 N apretado contra
   una pared vertical con 12 N horizontales, con μ = 0,6. El rozamiento disponible llega
   hasta `0,6 × 12 = 7,2 N`, que es más que los 5 N de peso, así que el bloque **no se
   mueve** y el rozamiento vale 5 N, no 7,2. `μN` es el techo, no el valor. La fuerza
   total que la pared le hace es `√(12² + 5²) = 13,0 N`.
3. **Ej. 10 — dos que bajan atados.** Dos bloques unidos bajando por el mismo plano con
   coeficientes distintos. La tensión sale
   `T = m_A m_B (μ_B − μ_A) g cos α / (m_A + m_B)`: se anula cuando los dos coeficientes
   son iguales, y cambia de signo según cuál frene más. La cuerda sólo trabaja si los dos
   bloques querrían bajar a ritmos distintos.
4. **Ej. 13 — el círculo vertical.** Una esfera atada a una cuerda de largo *R* gira en
   un plano vertical alrededor de un punto fijo. Con θ medido desde la vertical de abajo,
   la ecuación radial es `T − mg cos θ = m v²/R`, así que `T = m(v²/R + g cos θ)`: máxima
   abajo, donde la cuerda tiene que dar la vuelta **y** sostener el peso, y mínima arriba,
   donde el peso ayuda. Arriba la cuerda se afloja si `v² < gR`, y ése es el límite por
   debajo del cual la esfera no completa la vuelta. Es el widget 3 con la gravedad
   cambiando de papel según dónde esté el cuerpo.
5. **Ej. 19 — un bloque sobre otro.** A (40 N) apoyado sobre B (80 N), unidos por una
   cuerda que pasa por una polea, con μ_d = 0,25. El rozamiento entre los dos vale
   `0,25 × 40 = 10 N`, y ése es el valor de la tensión; para arrastrar a B hacen falta
   `10 + 10 = 20 N` si B está sobre una mesa lisa, y `50 N` si además hay rozamiento con
   el piso, que carga los 120 N de los dos juntos.

Los valores —49,03; 78,7; 7,2; 13,0; 10, 20 y 50— están en los bloques "Ej 6", "Ej 8",
"Ej 10" y "Ej 19" del script. Corrélo y copialos de ahí.

El ejercicio 13 es el único de los cinco que no tiene bloque propio, porque el práctico lo
pide simbólico. Agregaselo, para que la fórmula que escribís en la página tenga el mismo
respaldo que todo lo demás:

```python
# ---------------------------------------------------------------- Ej 13
title("Ej 13: circulo vertical, tension en funcion del angulo")
mv, Rv, vv, thv = symbols("m R v theta", positive=True)
Tsym = symbols("T")
# Ecuacion radial, con theta medido desde la vertical de abajo: lo que apunta al centro
# es la tension menos la componente radial del peso.
Tv = solve(Eq(Tsym - mv * g * cos(thv), mv * vv**2 / Rv), Tsym)[0]
print("  T =", sp.simplify(Tv))
print("  abajo (theta=0):", sp.simplify(Tv.subs(thv, 0)), "   arriba (theta=pi):", sp.simplify(Tv.subs(thv, pi)))
print("  la cuerda se afloja arriba si v^2 < g R")
```

Va con el commit del práctico, junto a los otros dos cambios del script que piden las
tareas 10 y 15.

- [ ] **Paso 6: el cierre del ensayo**

Con el mismo formato que los cierres de los tres ensayos anteriores —mirá cómo los
escribe `movimiento-circular.html`—, un `<h2>` `Para tener a mano` y una lista de reglas
operativas, cortas, cada una ganada en una de las tres secciones:

- Elegí el cuerpo primero. Todo lo que no sea ese cuerpo entra al dibujo sólo como una
  flecha que lo toca.
- Las fuerzas de contacto —normal, rozamiento— no tienen valor propio: valen lo que haga
  falta, y eso se averigua al final, no al principio.
- `N = mg` es un caso particular, no una fórmula. Vale sólo si el piso es horizontal y
  nada más empuja o tira en vertical.
- Los ejes se eligen. Sobre un plano inclinado, a lo largo y perpendicular al plano; en
  un problema circular, radial y tangencial.
- La aceleración centrípeta no es una fuerza. Va del lado derecho de `F = ma`, con las
  demás aceleraciones.
- El rozamiento dinámico vale `μ N` y apunta contra el movimiento; el estático vale lo
  que haga falta hasta `μ_e N`, y ahí se acaba.

- [ ] **Paso 7: verificar la página entera**

1. Las lecturas del widget 3 a 10 rpm contra la salida del script, cifra por cifra.
2. El tope del deslizador: llevalo al máximo y comprobá que *N* llega a `0.00 N` y la
   resultante queda horizontal.
3. Los tres widgets pintan al cargar y **ninguno se anima solo**; el widget 3 arranca en
   `Reproducir`, no en `Seguir`.
4. Los dos temas, 1280 y 390 px, sin desborde. Consola limpia en las dos anchuras.
5. Con `docs/` servido como raíz: los dos enlaces del pie y los dos PDF resuelven.
6. La barra de progreso llega a 100 % al final de la página.

- [ ] **Paso 8: commit**

```bash
node --test "test/**/*.test.js"
git add docs/ensayos/cuerpo-aislado.html
git commit -m "feat(ensayos): cuerpo aislado, la resultante apunta al centro"
```

Y en el otro repositorio, el bloque del ejercicio 13:

```bash
cd ../Ejercicios-prácticos
git add parcial-1/soluciones/verificacion-practico-2.py
git commit -m "test(verificacion): ejercicio 13, circulo vertical"
```

---

## Fase E — Ensayo 5: Sistemas acoplados

Dos cuerpos atados son **un** problema, pero se resuelve haciendo **dos** diagramas. Ese
es el tema entero, y el error clásico es querer resolverlo con un solo diagrama del
conjunto: sirve para la aceleración y no sirve para la tensión, que es justo lo que casi
siempre preguntan.

---

### Tarea 12: La página y el widget 1 — cortar la cuerda

**Archivos:**
- Crear: `docs/ensayos/sistemas-acoplados.html`

**Interfaces:**
- Consume: todo lo de la Fase D, más `crearEscena`, `rotuloReproducir` y el `angulo` del
  lienzo.
- Produce: la página con su encabezado, la sección 01 y el primer widget.

**El ejercicio (Guía 2, ej. 4).** Un cuerpo A de 8 kg sobre un plano liso inclinado 37°,
atado por una cuerda que pasa por una polea en la cima y sostiene a un cuerpo B de 4 kg
que cuelga. ¿Para dónde arranca el sistema, con qué aceleración, y cuánto vale la
tensión?

Del script, bloque "Ej 4": `m_A g sen 37° = 47,18 N` contra `m_B g = 39,20 N`, así que
**A baja y B sube**; **a = 0,665 m/s²** y **T = 41,86 N**.

- [ ] **Paso 1: el esqueleto**

Igual que en la Tarea 9, copiando el esqueleto de `cuerpo-aislado.html` —que ya usa las
clases de la Tarea 2— y cambiando:

- kicker `Ensayo 5 · Física 1`, `<title>` `Sistemas acoplados · Física 1`,
  `<h1>` `Sistemas acoplados`
- bajada: `Dos cuerpos atados son un problema solo, y se resuelve haciendo dos dibujos.`
- pie: a la izquierda `Ensayo 4 · Diagrama de cuerpo aislado`
  (`cuerpo-aislado.html`), a la derecha `Portada`; línea de fuentes con la hoja resumen
  de sistemas acoplados y `práctico 2, ej. 2 a 7`.

Dos párrafos de introducción. El primero: la cuerda ideal —sin masa, inextensible— hace
dos cosas y hay que decirlas por separado, porque cada una es una ecuación distinta.
Inextensible significa que las dos aceleraciones tienen el **mismo módulo**: es un
vínculo geométrico, no una fuerza. Sin masa significa que la tensión es la **misma en los
dos extremos**: eso sí sale de la segunda ley aplicada a la cuerda, con `m = 0`.
El segundo: por qué el diagrama del conjunto no alcanza. La tensión es interna, se
cancela sola en la suma, y por eso el conjunto da la aceleración pero se queda mudo sobre
*T*. Para que *T* aparezca hay que cortar.

- [ ] **Paso 2: la sección 01 y su franja**

`<h2>`: `01 · Cortar la cuerda`. Párrafo previo: mirá primero quién gana. No hace falta
ninguna cuenta fina: de un lado tira `m_A g sen α`, del otro `m_B g`, y con los números
del ejercicio son 47,18 N contra 39,20 N. Gana A, y por poco. Después de decidir el
sentido recién se puede escribir la segunda ley, porque el signo de *a* depende de haber
elegido un sentido positivo y haberlo respetado en los dos cuerpos.

La franja:

- `.encabezado-widget`: `Simulación 1` · `Cortar la cuerda` ·
  `— las dos tensiones se calculan por separado, de dos ecuaciones distintas, y dan lo mismo.`
- `<canvas id="w1-cv">`
- controles: `Reproducir` (`w1-play`), `Reiniciar` (`w1-reset`), un deslizador de masa de
  B (`w1-mb`, `min="0" max="10" step="0.1" value="4"`, salida en kg) y una casilla
  `w1-aislar` con la etiqueta `Aislar los cuerpos`.
- `.lecturas`: `a` (`w1-a`), `T desde A` (`w1-ta`) y `T desde B` (`w1-tb`), las dos en
  `--red`, y `diferencia` (`w1-dif`) en `--dim`.

Las dos lecturas de tensión son el corazón del widget. **No se copian una de la otra**:
cada una sale de la ecuación de su cuerpo, y la tercera lectura es la resta. Que la resta
dé `0.00 N` es la prueba, a la vista, de que la cuerda transmite la misma tensión a los
dos lados — y si alguien rompiera una de las dos ecuaciones, la resta dejaría de dar
cero. Es la misma clase de lectura que `r̂ · v` en el ensayo de circular.

- [ ] **Paso 3: la física**

```js
/* ---------- widget 1: cortar la cuerda ---------- */

// Guia 2, ej. 4. A (8 kg) en un plano liso de 37 grados, atado por una cuerda que pasa
// por una polea en la cima y sostiene a B, que cuelga. Verificado en el bloque "Ej 4":
//   m_A g sen37 = 47.18 N  vs  m_B g = 39.20 N  ->  A baja, B sube
//   a = 0.665 m/s^2   T = 41.86 N
const G = 9.8;
const M_A = 8, ALFA = 37 * Math.PI / 180;

// El sentido positivo: A baja por el plano y B sube. Si `a` sale negativa, el sistema
// va para el otro lado -- y eso pasa de verdad al subir el deslizador de m_B, que es
// justamente lo que el widget deja probar.
function estadoPlano(mB) {
  const a = (M_A * G * Math.sin(ALFA) - mB * G) / (M_A + mB);
  // Las dos tensiones, cada una de la ecuacion de SU cuerpo. Estan escritas por separado
  // a proposito: la lectura de la pagina muestra la resta, y esa resta es la prueba.
  const tDesdeA = M_A * (G * Math.sin(ALFA) - a);   // m_A a = m_A g sen(alfa) - T
  const tDesdeB = mB * (G + a);                      // m_B a = T - m_B g
  return { a, tDesdeA, tDesdeB };
}
```

Con `estadoPlano(4)` tiene que dar `a = 0.665` y las dos tensiones `41.86`. Comprobalo en
la consola antes de dibujar nada.

Un detalle que el párrafo de cierre usa: hay una masa de B para la cual el sistema queda
quieto, y es `M_A * Math.sin(ALFA)` —unos 4,8 kg—. Calculala, no la escribas.

- [ ] **Paso 4: el dibujo y la animación**

Acá el lienzo va **sin ángulo**, al revés que en el ensayo 4. La escena tiene un plano
inclinado y un cuerpo colgando en vertical al mismo tiempo, y no hay un marco girado que
le sirva a los dos: si girás el lienzo, el peso de B deja de apuntar hacia abajo de la
pantalla. Dibujá el plano como una recta a 37° y el bloque A con
`bloque(..., { angulo: ALFA })`, que para eso el bloque acepta ángulo propio.

La escena se anima: los dos cuerpos parten del reposo y se mueven con aceleración
constante *a*, A a lo largo del plano y B en vertical, recorriendo lo mismo. Elegí la
`duracion` de modo que B llegue al piso o A a la polea —la que pase antes— y dejá la
cuenta escrita; con `velocidad` ajustada para que se vea, como hacen los otros ensayos.
Las flechas de velocidad, en azul, salen de `a * t`.

Con la casilla marcada, el canvas se parte en dos mitades y muestra **dos diagramas de
cuerpo aislado**, uno por cuerpo, cada uno con sus fuerzas en rojo:

- A: peso, normal, y la tensión tirando hacia arriba del plano.
- B: peso, y la tensión tirando hacia arriba.

Y en cada uno, la resultante en azul, que no es cero: es `m a` de ese cuerpo. Rotulá las
dos flechas de tensión con la misma letra *T* y dibujalas del mismo largo — es la única
manera de que se vea que son la misma.

Los dos diagramas van **lado a lado**, y `panelesApilados` apila en vertical, así que no
sirve acá. Armalos con **un solo lienzo** y dos orígenes distintos, uno a la izquierda y
otro a la derecha del encuadre. Es más simple que agregarle un modo horizontal al motor,
y el motor no necesita crecer para esto.

- [ ] **Paso 5: los párrafos de cierre**

1. Los números: con B de 4 kg, *a* = 0,665 m/s² y *T* = 41,86 N. Compará esa tensión
   con el peso de B, que vale 39,20 N: la cuerda tira **más** de lo que B pesa, y tiene
   que ser así, porque B no está colgado quieto, está subiendo cada vez más rápido. Una
   cuerda que sostiene tira igual al peso; una que además acelera hacia arriba, tira más.
   Escribí la comparación con los dos números.
2. Subí el deslizador de B: en algún punto el sistema se frena y después se da vuelta. El
   punto de equilibrio está en `m_B = m_A sen α ≈ 4,8 kg`, y no es casualidad que ahí la
   aceleración cambie de signo: es la misma comparación de fuerzas del principio, ahora
   como ecuación.
3. Que las dos tensiones den lo mismo no es una comprobación de que la cuenta esté bien:
   es lo que significa "cuerda sin masa". Si la cuerda pesara, las dos puntas tirarían
   distinto, y esa diferencia sería la que acelera a la cuerda misma — que es el
   ejercicio 3, donde `F_BC / F = M / (M + m)`.

- [ ] **Paso 6: verificar**

1. Lecturas con `m_B = 4`: `0.665`, `41.86`, `41.86`, `0.00`. Contra el script.
2. Deslizador a `m_B = 4.8`: *a* cerca de cero. A `m_B = 8`: *a* negativa, y la animación
   va para el otro lado — comprobá que los cuerpos se mueven en el sentido contrario y no
   simplemente al revés en las flechas.
3. `m_B = 0`: *T* tiene que dar `0.00 N` en las dos lecturas y *a* el valor de caída libre
   por el plano, `G * sen 37° = 5.90 m/s²`.
4. La casilla parte el canvas y las dos flechas de tensión tienen el mismo largo en
   píxeles. Medilo, no lo mires.
5. 1280 y 390 px, los dos temas, consola limpia, ningún widget animándose solo al cargar.

- [ ] **Paso 7: commit**

```bash
node --test "test/**/*.test.js"
git add docs/ensayos/sistemas-acoplados.html docs/recursos
git commit -m "feat(ensayos): sistemas acoplados, cortar la cuerda"
```

---

### Tarea 13: Widget 2 — cada cuerda lleva lo que tiene adelante, y el cierre

**Archivos:**
- Modificar: `docs/ensayos/sistemas-acoplados.html`

**Interfaces:**
- Consume: lo mismo que la Tarea 12.
- Produce: la página terminada.

**El ejercicio (Guía 2, ej. 7).** Tres bloques de 20, 20 y 30 kg unidos en fila por dos
cuerdas, y una tercera cuerda adelante que tira con 60 N. Del bloque "Ej 7" del script:

- tirando en **horizontal**: `a = 0,857 m/s²`, `T1 = 17,14 N`, `T2 = 34,29 N`
- tirando en **vertical**, hacia arriba: `a = −8,943 m/s²` (el conjunto baja, porque
  60 N no alcanzan para sostener 70 kg), y `T1 = 17,14 N`, `T2 = 34,29 N` — **los mismos
  valores**.

Que las dos tensiones sean idénticas en los dos casos es el resultado más lindo del
ejercicio, y el widget existe para hacerlo evidente.

- [ ] **Paso 1: la sección 02 y su franja**

`<h2>`: `02 · Cada cuerda lleva lo que tiene adelante`. Párrafo previo: una cuerda
intermedia no "reparte" la fuerza. Tiene un trabajo concreto y acotado — acelerar todo lo
que cuelga de ella hacia adelante — y su tensión es exactamente la masa de eso por la
aceleración. De ahí que la cuerda de más atrás sea la que menos tensión soporta, que es
al revés de lo que casi todos dicen la primera vez.

La franja:

- `.encabezado-widget`: `Simulación 2` · `Tres bloques y dos cuerdas` ·
  `— cambiá a vertical: la aceleración se da vuelta y las tensiones no se mueven.`
- `<canvas id="w2-cv">`
- controles: un deslizador de fuerza (`w2-F`, `min="0" max="900" step="10" value="60"`,
  salida en N) y una casilla `w2-vertical` con la etiqueta `Tirar hacia arriba`.
- `.lecturas`: `a` (`w2-a`), `T1` (`w2-t1`), `T2` (`w2-t2`), `T3` (`w2-t3`).

`T3` es la fuerza aplicada misma: se muestra para que se vea la escalera 17,14 / 34,29 /
60 y que cada escalón es proporcional a la masa acumulada.

- [ ] **Paso 2: la física**

```js
/* ---------- widget 2: tres bloques y dos cuerdas ---------- */

// Guia 2, ej. 7. Tres bloques de 20, 20 y 30 kg en fila, unidos por dos cuerdas, con 60 N
// tirando del de adelante. Verificado en el bloque "Ej 7":
//   horizontal: a = 0.857 m/s^2, T1 = 17.14 N, T2 = 34.29 N
//   vertical:   a = -8.943 m/s^2, T1 = 17.14 N, T2 = 34.29 N   <- las mismas tensiones
const MASAS = [20, 20, 30];                       // del de adelante hacia atras
const M_TOTAL = MASAS.reduce((s, m) => s + m, 0); // 70 kg

// Una sola cuenta para los dos casos. En vertical la gravedad entra restando en la
// aceleracion Y sumando en cada tension, y las dos entradas se cancelan exactamente:
// por eso las tensiones no se mueven. El codigo no lo asume -- lo calcula, y el widget
// deja verlo.
function estadoTren(F, vertical) {
  const a = vertical ? (F - M_TOTAL * G) / M_TOTAL : F / M_TOTAL;
  const acumulada = [];
  let suma = 0;
  for (const m of MASAS) { suma += m; acumulada.push(suma); }
  // T_i acelera todo lo que tiene ADELANTE (incluido su propio bloque siguiente): en
  // vertical, ademas, tiene que sostener ese mismo peso.
  const tension = i => acumulada[i] * (vertical ? a + G : a);
  return { a, T: [tension(0), tension(1), tension(2)] };
}
```

Comprobá en la consola: `estadoTren(60, false)` da `a = 0.857`,
`T = [17.14, 34.29, 60.00]`; `estadoTren(60, true)` da `a = -8.943` y **las mismas tres
tensiones**. Si `T[2]` no da
exactamente la fuerza aplicada, el modelo está mal, y esa es la mejor prueba interna que
tiene este widget: la última tensión **tiene** que reproducir el dato.

- [ ] **Paso 3: el dibujo**

En horizontal: los tres bloques en fila sobre un `suelo`, las dos cuerdas entre ellos
como segmentos, y la tercera saliendo hacia la derecha. Sobre cada cuerda, una flecha
roja en cada extremo, apuntando hacia afuera —la cuerda tira de los dos bloques que une,
en sentidos opuestos— con largo proporcional a su tensión. Sobre el conjunto, la flecha
azul de la resultante.

En vertical: los mismos tres bloques colgando uno del otro, con el peso de cada uno en
rojo, y la escena rotada 90°. **No** uses `angulo` del lienzo para esto: el peso seguiría
apuntando "abajo" del marco, que ya no es abajo de la pantalla, y el dibujo mentiría. Son
dos disposiciones distintas de los mismos bloques; escribí las dos.

La escala de flechas: la más larga posible es la fuerza aplicada en el tope del
deslizador, 900 N. Derivala de ahí.

- [ ] **Paso 4: el cierre del ensayo**

Los párrafos de la sección 02:

1. La escalera de tensiones: 17,14 / 34,29 / 60 N. Cada una es la masa acumulada por la
   aceleración, y la de más atrás es la más chica — la cuerda que menos aguanta es la que
   menos carga lleva.
2. Pasá a vertical. La aceleración se da vuelta: 60 N contra 686 N de peso total, el
   conjunto baja con 8,94 m/s². Y las tensiones **no se mueven**. La razón está en la
   cuenta: en vertical cada tensión vale `M_acumulada (a + g)`, y `a + g` vale lo mismo
   que valía `a` en horizontal, porque `a = F/M − g`. La gravedad entra dos veces y se
   cancela.
3. Y la generalización, que es lo que hay que llevarse: **la tensión de una cuerda no
   depende de qué hay detrás de ella**. Ni de la masa de atrás, ni de si hay gravedad. Es
   lo que hace falta para acelerar lo de adelante, y nada más. En el ejercicio 5, dos
   bloques en contacto con 3 N empujando 2 kg + 1 kg dan `a = 1 m/s²`, y la fuerza de
   contacto vale 1 N si empujás el de 2 kg y 2 N si empujás el de 1 kg: la misma idea,
   con "adelante" cambiado de lado.

Y el cierre de la página, con el `<h2>` `Para tener a mano` y sus reglas:

- Un sistema acoplado se resuelve con un diagrama **por cuerpo**, no con uno del
  conjunto. El del conjunto sirve sólo para la aceleración.
- La cuerda ideal aporta dos cosas distintas: inextensible da un vínculo entre
  aceleraciones; sin masa da una tensión igual en los dos extremos.
- Elegí un sentido positivo **antes** de escribir nada, y respetalo en los dos cuerpos.
  Si la aceleración sale negativa, el sistema va para el otro lado y la cuenta ya lo dijo.
- La tensión de una cuerda es la masa de lo que tiene adelante por la aceleración —más el
  peso de eso, si la cosa va en vertical.
- La polea ideal sólo cambia la dirección de la cuerda. No cambia el módulo de la
  tensión.

- [ ] **Paso 5: verificar**

1. Las lecturas en los dos modos con `F = 60`, contra el script, cifra por cifra.
2. `T3` tiene que ser igual a la fuerza del deslizador en todo el rango. Probá tres
   valores.
3. Mové la casilla: capturá el canvas antes y después y comprobá que las flechas de `T1`
   y `T2` tienen el **mismo largo en píxeles** en los dos modos. Es la afirmación del
   encabezado y es medible.
4. `F = 900` en vertical: `a = 900/70 − 9.8 = 3.06 m/s²`, positiva, el conjunto sube.
   Verificá que el dibujo lo refleje.
5. Página entera: 1280 y 390 px, dos temas, consola limpia, enlaces del pie con `docs/`
   como raíz, barra de progreso al 100 % abajo.

- [ ] **Paso 6: commit**

```bash
node --test "test/**/*.test.js"
git add docs/ensayos/sistemas-acoplados.html
git commit -m "feat(ensayos): sistemas acoplados, tres bloques y dos cuerdas"
```

---

## Fase F — Ensayo 6: Fuerzas que dependen de la posición

La Guía 2 no termina en las cuerdas. Le quedan resortes, gravitación y movimiento
armónico simple, que en los prácticos parecen tres temas sueltos y son uno solo: hasta
acá toda fuerza era un dato constante, y ahora la fuerza **depende de dónde está el
cuerpo**. Cambiar eso cambia todo el método, porque la aceleración deja de ser un número
y pasa a ser una función de la posición.

Dos widgets: el resorte, donde esa dependencia es lineal y produce una oscilación; y la
gravedad, donde va como `1/r²` y produce un punto donde no tira nada.

---

### Tarea 14: La página y el widget 1 — el resorte que se dibuja a sí mismo

**Archivos:**
- Crear: `docs/ensayos/fuerzas-de-posicion.html`

**Interfaces:**
- Consume: `panelesApilados` de `widget.js` con el rango horizontal por panel de la
  Tarea 3, `crearEscena`, `curva`, `eje`, `bloque`, `cuerpo`, `punteado`, `vectorPx`.
- Produce: la página con su encabezado, la sección 01 y el primer widget.

**El ejercicio (Guía 2, ej. 17).** Un bloque de 2 kg atado a un resorte de
*k* = 8 N/m sobre una mesa lisa. La posición de equilibrio está en 0,40 m; se lo lleva a
0,55 m y se lo suelta. Del bloque "Ej 17" del script:

**ω = 2 rad/s, T = 3,142 s, f = 0,318 Hz, A = 0,15 m**,
`x(t) = 0,40 + 0,15 cos(2t)`, **v_max = 0,3 m/s**, **a_max = 0,6 m/s²**, y los extremos
del movimiento en **0,25 m y 0,55 m**.

- [ ] **Paso 1: el esqueleto**

Como en las tareas 9 y 12:

- kicker `Ensayo 6 · Física 1`, `<title>` `Fuerzas que dependen de la posición · Física 1`,
  `<h1>` `Fuerzas que dependen de la posición`
- bajada: `Cuando la fuerza cambia según dónde está el cuerpo, la aceleración deja de ser un número.`
- pie: a la izquierda `Ensayo 5 · Sistemas acoplados` (`sistemas-acoplados.html`), a la
  derecha `Portada`; línea de fuentes con `práctico 2, ej. 11 a 18`.

Dos párrafos de introducción. El primero: en toda la guía hasta acá, `a` salía de una
cuenta con números fijos y de ahí las fórmulas de siempre. Con una fuerza que depende de
`x`, esa salida se cierra: `a` depende de `x`, y `x` depende de `a`. El segundo: la buena
noticia es que los dos casos que pide la guía —el resorte y la gravedad— tienen solución
conocida, y las dos se entienden mirando, no derivando. En el resorte, `F = −kx` produce
un coseno; en la gravedad, `F ∝ 1/r²` produce un punto de equilibrio donde no hay nada.

- [ ] **Paso 2: la sección 01 y su franja**

`<h2>`: `01 · La fuerza que empuja siempre hacia el centro`. Párrafo previo: la ley de
Hooke no dice que el resorte tire fuerte, dice que tira **proporcional al estiramiento y
en contra**. Ese "en contra" es lo que hace que el bloque no se quede quieto en el
equilibrio: llega ahí con velocidad, se pasa, y entonces el resorte tira para el otro
lado. Eso, repetido, es la oscilación.

La franja:

- `.encabezado-widget`: `Simulación 1` · `El resorte y sus tres gráficos` ·
  `— la aceleración es el espejo de la posición, escalado por ω².`
- `<canvas id="w1-cv">`
- controles: `Reproducir` (`w1-play`), `Reiniciar` (`w1-reset`), deslizador de constante
  (`w1-k`, `min="2" max="20" step="0.5" value="8"`, salida en N/m) y deslizador de masa
  (`w1-m`, `min="0.5" max="5" step="0.1" value="2"`, salida en kg).
- `.lecturas`: `ω` (`w1-omega`), `T` (`w1-T`), `f` (`w1-f`), `v máx` (`w1-vmax`) en
  `--blue`, `a máx` (`w1-amax`) en `--red`, y `a + ω²(x−x₀)` (`w1-mas`) en `--dim`.

La última lectura es la prueba: `a + ω²(x − x₀) = 0` **es** la definición de movimiento
armónico simple, y tiene que salir de evaluar las dos funciones en el instante actual, no
de escribir un cero. Si alguien le cambiara el signo a la aceleración, esa lectura se
movería.

- [ ] **Paso 3: la física**

```js
/* ---------- widget 1: el resorte y sus tres graficos ---------- */

// Guia 2, ej. 17. Bloque de 2 kg, resorte de 8 N/m, equilibrio en 0.40 m, soltado desde
// 0.55 m. Verificado en el bloque "Ej 17" de verificacion-practico-2.py:
//   omega = 2 rad/s, T = 3.142 s, f = 0.318 Hz, A = 0.15 m
//   x(t) = 0.40 + 0.15 cos(2t), v_max = 0.3 m/s, a_max = 0.6 m/s^2, extremos 0.25 y 0.55
const X0 = 0.40;      // m, posicion de equilibrio: ahi el resorte no tira
const A_OSC = 0.15;   // m, amplitud: 0.55 - 0.40, la distancia a la que se lo lleva

// Soltado desde el reposo en el extremo: la solucion arranca en el maximo, asi que es un
// coseno puro, sin fase. v y a son sus derivadas -- las mismas que el ensayo 1 dibujaba
// a mano, ahora con una funcion que sale de la fisica y no de un menu.
function oscilador(k, m) {
  const omega = Math.sqrt(k / m);
  return {
    omega,
    periodo: 2 * Math.PI / omega,
    frecuencia: omega / (2 * Math.PI),
    x: t => X0 + A_OSC * Math.cos(omega * t),
    v: t => -A_OSC * omega * Math.sin(omega * t),
    a: t => -A_OSC * omega * omega * Math.cos(omega * t),
  };
}
```

Comprobá en la consola que `oscilador(8, 2)` da `omega = 2`, `periodo = 3.1416`,
`frecuencia = 0.3183`, y que `v(periodo/4) = -0.3` y `a(0) = -0.6`. Contra el script.

- [ ] **Paso 4: el dibujo, con cuatro franjas**

`panelesApilados` con cuatro paneles. El de arriba es la escena, los tres de abajo los
gráficos. Los tres gráficos comparten el eje de tiempo; la escena está en metros, así que
necesita **su propio rango horizontal** — es el segundo uso de lo que la Tarea 3 le
agregó al motor, y acá es indispensable, no cómodo.

- **Panel 1, la escena.** La pared a la izquierda, el resorte dibujado como una zigzag
  entre la pared y el bloque, el bloque con `bloque`, y una marca punteada vertical en
  `X0`. Sobre el bloque, la flecha roja de la fuerza del resorte, `−k(x − X0)`, y la azul
  de la velocidad. El zigzag del resorte se dibuja con `N` vueltas entre la pared y el
  bloque: al comprimirse, las vueltas se juntan. Elegí `N` y la amplitud del zigzag y
  dejá escrito de dónde salen.
- **Paneles 2, 3 y 4.** `x(t)`, `v(t)`, `a(t)`, cada uno con su `eje` rotulado, su
  `curva` sobre un período completo, y un `cuerpo` chico en el instante actual. `x` en
  `--graph`, `v` en `--blue`, `a` en `--red`: el mismo reparto de colores del ensayo 1,
  que es a propósito — esta es la misma figura, con la función puesta por la física.

El rango de tiempo de los tres gráficos es un período, que cambia con los deslizadores.
Que las tres curvas se reacomoden juntas al mover `k` es parte de lo que el widget
enseña.

- [ ] **Paso 5: los párrafos de cierre de la sección**

1. Los números del ejercicio: ω = 2 rad/s, período 3,14 s, frecuencia 0,318 Hz, y el
   bloque va y viene entre 0,25 m y 0,55 m. La amplitud es la distancia a la que se lo
   llevó, ni más ni menos, porque se lo soltó del reposo.
2. Mirá los tres gráficos juntos. La velocidad es cero justo donde la posición está en un
   extremo, y máxima al pasar por el equilibrio; la aceleración es el espejo exacto de la
   posición. Eso último no es una coincidencia del dibujo: es `a = −ω²(x − x₀)`, que es la
   segunda ley con `F = −k(x − x₀)` dividida por `m`. La lectura de la derecha lo muestra
   dando cero en todo instante.
3. Mové los deslizadores: la frecuencia depende **sólo** de `k/m`. Ni de la amplitud, ni
   de con cuánta fuerza lo soltaste. Un resorte más duro o un bloque más liviano oscilan
   más rápido, y nada más entra en la cuenta — que es por qué un reloj de péndulo anda
   igual con la cuerda floja que apretada.
4. Y los otros tres ejercicios de resortes de la guía, en una frase cada uno. El
   dinamómetro del ejercicio 11, donde `k = 2 N / 0,117 m = 17,09 N/m` y 0,4 N estiran
   2,34 cm. Los dos resortes en paralelo del 12, que suman constantes —50 + 100 =
   150 N/m— y con 0,5 m de estiramiento dan 75 N contra un peso de 24,5 N, o sea
   20,20 m/s² hacia arriba. Y el ejercicio 14, que es el más lindo de los tres porque
   junta este ensayo con el 4: un resorte de 400 N/m y largo natural 0,5 m hace girar una
   masa de 2 kg, y es **el resorte** el que provee la fuerza centrípeta. Con radio 1 m la
   velocidad es 10,00 m/s; al doble de velocidad el resorte se estira hasta 1,686 m,
   porque al alejarse necesita más fuerza y estirándose la consigue. Los cuatro números
   salen del script.

- [ ] **Paso 6: verificar**

1. Las lecturas con los valores por defecto, contra el script: `2.00 rad/s`, `3.14 s`,
   `0.318 Hz`, `0.300 m/s`, `0.600 m/s²`, y la última en `0.000`.
2. Reproducí un período completo y comprobá que el bloque vuelve exactamente al punto de
   partida y que las tres curvas cierran.
3. Movelo a `k = 8`, `m = 0.5`: ω tiene que dar 4 rad/s y el período la mitad. A
   `k = 2`, `m = 2`: ω = 1 rad/s.
4. La lectura de `a + ω²(x−x₀)` se queda en `0.000` durante toda la animación y con todos
   los valores de los deslizadores. Es la prueba de que es un MAS de verdad.
5. Los cuatro paneles: el de arriba en metros, los tres de abajo en segundos. Si el de
   arriba hereda el rango de los de abajo, el rango por panel no está andando.
6. 1280 y 390 px, los dos temas, consola limpia, nada que se anime solo al cargar.

- [ ] **Paso 7: commit**

```bash
node --test "test/**/*.test.js"
git add docs/ensayos/fuerzas-de-posicion.html docs/recursos
git commit -m "feat(ensayos): fuerzas de posicion, el resorte y sus tres graficos"
```

---

### Tarea 15: Widget 2 — el punto donde la Tierra y la Luna empatan, y el cierre

**Archivos:**
- Modificar: `docs/ensayos/fuerzas-de-posicion.html`
- Modificar: `../Ejercicios-prácticos/parcial-1/soluciones/verificacion-practico-2.py`

**Interfaces:**
- Consume: lo mismo que la Tarea 14.
- Produce: la página terminada.

**El ejercicio (Guía 2, ej. 15).** ¿En qué punto de la recta Tierra-Luna la fuerza neta
sobre una masa de prueba es cero? Del bloque "Ej 15" del script, con
`M_T = 5,97·10²⁴ kg`, `M_L = 7,35·10²² kg` y `d = 3,84·10⁸ m`:

```
r = d / (1 + √(M_L/M_T))
```

y da **r = 3,456·10⁸ m = 0,900 d**. Está al 90 % del camino: mucho más cerca de la Luna,
porque la Tierra es unas 81 veces más masiva.

- [ ] **Paso 1: agregar al script lo que el widget muestra**

El widget muestra los módulos de las dos fuerzas sobre una masa de prueba, y esos números
no están en el script todavía. Agregá al bloque "Ej 15", después de lo que ya está:

```python
# Fuerzas sobre una masa de prueba de 1 kg, que es lo que muestra el ensayo 6.
Gc = 6.674e-11
for frac in (0.5, 0.9, r15 / d, 0.95):
    s = frac * d
    FT, FL = Gc * MT / s**2, Gc * ML / (d - s) ** 2
    print(f"  s = {frac:.4f} d:  F_T = {FT:.4e} N   F_L = {FL:.4e} N   neta = {FT-FL:+.4e} N")
```

Corrélo y usá **esos** valores para verificar el widget.

- [ ] **Paso 2: la sección 02 y su franja**

`<h2>`: `02 · El punto donde nadie tira`. Párrafo previo: la gravedad no se apaga con la
distancia, se diluye — nunca llega a cero, pero baja como el cuadrado. Entre dos cuerpos
eso alcanza para que haya un punto donde las dos atracciones se cancelan exactamente. No
es "donde no hay gravedad": es donde hay dos y se anulan, que es una cosa completamente
distinta y vale la pena decirlo así.

La franja:

- `.encabezado-widget`: `Simulación 2` · `Entre la Tierra y la Luna` ·
  `— el punto de empate está al 90 % del camino, no a la mitad.`
- `<canvas id="w2-cv">`
- controles: un deslizador de posición (`w2-s`, `min="0.10" max="0.99" step="0.001"
  value="0.500"`, salida en fracciones de *d*) y una casilla `w2-log` con la etiqueta
  `Escala logarítmica`.
- `.lecturas`: `F Tierra` (`w2-ft`) y `F Luna` (`w2-fl`), las dos en `--red`, `neta`
  (`w2-fn`) en `--blue`, y `punto de empate` (`w2-eq`) en `--dim`.

`punto de empate` se **calcula** con la fórmula, no se escribe: tiene que decir `0.900 d`
y moverse si alguien cambiara una masa.

- [ ] **Paso 3: la física y el problema de escala**

```js
/* ---------- widget 2: entre la Tierra y la Luna ---------- */

// Guia 2, ej. 15. Verificado en el bloque "Ej 15" de verificacion-practico-2.py:
//   r = d/(1 + sqrt(M_L/M_T)) = 3.456e8 m = 0.900 d
const GRAV = 6.674e-11;
const M_TIERRA = 5.97e24, M_LUNA = 7.35e22, D_TL = 3.84e8;
const S_EQUILIBRIO = 1 / (1 + Math.sqrt(M_LUNA / M_TIERRA));   // en fracciones de d

// Fuerzas sobre una masa de prueba de 1 kg, a una fraccion `s` del camino desde la
// Tierra. Positiva = hacia la Luna.
function campo(s) {
  const rT = s * D_TL, rL = (1 - s) * D_TL;
  const fT = GRAV * M_TIERRA / (rT * rT);      // tira hacia la Tierra
  const fL = GRAV * M_LUNA / (rL * rL);        // tira hacia la Luna
  return { fT, fL, neta: fL - fT };
}
```

El problema de dibujo es la escala: entre `s = 0,10` y `s = 0,99` los módulos cambian
varios órdenes de magnitud, y una flecha proporcional o se sale del canvas o no se ve.
Resolvelo así, y **decilo en el encabezado del widget**, porque un dibujo cuya escala no
es proporcional tiene que anunciarlo:

- Sin la casilla marcada, las dos flechas se dibujan con largos proporcionales a
  `fT / (fT + fL)` y `fL / (fT + fL)`, de modo que las dos juntas siempre ocupan lo
  mismo. Lo que se lee es **la proporción entre las dos**, que es justo lo que decide
  dónde está el empate, y el empate se ve como el momento en que las dos flechas miden
  igual.
- Con la casilla marcada, los largos van con el logaritmo del módulo, normalizado entre
  el mínimo y el máximo del rango del deslizador. Ahí se ve la caída como `1/r²` y se
  pierde la comparación directa.

Los módulos de verdad, en newtons, están siempre en las lecturas. Ninguna de las dos
escalas inventa un número: las dos son maneras de mirar los mismos dos valores, y las
lecturas son la fuente.

- [ ] **Paso 4: el dibujo, en dos paneles**

`panelesApilados` con dos paneles, con rango horizontal propio cada uno.

- **Panel 1, la recta Tierra-Luna.** La Tierra como un `cuerpo` grande a la izquierda, la
  Luna como uno chico a la derecha, la recta entre las dos, y la masa de prueba como un
  punto en `s`. Desde ella, las dos flechas rojas en sentidos opuestos y la azul de la
  neta. Una marca punteada vertical en `S_EQUILIBRIO`. Los tamaños de Tierra y Luna son
  **decorativos y no están a escala**; poné la Luna más chica que la Tierra en la
  proporción de sus radios reales si querés, pero el enunciado del widget no depende de
  eso, y una línea del párrafo de cierre tiene que aclararlo.
- **Panel 2, la fuerza neta contra la posición.** `curva` de `s => campo(s).neta` entre
  0,10 y 0,99 —con el eje vertical en escala logarítmica con signo, o recortado, porque
  cerca de los extremos se dispara—, el eje horizontal en fracciones de *d*, un `cuerpo`
  en el cruce por cero y un `punteado` vertical en el `s` actual. El cruce por cero es la
  imagen que queda.

Elegí el recorte del eje vertical mirando los valores que imprime el script en los cuatro
puntos del Paso 1, y dejá escrito el criterio. No lo elijas de ojo.

- [ ] **Paso 5: los párrafos de cierre de la sección y del ensayo**

De la sección:

1. Dónde está el empate y por qué tan cerca de la Luna: `r/d = 1/(1 + √(M_L/M_T))`, y
   como la Tierra es unas 81 veces más masiva, la raíz vale cerca de 1/9, y el punto queda
   al 90 % del camino. Que la respuesta dependa de la **raíz** del cociente de masas, y no
   del cociente, es lo que la hace menos extrema de lo que uno esperaría.
2. Que en ese punto la fuerza neta sea cero no significa que ahí no pase nada: una masa
   soltada exactamente ahí se queda, pero es un equilibrio **inestable** — un milímetro
   para cualquier lado y se va. El gráfico de abajo lo muestra: la curva cruza el cero con
   pendiente, y el signo de la neta empuja siempre para afuera del punto.
3. El ejercicio 16, en dos frases: tres masas iguales en los vértices de un triángulo
   equilátero de lado *L*. Sobre cada una, la fuerza de las otras dos suma
   `√3 G m²/L²` apuntando al baricentro. Y en el baricentro mismo el campo es cero por
   simetría, aunque las tres masas estén tirando: otra vez, cero **no** es ausencia.

Y el cierre de la página, `<h2>` `Para tener a mano`:

- Si la fuerza depende de la posición, la aceleración no es un número: las fórmulas de
  aceleración constante no se pueden usar, y hay que ir a la ecuación o a un caso conocido.
- Ley de Hooke: `F = −k(x − x₀)`, y el signo menos es todo — es lo que produce la
  oscilación en vez de una huida.
- En un MAS, `ω = √(k/m)`, y el período no depende de la amplitud. Soltarlo de más lejos
  lo hace ir más rápido, no tardar más.
- Resortes en paralelo suman constantes; en serie suman inversas.
- Gravitación: `F = G m₁m₂/r²`, siempre atractiva, y `r` es la distancia entre centros.
- Entre dos cuerpos hay un punto de fuerza neta nula, y está a `d/(1 + √(m₂/m₁))` del más
  masivo. Es un equilibrio inestable.

- [ ] **Paso 6: verificar**

1. Las cuatro filas que imprime el script contra las lecturas del widget, poniendo el
   deslizador en cada valor. Cifra por cifra.
2. Con el deslizador en `0.900`: las dos lecturas de fuerza tienen que dar prácticamente
   iguales, la neta cerca de cero, y las dos flechas del mismo largo en el modo
   proporcional. Medí los largos, no los mires.
3. La lectura `punto de empate` dice `0.900 d`.
4. La casilla de escala logarítmica cambia los largos y **no** cambia ninguna lectura.
5. En los extremos del deslizador —`0.10` y `0.99`— nada se sale del canvas ni tira
   `Infinity`. Ése es el motivo del recorte del eje vertical.
6. 1280 y 390 px, los dos temas, consola limpia, enlaces del pie con `docs/` como raíz,
   barra de progreso al 100 % abajo.

- [ ] **Paso 7: commit**

```bash
node --test "test/**/*.test.js"
git add docs/ensayos/fuerzas-de-posicion.html
git commit -m "feat(ensayos): fuerzas de posicion, entre la Tierra y la Luna"
```

Y en el otro repositorio:

```bash
cd ../Ejercicios-prácticos
git add parcial-1/soluciones/verificacion-practico-2.py
git commit -m "test(verificacion): fuerzas sobre la masa de prueba del ejercicio 15"
```

---

## Fase G — cerrar

### Tarea 16: Navegación, portada y README

Las páginas nuevas existen pero están sueltas: la portada todavía las lista en `--dim`
sin enlace, y la cadena de "anterior / siguiente" del pie se corta en el ensayo 3.

**Archivos:**
- Modificar: `docs/index.html`, los seis ensayos, las dos notas de ejemplo, `README.md`

**Interfaces:**
- Consume: todas las páginas de este plan.
- Produce: el sitio navegable de punta a punta.

- [ ] **Paso 1: enlazar en la portada**

Las tres filas de ensayos que la Tarea 1 dejó sin enlace —4, 5 y 6— pasan a ser `<a>`,
con exactamente la misma forma que las de los ensayos 1 a 3. El ensayo 7, `Energía`,
sigue sin enlace. Las dos filas de `EJEMPLOS RESUELTOS` ya quedaron enlazadas por las
tareas 4 y 5; confirmalo.

- [ ] **Paso 2: cerrar la cadena del pie**

Cada página lleva en el pie el enlace a la anterior y a `Portada`. Con seis ensayos, la
cadena tiene que quedar completa y **coherente con el orden temático nuevo**, no con el
de construcción:

| Página | Enlace de la izquierda |
|---|---|
| `derivada-integral.html` | `Portada` (es la primera; a la izquierda va la portada y a la derecha nada) |
| `tiro-parabolico.html` | `Ensayo 1 · Derivada e integral, vistas` |
| `movimiento-circular.html` | `Ensayo 2 · Tiro parabólico` |
| `cuerpo-aislado.html` | `Ensayo 3 · Movimiento circular` |
| `sistemas-acoplados.html` | `Ensayo 4 · Diagrama de cuerpo aislado` |
| `fuerzas-de-posicion.html` | `Ensayo 5 · Sistemas acoplados` |
| `ejemplos/la-tierra.html` | `Portada` |
| `ejemplos/auto-y-camion.html` | `Portada` |

Revisá los tres ensayos viejos: `tiro-parabolico.html` y `derivada-integral.html` fueron
escritos cuando el orden era otro, y es muy probable que sus enlaces apunten mal ahora.
Corregilos.

Las dos notas de ejemplo están en `docs/ejemplos/`, un nivel distinto: sus rutas
relativas a la portada son `../index.html`, igual que las de los ensayos, pero
comprobalas sirviendo `docs/` como raíz, no des por sentado que están bien.

- [ ] **Paso 3: el README**

`README.md` de la plataforma describe qué hay. Actualizalo: seis ensayos y dos notas de
ejemplo, con una línea por cada uno diciendo qué construye y qué ejercicios de qué
práctico cubre. Y una línea honesta sobre lo que **no** está: la Guía 3 entera —trabajo,
energía, cantidad de movimiento— y la portada, que la diseña el dueño.

- [ ] **Paso 4: el recorrido completo**

Con `docs/` servido como raíz y un proceso de Chrome fresco, recorré **todas** las
páginas, a 1280 y a 390 px, en los dos temas:

1. Ningún enlace 404. Incluidos los PDF del pie de cada página — es el defecto que se
   escapó entero la vez pasada, así que abrí cada uno.
2. Ningún error en la consola en ninguna página.
3. Ningún desborde horizontal a 390 px: comprobalo con
   `document.documentElement.scrollWidth <= window.innerWidth` en cada página, no a ojo.
4. Ningún widget animándose solo al cargar: todos los botones dicen `Reproducir`.
5. Cada canvas pinta algo: bitmap no uniforme, no en blanco.
6. Cambiar de tema desde cualquier página y volver a la portada conserva el tema.

Guardá los resultados en el informe, página por página. Un "recorrí todo y anda" sin la
tabla no es una verificación.

- [ ] **Paso 5: commit**

```bash
node --test "test/**/*.test.js"
git add docs README.md
git commit -m "feat(plataforma): enlazar los ensayos nuevos y cerrar la navegacion"
```
