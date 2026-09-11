// test/tokens.test.js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const css = readFileSync('docs/estilos/base.css', 'utf8');

function tokens(selector) {
  const i = css.indexOf(selector);
  assert.ok(i >= 0, `falta el selector ${selector}`);
  const bloque = css.slice(i, css.indexOf('}', i));
  return Object.fromEntries(
    [...bloque.matchAll(/--([a-z-]+)\s*:\s*(#[0-9a-f]{6})/gi)]
      .map(m => [m[1], m[2].toLowerCase()])
  );
}

test('tokens del tema claro, exactos al diseño', () => {
  assert.deepEqual(tokens(':root{'), {
    paper: '#fbfaf7', band: '#f2f0ea', ink: '#16151a', dim: '#6a6760',
    rule: '#dcd8ce', blue: '#1b4fd4', 'blue-soft': '#8aa3e6',
    red: '#c02a24', graph: '#8e8a80',
  });
});

test('tokens del tema oscuro, exactos al diseño', () => {
  assert.deepEqual(tokens(':root[data-theme="dark"]{'), {
    paper: '#131316', band: '#191a1e', ink: '#eceae4', dim: '#948f86',
    rule: '#2e2f35', blue: '#7aa2ff', 'blue-soft': '#3f5694',
    red: '#ef5f52', graph: '#6f6c66',
  });
});
