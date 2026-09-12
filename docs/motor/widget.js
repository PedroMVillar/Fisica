import { crearLienzo } from './lienzo.js';
import { reiniciarEtiquetas } from './etiqueta.js';

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
// el encuadre contra el margen izquierdo/inferior (el comportamiento de siempre); true
// reparte ese sobrante en partes iguales entre los dos margenes de cada dimension, asi
// el encuadre queda centrado en el area util. Es lo que piden las circunferencias: un
// circulo pegado a un margen con todo el aire del lado opuesto se ve roto.
//
// Los dos son el mismo mecanismo con un solo numero distinto (ver `reparto` mas
// abajo): el sobrante de cada dimension se absorbe corriendo el margen, nunca
// estirando el encuadre, asi que en los dos casos el lienzo reporta siempre los
// bordes PEDIDOS -no hace falta pisar nada despues de armarlo.
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

      const { xMin = 0, xMax, yMin = 0, yMax, angulo = 0 } = encuadre();
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
      // Estado que los ensayos cambian y reponen a mano al dibujar (`globalAlpha` en
      // cinco lugares de los ensayos, `setLineDash` dentro de `curva` y `punteado`).
      // El contexto de un canvas sobrevive entre repintados y `repintarTodo` se traga
      // la excepcion de un widget: si algo lanza ENTRE el set y el reset, ese contexto
      // queda con alpha < 1 o con guiones puestos PARA SIEMPRE, y el widget se dibuja
      // translucido o punteado en cada repintado posterior, sin error visible.
      // Reponerlos aca, al lado de lineJoin/lineCap, hace que todo repintado arranque
      // del mismo estado, haya lanzado o no el anterior.
      ctx.globalAlpha = 1;
      ctx.setLineDash([]);

      if (escalaUniforme) {
        // Una sola escala para los dos ejes, para no deformar el dibujo: se elige la
        // que entra, y el sobrante de la dimension que no manda se reparte entre sus
        // dos margenes -- nunca se estira el encuadre para llenarlo.
        //
        // `reparto` es el unico numero que distingue los dos modos: la fraccion del
        // sobrante que absorbe el margen de abajo/izquierda (L en x, B en y) contra
        // el de arriba/derecha (R en x, T en y). `centrar:false` empuja TODO el
        // sobrante al margen de arriba/derecha (reparto=0: L y B quedan como se
        // pidieron, el dibujo quedan pegado contra ellos); `centrar:true` lo reparte
        // mitad y mitad (reparto=0.5).
        //
        // reparto=0 reproduce, punto por punto, el viejo camino de "estirar el
        // encuadre hasta llenar el area util y despues pisar xMax/yMax con los
        // pedidos": con L y B sin tocar y R/T absorbiendo el sobrante entero,
        // kx = (ancho - L - (R+sobranteX)) / (xMax-xMin) = (anchoUtil-sobranteX) /
        // (xMax-xMin) = sc -- la misma kx que salia de estirar xMax hasta
        // xMin + anchoUtil/sc. Y como px(x) = L + (x-xMin)*kx no depende de xMax en
        // absoluto, correr el margen o estirar el borde dan la MISMA funcion px (lo
        // mismo vale para py/yMax con T/B). El mecanismo de correr el margen es mas
        // general y subsume al de estirar, que era apenas el caso reparto=0.
        const altoUtil = alto - margen.T - margen.B;
        const sc = Math.min(anchoUtil / (xMax - xMin), altoUtil / (yMax - yMin));
        const sobranteX = anchoUtil - sc * (xMax - xMin);
        const sobranteY = altoUtil - sc * (yMax - yMin);
        const reparto = centrar ? 0.5 : 0;
        l = crearLienzo({
          ancho, alto, xMin, xMax, yMin, yMax, angulo,
          margen: {
            L: margen.L + sobranteX * reparto, R: margen.R + sobranteX * (1 - reparto),
            B: margen.B + sobranteY * reparto, T: margen.T + sobranteY * (1 - reparto),
          },
        });
      } else {
        // Escalas independientes, cada una llenando su dimension del area util: xMax
        // cae exacto en el borde derecho del area util y yMax en el borde superior.
        // No hay nada que estirar, asi que el lienzo reporta los bordes pedidos sin
        // ajuste alguno -la distincion "pedido vs. estirado" de arriba no existe aca.
        l = crearLienzo({ ancho, alto, margen, xMin, xMax, yMin, yMax, angulo });
      }

      // Vacia el registro de rotulos ya colocados antes del `dibujar` de ESTE widget:
      // cada canvas repinta su propio cuadro, y un rotulo del repintado anterior (o de
      // otro widget de la misma pagina, que comparte el registro porque es un modulo
      // con un solo estado) no tiene que poder empujar a uno de este. `crearWidget` es
      // el lugar natural porque ya envuelve el `dibujar` de cada widget y ya conoce el
      // tamaño del canvas (`ancho`/`alto`, en pixeles CSS -el mismo sistema de
      // coordenadas en el que dibuja `ctx`, ver el `setTransform` de arriba): asi
      // ninguna pagina tiene que acordarse de llamarlo, y el arreglo no se pudre con
      // el tiempo.
      reiniciarEtiquetas({ ancho, alto });
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
//   vertical propio del panel y el rango horizontal compartido del lienzo exterior
//   -salvo que el panel pida el suyo, ver `xMin`/`xMax` mas abajo.
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
        // Cada panel hereda el rango horizontal del lienzo de afuera, que es lo que
        // hace que una columna vertical signifique lo mismo en todos. Un panel puede
        // pedir el suyo cuando de verdad mide otra cosa: en la nota del auto y el
        // camion, la franja de arriba es la ruta en metros y la de abajo el grafico
        // de posicion contra tiempo en segundos.
        xMin: panel.xMin ?? lienzo.xMin,
        xMax: panel.xMax ?? lienzo.xMax,
        yMin: panel.yMin, yMax: panel.yMax,
      }),
    };
  });
}
