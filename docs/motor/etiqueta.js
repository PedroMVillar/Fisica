// Un rotulo que no se sale del canvas ni pisa a otro rotulo ya puesto en este cuadro.
//
// El problema que resuelve: `texto()` (docs/motor/dibujo.js) dibuja en el pixel exacto
// que se le pide, sin saber nada del ancho del canvas ni de los otros rotulos del
// mismo dibujo. A 390px eso corta rotulos contra el borde y hace que dos cuerpos que
// se acercan (o cinco flechas que salen del mismo punto, el peor caso real del sitio
// en los widgets de fuerzas de cuerpo-aislado.html) se escriban uno encima del otro.
//
// `colocarEtiqueta` prueba la posicion pedida (`x + dx`, `y + dy`); si se sale del
// canvas, espeja el desplazamiento hacia adentro; si el resultado pisa un rectangulo ya
// colocado EN ESTE CUADRO, prueba ocho posiciones alrededor del punto -arriba, abajo,
// izquierda, derecha y las cuatro diagonales- y se queda con la primera libre. Si
// ninguna esta libre, dibuja igual en la mejor que tenia: un rotulo mal puesto es mejor
// que ninguno.
//
// Evitar colisiones exige memoria entre llamadas -no alcanza con una funcion pura: para
// que el quinto rotulo esquive a los otros cuatro hace falta saber donde cayeron- asi
// que el modulo lleva un registro de los rectangulos ya colocados. `reiniciarEtiquetas`
// lo vacia; la llama `crearWidget` (docs/motor/widget.js) al principio de cada
// repintado, antes de invocar el `dibujar` del widget, asi que ninguna pagina tiene que
// acordarse de hacerlo -y el registro no se pudre con el tiempo porque nunca queda en
// manos de quien dibuja.
//
// Como `texto()`, esta funcion escribe `font`, `fillStyle` y `textAlign` sobre el
// contexto y no los repone -ver el contrato de estado en docs/motor/dibujo.js.
//
// `evitar: false` salta el paso de esquivar colisiones (aunque sigue registrando el
// rectangulo elegido, para que el SIGUIENTE rotulo lo pueda esquivar a el). Existe para
// la unica convergencia intencional del sitio: en derivada-integral.html el rotulo `Q`
// tiene que poder superponerse a `P` a medida que el usuario arrastra Q hacia P y la
// secante se vuelve tangente -esquivarlo ahi rompe la leccion. Ver el comentario en el
// sitio que lo usa.

// Alto de linea usado solo para decidir colisiones (no para medir glifos de verdad):
// dos rotulos cuya diferencia en y es menor que esto se consideran en la misma fila.
const ALTO_LINEA = 12;

let limitesActuales = { ancho: Infinity, alto: Infinity };
let ocupados = [];

export function reiniciarEtiquetas(limites = {}) {
  limitesActuales = { ancho: limites.ancho ?? Infinity, alto: limites.alto ?? Infinity };
  ocupados = [];
}

function pisaAlgo(x, y, ancho) {
  for (const r of ocupados) {
    if (Math.abs(y - r.y) < ALTO_LINEA && Math.abs(x - r.x) < Math.max(ancho, r.ancho)) {
      return true;
    }
  }
  return false;
}

function acotar(v, min, max) {
  return Math.max(min, Math.min(max, v));
}

// Un rotulo pegado pixel a pixel contra el borde se lee peor que uno con un poco de
// aire (se verifico en pantalla con 'sin gravedad' en la-tierra.html, que sin este
// margen quedaba a 0,35px del borde derecho -entraba por la prueba, pero se veia
// pegado). Si el canvas no da ni para el margen de los dos lados, se cae al recorte
// simple sin margen: entrar (aunque sea justo) sigue siendo mejor que no entrar.
const MARGEN_BORDE = 2;

function acotarX(v, ancho, anchoLim) {
  if (anchoLim < ancho) return v;
  const min = 0, max = anchoLim - ancho;
  return max - min > MARGEN_BORDE * 2
    ? acotar(v, min + MARGEN_BORDE, max - MARGEN_BORDE)
    : acotar(v, min, max);
}

