// Servicios que comparten todos los widgets de una pagina: la paleta leida de los
// tokens CSS, el registro de widgets para repintarlos juntos cuando cambia el tema o
// el tamano, la barra de progreso de lectura, y la marca de "el lector ya toco algo",
// que es la que apaga el pulso del boton.

const TOKENS = [
  ['paper', '--paper'], ['band', '--band'], ['ink', '--ink'], ['dim', '--dim'],
  ['rule', '--rule'], ['blue', '--blue'], ['blueSoft', '--blue-soft'],
  ['red', '--red'], ['graph', '--graph'],
];

export function crearPagina({ documento = globalThis.document } = {}) {
  const registrados = [];
  const suscriptos = [];
  let cache = null;
  let tocada = false;
  let observador = null;

  const api = {
    paleta() {
      if (cache) return cache;
      const cs = documento.getComputedStyle
        ? documento.getComputedStyle(documento.documentElement)
        : globalThis.getComputedStyle(documento.documentElement);
      cache = {};
      for (const [nombre, token] of TOKENS) cache[nombre] = cs.getPropertyValue(token).trim();
      return cache;
    },
    olvidarPaleta() { cache = null; },
    registrar(widget) { registrados.push(widget); },
    widgets() { return registrados.slice(); },
    // Cada widget se repinta en su propio try/catch: sin esto, una excepcion en el
    // `dibujar` de UN widget aborta el bucle entero y deja sin repintar a los que
    // venian despues (hallazgo de revision de la Tarea 18) -- y este metodo corre al
    // cambiar de tema, al redimensionar la ventana y al resolver `fonts.ready`, asi
    // que un widget roto se llevaba puestos a los demas en los tres casos. El error
    // se deja visible en la consola (no se traga en silencio): un widget que falla
    // sigue siendo un bug a corregir, sólo que ya no bloquea a los otros tres.
    repintarTodo() {
      for (const w of registrados) {
        try {
          w.repintar();
        } catch (error) {
          console.error(error);
        }
      }
    },
    observar() {
      if (typeof ResizeObserver !== 'function') return;
      if (observador) observador.disconnect();
      observador = new ResizeObserver(() => api.repintarTodo());
      for (const w of registrados) {
        const padre = w.canvas && w.canvas.parentElement;
        if (padre) observador.observe(padre);
      }
    },
    tocar() {
      if (tocada) return;
      tocada = true;
      for (const fn of suscriptos) fn();
    },
    // Consumida por la Tarea 6: decide si arrancar el pulso del boton "Reproducir"
    // al cargar (no lo arranca si el lector ya toco algo).
    tocada() { return tocada; },
    alTocar(fn) { suscriptos.push(fn); },
    progreso(elemento) {
      if (!elemento || typeof globalThis.addEventListener !== 'function') return;
      globalThis.addEventListener('scroll', () => {
        const max = documento.documentElement.scrollHeight - globalThis.innerHeight;
        const pct = max > 0 ? Math.min(100, (globalThis.scrollY / max) * 100) : 0;
        elemento.style.width = pct + '%';
      });
    },
  };

  // Los widgets pintan texto en el canvas y el canvas se pinta pocas veces: si las
  // tipografias de la pagina todavia no llegaron, los rotulos quedan en la fuente de
  // respaldo PARA SIEMPRE, porque despues nadie repinta. Un repintado cuando
  // `fonts.ready` resuelve cierra esa carrera. En Node (pruebas) no hay
  // `documento.fonts`, y en navegadores viejos puede no haber `ready`: por eso las dos
  // guardas.
  if (documento.fonts && typeof documento.fonts.ready?.then === 'function') {
    documento.fonts.ready
      .then(() => api.repintarTodo())
      // Sin esto, un widget que lance en su `dibujar` queda como rechazo no manejado:
      // un error de consola sin traza a quien lo causo. Se relanza fuera de la cadena
      // para que llegue a window.onerror con su pila entera.
      .catch(error => setTimeout(() => { throw error; }, 0));
  }

  return api;
}
