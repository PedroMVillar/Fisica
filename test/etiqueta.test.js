import { test } from 'node:test';
import assert from 'node:assert/strict';
import { colocarEtiqueta, reiniciarEtiquetas } from '../docs/motor/etiqueta.js';

// Mismo `ctxFalso` que test/dibujo.test.js, mas un `measureText`/`medirTexto` -- las
// pruebas de este archivo necesitan que el falso contexto sepa "cuanto mide" un texto
// para poder verificar que un rotulo entra en el canvas o no pisa a otro. No hace falta
// una metrica real (no se compara contra fuentes de verdad), alcanza con que sea
// proporcional al largo de la cadena y consistente entre llamadas: `colocarEtiqueta`
// usa `ctx.measureText(...).width` para decidir donde cae cada rotulo, y las pruebas
// usan `c.medirTexto(...)` -la misma cuenta- para verificar el resultado con el mismo
// numero que uso el codigo bajo prueba.
const ANCHO_POR_CARACTER = 7;

function ctxFalso() {
  const ops = [];
  const c = { ops, strokeStyle: '', fillStyle: '', lineWidth: 0, font: '', textAlign: '' };
  for (const m of ['beginPath','moveTo','lineTo','stroke','fill','arc','closePath','save','restore','translate','rotate','setLineDash','fillText']) {
    c[m] = (...a) => ops.push([m, ...a]);
  }
  c.measureText = (cadena) => ({ width: cadena.length * ANCHO_POR_CARACTER });
  c.medirTexto = (cadena) => cadena.length * ANCHO_POR_CARACTER;
  return c;
}

test('una etiqueta sola va donde le dicen', () => {
  reiniciarEtiquetas({ ancho: 400, alto: 200 });
  const c = ctxFalso();
  colocarEtiqueta(c, 'v', 100, 100, { dx: 8, dy: -6, color: '#000' });
  const t = c.ops.find(o => o[0] === 'fillText');
  assert.equal(t[2], 108);
  assert.equal(t[3], 94);
});

test('una etiqueta contra el borde derecho entra en el canvas', () => {
  reiniciarEtiquetas({ ancho: 400, alto: 200 });
  const c = ctxFalso();
  colocarEtiqueta(c, 'se alcanzan', 396, 100, { dx: 8, dy: -6, color: '#000' });
  const t = c.ops.find(o => o[0] === 'fillText');
  const ancho = c.medirTexto('se alcanzan');
  assert.ok(t[2] + ancho <= 400, 'no se sale por la derecha');
  assert.ok(t[2] >= 0, 'ni por la izquierda');
});

test('dos etiquetas en el mismo punto no se superponen', () => {
  reiniciarEtiquetas({ ancho: 400, alto: 200 });
  const c = ctxFalso();
  colocarEtiqueta(c, 'auto', 200, 100, { dx: 8, dy: -6, color: '#000' });
  colocarEtiqueta(c, 'camion', 200, 100, { dx: 8, dy: -6, color: '#000' });
  const ts = c.ops.filter(o => o[0] === 'fillText');
  assert.equal(ts.length, 2);
  const [a, b] = ts;
  const altoLinea = 12;
  const seSolapan = Math.abs(a[3] - b[3]) < altoLinea &&
    Math.abs(a[2] - b[2]) < Math.max(c.medirTexto(a[1]), c.medirTexto(b[1]));
  assert.ok(!seSolapan, 'la segunda se corrio');
});

test('cinco etiquetas desde un punto caen las cinco dentro y sin pisarse', () => {
  // Es el peor caso real del sitio: las cuatro fuerzas mas la resultante del
  // widget 1 de cuerpo-aislado, todas naciendo del mismo bloque.
  reiniciarEtiquetas({ ancho: 400, alto: 200 });
  const c = ctxFalso();
  for (const s of ['P', 'N', 'T', 'Q', 'R']) {
    colocarEtiqueta(c, s, 200, 100, { dx: 8, dy: -6, color: '#000' });
  }
  const ts = c.ops.filter(o => o[0] === 'fillText');
  assert.equal(ts.length, 5);
  for (const t of ts) {
    assert.ok(t[2] >= 0 && t[2] + c.medirTexto(t[1]) <= 400, `${t[1]} entra a lo ancho`);
    assert.ok(t[3] >= 0 && t[3] <= 200, `${t[1]} entra a lo alto`);
  }
  for (let i = 0; i < 5; i++) for (let j = i + 1; j < 5; j++) {
    const solapan = Math.abs(ts[i][3] - ts[j][3]) < 12 &&
      Math.abs(ts[i][2] - ts[j][2]) < c.medirTexto(ts[i][1]);
    assert.ok(!solapan, `${ts[i][1]} y ${ts[j][1]} no se pisan`);
  }
});

test('con evitar:false la etiqueta se queda donde le dicen aunque pise', () => {
  // La convergencia de Q sobre P en derivada-integral es el punto del ejercicio.
  reiniciarEtiquetas({ ancho: 400, alto: 200 });
  const c = ctxFalso();
  colocarEtiqueta(c, 'P', 200, 100, { dx: 8, dy: -6, color: '#000' });
  colocarEtiqueta(c, 'Q', 200, 100, { dx: 8, dy: -6, color: '#000', evitar: false });
  const ts = c.ops.filter(o => o[0] === 'fillText');
  assert.equal(ts[0][2], ts[1][2]);
  assert.equal(ts[0][3], ts[1][3]);
});
