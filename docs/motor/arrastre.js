// Arrastrar un punto sobre un canvas, en coordenadas fisicas. El lienzo se pasa como
// funcion porque cambia en cada repintado: el widget lo reconstruye al cambiar de
// tamano, y un arrastre que guardara el viejo dibujaria corrido.

export function arrastrable({ canvas, lienzo, alArrastrar, acotar, pagina }) {
  let arrastrando = false;

  const puntoDe = evento => {
    const r = canvas.getBoundingClientRect();
    const l = lienzo();
    if (!l) return null;
    let x = l.ux(evento.clientX - r.left);
    let y = l.uy(evento.clientY - r.top);
    if (acotar) [x, y] = acotar(x, y);
    return [x, y];
  };

  canvas.addEventListener('pointerdown', e => {
    arrastrando = true;
    if (canvas.setPointerCapture) canvas.setPointerCapture(e.pointerId);
    canvas.style.cursor = 'grabbing';
    if (pagina) pagina.tocar();
    const p = puntoDe(e);
    if (p) alArrastrar(p[0], p[1]);
  });

  canvas.addEventListener('pointermove', e => {
    if (!arrastrando) return;
    const p = puntoDe(e);
    if (p) alArrastrar(p[0], p[1]);
  });

  // pointerup fuera del canvas y pointercancel (gesto cortado por el sistema) tienen
  // que soltar igual: setPointerCapture asegura que ambos eventos sigan llegando aca
  // aunque el puntero ya no este sobre el elemento, asi el arrastre nunca queda pegado.
  const soltar = () => {
    arrastrando = false;
    canvas.style.cursor = 'grab';
  };
  canvas.addEventListener('pointerup', soltar);
  canvas.addEventListener('pointercancel', soltar);

  return { arrastrando: () => arrastrando };
}
