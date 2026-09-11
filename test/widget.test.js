import { test } from 'node:test';
import assert from 'node:assert/strict';
import { crearPagina } from '../docs/motor/pagina.js';
import { crearWidget } from '../docs/motor/widget.js';

// Documento falso: lo mínimo que pagina.js y widget.js le piden al DOM.
function documentoFalso({ tokens = {} } = {}) {
  const raiz = { atributos: {} };
  return {
    documentElement: raiz,
    _tokens: tokens,
    getComputedStyle: () => ({ getPropertyValue: n => tokens[n] || '' }),
  };
}

function canvasFalso(ancho = 800, alto = 400) {
  const ops = [];
  const ctx = new Proxy({ ops }, {
    get: (o, k) => k in o ? o[k] : (...a) => ops.push([k, ...a]),
    set: (o, k, v) => { o[k] = v; return true; },
  });
  return {
    ops,
    style: {},
    width: 0,
    height: 0,
    getContext: () => ctx,
    getBoundingClientRect: () => ({ width: ancho, height: alto, left: 0, top: 0 }),
    parentElement: { getBoundingClientRect: () => ({ width: ancho }) },
  };
}

test('la paleta se lee una vez y se cachea hasta que se la olvida', () => {
  let lecturas = 0;
  const doc = documentoFalso({ tokens: { '--blue': '#1b4fd4' } });
  doc.getComputedStyle = () => { lecturas++; return { getPropertyValue: n => n === '--blue' ? '#1b4fd4' : '' }; };
  const p = crearPagina({ documento: doc });
  p.paleta(); p.paleta(); p.paleta();
  assert.equal(lecturas, 1);
  p.olvidarPaleta();
  p.paleta();
  assert.equal(lecturas, 2);
});

test('la paleta expone los nueve tokens con nombres en camello', () => {
  const doc = documentoFalso({ tokens: { '--blue-soft': '#8aa3e6' } });
  const p = crearPagina({ documento: doc });
  const pal = p.paleta();
  assert.deepEqual(Object.keys(pal).sort(),
    ['band', 'blue', 'blueSoft', 'dim', 'graph', 'ink', 'paper', 'red', 'rule']);
  assert.equal(pal.blueSoft, '#8aa3e6');
});

test('repintarTodo repinta cada widget registrado, una vez cada uno', () => {
  const doc = documentoFalso();
  const p = crearPagina({ documento: doc });
  const cuenta = { a: 0, b: 0 };
  p.registrar({ repintar: () => cuenta.a++ });
  p.registrar({ repintar: () => cuenta.b++ });
  p.repintarTodo();
  assert.deepEqual(cuenta, { a: 1, b: 1 });
});

test('tocar avisa a los suscriptos una sola vez', () => {
  const p = crearPagina({ documento: documentoFalso() });
  let avisos = 0;
  p.alTocar(() => avisos++);
  p.tocar();
  p.tocar();
  p.tocar();
  assert.equal(avisos, 1);
});

test('el widget escala el canvas por devicePixelRatio y limpia antes de dibujar', () => {
  const p = crearPagina({ documento: documentoFalso() });
  const cv = canvasFalso(800, 400);
  const w = crearWidget({
    pagina: p, canvas: cv, dpr: 2,
    margen: { L: 60, R: 20, T: 30, B: 40 },
    encuadre: () => ({ xMax: 10, yMax: 5 }),
    dibujar: () => {},
  });
  w.repintar();
  assert.equal(cv.width, 1600);
  const nombres = cv.ops.map(o => o[0]);
  assert.ok(nombres.includes('setTransform'));
  assert.ok(nombres.includes('clearRect'));
  assert.ok(nombres.indexOf('clearRect') < nombres.length);
});

test('el lienzo del widget lleva el margen que se le dio', () => {
  const p = crearPagina({ documento: documentoFalso() });
  const cv = canvasFalso(800, 400);
  const margen = { L: 60, R: 20, T: 30, B: 40 };
  const w = crearWidget({
    pagina: p, canvas: cv, dpr: 1, margen,
    encuadre: () => ({ xMax: 10, yMax: 5 }),
    dibujar: () => {},
  });
  w.repintar();
  assert.deepEqual(w.lienzo().margen, margen);
  assert.equal(w.lienzo().px(0), 60);
});

test('el encuadre se vuelve a consultar en cada repintado', () => {
  const p = crearPagina({ documento: documentoFalso() });
  const cv = canvasFalso(800, 400);
  let xMax = 10;
  const w = crearWidget({
    pagina: p, canvas: cv, dpr: 1, margen: { L: 0, R: 0, T: 0, B: 0 },
    encuadre: () => ({ xMax, yMax: 5 }),
    dibujar: () => {},
  });
  w.repintar();
  assert.equal(w.lienzo().xMax, 10);
  xMax = 40;
  w.repintar();
  assert.equal(w.lienzo().xMax, 40);
});

