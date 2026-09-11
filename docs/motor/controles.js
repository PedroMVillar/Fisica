// Cableado de los controles de un widget. Nada de esto sabe de fisica ni de canvas:
// traduce eventos del DOM a llamadas con valores ya parseados y formateados.

export function deslizador({ entrada, salida, formato, alCambiar, pagina }) {
  const leer = () => parseFloat(entrada.value);
  const pintar = () => { if (salida) salida.textContent = formato(leer()); };
  pintar();
  entrada.addEventListener('input', () => {
    pintar();
    if (pagina) pagina.tocar();
    alCambiar(leer());
  });
  return { valor: leer };
}

export function casilla({ entrada, alCambiar, pagina }) {
  const leer = () => entrada.checked;
  entrada.addEventListener('change', () => {
    if (pagina) pagina.tocar();
    alCambiar(leer());
  });
  return { valor: leer };
}

export function boton({ elemento, alApretar, pagina }) {
  elemento.addEventListener('click', () => {
    if (pagina) pagina.tocar();
    alApretar();
  });
}

// El rotulo distingue "pausado a mitad de camino" (Seguir) de "pausado justo al
// final" (Reproducir): crearEscena() lleva ambos casos al mismo estado 'pausado'
// (avanzar() para en t === duracion), asi que la unica forma de diferenciarlos
// es comparar t contra duracion, como en docs/plataforma/diseno/Tiro parabolico.dc.html.
export function rotuloReproducir(elemento, escena) {
  if (!elemento) return;
  if (escena.estado === 'reproduciendo') { elemento.textContent = 'Pausar'; return; }
  const aMitad = escena.t > 0 && escena.t < escena.duracion - 1e-6;
  elemento.textContent = aMitad ? 'Seguir' : 'Reproducir';
}
