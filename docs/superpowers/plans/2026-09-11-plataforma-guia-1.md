# Plataforma de Física 1 — Guía 1 completa · Plan de implementación

> **Para trabajadores agénticos:** SUB-SKILL REQUERIDA: usar superpowers:subagent-driven-development (recomendada) o superpowers:executing-plans para implementar este plan tarea por tarea. Los pasos usan sintaxis de casilla (`- [ ]`) para seguimiento.

**Objetivo:** cubrir toda la Guía 1 con tres ensayos interactivos —tiro parabólico completo, derivada e integral, y movimiento circular— sobre un motor que soporte varios widgets por página.

**Arquitectura:** el plan 1 dejó un motor que alcanza para un widget por página y un ensayo con una sola sección. Este plan primero cierra los cinco huecos que la revisión final identificó (márgenes en el lienzo, reloj gobernable, vectores en píxeles con rótulo, servicios de página compartidos, arrastre), y recién después escribe contenido. Cada ensayo es un HTML suelto que importa módulos; no hay build ni dependencias.

**Stack:** ES modules vanilla, canvas 2D, `node --test` de Node 22, GitHub Pages desde `/docs`.

**Spec:** `docs/plataforma/brief.md`

**Autoridad de diseño:** `docs/plataforma/diseno/Tiro parabolico.dc.html`

## Supuesto que este plan hace explícito

El dueño del proyecto diseñó a mano el ensayo de tiro parabólico y va a diseñar la portada. Los ensayos 1 y 3 **no tienen archivo de diseño propio**, así que este plan los construye aplicando el sistema de diseño ya cerrado: la sección 6 del brief más el archivo de tiro parabólico como implementación de referencia de ese sistema. Ninguna tarea inventa un valor visual nuevo: todos salen de uno de esos dos lugares. Si el dueño prefiere diseñar también los ensayos 1 y 3, las tareas a frenar son las 11 a 18; las 1 a 9 no dependen de esa decisión.

## Restricciones globales

Aplican a todas las tareas.

- **Cero dependencias de runtime** salvo KaTeX por CDN. Nada de `npm install`.
- **Cero build.** Lo que está en el repositorio es lo que sirve el navegador.
- **Los tokens de color son exactamente estos**, y no se inventa ninguno:
  claro `--paper:#fbfaf7` `--band:#f2f0ea` `--ink:#16151a` `--dim:#6a6760`
  `--rule:#dcd8ce` `--blue:#1b4fd4` `--blue-soft:#8aa3e6` `--red:#c02a24`
  `--graph:#8e8a80`; oscuro `--paper:#131316` `--band:#191a1e` `--ink:#eceae4`
  `--dim:#948f86` `--rule:#2e2f35` `--blue:#7aa2ff` `--blue-soft:#3f5694`
  `--red:#ef5f52` `--graph:#6f6c66`. Nunca se escriben literales hex en JS: se leen de los tokens CSS.
- **Reparto semántico fijo:** azul para cinemática y velocidad, rojo para aceleración y fuerza. Nunca al revés. La trayectoria va en `--graph`.
- **Tipografías:** Source Serif 4 para el contenido, JetBrains Mono para la interfaz. Serif para lo que se lee, mono para lo que se opera.
- **Grilla:** columna de texto `max-width:680px` con `padding:0 24px`, widget `max-width:880px` dentro de una franja a todo el ancho.
- **Canvas:** `width:100%`, `aspect-ratio:16/8`, `touch-action:none`.
- **Ningún widget se anima solo al cargar.** Arranca quieto en un estado representativo.
- **Ningún número aparece sin respaldo** en un `verificacion-*.py` del repositorio. Para la Guía 1 el respaldo es `parcial-1/soluciones/verificacion-practico-1.py`, que usa `g = 9.8` salvo en el ejercicio 15, donde usa `g = 10` (líneas 118-119).
- **Todo widget lleva la frase de "qué mirar"** en su encabezado, en `--dim`, después del nombre.
- **El tema se aplica en un script clásico bloqueante del `<head>`**, con `try/catch` alrededor de todo acceso a `localStorage`, como en `docs/index.html:6-12`.
- Ante discrepancia entre el spec y el archivo de diseño, manda el archivo de diseño.
- Nombres en español, como todo el proyecto.
- Las pruebas corren desde la raíz del worktree: `node --test "test/**/*.test.js"`.

## Estructura de archivos

**Motor, modificados:**

| Archivo | Qué cambia |
|---|---|
| `docs/motor/lienzo.js` | acepta `margen`, así que el área dibujable se calcula sola y `eje` deja de necesitar el rodeo del `translate` |
| `docs/motor/escena.js` | `duracion` y `velocidad` mutables, y `ir(t)` para saltar a un instante |
| `docs/motor/dibujo.js` | `vectorPx` en píxeles con punta, guiones y rótulo; `vector` pasa a ser su envoltura en coordenadas físicas; se suman `punteado` y `texto` |

**Motor, nuevos:**

| Archivo | Responsabilidad |
|---|---|
| `docs/motor/pagina.js` | lo que comparten todos los widgets de una página: caché de paleta, `ResizeObserver`, barra de progreso de lectura, y el pulso de la primera interacción |
| `docs/motor/widget.js` | un canvas: lo mide, lo escala por `devicePixelRatio`, arma su lienzo y lo repinta |
| `docs/motor/controles.js` | cablear botones, sliders, casillas y lecturas sin repetir el mismo `oninput` en cada ensayo |
| `docs/motor/arrastre.js` | arrastrar un punto sobre el canvas en coordenadas físicas, con acotado |

**Física, nuevos:**

| Archivo | Responsabilidad |
|---|---|
| `docs/fisica/calculo.js` | derivada e integral numéricas sobre muestras, y el muestreo mismo |
| `docs/fisica/circular.js` | movimiento circular uniforme y uniformemente acelerado |

**Ensayos:**

| Archivo | Qué pasa |
|---|---|
| `docs/ensayos/tiro-parabolico.html` | se migra a la fábrica y se completa con las secciones 02, 03, 04 y el cierre |
| `docs/ensayos/derivada-integral.html` | nuevo, cuatro widgets |
| `docs/ensayos/movimiento-circular.html` | nuevo, cuatro widgets |

**Pruebas:** `test/lienzo.test.js`, `test/escena.test.js`, `test/dibujo.test.js` se extienden; se crean `test/widget.test.js`, `test/controles.test.js`, `test/arrastre.test.js`, `test/calculo.test.js`, `test/circular.test.js`.

---

## Fase A — cerrar los huecos del motor

### Tarea 1: Márgenes en el lienzo

Hoy `crearLienzo` mapea el rectángulo entero del canvas, así que el ensayo de tiro
parabólico dibuja sus ejes construyendo un lienzo auxiliar y aplicando un `translate`.
Funciona y es exacto, pero no escala a doce widgets.

**Archivos:**
- Modificar: `docs/motor/lienzo.js`
- Prueba: `test/lienzo.test.js`

**Interfaces:**
- Consume: nada.
- Produce: `crearLienzo({ ancho, alto, xMin, xMax, yMin, yMax, margen })` donde
  `margen` es `{ L, R, T, B }` en píxeles y su valor por defecto es
  `{ L: 0, R: 0, T: 0, B: 0 }`. Con el margen por defecto el comportamiento es
  idéntico al actual. El objeto devuelto suma `margen` a lo que ya devolvía
  (`ancho, alto, xMin, xMax, yMin, yMax, px, py, p, ux, uy, escala`).

- [ ] **Paso 1: escribir las pruebas que fallan**

Agregar al final de `test/lienzo.test.js`:

```js
test('sin margen el lienzo mapea el rectangulo entero, como antes', () => {
  const l = crearLienzo({ ancho: 200, alto: 100, xMin: 0, xMax: 10, yMin: 0, yMax: 5 });
  assert.equal(l.px(0), 0);
  assert.equal(l.px(10), 200);
  assert.equal(l.py(0), 100);
  assert.equal(l.py(5), 0);
});

test('el margen deja el origen adentro y acorta el area dibujable', () => {
  const l = crearLienzo({
    ancho: 200, alto: 100, xMin: 0, xMax: 10, yMin: 0, yMax: 5,
    margen: { L: 20, R: 10, T: 8, B: 12 },
  });
  assert.equal(l.px(0), 20);          // el origen queda sobre el margen izquierdo
  assert.equal(l.px(10), 190);        // 200 - 10
  assert.equal(l.py(0), 88);          // 100 - 12
  assert.equal(l.py(5), 8);           // el margen superior
  assert.equal(l.escala.x, 17);       // (200 - 20 - 10) / 10
  assert.equal(l.escala.y, 16);       // (100 - 8 - 12) / 5
});

test('ux y uy invierten a px y py tambien con margen', () => {
  const l = crearLienzo({
    ancho: 320, alto: 180, xMin: -4, xMax: 12, yMin: -2, yMax: 9,
    margen: { L: 31, R: 17, T: 13, B: 23 },
  });
  for (const x of [-4, 0, 3.7, 12]) assert.ok(Math.abs(l.ux(l.px(x)) - x) < 1e-9);
  for (const y of [-2, 0, 4.25, 9]) assert.ok(Math.abs(l.uy(l.py(y)) - y) < 1e-9);
});

test('el margen viaja en el objeto devuelto', () => {
  const m = { L: 5, R: 6, T: 7, B: 8 };
  const l = crearLienzo({ ancho: 100, alto: 50, xMin: 0, xMax: 1, yMin: 0, yMax: 1, margen: m });
  assert.deepEqual(l.margen, m);
  const d = crearLienzo({ ancho: 100, alto: 50, xMin: 0, xMax: 1, yMin: 0, yMax: 1 });
  assert.deepEqual(d.margen, { L: 0, R: 0, T: 0, B: 0 });
});
```

- [ ] **Paso 2: correrlas y verificar que fallan**

Ejecutar: `node --test test/lienzo.test.js`
Esperado: FALLAN las tres últimas; la primera pasa, porque fija el comportamiento que ya existe.

- [ ] **Paso 3: implementar**

Reemplazar el cuerpo de `crearLienzo` en `docs/motor/lienzo.js`:

```js
export function crearLienzo({ ancho, alto, xMin, xMax, yMin, yMax, margen }) {
  const m = { L: 0, R: 0, T: 0, B: 0, ...(margen || {}) };
  const kx = (ancho - m.L - m.R) / (xMax - xMin);
  const ky = (alto - m.T - m.B) / (yMax - yMin);
  const px = x => m.L + (x - xMin) * kx;
  const py = y => alto - m.B - (y - yMin) * ky;
  return {
    ancho, alto, xMin, xMax, yMin, yMax, margen: m, px, py,
    p: ([x, y]) => [px(x), py(y)],
    ux: v => (v - m.L) / kx + xMin,
    uy: v => (alto - m.B - v) / ky + yMin,
    escala: { x: kx, y: ky },
  };
}
```

- [ ] **Paso 4: correr toda la suite**

Ejecutar: `node --test "test/**/*.test.js"`
Esperado: todo verde. Las pruebas de dibujo escritas contra el lienzo sin margen siguen valiendo porque el margen por defecto es cero.

- [ ] **Paso 5: commit**

```bash
git add docs/motor/lienzo.js test/lienzo.test.js
git commit -m "feat(plataforma): margenes en el lienzo"
```

---

### Tarea 2: Reloj gobernable en la escena

Hoy `duracion` queda congelada al construir la escena, así que cambiar un parámetro
obliga a destruirla y rehacerla —catorce líneas en el ensayo— y a convertir a mano
entre segundos de pantalla y segundos de física en cuatro lugares. Además no hay
forma de saltar a un instante, que es lo que va a necesitar cualquier línea de tiempo
arrastrable.

**Archivos:**
- Modificar: `docs/motor/escena.js`
- Prueba: `test/escena.test.js`

**Interfaces:**
- Consume: nada.
- Produce: `crearEscena({ dibujar, duracion, velocidad = 1, alCambiar })`. A lo que ya
  devolvía (`reproducir()`, `pausar()`, `reiniciar()`, `avanzar(dt)`, `t`, `estado`)
  se le suman: `duracion` y `velocidad` como propiedades **escribibles**, y `ir(t)`
  que lleva el reloj a un instante absoluto sin cambiar el estado.
  `avanzar(dt)` ahora adelanta `dt * velocidad` segundos de física, de modo que
  `duracion` se expresa siempre en tiempo físico.

- [ ] **Paso 1: escribir las pruebas que fallan**

Agregar al final de `test/escena.test.js`:

Ojo con una cosa antes de escribirlas: `avanzar(dt)` arranca con el guard
`if (estado !== 'reproduciendo') return;`, que es comportamiento aprobado y está fijado
por la prueba `no avanza el tiempo mientras no se reproduce`. **Ese guard se queda.** Por
eso toda prueba que espere que el reloj se mueva tiene que llamar `reproducir()` antes.

```js
test('velocidad escala lo que avanza el reloj', () => {
  const e = crearEscena({ dibujar() {}, duracion: 10, velocidad: 0.5 });
  e.reproducir();
  e.avanzar(2);
  assert.equal(e.t, 1);
});

test('velocidad por defecto es 1 y no cambia el comportamiento viejo', () => {
  const e = crearEscena({ dibujar() {}, duracion: 10 });
  e.reproducir();
  e.avanzar(2);
  assert.equal(e.t, 2);
});

test('la velocidad no le pasa por encima al guard: en reposo el reloj no se mueve', () => {
  const e = crearEscena({ dibujar() {}, duracion: 10, velocidad: 4 });
  e.avanzar(2);
  assert.equal(e.t, 0);
});

test('cambiar velocidad a mitad de camino no mueve el reloj, solo su ritmo', () => {
  const e = crearEscena({ dibujar() {}, duracion: 10 });
  e.reproducir();
  e.avanzar(2);
  e.velocidad = 0.25;
  assert.equal(e.t, 2);
  e.avanzar(2);
  assert.equal(e.t, 2.5);
});

test('duracion es escribible y recorta el reloj si se acorta', () => {
  const e = crearEscena({ dibujar() {}, duracion: 10 });
  e.reproducir();
  e.avanzar(8);
  e.duracion = 3;
  assert.equal(e.duracion, 3);
  assert.equal(e.t, 3);
});

test('alargar la duracion no mueve el reloj', () => {
  const e = crearEscena({ dibujar() {}, duracion: 10 });
  e.reproducir();
  e.avanzar(4);
  e.duracion = 20;
  assert.equal(e.t, 4);
});

test('ir(t) salta a un instante y repinta sin cambiar el estado', () => {
  let pintados = 0;
  const e = crearEscena({ dibujar() { pintados++; }, duracion: 10 });
  const antes = pintados;
  e.ir(6.5);
  assert.equal(e.t, 6.5);
  assert.equal(e.estado, 'reposo');
  assert.equal(pintados, antes + 1);
});

test('ir(t) acota a [0, duracion]', () => {
  const e = crearEscena({ dibujar() {}, duracion: 10 });
  e.ir(-5);
  assert.equal(e.t, 0);
  e.ir(999);
  assert.equal(e.t, 10);
});

test('ir(t) recibe el instante que dibujar tiene que pintar', () => {
  const vistos = [];
  const e = crearEscena({ dibujar(t) { vistos.push(t); }, duracion: 10 });
  e.ir(3);
  assert.equal(vistos.at(-1), 3);
});
```

- [ ] **Paso 2: correrlas y verificar que fallan**

Ejecutar: `node --test test/escena.test.js`
Esperado: FALLAN todas menos la de la velocidad por defecto.

- [ ] **Paso 3: implementar**

`docs/motor/escena.js` ya existe y está aprobado; esto es una modificación quirúrgica,
no una reescritura. Son cinco cambios y ninguno toca el loop de `requestAnimationFrame`,
el tope de `SALTO_MAXIMO` ni `detenerLoop`, que quedan exactamente como están:

1. Agregar `velocidad = 1` al destructurado del argumento.
2. Sumar dos variables al bloque de estado que ya tiene `t` y `estado`:
   `let dur = duracion;` y `let vel = velocidad;`.
3. Reemplazar toda referencia interna a `duracion` por `dur` — hoy hay una sola, la
   comparación dentro de `avanzar`.
4. Dentro de `avanzar(dt)`, y **después** del guard `if (estado !== 'reproduciendo') return;`
   que queda tal cual está, cambiar `t = Math.min(t + dt, duracion)` por
   `t = Math.min(t + dt * vel, dur)`.
5. Agregar al objeto devuelto los getters y setters de `duracion` y `velocidad`, y el
   método `ir`.

El guard de `avanzar` **no se toca**: que el reloj no se mueva mientras la escena no
reproduce es comportamiento aprobado, lo fija la prueba `no avanza el tiempo mientras no
se reproduce`, y los widgets se apoyan en él para quedarse quietos al cargar. `ir(t)` es
la vía deliberada para mover el reloj sin reproducir, y por eso no pasa por `avanzar`.

Así queda la parte que cambia, con lo que no cambia marcado como tal:

```js
export function crearEscena({ dibujar, duracion, velocidad = 1, alCambiar }) {
  let t = 0;
  let estado = 'reposo';
  let dur = duracion;
  let vel = velocidad;
  // [SIN CAMBIOS] idAnimacion, tAnterior, detenerLoop, pasarA y paso quedan tal cual

  const api = {
    get t() { return t; },
    get estado() { return estado; },
    get duracion() { return dur; },
    set duracion(v) {
      dur = v;
      if (t > dur) { t = dur; dibujar(t); }
    },
    get velocidad() { return vel; },
    set velocidad(v) { vel = v; },
    ir(nuevo) {
      t = Math.min(dur, Math.max(0, nuevo));
      dibujar(t);
    },
    avanzar(dt) {
      if (estado !== 'reproduciendo') return;   // [SIN CAMBIOS] el guard se queda
      t = Math.min(t + dt * vel, dur);
      if (t >= dur) {
        detenerLoop();
        pasarA('pausado');
      }
      dibujar(t);
    },
    // [SIN CAMBIOS] reproducir, pausar y reiniciar quedan tal cual
  };
  return api;
}
```

Cuidar tres cosas: `duracion` en el setter tiene que recortar `t` **y** repintar, para
que la pantalla no quede mostrando un instante que ya no existe; `ir` no toca
`estado` ni el loop; y toda referencia interna a `duracion` pasa a usar `dur`.

- [ ] **Paso 4: correr toda la suite**

Ejecutar: `node --test "test/**/*.test.js"`
Esperado: todo verde, incluidas las pruebas del tope de `dt` y del loop de rAF, que no cambian.

- [ ] **Paso 5: commit**

```bash
git add docs/motor/escena.js test/escena.test.js
git commit -m "feat(plataforma): duracion y velocidad gobernables, mas ir(t)"
```

---

### Tarea 3: Vectores en píxeles, con punta, guiones y rótulo

`vector` sólo acepta extremos en coordenadas físicas, y el diseño necesita flechas
cuyo largo es en píxeles: la de `g` mide 24 px fijos y la de `v_y` mide `vy·sc·0.42`.
Además `vector` corre el asta hasta la punta —el diseño la frena en `0.85·hd`— y corta
en `largo < 1e-9` en vez del `len < 1` del diseño, así que en el ápice, donde `v_y → 0`,
dibujaría una punta de 9 px sobre un asta de menos de un píxel.

**Archivos:**
- Modificar: `docs/motor/dibujo.js`
- Prueba: `test/dibujo.test.js`

**Interfaces:**
- Consume: nada.
- Produce:
  - `vectorPx(ctx, x1, y1, x2, y2, { color, grosor = 2, punta = 9, guiones = [], rotulo, rdx = 8, rdy = -6, rAlineacion = 'left' })` — extremos en píxeles.
  - `vector(ctx, l, desde, hasta, opciones)` — envoltura que convierte con `l.p(...)` y delega en `vectorPx`. Mismas opciones.
  - `punteado(ctx, x1, y1, x2, y2, { color, guiones = [2, 4], grosor = 1 })` — extremos en píxeles.
  - `texto(ctx, cadena, x, y, { color, px = 11, peso = 500, alineacion = 'left' })` — en JetBrains Mono, extremos en píxeles.
  - `curva(ctx, l, f, t0, t1, { color, grosor = 1.6, guiones = [], n = 140 })` — muestrea `f(t)`, que devuelve `[x, y]` en unidades físicas, y la traza. Es el `path()` del diseño. `traza`, que recibe un arreglo de puntos ya calculados, se queda como está: la necesita el widget que dibuja a mano alzada.
  - `eje` pasa a aceptar `{ color, colorTexto, etiquetaX, etiquetaY }` y a dibujar además las marcas y sus números, como el `axes()` del diseño. Sin `etiquetaX`/`etiquetaY` se comporta como hoy.
- `color` sigue siendo obligatorio en todas.

- [ ] **Paso 1: escribir las pruebas que fallan**

Agregar al final de `test/dibujo.test.js`:

