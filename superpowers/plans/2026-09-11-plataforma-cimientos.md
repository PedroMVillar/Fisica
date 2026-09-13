# Plataforma de Física 1 — Cimientos y primer widget

> **Para quien ejecute:** SUB-SKILL REQUERIDA: usar `superpowers:subagent-driven-development`
> (recomendado) o `superpowers:executing-plans` para implementar tarea por tarea.
> Los pasos usan `- [ ]` para seguimiento.

**Objetivo:** dejar funcionando el motor de escenas y el primer widget interactivo
("Las dos sombras" del ensayo de tiro parabólico), publicado y con pruebas.

**Arquitectura:** sitio estático sin build. Módulos ES nativos en el navegador,
canvas 2D para dibujar, cero dependencias salvo KaTeX por CDN. La lógica pura
(coordenadas, física, descriptores de control) vive separada del dibujo, y es lo que
se testea con el runner de pruebas incorporado de Node. El dibujo se testea contra un
contexto de canvas falso que registra las llamadas.

**Stack:** HTML + CSS + JavaScript (módulos ES). Node 22 para las pruebas
(`node --test`, sin dependencias). Python para el servidor local. GitHub Pages.

**Spec:** `plataforma/brief.md`
**Fuente de verdad del diseño:** `plataforma/diseno/Tiro parabolico.dc.html`

## Restricciones globales

Aplican a todas las tareas de este plan y de los siguientes.

- **Cero dependencias de runtime** salvo KaTeX por CDN. Nada de `npm install`.
- **Cero build.** Lo que está en el repositorio es lo que sirve el navegador.
- **Los tokens de color son exactamente estos**, y no se inventa ninguno:
  claro `--paper:#fbfaf7` `--band:#f2f0ea` `--ink:#16151a` `--dim:#6a6760`
  `--rule:#dcd8ce` `--blue:#1b4fd4` `--blue-soft:#8aa3e6` `--red:#c02a24`
  `--graph:#8e8a80`; oscuro `--paper:#131316` `--band:#191a1e` `--ink:#eceae4`
  `--dim:#948f86` `--rule:#2e2f35` `--blue:#7aa2ff` `--blue-soft:#3f5694`
  `--red:#ef5f52` `--graph:#6f6c66`.
- **Reparto semántico fijo:** azul para cinemática y velocidad, rojo para aceleración
  y fuerza. Nunca al revés.
- **Tipografías:** Source Serif 4 para el contenido, JetBrains Mono para la interfaz.
  Serif para lo que se lee, mono para lo que se opera.
- **Grilla:** columna de texto `max-width:680px`, widget `max-width:880px` dentro de
  una franja a todo el ancho.
- **Canvas:** `width:100%`, `aspect-ratio:16/8`, `touch-action:none`.
- **Ningún widget se anima solo al cargar.** Arranca quieto en un estado
  representativo.
- **Ningún número aparece sin respaldo** en un `verificacion-*.py` del repositorio.
- **Todo widget lleva la frase de "qué mirar"** en su encabezado.
- Ante discrepancia entre el spec y el archivo de diseño, manda el archivo de diseño.

---

## Estructura de archivos

El sitio vive en `docs/` porque GitHub Pages sólo puede servir desde la raíz o desde
`docs/`, y así no hace falta ninguna GitHub Action.

| Archivo | Responsabilidad |
|---|---|
| `docs/.nojekyll` | Evita que Pages procese el sitio con Jekyll |
| `docs/index.html` | Portada con los ensayos |
| `docs/estilos/base.css` | Tokens, tipografía, grilla y anatomía del widget |
| `docs/motor/lienzo.js` | Conversión de coordenadas físicas a píxeles y viceversa |
| `docs/motor/dibujo.js` | Primitivas: eje, vector, cuerpo, traza, ángulo, barra |
| `docs/motor/controles.js` | Descriptores de slider, toggle, botón y lectura |
| `docs/motor/escena.js` | Ciclo de vida: reposo, reproduciendo, pausado; el loop |
| `docs/fisica/tiro.js` | Tiro parabólico: posición, velocidad e hitos |
| `docs/ensayos/tiro-parabolico.html` | El ensayo |
| `test/*.test.js` | Pruebas con `node --test` |
| `package.json` | Sólo `{"type":"module","private":true}`; sin dependencias |

