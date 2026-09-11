import { test } from 'node:test';
import assert from 'node:assert/strict';
import { deslizador, casilla, boton, rotuloReproducir } from '../docs/motor/controles.js';

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
const botonFalso = () => ({
  _manejadores: {},
  addEventListener(ev, fn) { this._manejadores[ev] = fn; },
  disparar(ev) { this._manejadores[ev](); },
});

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

test('el boton avisa al apretar y marca la pagina', () => {
  const b = botonFalso(), p = paginaFalsa();
  const vistos = [];
  boton({ elemento: b, alApretar: () => vistos.push('apretado'), pagina: p });
  b.disparar('click');
  assert.deepEqual(vistos, ['apretado']);
  assert.equal(p.toques(), 1);
});

test('el boton funciona sin pagina', () => {
  const b = botonFalso();
  const vistos = [];
  boton({ elemento: b, alApretar: () => vistos.push('apretado') });
  b.disparar('click');
  assert.deepEqual(vistos, ['apretado']);
});

test('el rotulo del boton dice Reproducir en reposo, aunque el reloj no este en cero', () => {
  // El estado de reposo de los widgets NO es t = 0: es un instante representativo
  // del vuelo. Sin el tercer argumento esto diria "Seguir" al cargar la pagina.
  const b = { textContent: '' };
  rotuloReproducir(b, { estado: 'reposo', t: 1.3, duracion: 3.7 }, true);
  assert.equal(b.textContent, 'Reproducir');
});

test('el rotulo dice Pausar mientras reproduce', () => {
  const b = { textContent: '' };
  rotuloReproducir(b, { estado: 'reproduciendo', t: 3, duracion: 10 }, false);
  assert.equal(b.textContent, 'Pausar');
});

test('el rotulo dice Seguir si esta pausado a mitad de camino', () => {
  const b = { textContent: '' };
  rotuloReproducir(b, { estado: 'pausado', t: 3, duracion: 10 }, false);
  assert.equal(b.textContent, 'Seguir');
});

test('el rotulo dice Seguir tambien al final, como el diseno', () => {
  // El diseno no distingue "pausado a mitad" de "terminado": las dos dicen Seguir,
  // y apretar el boton reinicia desde cero. No se corrige, se copia.
  const b = { textContent: '' };
  rotuloReproducir(b, { estado: 'pausado', t: 10, duracion: 10 }, false);
  assert.equal(b.textContent, 'Seguir');
});

test('el rotulo dice Reproducir si el reloj esta en cero y no se reprodujo nada', () => {
  const b = { textContent: '' };
  rotuloReproducir(b, { estado: 'reposo', t: 0, duracion: 10 }, false);
  assert.equal(b.textContent, 'Reproducir');
});
