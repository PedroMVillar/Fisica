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

// El canvas se pinta pocas veces y nunca mas. Si las tipografias llegan despues del
// unico pintado, los rotulos quedan en la fuente de respaldo para siempre: por eso
// crearPagina repinta cuando resuelve `fonts.ready`.
test('cuando terminan de cargar las fuentes se repinta todo', async () => {
  // Promesa diferida, no una ya resuelta: asi la asercion de abajo prueba el orden real
  // -- las fuentes todavia no llegaron -- y no apenas que el repintado sea asincronico.
  let cargaron;
  const doc = documentoFalso();
  doc.fonts = { ready: new Promise(r => { cargaron = r; }) };
  const p = crearPagina({ documento: doc });
  let repintados = 0;
  p.registrar({ repintar: () => repintados++ });

  await null;
  assert.equal(repintados, 0, 'no repinta mientras las fuentes no terminaron de cargar');

  cargaron();
  await doc.fonts.ready;
  await null;
  assert.equal(repintados, 1);
});

test('un documento sin fonts (o sin fonts.ready) no rompe crearPagina', () => {
  assert.doesNotThrow(() => crearPagina({ documento: documentoFalso() }));
  const doc = documentoFalso();
  doc.fonts = {};
  assert.doesNotThrow(() => crearPagina({ documento: doc }));
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

// Encuadre cuya relacion de aspecto NO coincide con la del canvas: el alto sale del
// tope de 430 px, asi que la escala la fija y, y en x sobra area util. El lienzo tiene
// que reportar el borde PEDIDO -- `eje` traza hasta ahi, como el axes() del archivo de
// diseno -- y no el estirado. Si alguien vuelve a reportar el estirado, el eje x se
// corre casi 9 unidades (en el ensayo de tiro eso eran 1.05 px).
test('el lienzo reporta el encuadre pedido, no el estirado al area util', () => {
  const p = crearPagina({ documento: documentoFalso() });
  const cv = canvasFalso(800, 400);
  const w = crearWidget({
    pagina: p, canvas: cv, dpr: 1, margen: { L: 0, R: 0, T: 0, B: 0 },
    encuadre: () => ({ xMax: 10, yMax: 10 }),
    dibujar: () => {},
  });
  w.repintar();
  const l = w.lienzo();

  // alto = min(430, 800 * 10/10) = 430  ->  sc = min(800/10, 430/10) = 43, o sea que
  // manda y: en x sobran 800 - 10*43 = 370 px de area util que NO son del encuadre.
  assert.equal(l.xMax, 10);
  assert.equal(l.yMax, 10);
  assert.equal(l.px(l.xMax), 430, 'el borde reportado cae adentro del area util, no en 800');

  // Y el mapeo no se movio: una sola escala para los dos ejes, la que entra.
  assert.equal(l.escala.x, 43);
  assert.equal(l.escala.y, 43);
  assert.equal(l.px(10), 430);
  assert.equal(l.py(10), 0);
});

// Sin pasar la opcion, escalaUniforme tiene que seguir valiendo true: mismo encuadre
// de la prueba de arriba (aspecto que NO coincide con el del canvas), misma escala
// unica para los dos ejes.
test('escalaUniforme por defecto es true: el comportamiento de hoy no cambia', () => {
  const p = crearPagina({ documento: documentoFalso() });
  const cv = canvasFalso(800, 400);
  const w = crearWidget({
    pagina: p, canvas: cv, dpr: 1, margen: { L: 0, R: 0, T: 0, B: 0 },
    encuadre: () => ({ xMax: 10, yMax: 10 }),
    dibujar: () => {},
  });
  w.repintar();
  const l = w.lienzo();
  assert.equal(l.escala.x, l.escala.y);
});

// Con escalaUniforme:false cada eje llena su propia dimension del area util: las dos
// escalas salen distintas cuando los rangos lo piden (aca 10 s de ancho contra 5 m de
// alto), y cada una toca justo el borde opuesto -- px(xMax) en `ancho - margen.R`,
// py(yMax) en `margen.T`.
test('escalaUniforme:false calcula escalas independientes que llenan cada dimension', () => {
  const p = crearPagina({ documento: documentoFalso() });
  const cv = canvasFalso(800, 400);
  const margen = { L: 60, R: 20, T: 30, B: 40 };
  const w = crearWidget({
    pagina: p, canvas: cv, dpr: 1, margen, escalaUniforme: false,
    encuadre: () => ({ xMax: 10, yMax: 5 }),
    dibujar: () => {},
  });
  w.repintar();
  const l = w.lienzo();
  assert.notEqual(l.escala.x, l.escala.y);
  assert.equal(l.px(l.xMax), 800 - margen.R, 'px(xMax) llena hasta el borde derecho del area util');
  assert.equal(l.py(l.yMax), margen.T, 'py(yMax) llena hasta el borde superior del area util');
});

// Con escalaUniforme:false no hay estiramiento que corregir (a diferencia del camino
// uniforme): el lienzo reporta el encuadre pedido exacto, sin desvio.
test('escalaUniforme:false reporta los bordes pedidos, exactos', () => {
  const p = crearPagina({ documento: documentoFalso() });
  const cv = canvasFalso(800, 400);
  const w = crearWidget({
    pagina: p, canvas: cv, dpr: 1, margen: { L: 0, R: 0, T: 0, B: 0 }, escalaUniforme: false,
    encuadre: () => ({ xMin: 1, xMax: 11, yMin: 2, yMax: 7 }),
    dibujar: () => {},
  });
  w.repintar();
  const l = w.lienzo();
  assert.equal(l.xMin, 1);
  assert.equal(l.xMax, 11);
  assert.equal(l.yMin, 2);
  assert.equal(l.yMax, 7);
});

// El alto sale de la proporcion 16:8 del sistema de diseno (ancho/2), pero sigue
// acotado entre 215 y 430 px igual que en el camino uniforme.
test('escalaUniforme:false acota el alto entre 215 y 430 px', () => {
  const p = crearPagina({ documento: documentoFalso() });

  const angosto = canvasFalso(200, 100);
  const wAngosto = crearWidget({
    pagina: p, canvas: angosto, dpr: 1, margen: { L: 0, R: 0, T: 0, B: 0 }, escalaUniforme: false,
    encuadre: () => ({ xMax: 1, yMax: 1 }),
    dibujar: () => {},
  });
  wAngosto.repintar();
  assert.equal(Math.round(parseFloat(angosto.style.height)), 215);

  const ancho = canvasFalso(2000, 100);
  const wAncho = crearWidget({
    pagina: p, canvas: ancho, dpr: 1, margen: { L: 0, R: 0, T: 0, B: 0 }, escalaUniforme: false,
    encuadre: () => ({ xMax: 1, yMax: 1 }),
    dibujar: () => {},
  });
  wAncho.repintar();
  assert.equal(Math.round(parseFloat(ancho.style.height)), 430);
});

// Esta prueba mira que el encuadre se RELEA, no que se reporte sin estirar (eso lo fija
// la de arriba). Por eso afirma solo xMax: con xMax = 10 el aspecto coincide exacto y no
// hay nada estirado, pero con xMax = 40 el alto cae al piso de 215 px y el estirado pasa
// a y, que la prueba no mira.
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