Separación clave: `lienzo`, `controles` y `fisica` son **funciones puras** y se
testean directo. `dibujo` recibe un contexto y se testea con uno falso. `escena` recibe
un reloj inyectable y se testea sin navegador.

---

## Tarea 1: Estructura, tokens y prueba de fidelidad al diseño

La prueba de esta tarea es la red de seguridad de todo el proyecto: falla si alguien
cambia un color respecto del diseño.

**Archivos:**
- Crear: `package.json`, `docs/.nojekyll`, `docs/estilos/base.css`
- Test: `test/tokens.test.js`

**Interfaces:**
- Produce: `docs/estilos/base.css` con los dieciocho tokens (nueve por tema).

- [ ] **Paso 1: escribir la prueba que falla**

```js
// test/tokens.test.js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const css = readFileSync('docs/estilos/base.css', 'utf8');

function tokens(selector) {
  const i = css.indexOf(selector);
  assert.ok(i >= 0, `falta el selector ${selector}`);
  const bloque = css.slice(i, css.indexOf('}', i));
  return Object.fromEntries(
    [...bloque.matchAll(/--([a-z-]+)\s*:\s*(#[0-9a-f]{6})/gi)]
      .map(m => [m[1], m[2].toLowerCase()])
  );
}

test('tokens del tema claro, exactos al diseño', () => {
  assert.deepEqual(tokens(':root{'), {
    paper: '#fbfaf7', band: '#f2f0ea', ink: '#16151a', dim: '#6a6760',
    rule: '#dcd8ce', blue: '#1b4fd4', 'blue-soft': '#8aa3e6',
    red: '#c02a24', graph: '#8e8a80',
  });
});

test('tokens del tema oscuro, exactos al diseño', () => {
  assert.deepEqual(tokens(':root[data-theme="dark"]{'), {
    paper: '#131316', band: '#191a1e', ink: '#eceae4', dim: '#948f86',
    rule: '#2e2f35', blue: '#7aa2ff', 'blue-soft': '#3f5694',
    red: '#ef5f52', graph: '#6f6c66',
  });
});
```

- [ ] **Paso 2: correrla y verificar que falla**

Ejecutar: `node --test test/tokens.test.js`
Esperado: FALLA con `ENOENT` porque `docs/estilos/base.css` no existe.

- [ ] **Paso 3: crear los archivos**

```bash
mkdir -p docs/estilos docs/motor docs/fisica docs/ensayos test
printf '%s\n' '{"type":"module","private":true}' > package.json
touch docs/.nojekyll
```

```css
/* docs/estilos/base.css */
:root{
  --paper:#fbfaf7; --band:#f2f0ea; --ink:#16151a; --dim:#6a6760; --rule:#dcd8ce;
  --blue:#1b4fd4; --blue-soft:#8aa3e6; --red:#c02a24; --graph:#8e8a80;
}
:root[data-theme="dark"]{
  --paper:#131316; --band:#191a1e; --ink:#eceae4; --dim:#948f86; --rule:#2e2f35;
  --blue:#7aa2ff; --blue-soft:#3f5694; --red:#ef5f52; --graph:#6f6c66;
}
html{background:var(--paper)}
body{margin:0;background:var(--paper);color:var(--ink);
     font-family:"Source Serif 4",Charter,Georgia,serif;-webkit-font-smoothing:antialiased}
a{color:var(--blue);text-decoration:none;border-bottom:1px solid var(--blue-soft)}
a:hover{color:var(--red);border-bottom-color:var(--red)}
input[type=range]{accent-color:var(--blue);background:transparent}
button{font-family:"JetBrains Mono",ui-monospace,monospace}
@keyframes tp-pulse{
  0%,100%{box-shadow:0 0 0 0 rgba(27,79,212,0)}
  50%{box-shadow:0 0 0 7px rgba(27,79,212,.16)}
}
```

- [ ] **Paso 4: correr y verificar que pasa**

Ejecutar: `node --test test/tokens.test.js`
Esperado: 2 pruebas OK.

- [ ] **Paso 5: commit**

```bash
git add package.json docs/.nojekyll docs/estilos/base.css test/tokens.test.js
git commit -m "feat(plataforma): tokens de color con prueba de fidelidad al diseno"
```

---

## Tarea 2: Lienzo — coordenadas físicas a píxeles

