import { test } from 'node:test';
import assert from 'node:assert/strict';
import { conectarTema } from '../docs/motor/tema.js';

const raizFalsa = (inicial = {}) => {
  const atributos = { ...inicial };
  return {
    getAttribute: k => (k in atributos ? atributos[k] : null),
    setAttribute: (k, v) => { atributos[k] = v; },
    removeAttribute: k => { delete atributos[k]; },
  };
};
const documentoFalso = raiz => ({ documentElement: raiz });
const botonFalso = () => ({ textContent: '', onclick: null });
const paginaFalsa = () => {
  const llamadas = [];
  return {
    llamadas,
    olvidarPaleta: () => llamadas.push('olvidarPaleta'),
    repintarTodo: () => llamadas.push('repintarTodo'),
  };
};

function conAlmacenamiento(stub, fn) {
  const previo = globalThis.localStorage;
  globalThis.localStorage = stub;
  try {
    fn();
  } finally {
    if (previo === undefined) delete globalThis.localStorage;
    else globalThis.localStorage = previo;
  }
}

test('alterna el atributo data-theme en cada click', () => {
  conAlmacenamiento({ setItem() {}, getItem() {} }, () => {
    const raiz = raizFalsa();
    const boton = botonFalso();
    conectarTema({ pagina: paginaFalsa(), boton, documento: documentoFalso(raiz) });

    assert.equal(raiz.getAttribute('data-theme'), null);
    boton.onclick();
    assert.equal(raiz.getAttribute('data-theme'), 'dark');
    boton.onclick();
    assert.equal(raiz.getAttribute('data-theme'), null);
  });
});

test('persiste la preferencia en localStorage con la clave tp-theme', () => {
  const guardado = {};
  conAlmacenamiento({
    setItem: (k, v) => { guardado[k] = v; },
    getItem: k => guardado[k],
  }, () => {
    const raiz = raizFalsa();
    const boton = botonFalso();
    conectarTema({ pagina: paginaFalsa(), boton, documento: documentoFalso(raiz) });

    boton.onclick();
    assert.equal(guardado['tp-theme'], 'dark');
    boton.onclick();
    assert.equal(guardado['tp-theme'], 'light');
  });
});

test('tolera un almacenamiento bloqueado: el tema cambia igual, sin excepcion', () => {
  conAlmacenamiento({
    setItem() { throw new Error('SecurityError'); },
    getItem() { throw new Error('SecurityError'); },
  }, () => {
    const raiz = raizFalsa();
    const boton = botonFalso();
    const pagina = paginaFalsa();
    conectarTema({ pagina, boton, documento: documentoFalso(raiz) });

    assert.doesNotThrow(() => boton.onclick());
    assert.equal(raiz.getAttribute('data-theme'), 'dark');
    assert.deepEqual(pagina.llamadas, ['olvidarPaleta', 'repintarTodo']);
  });
});

test('tolera que localStorage no exista en absoluto', () => {
  const previo = globalThis.localStorage;
  delete globalThis.localStorage;
  try {
    const raiz = raizFalsa();
    const boton = botonFalso();
    conectarTema({ pagina: paginaFalsa(), boton, documento: documentoFalso(raiz) });
    assert.doesNotThrow(() => boton.onclick());
    assert.equal(raiz.getAttribute('data-theme'), 'dark');
  } finally {
    if (previo === undefined) delete globalThis.localStorage;
    else globalThis.localStorage = previo;
  }
});

test('rotula el boton segun el estado ya aplicado al conectar (sin flash)', () => {
  conAlmacenamiento({ setItem() {}, getItem() {} }, () => {
    const claro = botonFalso();
    conectarTema({ pagina: paginaFalsa(), boton: claro, documento: documentoFalso(raizFalsa()) });
    assert.equal(claro.textContent, 'Oscuro');

    const oscuro = botonFalso();
    conectarTema({
      pagina: paginaFalsa(), boton: oscuro,
      documento: documentoFalso(raizFalsa({ 'data-theme': 'dark' })),
    });
    assert.equal(oscuro.textContent, 'Claro');
  });
});

test('rotula el boton despues de cada click', () => {
  conAlmacenamiento({ setItem() {}, getItem() {} }, () => {
    const raiz = raizFalsa();
    const boton = botonFalso();
    conectarTema({ pagina: paginaFalsa(), boton, documento: documentoFalso(raiz) });

    boton.onclick();
    assert.equal(boton.textContent, 'Claro');
    boton.onclick();
    assert.equal(boton.textContent, 'Oscuro');
  });
});

test('avisa a la pagina para que olvide la paleta cacheada y repinte todo', () => {
  conAlmacenamiento({ setItem() {}, getItem() {} }, () => {
    const pagina = paginaFalsa();
    const boton = botonFalso();
    conectarTema({ pagina, boton, documento: documentoFalso(raizFalsa()) });

    boton.onclick();
    assert.deepEqual(pagina.llamadas, ['olvidarPaleta', 'repintarTodo']);
  });
});