```js
test('vectorPx no dibuja nada si el largo es menor a un pixel', () => {
  const c = ctxFalso();
  vectorPx(c, 10, 10, 10.4, 10, { color: '#000' });
  assert.deepEqual(c.ops, []);
});

test('vectorPx frena el asta antes de la punta, no la corre hasta el extremo', () => {
  const c = ctxFalso();
  vectorPx(c, 0, 0, 100, 0, { color: '#000', punta: 10 });
  const linea = c.ops.find(o => o[0] === 'lineTo');
  // 100 - cos(0) * 10 * 0.85
  assert.ok(Math.abs(linea[1] - 91.5) < 1e-9, `asta hasta ${linea[1]}`);
});

test('vectorPx acota la punta a la mitad del largo', () => {
  const c = ctxFalso();
  vectorPx(c, 0, 0, 6, 0, { color: '#000', punta: 20 });
  const linea = c.ops.find(o => o[0] === 'lineTo');
  // hd = min(20, 6 * 0.5) = 3  ->  6 - 3 * 0.85
  assert.ok(Math.abs(linea[1] - 3.45) < 1e-9, `asta hasta ${linea[1]}`);
});

test('vectorPx pinta la cabeza con fill y la deja cerrada', () => {
  const c = ctxFalso();
  vectorPx(c, 0, 0, 50, 0, { color: '#000' });
  const nombres = c.ops.map(o => o[0]);
  assert.ok(nombres.includes('closePath'));
  assert.ok(nombres.includes('fill'));
});

test('vectorPx aplica los guiones al asta y los limpia despues', () => {
  const c = ctxFalso();
  vectorPx(c, 0, 0, 50, 0, { color: '#000', guiones: [4, 4] });
  const dashes = c.ops.filter(o => o[0] === 'setLineDash').map(o => o[1]);
  assert.deepEqual(dashes[0], [4, 4]);
  assert.deepEqual(dashes.at(-1), []);
});

test('vectorPx dibuja el rotulo cuando se lo pide, y no cuando no', () => {
  const con = ctxFalso();
  vectorPx(con, 0, 0, 50, 0, { color: '#000', rotulo: 'v' });
  const sin = ctxFalso();
  vectorPx(sin, 0, 0, 50, 0, { color: '#000' });
  const textos = con.ops.filter(o => o[0] === 'fillText');
  assert.equal(textos.length, 1);
  assert.equal(textos[0][1], 'v');
  assert.equal(sin.ops.filter(o => o[0] === 'fillText').length, 0);
});

test('vector convierte coordenadas fisicas y delega en vectorPx', () => {
  const l = crearLienzo({ ancho: 100, alto: 100, xMin: 0, xMax: 10, yMin: 0, yMax: 10 });
  const enFisicas = ctxFalso();
  vector(enFisicas, l, [0, 0], [5, 0], { color: '#000' });
  const enPixeles = ctxFalso();
  vectorPx(enPixeles, l.px(0), l.py(0), l.px(5), l.py(0), { color: '#000' });
  assert.deepEqual(enFisicas.ops, enPixeles.ops);
});

test('punteado traza con guiones y los limpia', () => {
  const c = ctxFalso();
  punteado(c, 0, 0, 10, 10, { color: '#000' });
  const dashes = c.ops.filter(o => o[0] === 'setLineDash').map(o => o[1]);
  assert.deepEqual(dashes[0], [2, 4]);
  assert.deepEqual(dashes.at(-1), []);
});

test('texto escribe en mono y respeta la alineacion', () => {
  const c = ctxFalso();
  texto(c, 'hola', 5, 7, { color: '#000', alineacion: 'right' });
  const t = c.ops.find(o => o[0] === 'fillText');
  assert.deepEqual([t[1], t[2], t[3]], ['hola', 5, 7]);
  assert.equal(c.textAlign, 'right');
  assert.ok(/JetBrains Mono/.test(c.font));
});

test('curva muestrea la funcion y traza n+1 puntos', () => {
  const l = crearLienzo({ ancho: 100, alto: 100, xMin: 0, xMax: 10, yMin: 0, yMax: 10 });
  const c = ctxFalso();
  curva(c, l, t => [t, t], 0, 10, { color: '#000', n: 4 });
  assert.equal(c.ops.filter(o => o[0] === 'moveTo').length, 1);
  assert.equal(c.ops.filter(o => o[0] === 'lineTo').length, 4);
});

test('curva arranca en t0 y termina en t1', () => {
  const l = crearLienzo({ ancho: 100, alto: 100, xMin: 0, xMax: 10, yMin: 0, yMax: 10 });
  const c = ctxFalso();
  curva(c, l, t => [t, 0], 2, 8, { color: '#000', n: 6 });
  assert.equal(c.ops.find(o => o[0] === 'moveTo')[1], l.px(2));
  assert.equal(c.ops.filter(o => o[0] === 'lineTo').at(-1)[1], l.px(8));
});

test('eje sin etiquetas dibuja solo los dos ejes, como antes', () => {
  const l = crearLienzo({ ancho: 100, alto: 100, xMin: 0, xMax: 10, yMin: 0, yMax: 10 });
  const c = ctxFalso();
  eje(c, l, { color: '#000' });
  assert.equal(c.ops.filter(o => o[0] === 'fillText').length, 0);
});

test('eje con etiquetas escribe las marcas y los dos rotulos', () => {
  const l = crearLienzo({ ancho: 300, alto: 200, xMin: 0, xMax: 10, yMin: 0, yMax: 5 });
  const c = ctxFalso();
  eje(c, l, { color: '#000', colorTexto: '#666', etiquetaX: 'x [m]', etiquetaY: 'y [m]' });
  const textos = c.ops.filter(o => o[0] === 'fillText').map(o => o[1]);
  assert.ok(textos.includes('x [m]'));
  assert.ok(textos.includes('y [m]'));
  // paso de 2 en x (10 / 5) y de 1 en y (5 / 5), sin escribir el cero
  assert.ok(textos.includes('2') && textos.includes('4'));
  assert.ok(!textos.includes('0'));
});
```

El `ctxFalso()` que ya existe en ese archivo tiene que registrar además
`setLineDash`, `closePath`, `fill` y `fillText`, y guardar `font` y `textAlign` como
propiedades. Extenderlo, no reescribirlo: las pruebas viejas dependen de su forma actual.

- [ ] **Paso 2: correrlas y verificar que fallan**

Ejecutar: `node --test test/dibujo.test.js`
Esperado: FALLAN todas las nuevas; `vectorPx`, `punteado` y `texto` no existen.

- [ ] **Paso 3: implementar**

En `docs/motor/dibujo.js`, agregar las tres primitivas y reescribir `vector` como
envoltura. La geometría sale literal del `arrow` del diseño
(`docs/plataforma/diseno/Tiro parabolico.dc.html:402-419`):

```js
export function vectorPx(ctx, x1, y1, x2, y2, opciones = {}) {
  const { color, grosor = 2, punta = 9, guiones = [],
          rotulo, rdx = 8, rdy = -6, rAlineacion = 'left' } = opciones;
  exigirColor(color, 'vectorPx');
  const dx = x2 - x1, dy = y2 - y1, largo = Math.hypot(dx, dy);
  if (largo < 1) return;
  const hd = Math.min(punta, largo * 0.5);
  const a = Math.atan2(dy, dx);
  ctx.strokeStyle = color;
  ctx.fillStyle = color;
  ctx.lineWidth = grosor;
  ctx.setLineDash(guiones);
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2 - Math.cos(a) * hd * 0.85, y2 - Math.sin(a) * hd * 0.85);
  ctx.stroke();
  ctx.setLineDash([]);
  ctx.beginPath();
  ctx.moveTo(x2, y2);
  ctx.lineTo(x2 - Math.cos(a - 0.42) * hd, y2 - Math.sin(a - 0.42) * hd);
  ctx.lineTo(x2 - Math.cos(a + 0.42) * hd, y2 - Math.sin(a + 0.42) * hd);
  ctx.closePath();
  ctx.fill();
  if (rotulo) texto(ctx, rotulo, x2 + rdx, y2 + rdy, { color, alineacion: rAlineacion });
}

export function vector(ctx, l, desde, hasta, opciones = {}) {
  const [x1, y1] = l.p(desde);
  const [x2, y2] = l.p(hasta);
  vectorPx(ctx, x1, y1, x2, y2, opciones);
}

export function punteado(ctx, x1, y1, x2, y2, { color, guiones = [2, 4], grosor = 1 } = {}) {
  exigirColor(color, 'punteado');
  ctx.strokeStyle = color;
  ctx.lineWidth = grosor;
  ctx.setLineDash(guiones);
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.stroke();
  ctx.setLineDash([]);
}

export function texto(ctx, cadena, x, y, { color, px = 11, peso = 500, alineacion = 'left' } = {}) {
  exigirColor(color, 'texto');
  ctx.font = `${peso} ${px}px "JetBrains Mono", ui-monospace, monospace`;
  ctx.fillStyle = color;
  ctx.textAlign = alineacion;
  ctx.fillText(cadena, x, y);
}
```

Y las dos que faltan. `curva` es el `path()` del diseño (`:421-429`), con `n = 140`:

```js
export function curva(ctx, l, f, t0, t1, { color, grosor = 1.6, guiones = [], n = 140 } = {}) {
  exigirColor(color, 'curva');
  ctx.strokeStyle = color;
  ctx.lineWidth = grosor;
  ctx.setLineDash(guiones);
  ctx.beginPath();
  for (let i = 0; i <= n; i++) {
    const t = t0 + (t1 - t0) * i / n;
    const [x, y] = l.p(f(t));
    if (i) ctx.lineTo(x, y); else ctx.moveTo(x, y);
  }
  ctx.stroke();
  ctx.setLineDash([]);
}
```

`eje` suma las marcas y los rótulos, que es el `axes()` del diseño (`:376-401`). El paso
sale del mismo redondeo a 1, 2 o 5:

```js
function paso(rango) {
  const crudo = rango / 5;
  const p = Math.pow(10, Math.floor(Math.log10(crudo)));
  const n = crudo / p;
  return (n >= 5 ? 5 : n >= 2 ? 2 : 1) * p;
}

export function eje(ctx, l, { color, colorTexto, etiquetaX, etiquetaY } = {}) {
  exigirColor(color, 'eje');
  ctx.strokeStyle = color;
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(l.px(l.xMin), l.py(0));
  ctx.lineTo(l.px(l.xMax), l.py(0));
  ctx.moveTo(l.px(0), l.py(l.yMin));
  ctx.lineTo(l.px(0), l.py(l.yMax));
  ctx.stroke();
  if (!etiquetaX && !etiquetaY) return;
  exigirColor(colorTexto, 'eje (colorTexto)');

  const sx = paso(l.xMax - l.xMin);
  for (let x = Math.ceil(l.xMin / sx) * sx; x <= l.xMax + 1e-6; x += sx) {
    ctx.strokeStyle = color;
    ctx.beginPath();
    ctx.moveTo(l.px(x), l.py(0));
    ctx.lineTo(l.px(x), l.py(0) + 4);
    ctx.stroke();
    // El cero no se rotula: se lee del cruce de los ejes y ahi choca con el de y.
    if (Math.abs(x) > 1e-9) {
      texto(ctx, String(Math.round(x * 10) / 10), l.px(x), l.py(0) + 16,
        { color: colorTexto, px: 10, peso: 400, alineacion: 'center' });
    }
  }
  const sy = paso(l.yMax - l.yMin);
  for (let y = Math.ceil((l.yMin || sy) / sy) * sy; y <= l.yMax + 1e-6; y += sy) {
    if (Math.abs(y) < 1e-9) continue;
    ctx.strokeStyle = color;
    ctx.beginPath();
    ctx.moveTo(l.px(0), l.py(y));
    ctx.lineTo(l.px(0) - 4, l.py(y));
    ctx.stroke();
    texto(ctx, String(Math.round(y * 10) / 10), l.px(0) - 8, l.py(y) + 3.5,
      { color: colorTexto, px: 10, peso: 400, alineacion: 'right' });
  }
  if (etiquetaX) {
    texto(ctx, etiquetaX, l.px(l.xMax), l.py(0) + 28,
      { color: colorTexto, px: 10, alineacion: 'right' });
  }
  if (etiquetaY) {
    texto(ctx, etiquetaY, l.px(0) - 34, l.py(l.yMax) - 15,
      { color: colorTexto, px: 10, alineacion: 'left' });
  }
}
```

Actualizar el comentario de cabecera del módulo: ahora sí toca `setLineDash`, `font` y
`textAlign`, así que la regla 3 del contrato de estado deja de valer tal como está
escrita y hay que reescribirla diciendo qué deja puesto cada primitiva.

Y hay un cambio de comportamiento que tocar con cuidado: el ensayo de tiro parabólico
dibuja hoy sus propias marcas y rótulos de eje con código local. Al mudarlos a `eje` en
la Tarea 6 tienen que quedar en el **mismo píxel**, porque esa tarea compara capturas.
Por eso los desplazamientos de arriba (`+4`, `+16`, `+28`, `−8`, `−34`, `+3.5`, `−15`)
se copian del diseño y no se redondean.

- [ ] **Paso 4: correr toda la suite**

Ejecutar: `node --test "test/**/*.test.js"`
Esperado: todo verde.

- [ ] **Paso 5: commit**

```bash
git add docs/motor/dibujo.js test/dibujo.test.js
git commit -m "feat(plataforma): vectores en pixeles con punta, guiones y rotulo"
```

---

### Tarea 4: Servicios de página y fábrica de widget

Esto es lo que hoy impide que un ensayo tenga más de un widget: todo el estado del
ensayo de tiro parabólico vive en variables sueltas del módulo, y `window.onscroll` se
asigna directo. Dos widgets en el mismo archivo se pisarían.

**Archivos:**
- Crear: `docs/motor/pagina.js`, `docs/motor/widget.js`
- Prueba: `test/widget.test.js`

**Interfaces:**
- Consume: `crearLienzo` de la Tarea 1.
- Produce:
  - `crearPagina({ documento })` → `{ paleta(), olvidarPaleta(), registrar(widget), repintarTodo(), observar(), tocar(), alTocar(fn), progreso(elemento) }`.
    `paleta()` cachea la lectura de los nueve tokens CSS y devuelve
    `{ paper, band, ink, dim, rule, blue, blueSoft, red, graph }`.
    `tocar()` marca que el lector ya interactuó y dispara los `alTocar`.
  - `crearWidget({ pagina, canvas, margen, encuadre, dibujar })` → `{ repintar(), lienzo() }`.
    `encuadre` es una función sin argumentos que devuelve `{ xMax, yMax, xMin = 0, yMin = 0 }`
    en unidades físicas; se la vuelve a llamar en cada repintado, así que el encuadre
    puede depender de los controles. `dibujar(ctx, lienzo, pagina)` es lo que el widget pinta.

- [ ] **Paso 1: escribir las pruebas que fallan**

Crear `test/widget.test.js`:

```js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { crearPagina } from '../docs/motor/pagina.js';
import { crearWidget } from '../docs/motor/widget.js';

// Documento falso: lo mínimo que pagina.js y widget.js le piden al DOM.
function documentoFalso({ tokens = {} } = {}) {
  const raiz = { atributos: {} };
  return {
    documentElement: raiz,
    _tokens: tokens,
    getComputedStyle: () => ({ getPropertyValue: n => tokens[n] || '' }),
  };
}

function canvasFalso(ancho = 800, alto = 400) {
  const ops = [];
  const ctx = new Proxy({ ops }, {
    get: (o, k) => k in o ? o[k] : (...a) => ops.push([k, ...a]),
    set: (o, k, v) => { o[k] = v; return true; },
  });
  return {
    ops,
    style: {},
    width: 0,
    height: 0,
    getContext: () => ctx,
    getBoundingClientRect: () => ({ width: ancho, height: alto, left: 0, top: 0 }),
    parentElement: { getBoundingClientRect: () => ({ width: ancho }) },
  };
}

test('la paleta se lee una vez y se cachea hasta que se la olvida', () => {
  let lecturas = 0;
  const doc = documentoFalso({ tokens: { '--blue': '#1b4fd4' } });
  doc.getComputedStyle = () => { lecturas++; return { getPropertyValue: n => n === '--blue' ? '#1b4fd4' : '' }; };
  const p = crearPagina({ documento: doc });
  p.paleta(); p.paleta(); p.paleta();
  assert.equal(lecturas, 1);
  p.olvidarPaleta();
  p.paleta();
  assert.equal(lecturas, 2);
});

test('la paleta expone los nueve tokens con nombres en camello', () => {
  const doc = documentoFalso({ tokens: { '--blue-soft': '#8aa3e6' } });
  const p = crearPagina({ documento: doc });
  const pal = p.paleta();
  assert.deepEqual(Object.keys(pal).sort(),
    ['band', 'blue', 'blueSoft', 'dim', 'graph', 'ink', 'paper', 'red', 'rule']);
  assert.equal(pal.blueSoft, '#8aa3e6');
});

test('repintarTodo repinta cada widget registrado, una vez cada uno', () => {
  const doc = documentoFalso();
  const p = crearPagina({ documento: doc });
  const cuenta = { a: 0, b: 0 };
  p.registrar({ repintar: () => cuenta.a++ });
  p.registrar({ repintar: () => cuenta.b++ });
  p.repintarTodo();
  assert.deepEqual(cuenta, { a: 1, b: 1 });
});

test('tocar avisa a los suscriptos una sola vez', () => {
  const p = crearPagina({ documento: documentoFalso() });
  let avisos = 0;
  p.alTocar(() => avisos++);
  p.tocar();
  p.tocar();
  p.tocar();
  assert.equal(avisos, 1);
});

test('el widget escala el canvas por devicePixelRatio y limpia antes de dibujar', () => {
  const p = crearPagina({ documento: documentoFalso() });
  const cv = canvasFalso(800, 400);
  const w = crearWidget({
    pagina: p, canvas: cv, dpr: 2,
    margen: { L: 60, R: 20, T: 30, B: 40 },
    encuadre: () => ({ xMax: 10, yMax: 5 }),
    dibujar: () => {},
  });
  w.repintar();
  assert.equal(cv.width, 1600);
  const nombres = cv.ops.map(o => o[0]);
  assert.ok(nombres.includes('setTransform'));
  assert.ok(nombres.includes('clearRect'));
  assert.ok(nombres.indexOf('clearRect') < nombres.length);
});

test('el lienzo del widget lleva el margen que se le dio', () => {
  const p = crearPagina({ documento: documentoFalso() });
  const cv = canvasFalso(800, 400);
  const margen = { L: 60, R: 20, T: 30, B: 40 };
  const w = crearWidget({
    pagina: p, canvas: cv, dpr: 1, margen,
    encuadre: () => ({ xMax: 10, yMax: 5 }),
    dibujar: () => {},
  });
  w.repintar();
  assert.deepEqual(w.lienzo().margen, margen);
  assert.equal(w.lienzo().px(0), 60);
});

test('el encuadre se vuelve a consultar en cada repintado', () => {
  const p = crearPagina({ documento: documentoFalso() });
  const cv = canvasFalso(800, 400);
  let xMax = 10;
  const w = crearWidget({
    pagina: p, canvas: cv, dpr: 1, margen: { L: 0, R: 0, T: 0, B: 0 },
    encuadre: () => ({ xMax, yMax: 5 }),
    dibujar: () => {},
  });
  w.repintar();
  assert.equal(w.lienzo().xMax, 10);
  xMax = 40;
  w.repintar();
  assert.equal(w.lienzo().xMax, 40);
});

test('un canvas sin ancho no rompe: el widget no dibuja', () => {
  const p = crearPagina({ documento: documentoFalso() });
  const cv = canvasFalso(0, 0);
  let dibujos = 0;
  const w = crearWidget({
    pagina: p, canvas: cv, dpr: 1, margen: { L: 0, R: 0, T: 0, B: 0 },
    encuadre: () => ({ xMax: 10, yMax: 5 }),
    dibujar: () => { dibujos++; },
  });
  w.repintar();
  assert.equal(dibujos, 0);
});

test('crear un widget lo registra en la pagina', () => {
  const p = crearPagina({ documento: documentoFalso() });
  const cv = canvasFalso();
  crearWidget({
    pagina: p, canvas: cv, dpr: 1, margen: { L: 0, R: 0, T: 0, B: 0 },
    encuadre: () => ({ xMax: 1, yMax: 1 }),
    dibujar: () => {},
  });
  assert.equal(p.widgets().length, 1);
});
```

- [ ] **Paso 2: correrlas y verificar que fallan**

Ejecutar: `node --test test/widget.test.js`
Esperado: FALLAN todas; los módulos no existen.

- [ ] **Paso 3: implementar `docs/motor/pagina.js`**