**Archivos:**
- Crear: `docs/motor/lienzo.js`
- Test: `test/lienzo.test.js`

**Interfaces:**
- Produce: `crearLienzo({ ancho, alto, xMin, xMax, yMin, yMax })` que devuelve un
  objeto con `px(x)`, `py(y)`, `p([x,y])`, `ux(px)`, `uy(py)` y `escala`.
  `px`/`py` van de unidades físicas a píxeles; `ux`/`uy` vuelven. El eje `y` se
  invierte, porque en canvas crece hacia abajo.

- [ ] **Paso 1: escribir la prueba que falla**

```js
// test/lienzo.test.js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { crearLienzo } from '../docs/motor/lienzo.js';

const L = () => crearLienzo({ ancho: 800, alto: 400, xMin: 0, xMax: 100, yMin: 0, yMax: 50 });

test('el origen fisico cae en la esquina inferior izquierda', () => {
  const l = L();
  assert.equal(l.px(0), 0);
  assert.equal(l.py(0), 400);
});

test('el maximo cae en la esquina superior derecha', () => {
  const l = L();
  assert.equal(l.px(100), 800);
  assert.equal(l.py(50), 0);
});

test('el eje y se invierte', () => {
  const l = L();
  assert.equal(l.py(25), 200);
});

test('p() convierte un par', () => {
  assert.deepEqual(L().p([50, 25]), [400, 200]);
});

test('ux y uy son la inversa exacta', () => {
  const l = L();
  assert.equal(l.ux(l.px(37)), 37);
  assert.ok(Math.abs(l.uy(l.py(12.5)) - 12.5) < 1e-9);
});

test('escala expone pixeles por unidad en cada eje', () => {
  const l = L();
  assert.equal(l.escala.x, 8);
  assert.equal(l.escala.y, 8);
});
```

- [ ] **Paso 2: correrla y verificar que falla**

Ejecutar: `node --test test/lienzo.test.js`
Esperado: FALLA, `crearLienzo` no existe.

- [ ] **Paso 3: implementar lo mínimo**

```js
// docs/motor/lienzo.js
export function crearLienzo({ ancho, alto, xMin, xMax, yMin, yMax }) {
  const kx = ancho / (xMax - xMin);
  const ky = alto / (yMax - yMin);
  const px = x => (x - xMin) * kx;
  const py = y => alto - (y - yMin) * ky;
  return {
    ancho, alto, xMin, xMax, yMin, yMax,
    px, py,
    p: ([x, y]) => [px(x), py(y)],
    ux: v => v / kx + xMin,
    uy: v => (alto - v) / ky + yMin,
    escala: { x: kx, y: ky },
  };
}
```

- [ ] **Paso 4: correr y verificar que pasa**

Ejecutar: `node --test test/lienzo.test.js`
Esperado: 6 pruebas OK.

- [ ] **Paso 5: commit**

```bash
git add docs/motor/lienzo.js test/lienzo.test.js
git commit -m "feat(plataforma): lienzo, conversion de coordenadas fisicas a pixeles"
```

---

## Tarea 3: Primitivas de dibujo

Se testean contra un contexto falso que registra las llamadas, así se verifica que
cada primitiva dibuja lo que debe y **con el color semántico correcto**.

**Archivos:**
- Crear: `docs/motor/dibujo.js`
- Test: `test/dibujo.test.js`

**Interfaces:**
- Consume: `crearLienzo` de la Tarea 2.
- Produce: `eje(ctx, l, opciones)`, `vector(ctx, l, desde, hasta, { color, rotulo })`,
  `cuerpo(ctx, l, punto, { radio })`, `traza(ctx, l, puntos)`,
  `huella(ctx, l, punto)`. Todas reciben el contexto primero y el lienzo segundo.
  Todas devuelven `undefined` y sólo dibujan.
- Produce también `ctxFalso()` exportado desde el test, no desde el módulo.

- [ ] **Paso 1: escribir la prueba que falla**

