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
//      salvo que `rotulo` esté presente, en cuyo caso `colocarEtiqueta`
//      (motor/etiqueta.js) los deja como se describe abajo -- `textAlign`
//      siempre en `'left'`, sea cual sea la `rAlineacion` pedida (ver el
//      comentario de `colocarEtiqueta`).
//    - `punteado` también limpia `setLineDash` a `[]` al final.
//    - `curva` también limpia `setLineDash` a `[]` al final.
//    - `texto` deja `font` en la tipografía JetBrains Mono con el `px`/`peso`
//      pedidos y `textAlign` en la `alineacion` pedida: ninguno de los dos
//      se repone.
//    - `eje` sin `etiquetaX`/`etiquetaY` no toca ninguno de los tres. Con
//      alguna etiqueta, dibuja marcas y rótulos con `texto` y queda en el
//      estado que haya dejado la última llamada (rótulo de y si hay
//      `etiquetaY`, si no el de x).
//    - `cuerpo`, `traza`, `marcaDeTope` y `bloque` no tocan ninguno de los tres.
//    - `suelo` tampoco toca `setLineDash`/`font`/`textAlign`, pero sí toca
//      `globalAlpha` para las rayitas (a 0.5) y lo repone a 1 antes de salir:
//      a diferencia de las tres propiedades de arriba, `globalAlpha` sale
//      siempre en el mismo estado en el que entró.
//    - `componentes` también limpia `setLineDash` a `[]` al final, igual que
//      `punteado`/`curva`; no toca `font`/`textAlign`.
//    - `arco` sin `rotulo` no toca ninguno de los tres. Con `rotulo`, delega en
//      `colocarEtiqueta` para escribirlo y queda en el estado que esa deja: `font`
//      en JetBrains Mono al tamaño por defecto y `textAlign` en `'left'` (el
//      `'center'` que pedía el arco se resuelve adentro, corriendo el
//      desplazamiento -- ver `colocarEtiqueta`).
//    - `presupuestoPx` deja escritos `fillStyle`, `strokeStyle` y `lineWidth`; no
//      toca `setLineDash` ni `globalAlpha`. Toca `font`/`textAlign` SÓLO si algún
//      segmento llegó a rotularse -queda lo que deje `texto`: JetBrains Mono a
//      10px y `textAlign` en `'center'`-. Con todos los segmentos más angostos
//      que `minEtiquetaPx` no los toca: el estado en que sale depende de los
//      datos que se le pasaron, no sólo de las opciones.
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

import { marca } from './formato.js';
import { colocarEtiqueta } from './etiqueta.js';
import { exigirColor } from './color.js';

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
  if (rotulo) colocarEtiqueta(ctx, rotulo, x2, y2, { dx: rdx, dy: rdy, color, alineacion: rAlineacion });
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

// Devuelve [dx, dy, acotado] con (dx, dy) recortado a lo sumo a `tope` pixeles de largo,
// conservando la direccion. `acotado` es true si hubo que recortar, y lo usa quien llama
// para decidir si dibuja la marca de tope.
//
// Hace falta cuando dos magnitudes del mismo dibujo tienen escalas muy distintas: en el
// widget de aceleraciones la normal llega a 600 mientras la tangencial vale 6, y sin
// acotar la flecha larga se va del canvas. La escala se deja fija a proposito --
// normalizar al valor del momento borraria que la magnitud crece.
export function acotarFlecha(dx, dy, tope) {
  const largo = Math.hypot(dx, dy);
  if (largo <= tope) return [dx, dy, false];
  const f = tope / largo;
  return [dx * f, dy * f, true];
}

// La marca de una flecha que llego a su tope: dos trazos cortos perpendiculares a la
// punta, la misma convencion que el quiebre de un eje partido en un grafico. No es
// sutil a proposito -- tiene que quedar claro que la magnitud real sigue creciendo
// aunque el dibujo ya no.
export function marcaDeTope(ctx, x, y, dx, dy, { color } = {}) {
  exigirColor(color, 'marcaDeTope');
  const angulo = Math.atan2(dy, dx);
  const nx = -Math.sin(angulo), ny = Math.cos(angulo);
  ctx.strokeStyle = color;
  ctx.lineWidth = 1.4;
  for (const d of [-3, 3]) {
    ctx.beginPath();
    ctx.moveTo(x + Math.cos(angulo) * d - nx * 5, y + Math.sin(angulo) * d - ny * 5);
    ctx.lineTo(x + Math.cos(angulo) * d + nx * 5, y + Math.sin(angulo) * d + ny * 5);
    ctx.stroke();
  }
}

