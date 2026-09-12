import { test } from 'node:test';
import assert from 'node:assert/strict';
import { crearLienzo } from '../docs/motor/lienzo.js';
import { vector, vectorPx, cuerpo, traza, eje, punteado, texto, curva, acotarFlecha, marcaDeTope, bloque, suelo } from '../docs/motor/dibujo.js';

function ctxFalso() {
  const ops = [];
  const c = { ops, strokeStyle: '', fillStyle: '', lineWidth: 0, font: '', textAlign: '' };
  for (const m of ['beginPath','moveTo','lineTo','stroke','fill','arc','closePath','save','restore','translate','rotate','setLineDash','fillText']) {
    c[m] = (...a) => ops.push([m, ...a]);
  }
  return c;
}

const L = crearLienzo({ ancho: 800, alto: 400, xMin: 0, xMax: 100, yMin: 0, yMax: 50 });

test('vector usa el color que se le pasa', () => {
  const c = ctxFalso();
  vector(c, L, [0, 0], [10, 10], { color: '#c02a24' });
  assert.equal(c.strokeStyle, '#c02a24');
});

test('vector de largo nulo no dibuja nada', () => {
  const c = ctxFalso();
  vector(c, L, [5, 5], [5, 5], { color: '#1b4fd4' });
  assert.equal(c.ops.length, 0);
});

test('cuerpo dibuja un arco cerrado en la posicion', () => {
  const c = ctxFalso();
  cuerpo(c, L, [50, 25], { radio: 4, color: '#16151a' });
  const arco = c.ops.find(o => o[0] === 'arc');
  assert.deepEqual(arco.slice(1, 4), [400, 200, 4]);
});

test('traza recorre todos los puntos', () => {
  const c = ctxFalso();
  traza(c, L, [[0, 0], [50, 25], [100, 0]], { color: '#8e8a80' });
  assert.equal(c.ops.filter(o => o[0] === 'lineTo').length, 2);
});

test('eje traza la horizontal en py(0) y la vertical en px(0), dentro de los limites del lienzo', () => {
  const c = ctxFalso();
  eje(c, L, { color: '#dcd8ce' });
  const moves = c.ops.filter(o => o[0] === 'moveTo');
  const lines = c.ops.filter(o => o[0] === 'lineTo');
  assert.equal(moves.length, 2);
  assert.equal(lines.length, 2);
  assert.deepEqual(moves[0].slice(1), [0, 400]);
  assert.deepEqual(lines[0].slice(1), [800, 400]);
  assert.deepEqual(moves[1].slice(1), [0, 400]);
  assert.deepEqual(lines[1].slice(1), [0, 0]);
});

// --- El color es obligatorio y no tiene valor por defecto ---------------
//
// Un default seria una copia mas de la paleta, escondida en un modulo que no
// sabe que existen los temas: podria desviarse en silencio de
// docs/estilos/base.css y pintaria colores de tema claro sobre una pagina
// oscura. Estas pruebas fijan que omitirlo no dibuje "algo" sino que falle.

for (const [nombre, llamar] of [
  ['vector', (c, opt) => vector(c, L, [0, 0], [50, 0], opt)],
  ['cuerpo', (c, opt) => cuerpo(c, L, [50, 25], { radio: 4, ...opt })],
  ['traza', (c, opt) => traza(c, L, [[0, 0], [50, 25]], opt)],
  ['eje', (c, opt) => eje(c, L, opt)],
]) {
  test(`${nombre} falla si se omite el color`, () => {
    const c = ctxFalso();
    assert.throws(() => llamar(c, undefined), /falta el color/);
    assert.throws(() => llamar(c, {}), /falta el color/);
    assert.deepEqual(c.ops, [], 'tiene que fallar antes de dibujar nada');
  });
}

test('cuerpo deja el arco como trazado actual: no cierra ni reabre el path despues del fill', () => {
  // El ensayo de tiro parabolico dibuja los puntos huecos rellenando con
  // `cuerpo` y contorneando con un ctx.stroke() inmediato, que solo funciona si
  // el arco sigue siendo el trazado actual. Esto fija ese contrato: si alguien
  // agrega un closePath() o un beginPath() al final de `cuerpo`, los puntos
  // huecos se volverian discos sin borde y esta prueba se cae.
  const c = ctxFalso();
  cuerpo(c, L, [50, 25], { radio: 4, color: '#f2f0ea' });
  assert.deepEqual(c.ops.map(o => o[0]), ['beginPath', 'arc', 'fill']);
});