```js
// Servicios que comparten todos los widgets de una pagina: la paleta leida de los
// tokens CSS, el registro de widgets para repintarlos juntos cuando cambia el tema o
// el tamano, la barra de progreso de lectura, y la marca de "el lector ya toco algo",
// que es la que apaga el pulso del boton.

const TOKENS = [
  ['paper', '--paper'], ['band', '--band'], ['ink', '--ink'], ['dim', '--dim'],
  ['rule', '--rule'], ['blue', '--blue'], ['blueSoft', '--blue-soft'],
  ['red', '--red'], ['graph', '--graph'],
];

export function crearPagina({ documento = globalThis.document } = {}) {
  const registrados = [];
  const suscriptos = [];
  let cache = null;
  let tocada = false;
  let observador = null;

  const api = {
    paleta() {
      if (cache) return cache;
      const cs = documento.getComputedStyle
        ? documento.getComputedStyle(documento.documentElement)
        : globalThis.getComputedStyle(documento.documentElement);
      cache = {};
      for (const [nombre, token] of TOKENS) cache[nombre] = cs.getPropertyValue(token).trim();
      return cache;
    },
    olvidarPaleta() { cache = null; },
    registrar(widget) { registrados.push(widget); },
    widgets() { return registrados.slice(); },
    repintarTodo() { for (const w of registrados) w.repintar(); },
    observar() {
      if (typeof ResizeObserver !== 'function') return;
      if (observador) observador.disconnect();
      observador = new ResizeObserver(() => api.repintarTodo());
      for (const w of registrados) {
        const padre = w.canvas && w.canvas.parentElement;
        if (padre) observador.observe(padre);
      }
    },
    tocar() {
      if (tocada) return;
      tocada = true;
      for (const fn of suscriptos) fn();
    },
    tocada() { return tocada; },
    alTocar(fn) { suscriptos.push(fn); },
    progreso(elemento) {
      if (!elemento || typeof globalThis.addEventListener !== 'function') return;
      globalThis.addEventListener('scroll', () => {
        const max = documento.documentElement.scrollHeight - globalThis.innerHeight;
        const pct = max > 0 ? Math.min(100, (globalThis.scrollY / max) * 100) : 0;
        elemento.style.width = pct + '%';
      });
    },
  };
  return api;
}
```

- [ ] **Paso 4: implementar `docs/motor/widget.js`**

La altura y la escala salen literales del `view()` del diseño
(`docs/plataforma/diseno/Tiro parabolico.dc.html:357-374`): alto acotado entre 215 y
430 px, `devicePixelRatio` acotado a 2, y la escala como el mínimo entre lo que entra
a lo ancho y lo que entra a lo alto, para que no se deforme.

```js
import { crearLienzo } from './lienzo.js';

export function crearWidget({ pagina, canvas, margen, encuadre, dibujar, dpr }) {
  let l = null;

  const api = {
    canvas,
    lienzo() { return l; },
    repintar() {
      const ancho = canvas.getBoundingClientRect().width
        || (canvas.parentElement ? canvas.parentElement.getBoundingClientRect().width : 0);
      if (!ancho) return;

      const { xMin = 0, xMax, yMin = 0, yMax } = encuadre();
      const anchoUtil = ancho - margen.L - margen.R;
      const alto = Math.round(Math.max(215, Math.min(430,
        margen.T + margen.B + anchoUtil * ((yMax - yMin) / (xMax - xMin)))));

      const escala = dpr ?? Math.min(2, globalThis.devicePixelRatio || 1);
      canvas.style.aspectRatio = 'auto';
      canvas.style.height = alto + 'px';
      canvas.width = Math.round(ancho * escala);
      canvas.height = Math.round(alto * escala);

      const ctx = canvas.getContext('2d');
      ctx.setTransform(escala, 0, 0, escala, 0, 0);
      ctx.clearRect(0, 0, ancho, alto);
      ctx.lineJoin = 'round';
      ctx.lineCap = 'round';

      // Una sola escala para los dos ejes, para no deformar el dibujo: se elige la
      // que entra, y el margen sobrante queda como aire.
      const sc = Math.min(anchoUtil / (xMax - xMin), (alto - margen.T - margen.B) / (yMax - yMin));
      l = crearLienzo({
        ancho, alto, margen,
        xMin, xMax: xMin + anchoUtil / sc,
        yMin, yMax: yMin + (alto - margen.T - margen.B) / sc,
      });

      dibujar(ctx, l, pagina);
    },
  };

  pagina.registrar(api);
  return api;
}
```

- [ ] **Paso 5: correr toda la suite**

Ejecutar: `node --test "test/**/*.test.js"`
Esperado: todo verde.

- [ ] **Paso 6: commit**

```bash
git add docs/motor/pagina.js docs/motor/widget.js test/widget.test.js
git commit -m "feat(plataforma): servicios de pagina y fabrica de widget"
```

---

### Tarea 5: Controles y arrastre

Cada ensayo cablea hoy sus botones y sliders a mano. Con doce widgets eso son cien
líneas repetidas, y el arrastre —que hoy no existe como pieza— lo necesitan dos
widgets de este plan.

**Archivos:**
- Crear: `docs/motor/controles.js`, `docs/motor/arrastre.js`
- Prueba: `test/controles.test.js`, `test/arrastre.test.js`

**Interfaces:**
- Consume: `crearPagina` de la Tarea 4 (para `tocar()`), `crearLienzo` de la Tarea 1.
- Produce:
  - `deslizador({ entrada, salida, formato, alCambiar, pagina })` — conecta un `<input type="range">` a su `<output>` y a una función. Devuelve `{ valor() }`.
  - `casilla({ entrada, alCambiar, pagina })` — conecta un `<input type="checkbox">`. Devuelve `{ valor() }`.
  - `boton({ elemento, alApretar, pagina })` — conecta un `<button>`.
  - `rotuloReproducir(elemento, escena, enReposo)` — pone en el botón `Reproducir`, `Pausar` o `Seguir`. Es la traducción literal del `label()` del diseño (`docs/plataforma/diseno/Tiro parabolico.dc.html:319-323`): `reproduciendo → 'Pausar'`, y si no, `'Seguir'` cuando **no** está en reposo y el reloj pasó de cero, `'Reproducir'` en cualquier otro caso. El tercer argumento hace falta porque `crearEscena` no distingue "en reposo mostrando un instante representativo" de "pausado a mitad de vuelo": las dos son `estado === 'pausado'` o `'reposo'` con `t > 0`. Esa distinción la lleva el ensayo, igual que el `s.rest` del diseño.
  - `arrastrable({ canvas, lienzo, alArrastrar, acotar, pagina })` — traduce los eventos de puntero a coordenadas físicas y llama a `alArrastrar(x, y)`. `acotar(x, y)` devuelve el par ya acotado.

- [ ] **Paso 1: escribir las pruebas que fallan**

Crear `test/controles.test.js`:

```js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { deslizador, casilla, rotuloReproducir } from '../docs/motor/controles.js';

const entradaFalsa = (valor, tipo = 'range') => ({
  type: tipo, value: String(valor), checked: valor === true, _manejadores: {},
  addEventListener(ev, fn) { this._manejadores[ev] = fn; },
  disparar(ev, v) {
    if (v !== undefined) { this.value = String(v); this.checked = v === true; }
    this._manejadores[ev]({ target: this });
  },
});
const salidaFalsa = () => ({ textContent: '' });
const paginaFalsa = () => { let n = 0; return { tocar: () => n++, toques: () => n }; };

test('el deslizador formatea su salida y avisa el valor numerico', () => {
  const e = entradaFalsa(24), s = salidaFalsa();
  const vistos = [];
  deslizador({ entrada: e, salida: s, formato: v => v.toFixed(1) + ' m/s', alCambiar: v => vistos.push(v) });
  e.disparar('input', 30);
  assert.equal(s.textContent, '30.0 m/s');
  assert.deepEqual(vistos, [30]);
});

test('el deslizador escribe la salida inicial sin esperar a que lo toquen', () => {
  const e = entradaFalsa(24), s = salidaFalsa();
  deslizador({ entrada: e, salida: s, formato: v => Math.round(v) + '°', alCambiar: () => {} });
  assert.equal(s.textContent, '24°');
});

test('el deslizador marca la pagina como tocada', () => {
  const e = entradaFalsa(1), p = paginaFalsa();
  deslizador({ entrada: e, salida: salidaFalsa(), formato: String, alCambiar: () => {}, pagina: p });
  assert.equal(p.toques(), 0);
  e.disparar('input', 2);
  assert.equal(p.toques(), 1);
});

test('la casilla avisa booleanos', () => {
  const e = entradaFalsa(true, 'checkbox');
  const vistos = [];
  casilla({ entrada: e, alCambiar: v => vistos.push(v) });
  e.disparar('change', false);
  assert.deepEqual(vistos, [false]);
});

test('el rotulo del boton dice Reproducir en reposo, aunque el reloj no este en cero', () => {
  // El estado de reposo de los widgets NO es t = 0: es un instante representativo
  // del vuelo. Sin el tercer argumento esto diria "Seguir" al cargar la pagina.
  const b = { textContent: '' };
  rotuloReproducir(b, { estado: 'reposo', t: 1.3, duracion: 3.7 }, true);
  assert.equal(b.textContent, 'Reproducir');
});

test('el rotulo dice Pausar mientras reproduce', () => {
  const b = { textContent: '' };
  rotuloReproducir(b, { estado: 'reproduciendo', t: 3, duracion: 10 }, false);
  assert.equal(b.textContent, 'Pausar');
});

test('el rotulo dice Seguir si esta pausado a mitad de camino', () => {
  const b = { textContent: '' };
  rotuloReproducir(b, { estado: 'pausado', t: 3, duracion: 10 }, false);
  assert.equal(b.textContent, 'Seguir');
});

test('el rotulo dice Seguir tambien al final, como el diseno', () => {
  // El diseno no distingue "pausado a mitad" de "terminado": las dos dicen Seguir,
  // y apretar el boton reinicia desde cero. No se corrige, se copia.
  const b = { textContent: '' };
  rotuloReproducir(b, { estado: 'pausado', t: 10, duracion: 10 }, false);
  assert.equal(b.textContent, 'Seguir');
});

test('el rotulo dice Reproducir si el reloj esta en cero y no se reprodujo nada', () => {
  const b = { textContent: '' };
  rotuloReproducir(b, { estado: 'reposo', t: 0, duracion: 10 }, false);
  assert.equal(b.textContent, 'Reproducir');
});
```

Crear `test/arrastre.test.js`:

```js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { crearLienzo } from '../docs/motor/lienzo.js';
import { arrastrable } from '../docs/motor/arrastre.js';

function canvasFalso() {
  return {
    style: {}, _m: {},
    setPointerCapture() {},
    releasePointerCapture() {},
    addEventListener(ev, fn) { this._m[ev] = fn; },
    disparar(ev, x, y) { this._m[ev]({ clientX: x, clientY: y, pointerId: 1 }); },
    getBoundingClientRect: () => ({ left: 0, top: 0, width: 200, height: 100 }),
  };
}

const lienzo = () => crearLienzo({ ancho: 200, alto: 100, xMin: 0, xMax: 10, yMin: 0, yMax: 5 });

test('sin apretar, mover no avisa nada', () => {
  const cv = canvasFalso();
  const vistos = [];
  arrastrable({ canvas: cv, lienzo, alArrastrar: (x, y) => vistos.push([x, y]) });
  cv.disparar('pointermove', 100, 50);
  assert.deepEqual(vistos, []);
});

test('apretar y mover avisa en coordenadas fisicas', () => {
  const cv = canvasFalso();
  const vistos = [];
  arrastrable({ canvas: cv, lienzo, alArrastrar: (x, y) => vistos.push([x, y]) });
  cv.disparar('pointerdown', 100, 50);
  cv.disparar('pointermove', 20, 20);
  // px 100 -> x 5 ; py 50 -> y 2.5     px 20 -> x 1 ; py 20 -> y 4
  assert.deepEqual(vistos, [[5, 2.5], [1, 4]]);
});

test('soltar corta el arrastre', () => {
  const cv = canvasFalso();
  const vistos = [];
  arrastrable({ canvas: cv, lienzo, alArrastrar: (x, y) => vistos.push([x, y]) });
  cv.disparar('pointerdown', 100, 50);
  cv.disparar('pointerup', 100, 50);
  cv.disparar('pointermove', 20, 20);
  assert.equal(vistos.length, 1);
});

test('acotar se aplica antes de avisar', () => {
  const cv = canvasFalso();
  const vistos = [];
  arrastrable({
    canvas: cv, lienzo,
    acotar: (x, y) => [Math.max(3, x), Math.max(3, y)],
    alArrastrar: (x, y) => vistos.push([x, y]),
  });
  cv.disparar('pointerdown', 20, 20);
  assert.deepEqual(vistos, [[3, 4]]);
});

test('el cursor cambia mientras se arrastra y vuelve al soltar', () => {
  const cv = canvasFalso();
  arrastrable({ canvas: cv, lienzo, alArrastrar: () => {} });
  cv.disparar('pointerdown', 50, 50);
  assert.equal(cv.style.cursor, 'grabbing');
  cv.disparar('pointerup', 50, 50);
  assert.equal(cv.style.cursor, 'grab');
});
```

- [ ] **Paso 2: correrlas y verificar que fallan**

Ejecutar: `node --test test/controles.test.js test/arrastre.test.js`
Esperado: FALLAN todas; los módulos no existen.

- [ ] **Paso 3: implementar `docs/motor/controles.js`**

```js
// Cableado de los controles de un widget. Nada de esto sabe de fisica ni de canvas:
// traduce eventos del DOM a llamadas con valores ya parseados y formateados.

export function deslizador({ entrada, salida, formato, alCambiar, pagina }) {
  const leer = () => parseFloat(entrada.value);
  const pintar = () => { if (salida) salida.textContent = formato(leer()); };
  pintar();
  entrada.addEventListener('input', () => {
    pintar();
    if (pagina) pagina.tocar();
    alCambiar(leer());
  });
  return { valor: leer };
}

export function casilla({ entrada, alCambiar, pagina }) {
  const leer = () => entrada.checked;
  entrada.addEventListener('change', () => {
    if (pagina) pagina.tocar();
    alCambiar(leer());
  });
  return { valor: leer };
}

export function boton({ elemento, alApretar, pagina }) {
  elemento.addEventListener('click', () => {
    if (pagina) pagina.tocar();
    alApretar();
  });
}

// Traduccion literal del label() del diseno
// (docs/plataforma/diseno/Tiro parabolico.dc.html:319-323):
//   s.playing ? 'Pausar' : (!s.rest && s.t > 0 ? 'Seguir' : 'Reproducir')
// `enReposo` es el `s.rest` del diseno. No sale de la escena porque crearEscena no
// distingue "en reposo mostrando un instante representativo" de "pausado a mitad":
// esa distincion la lleva el ensayo, que es quien decide cuando salir del reposo.
export function rotuloReproducir(elemento, escena, enReposo) {
  if (!elemento) return;
  if (escena.estado === 'reproduciendo') { elemento.textContent = 'Pausar'; return; }
  elemento.textContent = !enReposo && escena.t > 0 ? 'Seguir' : 'Reproducir';
}
```

- [ ] **Paso 4: implementar `docs/motor/arrastre.js`**

```js
// Arrastrar un punto sobre un canvas, en coordenadas fisicas. El lienzo se pasa como
// funcion porque cambia en cada repintado: el widget lo reconstruye al cambiar de
// tamano, y un arrastre que guardara el viejo dibujaria corrido.

export function arrastrable({ canvas, lienzo, alArrastrar, acotar, pagina }) {
  let arrastrando = false;

  const puntoDe = evento => {
    const r = canvas.getBoundingClientRect();
    const l = lienzo();
    if (!l) return null;
    let x = l.ux(evento.clientX - r.left);
    let y = l.uy(evento.clientY - r.top);
    if (acotar) [x, y] = acotar(x, y);
    return [x, y];
  };

  canvas.addEventListener('pointerdown', e => {
    arrastrando = true;
    if (canvas.setPointerCapture) canvas.setPointerCapture(e.pointerId);
    canvas.style.cursor = 'grabbing';
    if (pagina) pagina.tocar();
    const p = puntoDe(e);
    if (p) alArrastrar(p[0], p[1]);
  });

  canvas.addEventListener('pointermove', e => {
    if (!arrastrando) return;
    const p = puntoDe(e);
    if (p) alArrastrar(p[0], p[1]);
  });

  const soltar = () => {
    arrastrando = false;
    canvas.style.cursor = 'grab';
  };
  canvas.addEventListener('pointerup', soltar);
  canvas.addEventListener('pointercancel', soltar);

  return { arrastrando: () => arrastrando };
}
```

- [ ] **Paso 5: correr toda la suite**

Ejecutar: `node --test "test/**/*.test.js"`
Esperado: todo verde.

- [ ] **Paso 6: commit**

```bash
git add docs/motor/controles.js docs/motor/arrastre.js test/controles.test.js test/arrastre.test.js
git commit -m "feat(plataforma): controles declarativos y arrastre sobre el canvas"
```

---

## Fase B — terminar el ensayo de tiro parabólico

Las cuatro tareas de esta fase tienen su marcado y su código de dibujo **ya escritos
por el dueño** en `docs/plataforma/diseno/Tiro parabolico.dc.html`. No se inventa nada:
se transcribe y se cablea contra los módulos.

### Tarea 6: Migrar el widget 1 a la fábrica, sin que se note

El ensayo tiene hoy 331 líneas de script con todo su estado en variables sueltas del
módulo. Antes de sumarle tres widgets hay que apoyarlo en las piezas de la Fase A. La
vara de esta tarea es dura y simple: **la página tiene que quedar visualmente idéntica**.

**Archivos:**
- Modificar: `docs/ensayos/tiro-parabolico.html`

**Interfaces:**
- Consume: `crearPagina`, `crearWidget` (Tarea 4); `deslizador`, `casilla`, `boton`,
  `rotuloReproducir` (Tarea 5); `crearLienzo` con `margen` (Tarea 1); `crearEscena`
  con `duracion`/`velocidad`/`ir` (Tarea 2); `vectorPx`, `punteado`, `texto`, `curva` y
  el `eje` con marcas y rótulos (Tarea 3); `cuerpo` (ya existía); `crearTiro` (ya existía).
- Produce: el archivo queda con una función `widgetSombras(pagina)` que arma el widget 1
  entero y no deja nada en el ámbito del módulo salvo la llamada a `crearPagina`.

- [ ] **Paso 1: capturar la referencia antes de tocar nada**

Con el servidor andando (`python -m http.server 8080` desde la raíz del worktree):

```bash
chrome --headless --disable-gpu --window-size=1200,1400 \
  --screenshot=/tmp/antes.png --virtual-time-budget=6000 \
  "http://127.0.0.1:8080/docs/ensayos/tiro-parabolico.html"
```

Guardar `/tmp/antes.png`. Es la vara contra la que se compara al final.

- [ ] **Paso 2: reemplazar el rodeo del `translate` por el margen del lienzo**

Hoy los ejes se dibujan construyendo un lienzo auxiliar y trasladando el contexto. Con
la Tarea 1 eso sobra: el lienzo del widget ya nace con el margen `{L:62, R:24, T:38, B:42}`
y `eje` recibe ese mismo lienzo directamente. Borrar el lienzo auxiliar y el
`ctx.translate` / `ctx.restore` que lo envolvían.

- [ ] **Paso 3: reemplazar el estado suelto por la fábrica**

Envolver todo el script en:

```js
const pagina = crearPagina({ documento: document });
widgetSombras(pagina);
pagina.observar();
pagina.progreso(document.getElementById('tp-prog'));
pagina.repintarTodo();
```

y dentro de `widgetSombras(pagina)` mover: el estado (`v0`, `ang`, `huellas`, `enReposo`),
el `crearWidget`, la escena, y el cableado de los controles con `deslizador` / `casilla` /
`boton`. El pulso del botón pasa a colgarse de `pagina.alTocar(...)`.

- [ ] **Paso 4: sacar las cuatro conversiones a mano de velocidad**

Con la Tarea 2, la escena se crea con `velocidad: 0.75` y `duracion: tiro.tVuelo`, y
`dibujar(t)` recibe **tiempo físico**. Borrar la constante `VELOCIDAD` y las cuatro
multiplicaciones y divisiones que la usaban.

- [ ] **Paso 5: reemplazar `rehacerEscena` por los setters**

Las catorce líneas de destruir y reconstruir la escena se vuelven dos:

```js
escena.duracion = tiro.tVuelo;
if (enReposo) escena.ir(0.35 * tiro.tVuelo);
```

Esto además borra de raíz el caso en que el reloj se congelaba al arrastrar un slider,
porque ya no hay reconstrucción.

- [ ] **Paso 6: correr la suite y comparar las capturas**

```bash
node --test "test/**/*.test.js"
chrome --headless --disable-gpu --window-size=1200,1400 \
  --screenshot=/tmp/despues.png --virtual-time-budget=6000 \
  "http://127.0.0.1:8080/docs/ensayos/tiro-parabolico.html"
```

Y después, con Python:

