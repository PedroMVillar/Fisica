import { test } from 'node:test';
import assert from 'node:assert/strict';
import { ajustarCirculo } from '../docs/fisica/ajuste.js';

const cerca = (a, b, tol = 1e-6) =>
  assert.ok(Math.abs(a - b) < tol, `${a} != ${b} (tol ${tol})`);

// n puntos evenly repartidos sobre una circunferencia completa: para un numero de
// angulos equiespaciados sobre un periodo entero, sum(cos) = sum(sin) = 0 exacto, asi
// que el centroide cae exactamente en el centro real y el ajuste tiene que devolverlo
// sin ningun error de muestreo.
function puntosCirculo(cx, cy, r, n = 40) {
  const pts = [];
  for (let i = 0; i < n; i++) {
    const theta = (2 * Math.PI * i) / n;
    pts.push([cx + r * Math.cos(theta), cy + r * Math.sin(theta)]);
  }
  return pts;
}

test('circulo exacto centrado en el origen', () => {
  const centro = ajustarCirculo(puntosCirculo(0, 0, 1));
  assert.ok(centro);
  cerca(centro[0], 0);
  cerca(centro[1], 0);
});

test('circulo exacto desplazado del origen', () => {
  const centro = ajustarCirculo(puntosCirculo(3.5, -2.1, 2, 50));
  assert.ok(centro);
  cerca(centro[0], 3.5, 1e-9);
  cerca(centro[1], -2.1, 1e-9);
});

test('un semiarco (media vuelta, no la vuelta completa) tambien da el centro exacto', () => {
  // El ajuste algebraico de Kasa es exacto para cualquier subconjunto de puntos de una
  // circunferencia real, no solo para una vuelta completa: no depende de que las sumas
  // de primer momento se cancelen por simetria.
  const pts = [];
  const n = 30;
  for (let i = 0; i < n; i++) {
    const theta = Math.PI * (i / (n - 1)); // 0 a pi: media vuelta
    pts.push([1 + 2 * Math.cos(theta), -1 + 2 * Math.sin(theta)]);
  }
  const centro = ajustarCirculo(pts);
  assert.ok(centro);
  cerca(centro[0], 1, 1e-6);
  cerca(centro[1], -1, 1e-6);
});

test('una elipse no es un circulo: hay ajuste, pero la distancia al centro varia', () => {
  const pts = [];
  const n = 60;
  for (let i = 0; i < n; i++) {
    const t = i / n;
    pts.push([2 * Math.sin(2 * Math.PI * t), Math.cos(2 * Math.PI * t)]);
  }
  const centro = ajustarCirculo(pts);
  assert.ok(centro, 'una elipse deberia tener un ajuste (no es degenerada)');
  const [cx, cy] = centro;
  const distancias = pts.map(([x, y]) => Math.hypot(x - cx, y - cy));
  const min = Math.min(...distancias), max = Math.max(...distancias);
  assert.ok(max - min > 0.3, `la distancia deberia variar bastante; min=${min} max=${max}`);
});

test('la recta del preset (x = t, y = t) no tiene circulo: null', () => {
  const pts = Array.from({ length: 50 }, (_, i) => {
    const t = i / 49;
    return [t, t];
  });
  assert.equal(ajustarCirculo(pts), null);
});

// El caso que fallaba antes de normalizar: una recta GENERICA, con pendiente y
// ordenada al origen cualesquiera (no la diagonal x=y del preset). Sin normalizar, el
// determinante del sistema sin centrar podia superar el umbral absoluto por el solo
// hecho de que las coordenadas eran grandes, y el ajuste devolvia un centro espurio.
test('una recta GENERICA (no la del preset) tampoco tiene circulo: null', () => {
  const pts = Array.from({ length: 50 }, (_, i) => {
    const t = i / 49;
    return [t, 3 * t + 5];
  });
  assert.equal(ajustarCirculo(pts), null);
});

test('otra recta generica, con pendiente negativa y muy corrida del origen', () => {
  const pts = Array.from({ length: 40 }, (_, i) => {
    const t = -10 + (20 * i) / 39;
    return [t, -0.7 * t + 120];
  });
  assert.equal(ajustarCirculo(pts), null);
});

test('un circulo diminuto (radio 1e-4) no se confunde con degenerado', () => {
  const centro = ajustarCirculo(puntosCirculo(0.5, 0.5, 1e-4, 40));
  assert.ok(centro, 'un circulo perfecto, por chico que sea, tiene que dar un ajuste');
  cerca(centro[0], 0.5, 1e-8);
  cerca(centro[1], 0.5, 1e-8);
});

test('un circulo grande (radio 1e6) tampoco se confunde con degenerado', () => {
  const centro = ajustarCirculo(puntosCirculo(10, -20, 1e6, 40));
  assert.ok(centro);
  cerca(centro[0], 10, 1);
  cerca(centro[1], -20, 1);
});

test('puntos con NaN o Infinito: null, sin excepcion', () => {
  const base = puntosCirculo(0, 0, 1, 10);
  assert.equal(ajustarCirculo([...base, [NaN, 0]]), null);
  assert.equal(ajustarCirculo([...base, [Infinity, 0]]), null);
  assert.equal(ajustarCirculo([...base, [0, -Infinity]]), null);
});

test('todos los puntos iguales (o casi): null, no hay geometria que ajustar', () => {
  const pts = Array.from({ length: 10 }, () => [1, 1]);
  assert.equal(ajustarCirculo(pts), null);
});

test('menos de 3 puntos: null', () => {
  assert.equal(ajustarCirculo([]), null);
  assert.equal(ajustarCirculo([[0, 0]]), null);
  assert.equal(ajustarCirculo([[0, 0], [1, 1]]), null);
});
