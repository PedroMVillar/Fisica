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
