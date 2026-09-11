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