```python
from PIL import Image, ImageChops
a, b = Image.open('/tmp/antes.png'), Image.open('/tmp/despues.png')
assert a.size == b.size, f'{a.size} != {b.size}'
caja = ImageChops.difference(a.convert('RGB'), b.convert('RGB')).getbbox()
print('identicas' if caja is None else f'DIFIEREN en {caja}')
```

Esperado: `identicas`. Si difieren, la diferencia es un defecto de la migración, no una
mejora: el estado de reposo es determinista (`0.35·tVuelo`, sin animación al cargar), así
que dos capturas de la misma página tienen que coincidir píxel a píxel. Informar la caja
que devuelve el script si no coinciden.

- [ ] **Paso 7: commit**

```bash
git add docs/ensayos/tiro-parabolico.html
git commit -m "refactor(plataforma): el ensayo de tiro sobre la fabrica de widgets"
```

---

### Tarea 7: Sección 02 y el widget "Galileo"

**Archivos:**
- Modificar: `docs/ensayos/tiro-parabolico.html`
- Referencia obligatoria: `docs/plataforma/diseno/Tiro parabolico.dc.html:93-130` (marcado) y `:499-530` (dibujo)

**Interfaces:**
- Consume: todo lo de la Tarea 6.
- Produce: `widgetGalileo(pagina)`.

- [ ] **Paso 1: copiar el marcado**

Copiar **byte a byte** las líneas 93 a 130 del archivo de diseño: el `<h2>` de la
sección 02, el párrafo que la abre, la `<section>` completa del widget 2 con sus dos
botones, sus dos sliders (`w2-vx` de 0 a 30 paso 0.5 valor 15; `w2-h` de 5 a 45 paso 1
valor 25), su fila de cuatro lecturas, y los dos párrafos de cierre de la sección.

- [ ] **Paso 2: escribir el dibujo**

Transcripción de `drawW2` del diseño, cableada a los módulos. `g = 9.8`, que es el
valor que usa `parcial-1/soluciones/verificacion-practico-1.py` para todo lo que no es
el ejercicio 15:

```js
function widgetGalileo(pagina) {
  const G = 9.8;
  const X0 = 3;                       // el soltado no arranca pegado al eje
  let vx = 15, altura = 25;

  const tf = () => Math.sqrt(2 * altura / G);
  const yEn = t => altura - 0.5 * G * t * t;

  const canvas = document.getElementById('w2-cv');
  const widget = crearWidget({
    pagina, canvas,
    margen: { L: 58, R: 24, T: 38, B: 42 },
    encuadre: () => ({ xMax: Math.max((X0 + vx * tf()) * 1.1, 10), yMax: altura * 1.12 }),
    dibujar: (ctx, l) => pintar(ctx, l, escena.t),
  });

  const escena = crearEscena({
    dibujar: () => widget.repintar(),
    duracion: tf(),
    velocidad: 0.75,
    alCambiar: () => rotuloReproducir(document.getElementById('w2-play'), escena, enReposo),
  });

  function pintar(ctx, l, t) {
    const p = pagina.paleta();
    const soltado = s => [X0, yEn(s)];
    const lanzado = s => [X0 + vx * s, yEn(s)];

    eje(ctx, l, { color: p.rule, colorTexto: p.dim, etiquetaX: 'x [m]', etiquetaY: 'y [m]' });
    suelo(ctx, l, p.graph);
    curva(ctx, l, lanzado, 0, tf(), { color: p.graph, guiones: [3, 5], grosor: 1.2 });

    // Las lineas horizontales que unen las dos alturas: son el argumento entero del
    // widget, asi que se dibujan hasta el instante actual y no mas alla.
    const n = Math.max(1, Math.round(tf() / 0.3));
    for (let i = 0; i <= n; i++) {
      const s = i * tf() / n;
      if (s > t + 1e-9) break;
      const y = l.py(yEn(s));
      ctx.globalAlpha = 0.55;
      punteado(ctx, l.px(X0), y, l.px(X0 + vx * s), y, { color: p.graph });
      ctx.globalAlpha = 1;
    }

    const a = soltado(t), b = lanzado(t);
    cuerpo(ctx, l, a, { radio: 6.5, color: p.ink });
    cuerpo(ctx, l, b, { radio: 6.5, color: p.blue });
    texto(ctx, 'soltado', l.px(X0) - 11, l.py(altura) - 13,
      { color: p.dim, px: 10, peso: 400, alineacion: 'right' });
    texto(ctx, 'lanzado', l.px(X0) + 11, l.py(altura) - 13,
      { color: p.blue, px: 10, peso: 400 });

    leer('w2-t', t.toFixed(2) + ' s');
    leer('w2-alt', Math.max(0, yEn(t)).toFixed(1) + ' m');
    leer('w2-dif', '0.00 m');
    leer('w2-tf', tf().toFixed(2) + ' s');
  }
```

`suelo(ctx, l, color)` y `leer(id, valor)` son los dos ayudantes que el ensayo ya tiene
de la Tarea 6; si `suelo` no existe todavía, transcribirlo del `ground()` del diseño
(`:431-437`): una línea horizontal en `--graph` más rayitas de 6 px cada 9 px con
`globalAlpha` 0.5.

- [ ] **Paso 3: cablear los controles**

```js
  const alReposo = () => { escena.duracion = tf(); if (enReposo) escena.ir(0.35 * tf()); };
  deslizador({
    entrada: document.getElementById('w2-vx'), salida: document.getElementById('w2-vx-out'),
    formato: v => v.toFixed(1) + ' m/s', pagina,
    alCambiar: v => { vx = v; alReposo(); widget.repintar(); },
  });
  deslizador({
    entrada: document.getElementById('w2-h'), salida: document.getElementById('w2-h-out'),
    formato: v => Math.round(v) + ' m', pagina,
    alCambiar: v => { altura = v; alReposo(); widget.repintar(); },
  });
```

Los botones `w2-play` y `w2-reset` se cablean igual que los del widget 1.

- [ ] **Paso 4: verificar en el navegador**

Con el servidor andando, abrir la página y comprobar cuatro cosas:
el widget arranca quieto; subir `vₓ` al máximo no cambia el `t de caída`, que es
justamente lo que la frase de "qué mirar" promete; las líneas punteadas quedan
horizontales para todo `vₓ`; y `diferencia de alturas` se queda en `0.00 m` todo el vuelo.

Con `altura = 25` y `g = 9.8`, el tiempo de caída es `√(2·25/9.8) = 2.26 s`, que es el
valor que el propio marcado del diseño trae escrito en `w2-tf`.

- [ ] **Paso 5: correr la suite y commitear**

```bash
node --test "test/**/*.test.js"
git add docs/ensayos/tiro-parabolico.html
git commit -m "feat(plataforma): seccion 02 y el widget de Galileo"
```

---

### Tarea 8: Sección 03 y el widget "El triángulo de v₀"

Es el widget que contesta la Duda 3 del archivo de dudas: de dónde sale el seno. Es
también el primero que se arrastra.

**Archivos:**
- Modificar: `docs/ensayos/tiro-parabolico.html`
- Referencia obligatoria: `docs/plataforma/diseno/Tiro parabolico.dc.html:132-168` (marcado) y `:533-573` (dibujo)

**Interfaces:**
- Consume: todo lo anterior más `arrastrable` (Tarea 5).
- Produce: `widgetTriangulo(pagina)`.

- [ ] **Paso 1: copiar el marcado**

Ojo con la costura, que no es una regresión sino el precio de cortar el diseño por
secciones: el `<div>` de texto que la Tarea 7 cerró con `padding:0 24px 80px` es el
mismo que en el diseño sigue hasta la sección 03. Al insertar esta sección hay que
deshacer ese cierre y devolverle su `padding:0 24px`, igual que la Tarea 7 deshizo el
de la Tarea 6. El `80px` vuelve recién en el último bloque del ensayo.

Copiar byte a byte las líneas 132 a 168 del diseño: el `<h2>` de la sección 03, su
párrafo, la `<section>` con el canvas `w3-cv` —que lleva `cursor:grab`—, los dos botones
de preset (`w3-p45` dice `45°`, `w3-p30` dice `Ej. 9`), la casilla `w3-vert`, la fila de
cuatro lecturas, los dos párrafos siguientes, el bloque de fórmulas con su borde
izquierdo, y el párrafo del alcance máximo en 45°.

- [ ] **Paso 2: escribir el dibujo**

Transcripción de `drawW3`. El encuadre es fijo, 44 × 44 m/s, y el margen derecho es
grande (130 px) porque ahí van los rótulos:

```js
function widgetTriangulo(pagina) {
  const RAD = Math.PI / 180;
  let vx = 16.1, vy = 19.2, desdeVertical = false;

  const canvas = document.getElementById('w3-cv');
  const widget = crearWidget({
    pagina, canvas,
    margen: { L: 62, R: 130, T: 38, B: 48 },
    encuadre: () => ({ xMax: 44, yMax: 44 }),
    dibujar: pintar,
  });

  function pintar(ctx, l) {
    const p = pagina.paleta();
    const ox = l.px(0), oy = l.py(0), tx = l.px(vx), ty = l.py(vy);

    eje(ctx, l, { color: p.rule, colorTexto: p.dim, etiquetaX: 'vₓ [m/s]', etiquetaY: 'v_y [m/s]' });

    // Las dos sombras del vector, que son las mismas de la simulacion 1 en t = 0.
    vectorPx(ctx, ox, oy, tx, oy, { color: p.blue, grosor: 1.4, punta: 7, guiones: [4, 4] });
    vectorPx(ctx, tx, oy, tx, ty, { color: p.blue, grosor: 1.4, punta: 7, guiones: [4, 4] });
    punteado(ctx, ox, ty, tx, ty, { color: p.blueSoft });

    texto(ctx, (desdeVertical ? 'v₀ sen α' : 'v₀ cos α') + ' = ' + vx.toFixed(1),
      (ox + tx) / 2, oy + 33, { color: p.blue, alineacion: 'center' });
    texto(ctx, (desdeVertical ? 'v₀ cos α' : 'v₀ sen α') + ' = ' + vy.toFixed(1),
      tx + 10, (oy + ty) / 2 + 4, { color: p.blue });

    const modulo = Math.hypot(vx, vy), ang = Math.atan2(vy, vx);
    const r = Math.min(46, l.escala.x * modulo * 0.5);
    ctx.strokeStyle = p.ink;
    ctx.lineWidth = 1.2;
    ctx.beginPath();
    if (desdeVertical) ctx.arc(ox, oy, r, -Math.PI / 2, -ang, false);
    else ctx.arc(ox, oy, r, 0, -ang, true);
    ctx.stroke();
    const medio = desdeVertical ? -(Math.PI / 2 + ang) / 2 - Math.PI / 4 : -ang / 2;
    texto(ctx, 'α', ox + Math.cos(medio) * (r + 13), oy + Math.sin(medio) * (r + 13) + 4,
      { color: p.ink, alineacion: 'center' });

    vectorPx(ctx, ox, oy, tx, ty, { color: p.ink, grosor: 2.6, punta: 12 });
    cuerpo(ctx, l, [vx, vy], { radio: 7, color: p.blue });
    cuerpo(ctx, l, [vx, vy], { radio: 3, color: p.paper });
    texto(ctx, 'v₀ = ' + modulo.toFixed(1) + ' m/s', tx + 14, ty - 8, { color: p.ink });
    texto(ctx, 'arrastrá →', tx + 14, ty + 8, { color: p.dim, px: 10, peso: 400 });

    const grados = desdeVertical ? 90 - ang / RAD : ang / RAD;
    leer('w3-v0', modulo.toFixed(1) + ' m/s');
    leer('w3-ang', Math.round(grados) + '°');
    leer('w3-vx', vx.toFixed(1) + ' m/s');
    leer('w3-vy', vy.toFixed(1) + ' m/s');
    leer('w3-lx', 'vₓ = v₀·' + (desdeVertical ? 'sen' : 'cos') + ' α');
    leer('w3-ly', 'v_y = v₀·' + (desdeVertical ? 'cos' : 'sen') + ' α');
  }
```

Notar el detalle que hace al argumento del widget: al tildar la casilla **el vector no
se mueve**; lo único que cambia es desde qué eje se mide el ángulo y, por lo tanto,
cuál de las dos componentes se llama seno.

- [ ] **Paso 3: cablear el arrastre y los controles**

El acotado sale literal del diseño (`:307-310`): las dos componentes no bajan de 0.5,
el módulo se acota a 40 por arriba y a 6 por abajo.

```js
  arrastrable({
    canvas, pagina, lienzo: () => widget.lienzo(),
    acotar: (x, y) => {
      x = Math.max(0.5, x);
      y = Math.max(0.5, y);
      const m = Math.hypot(x, y);
      if (m > 40) { x *= 40 / m; y *= 40 / m; }
      if (m < 6) { x *= 6 / m; y *= 6 / m; }
      return [x, y];
    },
    alArrastrar: (x, y) => { vx = x; vy = y; widget.repintar(); },
  });

  const preset = (v0, grados) => {
    vx = v0 * Math.cos(grados * RAD);
    vy = v0 * Math.sin(grados * RAD);
    widget.repintar();
  };
  boton({ elemento: document.getElementById('w3-p45'), pagina, alApretar: () => preset(25, 45) });
  boton({ elemento: document.getElementById('w3-p30'), pagina, alApretar: () => preset(20, 30) });
  casilla({
    entrada: document.getElementById('w3-vert'), pagina,
    alCambiar: v => { desdeVertical = v; widget.repintar(); },
  });
```

- [ ] **Paso 4: verificar en el navegador**

Cuatro comprobaciones: arrastrar mueve la punta y las lecturas siguen; el preset `45°`
deja `vₓ` y `v_y` iguales entre sí (`25·cos45° = 25·sen45° = 17.7`); tildar la casilla
intercambia los rótulos **sin mover el vector**; y el arco del ángulo cambia de lado
—del eje x al eje y— al tildarla.

- [ ] **Paso 5: correr la suite y commitear**

```bash
node --test "test/**/*.test.js"
git add docs/ensayos/tiro-parabolico.html
git commit -m "feat(plataforma): seccion 03 y el triangulo de v0"
```

---

### Tarea 9: Sección 04, el widget "Con viento" y el cierre

Cierra el ensayo. El widget es el ejercicio 15, y el cierre es la receta de cuatro pasos
para resolver 9, 10 y 15.

**Archivos:**
- Modificar: `docs/ensayos/tiro-parabolico.html`
- Referencia obligatoria: `docs/plataforma/diseno/Tiro parabolico.dc.html:170-216` (marcado) y `:576-608` (dibujo)

**Interfaces:**
- Consume: todo lo anterior.
- Produce: `widgetViento(pagina)`, y el ensayo queda completo.

- [ ] **Paso 1: copiar el marcado**

Copiar byte a byte las líneas 170 a 216: el `<h2>` de la sección 04, su párrafo, la
`<section>` con el canvas `w4-cv`, los botones, el slider `w4-ax` —que va de −8 a 8 paso
0.2 valor 0 y lleva `accent-color:var(--red)` porque es una aceleración—, el slider
`w4-ang` de 15 a 80 valor 55, la fila de cuatro lecturas, el párrafo de cierre de la
sección, el `<h2>` "Para resolver 9, 10 y 15", la lista ordenada de cuatro pasos, la
línea divisoria y el pie con las fuentes.

En el pie, reemplazar los dos `href="#"` por los enlaces reales:
`../../parcial-1/preparacion/resumen-tiro-parabolico.pdf` y
`../../parcial-1/practicos/practico_1_2026.pdf`.

- [ ] **Paso 2: escribir el dibujo**

Transcripción de `drawW4`. Acá `v0` está fijo en 20 m/s y el que se mueve es el ángulo;
la curva gris es el tiro sin viento y la azul el tiro con viento:

```js
function widgetViento(pagina) {
  const G = 9.8, V0 = 20;
  let ax = 0, grados = 55;

  const conViento = () => crearTiro({ v0: V0, alfaGrados: grados, ax, g: G });
  const sinViento = () => crearTiro({ v0: V0, alfaGrados: grados, g: G });

  const canvas = document.getElementById('w4-cv');
  const widget = crearWidget({
    pagina, canvas,
    margen: { L: 62, R: 24, T: 38, B: 42 },
    encuadre: () => {
      const s = sinViento(), c = conViento();
      const xMin = Math.min(0, c.alcance * 1.08);
      const xMax = Math.max(s.alcance, c.alcance, 5) * 1.08;
      return { xMin, xMax, yMax: Math.max(s.yMax, 1) * 1.3 };
    },
    dibujar: (ctx, l) => pintar(ctx, l, escena.t),
  });

  const escena = crearEscena({
    dibujar: () => widget.repintar(),
    duracion: sinViento().tVuelo,
    velocidad: 0.75,
    alCambiar: () => rotuloReproducir(document.getElementById('w4-play'), escena, enReposo),
  });

  function pintar(ctx, l, t) {
    const p = pagina.paleta();
    const s = sinViento(), c = conViento();
    const tf = s.tVuelo, H = s.yMax;

    eje(ctx, l, { color: p.rule, colorTexto: p.dim, etiquetaX: 'x [m]', etiquetaY: 'y [m]' });
    curva(ctx, l, s.pos, 0, tf, { color: p.graph, guiones: [3, 5], grosor: 1.2 });
    curva(ctx, l, c.pos, 0, tf, { color: p.blue, grosor: 1.9 });

    // El corrimiento en el punto medio del vuelo: es la lectura que el widget pide mirar.
    const mr = s.pos(tf / 2), ma = c.pos(tf / 2);
    punteado(ctx, ...l.p(mr), ...l.p(ma), { color: p.red });
    cuerpo(ctx, l, mr, { radio: 3.5, color: p.graph });
    cuerpo(ctx, l, ma, { radio: 3.5, color: p.blue });

    // La altura maxima, que no se mueve por mas viento que haya: es el punto del widget.
    punteado(ctx, l.px(l.xMin), l.py(H), l.px(l.xMax), l.py(H), { color: p.rule });
    texto(ctx, 'altura máx — no cambia', l.px(l.xMin) + 6, l.py(H) - 6,
      { color: p.dim, px: 10, peso: 400 });

    const [cx, cy] = l.p(c.pos(t));
    if (Math.abs(ax) > 0.05) {
      vectorPx(ctx, cx, cy, cx + Math.sign(ax) * (18 + Math.abs(ax) * 3.4), cy, {
        color: p.red, grosor: 1.8, punta: 8, rotulo: 'aₓ', rdy: -8,
        rAlineacion: Math.sign(ax) > 0 ? 'left' : 'right',
        rdx: Math.sign(ax) > 0 ? 6 : -6,
      });
    }
    vectorPx(ctx, cx, cy, cx, cy + 26, { color: p.red, grosor: 1.6, punta: 7 });
    cuerpo(ctx, l, c.pos(t), { radio: 5.5, color: p.ink });

    const dif = c.alcance - s.alcance;
    leer('w4-alc', c.alcance.toFixed(1) + ' m');
    leer('w4-dif', (dif >= 0 ? '+' : '') + dif.toFixed(1) + ' m');
    leer('w4-tf', tf.toFixed(2) + ' s');
    leer('w4-hmax', H.toFixed(1) + ' m');
  }
```

Este widget es el primero que consume `crearTiro` con `ax`, que existe desde el plan 1
y está probado contra el ejercicio 15 del `verificacion-practico-1.py`.

- [ ] **Paso 3: cablear los controles**

```js
  const alReposo = () => {
    escena.duracion = sinViento().tVuelo;
    if (enReposo) escena.ir(0.35 * sinViento().tVuelo);
  };
  deslizador({
    entrada: document.getElementById('w4-ax'), salida: document.getElementById('w4-ax-out'),
    formato: v => v.toFixed(1) + ' m/s²', pagina,
    alCambiar: v => { ax = v; widget.repintar(); },
  });
  deslizador({
    entrada: document.getElementById('w4-ang'), salida: document.getElementById('w4-ang-out'),
    formato: v => Math.round(v) + '°', pagina,
    alCambiar: v => { grados = v; alReposo(); widget.repintar(); },
  });
```

Fijarse en la asimetría, que es deliberada y es el argumento del widget: mover `aₓ` **no**
toca `escena.duracion`, porque el viento no cambia el tiempo de vuelo. Mover el ángulo sí.

- [ ] **Paso 4: verificar en el navegador**

Con `α = 55°`, `v₀ = 20` y `g = 9.8`: `t de vuelo = 2·20·sen55°/9.8 = 3.34 s` y
`altura máx = (20·sen55°)²/(2·9.8) = 13.7 m`. Mover `aₓ` de −8 a 8 y confirmar que esas
dos lecturas **no se mueven ni un decimal**, mientras alcance y corrimiento sí. Es
exactamente lo que el párrafo de cierre de la sección afirma.

- [ ] **Paso 5: recorrer el ensayo entero**

Es el primer momento en que las cuatro simulaciones conviven. Comprobar que ninguna se
anima sola al cargar, que reproducir una no arranca las otras, que cambiar el tema
repinta las cuatro, y que achicar la ventana a 400 px de ancho no rompe ninguna.

