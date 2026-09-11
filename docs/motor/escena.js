// Motor de escena: máquina de estados y reloj para widgets animados.
//
// No sabe qué se dibuja ni cómo: recibe `dibujar(t)` como callback y solo
// gobierna el paso del tiempo y las transiciones de estado. El widget que la
// usa decide qué representar en cada instante.
//
// `avanzar(dt)` es el único punto de entrada que mueve el reloj. En el
// navegador, `reproducir()` lo llama solo mediante un loop de
// requestAnimationFrame; en las pruebas (sin navegador) se llama a mano.

// Tope del salto de un frame, en segundos, igual que el diseño
// (`docs/plataforma/diseno/Tiro parabolico.dc.html`: `Math.min(0.05, ...)`).
// Si la pestaña queda en segundo plano el navegador suspende el rAF, y sin tope
// el primer frame de vuelta se comería de un saque todo el tiempo ausente: la
// animación saltaría al final en vez de seguir donde estaba. El tope vive acá,
// en el loop, que es quien mide tiempo real entre frames; `avanzar(dt)` es el
// punto de entrada manual y respeta el dt que le pasan.
const SALTO_MAXIMO = 0.05;

export function crearEscena({ dibujar, duracion, alCambiar = () => {} }) {
  let t = 0;
  let estado = 'reposo';
  let idAnimacion = null;
  let tAnterior = null;

  const pasarA = nuevo => {
    if (nuevo === estado) return;
    estado = nuevo;
    alCambiar(estado);
  };

  const detenerLoop = () => {
    if (idAnimacion !== null && typeof cancelAnimationFrame === 'function') {
      cancelAnimationFrame(idAnimacion);
    }
    idAnimacion = null;
    tAnterior = null;
  };

  const paso = ahora => {
    if (estado !== 'reproduciendo') {
      idAnimacion = null;
      tAnterior = null;
      return;
    }
    if (tAnterior === null) tAnterior = ahora;
    const dt = Math.min(SALTO_MAXIMO, (ahora - tAnterior) / 1000);
    tAnterior = ahora;
    api.avanzar(dt);
    if (estado === 'reproduciendo') {
      idAnimacion = requestAnimationFrame(paso);
    } else {
      idAnimacion = null;
      tAnterior = null;
    }
  };

  const api = {
    get t() { return t; },
    get estado() { return estado; },
    reproducir() {
      if (estado === 'reproduciendo') return;
      pasarA('reproduciendo');
      // Sin navegador (pruebas) no hay requestAnimationFrame: el reloj lo
      // mueve quien llame a avanzar(dt) a mano.
      if (typeof requestAnimationFrame === 'function') {
        tAnterior = null;
        idAnimacion = requestAnimationFrame(paso);
      }
    },
    pausar() {
      detenerLoop();
      pasarA('pausado');
    },
    reiniciar() {
      detenerLoop();
      t = 0;
      pasarA('reposo');
      dibujar(t);
    },
    avanzar(dt) {
      if (estado !== 'reproduciendo') return;
      t = Math.min(t + dt, duracion);
      if (t >= duracion) {
        detenerLoop();
        pasarA('pausado');
      }
      dibujar(t);
    },
  };
  return api;
}
