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
// centrado en (0, 1), recorrido en sentido horario desde el punto mas alto: theta0 = pi/2
// y omega0 negativa, porque cos(pi/2 - wt) = sen(wt) y sen(pi/2 - wt) = cos(wt).
const ej14 = () => crearCircular({ R: 1, omega0: -2 * Math.PI, theta0: Math.PI / 2, centro: [0, 1] });

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
  const [ax, ay] = uniforme.aTotalVector(0.3);   // sin fallback: si el metodo no esta, esto rompe
  cerca(vx * ax + vy * ay, 0, 1e-6);
  // Con gamma distinto de cero deja de valer: hay componente a lo largo de v, y el
  // producto escalar NO da cero. Sin esta mitad, la prueba pasaba con cualquier signo
  // de la componente normal.
  const acelerado = ej13();
  const [wx, wy] = acelerado.vel(2);
  const [bx, by] = acelerado.aTotalVector(2);
  assert.ok(Math.abs(wx * bx + wy * by) > 1e-6,
    `con gamma != 0 la velocidad y la aceleracion no pueden ser perpendiculares (dio ${wx * bx + wy * by})`);
  // Y esa componente a lo largo de v es exactamente la tangencial, no otra cosa.
  cerca((wx * bx + wy * by) / Math.hypot(wx, wy), acelerado.aT(2), 1e-9);
});

// La direccion de `aTotalVector` es todo el argumento del widget de aceleraciones: la
// flecha roja apunta HACIA EL CENTRO, no hacia afuera. Pedir solo que a . v sea cero en
// el uniforme no lo comprueba -- eso se cumple con la componente normal en cualquiera
// de los dos sentidos. Aca se fija el signo: la proyeccion sobre r̂ tiene que ser -aN.
test('la componente radial de la aceleracion es -aN: la flecha apunta al centro', () => {
  for (const c of [ej13(), ej14()]) {
    for (const t of [0, 0.3, 1, 2.5]) {
      const [rx, ry] = c.versorR(t);
      const [ax, ay] = c.aTotalVector(t);
      cerca(ax * rx + ay * ry, -c.aN(t), 1e-9);
    }
  }
});

test('la aceleracion total se reconstruye como -aN r̂ + aT θ̂, y su modulo es aTotal', () => {
  const c = ej13();
  for (const t of [0.4, 3]) {
    const [rx, ry] = c.versorR(t);
    const [tx, ty] = c.versorTheta(t);
    const [ax, ay] = c.aTotalVector(t);
    cerca(ax, -c.aN(t) * rx + c.aT(t) * tx, 1e-9);
    cerca(ay, -c.aN(t) * ry + c.aT(t) * ty, 1e-9);
    cerca(Math.hypot(ax, ay), c.aTotal(t), 1e-9);
  }
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

test('sin velocidad angular ni aceleracion angular no hay periodo (no divide por cero)', () => {
  const c = crearCircular({ R: 1, omega0: 0 });
  assert.equal(c.periodo, null);
  assert.equal(c.frecuencia, null);
});

test('vueltasEn no depende de theta0: rota la fase, no la cuenta de vueltas', () => {
  const conFase = crearCircular({ R: 1, omega0: 2 * Math.PI, theta0: 1.7 });
  const sinFase = crearCircular({ R: 1, omega0: 2 * Math.PI, theta0: 0 });
  for (const t of [0, 0.37, 2, 5.5]) cerca(conFase.vueltasEn(t), sinFase.vueltasEn(t));
});
