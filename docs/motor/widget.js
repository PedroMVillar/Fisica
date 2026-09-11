import { crearLienzo } from './lienzo.js';

// Fabrica un widget: mide su canvas, arma el lienzo con escala uniforme y delega el
// dibujo. La medicion replica al literal la funcion `medir()` de
// docs/ensayos/tiro-parabolico.html (a su vez el `view()` de
// docs/plataforma/diseno/Tiro parabolico.dc.html:357-374): alto acotado entre 215 y
// 430 px, devicePixelRatio acotado a 2, y una sola escala para los dos ejes -el
// minimo entre lo que entra a lo ancho y lo que entra a lo alto- para no deformar.
export function crearWidget({ pagina, canvas, margen, encuadre, dibujar, dpr }) {
  let l = null;

  const api = {
    canvas,
    lienzo() { return l; },
    repintar() {
      const ancho = canvas.getBoundingClientRect().width
        || (canvas.parentElement ? canvas.parentElement.getBoundingClientRect().width : 0);
      if (!ancho) return;

      const { xMin = 0, xMax, yMin = 0, yMax } = encuadre();
      const anchoUtil = ancho - margen.L - margen.R;
      const alto = Math.round(Math.max(215, Math.min(430,
        margen.T + margen.B + anchoUtil * ((yMax - yMin) / (xMax - xMin)))));

      const escala = dpr ?? Math.min(2, globalThis.devicePixelRatio || 1);
      canvas.style.aspectRatio = 'auto';
      canvas.style.height = alto + 'px';
      canvas.width = Math.round(ancho * escala);
      canvas.height = Math.round(alto * escala);

      const ctx = canvas.getContext('2d');
      ctx.setTransform(escala, 0, 0, escala, 0, 0);
      ctx.clearRect(0, 0, ancho, alto);
      ctx.lineJoin = 'round';
      ctx.lineCap = 'round';

      // Una sola escala para los dos ejes, para no deformar el dibujo: se elige la
      // que entra, y el margen sobrante queda como aire.
      const sc = Math.min(anchoUtil / (xMax - xMin), (alto - margen.T - margen.B) / (yMax - yMin));
      const lEstirado = crearLienzo({
        ancho, alto, margen,
        xMin, xMax: xMin + anchoUtil / sc,
        yMin, yMax: yMin + (alto - margen.T - margen.B) / sc,
      });
      // NO SIMPLIFICAR: el lienzo se construye estirado a proposito, para que kx y ky
      // salgan los dos exactamente `sc` y px/py queden uniformes -- son el X/Y del
      // archivo de diseno. Pero los bordes que se REPORTAN son los pedidos: `eje` traza
      // hasta ahi, como el axes() del diseno (Tiro parabolico.dc.html:383-384, que usa
      // v.xmax, el tope pedido), y el sobrante del area util queda como aire en vez de
      // estirar el eje. Reportar los estirados corre el eje que no manda hasta un pixel.
      // El area util queda disponible en xMaxUtil/yMaxUtil para quien la necesite.
      l = { ...lEstirado, xMax, yMax, xMaxUtil: lEstirado.xMax, yMaxUtil: lEstirado.yMax };

      dibujar(ctx, l, pagina);
    },
  };

  pagina.registrar(api);
  return api;
}