test('vectorPx no dibuja nada si el largo es menor a un pixel', () => {
  const c = ctxFalso();
  vectorPx(c, 10, 10, 10.4, 10, { color: '#000' });
  assert.deepEqual(c.ops, []);
});

test('vectorPx frena el asta antes de la punta, no la corre hasta el extremo', () => {
  const c = ctxFalso();
  vectorPx(c, 0, 0, 100, 0, { color: '#000', punta: 10 });
  const linea = c.ops.find(o => o[0] === 'lineTo');
  // 100 - cos(0) * 10 * 0.85
  assert.ok(Math.abs(linea[1] - 91.5) < 1e-9, `asta hasta ${linea[1]}`);
});

test('vectorPx acota la punta a la mitad del largo', () => {
  const c = ctxFalso();
  vectorPx(c, 0, 0, 6, 0, { color: '#000', punta: 20 });
  const linea = c.ops.find(o => o[0] === 'lineTo');
  // hd = min(20, 6 * 0.5) = 3  ->  6 - 3 * 0.85
  assert.ok(Math.abs(linea[1] - 3.45) < 1e-9, `asta hasta ${linea[1]}`);
});

test('vectorPx pinta la cabeza con fill y la deja cerrada', () => {
  const c = ctxFalso();
  vectorPx(c, 0, 0, 50, 0, { color: '#000' });
  const nombres = c.ops.map(o => o[0]);
  assert.ok(nombres.includes('closePath'));
  assert.ok(nombres.includes('fill'));
});

test('vectorPx aplica los guiones al asta y los limpia despues', () => {
  const c = ctxFalso();
  vectorPx(c, 0, 0, 50, 0, { color: '#000', guiones: [4, 4] });
  const dashes = c.ops.filter(o => o[0] === 'setLineDash').map(o => o[1]);
  assert.deepEqual(dashes[0], [4, 4]);
  assert.deepEqual(dashes.at(-1), []);
});

test('vectorPx dibuja el rotulo cuando se lo pide, y no cuando no', () => {
  const con = ctxFalso();
  vectorPx(con, 0, 0, 50, 0, { color: '#000', rotulo: 'v' });
  const sin = ctxFalso();
  vectorPx(sin, 0, 0, 50, 0, { color: '#000' });
  const textos = con.ops.filter(o => o[0] === 'fillText');
  assert.equal(textos.length, 1);
  assert.equal(textos[0][1], 'v');
  assert.equal(sin.ops.filter(o => o[0] === 'fillText').length, 0);
});

test('vector convierte coordenadas fisicas y delega en vectorPx', () => {
  const l = crearLienzo({ ancho: 100, alto: 100, xMin: 0, xMax: 10, yMin: 0, yMax: 10 });
  const enFisicas = ctxFalso();
  vector(enFisicas, l, [0, 0], [5, 0], { color: '#000' });
  const enPixeles = ctxFalso();
  vectorPx(enPixeles, l.px(0), l.py(0), l.px(5), l.py(0), { color: '#000' });
  assert.deepEqual(enFisicas.ops, enPixeles.ops);
});

test('punteado traza con guiones y los limpia', () => {
  const c = ctxFalso();
  punteado(c, 0, 0, 10, 10, { color: '#000' });
  const dashes = c.ops.filter(o => o[0] === 'setLineDash').map(o => o[1]);
  assert.deepEqual(dashes[0], [2, 4]);
  assert.deepEqual(dashes.at(-1), []);
});

test('texto escribe en mono y respeta la alineacion', () => {
  const c = ctxFalso();
  texto(c, 'hola', 5, 7, { color: '#000', alineacion: 'right' });
  const t = c.ops.find(o => o[0] === 'fillText');
  assert.deepEqual([t[1], t[2], t[3]], ['hola', 5, 7]);
  assert.equal(c.textAlign, 'right');
  assert.ok(/JetBrains Mono/.test(c.font));
});