- [ ] **Paso 6: correr la suite y commitear**

```bash
node --test "test/**/*.test.js"
git add docs/ensayos/tiro-parabolico.html
git commit -m "feat(plataforma): seccion 04, el viento y el cierre del ensayo de tiro"
```

---

### Tarea 10b: Escala no uniforme y altos parametrizables

*Tarea insertada durante la ejecución, a partir de un bloqueo real de la Tarea 11.*

`crearWidget` usaba una sola escala para los dos ejes. Es correcto en el ensayo de tiro
—los dos ejes son metros, y una parábola tiene que verse como una parábola— pero este
ensayo grafica magnitudes **contra tiempo**, y ahí esa regla no significa nada físico.
Medido sobre un canvas de 880 px:

| widget | ejes | ratio | usa del ancho útil |
|---|---|---|---|
| tiro, widget 1 | m × m | 0.35 | 100.0 % |
| derivada, la secante | s × m | 4.42 | 10.0 % |
| derivada, los paneles | s × — | 0.88 | 53.7 % |
| derivada, el área | s × m/s | 11.18 | 3.9 % |

**Archivos:**
- Modificar: `docs/motor/widget.js`
- Prueba: `test/widget.test.js`

**Interfaces:**
- Produce: `crearWidget({ ..., escalaUniforme = true, altoMin = 215, altoMax = 430 })`.
  Con `escalaUniforme: false` el alto sale de la proporción 16:8 del sistema de diseño
  (`ancho / 2`, brief §6.4) acotada entre `altoMin` y `altoMax`, las dos escalas se
  calculan independientes y cada una llena su dimensión, y el lienzo reporta los bordes
  pedidos exactos — con escala no uniforme la distinción entre pedido y estirado
  desaparece. `altoMin`/`altoMax` existen porque el widget de tres paneles apilados no
  entra en el piso de 215: cada panel quedaría en 54 px, casi enteros consumidos por el
  rótulo y la fila de números.

El camino uniforme no cambia ni un píxel, y eso se verifica comparando el bitmap de los
cuatro canvas del ensayo de tiro por hash, con el caché de Chrome desactivado y un
control negativo que confirme que la comparación no es vacía.

---

## Fase C — el ensayo de derivada e integral

Es el ensayo más valioso de los seis: el capítulo 1 del apunte construye el cálculo
desde cero porque sin eso la mitad de la Guía 1 no se resuelve, y es exactamente el
contenido donde ver la construcción vale más que leerla. Cubre los ejercicios 1 a 8.

Este ensayo **no tiene archivo de diseño propio**. Aplica el sistema cerrado: la
estructura de secciones, la anatomía del widget y los valores tipográficos salen de
`docs/plataforma/diseno/Tiro parabolico.dc.html`, que es la implementación de
referencia del sistema. Ningún valor visual se inventa.

### Tarea 10: Cálculo numérico

**Archivos:**
- Crear: `docs/fisica/calculo.js`
- Modificar: `parcial-1/soluciones/verificacion-practico-1.py`
- Prueba: `test/calculo.test.js`

**Interfaces:**
- Consume: nada.
- Produce:
  - `derivar(f, t, h = 1e-4)` — derivada por diferencia centrada.
  - `integrar(f, t0, t1, n = 400)` — integral por Simpson compuesto; `n` se redondea al par de arriba.
  - `muestrear(f, t0, t1, n)` — devuelve `n + 1` pares `[t, f(t)]`.
  - `derivarMuestras(puntos)` — recibe pares `[t, x]` y devuelve pares `[t, dx/dt]` por diferencia centrada en el interior y hacia adelante o atrás en los bordes.
  - `suavizar(puntos, ventana = 5)` — promedio móvil sobre la segunda componente; la primera queda igual.

- [ ] **Paso 1: dejar respaldado el camino recorrido del ejercicio 4**

El ensayo va a afirmar que entre `t = 0` y `t = 3.4` el móvil del ejercicio 4 se desplaza
0 m pero recorre 28.9 m. `x_max = 349/20` ya está en el script; el camino no. Agregar al
bloque del ejercicio 4 de `parcial-1/soluciones/verificacion-practico-1.py`, después de
la línea que imprime `x_max`:

```python
t_vuelta = sp.solve(sp.Eq(x4, x4.subs(t, 0)), t)
t_v = max([s for s in t_vuelta if s > 0])
camino = 2 * (x4.subs(t, Rational(17, 10)) - x4.subs(t, 0))
print(f"  x(t) vuelve a x(0) en t = {float(t_v):.1f} s")
print(f"  desplazamiento en [0, {float(t_v):.1f}] = 0 m   camino = {float(camino):.1f} m")
```

Usá el estilo que el archivo ya tiene —`sp.Eq`, `sp.solve`, `Rational` importado directo—
y no introduzcas símbolos auxiliares: `x4` ya depende de `t`.

Correr `python parcial-1/soluciones/verificacion-practico-1.py` y anotar la salida:
tiene que decir `t = 3.4 s` y `camino = 28.9 m`. Si no coincide, **no seguir**: el número
del ensayo sale de acá, no al revés.

- [ ] **Paso 2: escribir las pruebas que fallan**

Crear `test/calculo.test.js`:

```js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { derivar, integrar, muestrear, derivarMuestras, suavizar } from '../docs/fisica/calculo.js';

const cerca = (a, b, tol = 1e-6) =>
  assert.ok(Math.abs(a - b) < tol, `${a} != ${b} (tol ${tol})`);

// Ejercicio 1 del practico 1: x(t) = -3 + 2 t^3, con v(t) = 6 t^2.
const x1 = t => -3 + 2 * t ** 3;

test('ejercicio 1: la derivada en t = 0 es cero y en t = 0.8 es 3.84', () => {
  cerca(derivar(x1, 0), 0, 1e-6);
  cerca(derivar(x1, 0.8), 3.84, 1e-5);
});

test('ejercicio 1: la velocidad media en [-1, 1] es 2 m/s', () => {
  cerca((x1(1) - x1(-1)) / 2, 2, 1e-12);
});

// Ejercicio 4: x(t) = 3 + 17 t - 5 t^2, v(t) = 17 - 10 t, a = -10.
const x4 = t => 3 + 17 * t - 5 * t ** 2;
const v4 = t => 17 - 10 * t;

test('ejercicio 4: la derivada reproduce v(t) = 17 - 10 t', () => {
  for (const t of [0, 1, 1.7, 3]) cerca(derivar(x4, t), v4(t), 1e-4);
});

test('ejercicio 4: la derivada segunda es la aceleracion constante -10', () => {
  const a = t => derivar(s => derivar(x4, s), t, 1e-3);
  cerca(a(1), -10, 1e-3);
  cerca(a(2.5), -10, 1e-3);
});

test('ejercicio 4: la integral de v da el desplazamiento, que en [0, 3.4] es cero', () => {
  cerca(integrar(v4, 0, 3.4), 0, 1e-9);
  cerca(integrar(v4, 0, 1.7), 14.45, 1e-9);   // x_max - x(0) = 349/20 - 3
});

test('la integral es exacta en un polinomio de grado tres, que es lo que Simpson promete', () => {
  cerca(integrar(t => t ** 3, 0, 2), 4, 1e-9);
});

test('integrar respeta el signo: de derecha a izquierda da lo mismo cambiado', () => {
  cerca(integrar(v4, 1.7, 0), -14.45, 1e-9);
});

test('muestrear devuelve n + 1 pares, del primero al ultimo inclusive', () => {
  const m = muestrear(t => t * t, 0, 2, 4);
  assert.equal(m.length, 5);
  assert.deepEqual(m[0], [0, 0]);
  assert.deepEqual(m[4], [2, 4]);
});

test('derivarMuestras recupera la pendiente de una recta en todos los puntos', () => {
  const m = muestrear(t => 3 * t + 1, 0, 1, 10);
  for (const [, d] of derivarMuestras(m)) cerca(d, 3, 1e-9);
});

test('derivarMuestras devuelve tantos puntos como recibe', () => {
  const m = muestrear(t => t ** 2, 0, 1, 7);
  assert.equal(derivarMuestras(m).length, m.length);
});

test('derivarMuestras aproxima 2t en una parabola, tambien en los bordes', () => {
  const m = muestrear(t => t ** 2, 0, 2, 200);
  const d = derivarMuestras(m);
  cerca(d[100][1], 2 * d[100][0], 1e-3);
  cerca(d.at(-1)[1], 4, 2e-2);            // el borde es de primer orden, tolera mas
});

test('suavizar no mueve una recta', () => {
  const m = muestrear(t => 2 * t, 0, 1, 20);
  for (const [i, [, y]] of suavizar(m).entries()) cerca(y, m[i][1], 1e-9);
});

test('suavizar aplasta un pico aislado', () => {
  const m = muestrear(() => 0, 0, 1, 20);
  m[10][1] = 10;
  const s = suavizar(m, 5);
  assert.ok(s[10][1] < 10, 'el pico tiene que bajar');
  assert.ok(s[10][1] > 0, 'pero no desaparecer');
});

test('suavizar conserva la cantidad de puntos y los tiempos', () => {
  const m = muestrear(t => Math.sin(t), 0, 6, 30);
  const s = suavizar(m);
  assert.equal(s.length, m.length);
  for (const [i, [t]] of s.entries()) cerca(t, m[i][0], 1e-12);
});
```

- [ ] **Paso 3: correrlas y verificar que fallan**

Ejecutar: `node --test test/calculo.test.js`
Esperado: FALLAN todas, el módulo no existe.

- [ ] **Paso 4: implementar**

```js
// Calculo numerico para los widgets. Nada de esto pretende ser un metodo de referencia:
// pretende ser estable a la vista, que es un requisito distinto. Una derivada ruidosa
// se nota como un temblor en el grafico aunque el error sea chico.

export function derivar(f, t, h = 1e-4) {
  return (f(t + h) - f(t - h)) / (2 * h);
}

export function integrar(f, t0, t1, n = 400) {
  const m = n % 2 ? n + 1 : n;            // Simpson necesita un numero par de tramos
  const h = (t1 - t0) / m;
  let s = f(t0) + f(t1);
  for (let i = 1; i < m; i++) s += f(t0 + i * h) * (i % 2 ? 4 : 2);
  return (s * h) / 3;
}

export function muestrear(f, t0, t1, n) {
  const pts = [];
  for (let i = 0; i <= n; i++) {
    const t = t0 + ((t1 - t0) * i) / n;
    pts.push([t, f(t)]);
  }
  return pts;
}

export function derivarMuestras(puntos) {
  const n = puntos.length;
  if (n < 2) return puntos.map(([t]) => [t, 0]);
  return puntos.map(([t], i) => {
    if (i === 0) {
      const [t1, x1] = puntos[0], [t2, x2] = puntos[1];
      return [t, (x2 - x1) / (t2 - t1)];
    }
    if (i === n - 1) {
      const [t1, x1] = puntos[n - 2], [t2, x2] = puntos[n - 1];
      return [t, (x2 - x1) / (t2 - t1)];
    }
    const [ta, xa] = puntos[i - 1], [tb, xb] = puntos[i + 1];
    return [t, (xb - xa) / (tb - ta)];
  });
}

export function suavizar(puntos, ventana = 5) {
  // Promedio movil con ventana simetrica tambien en los bordes: en vez de recortar
  // la ventana contra el borde —lo que sesga el promedio y curva una recta— se
  // extiende la serie por reflexion impar alrededor del punto extremo. Esa
  // extension es la unica que deja una recta exactamente igual tras suavizar, que
  // es lo que la prueba `suavizar no mueve una recta` exige: si se recorta, el
  // primer punto de una rampa se corre y el panel de velocidad deja de ser plano.
  const n = puntos.length;
  const r = Math.floor(ventana / 2);
  const valor = i => {
    if (i < 0) return 2 * puntos[0][1] - puntos[Math.min(-i, n - 1)][1];
    if (i >= n) return 2 * puntos[n - 1][1] - puntos[Math.max(2 * (n - 1) - i, 0)][1];
    return puntos[i][1];
  };
  return puntos.map(([t], i) => {
    let suma = 0;
    for (let k = i - r; k <= i + r; k++) suma += valor(k);
    return [t, suma / (2 * r + 1)];
  });
}
```

- [ ] **Paso 5: correr toda la suite y commitear**

```bash
node --test "test/**/*.test.js"
python parcial-1/soluciones/verificacion-practico-1.py
git add docs/fisica/calculo.js test/calculo.test.js parcial-1/soluciones/verificacion-practico-1.py
git commit -m "feat(plataforma): calculo numerico, contrastado con el practico 1"
```

---

### Tarea 11: El ensayo y el widget "De la secante a la tangente"

**Archivos:**
- Crear: `docs/ensayos/derivada-integral.html`
- Referencia de sistema: `docs/plataforma/diseno/Tiro parabolico.dc.html`

**Interfaces:**
- Consume: `crearPagina`, `crearWidget`, `deslizador`, `eje`, `curva`, `cuerpo`,
  `punteado`, `texto`. El widget es estático y no dibuja vectores, así que no usa
  `crearEscena`, `boton`, `casilla` ni `vectorPx`; y la velocidad instantánea en P no
  sale de `derivar` sino del número que imprime `verificacion-practico-1.py`, porque la
  restricción global es que el valor **sea** el del script y no una aproximación.
- Produce: el archivo del ensayo con `widgetSecante(pagina)`.

- [ ] **Paso 1: armar el esqueleto del ensayo**

Copiar de `docs/ensayos/tiro-parabolico.html` la estructura entera —el script de tema
del `<head>`, los `<link>` de fuentes, la barra de progreso, el encabezado con su kicker
y su botón de tema, y el pie— y cambiar sólo el contenido:

- kicker: `ENSAYO 1 · FÍSICA 1`
- `<h1>`: `Derivada e integral, vistas`
- bajada: `La velocidad es la pendiente y el desplazamiento es el área: la misma relación leída en dos direcciones.`
- pie: `Apunte cap. 1, pp. 3–24 · práctico 1, ej. 1 a 8`, con el enlace a
  `../../parcial-1/practicos/practico_1_2026.pdf`.

Los dos párrafos de entrada, antes de la sección 01:

> Un gráfico de posición contra tiempo parece decir una sola cosa: dónde está el móvil
> en cada instante. Dice dos más, y son las que los ejercicios piden: cuán rápido va, y
> cómo cambia esa rapidez. Las dos están ahí, en la forma de la curva, antes de que
> aparezca ninguna fórmula.

> Este ensayo tiene un solo objetivo: que puedas mirar una curva y leerle la velocidad
> sin calcular nada, y mirar una curva de velocidad y leerle el desplazamiento del
> mismo modo.

Y el encabezado de la sección 01, con los valores tipográficos del sistema:

- `<h2>`: `01 · La pendiente que se afila`
- párrafo: explica que la velocidad media entre dos instantes es la pendiente de la
  recta que une los dos puntos, y que la instantánea es a dónde va esa pendiente cuando
  los dos puntos se juntan. Cierra pidiendo: mové el slider hasta el fondo y mirá el número.

- [ ] **Paso 2: escribir el widget**

La curva es la del ejercicio 1: `x(t) = -3 + 2t³`, con `P` en `t = 0.8`, donde la
velocidad instantánea vale exactamente 3.84 m/s según
`parcial-1/soluciones/verificacion-practico-1.py`.

```js
function widgetSecante(pagina) {
  const x = t => -3 + 2 * t ** 3;
  const T_P = 0.8;
  let dt = 0.6;

  const canvas = document.getElementById('w1-cv');
  const widget = crearWidget({
    pagina, canvas,
    margen: { L: 62, R: 24, T: 38, B: 42 },
    encuadre: () => ({ xMin: -1, xMax: 1.6, yMin: -5.5, yMax: 6 }),
    dibujar: pintar,
  });

  function pintar(ctx, l) {
    const p = pagina.paleta();
    eje(ctx, l, { color: p.rule, colorTexto: p.dim, etiquetaX: 't [s]', etiquetaY: 'x [m]' });
    curva(ctx, l, t => [t, x(t)], l.xMin, l.xMax, { color: p.graph, grosor: 1.8 });

    const tQ = T_P + dt;
    const pendiente = (x(tQ) - x(T_P)) / dt;

    // La secante se dibuja larga a proposito, cruzando el encuadre: asi se ve como gira
    // alrededor de P en vez de parecer un segmento que se acorta.
    const recta = t => [t, x(T_P) + pendiente * (t - T_P)];
    curva(ctx, l, recta, l.xMin, l.xMax, { color: p.blue, grosor: 1.6 });

    // El triangulo de la pendiente: delta t abajo, delta x al costado.
    punteado(ctx, l.px(T_P), l.py(x(T_P)), l.px(tQ), l.py(x(T_P)), { color: p.blueSoft });
    punteado(ctx, l.px(tQ), l.py(x(T_P)), l.px(tQ), l.py(x(tQ)), { color: p.blueSoft });
    texto(ctx, 'Δt', (l.px(T_P) + l.px(tQ)) / 2, l.py(x(T_P)) + 15,
      { color: p.blue, alineacion: 'center' });
    texto(ctx, 'Δx', l.px(tQ) + 8, (l.py(x(T_P)) + l.py(x(tQ))) / 2,
      { color: p.blue });

    cuerpo(ctx, l, [T_P, x(T_P)], { radio: 5.5, color: p.ink });
    cuerpo(ctx, l, [tQ, x(tQ)], { radio: 5, color: p.blue });
    texto(ctx, 'P', l.px(T_P) - 14, l.py(x(T_P)) - 8, { color: p.ink });
    texto(ctx, 'Q', l.px(tQ) + 9, l.py(x(tQ)) - 9, { color: p.blue });

    leer('w1-dt', dt.toFixed(3) + ' s');
    leer('w1-pend', pendiente.toFixed(2) + ' m/s');
    leer('w1-lim', '3.84 m/s');
    leer('w1-error', Math.abs(pendiente - 3.84).toFixed(2) + ' m/s');
  }

  deslizador({
    entrada: document.getElementById('w1-dt'), salida: document.getElementById('w1-dt-out'),
    formato: v => v.toFixed(3) + ' s', pagina,
    alCambiar: v => { dt = v; widget.repintar(); },
  });
}
```

El slider `w1-dt` va de 0.001 a 0.8 con paso 0.001 y arranca en 0.6. Es deliberado que
arranque lejos: el widget tiene que abrir mostrando una secante que se ve claramente
distinta de la tangente, para que achicarla signifique algo.

- [ ] **Paso 3: escribir el encabezado del widget y su fila de lecturas**

Con la anatomía del sistema: `SIMULACIÓN 1`, el nombre `De la secante a la tangente`, y
la frase de qué mirar: `— achicá Δt y mirá el número de la pendiente, no la recta.`

Cuatro lecturas: `Δt`, `pendiente PQ`, `velocidad en P` (fija, `3.84 m/s`) y `diferencia`.
La cuarta es la que hace el punto: tiende a cero sin llegar nunca.

- [ ] **Paso 4: escribir el cierre de la sección**

Dos párrafos. El primero nombra lo que se vio: la pendiente de la secante se acerca a un
número y nunca lo toca, porque con `Δt = 0` la cuenta no existe; el límite es el nombre
de ese acercamiento. El segundo conecta con la notación del apunte, `v = dx/dt`, y avisa
que en el ejercicio 1 la consigna pide justamente leer velocidades instantáneas del
gráfico: en `t = 0` la curva está horizontal y la velocidad es 0; en `t = 0.8` vale 3.84 m/s.

- [ ] **Paso 5: verificar en el navegador**

Abrir la página con el servidor andando. Comprobar: el widget arranca quieto, con `Δt = 0.6`;
al llevar el slider al mínimo la `diferencia` baja por debajo de 0.01 m/s y la recta azul
queda apoyada sobre la curva; el triángulo punteado se achica con ella; y la lectura
`velocidad en P` no se mueve nunca.

- [ ] **Paso 6: correr la suite y commitear**

```bash
node --test "test/**/*.test.js"
git add docs/ensayos/derivada-integral.html
git commit -m "feat(plataforma): ensayo de derivada e integral, de la secante a la tangente"
```

---

### Tarea 12: El widget "Los tres paneles sincronizados"

Es el widget que enseña a leer los tres gráficos como un solo movimiento, que es lo que
piden los incisos "grafique x(t), v(t) y a(t)" de los ejercicios 4, 5 y 7.

**Archivos:**
- Modificar: `docs/ensayos/derivada-integral.html`

**Interfaces:**
- Consume: lo de la Tarea 11 más `derivar`.
- Produce: `widgetPaneles(pagina)`.

- [ ] **Paso 1: escribir la sección 02**

`<h2>`: `02 · Tres gráficos, un solo movimiento`. El párrafo explica que los tres
gráficos comparten el eje temporal, así que cada instante es una columna vertical que
los atraviesa, y que leerlos juntos convierte tres dibujos en una sola historia.

