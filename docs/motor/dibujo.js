// Primitivas de dibujo sobre un lienzo (motor/lienzo.js).
//
// CONTRATO DE ESTADO DEL CONTEXTO — leer antes de tocar nada acá.
//
// 1. Ninguna primitiva hace save()/restore(). Todas escriben `strokeStyle`,
//    `fillStyle` y/o `lineWidth` sobre el contexto y los dejan escritos: el
//    que llama es el dueño del estado y quien tiene que reponerlo si le
//    importa. Es a propósito —un save/restore por primitiva, con un widget
//    que dibuja decenas por frame, es puro costo—, y el ensayo ya está escrito
//    contando con eso.
// 2. `cuerpo` deja el arco como trazado actual: no hace closePath() ni vuelve
//    a abrir el path después del fill. Los puntos huecos del ensayo son un
//    `cuerpo` relleno con el color de fondo seguido de un ctx.stroke() propio
//    que contornea ese mismo arco. Un beginPath()/closePath() de más al final
//    los convierte en discos sin borde.
// 3. `setLineDash`, `font` y `textAlign` sí se tocan ahora, y cada primitiva
//    los deja en un estado distinto — el que llama no puede asumir que el
//    contexto vuelve como estaba:
//    - `vectorPx`/`vector` dejan `setLineDash([])` puesto (limpian los
//      guiones del asta después de trazarla) pero no tocan `font`/`textAlign`
//      salvo que `rotulo` esté presente, en cuyo caso `texto` los deja como
//      se describe abajo.
//    - `punteado` también limpia `setLineDash` a `[]` al final.
//    - `curva` también limpia `setLineDash` a `[]` al final.
//    - `texto` deja `font` en la tipografía JetBrains Mono con el `px`/`peso`
//      pedidos y `textAlign` en la `alineacion` pedida: ninguno de los dos
//      se repone.
//    - `eje` sin `etiquetaX`/`etiquetaY` no toca ninguno de los tres. Con
//      alguna etiqueta, dibuja marcas y rótulos con `texto` y queda en el
//      estado que haya dejado la última llamada (rótulo de y si hay
//      `etiquetaY`, si no el de x).
//    - `cuerpo` y `traza` no tocan ninguno de los tres.
//
// De las tres reglas, la 2 está fijada por prueba en test/dibujo.test.js, que
// afirma que `cuerpo` emite exactamente ['beginPath', 'arc', 'fill'] — o sea
// que también fija la regla 1, pero sólo para `cuerpo`. Nadie afirma hoy la
// ausencia de save()/restore() en `vector`, `traza` ni `eje`. Si alguna de
// esas reglas pasa a ser load-bearing para un widget nuevo, escribile su
// prueba antes de apoyarte en ella.
//
// `color` es obligatorio en todas las primitivas y no tiene valor por defecto.
// Un default sería una cuarta copia de la paleta —que vive en
// docs/estilos/base.css, copiada del archivo de diseño— escondida en un módulo
// que no sabe que existen los temas: se desviaría en silencio y pintaría
// colores de tema claro sobre una página oscura. El color sale siempre de los
// tokens CSS leídos por el widget.

function exigirColor(color, primitiva) {
  if (typeof color !== 'string' || color === '') {
    throw new TypeError(
      `${primitiva}: falta el color. Es obligatorio y sin default: pasalo desde los tokens CSS del widget.`
    );
  }
}

// La geometría sale literal del `arrow` del diseño
// (docs/plataforma/diseno/Tiro parabolico.dc.html:402-419).
export function vectorPx(ctx, x1, y1, x2, y2, opciones = {}) {
  const { color, grosor = 2, punta = 9, guiones = [],
          rotulo, rdx = 8, rdy = -6, rAlineacion = 'left' } = opciones;
  exigirColor(color, 'vectorPx');
  const dx = x2 - x1, dy = y2 - y1, largo = Math.hypot(dx, dy);
  if (largo < 1) return;
  const hd = Math.min(punta, largo * 0.5);
  const a = Math.atan2(dy, dx);
  ctx.strokeStyle = color;
  ctx.fillStyle = color;
  ctx.lineWidth = grosor;
  ctx.setLineDash(guiones);
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2 - Math.cos(a) * hd * 0.85, y2 - Math.sin(a) * hd * 0.85);
  ctx.stroke();
  ctx.setLineDash([]);
  ctx.beginPath();
  ctx.moveTo(x2, y2);
  ctx.lineTo(x2 - Math.cos(a - 0.42) * hd, y2 - Math.sin(a - 0.42) * hd);
  ctx.lineTo(x2 - Math.cos(a + 0.42) * hd, y2 - Math.sin(a + 0.42) * hd);
  ctx.closePath();
  ctx.fill();
  if (rotulo) texto(ctx, rotulo, x2 + rdx, y2 + rdy, { color, alineacion: rAlineacion });
}

export function vector(ctx, l, desde, hasta, opciones = {}) {
  const [x1, y1] = l.p(desde);
  const [x2, y2] = l.p(hasta);
  vectorPx(ctx, x1, y1, x2, y2, opciones);
}

