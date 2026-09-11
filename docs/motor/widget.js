import { crearLienzo } from './lienzo.js';

// Fabrica un widget: mide su canvas, arma el lienzo y delega el dibujo. La medicion
// replica al literal el `view()` del archivo de diseno (docs/plataforma/diseno/Tiro
// parabolico.dc.html:357-374): alto acotado entre `altoMin` y `altoMax` (default 215 y
// 430 px, los del archivo de diseno) y devicePixelRatio acotado a 2.
//
// `altoMin`/`altoMax` existen para el widget que apila varios paneles en un mismo
// canvas: el piso y el techo de un canvas suelto no le alcanzan (un panel se queda sin
// alto para su curva), y la constante no puede vivir escondida en cada pagina -- se
// pide como parametro del motor.
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
//   de diseno fija para el canvas (brief.md 6.4, `aspect-ratio:16/8`), acotado igual
//   que el camino uniforme.
//
// `centrar` (default false, solo tiene efecto con escalaUniforme:true) decide donde
// cae el sobrante que deja la escala unica en la dimension que no manda: false apoya
// el encuadre contra el margen izquierdo/superior (el comportamiento de siempre); true
// reparte ese sobrante en partes iguales entre los dos margenes de cada dimension, asi
// el encuadre queda centrado en el area util. Es lo que piden las circunferencias: un
// circulo pegado a un margen con todo el aire del lado opuesto se ve roto.
export function crearWidget({
  pagina, canvas, margen, encuadre, dibujar, dpr, escalaUniforme = true, centrar = false,
  altoMin = 215, altoMax = 430,
}) {
  let l = null;
  const acotarAlto = v => Math.round(Math.max(altoMin, Math.min(altoMax, v)));

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
        ? acotarAlto(margen.T + margen.B + anchoUtil * ((yMax - yMin) / (xMax - xMin)))
        : acotarAlto(ancho / 2);

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
        // que entra, y el sobrante de la otra dimension queda como aire.
        const altoUtil = alto - margen.T - margen.B;
        const sc = Math.min(anchoUtil / (xMax - xMin), altoUtil / (yMax - yMin));
        if (centrar) {
          // Mismo `sc` que el camino de abajo (la escala no cambia), pero en vez de
          // estirar el encuadre y despues acotar los bordes reportados, se deduce
          // cuanto ocupa el encuadre en cada dimension (sc * rango) y el sobrante de
          // cada una se reparte mitad y mitad entre sus dos margenes. El lienzo se
          // arma directo con los bordes PEDIDOS -no hay estirado que corregir despues-
          // y kx/ky salen `sc` los dos porque el margen efectivo absorbe exactamente
          // el sobrante: (ancho - mL - mR) = anchoUtil - sobranteX = sc * (xMax-xMin).
          const sobranteX = anchoUtil - sc * (xMax - xMin);
          const sobranteY = altoUtil - sc * (yMax - yMin);
          l = crearLienzo({
            ancho, alto, xMin, xMax, yMin, yMax,
            margen: {
              L: margen.L + sobranteX / 2, R: margen.R + sobranteX / 2,
              T: margen.T + sobranteY / 2, B: margen.B + sobranteY / 2,
            },
          });
        } else {
          const lEstirado = crearLienzo({
            ancho, alto, margen,
            xMin, xMax: xMin + anchoUtil / sc,
            yMin, yMax: yMin + altoUtil / sc,
          });
          // NO SIMPLIFICAR (solo aplica a este camino, sin centrar): el lienzo se
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
        }
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

// Arma los lienzos de un widget que apila N paneles verticales dentro de un mismo
// canvas, compartiendo el eje horizontal: los tres gráficos sincronizados de
// derivada-integral.html y el widget "Dibujá tu x(t)" del mismo ensayo son los dos
// casos de hoy, y hasta esta extracción cada uno llevaba su propia copia de esta
// aritmética -- 20 líneas idénticas salvo el nombre de dos variables.
//
// `lienzo` es el lienzo EXTERIOR del widget (el que devuelve `crearWidget`), con un
// encuadre vertical de `yMax: paneles.length` -- una unidad por panel; así
// `lienzo.py(0) - lienzo.py(paneles.length)` da el alto útil total en píxeles a
// repartir entre las franjas, y dividirlo por `paneles.length` da el alto de cada
// una. `margen` son los márgenes horizontales compartidos (`L`, `R`); el margen
// vertical de cada franja lo calcula esta función. `hueco` es el aire que se le
// agrega al margen superior de cada franja para que el rótulo del eje Y de `eje()`
// (que cuelga por encima de su techo) no caiga encima del panel de arriba -- ver el
// comentario de `HUECO_ROTULO` en los dos widgets que la llaman, que documentan de
// dónde sale ese número. `paneles` es la lista de descriptores, uno por franja, cada
// uno con al menos `yMin`/`yMax` (el rango vertical de esa franja); el widget que
// llama decide qué más lleva cada uno (color, etiqueta, función...) y lo recibe de
// vuelta intacto en `panel`.
//
// Devuelve, por cada elemento de `paneles`, en el mismo orden:
// - `panel`: el descriptor original, sin tocar.
// - `techo`: el borde superior de esa franja, en píxeles de canvas.
// - `alturaPanel`: el alto en píxeles de cada franja (igual para las N).
// - `lp`: el lienzo de esa franja, ya armado con `crearLienzo`, con el rango
//   vertical propio del panel y el rango horizontal compartido del lienzo exterior.
export function panelesApilados({ lienzo, margen, hueco, paneles }) {
  const n = paneles.length;
  const alturaPanel = (lienzo.py(0) - lienzo.py(n)) / n;
  const techoStack = lienzo.py(n);
  return paneles.map((panel, i) => {
    const techo = techoStack + i * alturaPanel;
    return {
      panel, techo, alturaPanel,
      lp: crearLienzo({
        ancho: lienzo.ancho, alto: lienzo.alto,
        margen: {
          L: margen.L, R: margen.R,
          T: techo + hueco, B: lienzo.alto - techo - alturaPanel + 10,
        },
        xMin: lienzo.xMin, xMax: lienzo.xMax, yMin: panel.yMin, yMax: panel.yMax,
      }),
    };
  });
}