```js
// test/dibujo.test.js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { crearLienzo } from '../docs/motor/lienzo.js';
import { vector, cuerpo, traza } from '../docs/motor/dibujo.js';

function ctxFalso() {
  const ops = [];
  const c = { ops, strokeStyle: '', fillStyle: '', lineWidth: 0 };
  for (const m of ['beginPath','moveTo','lineTo','stroke','fill','arc','closePath','save','restore','translate','rotate']) {
    c[m] = (...a) => ops.push([m, ...a]);
  }
  return c;
}

const L = crearLienzo({ ancho: 800, alto: 400, xMin: 0, xMax: 100, yMin: 0, yMax: 50 });

test('vector traza una linea del origen al destino en pixeles', () => {
  const c = ctxFalso();
  vector(c, L, [0, 0], [50, 0], { color: '#1b4fd4' });
  const move = c.ops.find(o => o[0] === 'moveTo');
  const line = c.ops.find(o => o[0] === 'lineTo');
  assert.deepEqual(move.slice(1), [0, 400]);
  assert.deepEqual(line.slice(1), [400, 400]);
});

test('vector usa el color que se le pasa', () => {
  const c = ctxFalso();
  vector(c, L, [0, 0], [10, 10], { color: '#c02a24' });
  assert.equal(c.strokeStyle, '#c02a24');
});

test('vector de largo nulo no dibuja nada', () => {
  const c = ctxFalso();
  vector(c, L, [5, 5], [5, 5], { color: '#1b4fd4' });
  assert.equal(c.ops.length, 0);
});

test('cuerpo dibuja un arco cerrado en la posicion', () => {
  const c = ctxFalso();
  cuerpo(c, L, [50, 25], { radio: 4 });
  const arco = c.ops.find(o => o[0] === 'arc');
  assert.deepEqual(arco.slice(1, 4), [400, 200, 4]);
});

test('traza recorre todos los puntos', () => {
  const c = ctxFalso();
  traza(c, L, [[0, 0], [50, 25], [100, 0]]);
  assert.equal(c.ops.filter(o => o[0] === 'lineTo').length, 2);
});
```

- [ ] **Paso 2: correrla y verificar que falla**

Ejecutar: `node --test test/dibujo.test.js`
Esperado: FALLA, el módulo no existe.

- [ ] **Paso 3: implementar lo mínimo**

```js
// docs/motor/dibujo.js
const PUNTA = 9;

export function vector(ctx, l, desde, hasta, { color, grosor = 2 } = {}) {
  const [x1, y1] = l.p(desde);
  const [x2, y2] = l.p(hasta);
  const dx = x2 - x1, dy = y2 - y1;
  const largo = Math.hypot(dx, dy);
  if (largo < 1e-9) return;
  ctx.strokeStyle = color;
  ctx.fillStyle = color;
  ctx.lineWidth = grosor;
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.stroke();
  const ux = dx / largo, uy = dy / largo;
  ctx.beginPath();
  ctx.moveTo(x2, y2);
  ctx.lineTo(x2 - ux * PUNTA - uy * PUNTA * 0.4, y2 - uy * PUNTA + ux * PUNTA * 0.4);
  ctx.lineTo(x2 - ux * PUNTA + uy * PUNTA * 0.4, y2 - uy * PUNTA - ux * PUNTA * 0.4);
  ctx.closePath();
  ctx.fill();
}

export function cuerpo(ctx, l, punto, { radio = 4, color = '#16151a' } = {}) {
  const [x, y] = l.p(punto);
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.arc(x, y, radio, 0, Math.PI * 2);
  ctx.fill();
}

export function huella(ctx, l, punto, { radio = 2.5, color = '#8e8a80' } = {}) {
  cuerpo(ctx, l, punto, { radio, color });
}

export function traza(ctx, l, puntos, { color = '#1b4fd4', grosor = 2 } = {}) {
  if (puntos.length < 2) return;
  ctx.strokeStyle = color;
  ctx.lineWidth = grosor;
  ctx.beginPath();
  const [x0, y0] = l.p(puntos[0]);
  ctx.moveTo(x0, y0);
  for (let i = 1; i < puntos.length; i++) {
    const [x, y] = l.p(puntos[i]);
    ctx.lineTo(x, y);
  }
  ctx.stroke();
}

export function eje(ctx, l, { color = '#dcd8ce' } = {}) {
  ctx.strokeStyle = color;
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(l.px(l.xMin), l.py(0));
  ctx.lineTo(l.px(l.xMax), l.py(0));
  ctx.moveTo(l.px(0), l.py(l.yMin));
  ctx.lineTo(l.px(0), l.py(l.yMax));
  ctx.stroke();
}
```