export function punteado(ctx, x1, y1, x2, y2, { color, guiones = [2, 4], grosor = 1 } = {}) {
  exigirColor(color, 'punteado');
  ctx.strokeStyle = color;
  ctx.lineWidth = grosor;
  ctx.setLineDash(guiones);
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.stroke();
  ctx.setLineDash([]);
}

export function texto(ctx, cadena, x, y, { color, px = 11, peso = 500, alineacion = 'left' } = {}) {
  exigirColor(color, 'texto');
  ctx.font = `${peso} ${px}px "JetBrains Mono", ui-monospace, monospace`;
  ctx.fillStyle = color;
  ctx.textAlign = alineacion;
  ctx.fillText(cadena, x, y);
}

export function curva(ctx, l, f, t0, t1, { color, grosor = 1.6, guiones = [], n = 140 } = {}) {
  exigirColor(color, 'curva');
  ctx.strokeStyle = color;
  ctx.lineWidth = grosor;
  ctx.setLineDash(guiones);
  ctx.beginPath();
  for (let i = 0; i <= n; i++) {
    const t = t0 + (t1 - t0) * i / n;
    const [x, y] = l.p(f(t));
    if (i) ctx.lineTo(x, y); else ctx.moveTo(x, y);
  }
  ctx.stroke();
  ctx.setLineDash([]);
}

export function cuerpo(ctx, l, punto, { radio = 4, color } = {}) {
  exigirColor(color, 'cuerpo');
  const [x, y] = l.p(punto);
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.arc(x, y, radio, 0, Math.PI * 2);
  ctx.fill();
}

export function traza(ctx, l, puntos, { color, grosor = 2 } = {}) {
  exigirColor(color, 'traza');
  if (puntos.length < 2) return;
  ctx.strokeStyle = color;
  ctx.lineWidth = grosor;
  ctx.beginPath();
  const [x0, y0] = l.p(puntos[0]);
  ctx.moveTo(x0, y0);
  for (let i = 1; i < puntos.length; i++) {
    const [x, y] = l.p(puntos[i]);
    ctx.lineTo(x, y);
  }
  ctx.stroke();
}

// El paso de grilla sale del mismo redondeo a 1, 2 o 5 que usa el diseño.
function paso(rango) {
  const crudo = rango / 5;
  const p = Math.pow(10, Math.floor(Math.log10(crudo)));
  const n = crudo / p;
  return (n >= 5 ? 5 : n >= 2 ? 2 : 1) * p;
}

// Las marcas y rótulos son el `axes()` del diseño
// (docs/plataforma/diseno/Tiro parabolico.dc.html:376-401).
export function eje(ctx, l, { color, colorTexto, etiquetaX, etiquetaY } = {}) {
  exigirColor(color, 'eje');
  ctx.strokeStyle = color;
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(l.px(l.xMin), l.py(0));
  ctx.lineTo(l.px(l.xMax), l.py(0));
  ctx.moveTo(l.px(0), l.py(l.yMin));
  ctx.lineTo(l.px(0), l.py(l.yMax));
  ctx.stroke();
  if (!etiquetaX && !etiquetaY) return;
  exigirColor(colorTexto, 'eje (colorTexto)');

  const sx = paso(l.xMax - l.xMin);
  for (let x = Math.ceil(l.xMin / sx) * sx; x <= l.xMax + 1e-6; x += sx) {
    ctx.strokeStyle = color;
    ctx.beginPath();
    ctx.moveTo(l.px(x), l.py(0));
    ctx.lineTo(l.px(x), l.py(0) + 4);
    ctx.stroke();
    // El cero no se rotula: se lee del cruce de los ejes y ahi choca con el de y.
    if (Math.abs(x) > 1e-9) {
      texto(ctx, String(Math.round(x * 10) / 10), l.px(x), l.py(0) + 16,
        { color: colorTexto, px: 10, peso: 400, alineacion: 'center' });
    }
  }
  const sy = paso(l.yMax - l.yMin);
  for (let y = Math.ceil(l.yMin / sy) * sy; y <= l.yMax + 1e-6; y += sy) {
    if (Math.abs(y) < 1e-9) continue;
    ctx.strokeStyle = color;
    ctx.beginPath();
    ctx.moveTo(l.px(0), l.py(y));
    ctx.lineTo(l.px(0) - 4, l.py(y));
    ctx.stroke();
    texto(ctx, String(Math.round(y * 10) / 10), l.px(0) - 8, l.py(y) + 3.5,
      { color: colorTexto, px: 10, peso: 400, alineacion: 'right' });
  }
  if (etiquetaX) {
    texto(ctx, etiquetaX, l.px(l.xMax), l.py(0) + 28,
      { color: colorTexto, px: 10, alineacion: 'right' });
  }
  if (etiquetaY) {
    texto(ctx, etiquetaY, l.px(0) - 34, l.py(l.yMax) - 15,
      { color: colorTexto, px: 10, alineacion: 'left' });
  }
}
