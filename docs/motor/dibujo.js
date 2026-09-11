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
// 3. Nada acá toca `setLineDash`, `globalAlpha`, `font` ni las transformadas:
//    lo que el llamador deje puesto es lo que se usa.
//
// De las tres reglas, la 2 está fijada por prueba en test/dibujo.test.js, que
// afirma que `cuerpo` emite exactamente ['beginPath', 'arc', 'fill'] — o sea
// que también fija la regla 1, pero sólo para `cuerpo`. Nadie afirma hoy la
// ausencia de save()/restore() en `vector`, `traza` ni `eje`, y la regla 3 se
// sostiene nada más que porque el contexto falso de las pruebas no tiene
// setLineDash ni font, así que una llamada reventaría la suite por accidente.
// Si alguna de esas reglas pasa a ser load-bearing para un widget nuevo,
// escribile su prueba antes de apoyarte en ella.
//
// `color` es obligatorio en todas las primitivas y no tiene valor por defecto.
// Un default sería una cuarta copia de la paleta —que vive en
// docs/estilos/base.css, copiada del archivo de diseño— escondida en un módulo
// que no sabe que existen los temas: se desviaría en silencio y pintaría
// colores de tema claro sobre una página oscura. El color sale siempre de los
// tokens CSS leídos por el widget.

const PUNTA = 9;

function exigirColor(color, primitiva) {
  if (typeof color !== 'string' || color === '') {
    throw new TypeError(
      `${primitiva}: falta el color. Es obligatorio y sin default: pasalo desde los tokens CSS del widget.`
    );
  }
}

// La firma real de las opciones es { color, grosor }. El rotulo todavia no
// esta implementado: dibujar texto en canvas exige elegir tipografia, cuerpo
// y desplazamiento, y eso se resuelve contra el archivo de diseno del widget
// que lo necesita (el triangulo de v0, plan 2), no aca. Si se pasa `rotulo`
// hoy, se acepta y se ignora sin romper nada; ver prueba en dibujo.test.js.
export function vector(ctx, l, desde, hasta, { color, grosor = 2 } = {}) {
  exigirColor(color, 'vector');
  const [x1, y1] = l.p(desde);
  const [x2, y2] = l.p(hasta);
  const dx = x2 - x1, dy = y2 - y1;
  const largo = Math.hypot(dx, dy);
  if (largo < 1e-9) return;
  ctx.strokeStyle = color;
  ctx.fillStyle = color;
  ctx.lineWidth = grosor;
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.stroke();
  const ux = dx / largo, uy = dy / largo;
  ctx.beginPath();
  ctx.moveTo(x2, y2);
  ctx.lineTo(x2 - ux * PUNTA - uy * PUNTA * 0.4, y2 - uy * PUNTA + ux * PUNTA * 0.4);
  ctx.lineTo(x2 - ux * PUNTA + uy * PUNTA * 0.4, y2 - uy * PUNTA - ux * PUNTA * 0.4);
  ctx.closePath();
  ctx.fill();
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

export function eje(ctx, l, { color } = {}) {
  exigirColor(color, 'eje');
  ctx.strokeStyle = color;
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(l.px(l.xMin), l.py(0));
  ctx.lineTo(l.px(l.xMax), l.py(0));
  ctx.moveTo(l.px(0), l.py(l.yMin));
  ctx.lineTo(l.px(0), l.py(l.yMax));
  ctx.stroke();
}
