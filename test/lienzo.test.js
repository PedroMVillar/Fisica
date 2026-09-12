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

test('sin angulo el lienzo se comporta igual que siempre', () => {
  const l = crearLienzo({ ancho: 200, alto: 100, xMin: 0, xMax: 10, yMin: 0, yMax: 5 });
  assert.equal(l.px(0), 0);
  assert.equal(l.px(10), 200);
  assert.equal(l.py(0), 100);
  assert.equal(l.ux(0), 0);
  assert.equal(l.uy(100), 0);
  assert.deepEqual(l.aMarco([1, 0]), [1, 0]);
  assert.deepEqual(l.aMundo([0, 1]), [0, 1]);
});

test('con angulo, avanzar sobre el eje x del marco sube en pantalla', () => {
  // 30 grados: el eje x del marco apunta 30 grados por encima de la horizontal, asi que
  // un punto en (10, 0) del marco tiene que quedar a la derecha y mas arriba del origen.
  const l = crearLienzo({
    ancho: 400, alto: 400, xMin: -10, xMax: 10, yMin: -10, yMax: 10,
    angulo: Math.PI / 6,
  });
  const [x0, y0] = l.p([0, 0]);
  const [x1, y1] = l.p([10, 0]);
  assert.ok(x1 > x0, 'avanza a la derecha');
  assert.ok(y1 < y0, 'y sube, porque en pantalla la y crece hacia abajo');
});

test('ux y uy invierten a p tambien con angulo', () => {
  const l = crearLienzo({
    ancho: 320, alto: 180, xMin: -4, xMax: 12, yMin: -2, yMax: 9,
    margen: { L: 31, R: 17, T: 13, B: 23 }, angulo: 0.37,
  });
  for (const punto of [[-4, -2], [0, 0], [3.7, 4.25], [12, 9]]) {
    const [vx, vy] = l.p(punto);
    assert.ok(Math.abs(l.ux(vx, vy) - punto[0]) < 1e-9, `x vuelve para ${punto}`);
    assert.ok(Math.abs(l.uy(vy, vx) - punto[1]) < 1e-9, `y vuelve para ${punto}`);
  }
});

test('aMarco y aMundo son inversas y conservan el largo', () => {
  const l = crearLienzo({
    ancho: 100, alto: 100, xMin: 0, xMax: 1, yMin: 0, yMax: 1, angulo: 0.8,
  });
  for (const v of [[1, 0], [0, 1], [3, -4]]) {
    const ida = l.aMarco(v);
    const vuelta = l.aMundo(ida);
    assert.ok(Math.abs(Math.hypot(...ida) - Math.hypot(...v)) < 1e-12, 'conserva el largo');
    assert.ok(Math.abs(vuelta[0] - v[0]) < 1e-12, 'vuelve x');
    assert.ok(Math.abs(vuelta[1] - v[1]) < 1e-12, 'vuelve y');
  }
});

test('el peso, que en el mundo apunta abajo, en un marco inclinado tiene dos componentes', () => {
  // Es la descomposicion que resuelve todo plano inclinado, y la razon de ser del marco
  // girado: el peso vale (0, -1) en el mundo y en el marco vale (-sen a, -cos a).
  const alfa = Math.PI / 6;
  const l = crearLienzo({
    ancho: 100, alto: 100, xMin: 0, xMax: 1, yMin: 0, yMax: 1, angulo: alfa,
  });
  const [aLoLargo, perpendicular] = l.aMarco([0, -1]);
  assert.ok(Math.abs(aLoLargo + Math.sin(alfa)) < 1e-12, 'tira hacia abajo del plano');
  assert.ok(Math.abs(perpendicular + Math.cos(alfa)) < 1e-12, 'y aprieta contra el plano');
});
