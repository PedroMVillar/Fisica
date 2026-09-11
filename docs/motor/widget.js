import { crearLienzo } from './lienzo.js';

// Fabrica un widget: mide su canvas, arma el lienzo y delega el dibujo. La medicion
// replica al literal el `view()` del archivo de diseno (docs/plataforma/diseno/Tiro
// parabolico.dc.html:357-374): alto acotado entre 215 y 430 px y devicePixelRatio
// acotado a 2.
//
// `escalaUniforme` (default true) decide como se reparte el area util entre los dos
// ejes:
// - true: una sola escala para los dos -el minimo entre lo que entra a lo ancho y lo
//   que entra a lo alto- para no deformar el dibujo. Es lo que pide un grafico donde
//   los dos ejes son la misma magnitud (tiro parabolico: metros x metros, una parabola
//   tiene que verse como una parabola).
// - false: cada eje se escala por separado, llenando su dimension del area util. Es lo
//   que pide un grafico de una magnitud contra el tiempo, donde no hay nada fisico que
//   igualar entre segundos y metros. El alto sale de la proporcion 16:8 que el sistema
//   de diseno fija para el canvas (brief.md 6.4, `aspect-ratio:16/8`), con el mismo
//   acotado entre 215 y 430 px.
export function crearWidget({ pagina, canvas, margen, encuadre, dibujar, dpr, escalaUniforme = true }) {
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
      const alto = escalaUniforme
        ? Math.round(Math.max(215, Math.min(430,
            margen.T + margen.B + anchoUtil * ((yMax - yMin) / (xMax - xMin)))))
        : Math.round(Math.max(215, Math.min(430, ancho / 2)));

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

      if (escalaUniforme) {
        // Una sola escala para los dos ejes, para no deformar el dibujo: se elige la
        // que entra, y el margen sobrante queda como aire.
        const sc = Math.min(anchoUtil / (xMax - xMin), (alto - margen.T - margen.B) / (yMax - yMin));
        const lEstirado = crearLienzo({
          ancho, alto, margen,
          xMin, xMax: xMin + anchoUtil / sc,
          yMin, yMax: yMin + (alto - margen.T - margen.B) / sc,
        });
        // NO SIMPLIFICAR (solo aplica a este camino, el uniforme): el lienzo se
        // construye estirado a proposito, para que kx y ky salgan los dos exactamente
        // `sc` y px/py queden uniformes -- son el X/Y del archivo de diseno. Pero los
        // bordes que se REPORTAN son los pedidos: `eje` traza hasta ahi, como el
        // axes() del diseno (Tiro parabolico.dc.html:383-384, que usa v.xmax, el tope
        // pedido), y el sobrante del area util queda como aire en vez de estirar el
        // eje. Reportar los estirados corre el eje que no manda hasta un pixel.
        //
        // El precio, y es el correcto, pero conviene tenerlo escrito: aca `px` y `ux`
        // dejan de cerrar en los bordes reportados. En el eje que no manda,
        // `l.px(l.xMax)` cae ADENTRO del area util (no en `ancho - margen.R`) y
        // `l.ux(ancho - margen.R)` da mas que `l.xMax`. Todo lienzo salido de
        // `crearLienzo` cumple esa vuelta; este, a proposito, no.
        l = { ...lEstirado, xMax, yMax };
      } else {
        // Escalas independientes, cada una llenando su dimension del area util: xMax
        // cae exacto en el borde derecho del area util y yMax en el borde superior.
        // No hay nada que estirar, asi que el lienzo reporta los bordes pedidos sin
        // ajuste alguno -la distincion "pedido vs. estirado" de arriba no existe aca.
        l = crearLienzo({ ancho, alto, margen, xMin, xMax, yMin, yMax });
      }

      dibujar(ctx, l, pagina);
    },
  };

  pagina.registrar(api);
  return api;
}
