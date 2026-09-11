import { test } from 'node:test';
import assert from 'node:assert/strict';
import { crearLienzo } from '../docs/motor/lienzo.js';
import { vector, cuerpo, traza, eje } from '../docs/motor/dibujo.js';

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
  cuerpo(c, L, [50, 25], { radio: 4, color: '#16151a' });
  const arco = c.ops.find(o => o[0] === 'arc');
  assert.deepEqual(arco.slice(1, 4), [400, 200, 4]);
});

test('traza recorre todos los puntos', () => {
  const c = ctxFalso();
  traza(c, L, [[0, 0], [50, 25], [100, 0]], { color: '#8e8a80' });
  assert.equal(c.ops.filter(o => o[0] === 'lineTo').length, 2);
});

test('eje traza la horizontal en py(0) y la vertical en px(0), dentro de los limites del lienzo', () => {
  const c = ctxFalso();
  eje(c, L, { color: '#dcd8ce' });
  const moves = c.ops.filter(o => o[0] === 'moveTo');
  const lines = c.ops.filter(o => o[0] === 'lineTo');
  assert.equal(moves.length, 2);
  assert.equal(lines.length, 2);
  assert.deepEqual(moves[0].slice(1), [0, 400]);
  assert.deepEqual(lines[0].slice(1), [800, 400]);
  assert.deepEqual(moves[1].slice(1), [0, 400]);
  assert.deepEqual(lines[1].slice(1), [0, 0]);
});

// --- El color es obligatorio y no tiene valor por defecto ---------------
//
// Un default seria una copia mas de la paleta, escondida en un modulo que no
// sabe que existen los temas: podria desviarse en silencio de
// docs/estilos/base.css y pintaria colores de tema claro sobre una pagina
// oscura. Estas pruebas fijan que omitirlo no dibuje "algo" sino que falle.

for (const [nombre, llamar] of [
  ['vector', (c, opt) => vector(c, L, [0, 0], [50, 0], opt)],
  ['cuerpo', (c, opt) => cuerpo(c, L, [50, 25], { radio: 4, ...opt })],
  ['traza', (c, opt) => traza(c, L, [[0, 0], [50, 25]], opt)],
  ['eje', (c, opt) => eje(c, L, opt)],
]) {
  test(`${nombre} falla si se omite el color`, () => {
    const c = ctxFalso();
    assert.throws(() => llamar(c, undefined), /falta el color/);
    assert.throws(() => llamar(c, {}), /falta el color/);
    assert.deepEqual(c.ops, [], 'tiene que fallar antes de dibujar nada');
  });
}

test('cuerpo deja el arco como trazado actual: no cierra ni reabre el path despues del fill', () => {
  // El ensayo de tiro parabolico dibuja los puntos huecos rellenando con
  // `cuerpo` y contorneando con un ctx.stroke() inmediato, que solo funciona si
  // el arco sigue siendo el trazado actual. Esto fija ese contrato: si alguien
  // agrega un closePath() o un beginPath() al final de `cuerpo`, los puntos
  // huecos se volverian discos sin borde y esta prueba se cae.
  const c = ctxFalso();
  cuerpo(c, L, [50, 25], { radio: 4, color: '#f2f0ea' });
  assert.deepEqual(c.ops.map(o => o[0]), ['beginPath', 'arc', 'fill']);
});
