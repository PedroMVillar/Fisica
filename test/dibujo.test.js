import { test } from 'node:test';
import assert from 'node:assert/strict';
import { crearLienzo } from '../docs/motor/lienzo.js';
import { vector, vectorPx, cuerpo, traza, eje, punteado, texto, curva, acotarFlecha, marcaDeTope, bloque, suelo, arco, componentes } from '../docs/motor/dibujo.js';

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

// --- El ancla del eje: 0 si esta en el encuadre, el borde mas cercano si no ---------
//
// Ruling 20 (revision de la Tarea 15): `eje()` anclaba sus dos ejes en px(0)/py(0) sin
// mirar si 0 caia dentro del encuadre. El panel de la fuerza neta de
// fuerzas-de-posicion.html mide de s=0.10 a s=0.99 -0 no es parte de ese rango- y a
// 1280px eso daba px(0) = -27.2: el eje, sus marcas y su etiqueta de palabra se
// dibujaban fuera del canvas, en silencio. Estas dos pruebas fijan el arreglo en los
// dos sentidos: que un encuadre que SI contiene el 0 no cambia (ancla = px(0)/py(0)
// exactos, ningun otro dominio del sitio se ve afectado), y que uno que NO lo contiene
// ancla en el borde mas cercano, dentro del area util.

test('eje con 0 estrictamente adentro del encuadre: el ancla sigue siendo exactamente px(0)/py(0)', () => {
  // xMin/yMin negativos y xMax/yMax positivos: 0 cae en el interior de los dos rangos,
  // no en un borde -a diferencia de L (arriba), donde xMin=yMin=0 es un caso limite.
  const l2 = crearLienzo({ ancho: 800, alto: 400, xMin: -50, xMax: 50, yMin: -20, yMax: 30 });
  const c = ctxFalso();
  eje(c, l2, { color: '#dcd8ce' });
  const moves = c.ops.filter(o => o[0] === 'moveTo');
  const lines = c.ops.filter(o => o[0] === 'lineTo');
  // Horizontal en py(0), de px(xMin) a px(xMax).
  assert.deepEqual(moves[0].slice(1), [l2.px(l2.xMin), l2.py(0)]);
  assert.deepEqual(lines[0].slice(1), [l2.px(l2.xMax), l2.py(0)]);
  // Vertical en px(0), de py(yMin) a py(yMax).
  assert.deepEqual(moves[1].slice(1), [l2.px(0), l2.py(l2.yMin)]);
  assert.deepEqual(lines[1].slice(1), [l2.px(0), l2.py(l2.yMax)]);
});