// Un rectangulo con medidas en unidades fisicas, centrado en un punto del marco. Las
// cuatro esquinas se calculan en el marco y se mapean una por una con `l.p`, en vez de
// rotar el contexto: asi el bloque queda consistente con el lienzo inclinado y con lo
// que `arrastrable` devuelve, que es lo que se rompe cuando uno gira el contexto a mano.
export function bloque(ctx, l, centro, { ancho, alto, color, borde, angulo = 0 } = {}) {
  exigirColor(color, 'bloque');
  const [cx, cy] = centro;
  const cos = Math.cos(angulo), sen = Math.sin(angulo);
  const esquinas = [[-1, -1], [1, -1], [1, 1], [-1, 1]].map(([sx, sy]) => {
    const dx = (sx * ancho) / 2, dy = (sy * alto) / 2;
    return l.p([cx + dx * cos - dy * sen, cy + dx * sen + dy * cos]);
  });
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.moveTo(esquinas[0][0], esquinas[0][1]);
  for (let i = 1; i < 4; i++) ctx.lineTo(esquinas[i][0], esquinas[i][1]);
  ctx.closePath();
  ctx.fill();
  if (borde) {
    ctx.strokeStyle = borde;
    ctx.lineWidth = 1.2;
    ctx.stroke();
  }
}

// La linea del suelo con sus rayitas a 45 grados (no perpendiculares: la convencion de
// ingenieria para representar terreno es un rayado a 45 grados entre la linea y la
// direccion "hacia adentro" del terreno, y eso es lo que dibuja esto, igual que el
// ensayo de tiro parabolico del que se muda). Aca el rango es explicito en vez de
// asumir que el encuadre arranca en cero, que es lo que un plano inclinado necesita.
//
// El lado del rayado (que las rayitas caigan del lado del terreno y no del aire) sale
// de mapear con `l.p` el paso de un `y` de marco a `y - 1`, no de rotar un cuarto de
// vuelta la tangente ya calculada en pixeles. Son dos cosas distintas: con angulo
// distinto de cero y escala anisotropa (`l.escala.x != l.escala.y`) rotar la tangente
// en pixeles mezcla la direccion del suelo con la deformacion de la escala, y para
// algunas combinaciones (por ejemplo escala 1:3 con -30 grados) el resultado cae del
// lado equivocado de la linea. Mapear directamente el vector "hacia -y del marco" no
// tiene ese problema: es geometricamente el lado correcto para cualquier angulo y
// cualquier escala, porque es la definicion misma de "hacia el terreno".
export function suelo(ctx, l, { color, desde, hasta, y = 0 } = {}) {
  exigirColor(color, 'suelo');
  const [x0, y0] = l.p([desde, y]);
  const [x1, y1] = l.p([hasta, y]);
  ctx.strokeStyle = color;
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(x0, y0);
  ctx.lineTo(x1, y1);
  ctx.stroke();
  const largo = Math.hypot(x1 - x0, y1 - y0);
  const ux = (x1 - x0) / largo, uy = (y1 - y0) / largo;
  const [xAdentro, yAdentro] = l.p([desde, y - 1]);
  const largoAdentro = Math.hypot(xAdentro - x0, yAdentro - y0);
  const nx = (xAdentro - x0) / largoAdentro, ny = (yAdentro - y0) / largoAdentro;
  ctx.globalAlpha = 0.5;
  for (let d = 0; d < largo; d += 9) {
    ctx.beginPath();
    ctx.moveTo(x0 + ux * d, y0 + uy * d);
    ctx.lineTo(x0 + ux * (d - 6) + nx * 6, y0 + uy * (d - 6) + ny * 6);
    ctx.stroke();
  }
  ctx.globalAlpha = 1;
}