- [ ] **Paso 4: correr y verificar que pasa**

Ejecutar: `node --test test/dibujo.test.js`
Esperado: 5 pruebas OK.

- [ ] **Paso 5: commit**

```bash
git add docs/motor/dibujo.js test/dibujo.test.js
git commit -m "feat(plataforma): primitivas de dibujo con contexto falso en las pruebas"
```

---

## Tarea 4: Física del tiro parabólico

Los valores esperados salen de `parcial-1/soluciones/verificacion-practico-1.py`, que
ya está verificado con sympy. No se inventa ningún número.

**Archivos:**
- Crear: `docs/fisica/tiro.js`
- Test: `test/tiro.test.js`

**Interfaces:**
- Produce: `crearTiro({ v0, alfaGrados, x0 = 0, y0 = 0, g = 9.8, ax = 0 })` que
  devuelve `{ pos(t), vel(t), tMax, yMax, tVuelo, alcance }`. `pos` y `vel` devuelven
  pares `[x, y]`. `tMax` es el instante del punto más alto.

- [ ] **Paso 1: escribir la prueba que falla**

```js
// test/tiro.test.js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { crearTiro } from '../docs/fisica/tiro.js';

const cerca = (a, b, tol = 0.05) =>
  assert.ok(Math.abs(a - b) < tol, `${a} != ${b} (tol ${tol})`);

test('ejercicio 9: canon horizontal desde 44 m con 25 m/s', () => {
  const t = crearTiro({ v0: 25, alfaGrados: 0, y0: 44 });
  cerca(t.tVuelo, 2.997);
  cerca(t.alcance, 74.9, 0.2);
  cerca(t.vel(t.tVuelo)[1], -29.4, 0.1);
});

test('ejercicio 15: 24 m/s a 30 grados, punto mas alto', () => {
  const t = crearTiro({ v0: 24, alfaGrados: 30 });
  cerca(t.tMax, 1.2, 0.01);
  cerca(t.yMax, 7.2, 0.05);
});

test('ejercicio 15 con viento: a_x = -2 acorta el alcance a 44.1 m', () => {
  const t = crearTiro({ v0: 24, alfaGrados: 30, ax: -2 });
  cerca(t.pos(2.4)[0], 44.1, 0.1);
});

test('el eje y no se entera del viento', () => {
  const sin = crearTiro({ v0: 24, alfaGrados: 30 });
  const con = crearTiro({ v0: 24, alfaGrados: 30, ax: -2 });
  cerca(con.tVuelo, sin.tVuelo, 1e-9);
  cerca(con.yMax, sin.yMax, 1e-9);
});

test('en el punto mas alto la velocidad vertical se anula pero la total no', () => {
  const t = crearTiro({ v0: 24, alfaGrados: 30 });
  const [vx, vy] = t.vel(t.tMax);
  cerca(vy, 0, 1e-9);
  cerca(vx, 24 * Math.cos(Math.PI / 6), 1e-9);
});
```

- [ ] **Paso 2: correrla y verificar que falla**

Ejecutar: `node --test test/tiro.test.js`
Esperado: FALLA, el módulo no existe.

- [ ] **Paso 3: implementar lo mínimo**

```js
// docs/fisica/tiro.js
export function crearTiro({ v0, alfaGrados, x0 = 0, y0 = 0, g = 9.8, ax = 0 }) {
  const a = (alfaGrados * Math.PI) / 180;
  const v0x = v0 * Math.cos(a);
  const v0y = v0 * Math.sin(a);

  const pos = t => [x0 + v0x * t + 0.5 * ax * t * t, y0 + v0y * t - 0.5 * g * t * t];
  const vel = t => [v0x + ax * t, v0y - g * t];

  const tMax = v0y / g;
  const yMax = y0 + (v0y * v0y) / (2 * g);
  // y(t) = 0  ->  (g/2) t^2 - v0y t - y0 = 0
  const tVuelo = (v0y + Math.sqrt(v0y * v0y + 2 * g * y0)) / g;
  const alcance = pos(tVuelo)[0];

  return { pos, vel, tMax, yMax, tVuelo, alcance, v0x, v0y };
}
```

- [ ] **Paso 4: correr y verificar que pasa**

Ejecutar: `node --test test/tiro.test.js`
Esperado: 5 pruebas OK.

