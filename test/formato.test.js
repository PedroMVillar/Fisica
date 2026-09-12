import { test } from 'node:test';
import assert from 'node:assert';
import { num, exp, marca } from '../docs/motor/formato.js';

test('num usa coma y respeta los decimales pedidos', () => {
  assert.equal(num(0.388, 3), '0,388');
  assert.equal(num(574.9, 1), '574,9');
  assert.equal(num(2, 2), '2,00');
  assert.equal(num(-1.5, 1), '-1,5');
});

test('num no deja el cero con signo', () => {
  // La cancelacion de una resultante deja a veces -1e-13, y toFixed lo imprime
  // como "-0,00". Es la lectura que varios widgets usan como prueba de su modelo:
  // tiene que decir cero, no menos cero.
  assert.equal(num(-1e-13, 2), '0,00');
  assert.equal(num(-0, 1), '0,0');
  assert.equal(num(0, 1), '0,0');
});

test('exp separa mantisa y exponente de forma legible', () => {
  // Hoy fuerzas-de-posicion.html imprime "1.0808e-2" crudo en pantalla.
  assert.equal(exp(1.0808e-2, 4), '1,0808 × 10⁻²');
  assert.equal(exp(3.456e8, 3), '3,456 × 10⁸');
  assert.equal(exp(-2.5e-3, 1), '-2,5 × 10⁻³');
});

test('exp trata el exponente cero sin ensuciar', () => {
  assert.equal(exp(1.5, 1), '1,5');
});

test('marca saca los decimales del paso y no deja ceros de mas', () => {
  // Es el comportamiento que `eje()` tiene HOY para paso >= 0.1, y que hay que
  // conservar exactamente: un entero se rotula sin coma decimal.
  assert.equal(marca(-1, 0.5), '-1');
  assert.equal(marca(2, 1), '2');
  assert.equal(marca(0.5, 0.5), '0,5');
  assert.equal(marca(0.25, 0.05), '0,25');
  assert.equal(marca(1.2, 0.2), '1,2');
});

test('marca con paso fino no produce rotulos repetidos', () => {
  // El defecto que este plan viene a cerrar: con paso 0.05, redondear a un decimal
  // daba "0,3" dos veces seguidas.
  const rotulos = [0.30, 0.35, 0.40].map(x => marca(x, 0.05));
  assert.deepEqual(rotulos, ['0,3', '0,35', '0,4']);
  assert.equal(new Set(rotulos).size, 3);
});