test('curva muestrea la funcion y traza n+1 puntos', () => {
  const l = crearLienzo({ ancho: 100, alto: 100, xMin: 0, xMax: 10, yMin: 0, yMax: 10 });
  const c = ctxFalso();
  curva(c, l, t => [t, t], 0, 10, { color: '#000', n: 4 });
  assert.equal(c.ops.filter(o => o[0] === 'moveTo').length, 1);
  assert.equal(c.ops.filter(o => o[0] === 'lineTo').length, 4);
});

test('curva arranca en t0 y termina en t1', () => {
  const l = crearLienzo({ ancho: 100, alto: 100, xMin: 0, xMax: 10, yMin: 0, yMax: 10 });
  const c = ctxFalso();
  curva(c, l, t => [t, 0], 2, 8, { color: '#000', n: 6 });
  assert.equal(c.ops.find(o => o[0] === 'moveTo')[1], l.px(2));
  assert.equal(c.ops.filter(o => o[0] === 'lineTo').at(-1)[1], l.px(8));
});

test('curva muestrea en 140 pasos por defecto', () => {
  const l = crearLienzo({ ancho: 100, alto: 100, xMin: 0, xMax: 10, yMin: 0, yMax: 10 });
  const c = ctxFalso();
  curva(c, l, t => [t, t], 0, 10, { color: '#000' });
  assert.equal(c.ops.filter(o => o[0] === 'lineTo').length, 140);
});

test('eje sin etiquetas dibuja solo los dos ejes, como antes', () => {
  const l = crearLienzo({ ancho: 100, alto: 100, xMin: 0, xMax: 10, yMin: 0, yMax: 10 });
  const c = ctxFalso();
  eje(c, l, { color: '#000' });
  assert.equal(c.ops.filter(o => o[0] === 'fillText').length, 0);
});

test('eje con etiquetas escribe las marcas y los dos rotulos', () => {
  const l = crearLienzo({ ancho: 300, alto: 200, xMin: 0, xMax: 10, yMin: 0, yMax: 5 });
  const c = ctxFalso();
  eje(c, l, { color: '#000', colorTexto: '#666', etiquetaX: 'x [m]', etiquetaY: 'y [m]' });
  const textos = c.ops.filter(o => o[0] === 'fillText').map(o => o[1]);
  assert.ok(textos.includes('x [m]'));
  assert.ok(textos.includes('y [m]'));
  // paso de 2 en x (10 / 5) y de 1 en y (5 / 5), sin escribir el cero
  assert.ok(textos.includes('2') && textos.includes('4'));
  assert.ok(!textos.includes('0'));
});

test('eje con yMin negativo rotula marcas negativas y positivas, y no el cero', () => {
  const l = crearLienzo({ ancho: 300, alto: 200, xMin: 0, xMax: 10, yMin: -10, yMax: 10 });
  const c = ctxFalso();
  eje(c, l, { color: '#000', colorTexto: '#666', etiquetaX: 'x [m]', etiquetaY: 'y [m]' });
  const textos = c.ops.filter(o => o[0] === 'fillText').map(o => o[1]);
  // paso de 2 en y (20 / 5): marcas de -10 a 10 salteando el cero.
  assert.ok(textos.includes('-10') && textos.includes('-2'));
  assert.ok(textos.includes('2') && textos.includes('10'));
  assert.ok(!textos.includes('0'));
});

test('eje cuelga la etiqueta del eje x del piso del encuadre, no del cero', () => {
  // Con yMin negativo, py(0) cae en el medio del grafico: si la etiqueta se colgara de
  // ahi, se superpondria con la curva y con los numeros de las marcas. Tiene que
  // quedar debajo de py(yMin), en el margen inferior.
  const l = crearLienzo({
    ancho: 300, alto: 200, xMin: 0, xMax: 10, yMin: -10, yMax: 10,
    margen: { L: 30, R: 10, T: 10, B: 20 },
  });
  const c = ctxFalso();
  eje(c, l, { color: '#000', colorTexto: '#666', etiquetaX: 'x [m]', etiquetaY: 'y [m]' });
  const rotulo = c.ops.find(o => o[0] === 'fillText' && o[1] === 'x [m]');
  assert.ok(rotulo, 'no se escribio la etiqueta del eje x');
  assert.equal(rotulo[3], l.py(l.yMin) + 28);
  assert.ok(rotulo[3] > l.py(0), 'la etiqueta quedo colgada del cero y no del piso');
});

