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

// Traduccion literal del label() del diseno
// (plataforma/diseno/Tiro parabolico.dc.html:319-323):
//   s.playing ? 'Pausar' : (!s.rest && s.t > 0 ? 'Seguir' : 'Reproducir')
// `enReposo` es el `s.rest` del diseno. No sale de la escena porque crearEscena no
// distingue "en reposo mostrando un instante representativo" de "pausado a mitad":
// esa distincion la lleva el ensayo, que es quien decide cuando salir del reposo.
export function rotuloReproducir(elemento, escena, enReposo) {
  if (!elemento) return;
  if (escena.estado === 'reproduciendo') { elemento.textContent = 'Pausar'; return; }
  elemento.textContent = !enReposo && escena.t > 0 ? 'Seguir' : 'Reproducir';
}