- [ ] **Paso 2: escribir el widget**

El movimiento es el del ejercicio 4: `x(t) = 3 + 17t - 5t²`, `v(t) = 17 - 10t`, `a = -10`.
Los tres paneles van en **un solo canvas**, apilados, con el mismo mapeo horizontal y
tres verticales distintos. Eso se resuelve con tres lienzos que comparten `xMin`/`xMax`
y se diferencian en el margen superior e inferior:

```js
function widgetPaneles(pagina) {
  const x = t => 3 + 17 * t - 5 * t ** 2;
  const v = t => derivar(x, t);
  const a = t => derivar(v, t, 1e-3);
  const T0 = 0, T1 = 3.4;                 // en t = 3.4 el movil vuelve a x(0)
  let cursor = 1.7;                       // el maximo de x, que es el cero de v

  const canvas = document.getElementById('w2-cv');

  // Tres paneles dentro del mismo canvas: la clave es que los tres usen el mismo
  // mapeo horizontal, porque el argumento del widget es que la columna vertical
  // significa lo mismo en los tres.
  const PANELES = [
    { f: x, etiqueta: 'x [m]', yMin: 0, yMax: 19, color: () => pagina.paleta().ink },
    { f: v, etiqueta: 'v [m/s]', yMin: -19, yMax: 19, color: () => pagina.paleta().blue },
    { f: a, etiqueta: 'a [m/s²]', yMin: -19, yMax: 19, color: () => pagina.paleta().red },
  ];

  // Tres paneles apilados dentro de un canvas. El encuadre de afuera mide tres
  // unidades de alto, una por panel, y cada panel arma despues su propio lienzo con
  // su rango real. `escalaUniforme: false` porque el eje horizontal es tiempo y el
  // vertical metros: una sola escala para los dos no significaria nada y dejaria el
  // grafico en la mitad del ancho. `altoMin` sube el piso del canvas para que cada
  // panel tenga 95 px: con el piso generico de 215 quedarian 54, que se van casi
  // enteros en el rotulo y la fila de numeros.
  const MARGEN = { L: 62, R: 24, T: 20, B: 34 };
  const ALTO_PANEL_MINIMO = 95;
  const widget = crearWidget({
    pagina, canvas,
    margen: MARGEN,
    escalaUniforme: false,
    altoMin: 3 * ALTO_PANEL_MINIMO + MARGEN.T + MARGEN.B,
    encuadre: () => ({ xMin: T0, xMax: T1, yMin: 0, yMax: 3 }),
    dibujar: pintar,
  });

  // Los lienzos de los paneles se arman aca, no adentro del bucle de dibujo, porque el
  // cursor tiene que usar EXACTAMENTE el mismo mapeo horizontal que ellos. El lienzo
  // que devuelve crearWidget no sirve para eso: cuando el alto choca contra el tope de
  // 430 px, su xMax deja de ser T1 y el cursor quedaria corrido respecto de las curvas.
  const lienzosPanel = l => {
    const alturaPanel = (l.py(0) - l.py(3)) / 3;
    const arriba = l.py(3);
    return PANELES.map((panel, i) => {
      const tope = arriba + i * alturaPanel;
      return {
        panel,
        arriba,
        alturaPanel,
        lp: crearLienzo({
          ancho: l.ancho, alto: l.alto,
          margen: { L: MARGEN.L, R: MARGEN.R, T: tope, B: l.alto - tope - alturaPanel + 10 },
          xMin: T0, xMax: T1, yMin: panel.yMin, yMax: panel.yMax,
        }),
      };
    });
  };

  function pintar(ctx, l) {
    const p = pagina.paleta();
    const capas = lienzosPanel(l);

    for (const { panel, lp } of capas) {
      eje(ctx, lp, { color: p.rule, colorTexto: p.dim, etiquetaY: panel.etiqueta });
      curva(ctx, lp, t => [t, panel.f(t)], T0, T1, { color: panel.color(), grosor: 1.8 });
      cuerpo(ctx, lp, [cursor, panel.f(cursor)], { radio: 4.5, color: panel.color() });
    }

    // El cursor compartido: una sola linea vertical que cruza los tres paneles. Es
    // literalmente el argumento del widget dibujado, y por eso su x sale del lienzo de
    // un panel y no del lienzo del widget.
    const { lp: primero, arriba, alturaPanel } = capas[0];
    punteado(ctx, primero.px(cursor), arriba, primero.px(cursor), arriba + 3 * alturaPanel,
      { color: p.blueSoft, guiones: [3, 4] });

    leer('w2-t', cursor.toFixed(2) + ' s');
    leer('w2-x', x(cursor).toFixed(2) + ' m');
    leer('w2-v', v(cursor).toFixed(2) + ' m/s');
    leer('w2-a', a(cursor).toFixed(1) + ' m/s²');
  }
```

- [ ] **Paso 3: cablear el arrastre horizontal y los dos presets**

El cursor se arrastra en horizontal; la componente vertical se descarta. El lienzo que
se le pasa es **el del primer panel**, por la misma razón que arriba: es el que tiene el
mapeo horizontal bueno, así que su `ux` convierte el píxel del puntero al segundo
correcto.

```js
  arrastrable({
    canvas, pagina,
    lienzo: () => { const l = widget.lienzo(); return l && lienzosPanel(l)[0].lp; },
    acotar: (t, y) => [Math.min(T1, Math.max(T0, t)), y],
    alArrastrar: t => { cursor = t; widget.repintar(); },
  });
  boton({
    elemento: document.getElementById('w2-pmax'), pagina,
    alApretar: () => { cursor = 1.7; widget.repintar(); },
  });
  boton({
    elemento: document.getElementById('w2-p0'), pagina,
    alApretar: () => { cursor = 0; widget.repintar(); },
  });
```

Los dos presets son el corazón pedagógico: `w2-pmax` dice `Máximo de x` y lleva el cursor
a `t = 1.7`, donde `x` vale 17.45 y `v` vale exactamente 0. `w2-p0` dice `Arranque` y
vuelve a `t = 0`, donde `v` vale 17 m/s.

Encabezado del widget: `SIMULACIÓN 2`, nombre `Los tres paneles`, y la frase de qué mirar:
`— arrastrá el cursor hasta la cima de x y mirá dónde queda el punto azul.`

- [ ] **Paso 4: escribir el cierre de la sección**

Dos párrafos que digan las dos lecturas que el widget hace visibles, con sus números
respaldados: donde `x` tiene su máximo (`t = 1.7 s`, `x = 17.45 m`) la velocidad vale
cero, porque la curva ahí está horizontal; y la aceleración es constante y negativa
(`−10 m/s²`) todo el tiempo, lo que se ve en que `v` es una recta que baja y en que `x`
es una parábola con la concavidad siempre para abajo. Cerrar advirtiendo lo que el
ejercicio 4 cobra: que velocidad cero no es lo mismo que aceleración cero.

- [ ] **Paso 5: verificar en el navegador**

Comprobar que el cursor arrastra y los tres puntos se mueven juntos; que en `t = 1.7` la
lectura de `v` marca `0.00 m/s`; que la lectura de `a` marca `-10.0 m/s²` en todo el
recorrido; y que los tres paneles comparten exactamente la misma coordenada horizontal
—soltar el cursor sobre una marca del eje y ver que cae en la misma marca en los tres—.

- [ ] **Paso 6: correr la suite y commitear**

```bash
node --test "test/**/*.test.js"
git add docs/ensayos/derivada-integral.html
git commit -m "feat(plataforma): los tres paneles sincronizados"
```

---

### Tarea 13: El widget "Dibujá tu x(t)"

El brief lo llama el que más enseña y el más difícil de implementar bien. La dificultad
es concreta: una curva trazada a mano tiene ruido de un píxel por muestra, y derivar dos
veces ese ruido da una aceleración ilegible.

**Archivos:**
- Modificar: `docs/ensayos/derivada-integral.html`

**Interfaces:**
- Consume: lo anterior más `derivarMuestras`, `suavizar`, `traza`.
- Produce: `widgetDibujar(pagina)`.

- [ ] **Paso 1: escribir la sección 03**

`<h2>`: `03 · Dibujá vos`. El párrafo invita: trazá con el mouse cualquier historia de
posición —arrancá quieto y acelerá, andá y frená, volvé— y mirá qué les pasa a los dos
gráficos de abajo. Aclarar que no hay respuesta correcta, que es el punto.

- [ ] **Paso 2: escribir el widget**

```js
function widgetDibujar(pagina) {
  const T0 = 0, T1 = 6, N = 120;
  // El estado es una grilla fija de N + 1 alturas: el lector pinta alturas, no puntos
  // sueltos, y asi la funcion nunca deja de ser una funcion aunque el mouse vuelva atras.
  let alturas = new Array(N + 1).fill(5);
  let hayTrazo = false;

  const tDe = i => T0 + ((T1 - T0) * i) / N;
  const muestras = () => alturas.map((y, i) => [tDe(i), y]);

  const canvas = document.getElementById('w3-cv');
  // Mismo esquema de tres paneles que el widget de la seccion 02, y por las mismas
  // razones. Copiale las tres constantes tal como quedaron ahi, incluido el hueco
  // derivado: el rotulo del eje vertical cuelga COLGADO_ROTULO_EJE por encima del
  // techo de su panel, y un glifo de 10 px sube unos 8 px mas sobre su linea de base.
  const MARGEN = { L: 62, R: 24, T: 20, B: 34 };
  const HUECO_ROTULO = COLGADO_ROTULO_EJE + 8;
  const ALTO_PANEL_MINIMO = 95 + HUECO_ROTULO;
  const widget = crearWidget({
    pagina, canvas,
    margen: MARGEN,
    escalaUniforme: false,
    altoMin: 3 * ALTO_PANEL_MINIMO + MARGEN.T + MARGEN.B,
    encuadre: () => ({ xMin: T0, xMax: T1, yMin: 0, yMax: 3 }),
    dibujar: pintar,
  });

  const RANGOS = [
    { etiqueta: 'x [m]', yMin: 0, yMax: 10 },
    { etiqueta: 'v [m/s]', yMin: -12, yMax: 12 },
    { etiqueta: 'a [m/s²]', yMin: -30, yMax: 30 },
  ];

  // Igual que en el widget de los tres paneles: los lienzos se arman aparte porque el
  // trazado a mano tiene que escribir en el mismo sistema en que se dibuja el panel de
  // arriba, y el lienzo del widget no lo garantiza.
  const lienzosPanel = l => {
    const alturaPanel = (l.py(0) - l.py(3)) / 3;
    const arriba = l.py(3);
    return RANGOS.map((r, i) => {
      const tope = arriba + i * alturaPanel;
      return {
        rango: r,
        arriba,
        alturaPanel,
        lp: crearLienzo({
          ancho: l.ancho, alto: l.alto,
          margen: {
            L: MARGEN.L, R: MARGEN.R,
            T: tope + HUECO_ROTULO, B: l.alto - tope - alturaPanel + 10,
          },
          xMin: T0, xMax: T1, yMin: r.yMin, yMax: r.yMax,
        }),
      };
    });
  };

  function pintar(ctx, l) {
    const p = pagina.paleta();
    const suaves = suavizar(muestras(), 7);
    const vel = derivarMuestras(suaves);
    const acel = derivarMuestras(suavizar(vel, 7));
    const series = [
      { pts: suaves, color: p.ink },
      { pts: vel, color: p.blue },
      { pts: acel, color: p.red },
    ];

    const capas = lienzosPanel(l);
    capas.forEach(({ rango, lp }, i) => {
      // El eje de tiempo se rotula una sola vez, en el panel de abajo: los tres lo
      // comparten, y repetirlo tres veces lo deja flotando en mitad de los graficos.
      const esElDeAbajo = i === capas.length - 1;
      eje(ctx, lp, {
        color: p.rule, colorTexto: p.dim, etiquetaY: rango.etiqueta,
        marcasX: esElDeAbajo,
        ...(esElDeAbajo ? { etiquetaX: 't [s]' } : {}),
      });
      traza(ctx, lp, series[i].pts, { color: series[i].color, grosor: 1.8 });
    });

    if (!hayTrazo) {
      const { lp, arriba, alturaPanel } = capas[0];
      texto(ctx, 'dibujá acá arriba con el mouse', lp.px((T0 + T1) / 2), arriba + alturaPanel / 2,
        { color: p.dim, px: 12, peso: 400, alineacion: 'center' });
    }
  }
```

Las dos decisiones que hacen que esto funcione están en el código y conviene entenderlas
antes de tocarlo. La primera: el estado no es la lista de puntos por los que pasó el
mouse sino un **arreglo de alturas indexado por tiempo**, así que volver con el mouse
hacia atrás reescribe alturas ya pintadas en vez de crear una curva que se muerde la
cola. La segunda: se suaviza **dos veces**, una antes de la primera derivada y otra antes
de la segunda, porque cada derivada amplifica el ruido y sin el segundo suavizado el
panel de aceleración es una pared de picos.

- [ ] **Paso 3: cablear el trazado**

El arrastre escribe en la grilla, y rellena los índices que el puntero se salteó cuando
el mouse va rápido:

```js
  let ultimoIndice = null;
  const escribir = (t, y) => {
    const i = Math.round(((t - T0) / (T1 - T0)) * N);
    if (i < 0 || i > N) return;
    const alt = Math.min(10, Math.max(0, y));
    if (ultimoIndice === null || Math.abs(i - ultimoIndice) <= 1) {
      alturas[i] = alt;
    } else {
      // Interpolar los indices salteados: sin esto, mover rapido deja huecos con el
      // valor viejo y la derivada dispara.
      const paso = i > ultimoIndice ? 1 : -1;
      const desde = alturas[ultimoIndice];
      const n = Math.abs(i - ultimoIndice);
      for (let k = 1; k <= n; k++) {
        alturas[ultimoIndice + k * paso] = desde + ((alt - desde) * k) / n;
      }
    }
    ultimoIndice = i;
    hayTrazo = true;
    widget.repintar();
  };
```

El arrastre trabaja sobre el lienzo del **panel de arriba**, no sobre el del widget: lo
que el lector dibuja son metros de posición, no las tres unidades del encuadre.

```js
  const arrastre = arrastrable({
    canvas, pagina,
    lienzo: () => { const l = widget.lienzo(); return l && lienzosPanel(l)[0].lp; },
    alArrastrar: escribir,
  });
  canvas.addEventListener('pointerup', () => { ultimoIndice = null; });
  canvas.addEventListener('pointercancel', () => { ultimoIndice = null; });
```

`ultimoIndice` tiene que volver a `null` al soltar: si no, el trazo siguiente interpola
desde donde terminó el anterior y aparece una rampa que el lector nunca dibujó.

Tres botones, con presets que el ejercicio 2 pide reconocer:
`w3-limpiar` deja la recta horizontal en 5 m; `w3-p-quieto` carga un tramo quieto seguido
de uno que acelera; `w3-p-frena` carga la parábola que sube y vuelve. Cada preset escribe
`alturas` entero y repinta.

Encabezado: `SIMULACIÓN 3`, nombre `Dibujá tu x(t)`, y la frase de qué mirar:
`— dibujá un tramo horizontal y mirá el panel del medio.`

- [ ] **Paso 4: escribir el cierre de la sección**

Un párrafo que nombre las tres cosas que el lector acaba de descubrir dibujando: un tramo
horizontal en `x` da velocidad cero; un tramo recto e inclinado da velocidad constante y
aceleración cero; y sólo cuando la curva se dobla aparece aceleración. Cerrar diciendo
que ésa es la lectura que el ejercicio 2 pide, con su `x(t)` a trozos.

- [ ] **Paso 5: verificar en el navegador**

Dibujar un tramo horizontal y confirmar que el panel de velocidad se va a cero y se queda
ahí; dibujar una rampa recta y confirmar que la velocidad es una horizontal y la
aceleración se queda cerca de cero; mover el mouse rápido de un lado al otro y confirmar
que no quedan escalones ni picos que se salgan del panel.

- [ ] **Paso 6: correr la suite y commitear**

```bash
node --test "test/**/*.test.js"
git add docs/ensayos/derivada-integral.html
git commit -m "feat(plataforma): dibuja tu x(t)"
```

---

### Tarea 14: El widget "El área es el desplazamiento" y el cierre del ensayo

**Archivos:**
- Modificar: `docs/ensayos/derivada-integral.html`

**Interfaces:**
- Consume: lo anterior más `integrar`.
- Produce: `widgetArea(pagina)`, y el ensayo queda completo.

- [ ] **Paso 1: escribir la sección 04**

`<h2>`: `04 · El área también cuenta`. El párrafo da vuelta la relación: si la velocidad
es la pendiente de la posición, entonces la posición tiene que poder leerse de la
velocidad, y lo que se lee es el área. Avisa que el signo importa y que ahí se separan
dos cosas que suenan iguales, desplazamiento y camino recorrido.

- [ ] **Paso 2: escribir el widget**

La `v(t)` es la del ejercicio 4, que cruza el cero en `t = 1.7` y por eso sirve para el
punto del signo:

```js
function widgetArea(pagina) {
  const v = t => 17 - 10 * t;
  const T0 = 0, T1 = 3.4;
  let hasta = 1.7;

  const canvas = document.getElementById('w4-cv');
  const widget = crearWidget({
    pagina, canvas,
    margen: { L: 62, R: 24, T: 38, B: 42 },
    // El eje horizontal es tiempo y el vertical velocidad: escala independiente por
    // eje. Con una sola escala este grafico ocuparia el 4 % del ancho.
    escalaUniforme: false,
    encuadre: () => ({ xMin: T0, xMax: T1, yMin: -19, yMax: 19 }),
    dibujar: pintar,
  });

  function pintar(ctx, l) {
    const p = pagina.paleta();

    // El area se pinta en dos tramos porque el signo cambia en t = 1.7, y ese cambio
    // de color es todo el argumento: lo que esta abajo del eje resta.
    const cortes = hasta <= 1.7 ? [[T0, hasta, p.blue]] : [[T0, 1.7, p.blue], [1.7, hasta, p.red]];
    for (const [a, b, color] of cortes) {
      if (b - a < 1e-9) continue;
      ctx.fillStyle = color;
      ctx.globalAlpha = 0.16;
      ctx.beginPath();
      ctx.moveTo(l.px(a), l.py(0));
      for (let i = 0; i <= 60; i++) {
        const t = a + ((b - a) * i) / 60;
        ctx.lineTo(l.px(t), l.py(v(t)));
      }
      ctx.lineTo(l.px(b), l.py(0));
      ctx.closePath();
      ctx.fill();
      ctx.globalAlpha = 1;
    }

    eje(ctx, l, { color: p.rule, colorTexto: p.dim, etiquetaX: 't [s]', etiquetaY: 'v [m/s]' });
    curva(ctx, l, t => [t, v(t)], T0, T1, { color: p.blue, grosor: 1.9 });
    punteado(ctx, l.px(hasta), l.py(l.yMin), l.px(hasta), l.py(l.yMax), { color: p.blueSoft });
    cuerpo(ctx, l, [hasta, v(hasta)], { radio: 5, color: p.ink });

    const desplazamiento = integrar(v, T0, hasta);
    const camino = hasta <= 1.7
      ? desplazamiento
      : integrar(v, T0, 1.7) - integrar(v, 1.7, hasta);

    leer('w4-t', hasta.toFixed(2) + ' s');
    leer('w4-desp', desplazamiento.toFixed(2) + ' m');
    leer('w4-cam', camino.toFixed(2) + ' m');
    leer('w4-v', v(hasta).toFixed(2) + ' m/s');
  }
```

El slider `w4-t` va de 0 a 3.4 con paso 0.01 y arranca en 1.7, que es justo donde la
velocidad se anula: el widget abre en el instante más informativo.

Encabezado: `SIMULACIÓN 4`, nombre `El área es el desplazamiento`, y la frase de qué
mirar: `— llevá el slider hasta el final y compará las dos lecturas de abajo.`

- [ ] **Paso 3: escribir el cierre de la sección y del ensayo**

El párrafo de cierre de la sección dice lo que el widget acaba de mostrar, con los
números que salen de `parcial-1/soluciones/verificacion-practico-1.py`: llevando el
slider hasta `t = 3.4 s` el desplazamiento vuelve a `0.00 m` mientras el camino recorrido
llega a `28.9 m`, porque el móvil subió 14.45 m y volvió a bajar los mismos 14.45 m. Son
dos preguntas distintas y el gráfico las contesta distinto: una suma áreas con su signo,
la otra las suma en valor absoluto.

Después, el cierre del ensayo con el `<h2>` `Para resolver 1 a 8` y una lista ordenada:

1. Mirá primero la forma, no la fórmula: dónde sube, dónde baja, dónde está horizontal.
2. Un máximo o un mínimo de `x` es un cero de `v`. Un tramo recto de `x` es una `v` constante.
3. La concavidad de `x` es el signo de `a`. Para abajo, `a` negativa.
4. Si te dan `v` y piden posición, estás midiendo un área, y el signo cuenta.
5. Desplazamiento y camino recorrido sólo coinciden si el móvil no se dio vuelta.