- [ ] **Paso 5: commit**

```bash
git add docs/fisica/tiro.js test/tiro.test.js
git commit -m "feat(plataforma): fisica del tiro parabolico, contrastada con la verificacion del practico 1"
```

---

## Tarea 5: Motor de escena — estados y reloj

**Archivos:**
- Crear: `docs/motor/escena.js`
- Test: `test/escena.test.js`

**Interfaces:**
- Produce: `crearEscena({ dibujar, duracion, alCambiar })` con los métodos
  `reproducir()`, `pausar()`, `reiniciar()`, `avanzar(dt)` y las propiedades `t` y
  `estado`. `estado` es `'reposo' | 'reproduciendo' | 'pausado'`. `avanzar` es lo que
  el loop llama; en las pruebas se llama a mano, sin navegador.

- [ ] **Paso 1: escribir la prueba que falla**

```js
// test/escena.test.js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { crearEscena } from '../docs/motor/escena.js';

test('arranca en reposo y en t=0', () => {
  const e = crearEscena({ dibujar() {}, duracion: 3 });
  assert.equal(e.estado, 'reposo');
  assert.equal(e.t, 0);
});

test('no avanza el tiempo mientras no se reproduce', () => {
  const e = crearEscena({ dibujar() {}, duracion: 3 });
  e.avanzar(0.5);
  assert.equal(e.t, 0);
});

test('avanza al reproducir y se frena al pausar', () => {
  const e = crearEscena({ dibujar() {}, duracion: 3 });
  e.reproducir();
  e.avanzar(0.5);
  assert.equal(e.t, 0.5);
  e.pausar();
  e.avanzar(0.5);
  assert.equal(e.t, 0.5);
  assert.equal(e.estado, 'pausado');
});

test('al llegar al final se detiene en la duracion', () => {
  const e = crearEscena({ dibujar() {}, duracion: 3 });
  e.reproducir();
  e.avanzar(10);
  assert.equal(e.t, 3);
  assert.equal(e.estado, 'pausado');
});

test('reiniciar vuelve a reposo en cero', () => {
  const e = crearEscena({ dibujar() {}, duracion: 3 });
  e.reproducir(); e.avanzar(1); e.reiniciar();
  assert.equal(e.t, 0);
  assert.equal(e.estado, 'reposo');
});

test('avisa cada vez que cambia de estado', () => {
  const vistos = [];
  const e = crearEscena({ dibujar() {}, duracion: 3, alCambiar: s => vistos.push(s) });
  e.reproducir(); e.pausar(); e.reiniciar();
  assert.deepEqual(vistos, ['reproduciendo', 'pausado', 'reposo']);
});
```

- [ ] **Paso 2: correrla y verificar que falla**

Ejecutar: `node --test test/escena.test.js`
Esperado: FALLA, el módulo no existe.

- [ ] **Paso 3: implementar lo mínimo**

```js
// docs/motor/escena.js
export function crearEscena({ dibujar, duracion, alCambiar = () => {} }) {
  let t = 0;
  let estado = 'reposo';

  const pasarA = nuevo => {
    if (nuevo === estado) return;
    estado = nuevo;
    alCambiar(estado);
  };

  const api = {
    get t() { return t; },
    get estado() { return estado; },
    reproducir() { pasarA('reproduciendo'); },
    pausar() { pasarA('pausado'); },
    reiniciar() { t = 0; pasarA('reposo'); dibujar(t); },
    avanzar(dt) {
      if (estado !== 'reproduciendo') return;
      t = Math.min(t + dt, duracion);
      if (t >= duracion) pasarA('pausado');
      dibujar(t);
    },
  };
  return api;
}
```

- [ ] **Paso 4: correr y verificar que pasa**

Ejecutar: `node --test test/escena.test.js`
Esperado: 6 pruebas OK.

- [ ] **Paso 5: commit**

```bash
git add docs/motor/escena.js test/escena.test.js
git commit -m "feat(plataforma): motor de escena con estados y reloj inyectable"
```

---

## Tarea 6: El ensayo y el primer widget, "Las dos sombras"

Acá se ensambla todo con el marcado exacto del diseño.

**Archivos:**
- Crear: `docs/ensayos/tiro-parabolico.html`
- Referencia obligatoria: `plataforma/diseno/Tiro parabolico.dc.html`

