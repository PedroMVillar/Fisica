// test/tokens.test.js
//
// La paleta tiene una sola fuente de verdad: el bloque `:root{...}` del archivo
// de diseno, que el dueno del proyecto escribio a mano.
// `docs/estilos/base.css` lo copia byte a byte. Estas pruebas leen LOS DOS
// archivos y comparan token a token, asi que si el diseno cambia un hex, la
// rama se entera: la comparacion se cae sola.
//
// La tercera prueba conserva los literales como inventario de la paleta que
// esta rama dio por buena. No es redundante con las dos primeras: si manana
// alguien cambia el diseno *y* base.css en el mismo commit, las comparaciones
// seguirian verdes y solo esta prueba obligaria a mirar el cambio de frente.
// Se afirma contra el diseno, no contra base.css, porque el diseno es la
// autoridad.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const CSS = readFileSync('docs/estilos/base.css', 'utf8');
const DISENO = readFileSync('docs/plataforma/diseno/Tiro parabolico.dc.html', 'utf8');

const CLARO = ':root{';
const OSCURO = ':root[data-theme="dark"]{';

function tokens(fuente, nombreFuente, selector) {
  const i = fuente.indexOf(selector);
  assert.ok(i >= 0, `falta el selector ${selector} en ${nombreFuente}`);
  const bloque = fuente.slice(i, fuente.indexOf('}', i));
  const encontrados = Object.fromEntries(
    [...bloque.matchAll(/--([a-z-]+)\s*:\s*(#[0-9a-f]{6})/gi)]
      .map(m => [m[1], m[2].toLowerCase()])
  );
  assert.ok(
    Object.keys(encontrados).length > 0,
    `el bloque ${selector} de ${nombreFuente} no trajo ningun token: el lector quedo desalineado`
  );
  return encontrados;
}

const deBase = selector => tokens(CSS, 'docs/estilos/base.css', selector);
const deDiseno = selector => tokens(DISENO, 'el archivo de diseno', selector);

test('el tema claro de base.css es, token a token, el del archivo de diseño', () => {
  assert.deepEqual(deBase(CLARO), deDiseno(CLARO));
});

test('el tema oscuro de base.css es, token a token, el del archivo de diseño', () => {
  assert.deepEqual(deBase(OSCURO), deDiseno(OSCURO));
});

test('la paleta del diseño sigue siendo la que esta rama dio por buena', () => {
  assert.deepEqual(deDiseno(CLARO), {
    paper: '#fbfaf7', band: '#f2f0ea', ink: '#16151a', dim: '#6a6760',
    rule: '#dcd8ce', blue: '#1b4fd4', 'blue-soft': '#8aa3e6',
    red: '#c02a24', graph: '#8e8a80',
  });
  assert.deepEqual(deDiseno(OSCURO), {
    paper: '#131316', band: '#191a1e', ink: '#eceae4', dim: '#948f86',
    rule: '#2e2f35', blue: '#7aa2ff', 'blue-soft': '#3f5694',
    red: '#ef5f52', graph: '#6f6c66',
  });
});
