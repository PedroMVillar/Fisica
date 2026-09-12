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

test('pointercancel corta el arrastre igual que pointerup', () => {
  const cv = canvasFalso();
  const vistos = [];
  arrastrable({ canvas: cv, lienzo, alArrastrar: (x, y) => vistos.push([x, y]) });
  cv.disparar('pointerdown', 100, 50);
  cv.disparar('pointercancel', 100, 50);
  cv.disparar('pointermove', 20, 20);
  assert.equal(vistos.length, 1);
});

test('el lienzo se pide de nuevo en cada evento, no se cachea', () => {
  // crearLienzo es pura: si arrastrable() la llamara una sola vez en el setup
  // (en vez de por evento), las cinco pruebas de arriba pasarian igual, porque
  // siempre reciben los mismos literales. Esta prueba usa un lienzo que cambia
  // de mapeo entre eventos -como pasa cuando el widget se repinta a otro ancho-
  // para que un arrastrable() que izara `lienzo()` una sola vez falle aca.
  const cv = canvasFalso();
  const vistos = [];
  let angosto = false;
  const lienzoCambiante = () => crearLienzo({
    ancho: angosto ? 100 : 200, alto: 100, xMin: 0, xMax: 10, yMin: 0, yMax: 5,
  });
  arrastrable({ canvas: cv, lienzo: lienzoCambiante, alArrastrar: (x, y) => vistos.push([x, y]) });
  cv.disparar('pointerdown', 100, 50);
  // ancho 200: ux(100) = 100 / (200/10) = 5
  angosto = true;
  cv.disparar('pointermove', 100, 50);
  // ancho 100: ux(100) = 100 / (100/10) = 10 -- distinto del mapeo viejo
  assert.deepEqual(vistos, [[5, 2.5], [10, 2.5]]);
});

test('con un lienzo inclinado, el punto que llega al callback es el del marco', () => {
  const alfa = Math.PI / 6;
  const l = crearLienzo({
    ancho: 400, alto: 400, xMin: -10, xMax: 10, yMin: -10, yMax: 10, angulo: alfa,
  });
  const esperado = [6, 2];
  const [vx, vy] = l.p(esperado);
  let visto = null;
  const cv = canvasFalso();
  arrastrable({ canvas: cv, lienzo: () => l, alArrastrar: (x, y) => { visto = [x, y]; } });
  cv.disparar('pointerdown', vx, vy);
  assert.ok(Math.abs(visto[0] - esperado[0]) < 1e-6, 'x en el marco');
  assert.ok(Math.abs(visto[1] - esperado[1]) < 1e-6, 'y en el marco');
});