**Interfaces:**
- Consume: `crearLienzo` (Tarea 2); `eje`, `traza`, `cuerpo`, `huella` (Tarea 3);
  `crearTiro` (Tarea 4); `crearEscena` (Tarea 5). `vector` queda disponible pero este
  widget no lo usa: entra recién en el plan 2, con el triángulo de $\vec v_0$.

- [ ] **Paso 1: copiar la estructura del diseño**

Abrir `plataforma/diseno/Tiro parabolico.dc.html` y copiar **literalmente**: el
`<head>` con el enlace a Google Fonts, el bloque `<style>` global (que ahora sale de
`base.css`), el kicker, el `<h1>`, la bajada, el `<h2>` de `01 · Dos movimientos, un
reloj`, y toda la `<section>` del widget con sus estilos en línea.

No se reescribe ni se "mejora" ningún valor. Si algo del diseño parece raro, se
respeta igual y se anota aparte.

- [ ] **Paso 2: cablear el canvas al motor**

```html
<script type="module">
import { crearLienzo } from '../motor/lienzo.js';
import { eje, traza, cuerpo, huella } from '../motor/dibujo.js';
import { crearTiro } from '../fisica/tiro.js';
import { crearEscena } from '../motor/escena.js';

const cv = document.getElementById('w1-cv');
const ctx = cv.getContext('2d');
const leer = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();

let tiro = crearTiro({ v0: 24, alfaGrados: 50 });

function medir() {
  const r = cv.getBoundingClientRect();
  const dpr = devicePixelRatio || 1;
  cv.width = r.width * dpr;
  cv.height = r.height * dpr;
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  return crearLienzo({
    ancho: r.width, alto: r.height,
    xMin: -4, xMax: Math.max(tiro.alcance * 1.12, 10),
    yMin: -3, yMax: Math.max(tiro.yMax * 1.5, 8),
  });
}

function dibujar(t) {
  const l = medir();
  ctx.clearRect(0, 0, cv.width, cv.height);
  eje(ctx, l, { color: leer('--rule') });

  const puntos = [];
  for (let s = 0; s <= tiro.tVuelo; s += tiro.tVuelo / 120) puntos.push(tiro.pos(s));
  traza(ctx, l, puntos, { color: leer('--blue-soft'), grosor: 1.5 });

  // Las huellas: una cada 0.2 s sobre cada eje. Las de abajo quedan equiespaciadas;
  // las de la izquierda se juntan cerca del vertice. Eso es todo el widget.
  for (let s = 0; s <= t + 1e-9; s += 0.2) {
    const [x, y] = tiro.pos(s);
    huella(ctx, l, [x, 0], { color: leer('--graph') });
    huella(ctx, l, [0, y], { color: leer('--graph') });
  }

  const [x, y] = tiro.pos(t);
  traza(ctx, l, puntos.filter((_, i) => i / 120 * tiro.tVuelo <= t),
        { color: leer('--blue'), grosor: 2.5 });
  cuerpo(ctx, l, [x, y], { radio: 5, color: leer('--ink') });
  cuerpo(ctx, l, [x, 0], { radio: 3.5, color: leer('--blue') });
  cuerpo(ctx, l, [0, y], { radio: 3.5, color: leer('--blue') });
}

const escena = crearEscena({ dibujar, duracion: tiro.tVuelo });
let ultimo = 0;
function loop(ms) {
  const dt = ultimo ? Math.min((ms - ultimo) / 1000, 0.05) : 0;
  ultimo = ms;
  escena.avanzar(dt);
  requestAnimationFrame(loop);
}
requestAnimationFrame(loop);

document.getElementById('w1-play').onclick = () =>
  escena.estado === 'reproduciendo' ? escena.pausar() : escena.reproducir();
document.getElementById('w1-reset').onclick = () => escena.reiniciar();

for (const [id, salida, fmt, aplica] of [
  ['w1-v0', 'w1-v0-out', v => `${(+v).toFixed(1)} m/s`, v => ({ v0: +v })],
  ['w1-ang', 'w1-ang-out', v => `${v}°`, v => ({ alfaGrados: +v })],
]) {
  const el = document.getElementById(id);
  el.oninput = () => {
    document.getElementById(salida).textContent = fmt(el.value);
    tiro = crearTiro({
      v0: +document.getElementById('w1-v0').value,
      alfaGrados: +document.getElementById('w1-ang').value,
    });
    escena.reiniciar();
  };
}

escena.reiniciar();  // arranca quieto, en un estado representativo
</script>
```

