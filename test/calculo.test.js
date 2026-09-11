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