Y el pie con las fuentes, igual que en el ensayo de tiro.

- [ ] **Paso 4: recorrer el ensayo entero**

Las cuatro simulaciones juntas: ninguna se anima sola, el tema las repinta a las cuatro,
y a 400 px de ancho los tres paneles apilados siguen siendo legibles.

- [ ] **Paso 5: correr la suite y commitear**

```bash
node --test "test/**/*.test.js"
git add docs/ensayos/derivada-integral.html
git commit -m "feat(plataforma): el area es el desplazamiento, y el cierre del ensayo 1"
```

---

## Fase D — el ensayo de movimiento circular

Cubre los ejercicios 11 a 14. La idea central: la aceleración tiene dos trabajos
distintos, y sólo uno de ellos cambia la rapidez.

Como el ensayo 1, **no tiene archivo de diseño propio** y aplica el sistema cerrado.

### Tarea 15: Física del movimiento circular

**Archivos:**
- Crear: `docs/fisica/circular.js`
- Prueba: `test/circular.test.js`

**Interfaces:**
- Consume: nada.
- Produce: `crearCircular({ R, omega0, gamma = 0, theta0 = 0, centro = [0, 0] })` que devuelve
  `{ theta(t), omega(t), pos(t), vel(t), rapidez(t), aT(t), aN(t), aTotal(t), versorR(t), versorTheta(t), periodo, frecuencia, vueltasEn(t) }`.
  `pos`, `vel`, `versorR` y `versorTheta` devuelven pares `[x, y]`. `periodo` y
  `frecuencia` valen `null` si `gamma` no es cero, porque entonces el movimiento no es
  periódico.

- [ ] **Paso 1: escribir las pruebas que fallan**

Crear `test/circular.test.js`. Todos los valores salen de
`parcial-1/soluciones/verificacion-practico-1.py`, ejercicios 12, 13 y 14:

```js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { crearCircular } from '../docs/fisica/circular.js';

const cerca = (a, b, tol = 1e-6) =>
  assert.ok(Math.abs(a - b) < tol, `${a} != ${b} (tol ${tol})`);

// Ejercicio 13: theta(t) = 2 t^2 sobre R = 1.5, o sea omega0 = 0 y gamma = 4.
const ej13 = () => crearCircular({ R: 1.5, omega0: 0, gamma: 4 });

test('ejercicio 13: omega(t) = 4 t y la aceleracion angular es constante', () => {
  const c = ej13();
  cerca(c.omega(0), 0);
  cerca(c.omega(1), 4);
  cerca(c.omega(5), 20);
});

test('ejercicio 13: theta(t) = 2 t^2', () => {
  const c = ej13();
  cerca(c.theta(3), 18);
});

test('ejercicio 13: la aceleracion tangencial vale 6 y no depende del tiempo', () => {
  const c = ej13();
  for (const t of [0, 1, 5, 20]) cerca(c.aT(t), 6);
});

test('ejercicio 13: la normal es 24 t^2, o sea 600 en t = 5', () => {
  const c = ej13();
  cerca(c.aN(5), 600);
  cerca(c.aN(1), 24);
});

test('ejercicio 13: el modulo de la aceleracion total en t = 5 es 600.030', () => {
  cerca(ej13().aTotal(5), 600.030, 1e-3);
});

test('ejercicio 13: da 127.32 vueltas en 20 segundos', () => {
  cerca(ej13().vueltasEn(20), 127.32, 1e-2);
});

test('ejercicio 13: sin velocidad angular constante no hay periodo', () => {
  assert.equal(ej13().periodo, null);
  assert.equal(ej13().frecuencia, null);
});

// Ejercicio 14: x = sen(wt), y = cos(wt) + 1, con w = 2 pi. Es un circulo de radio 1
// centrado en (0, 1), recorrido en sentido horario desde el punto mas alto.
const ej14 = () => crearCircular({ R: 1, omega0: 2 * Math.PI, centro: [0, 1] });

test('ejercicio 14: la rapidez es 2 pi y no cambia', () => {
  const c = ej14();
  for (const t of [0, 0.13, 0.5, 0.9]) cerca(c.rapidez(t), 2 * Math.PI);
});

test('ejercicio 14: el modulo de la aceleracion es 4 pi^2', () => {
  cerca(ej14().aTotal(0.3), 4 * Math.PI ** 2, 1e-9);
});

test('ejercicio 14: el periodo es 1 s y la frecuencia 1 Hz', () => {
  const c = ej14();
  cerca(c.periodo, 1);
  cerca(c.frecuencia, 1);
});

test('ejercicio 14: sin aceleracion angular la tangencial es cero', () => {
  cerca(ej14().aT(0.42), 0);
});

test('ejercicio 14: la trayectoria vive en el circulo de radio 1 centrado en (0, 1)', () => {
  const c = ej14();
  for (const t of [0, 0.2, 0.55, 0.99]) {
    const [x, y] = c.pos(t);
    cerca(Math.hypot(x - 0, y - 1), 1, 1e-9);
  }
});

test('inciso (d) del ejercicio 11: la posicion y la velocidad son siempre perpendiculares', () => {
  const c = ej13();                        // vale incluso con gamma distinto de cero
  for (const t of [0.3, 1, 4.2]) {
    const [rx, ry] = c.versorR(t);
    const [vx, vy] = c.vel(t);
    cerca(rx * vx + ry * vy, 0, 1e-9);
  }
});

test('inciso (e) del ejercicio 11: velocidad y aceleracion son perpendiculares solo en el uniforme', () => {
  const uniforme = ej14();
  const [vx, vy] = uniforme.vel(0.3);
  const [ax, ay] = uniforme.aTotalVector ? uniforme.aTotalVector(0.3) : [0, 0];
  cerca(vx * ax + vy * ay, 0, 1e-6);
  // Con gamma distinto de cero deja de valer: hay componente a lo largo de v.
  assert.ok(Math.abs(ej13().aT(2)) > 1e-9);
});

test('los dos versores son unitarios y perpendiculares entre si', () => {
  const c = ej13();
  const [rx, ry] = c.versorR(1.3);
  const [tx, ty] = c.versorTheta(1.3);
  cerca(Math.hypot(rx, ry), 1);
  cerca(Math.hypot(tx, ty), 1);
  cerca(rx * tx + ry * ty, 0, 1e-12);
});

// Ejercicio 12: la Tierra, 30 km/s sobre un radio de 150e6 km.
test('ejercicio 12: la aceleracion centripeta de la Tierra es 6.0e-3 m/s^2', () => {
  const R = 150e9, v = 30e3;
  const c = crearCircular({ R, omega0: v / R });
  cerca(c.aN(0), 6.0e-3, 1e-5);
});
```

La prueba del inciso (e) usa `aTotalVector`, así que el módulo lo expone además de
`aTotal`: devuelve el par `[ax, ay]`.

- [ ] **Paso 2: correrlas y verificar que fallan**

Ejecutar: `node --test test/circular.test.js`
Esperado: FALLAN todas, el módulo no existe.

- [ ] **Paso 3: implementar**

```js
// Movimiento circular, uniforme y uniformemente acelerado. El angulo crece en sentido
// antihorario desde theta0; para recorrer el circulo al reves basta con omega0 negativa.

export function crearCircular({ R, omega0, gamma = 0, theta0 = 0, centro = [0, 0] }) {
  const [cx, cy] = centro;

  const theta = t => theta0 + omega0 * t + 0.5 * gamma * t * t;
  const omega = t => omega0 + gamma * t;

  const versorR = t => [Math.cos(theta(t)), Math.sin(theta(t))];
  const versorTheta = t => [-Math.sin(theta(t)), Math.cos(theta(t))];

  const pos = t => {
    const [ux, uy] = versorR(t);
    return [cx + R * ux, cy + R * uy];
  };
  const vel = t => {
    const [ux, uy] = versorTheta(t);
    const v = omega(t) * R;
    return [v * ux, v * uy];
  };
  const rapidez = t => Math.abs(omega(t)) * R;

  // La tangencial cambia la rapidez; la normal cambia la direccion. Es toda la idea
  // del ensayo, y aca son dos lineas distintas a proposito.
  const aT = () => gamma * R;
  const aN = t => omega(t) ** 2 * R;
  const aTotal = t => Math.hypot(aT(t), aN(t));
  const aTotalVector = t => {
    const [rx, ry] = versorR(t);
    const [tx, ty] = versorTheta(t);
    return [aT(t) * tx - aN(t) * rx, aT(t) * ty - aN(t) * ry];
  };

  const uniforme = gamma === 0 && omega0 !== 0;
  const periodo = uniforme ? (2 * Math.PI) / Math.abs(omega0) : null;

  return {
    R, centro, theta, omega, pos, vel, rapidez,
    versorR, versorTheta, aT, aN, aTotal, aTotalVector,
    periodo,
    frecuencia: periodo === null ? null : 1 / periodo,
    vueltasEn: t => Math.abs(theta(t) - theta0) / (2 * Math.PI),
  };
}
```

- [ ] **Paso 4: correr toda la suite y commitear**

```bash
node --test "test/**/*.test.js"
git add docs/fisica/circular.js test/circular.test.js
git commit -m "feat(plataforma): movimiento circular, contrastado con el practico 1"
```

---

### Tarea 16: El ensayo, "Los versores que giran" y "Período y frecuencia"

Dos widgets en una tarea porque son los dos más simples del ensayo y comparten casi todo
el andamiaje.

**Archivos:**
- Crear: `docs/ensayos/movimiento-circular.html`

**Interfaces:**
- Consume: `crearPagina`, `crearWidget`, `crearEscena`, `crearCircular`, `eje`, `curva`,
  `cuerpo`, `punteado`, `texto`, `vectorPx`, `deslizador`, `boton`, `rotuloReproducir`.
- Produce: el ensayo con `widgetVersores(pagina)` y `widgetPeriodo(pagina)`.

- [ ] **Paso 1: armar el esqueleto**

Igual que en la Tarea 11, copiando la estructura del ensayo de tiro:

- kicker: `ENSAYO 3 · FÍSICA 1`
- `<h1>`: `Movimiento circular`
- bajada: `La aceleración tiene dos trabajos distintos, y sólo uno de ellos cambia la rapidez.`
- pie: `Apunte cap. 2, pp. 25–47 · hoja resumen · práctico 1, ej. 11 a 14`, con enlaces a
  `../../parcial-1/preparacion/resumen-movimiento-circular.pdf` y
  `../../parcial-1/practicos/practico_1_2026.pdf`.

Los párrafos de entrada plantean la trampa del tema: un movimiento circular uniforme
tiene rapidez constante y sin embargo está acelerado todo el tiempo, y eso suena a
contradicción hasta que se separa "cuánto" de "hacia dónde".

- [ ] **Paso 2: escribir la sección 01 y el widget de los versores**

`<h2>`: `01 · Dos direcciones que giran con vos`. El párrafo presenta `r̂` y `θ̂` como un
par de ejes que viajan con la partícula en vez de quedarse quietos, y anticipa lo que el
widget hace ver: la velocidad siempre cae sobre `θ̂`, nunca sobre `r̂`.

```js
function widgetVersores(pagina) {
  const R = 1.5;
  let omega = 2;
  const movil = () => crearCircular({ R, omega0: omega });

  const canvas = document.getElementById('w1-cv');
  const widget = crearWidget({
    pagina, canvas,
    margen: { L: 40, R: 40, T: 30, B: 30 },
    // Encuadre cuadrado en un canvas apaisado: la escala tiene que ser uniforme para
    // que la circunferencia se vea redonda, y eso deja aire a los costados. `centrar`
    // lo reparte en vez de apoyar el dibujo contra el margen izquierdo.
    centrar: true,
    encuadre: () => ({ xMin: -2.2, xMax: 2.2, yMin: -2.2, yMax: 2.2 }),
    dibujar: (ctx, l) => pintar(ctx, l, escena.t),
  });

  const escena = crearEscena({
    dibujar: () => widget.repintar(),
    duracion: movil().periodo,
    velocidad: 0.75,
    alCambiar: () => rotuloReproducir(document.getElementById('w1-play'), escena, enReposo),
  });

  function pintar(ctx, l, t) {
    const p = pagina.paleta();
    const c = movil();
    const [x, y] = c.pos(t);
    const [px, py] = l.p([x, y]);
    const [ox, oy] = l.p([0, 0]);

    eje(ctx, l, { color: p.rule });
    curva(ctx, l, s => c.pos(s), 0, c.periodo, { color: p.graph, guiones: [3, 5], grosor: 1.2 });
    punteado(ctx, ox, oy, px, py, { color: p.rule });

    // Los dos versores se dibujan con un largo fijo en pixeles, porque son unitarios:
    // si se escalaran con el radio dejarian de significar "una unidad en esta direccion".
    const LARGO = 46;
    const [rx, ry] = c.versorR(t);
    const [tx, ty] = c.versorTheta(t);
    vectorPx(ctx, px, py, px + rx * LARGO, py - ry * LARGO,
      { color: p.dim, grosor: 1.6, punta: 8, rotulo: 'r̂' });
    vectorPx(ctx, px, py, px + tx * LARGO, py - ty * LARGO,
      { color: p.dim, grosor: 1.6, punta: 8, rotulo: 'θ̂' });

    const [vx, vy] = c.vel(t);
    const k = 26;
    vectorPx(ctx, px, py, px + vx * k, py - vy * k,
      { color: p.blue, grosor: 2.2, punta: 10, rotulo: 'v' });

    cuerpo(ctx, l, [x, y], { radio: 5.5, color: p.ink });
    cuerpo(ctx, l, [0, 0], { radio: 3, color: p.dim });

    leer('w1-t', t.toFixed(2) + ' s');
    leer('w1-ang', ((c.theta(t) * 180 / Math.PI) % 360).toFixed(0) + '°');
    leer('w1-rap', c.rapidez(t).toFixed(2) + ' m/s');
    leer('w1-prod', '0.00');        // r . v, que es cero siempre: es el punto del widget
  }
```

La cuarta lectura dice `r̂ · v` y marca `0.00` en todo momento. No es un adorno: es el
inciso (d) del ejercicio 11 convertido en algo que se mira.

Encabezado: `SIMULACIÓN 1`, nombre `Los versores que giran`, frase de qué mirar:
`— la flecha azul nunca se apoya sobre la punteada gris.`

Controles: botones reproducir y reiniciar, y un slider `w1-omega` de 0.5 a 6 rad/s
paso 0.1 valor 2, que al cambiar actualiza `escena.duracion = movil().periodo`.

- [ ] **Paso 3: escribir la sección 04 y el widget de período y frecuencia**

Va al final del ensayo, después de los otros dos widgets, pero se implementa acá porque
comparte todo con el primero.

`<h2>`: `04 · Qué miden el período y la frecuencia`. El párrafo define las dos como dos
formas de decir lo mismo —cuánto tarda una vuelta, cuántas vueltas por segundo— y avisa
que el inciso (c) del ejercicio 11 las pide por nombre.

```js
function widgetPeriodo(pagina) {
  const R = 1.2;
  let omegaA = 2 * Math.PI, omegaB = 4 * Math.PI;   // 1 Hz y 2 Hz
  const movilA = () => crearCircular({ R, omega0: omegaA, centro: [-1.6, 0] });
  const movilB = () => crearCircular({ R, omega0: omegaB, centro: [1.6, 0] });

  const canvas = document.getElementById('w4-cv');
  const widget = crearWidget({
    pagina, canvas,
    margen: { L: 30, R: 30, T: 24, B: 64 },
    centrar: true,   // dos circunferencias lado a lado: mismo motivo que el widget 1
    encuadre: () => ({ xMin: -3.2, xMax: 3.2, yMin: -1.6, yMax: 1.6 }),
    dibujar: (ctx, l) => pintar(ctx, l, escena.t),
  });

  const escena = crearEscena({
    dibujar: () => widget.repintar(),
    duracion: 2,                 // dos segundos: una vuelta de A y dos de B
    velocidad: 0.5,
    alCambiar: () => rotuloReproducir(document.getElementById('w4-play'), escena, enReposo),
  });

  function pintar(ctx, l, t) {
    const p = pagina.paleta();
    for (const [c, color] of [[movilA(), p.blue], [movilB(), p.red]]) {
      curva(ctx, l, s => c.pos(s), 0, c.periodo, { color: p.rule, grosor: 1.4 });
      cuerpo(ctx, l, c.pos(t), { radio: 6, color });
      cuerpo(ctx, l, c.centro, { radio: 2.5, color: p.dim });
    }

    // La linea de tiempo de abajo con las vueltas marcadas: es donde period y frecuencia
    // dejan de ser dos palabras y se vuelven dos distancias entre marcas.
    const yLinea = l.py(l.yMin) + 34;
    const x0 = l.px(l.xMin), x1 = l.px(l.xMax);
    ctx.strokeStyle = p.rule;
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(x0, yLinea);
    ctx.lineTo(x1, yLinea);
    ctx.stroke();
    const enX = s => x0 + ((x1 - x0) * s) / escena.duracion;
    for (const [c, color, dy] of [[movilA(), p.blue, -7], [movilB(), p.red, 7]]) {
      for (let v = 1; v * c.periodo <= escena.duracion + 1e-9; v++) {
        const x = enX(v * c.periodo);
        ctx.strokeStyle = color;
        ctx.beginPath();
        ctx.moveTo(x, yLinea);
        ctx.lineTo(x, yLinea + dy);
        ctx.stroke();
      }
    }
    ctx.strokeStyle = p.ink;
    ctx.beginPath();
    ctx.moveTo(enX(t), yLinea - 11);
    ctx.lineTo(enX(t), yLinea + 11);
    ctx.stroke();

    leer('w4-ta', movilA().periodo.toFixed(2) + ' s');
    leer('w4-fa', movilA().frecuencia.toFixed(2) + ' Hz');
    leer('w4-tb', movilB().periodo.toFixed(2) + ' s');
    leer('w4-fb', movilB().frecuencia.toFixed(2) + ' Hz');
  }
```

Con `ω_A = 2π` el período de A es exactamente 1 s y su frecuencia 1 Hz, que es el valor
que `verificacion-practico-1.py` imprime para el ejercicio 14.

Encabezado: `SIMULACIÓN 4`, nombre `Período y frecuencia`, frase de qué mirar:
`— contá las marcas de cada color en la línea de abajo.`

Dos sliders, `w4-oa` y `w4-ob`, de 1 a 12 rad/s.

- [ ] **Paso 4: verificar en el navegador**

El widget 1: la flecha azul siempre perpendicular a la punteada, para cualquier instante
y cualquier `ω`; la lectura de `r̂ · v` fija en `0.00`; la rapidez constante mientras gira.
El widget 4: el rojo da exactamente dos vueltas mientras el azul da una, y las marcas de
la línea de tiempo lo confirman.

- [ ] **Paso 5: correr la suite y commitear**

```bash
node --test "test/**/*.test.js"
git add docs/ensayos/movimiento-circular.html
git commit -m "feat(plataforma): ensayo de movimiento circular, versores y periodo"
```

---

### Tarea 17: El widget "a_t y a_n"

Es el widget central del ensayo: el que muestra que `v ⊥ a` sólo vale en el uniforme,
que son los incisos (d) y (e) del ejercicio 11.

**Archivos:**
- Modificar: `docs/ensayos/movimiento-circular.html`

**Interfaces:**
- Consume: lo de la Tarea 16.
- Produce: `widgetAceleraciones(pagina)`.

- [ ] **Paso 1: escribir la sección 02**

`<h2>`: `02 · Los dos trabajos de la aceleración`. El párrafo separa los dos: la
componente que apunta al centro cambia la dirección y no la rapidez; la que va en la
dirección del movimiento cambia la rapidez y no la dirección. Anticipa el experimento:
con `γ = 0` la flecha roja apunta exactamente al centro; apenas `γ` deja de ser cero, se
inclina hacia adelante.

- [ ] **Paso 2: escribir el widget**

Los valores por defecto son los del ejercicio 13: `R = 1.5`, `ω₀ = 0`, `γ = 4`.