// El arquito que marca un angulo, con su letra en la bisectriz. El radio va en pixeles
// y no en unidades fisicas a proposito: un angulo no tiene tamaño fisico, y si el radio
// se escalara con el encuadre el arco cambiaria de tamaño al mover un slider. Grosor del
// trazo (1.2) y desplazamiento del rotulo (radio + 13, y + 4 de linea de base) son los
// mismos numeros con que el ensayo de tiro parabolico dibuja a mano el angulo de v0
// (docs/ensayos/tiro-parabolico.html:579-585).
export function arco(ctx, l, centro, { radio, desde, hasta, color, rotulo, colorTexto } = {}) {
  exigirColor(color, 'arco');
  const [ox, oy] = l.p(centro);
  ctx.strokeStyle = color;
  ctx.lineWidth = 1.2;
  ctx.beginPath();
  // En pantalla la y crece hacia abajo, asi que un angulo que en la fisica va en
  // sentido antihorario se dibuja con los signos cambiados: el angulo de canvas es
  // el opuesto del angulo fisico. El ultimo argumento no puede quedar fijo en `true`:
  // eso barre siempre en sentido de angulo de canvas decreciente, que es el camino
  // directo de `desde` a `hasta` solo cuando `desde < hasta`. Cuando el llamador pide
  // el arco al reves -- como el angulo medido desde la vertical en el ensayo de tiro
  // parabolico, que dibuja `ctx.arc(ox, oy, r, -Math.PI / 2, -ang, false)` -- barrer
  // siempre en el mismo sentido da la vuelta larga en vez del arco chico entre las dos
  // semirrectas. `ccw = desde < hasta` barre siempre directo, sin dar la vuelta.
  ctx.arc(ox, oy, radio, -desde, -hasta, desde < hasta);
  ctx.stroke();
  if (!rotulo) return;
  exigirColor(colorTexto, 'arco (colorTexto)');
  const medio = (desde + hasta) / 2;
  colocarEtiqueta(ctx, rotulo, ox, oy, {
    dx: Math.cos(medio) * (radio + 13), dy: -Math.sin(medio) * (radio + 13) + 4,
    color: colorTexto, alineacion: 'center',
  });
}

