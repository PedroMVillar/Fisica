import { test } from 'node:test';
import assert from 'node:assert/strict';
import { deslizador, casilla, rotuloReproducir } from '../docs/motor/controles.js';

const entradaFalsa = (valor, tipo = 'range') => ({
  type: tipo, value: String(valor), checked: valor === true, _manejadores: {},
  addEventListener(ev, fn) { this._manejadores[ev] = fn; },
  disparar(ev, v) {
    if (v !== undefined) { this.value = String(v); this.checked = v === true; }
    this._manejadores[ev]({ target: this });
  },
});
const salidaFalsa = () => ({ textContent: '' });
const paginaFalsa = () => { let n = 0; return { tocar: () => n++, toques: () => n }; };

test('el deslizador formatea su salida y avisa el valor numerico', () => {
  const e = entradaFalsa(24), s = salidaFalsa();
  const vistos = [];
  deslizador({ entrada: e, salida: s, formato: v => v.toFixed(1) + ' m/s', alCambiar: v => vistos.push(v) });
  e.disparar('input', 30);
  assert.equal(s.textContent, '30.0 m/s');
  assert.deepEqual(vistos, [30]);
});

test('el deslizador escribe la salida inicial sin esperar a que lo toquen', () => {
  const e = entradaFalsa(24), s = salidaFalsa();
  deslizador({ entrada: e, salida: s, formato: v => Math.round(v) + '°', alCambiar: () => {} });
  assert.equal(s.textContent, '24°');
});

test('el deslizador marca la pagina como tocada', () => {
  const e = entradaFalsa(1), p = paginaFalsa();
  deslizador({ entrada: e, salida: salidaFalsa(), formato: String, alCambiar: () => {}, pagina: p });
  assert.equal(p.toques(), 0);
  e.disparar('input', 2);
  assert.equal(p.toques(), 1);
});

test('la casilla avisa booleanos', () => {
  const e = entradaFalsa(true, 'checkbox');
  const vistos = [];
  casilla({ entrada: e, alCambiar: v => vistos.push(v) });
  e.disparar('change', false);
  assert.deepEqual(vistos, [false]);
});

test('el rotulo del boton dice Reproducir en reposo', () => {
  const b = { textContent: '' };
  rotuloReproducir(b, { estado: 'reposo', t: 0, duracion: 10 });
  assert.equal(b.textContent, 'Reproducir');
});

test('el rotulo dice Pausar mientras reproduce', () => {
  const b = { textContent: '' };
  rotuloReproducir(b, { estado: 'reproduciendo', t: 3, duracion: 10 });
  assert.equal(b.textContent, 'Pausar');
});

test('el rotulo dice Seguir si esta pausado a mitad de camino', () => {
  const b = { textContent: '' };
  rotuloReproducir(b, { estado: 'pausado', t: 3, duracion: 10 });
  assert.equal(b.textContent, 'Seguir');
});

test('el rotulo vuelve a Reproducir si esta pausado al final', () => {
  const b = { textContent: '' };
  rotuloReproducir(b, { estado: 'pausado', t: 10, duracion: 10 });
  assert.equal(b.textContent, 'Reproducir');
});
