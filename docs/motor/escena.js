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

// Lectura del mismo reloj que usa requestAnimationFrame para marcar sus frames:
// en el navegador, el timestamp que recibe el callback de rAF y performance.now()
// comparten origen. Si no hay performance (entorno pelado), devuelve null y el
// loop cae en el comportamiento de antes: fija el origen en el primer frame.
const ahoraDelReloj = () =>
  typeof performance !== 'undefined' && typeof performance.now === 'function'
    ? performance.now()
    : null;

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
    // El piso en 0 es por si el origen y el timestamp del frame no vinieran del
    // mismo reloj: un dt negativo haría retroceder el tiempo.
    const dt = Math.min(SALTO_MAXIMO, Math.max(0, (ahora - tAnterior) / 1000));
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
        // El origen del reloj se fija ACÁ, en el instante de la llamada, y no
        // en el primer frame. Si se fijara en el primer frame, ese frame
        // valdría siempre dt = 0, y una escena que se reconstruye a mitad de
        // la animación regalaría un frame congelado cada vez. El ensayo de
        // tiro parabólico rehace la escena en cada evento `input` del slider
        // —la duración se fija al crearla—, y `input` en un range dispara por
        // píxel de recorrido: con un mouse de alta tasa de sondeo o con el
        // dedo puede superar los 60 Hz y entonces *todos* los frames del
        // arrastre serían de dt cero, con el reloj clavado. Fijando el origen
        // en reproducir(), el tiempo transcurrido entre la reconstrucción y el
        // frame siguiente se cuenta igual, como en el tick compartido del
        // diseño.
        tAnterior = ahoraDelReloj();
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
