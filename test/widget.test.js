import { test } from 'node:test';
import assert from 'node:assert/strict';
import { crearPagina } from '../docs/motor/pagina.js';
import { crearWidget, panelesApilados } from '../docs/motor/widget.js';
import { crearLienzo } from '../docs/motor/lienzo.js';

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

// Hallazgo de revision de la Tarea 18: repintarTodo() corre sin proteccion al cambiar
// de tema, al redimensionar y al resolver `fonts.ready` -- una excepcion en el
// `repintar` de un widget no puede abortar el repintado de los que vienen despues en
// ninguno de esos tres casos.
test('un widget que lanza al repintar no interrumpe a los que vienen despues', () => {
  const doc = documentoFalso();
  const p = crearPagina({ documento: doc });
  const orden = [];
  p.registrar({ repintar: () => orden.push('antes') });
  p.registrar({ repintar: () => { throw new Error('widget roto'); } });
  p.registrar({ repintar: () => orden.push('despues') });
  assert.doesNotThrow(() => p.repintarTodo());
  assert.deepEqual(orden, ['antes', 'despues']);
});

test('el error de un widget roto se deja visible en la consola, no se traga en silencio', () => {
  const doc = documentoFalso();
  const p = crearPagina({ documento: doc });
  const error = new Error('widget roto');
  p.registrar({ repintar: () => { throw error; } });
  const original = console.error;
  const capturados = [];
  console.error = (...args) => capturados.push(args);
  try {
    p.repintarTodo();
  } finally {
    console.error = original;
  }
  assert.deepEqual(capturados, [[error]]);
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

// `repintar` repone el estado del contexto que los ensayos cambian a mano. `dibujar`
// puede lanzar a mitad de camino -- y `repintarTodo` se traga esa excepcion -- asi que
// el reset que el ensayo hace despues de bajar el alpha o poner guiones puede no
// llegar a correr nunca. Sin este reposicion, el canvas quedaria translucido (o
// punteado) en todos los repintados siguientes, sin ningun error visible.
test('cada repintado arranca con globalAlpha en 1 y sin guiones, aunque el anterior haya lanzado', () => {
  const p = crearPagina({ documento: documentoFalso() });
  const cv = canvasFalso(800, 400);
  const ultimoGuion = () => cv.ops.filter(o => o[0] === 'setLineDash').at(-1)?.[1];
  const alEmpezarADibujar = [];
  let lanzar = true;
  const w = crearWidget({
    pagina: p, canvas: cv, dpr: 1,
    margen: { L: 0, R: 0, T: 0, B: 0 },
    encuadre: () => ({ xMax: 10, yMax: 5 }),
    dibujar: ctx => {
      alEmpezarADibujar.push({ alpha: ctx.globalAlpha, guiones: ultimoGuion() });
      // Lo que hace un ensayo de verdad: baja el alpha y pone guiones...
      ctx.globalAlpha = 0.45;
      ctx.setLineDash([3, 5]);
      // ...y revienta antes de llegar a reponerlos.
      if (lanzar) throw new Error('un widget que revienta a mitad de dibujo');
    },
  });

  assert.throws(() => w.repintar(), /revienta/);
  lanzar = false;
  w.repintar();

  assert.equal(alEmpezarADibujar.length, 2);
  for (const [i, estado] of alEmpezarADibujar.entries()) {
    assert.equal(estado.alpha, 1, `el repintado ${i} no arranco opaco`);
    assert.deepEqual(estado.guiones, [], `el repintado ${i} arranco con guiones puestos`);
  }
});

// Tarea 6 le dio `angulo` a crearLienzo, pero crearWidget no lo reenviaba: destructuraba
// solo xMin/xMax/yMin/yMax del resultado de encuadre() y armaba el lienzo con esos
// cuatro, tirando el angulo pedido.
test('crearWidget reenvia el angulo del encuadre al lienzo', () => {
  const p = crearPagina({ documento: documentoFalso() });
  const cv = canvasFalso(800, 400);
  const w = crearWidget({
    pagina: p, canvas: cv, dpr: 1, margen: { L: 0, R: 0, T: 0, B: 0 },
    encuadre: () => ({ xMin: -1, xMax: 1, yMin: -1, yMax: 1, angulo: 0.5 }),
    dibujar: () => {},
  });
  w.repintar();
  assert.equal(w.lienzo().angulo, 0.5);
});

test('sin angulo en el encuadre, el lienzo queda en cero', () => {
  const p = crearPagina({ documento: documentoFalso() });
  const cv = canvasFalso(800, 400);
  const w = crearWidget({
    pagina: p, canvas: cv, dpr: 1, margen: { L: 0, R: 0, T: 0, B: 0 },
    encuadre: () => ({ xMin: -1, xMax: 1, yMin: -1, yMax: 1 }),
    dibujar: () => {},
  });
  w.repintar();
  assert.equal(w.lienzo().angulo, 0);
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

// centrar por defecto es false: mismo encuadre y mismo canvas que la prueba de arriba
// ("el lienzo reporta el encuadre pedido..."), sin pasar `centrar`, tiene que dar el
// mismo apoyo contra el margen izquierdo -px(xMin) cae justo en el margen L, todo el
// sobrante (370 px) queda a la derecha, nada a la izquierda.
test('centrar por defecto es false: el encuadre queda apoyado contra el margen izquierdo, como hoy', () => {
  const p = crearPagina({ documento: documentoFalso() });
  const cv = canvasFalso(800, 400);
  const margen = { L: 0, R: 0, T: 0, B: 0 };
  const w = crearWidget({
    pagina: p, canvas: cv, dpr: 1, margen,
    encuadre: () => ({ xMax: 10, yMax: 10 }),
    dibujar: () => {},
  });
  w.repintar();
  const l = w.lienzo();
  // alto = 430, sc = 43 (igual que la prueba de arriba): el encuadre ocupa 430 de los
  // 800 px de ancho util. Sin centrar, el px(xMin) pega contra el margen izquierdo (0)
  // y los 370 px de sobrante quedan enteros del lado derecho.
  assert.equal(l.px(l.xMin), 0, 'el borde izquierdo del encuadre pega contra el margen izquierdo');
  assert.equal(l.px(l.xMax), 430, 'nada del sobrante (370 px) se reparte a la izquierda');
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

// centrar:true reparte el sobrante de la dimension que no manda en partes iguales
// entre sus dos margenes: mismo encuadre y canvas que las dos pruebas de arriba
// (alto tope 430, sc = 43, sobran 370 px de ancho util), pero ahora el sobrante se
// reparte -185 px a cada lado- en vez de quedar todo a la derecha.
test('centrar:true reparte el sobrante en partes iguales entre los dos margenes', () => {
  const p = crearPagina({ documento: documentoFalso() });
  const cv = canvasFalso(800, 400);
  const margen = { L: 0, R: 0, T: 0, B: 0 };
  const w = crearWidget({
    pagina: p, canvas: cv, dpr: 1, margen, centrar: true,
    encuadre: () => ({ xMax: 10, yMax: 10 }),
    dibujar: () => {},
  });
  w.repintar();
  const l = w.lienzo();

  const aireIzquierda = l.px(l.xMin) - margen.L;
  const aireDerecha = (cv.getBoundingClientRect().width - margen.R) - l.px(l.xMax);
  assert.equal(aireIzquierda, 185, 'la mitad de los 370 px de sobrante queda a la izquierda');
  assert.equal(aireDerecha, 185, 'la otra mitad queda a la derecha');
  assert.equal(aireIzquierda, aireDerecha, 'el sobrante queda repartido en partes iguales');
});

// Con centrar:true las dos escalas siguen siendo la misma (lo que mantiene redondo a
// un circulo) MIENTRAS el sobrante se reparte de verdad -- a diferencia de la prueba
// de arriba (que usa el mismo encuadre que "reparte el sobrante..." y por eso, sola,
// no aportaria nada nuevo), esta usa un canvas ANGOSTO donde el sobrante cae del lado
// vertical (x manda, y sobra): canvas 200x* margen 0, encuadre xMax=10 yMax=2.
// anchoUtil=200 -> sc=min(200/10, altoUtil/2). alto = acotarAlto(200*2/10) =
// acotarAlto(40) = 215 (el piso), altoUtil=215 -> sc=min(20, 107.5)=20 (x manda).
// sobranteY = 215 - 20*2 = 175, sobranteX = 0.
//
// Esto SI discrimina el camino viejo: sin centrar, py(yMin) pega contra el piso del
// area util (alto - margen.B = 215) y py(yMax) queda mas arriba. Con centrar:true el
// sobrante vertical se reparte mitad y mitad, asi que py(yMin) se despega del piso
// tanto como py(yMax) se despega del techo -- y esa igualdad, junto con escala.x ==
// escala.y, es lo que revierte si el reparto se rompe (por ejemplo si una
// implementacion futura centrara estirando un solo eje en vez de correr el margen:
// ahi las escalas dejarian de coincidir).
test('centrar:true reparte el sobrante vertical sin romper la escala uniforme', () => {
  const p = crearPagina({ documento: documentoFalso() });
  const cv = canvasFalso(200, 100);
  const margen = { L: 0, R: 0, T: 0, B: 0 };
  const w = crearWidget({
    pagina: p, canvas: cv, dpr: 1, margen, centrar: true,
    encuadre: () => ({ xMax: 10, yMax: 2 }),
    dibujar: () => {},
  });
  w.repintar();
  const l = w.lienzo();
  const alto = parseFloat(cv.style.height);

  assert.equal(l.escala.x, l.escala.y, 'la escala sigue siendo unica para los dos ejes');
  assert.equal(l.escala.x, 20);

  const aireAbajo = (alto - margen.B) - l.py(l.yMin);
  const aireArriba = l.py(l.yMax) - margen.T;
  assert.equal(aireAbajo, 87.5, 'la mitad de los 175 px de sobrante vertical queda abajo');
  assert.equal(aireArriba, 87.5, 'la otra mitad queda arriba');
  assert.equal(aireAbajo, aireArriba, 'el sobrante vertical tambien se reparte en partes iguales');
});

// OJO: esta prueba, sola, no distingue centrar:true de centrar ausente -- el camino
// SIN centrar ya reporta bordes pedidos exactos (es lo que prueba "el lienzo reporta
// el encuadre pedido..." mas arriba: no hay estirado que corregir en ninguno de los
// dos caminos, centrado o no, porque el mecanismo -absorber el sobrante en el margen-
// nunca toca xMax/yMax). Un widget.js que ignorara `centrar` por completo la pasaria
// igual. Queda como prueba de regresion (si algun dia este camino vuelve a estirar el
// encuadre en vez de correr el margen, esto lo atrapa), no como evidencia de que
// `centrar` este implementado -esa evidencia la dan las dos pruebas de arriba, que
// verifican el reparto en sí.
test('centrar:true reporta los bordes pedidos, exactos', () => {
  const p = crearPagina({ documento: documentoFalso() });
  const cv = canvasFalso(800, 400);
  const w = crearWidget({
    pagina: p, canvas: cv, dpr: 1, margen: { L: 0, R: 0, T: 0, B: 0 }, centrar: true,
    encuadre: () => ({ xMin: 1, xMax: 11, yMin: 2, yMax: 12 }),
    dibujar: () => {},
  });
  w.repintar();
  const l = w.lienzo();
  assert.equal(l.xMin, 1);
  assert.equal(l.xMax, 11);
  assert.equal(l.yMin, 2);
  assert.equal(l.yMax, 12);
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
//
// OJO: esta prueba, sola, no distingue escalaUniforme:false de una implementacion
// ausente -- el camino uniforme YA reporta bordes pedidos exactos (es lo que prueba
// "el lienzo reporta el encuadre pedido..." mas arriba), asi que un widget.js viejo
// que ignorara escalaUniforme por completo la pasaria igual. Queda como prueba de
// regresion de la rama nueva (si algun dia esta rama empieza a estirar, esto lo
// atrapa), no como evidencia de que la rama exista.
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

// Los dos casos de arriba caen tan afuera de [215, 430] que cualquier formula monotona
// -la real (ancho/2), una con /3, o la del camino uniforme basada en el aspecto del
// encuadre- acota igual al mismo piso o techo: no fijan la formula, solo el acotado.
// Este caso usa un ancho que NO se acota (700 -> 350, adentro del rango) para que
// solo ancho/2 lo pase; un "me olvide del /2" o un "es /3" dan otro numero y fallan.
test('escalaUniforme:false: el alto sin acotar sale de ancho/2', () => {
  const p = crearPagina({ documento: documentoFalso() });
  const cv = canvasFalso(700, 100);
  const w = crearWidget({
    pagina: p, canvas: cv, dpr: 1, margen: { L: 0, R: 0, T: 0, B: 0 }, escalaUniforme: false,
    encuadre: () => ({ xMax: 1, yMax: 1 }),
    dibujar: () => {},
  });
  w.repintar();
  assert.equal(Math.round(parseFloat(cv.style.height)), 350);
});

// Sin pasar altoMin/altoMax, siguen siendo 215 y 430 -- los del archivo de diseno.
test('altoMin y altoMax por defecto son 215 y 430', () => {
  const p = crearPagina({ documento: documentoFalso() });

  const angosto = canvasFalso(200, 100);
  const wAngosto = crearWidget({
    pagina: p, canvas: angosto, dpr: 1, margen: { L: 0, R: 0, T: 0, B: 0 },
    encuadre: () => ({ xMax: 1, yMax: 1 }),
    dibujar: () => {},
  });
  wAngosto.repintar();
  assert.equal(Math.round(parseFloat(angosto.style.height)), 215);

  const ancho = canvasFalso(2000, 100);
  const wAncho = crearWidget({
    pagina: p, canvas: ancho, dpr: 1, margen: { L: 0, R: 0, T: 0, B: 0 },
    encuadre: () => ({ xMax: 1, yMax: 1 }),
    dibujar: () => {},
  });
  wAncho.repintar();
  assert.equal(Math.round(parseFloat(ancho.style.height)), 430);
});

// altoMin mas alto que el default se respeta de verdad: un widget que apila paneles
// puede pedir un piso propio en vez de heredar el de un canvas suelto.
test('un altoMin mayor que 215 se respeta', () => {
  const p = crearPagina({ documento: documentoFalso() });
  const cv = canvasFalso(200, 100);
  const w = crearWidget({
    pagina: p, canvas: cv, dpr: 1, margen: { L: 0, R: 0, T: 0, B: 0 }, altoMin: 285,
    encuadre: () => ({ xMax: 1, yMax: 1 }),
    dibujar: () => {},
  });
  w.repintar();
  assert.equal(Math.round(parseFloat(cv.style.height)), 285);
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

// --- panelesApilados: geometria de un widget que apila N paneles verticales -----
//
// `lienzo` es el lienzo EXTERIOR del widget (el que arma crearWidget), con un
// encuadre vertical de `yMax: n` -- una unidad por panel. Estas pruebas construyen
// ese lienzo exterior a mano con crearLienzo, del mismo modo en que lo arma
// crearWidget, para no depender de un canvas ni de crearWidget en las aserciones.

function lienzoExterior({ ancho = 800, alto = 400, n = 3 } = {}) {
  return crearLienzo({
    ancho, alto, margen: { L: 60, R: 20, T: 20, B: 34 },
    xMin: 0, xMax: 6, yMin: 0, yMax: n,
  });
}

test('panelesApilados devuelve tantas franjas como paneles se le piden', () => {
  const l = lienzoExterior({ n: 4 });
  const paneles = [{ yMin: 0, yMax: 1 }, { yMin: 0, yMax: 1 }, { yMin: 0, yMax: 1 }, { yMin: 0, yMax: 1 }];
  const capas = panelesApilados({ lienzo: l, margen: { L: 60, R: 20 }, hueco: 23, paneles });
  assert.equal(capas.length, 4);
});

// Sin superposicion ni huecos entre franjas, y las N cubren el alto util completo:
// del techo del area util del lienzo exterior (l.py(n)) al piso (l.py(0)), sin que
// sobre ni falte espacio. A proposito con CUATRO paneles, no tres: una aritmetica que
// hardcodee "3" en vez de `paneles.length` (facil de escribir sin querer, viniendo de
// los dos widgets que solo apilaban 3) pasaria la prueba de arriba igual -- `.map`
// itera los 4 elementos la pida quien la pida -- pero fallaria esta, porque
// `alturaPanel` saldria calculado para 3 franjas y la cuarta se saldria del piso del
// area util (o, con 3 paneles reales, sobraria un hueco al final que esta prueba con
// n=3 no distinguiria del redondeo).
test('panelesApilados: las franjas no se superponen y cubren el alto util', () => {
  const l = lienzoExterior({ n: 4 });
  const paneles = [{ yMin: 0, yMax: 1 }, { yMin: -1, yMax: 1 }, { yMin: -2, yMax: 2 }, { yMin: -3, yMax: 3 }];
  const capas = panelesApilados({ lienzo: l, margen: { L: 60, R: 20 }, hueco: 23, paneles });

  // assert.ok con una tolerancia de punto flotante, no assert.equal: la aritmetica
  // encadena divisiones y sumas (alturaPanel = .../n, techo = techoStack + i*altura),
  // y eso deja un resto de redondeo de un par de unidades en el ultimo bit (~1e-13)
  // que no tiene nada que ver con que las franjas encajen o no.
  const cerca = (a, b, mensaje) => assert.ok(Math.abs(a - b) < 1e-9, `${mensaje}: ${a} vs ${b}`);

  cerca(capas[0].techo, l.py(4), 'la primera franja arranca en el techo del area util');
  for (let i = 1; i < capas.length; i++) {
    cerca(capas[i].techo, capas[i - 1].techo + capas[i - 1].alturaPanel,
      `la franja ${i} arranca exactamente donde termina la anterior`);
  }
  const ultima = capas[capas.length - 1];
  cerca(ultima.techo + ultima.alturaPanel, l.py(0), 'la ultima franja termina en el piso del area util');
});

test('panelesApilados: cada lienzo reporta el rango vertical de su panel y el horizontal compartido', () => {
  const l = lienzoExterior({ n: 3 });
  const paneles = [{ yMin: 0, yMax: 10 }, { yMin: -12, yMax: 12 }, { yMin: -30, yMax: 30 }];
  const capas = panelesApilados({ lienzo: l, margen: { L: 60, R: 20 }, hueco: 23, paneles });
  capas.forEach(({ lp, panel }, i) => {
    assert.equal(lp.yMin, paneles[i].yMin);
    assert.equal(lp.yMax, paneles[i].yMax);
    assert.equal(lp.xMin, l.xMin, 'el rango horizontal es el del lienzo exterior, compartido por todas las franjas');
    assert.equal(lp.xMax, l.xMax);
    assert.equal(panel, paneles[i], 'el descriptor original vuelve intacto, no una copia');
  });
});

test('panelesApilados: el hueco se aplica al margen superior de cada franja', () => {
  const l = lienzoExterior({ n: 3 });
  const paneles = [{ yMin: 0, yMax: 10 }, { yMin: -12, yMax: 12 }, { yMin: -30, yMax: 30 }];
  const hueco = 23;
  const capas = panelesApilados({ lienzo: l, margen: { L: 60, R: 20 }, hueco, paneles });
  capas.forEach(({ techo, lp }) => {
    assert.equal(lp.margen.T, techo + hueco);
  });
  // Con otro hueco cambia el margen superior en la misma medida: no es un numero que
  // panelesApilados eligio por su cuenta, es el que se le paso.
  const capasOtroHueco = panelesApilados({ lienzo: l, margen: { L: 60, R: 20 }, hueco: 0, paneles });
  capasOtroHueco.forEach(({ techo, lp }) => {
    assert.equal(lp.margen.T, techo);
  });
});

test('panelesApilados: el margen horizontal de cada franja es el que se le paso', () => {
  const l = lienzoExterior({ n: 3 });
  const paneles = [{ yMin: 0, yMax: 10 }, { yMin: -12, yMax: 12 }, { yMin: -30, yMax: 30 }];
  const capas = panelesApilados({ lienzo: l, margen: { L: 62, R: 24 }, hueco: 23, paneles });
  capas.forEach(({ lp }) => {
    assert.equal(lp.margen.L, 62);
    assert.equal(lp.margen.R, 24);
  });
});

test('panelesApilados hereda el rango horizontal del lienzo de afuera', () => {
  const l = crearLienzo({ ancho: 800, alto: 400, xMin: 0, xMax: 10, yMin: 0, yMax: 2,
    margen: { L: 0, R: 0, T: 0, B: 0 } });
  const capas = panelesApilados({
    lienzo: l, margen: { L: 0, R: 0, T: 0, B: 0 }, hueco: 0,
    paneles: [{ yMin: 0, yMax: 1 }, { yMin: -5, yMax: 5 }],
  });
  for (const { lp } of capas) {
    assert.equal(lp.xMin, 0);
    assert.equal(lp.xMax, 10);
  }
});

test('un panel puede pedir su propio rango horizontal', () => {
  const l = crearLienzo({ ancho: 800, alto: 400, xMin: 0, xMax: 10, yMin: 0, yMax: 2,
    margen: { L: 0, R: 0, T: 0, B: 0 } });
  const capas = panelesApilados({
    lienzo: l, margen: { L: 0, R: 0, T: 0, B: 0 }, hueco: 0,
    paneles: [
      { yMin: 0, yMax: 1, xMin: -40, xMax: 60 },   // la ruta, en metros
      { yMin: 0, yMax: 50 },                        // el grafico, en segundos
    ],
  });
  assert.equal(capas[0].lp.xMin, -40);
  assert.equal(capas[0].lp.xMax, 60);
  assert.equal(capas[1].lp.xMin, 0);
  assert.equal(capas[1].lp.xMax, 10);
});