test('eje con marcasX:false omite los numeros del eje horizontal pero conserva los del vertical', () => {
  // xMax=10 (paso 2: marcas 2,4,6,8,10) e yMax=5 (paso 1: marcas 1,2,3,4,5). "6", "8" y
  // "10" son exclusivas de x; "1", "3" y "5" son exclusivas de y -- eligiendolas asi la
  // prueba no se confunde con el "2" y el "4" que comparten los dos ejes.
  const l = crearLienzo({ ancho: 300, alto: 200, xMin: 0, xMax: 10, yMin: 0, yMax: 5 });
  const c = ctxFalso();
  eje(c, l, { color: '#000', colorTexto: '#666', etiquetaY: 'y [m]', marcasX: false });
  const textos = c.ops.filter(o => o[0] === 'fillText').map(o => o[1]);
  assert.ok(!textos.includes('6') && !textos.includes('8') && !textos.includes('10'),
    'no tendria que escribir ningun numero del eje horizontal');
  assert.ok(textos.includes('1') && textos.includes('3') && textos.includes('5'),
    'los numeros del eje vertical tienen que seguir apareciendo');
});

test('eje con marcasY:false omite los numeros del eje vertical pero conserva los del horizontal', () => {
  // Misma pareja de rangos y misma eleccion de marcas exclusivas que la prueba de
  // marcasX:false, para que los dos bucles queden probados por separado y de forma
  // simetrica.
  const l = crearLienzo({ ancho: 300, alto: 200, xMin: 0, xMax: 10, yMin: 0, yMax: 5 });
  const c = ctxFalso();
  eje(c, l, { color: '#000', colorTexto: '#666', etiquetaX: 'x [m]', marcasY: false });
  const textos = c.ops.filter(o => o[0] === 'fillText').map(o => o[1]);
  assert.ok(!textos.includes('1') && !textos.includes('3') && !textos.includes('5'),
    'no tendria que escribir ningun numero del eje vertical');
  assert.ok(textos.includes('6') && textos.includes('8') && textos.includes('10'),
    'los numeros del eje horizontal tienen que seguir apareciendo');
});

test('eje sin colorTexto no escribe nada, aunque pidan marcas y etiquetas', () => {
  const l = crearLienzo({ ancho: 300, alto: 200, xMin: 0, xMax: 10, yMin: 0, yMax: 5 });
  const c = ctxFalso();
  eje(c, l, { color: '#000', etiquetaX: 'x [m]', etiquetaY: 'y [m]', marcasX: true, marcasY: true });
  assert.equal(c.ops.filter(o => o[0] === 'fillText').length, 0);
});

test('eje con yMin = 0 deja la etiqueta del eje x donde estaba', () => {
  // El ensayo de tiro parabolico encuadra siempre desde yMin = 0: su etiqueta no se
  // puede mover ni un pixel.
  const l = crearLienzo({
    ancho: 300, alto: 200, xMin: 0, xMax: 10, yMin: 0, yMax: 10,
    margen: { L: 30, R: 10, T: 10, B: 20 },
  });
  const c = ctxFalso();
  eje(c, l, { color: '#000', colorTexto: '#666', etiquetaX: 'x [m]' });
  const rotulo = c.ops.find(o => o[0] === 'fillText' && o[1] === 'x [m]');
  assert.equal(rotulo[3], l.py(0) + 28);
});

test('acotarFlecha deja pasar una flecha mas corta que el tope', () => {
  const [dx, dy, acotada] = acotarFlecha(30, 40, 100);
  assert.equal(dx, 30);
  assert.equal(dy, 40);
  assert.equal(acotada, false);
});

test('acotarFlecha recorta al tope y avisa, conservando la direccion', () => {
  const [dx, dy, acotada] = acotarFlecha(300, 400, 100);   // largo 500
  assert.ok(Math.abs(Math.hypot(dx, dy) - 100) < 1e-9);
  assert.ok(Math.abs(dx / dy - 300 / 400) < 1e-12, 'la direccion no cambia');
  assert.equal(acotada, true);
});

