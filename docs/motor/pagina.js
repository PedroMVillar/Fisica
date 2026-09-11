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
    repintarTodo() { for (const w of registrados) w.repintar(); },
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
    documento.fonts.ready.then(() => api.repintarTodo());
  }

  return api;
}