// Las dos punteadas que cierran el rectangulo entre el origen de un vector y su punta,
// en los ejes del marco. Es lo que hace ver que una fuerza oblicua no es una cosa nueva:
// son dos fuerzas, una por eje. Sobre un lienzo inclinado los ejes son los del plano,
// que es exactamente como se resuelve un plano inclinado.
export function componentes(ctx, l, desde, hasta, { color, guiones = [3, 4] } = {}) {
  exigirColor(color, 'componentes');
  const [x0, y0] = desde, [x1, y1] = hasta;
  ctx.strokeStyle = color;
  ctx.lineWidth = 1;
  ctx.setLineDash(guiones);
  for (const [a, b] of [[[x1, y0], [x1, y1]], [[x0, y1], [x1, y1]]]) {
    ctx.beginPath();
    ctx.moveTo(...l.p(a));
    ctx.lineTo(...l.p(b));
    ctx.stroke();
  }
  ctx.setLineDash([]);
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

// Cuanto cuelga la etiqueta de un eje por encima del techo de su encuadre (el `- 15`
// de mas abajo, `l.py(l.yMax) - COLGADO_ROTULO_EJE`). Exportada porque un widget que
// apila varios paneles en un mismo canvas -- el de los tres paneles de
// derivada-integral.html -- necesita el mismo numero para calcular cuanto aire dejar
// entre paneles y que la etiqueta de uno no caiga adentro del panel de arriba.
export const COLGADO_ROTULO_EJE = 15;

// Las marcas y rótulos son el `axes()` del diseño
// (docs/plataforma/diseno/Tiro parabolico.dc.html:376-401).
//
// `marcasX`/`marcasY` (default true) gobiernan cada bucle de marcas -y el numero que
// cuelga de cada una- por separado. Existen por el widget de los tres paneles de
// derivada-integral.html: ahi los tres paneles comparten el eje temporal, asi que ese
// eje se rotula una sola vez, en el panel de abajo, y los otros dos piden `marcasX:
// false` para no repetir los mismos numeros tres veces (y, en los paneles con yMin
// negativo, flotando en la mitad del grafico en vez de al pie).
//
// La guarda temprana es `!colorTexto`, no `!etiquetaX && !etiquetaY`: pedir las marcas
// de un eje sin su rotulo de palabra (`marcasX: true` sin `etiquetaX`) tiene que
// dibujar igual los numeros, y antes la ausencia de las dos etiquetas cortaba la
// funcion entera antes de llegar a los bucles. Sigue siendo compatible con todo
// llamador de hoy: quien pasa las dos etiquetas pasa tambien `colorTexto` (los cuatro
// widgets de tiro-parabolico.html y el widget 1 de derivada-integral.html), asi que
// entra igual que antes; quien pasa solo `color` no pasa `colorTexto`, asi que sigue
// saliendo despues de trazar nada mas que las dos lineas.
export function eje(ctx, l, { color, colorTexto, etiquetaX, etiquetaY, marcasX = true, marcasY = true } = {}) {
  exigirColor(color, 'eje');

  // El eje vertical se ancla en x=0 y el horizontal en y=0 SOLO cuando 0 esta dentro
  // del encuadre. Si no lo esta -el panel de la fuerza neta de fuerzas-de-posicion.html
  // mide de s=0.10 a s=0.99, y 0 no es parte de ese rango- anclar en 0 de todos modos
  // manda el eje, sus marcas Y SU ETIQUETA de palabra afuera del canvas, en silencio: a
  // 1280px ese encuadre da l.px(0) = -27.2, y ahi se dibujaba un eje invisible con
  // todas sus marcas y casi toda la etiqueta "F neta [mN]" fuera de los limites
  // (hallazgo de revision de la Tarea 15, Ruling 20). El ancla pasa a ser el valor del
  // encuadre MAS CERCANO a 0 dentro de el -que es 0 mismo siempre que el encuadre lo
  // contenga, asi que para todo otro dominio del sitio (el unico que excluye el 0 es
  // ese panel) esto es un no-op exacto: los tests de dibujo.test.js lo verifican en
  // los dos sentidos.
  const anclaX = Math.max(l.xMin, Math.min(l.xMax, 0));
  const anclaY = Math.max(l.yMin, Math.min(l.yMax, 0));

  ctx.strokeStyle = color;
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(l.px(l.xMin), l.py(anclaY));
  ctx.lineTo(l.px(l.xMax), l.py(anclaY));
  ctx.moveTo(l.px(anclaX), l.py(l.yMin));
  ctx.lineTo(l.px(anclaX), l.py(l.yMax));
  ctx.stroke();
  if (!colorTexto) return;

  if (marcasX) {
    const sx = paso(l.xMax - l.xMin);
    for (let x = Math.ceil(l.xMin / sx) * sx; x <= l.xMax + 1e-6; x += sx) {
      ctx.strokeStyle = color;
      ctx.beginPath();
      ctx.moveTo(l.px(x), l.py(anclaY));
      ctx.lineTo(l.px(x), l.py(anclaY) + 4);
      ctx.stroke();
      // El cero no se rotula: se lee del cruce de los ejes y ahi choca con el de y.
      // Los decimales del rotulo salen de `sx`, el paso de ESTE eje -- no de un decimal
      // fijo -- porque con un paso fino (0.05) un decimal solo repite rotulo ("0,3" dos
      // veces seguidas). `marca()` calcula cuantos decimales hacen falta a partir del
      // paso y ademas evita que un entero salga con un ",0" de mas.
      if (Math.abs(x) > 1e-9) {
        texto(ctx, marca(x, sx), l.px(x), l.py(anclaY) + 16,
          { color: colorTexto, px: 10, peso: 400, alineacion: 'center' });
      }
    }
  }
  if (marcasY) {
    const sy = paso(l.yMax - l.yMin);
    for (let y = Math.ceil(l.yMin / sy) * sy; y <= l.yMax + 1e-6; y += sy) {
      if (Math.abs(y) < 1e-9) continue;
      ctx.strokeStyle = color;
      ctx.beginPath();
      ctx.moveTo(l.px(anclaX), l.py(y));
      ctx.lineTo(l.px(anclaX) - 4, l.py(y));
      ctx.stroke();
      // Mismo motivo que en el bucle de x: los decimales salen de `sy`, el paso de este
      // eje, via `marca()`.
      texto(ctx, marca(y, sy), l.px(anclaX) - 8, l.py(y) + 3.5,
        { color: colorTexto, px: 10, peso: 400, alineacion: 'right' });
    }
  }
  if (etiquetaX) {
    // La etiqueta cuelga del PISO del encuadre, no del eje. En el diseno los dos
    // coinciden porque ahi todo encuadre arranca en yMin = 0 y debajo del eje solo hay
    // margen. Con un encuadre que baja de cero -- una x(t) que vale -3 en t = 0, por
    // ejemplo -- "debajo del eje" cae en el medio del grafico, y la etiqueta termina
    // encima de la curva y de los numeros de las marcas. Con yMin = 0 la posicion es
    // exactamente la misma de antes.
    texto(ctx, etiquetaX, l.px(l.xMax), l.py(l.yMin) + 28,
      { color: colorTexto, px: 10, alineacion: 'right' });
  }
  if (etiquetaY) {
    texto(ctx, etiquetaY, l.px(anclaX) - 34, l.py(l.yMax) - COLGADO_ROTULO_EJE,
      { color: colorTexto, px: 10, alineacion: 'left' });
  }
}

// Una barra apilada en pixeles: `segmentos` es una lista de {valor, color, etiqueta},
// todos en las mismas unidades que `total`. El ancho de cada uno es proporcional a su
// valor sobre `total` -- NO sobre la suma de los segmentos, y eso es a proposito.
//
// `total` se pide explicito, igual que `color` en las demas primitivas, porque la
// distancia entre "lo que suman los segmentos" y "el total declarado" ES la lectura que
// esta barra existe para mostrar. Una barra normalizada a si misma siempre se ve llena,
// y una barra que siempre se ve llena no delata nada: ni el calor que todavia no se
// disipo (suma < total: queda un tramo sin pintar) ni una energia contada dos veces
// (suma > total: la barra se desborda y lleva `marcaDeTope`). Clipear en silencio
// esconderia justo el error que hay que mostrar.
//
// El calculo del chequeo -- `total - suma`, o la diferencia entre dos energias que
// deberian coincidir -- lo hace el widget, no la primitiva: aca solo se dibuja lo que se
// pasa, igual que `vectorPx` no suma las fuerzas.
export function presupuestoPx(ctx, x, y, ancho, alto, segmentos,
  { total, colorBorde, colorTexto, minEtiquetaPx = 24 } = {}) {
  exigirColor(colorBorde, 'presupuestoPx (colorBorde)');
  for (const s of segmentos) {
    exigirColor(s.color, 'presupuestoPx (segmento)');
    // Un presupuesto de energia no tiene segmentos negativos: si hace falta mostrar el
    // trabajo negativo de un agente externo (la mano del ej. 5), son DOS barras --
    // "entra" y "sale" -- no un segmento al reves dentro de la misma. `Number.isFinite`
    // hace falta ademas de `>= 0`: `!(Infinity >= 0)` da `false`, asi que sin esta
    // guarda un valor infinito pasaba de largo y terminaba en
    // `fillRect(cursor, y, Infinity, alto)`, comportamiento de canvas no especificado.
    if (!(Number.isFinite(s.valor) && s.valor >= 0)) {
      throw new TypeError(
        `presupuestoPx: el segmento "${s.etiqueta ?? ''}" vale ${s.valor}. Un presupuesto no admite valores negativos, NaN ni infinitos: partilo en dos barras.`);
    }
  }
  // `total` es obligatorio, igual que `colorBorde`, y vive en la misma bolsa de
  // opciones donde es facil olvidarlo. Sin esta guarda, un `total` ausente caia en la
  // rama de abajo -"no dibuja nada"- y quedaba indistinguible de un presupuesto vacio
  // legitimo (`total: 0`, que SI tiene que seguir sin dibujar nada).
  if (total === undefined) {
    throw new TypeError(
      'presupuestoPx: falta `total`. Es obligatorio y sin default: sin el no hay escala que definir.');
  }
  // Sin total no hay escala que definir; dividir por cero daria NaN en cada ancho.
  if (!(total > 0)) return;
  const k = ancho / total;
  let cursor = x;
  for (const s of segmentos) {
    const w = s.valor * k;
    ctx.fillStyle = s.color;
    ctx.fillRect(cursor, y, w, alto);
    // Mismo criterio que `eje` al no rotular el cero: un rotulo que no entra se
    // superpone con el vecino y se lee peor que no estar.
    if (s.etiqueta && w >= minEtiquetaPx) {
      exigirColor(colorTexto, 'presupuestoPx (colorTexto)');
      texto(ctx, s.etiqueta, cursor + w / 2, y + alto / 2 + 4,
        { color: colorTexto, px: 10, alineacion: 'center' });
    }
    cursor += w;
  }
  ctx.strokeStyle = colorBorde;
  ctx.lineWidth = 1;
  ctx.strokeRect(x, y, ancho, alto);
  // La tolerancia es media unidad de pixel, no un margen contra el ruido de punto
  // flotante -ese ruido es del orden de 1e-10, ocho o nueve ordenes de magnitud mas
  // chico que esto-. Media unidad de pixel es lo razonable contra el antialiasing del
  // canvas y el redondeo de la geometria, pero en unidades del `total` deja pasar mas
  // de lo que suena: en una barra de 828 px con un total de 541,2 J, medio pixel son
  // `0.5 * 541.2 / 828` = 0,33 J de desborde que no dispara la marca de tope. Eso esta
  // bien -no es el trabajo de esta marca detectar diferencias de esa escala- porque
  // quien vigila que el modelo cierre es la lectura de chequeo del widget
  // (`total - suma`, calculada aparte), no esta marca: la marca avisa un desborde
  // visible, no certifica precision numerica.
  if (cursor > x + ancho + 0.5) {
    marcaDeTope(ctx, cursor, y + alto / 2, 1, 0, { color: colorBorde });
  }
}