test('marcaDeTope dibuja dos trazos perpendiculares a la flecha', () => {
  const c = ctxFalso();
  marcaDeTope(c, 100, 100, 50, 0, { color: '#000' });
  // Dos trazos: dos moveTo y dos lineTo, y los dos verticales porque la flecha es
  // horizontal -- misma x en cada par, distinta y.
  const moves = c.ops.filter(o => o[0] === 'moveTo');
  const lines = c.ops.filter(o => o[0] === 'lineTo');
  assert.equal(moves.length, 2);
  assert.equal(lines.length, 2);
  for (let i = 0; i < 2; i++) {
    assert.ok(Math.abs(moves[i][1] - lines[i][1]) < 1e-9, 'trazo vertical');
    assert.ok(Math.abs(moves[i][2] - lines[i][2]) > 1, 'con largo');
  }
});

test('bloque dibuja un rectangulo cerrado de cuatro esquinas', () => {
  const l = crearLienzo({ ancho: 200, alto: 200, xMin: 0, xMax: 10, yMin: 0, yMax: 10 });
  const c = ctxFalso();
  bloque(c, l, [5, 5], { ancho: 2, alto: 1, color: '#000' });
  const nombres = c.ops.map(o => o[0]);
  assert.equal(c.ops.filter(o => o[0] === 'moveTo').length, 1);
  assert.equal(c.ops.filter(o => o[0] === 'lineTo').length, 3);
  assert.ok(nombres.includes('closePath'));
  assert.ok(nombres.includes('fill'));
});

test('el bloque queda centrado en el punto que se le da', () => {
  const l = crearLienzo({ ancho: 200, alto: 200, xMin: 0, xMax: 10, yMin: 0, yMax: 10 });
  const c = ctxFalso();
  bloque(c, l, [5, 5], { ancho: 2, alto: 1, color: '#000' });
  const xs = c.ops.filter(o => o[0] === 'moveTo' || o[0] === 'lineTo').map(o => o[1]);
  const ys = c.ops.filter(o => o[0] === 'moveTo' || o[0] === 'lineTo').map(o => o[2]);
  const cx = (Math.min(...xs) + Math.max(...xs)) / 2;
  const cy = (Math.min(...ys) + Math.max(...ys)) / 2;
  assert.ok(Math.abs(cx - l.p([5, 5])[0]) < 1e-9);
  assert.ok(Math.abs(cy - l.p([5, 5])[1]) < 1e-9);
});

test('con borde, el bloque ademas se contornea', () => {
  const l = crearLienzo({ ancho: 200, alto: 200, xMin: 0, xMax: 10, yMin: 0, yMax: 10 });
  const c = ctxFalso();
  bloque(c, l, [5, 5], { ancho: 2, alto: 1, color: '#000', borde: '#f00' });
  assert.ok(c.ops.some(o => o[0] === 'stroke'));
});

test('suelo dibuja la linea y sus rayitas dentro del rango pedido', () => {
  const l = crearLienzo({ ancho: 400, alto: 200, xMin: -5, xMax: 15, yMin: 0, yMax: 10 });
  const c = ctxFalso();
  suelo(c, l, { color: '#000', desde: 0, hasta: 10 });
  const xs = c.ops.filter(o => o[0] === 'moveTo').map(o => o[1]);
  assert.ok(Math.min(...xs) >= l.p([0, 0])[0] - 1e-9, 'no arranca antes');
  assert.ok(Math.max(...xs) <= l.p([10, 0])[0] + 1e-9, 'no termina despues');
  assert.ok(xs.length > 3, 'hay rayitas, no solo la linea');
});

test('suelo puede ir a una altura distinta de cero', () => {
  const l = crearLienzo({ ancho: 400, alto: 200, xMin: 0, xMax: 10, yMin: 0, yMax: 10 });
  const c = ctxFalso();
  suelo(c, l, { color: '#000', desde: 0, hasta: 10, y: 4 });
  const ys = c.ops.filter(o => o[0] === 'moveTo').map(o => o[2]);
  assert.ok(Math.abs(Math.max(...ys) - l.p([0, 4])[1]) < 1e-9);
});