```js
function widgetAceleraciones(pagina) {
  const R = 1.5;
  let omega0 = 2, gamma = 0;
  const movil = () => crearCircular({ R, omega0, gamma });

  const canvas = document.getElementById('w2-cv');
  const widget = crearWidget({
    pagina, canvas,
    margen: { L: 40, R: 130, T: 30, B: 30 },
    centrar: true,   // encuadre cuadrado, escala uniforme: mismo motivo que el widget 1
    encuadre: () => ({ xMin: -2.4, xMax: 2.4, yMin: -2.4, yMax: 2.4 }),
    dibujar: (ctx, l) => pintar(ctx, l, escena.t),
  });

  const escena = crearEscena({
    dibujar: () => widget.repintar(),
    duracion: 3,
    velocidad: 0.6,
    alCambiar: () => rotuloReproducir(document.getElementById('w2-play'), escena, enReposo),
  });

  function pintar(ctx, l, t) {
    const p = pagina.paleta();
    const c = movil();
    const [px, py] = l.p(c.pos(t));
    const [ox, oy] = l.p([0, 0]);

    eje(ctx, l, { color: p.rule });
    curva(ctx, l, s => [R * Math.cos(s), R * Math.sin(s)], 0, 2 * Math.PI,
      { color: p.graph, guiones: [3, 5], grosor: 1.2 });

    const [vx, vy] = c.vel(t);
    const kv = 22;
    vectorPx(ctx, px, py, px + vx * kv, py - vy * kv,
      { color: p.blue, grosor: 2.2, punta: 10, rotulo: 'v' });

    // Las dos componentes primero, en tenue, y la total encima: asi se ve que la total
    // es la suma de las dos y no una tercera flecha independiente.
    const ka = 6;
    const [rx, ry] = c.versorR(t);
    const [tx, ty] = c.versorTheta(t);
    const aN = c.aN(t), aT = c.aT(t);
    ctx.globalAlpha = 0.45;
    vectorPx(ctx, px, py, px - rx * aN * ka, py + ry * aN * ka,
      { color: p.red, grosor: 1.4, punta: 7, rotulo: 'aₙ', rdy: 12 });
    vectorPx(ctx, px, py, px + tx * aT * ka, py - ty * aT * ka,
      { color: p.red, grosor: 1.4, punta: 7, rotulo: 'a_t', rdy: -12 });
    ctx.globalAlpha = 1;
    const [ax, ay] = c.aTotalVector(t);
    vectorPx(ctx, px, py, px + ax * ka, py - ay * ka,
      { color: p.red, grosor: 2.4, punta: 11, rotulo: 'a' });

    punteado(ctx, ox, oy, px, py, { color: p.rule });
    cuerpo(ctx, l, c.pos(t), { radio: 5.5, color: p.ink });

    // El angulo entre v y a: 90 grados exactos mientras gamma sea cero, y es la lectura
    // que contesta el inciso (e) del ejercicio 11.
    const cosAng = (vx * ax + vy * ay) / (Math.hypot(vx, vy) * Math.hypot(ax, ay) || 1);
    const grados = Math.acos(Math.min(1, Math.max(-1, cosAng))) * 180 / Math.PI;

    leer('w2-rap', c.rapidez(t).toFixed(2) + ' m/s');
    leer('w2-at', aT.toFixed(2) + ' m/s²');
    leer('w2-an', aN.toFixed(2) + ' m/s²');
    leer('w2-ang', grados.toFixed(1) + '°');
  }
```

Encabezado: `SIMULACIÓN 2`, nombre `aₜ y aₙ`, frase de qué mirar:
`— subí γ apenas y mirá el ángulo de abajo dejar de ser 90°.`

Dos sliders: `w2-omega` de 0 a 6 rad/s valor 2, y `w2-gamma` de 0 a 4 rad/s² paso 0.1
valor 0, este último con `accent-color:var(--red)` porque es una aceleración.

- [ ] **Paso 3: escribir el cierre de la sección**

Un párrafo que diga las dos cosas que se acaban de ver, con los números del ejercicio 13
respaldados por `verificacion-practico-1.py`: con `γ = 0` el ángulo entre `v` y `a` es
90° exactos y la rapidez no se mueve; con `γ = 4` sobre `R = 1.5` la tangencial vale
`6 m/s²` fijos mientras la normal crece con el cuadrado de `ω`, y en `t = 5 s` la normal
ya vale `600 m/s²` contra esos mismos 6, así que la total es `600.03 m/s²` y apunta casi
exactamente al centro. Cerrar con la lectura que importa: que la normal domine no
significa que la tangencial no esté; significa que la rapidez cambia despacio comparada
con la dirección.

- [ ] **Paso 4: verificar en el navegador**

Con `γ = 0` el ángulo tiene que marcar `90.0°` en todo el recorrido y la rapidez quedarse
fija. Subir `γ` a 0.1 y ver el ángulo despegarse. Con `ω = 0` y `γ = 4`, esperar a
`t = 5 s` y confirmar `aₜ = 6.00`, `aₙ = 600.00`.

- [ ] **Paso 5: correr la suite y commitear**

```bash
node --test "test/**/*.test.js"
git add docs/ensayos/movimiento-circular.html
git commit -m "feat(plataforma): el widget de aceleracion tangencial y normal"
```

---

### Tarea 18: El widget "De las ecuaciones al círculo" y el cierre del ensayo

El lector escribe `x(t)` e `y(t)` y ve qué trayectoria dan. Viene precargado con el
ejercicio 14. Evaluar texto que escribe el usuario exige un intérprete propio: **nada de
`eval` ni de `new Function`**, que además de inseguro está prohibido por la política de
contenido de la mayoría de los navegadores en páginas servidas.

**Archivos:**
- Crear: `docs/fisica/expresion.js`
- Modificar: `docs/ensayos/movimiento-circular.html`
- Prueba: `test/expresion.test.js`

**Interfaces:**
- Consume: nada para el parser; el widget consume lo de la Tarea 16.
- Produce: `compilar(fuente)` que devuelve `{ ok: true, f }` donde `f(t)` es un número, o
  `{ ok: false, error }` con un mensaje en castellano. La gramática acepta: números,
  la variable `t`, las constantes `pi` y `e`, los operadores `+ - * / ^` con el unario
  menos, paréntesis, y las funciones `sen`, `cos`, `tan`, `raiz`, `abs`, `exp`, `ln`.

- [ ] **Paso 1: escribir las pruebas que fallan**

Crear `test/expresion.test.js`:

```js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { compilar } from '../docs/fisica/expresion.js';

const f = fuente => {
  const r = compilar(fuente);
  assert.ok(r.ok, `no compilo: ${r.error}`);
  return r.f;
};
const cerca = (a, b, tol = 1e-9) =>
  assert.ok(Math.abs(a - b) < tol, `${a} != ${b}`);

test('numeros y la variable t', () => {
  cerca(f('3')(0), 3);
  cerca(f('t')(4.5), 4.5);
  cerca(f('2.5')(0), 2.5);
});

test('las cuatro operaciones con la precedencia de siempre', () => {
  cerca(f('2 + 3 * 4')(0), 14);
  cerca(f('(2 + 3) * 4')(0), 20);
  cerca(f('10 / 4')(0), 2.5);
  cerca(f('10 - 3 - 2')(0), 5);       // asociatividad a izquierda
});

test('la potencia asocia a derecha y gana sobre el producto', () => {
  cerca(f('2 ^ 3 ^ 2')(0), 512);
  cerca(f('2 * 3 ^ 2')(0), 18);
});

test('el menos unario', () => {
  cerca(f('-t')(3), -3);
  cerca(f('-2 ^ 2')(0), -4);          // se aplica despues de la potencia
  cerca(f('3 * -2')(0), -6);
});

test('las constantes', () => {
  cerca(f('pi')(0), Math.PI);
  cerca(f('e')(0), Math.E);
});

test('las funciones, con nombres en castellano', () => {
  cerca(f('sen(0)')(0), 0);
  cerca(f('cos(0)')(0), 1);
  cerca(f('raiz(9)')(0), 3);
  cerca(f('abs(0 - 4)')(0), 4);
  cerca(f('ln(e)')(0), 1);
});

test('el ejercicio 14: x = sen(2 pi t), y = cos(2 pi t) + 1', () => {
  const x = f('sen(2 * pi * t)');
  const y = f('cos(2 * pi * t) + 1');
  cerca(x(0), 0);
  cerca(y(0), 2);
  cerca(x(0.25), 1);
  cerca(y(0.25), 1);
  // Todo punto cae sobre el circulo de radio 1 centrado en (0, 1).
  for (const t of [0.1, 0.37, 0.8]) cerca(Math.hypot(x(t), y(t) - 1), 1);
});

test('un parentesis sin cerrar da error, no una excepcion', () => {
  const r = compilar('sen(2 * t');
  assert.equal(r.ok, false);
  assert.ok(typeof r.error === 'string' && r.error.length > 0);
});

test('una funcion desconocida da error con su nombre adentro', () => {
  const r = compilar('tang(t)');
  assert.equal(r.ok, false);
  assert.ok(r.error.includes('tang'));
});

test('una variable que no es t da error', () => {
  const r = compilar('x + 1');
  assert.equal(r.ok, false);
});

test('el texto vacio da error', () => {
  assert.equal(compilar('').ok, false);
  assert.equal(compilar('   ').ok, false);
});

test('sobra basura al final: tambien es error', () => {
  assert.equal(compilar('2 + 3 )').ok, false);
  assert.equal(compilar('2 3').ok, false);
});

test('no se puede colar codigo: nada de propiedades ni llamadas raras', () => {
  for (const fuente of ['constructor', 't.constructor', 'globalThis', '[].map']) {
    assert.equal(compilar(fuente).ok, false, `${fuente} no deberia compilar`);
  }
});

test('una division por cero da infinito, no una excepcion', () => {
  assert.equal(f('1 / 0')(0), Infinity);
});
```

- [ ] **Paso 2: correrlas y verificar que fallan**

Ejecutar: `node --test test/expresion.test.js`
Esperado: FALLAN todas, el módulo no existe.

- [ ] **Paso 3: implementar el intérprete**

Análisis léxico y descenso recursivo. Corto porque la gramática es chica:

```js
// Interprete de expresiones de una variable. Es a proposito un interprete y no un
// eval: lo que se evalua lo escribe el lector en un campo de texto de una pagina
// publicada, y eval le daria acceso a todo el documento.

const FUNCIONES = {
  sen: Math.sin, cos: Math.cos, tan: Math.tan,
  raiz: Math.sqrt, abs: Math.abs, exp: Math.exp, ln: Math.log,
};
const CONSTANTES = { pi: Math.PI, e: Math.E };

function tokenizar(fuente) {
  const tokens = [];
  let i = 0;
  while (i < fuente.length) {
    const c = fuente[i];
    if (/\s/.test(c)) { i++; continue; }
    if (/[0-9.]/.test(c)) {
      let j = i;
      while (j < fuente.length && /[0-9.]/.test(fuente[j])) j++;
      const n = Number(fuente.slice(i, j));
      if (!Number.isFinite(n)) throw new Error(`no entiendo el número «${fuente.slice(i, j)}»`);
      tokens.push({ tipo: 'numero', valor: n });
      i = j;
      continue;
    }
    if (/[a-zA-Z]/.test(c)) {
      let j = i;
      while (j < fuente.length && /[a-zA-Z]/.test(fuente[j])) j++;
      tokens.push({ tipo: 'nombre', valor: fuente.slice(i, j) });
      i = j;
      continue;
    }
    if ('+-*/^()'.includes(c)) { tokens.push({ tipo: c }); i++; continue; }
    throw new Error(`no entiendo el símbolo «${c}»`);
  }
  return tokens;
}

export function compilar(fuente) {
  try {
    const tokens = tokenizar(fuente);
    if (!tokens.length) throw new Error('la expresión está vacía');
    let k = 0;
    const mirar = () => tokens[k];
    const comer = tipo => {
      if (!tokens[k] || tokens[k].tipo !== tipo) throw new Error(`falta «${tipo}»`);
      return tokens[k++];
    };

    // suma := producto (('+' | '-') producto)*
    const suma = () => {
      let izq = producto();
      while (mirar() && (mirar().tipo === '+' || mirar().tipo === '-')) {
        const op = tokens[k++].tipo;
        const der = producto();
        const a = izq;
        izq = op === '+' ? t => a(t) + der(t) : t => a(t) - der(t);
      }
      return izq;
    };
    // producto := unario (('*' | '/') unario)*
    const producto = () => {
      let izq = unario();
      while (mirar() && (mirar().tipo === '*' || mirar().tipo === '/')) {
        const op = tokens[k++].tipo;
        const der = unario();
        const a = izq;
        izq = op === '*' ? t => a(t) * der(t) : t => a(t) / der(t);
      }
      return izq;
    };
    // unario := '-' unario | potencia     (el menos se aplica despues de la potencia)
    const unario = () => {
      if (mirar() && mirar().tipo === '-') { k++; const u = unario(); return t => -u(t); }
      return potencia();
    };
    // potencia := atomo ('^' unario)?     (asocia a derecha)
    const potencia = () => {
      const base = atomo();
      if (mirar() && mirar().tipo === '^') { k++; const exp = unario(); return t => base(t) ** exp(t); }
      return base;
    };
    const atomo = () => {
      const tk = mirar();
      if (!tk) throw new Error('la expresión se corta antes de tiempo');
      if (tk.tipo === 'numero') { k++; return () => tk.valor; }
      if (tk.tipo === '(') { k++; const dentro = suma(); comer(')'); return dentro; }
      if (tk.tipo === 'nombre') {
        k++;
        const nombre = tk.valor;
        if (mirar() && mirar().tipo === '(') {
          k++;
          const arg = suma();
          comer(')');
          const fn = Object.prototype.hasOwnProperty.call(FUNCIONES, nombre) ? FUNCIONES[nombre] : null;
          if (!fn) throw new Error(`no conozco la función «${nombre}»`);
          return t => fn(arg(t));
        }
        if (nombre === 't') return t => t;
        if (Object.prototype.hasOwnProperty.call(CONSTANTES, nombre)) {
          const v = CONSTANTES[nombre];
          return () => v;
        }
        throw new Error(`no conozco «${nombre}»; la única variable es t`);
      }
      throw new Error('esperaba un número, una variable o un paréntesis');
    };

    const f = suma();
    if (k !== tokens.length) throw new Error('sobra texto al final de la expresión');
    return { ok: true, f };
  } catch (e) {
    return { ok: false, error: e.message };
  }
}
```

El `hasOwnProperty` no es adorno: sin él, `constructor` o `toString` como nombre de
función encontrarían algo en la cadena de prototipos.

- [ ] **Paso 4: escribir la sección 03 y el widget**

`<h2>`: `03 · De las ecuaciones al círculo`. El párrafo dice que un movimiento circular
no siempre viene anunciado: a veces llega como dos ecuaciones paramétricas y hay que
reconocerlo, que es exactamente lo que pide el ejercicio 14.

El widget tiene dos `<input type="text">` —`w3-x` precargado con `sen(2 * pi * t)` y
`w3-y` con `cos(2 * pi * t) + 1`— y dibuja la trayectoria que generan entre `t = 0` y
`t = 1`, más el punto en el instante del slider `w3-t`. Si alguna expresión no compila,
se muestra el mensaje de error debajo del campo, en `--red`, y se conserva en pantalla la
última trayectoria válida en vez de dejar el canvas en blanco.

Tres presets: `Ej. 14` recarga el par original; `Elipse` carga `2 * sen(2 * pi * t)` y
`cos(2 * pi * t)`; `Recta` carga `t` y `t`. Los dos últimos existen para que se vea qué
**no** es un círculo.

Encabezado: `SIMULACIÓN 3`, nombre `De las ecuaciones al círculo`, frase de qué mirar:
`— cambiá un 2 por un 3 y fijate si sigue siendo una circunferencia.`

Cuatro lecturas: `t`, `x(t)`, `y(t)`, y `distancia al centro`, esta última calculada
contra el centro del círculo que mejor ajusta la trayectoria muestreada; es la que
delata si la figura es o no una circunferencia, porque se queda fija sólo cuando lo es.

- [ ] **Paso 5: escribir el cierre del ensayo**

Con el `<h2>` `Para resolver 11 a 14` y la lista ordenada:

1. Separá siempre "cuánto" de "hacia dónde": la rapidez la cambia sólo `aₜ`.
2. En el uniforme, `aₜ = 0` y toda la aceleración apunta al centro. No es que no haya aceleración: es que no cambia la rapidez.
3. `v = ω R` y `aₙ = ω² R = v²/R`. Si en el enunciado hay rpm, pasalas a rad/s antes de tocar nada.
4. Frente a dos ecuaciones paramétricas, calculá la distancia al centro candidato. Si no depende de `t`, es una circunferencia.
5. `T = 2π/ω` y `f = 1/T`. Son la misma información dicha de dos maneras.

- [ ] **Paso 6: verificar en el navegador**

Confirmar que el par precargado dibuja la circunferencia de radio 1 centrada en `(0, 1)`
y que la lectura de distancia al centro se queda en `1.00` para todo `t`; que `Elipse` la
hace variar; que escribir `sen(` deja el mensaje de error y **no** borra el dibujo; y que
escribir `constructor` da error en vez de cualquier otra cosa.

- [ ] **Paso 7: correr la suite y commitear**

```bash
node --test "test/**/*.test.js"
git add docs/fisica/expresion.js test/expresion.test.js docs/ensayos/movimiento-circular.html
git commit -m "feat(plataforma): de las ecuaciones al circulo, con interprete propio"
```

---

## Fase E — cierre

### Tarea 19: La portada del dueño y el hilo entre los tres ensayos

El dueño del proyecto está diseñando la portada por su cuenta. Esta tarea la incorpora
y deja la Guía 1 navegable de punta a punta.

**Archivos:**
- Modificar: `docs/index.html`, `docs/ensayos/tiro-parabolico.html`,
  `docs/ensayos/derivada-integral.html`, `docs/ensayos/movimiento-circular.html`,
  `README.md`

**Interfaces:**
- Consume: los tres ensayos terminados.
- Produce: la portada del dueño integrada y la navegación entre ensayos.

- [ ] **Paso 1: incorporar el diseño de la portada**

Cuando el archivo de diseño de la portada esté en el repositorio, reemplazar
`docs/index.html` siguiéndolo al pie de la letra, con el mismo criterio que la Tarea 6 del
plan anterior: los valores se copian, no se aproximan, y toda diferencia se declara en el
informe. La única fontanería que se agrega es el script de tema en el `<head>` y los
enlaces reales a los tres ensayos.

**Si el diseño todavía no llegó**, esta tarea se limita a los pasos 2 a 5 y la portada
queda como está. No se inventa una portada nueva para adelantarse.

- [ ] **Paso 2: que la portada enlace los tres ensayos**

Esto va **aunque el diseño de la portada no haya llegado** y el paso 1 se haya salteado.
Hoy `docs/index.html` lista los seis ensayos pero sólo el de tiro tiene enlace; los otros
dos existen y no se puede llegar a ellos desde ningún lado. Los que siguen sin existir
quedan como están, sin enlace y en `--dim`.

- [ ] **Paso 3: sacar `tema()` de los ensayos a un módulo**

Los tres ensayos repiten el mismo bloque de veinte líneas —leer el tema, alternarlo,
persistirlo, rotular el botón y repintar—, copiado carácter a carácter. Con tres copias
ya conviene, y el brief del proyecto tiene seis ensayos: mudalo a `docs/motor/tema.js`
como `conectarTema({ pagina, boton, documento })` y dejá en cada ensayo la llamada.

El script bloqueante del `<head>` **no** se muda: tiene que seguir corriendo antes del
primer pintado y no puede depender de un módulo diferido.

Verificá que los tres ensayos queden con el bitmap de sus canvas idéntico antes y después
—hash de `toDataURL()`, con el caché de Chrome desactivado y un control negativo—, y que
el tema siga persistiendo entre páginas.

- [ ] **Paso 4: enlazar los tres ensayos entre sí**

Al pie de cada ensayo, antes de la línea de fuentes, una fila con el anterior y el
siguiente en el orden de lectura —1 → 2 → 3—, con la tipografía mono de interfaz y en
`--dim`, y un enlace a la portada. El primero no lleva anterior y el tercero no lleva
siguiente.

- [ ] **Paso 5: actualizar el README**

La viñeta de la plataforma que ya existe en "Material de repaso" pasa a nombrar los tres
ensayos que hay. Una línea, sobria: el dueño ya avisó que no hace falta explicar todo en
el README.

- [ ] **Paso 6: recorrer las cuatro páginas**

Portada, tres ensayos, doce widgets. Comprobar: ningún enlace roto; el tema elegido
sobrevive a navegar entre las cuatro; ningún widget se anima solo; y a 400 px de ancho
ninguna página desborda en horizontal.

- [ ] **Paso 7: correr la suite y commitear**

```bash
node --test "test/**/*.test.js"
git add docs/index.html docs/ensayos docs/motor/tema.js README.md
git commit -m "feat(plataforma): portada y navegacion entre los ensayos de la guia 1"
```

---

## Qué queda para después de este plan

- Los ensayos 4, 5 y 6 del brief —cuerpo aislado, sistemas acoplados y energía—, que
  cubren las guías 2 y 3.
- La línea de tiempo arrastrable que el brief lista entre los controles estándar. `ir(t)`
  de la Tarea 2 es la mitad que faltaba; queda el control.
- Publicar en GitHub Pages, que es una acción manual del dueño en la configuración del
  repositorio, y la decisión sobre si `docs/plataforma/` y `docs/superpowers/` deben
  seguir dentro de la carpeta que Pages publica.
