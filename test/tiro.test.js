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
  const t = crearTiro({ v0: 24, alfaGrados: 30, g: 10 });
  cerca(t.tMax, 1.2, 0.01);
  cerca(t.yMax, 7.2, 0.05);
});

test('ejercicio 15 con viento: a_x = -2 acorta el alcance a 44.1 m', () => {
  const t = crearTiro({ v0: 24, alfaGrados: 30, ax: -2, g: 10 });
  cerca(t.pos(2.4)[0], 44.1, 0.1);
});

test('el eje y no se entera del viento', () => {
  const sin = crearTiro({ v0: 24, alfaGrados: 30, g: 10 });
  const con = crearTiro({ v0: 24, alfaGrados: 30, ax: -2, g: 10 });
  cerca(con.tVuelo, sin.tVuelo, 1e-9);
  cerca(con.yMax, sin.yMax, 1e-9);
});

test('en el punto mas alto la velocidad vertical se anula pero la total no', () => {
  const t = crearTiro({ v0: 24, alfaGrados: 30, g: 10 });
  const [vx, vy] = t.vel(t.tMax);
  cerca(vy, 0, 1e-9);
  cerca(vx, 24 * Math.cos(Math.PI / 6), 1e-9);
});