- [ ] **Paso 3: levantar el servidor y mirarlo**

Ejecutar: `python -m http.server 8000 --directory docs`
Abrir: `http://localhost:8000/ensayos/tiro-parabolico.html`

Los módulos ES no funcionan con `file://`, así que el servidor no es opcional.

Verificar a ojo, contra el diseño abierto al lado:

- La franja del widget va a todo el ancho, con fondo `--band` y filete arriba y abajo.
- El texto queda a 680 px y el canvas a 880 px.
- El encabezado tiene las tres partes, incluida la frase de qué mirar.
- Al reproducir, **las huellas de abajo quedan a distancias iguales y las de la
  izquierda se amontonan cerca del punto más alto**. Ése es el fenómeno que el widget
  existe para mostrar: si no se ve, el widget no sirve.
- Nada se mueve solo hasta que se toca Reproducir.

- [ ] **Paso 4: capturar y comparar**

```bash
chrome --headless --disable-gpu --window-size=1400,900 \
  --screenshot=/tmp/tp.png http://localhost:8000/ensayos/tiro-parabolico.html
```

Comparar la captura con el diseño. Cualquier diferencia de color, tamaño o espaciado
es un error de implementación, no una mejora.

- [ ] **Paso 5: commit**

```bash
git add docs/ensayos/tiro-parabolico.html
git commit -m "feat(plataforma): ensayo de tiro parabolico con el widget de las dos sombras"
```

---

## Tarea 7: Portada y publicación

**Archivos:**
- Crear: `docs/index.html`
- Modificar: `README.md`

- [ ] **Paso 1: portada con la tipografía y la grilla del diseño**

Una columna de 680 px con el kicker, un `<h1>`, una bajada y la lista de ensayos.
Los cinco que todavía no existen se listan sin enlace y en `--dim`, para que se vea
qué falta. Reusa `docs/estilos/base.css`; no se define ningún estilo nuevo.

- [ ] **Paso 2: activar GitHub Pages**

En el repositorio: *Settings → Pages → Source: Deploy from a branch → main → /docs*.
El `.nojekyll` de la Tarea 1 evita que Jekyll se coma las carpetas.

- [ ] **Paso 3: verificar que la versión publicada anda**

Abrir `https://pedromvillar.github.io/Fisica/` y después el ensayo. Confirmar que las
tipografías cargan y que el widget responde.

- [ ] **Paso 4: sumar la plataforma al README**

Una fila en la tabla de material de repaso, con el enlace a la versión publicada.

- [ ] **Paso 5: commit**

```bash
git add docs/index.html README.md
git commit -m "feat(plataforma): portada y publicacion en GitHub Pages"
```

---

## Planes siguientes

Cada ensayo restante es un plan propio, porque son independientes entre sí y cada uno
entrega software funcionando. El orden sale del spec.

| Plan | Ensayo | Widgets | Qué agrega al motor |
|---|---|---|---|
| 2 | Tiro parabólico, completo | Galileo, triángulo de $\vec v_0$, con viento | arrastre de un vector, comparación de dos cuerpos |
| 3 | Derivada e integral | secante a tangente, tres paneles, dibujá tu $x(t)$, el área | paneles apilados con cursor compartido, dibujo a mano alzada, derivada numérica, relleno de área |
| 4 | Diagrama de cuerpo aislado | plano inclinado vivo, armá el diagrama, los dos regímenes del roce | bloque rotado, descomposición punteada, superficie rayada, control de selección |
| 5 | Movimiento circular | versores que giran, $a_t$ y $a_n$, ecuaciones al círculo, período | base polar, arco acotado, evaluación de expresiones, línea de tiempo |
| 6 | Energía | barras de energía, montaña rusa, resorte | barras apiladas, perfil de pista, zigzag de resorte |
| 7 | Sistemas acoplados | dos cuerpos con sus diagramas, casos límite | polea y cuerda, diagramas laterales sincronizados |

El plan 3 es el que más motor nuevo necesita y el que más enseña; conviene atacarlo
apenas el molde del plan 2 esté firme.
