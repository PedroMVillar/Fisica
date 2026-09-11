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