test('eje con un dominio horizontal que NO contiene el 0 (como [0.10, 0.99]): el eje y sus marcas caen dentro del area util', () => {
  // Mismo xMin/xMax/margen que el panel 2 del widget 2 de fuerzas-de-posicion.html a
  // 1280px de ancho fisico de canvas (880px), donde se midio el defecto.
  const margen = { L: 62, R: 24, T: 20, B: 34 };
  const l3 = crearLienzo({ ancho: 880, alto: 200, xMin: 0.10, xMax: 0.99, yMin: -12, yMax: 12, margen });
  const c = ctxFalso();
  eje(c, l3, { color: '#dcd8ce', colorTexto: '#6a6760', etiquetaY: 'F neta [mN]' });

  // "Dentro del area util" quiere decir dentro del CANVAS VISIBLE (0..ancho): la
  // etiqueta y los numeros de marca cuelgan a proposito del margen izquierdo -esa es
  // justamente su funcion, en todo widget del sitio que tiene xMin=0- asi que caer
  // ANTES de margen.L (en el hueco reservado para ellos) es correcto; caer en x<0 es
  // el defecto (queda recortado por el borde del canvas, invisible).
  const moves = c.ops.filter(o => o[0] === 'moveTo');
  // moves[1] es el arranque de la vertical (el eje "y"), en x = ancla, y = py(yMin).
  const xEje = moves[1][1];
  assert.ok(xEje >= 0 && xEje <= l3.ancho,
    `el eje vertical cae en x=${xEje}, fuera del canvas [0, ${l3.ancho}]`);

  const textos = c.ops.filter(o => o[0] === 'fillText');
  const rotuloY = textos.find(o => o[1] === 'F neta [mN]');
  assert.ok(rotuloY, 'la etiqueta "F neta [mN]" no se dibujo');
  assert.ok(rotuloY[2] >= 0 && rotuloY[2] <= l3.ancho,
    `la etiqueta "F neta [mN]" arranca en x=${rotuloY[2]}, fuera del canvas [0, ${l3.ancho}]`);

  // Los numeros de las marcas Y (que cuelgan del mismo ancla) tambien tienen que caer
  // dentro del canvas visible.
  const numerosY = textos.filter(o => /^-?\d+$/.test(o[1]) && o[1] !== '');
  assert.ok(numerosY.length > 0, 'no se dibujo ningun numero de marca');
  for (const n of numerosY) {
    assert.ok(n[2] >= 0 && n[2] <= l3.ancho,
      `la marca "${n[1]}" cae en x=${n[2]}, fuera del canvas [0, ${l3.ancho}]`);
  }
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

test('bloque rota las esquinas segun su propio angulo, no el del lienzo', () => {
  // angulo = 30 grados: ni 0 ni multiplo de 90, para que un angulo ignorado en
  // silencio (destructuring que se cae, o cos/sen calculados y nunca aplicados) no
  // pueda pasar por casualidad. Las posiciones esperadas se calculan aca con la
  // formula de rotacion, no llamando a `bloque`: si la funcion ignora `angulo`, las
  // esquinas reales quedan en el rectangulo sin rotar y no coinciden.
  const l = crearLienzo({ ancho: 200, alto: 200, xMin: 0, xMax: 10, yMin: 0, yMax: 10 });
  const c = ctxFalso();
  const angulo = Math.PI / 6;
  bloque(c, l, [5, 5], { ancho: 2, alto: 1, color: '#000', angulo });

  const cos = Math.cos(angulo), sen = Math.sin(angulo);
  const esperadas = [[-1, -1], [1, -1], [1, 1], [-1, 1]].map(([sx, sy]) => {
    const dx = sx * 1, dy = sy * 0.5; // ancho/2, alto/2
    return l.p([5 + dx * cos - dy * sen, 5 + dx * sen + dy * cos]);
  });
  const puntos = c.ops.filter(o => o[0] === 'moveTo' || o[0] === 'lineTo').map(o => [o[1], o[2]]);
  assert.equal(puntos.length, 4);
  for (let i = 0; i < 4; i++) {
    assert.ok(Math.abs(puntos[i][0] - esperadas[i][0]) < 1e-9, `esquina ${i}, x`);
    assert.ok(Math.abs(puntos[i][1] - esperadas[i][1]) < 1e-9, `esquina ${i}, y`);
  }
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

test('el rayado de suelo cae del lado del terreno con escala anisotropa y lienzo inclinado', () => {
  // Caso que se invierte con una construccion que obtiene el lado rotando un cuarto de
  // vuelta la tangente ya calculada en pixeles: escala anisotropa 1:3 (kx=1, ky=3) con
  // el lienzo a -30 grados. El lado correcto se define de forma independiente de la
  // implementacion: es la direccion en la que mapea con `l.p` el paso de un `y` de
  // marco a `y - 1` (hacia adentro del terreno). El rayado tiene que apuntar del mismo
  // lado que esa direccion -- que su producto punto con ella de positivo -- y no del
  // lado contrario, que es lo que pasaba antes de este arreglo (el producto punto daba
  // negativo con estos mismos numeros).
  const l = crearLienzo({
    ancho: 100, alto: 300, xMin: 0, xMax: 100, yMin: 0, yMax: 100, angulo: -Math.PI / 6,
  });
  const c = ctxFalso();
  suelo(c, l, { color: '#000', desde: 0, hasta: 10, y: 0 });
  const moves = c.ops.filter(o => o[0] === 'moveTo');
  const lines = c.ops.filter(o => o[0] === 'lineTo');
  // ops[0] es la linea del suelo en si; la primera rayita es el par de indice 1.
  const [mx, my] = moves[1].slice(1);
  const [lx, ly] = lines[1].slice(1);
  const rayitaX = lx - mx, rayitaY = ly - my;

  const [x0, y0] = l.p([0, 0]);
  const [xAdentro, yAdentro] = l.p([0, -1]);
  const largo = Math.hypot(xAdentro - x0, yAdentro - y0);
  const nx = (xAdentro - x0) / largo, ny = (yAdentro - y0) / largo;

  const dot = rayitaX * nx + rayitaY * ny;
  assert.ok(dot > 0, `el rayado quedo del lado del aire, no del terreno (producto punto ${dot})`);
});

test('arco traza un arco y escribe su rotulo', () => {
  const l = crearLienzo({ ancho: 200, alto: 200, xMin: -5, xMax: 5, yMin: -5, yMax: 5 });
  const c = ctxFalso();
  arco(c, l, [0, 0], { radio: 30, desde: 0, hasta: Math.PI / 3,
    color: '#000', rotulo: 'α', colorTexto: '#666' });
  assert.equal(c.ops.filter(o => o[0] === 'arc').length, 1);
  const t = c.ops.find(o => o[0] === 'fillText');
  assert.equal(t[1], 'α');
});

test('el rotulo del arco cae en la bisectriz, del lado de afuera', () => {
  const l = crearLienzo({ ancho: 200, alto: 200, xMin: -5, xMax: 5, yMin: -5, yMax: 5 });
  const c = ctxFalso();
  arco(c, l, [0, 0], { radio: 30, desde: 0, hasta: Math.PI / 2,
    color: '#000', rotulo: 'α', colorTexto: '#666' });
  const [ox, oy] = l.p([0, 0]);
  const t = c.ops.find(o => o[0] === 'fillText');
  // Bisectriz de 0 a 90 grados: 45. En pantalla la y crece hacia abajo, asi que el
  // rotulo queda a la derecha y arriba del centro.
  assert.ok(t[2] > ox, 'a la derecha');
  assert.ok(t[3] < oy, 'arriba');
  assert.ok(Math.hypot(t[2] - ox, t[3] - oy) > 30, 'afuera del arco');
});

test('arco sin rotulo no escribe nada', () => {
  const l = crearLienzo({ ancho: 200, alto: 200, xMin: -5, xMax: 5, yMin: -5, yMax: 5 });
  const c = ctxFalso();
  arco(c, l, [0, 0], { radio: 30, desde: 0, hasta: 1, color: '#000' });
  assert.equal(c.ops.filter(o => o[0] === 'fillText').length, 0);
});

test('componentes cierra el rectangulo con dos punteadas', () => {
  const l = crearLienzo({ ancho: 200, alto: 200, xMin: 0, xMax: 10, yMin: 0, yMax: 10 });
  const c = ctxFalso();
  componentes(c, l, [2, 2], [6, 5], { color: '#000' });
  // Dos segmentos: cada uno es un moveTo y un lineTo.
  assert.equal(c.ops.filter(o => o[0] === 'moveTo').length, 2);
  assert.equal(c.ops.filter(o => o[0] === 'lineTo').length, 2);
  const dashes = c.ops.filter(o => o[0] === 'setLineDash').map(o => o[1]);
  assert.deepEqual(dashes.at(-1), [], 'limpia los guiones al salir');
});

test('las dos punteadas pasan por las esquinas del rectangulo', () => {
  const l = crearLienzo({ ancho: 200, alto: 200, xMin: 0, xMax: 10, yMin: 0, yMax: 10 });
  const c = ctxFalso();
  componentes(c, l, [2, 2], [6, 5], { color: '#000' });
  const puntos = c.ops.filter(o => o[0] === 'moveTo' || o[0] === 'lineTo')
    .map(o => [o[1], o[2]]);
  const esquinaA = l.p([6, 2]), esquinaB = l.p([2, 5]);
  const cerca = (a, b) => Math.hypot(a[0] - b[0], a[1] - b[1]) < 1e-9;
  assert.ok(puntos.some(q => cerca(q, esquinaA)), 'la esquina de abajo');
  assert.ok(puntos.some(q => cerca(q, esquinaB)), 'la esquina del costado');
});

// --- El sentido del barrido (agregada mas alla de las cinco del brief) --------
//
// La convencion de canvas mide angulo creciente en sentido horario en pantalla (la y
// crece hacia abajo), asi que un angulo fisico (antihorario, creciente hacia +y) se
// dibuja con los signos cambiados: `ctx.arc(ox, oy, radio, -desde, -hasta, ccw)`. El
// bug tipico es fijar `ccw` en `true` siempre: eso funciona mientras `desde < hasta`
// (los cinco casos de arriba), pero cuando el llamador pide el arco al reves --
// `desde` mayor que `hasta`, como el angulo medido desde la vertical del ensayo de
// tiro parabolico, que dibuja `ctx.arc(ox, oy, r, -Math.PI/2, -ang, false)` -- un
// `ccw` fijo en `true` barre la vuelta larga (la de afuera del angulo) en vez del
// arco chico entre las dos semirrectas. La regla correcta es `ccw = desde < hasta`:
// con `desde` mayor, hay que barrer en sentido de angulo de canvas creciente
// (`ccw: false`) para ir directo de una semirrecta a la otra sin dar la vuelta.
test('arco con hasta menor que desde barre directo entre los dos angulos, no la vuelta larga', () => {
  const l = crearLienzo({ ancho: 200, alto: 200, xMin: -5, xMax: 5, yMin: -5, yMax: 5 });
  const c = ctxFalso();
  arco(c, l, [0, 0], { radio: 30, desde: Math.PI / 2, hasta: Math.PI / 3, color: '#000' });
  const a = c.ops.find(o => o[0] === 'arc');
  assert.equal(a[4], -Math.PI / 2, 'angulo inicial en pixeles');
  assert.equal(a[5], -Math.PI / 3, 'angulo final en pixeles');
  assert.equal(a[6], false, 'con desde > hasta hay que barrer sin dar la vuelta larga');
});
