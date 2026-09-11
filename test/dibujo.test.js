import { test } from 'node:test';
import assert from 'node:assert/strict';
import { crearLienzo } from '../docs/motor/lienzo.js';
import { vector, cuerpo, traza, eje, huella } from '../docs/motor/dibujo.js';

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

test('vector ignora rotulo sin cambiar lo que dibuja (rotulo aun no implementado)', () => {
  const sinRotulo = ctxFalso();
  vector(sinRotulo, L, [0, 0], [50, 0], { color: '#1b4fd4' });
  const conRotulo = ctxFalso();
  vector(conRotulo, L, [0, 0], [50, 0], { color: '#1b4fd4', rotulo: 'v' });
  assert.deepEqual(conRotulo.ops, sinRotulo.ops);
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

test('huella dibuja un arco chico en la posicion con el color por defecto', () => {
  const c = ctxFalso();
  huella(c, L, [50, 25]);
  const arco = c.ops.find(o => o[0] === 'arc');
  assert.deepEqual(arco.slice(1, 4), [400, 200, 2.5]);
  assert.equal(c.fillStyle, '#8e8a80');
});

test('eje traza la horizontal en py(0) y la vertical en px(0), dentro de los limites del lienzo', () => {
  const c = ctxFalso();
  eje(c, L);
  const moves = c.ops.filter(o => o[0] === 'moveTo');
  const lines = c.ops.filter(o => o[0] === 'lineTo');
  assert.equal(moves.length, 2);
  assert.equal(lines.length, 2);
  assert.deepEqual(moves[0].slice(1), [0, 400]);
  assert.deepEqual(lines[0].slice(1), [800, 400]);
  assert.deepEqual(moves[1].slice(1), [0, 400]);
  assert.deepEqual(lines[1].slice(1), [0, 0]);
});
