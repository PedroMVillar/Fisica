import { test } from 'node:test';
import assert from 'node:assert/strict';
import { crearEscena } from '../docs/motor/escena.js';

test('arranca en reposo y en t=0', () => {
  const e = crearEscena({ dibujar() {}, duracion: 3 });
  assert.equal(e.estado, 'reposo');
  assert.equal(e.t, 0);
});

test('no avanza el tiempo mientras no se reproduce', () => {
  const e = crearEscena({ dibujar() {}, duracion: 3 });
  e.avanzar(0.5);
  assert.equal(e.t, 0);
});

test('avanza al reproducir y se frena al pausar', () => {
  const e = crearEscena({ dibujar() {}, duracion: 3 });
  e.reproducir();
  e.avanzar(0.5);
  assert.equal(e.t, 0.5);
  e.pausar();
  e.avanzar(0.5);
  assert.equal(e.t, 0.5);
  assert.equal(e.estado, 'pausado');
});

test('al llegar al final se detiene en la duracion', () => {
  const e = crearEscena({ dibujar() {}, duracion: 3 });
  e.reproducir();
  e.avanzar(10);
  assert.equal(e.t, 3);
  assert.equal(e.estado, 'pausado');
});

test('reiniciar vuelve a reposo en cero', () => {
  const e = crearEscena({ dibujar() {}, duracion: 3 });
  e.reproducir(); e.avanzar(1); e.reiniciar();
  assert.equal(e.t, 0);
  assert.equal(e.estado, 'reposo');
});

test('avisa cada vez que cambia de estado', () => {
  const vistos = [];
  const e = crearEscena({ dibujar() {}, duracion: 3, alCambiar: s => vistos.push(s) });
  e.reproducir(); e.pausar(); e.reiniciar();
  assert.deepEqual(vistos, ['reproduciendo', 'pausado', 'reposo']);
});
