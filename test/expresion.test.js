import { test } from 'node:test';
import assert from 'node:assert/strict';
import { compilar } from '../docs/fisica/expresion.js';

const f = fuente => {
  const r = compilar(fuente);
  assert.ok(r.ok, `no compilo: ${r.error}`);
  return r.f;
};
const cerca = (a, b, tol = 1e-9) =>
  assert.ok(Math.abs(a - b) < tol, `${a} != ${b}`);

test('numeros y la variable t', () => {
  cerca(f('3')(0), 3);
  cerca(f('t')(4.5), 4.5);
  cerca(f('2.5')(0), 2.5);
});

test('las cuatro operaciones con la precedencia de siempre', () => {
  cerca(f('2 + 3 * 4')(0), 14);
  cerca(f('(2 + 3) * 4')(0), 20);
  cerca(f('10 / 4')(0), 2.5);
  cerca(f('10 - 3 - 2')(0), 5);       // asociatividad a izquierda
});

test('la potencia asocia a derecha y gana sobre el producto', () => {
  cerca(f('2 ^ 3 ^ 2')(0), 512);
  cerca(f('2 * 3 ^ 2')(0), 18);
});

test('el menos unario', () => {
  cerca(f('-t')(3), -3);
  cerca(f('-2 ^ 2')(0), -4);          // se aplica despues de la potencia
  cerca(f('3 * -2')(0), -6);
});

test('las constantes', () => {
  cerca(f('pi')(0), Math.PI);
  cerca(f('e')(0), Math.E);
});

test('las funciones, con nombres en castellano', () => {
  cerca(f('sen(0)')(0), 0);
  cerca(f('cos(0)')(0), 1);
  cerca(f('raiz(9)')(0), 3);
  cerca(f('abs(0 - 4)')(0), 4);
  cerca(f('ln(e)')(0), 1);
});

test('el ejercicio 14: x = sen(2 pi t), y = cos(2 pi t) + 1', () => {
  const x = f('sen(2 * pi * t)');
  const y = f('cos(2 * pi * t) + 1');
  cerca(x(0), 0);
  cerca(y(0), 2);
  cerca(x(0.25), 1);
  cerca(y(0.25), 1);
  // Todo punto cae sobre el circulo de radio 1 centrado en (0, 1).
  for (const t of [0.1, 0.37, 0.8]) cerca(Math.hypot(x(t), y(t) - 1), 1);
});

test('un parentesis sin cerrar da error, no una excepcion', () => {
  const r = compilar('sen(2 * t');
  assert.equal(r.ok, false);
  assert.ok(typeof r.error === 'string' && r.error.length > 0);
});

test('una funcion desconocida da error con su nombre adentro', () => {
  const r = compilar('tang(t)');
  assert.equal(r.ok, false);
  assert.ok(r.error.includes('tang'));
});

test('una variable que no es t da error', () => {
  const r = compilar('x + 1');
  assert.equal(r.ok, false);
});

test('el texto vacio da error', () => {
  assert.equal(compilar('').ok, false);
  assert.equal(compilar('   ').ok, false);
});

test('sobra basura al final: tambien es error', () => {
  assert.equal(compilar('2 + 3 )').ok, false);
  assert.equal(compilar('2 3').ok, false);
});

test('no se puede colar codigo: nada de propiedades ni llamadas raras', () => {
  for (const fuente of ['constructor', 't.constructor', 'globalThis', '[].map']) {
    assert.equal(compilar(fuente).ok, false, `${fuente} no deberia compilar`);
  }
});

test('una division por cero da infinito, no una excepcion', () => {
  assert.equal(f('1 / 0')(0), Infinity);
});