test('un canvas sin ancho no rompe: el widget no dibuja', () => {
  const p = crearPagina({ documento: documentoFalso() });
  const cv = canvasFalso(0, 0);
  let dibujos = 0;
  const w = crearWidget({
    pagina: p, canvas: cv, dpr: 1, margen: { L: 0, R: 0, T: 0, B: 0 },
    encuadre: () => ({ xMax: 10, yMax: 5 }),
    dibujar: () => { dibujos++; },
  });
  w.repintar();
  assert.equal(dibujos, 0);
});

test('crear un widget lo registra en la pagina', () => {
  const p = crearPagina({ documento: documentoFalso() });
  const cv = canvasFalso();
  crearWidget({
    pagina: p, canvas: cv, dpr: 1, margen: { L: 0, R: 0, T: 0, B: 0 },
    encuadre: () => ({ xMax: 1, yMax: 1 }),
    dibujar: () => {},
  });
  assert.equal(p.widgets().length, 1);
});

// --- Cobertura de observar() y progreso() sin DOM real -----------------
//
// Node no tiene ResizeObserver ni addEventListener/onscroll en el global: estas
// pruebas stubean ambos para fijar la superficie de seguridad que once widgets
// mas en la misma pagina necesitan -- observar() no debe lanzar sin
// ResizeObserver, no debe acumular observadores vivos en llamadas repetidas, y
// observa el padre del canvas (el que cambia de tamano), no el canvas.
// progreso() tiene que colgarse de addEventListener('scroll', ...) y no volver
// jamas al viejo `window.onscroll = ...`, que un solo widget que lo reasigne le
// pisa el evento a todos los demas.

function instalarStubResizeObserver() {
  const original = globalThis.ResizeObserver;
  const instancias = [];
  class FalsoResizeObserver {
    constructor(cb) {
      this.cb = cb;
      this.observados = [];
      this.desconectado = false;
      instancias.push(this);
    }
    observe(el) { this.observados.push(el); }
    disconnect() { this.desconectado = true; }
  }
  globalThis.ResizeObserver = FalsoResizeObserver;
  return {
    instancias,
    restaurar() {
      if (original === undefined) delete globalThis.ResizeObserver;
      else globalThis.ResizeObserver = original;
    },
  };
}

test('observar() sin ResizeObserver no lanza', () => {
  const original = globalThis.ResizeObserver;
  try {
    delete globalThis.ResizeObserver;
    const p = crearPagina({ documento: documentoFalso() });
    assert.doesNotThrow(() => p.observar());
  } finally {
    if (original === undefined) delete globalThis.ResizeObserver;
    else globalThis.ResizeObserver = original;
  }
});

test('observar() dos veces no deja dos observadores vivos', () => {
  const stub = instalarStubResizeObserver();
  try {
    const p = crearPagina({ documento: documentoFalso() });
    const cv = canvasFalso();
    p.registrar({ canvas: cv, repintar: () => {} });
    p.observar();
    p.observar();
    assert.equal(stub.instancias.length, 2);
    assert.equal(stub.instancias[0].desconectado, true);
    assert.equal(stub.instancias[1].desconectado, false);
  } finally {
    stub.restaurar();
  }
});

test('observar() observa el padre de cada canvas registrado, no el canvas', () => {
  const stub = instalarStubResizeObserver();
  try {
    const p = crearPagina({ documento: documentoFalso() });
    const cv = canvasFalso();
    p.registrar({ canvas: cv, repintar: () => {} });
    p.observar();
    const [instancia] = stub.instancias;
    assert.equal(instancia.observados.length, 1);
    assert.equal(instancia.observados[0], cv.parentElement);
  } finally {
    stub.restaurar();
  }
});

test('progreso() sin addEventListener no lanza', () => {
  const original = globalThis.addEventListener;
  try {
    delete globalThis.addEventListener;
    const p = crearPagina({ documento: documentoFalso() });
    assert.doesNotThrow(() => p.progreso({ style: {} }));
  } finally {
    if (original === undefined) delete globalThis.addEventListener;
    else globalThis.addEventListener = original;
  }
});

test('progreso() usa addEventListener("scroll", ...) y no toca onscroll', () => {
  const originalAEL = globalThis.addEventListener;
  const originalOnscroll = globalThis.onscroll;
  const eventos = [];
  try {
    globalThis.addEventListener = nombre => eventos.push(nombre);
    globalThis.onscroll = undefined;
    const p = crearPagina({ documento: documentoFalso() });
    p.progreso({ style: {} });
    assert.deepEqual(eventos, ['scroll']);
    assert.equal(globalThis.onscroll, undefined);
  } finally {
    if (originalAEL === undefined) delete globalThis.addEventListener;
    else globalThis.addEventListener = originalAEL;
    if (originalOnscroll === undefined) delete globalThis.onscroll;
    else globalThis.onscroll = originalOnscroll;
  }
});

test('progreso() sin elemento no hace nada y no lanza', () => {
  const p = crearPagina({ documento: documentoFalso() });
  assert.doesNotThrow(() => p.progreso(null));
  assert.doesNotThrow(() => p.progreso(undefined));
});