function acotarY(v, altoLim) {
  return altoLim > MARGEN_BORDE * 2
    ? acotar(v, MARGEN_BORDE, altoLim - MARGEN_BORDE)
    : acotar(v, 0, altoLim);
}

export function colocarEtiqueta(ctx, cadena, x, y, opciones = {}) {
  const {
    dx = 8, dy = -6, color, px = 11, peso = 500, alineacion = 'left',
    limites = limitesActuales, evitar = true,
  } = opciones;

  ctx.font = `${peso} ${px}px "JetBrains Mono", ui-monospace, monospace`;
  ctx.fillStyle = color;
  ctx.textAlign = 'left';
  const ancho = ctx.measureText(cadena).width;
  const anchoLim = limites.ancho ?? Infinity;
  const altoLim = limites.alto ?? Infinity;

  // El registro y el recorte de borde trabajan siempre sobre el borde IZQUIERDO del
  // texto: si el llamador pidio 'right' o 'center' (asi dibujaban `vectorPx`/`arco`
  // algunos rotulos antes de migrar) convertimos el desplazamiento pedido a esa misma
  // convencion aca, una sola vez.
  let ddx = dx;
  if (alineacion === 'right') ddx -= ancho;
  else if (alineacion === 'center') ddx -= ancho / 2;
  // Cuanto corrio la alineacion el borde izquierdo respecto del `dx` pedido: las
  // posiciones alternativas del paso 2 (abajo) tienen que arrastrar el mismo corrimiento
  // -si no, un rotulo centrado o alineado a la derecha que necesita esquivar cae
  // alineado a la izquierda "por accidente" en cuanto la esquiva lo manda a una
  // alternativa con `cdx = 0` (arriba/abajo), que es exactamente lo que paso con
  // 'camión' en auto-y-camion.html antes de este arreglo (ver t5-comparacion-*.txt).
  const corrimiento = ddx - dx;

  // 1. La posicion pedida, espejada hacia el centro del canvas si se sale por algun
  // lado. Espejar (no solo recortar) conserva el "colgar del lado de afuera de la
  // punta" que tenian los rotulos manuales -el mismo efecto que buscaba a mano el
  // `rAlineacion` de la flecha "neta" en fuerzas-de-posicion.html.
  let fx = x + ddx, fy = y + dy;
  if (fx < 0) fx = x - ddx;
  else if (fx + ancho > anchoLim) fx = x - ddx - ancho;
  if (fy < 0) fy = y - dy;
  else if (fy > altoLim) fy = y - dy;
  // Recorte final de seguridad: por si el espejado tampoco alcanza (un canvas mas
  // angosto que el propio rotulo, o un punto ya pegado al borde opuesto).
  fx = acotarX(fx, ancho, anchoLim);
  fy = acotarY(fy, altoLim);

  // 2. Si pisa un rectangulo ya colocado en este cuadro, probar alrededor del punto
  // pedido -arriba, abajo, izquierda, derecha, diagonales- y quedarse con la primera
  // libre. `evitar: false` salta este paso entero (ver comentario del modulo).
  if (evitar && pisaAlgo(fx, fy, ancho)) {
    const d = Math.hypot(dx, dy) || 10;
    const alternativas = [
      [0, -d], [0, d], [-d, 0], [d, 0],
      [-d, -d], [d, -d], [-d, d], [d, d],
    ];
    for (const [cdx, cdy] of alternativas) {
      let cx = x + cdx + corrimiento, cy = y + cdy;
      cx = acotarX(cx, ancho, anchoLim);
      cy = acotarY(cy, altoLim);
      if (!pisaAlgo(cx, cy, ancho)) { fx = cx; fy = cy; break; }
    }
    // Si ninguna esta libre seguimos con `fx`/`fy` de arriba: un rotulo mal puesto es
    // mejor que ninguno.
  }

  ocupados.push({ x: fx, y: fy, ancho });
  ctx.fillText(cadena, fx, fy);
}
