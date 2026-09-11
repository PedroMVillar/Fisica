// Alternar el tema claro/oscuro, persistirlo y rotular el boton que lo controla.
// Los tres primeros ensayos repetian este bloque de ~20 lineas letra por letra
// (docs/ensayos/tiro-parabolico.html, derivada-integral.html, movimiento-circular.html);
// con seis ensayos en el brief del proyecto ya conviene un solo lugar.
//
// El script bloqueante del <head> que aplica el tema ANTES del primer pintado (para que
// no haya flash de tema claro) no se muda aca: tiene que seguir corriendo de forma
// sincronica y no puede depender de un modulo diferido como este.

const CLAVE = 'tp-theme';

export function conectarTema({ pagina, boton, documento = globalThis.document }) {
  const raiz = documento.documentElement;

  const sincronizar = () => {
    boton.textContent = raiz.getAttribute('data-theme') === 'dark' ? 'Claro' : 'Oscuro';
  };

  boton.onclick = () => {
    const oscuro = raiz.getAttribute('data-theme') === 'dark';
    if (oscuro) raiz.removeAttribute('data-theme');
    else raiz.setAttribute('data-theme', 'dark');
    // Si el almacenamiento esta bloqueado, la preferencia no se recuerda, pero
    // el tema de esta visita tiene que cambiar igual: sin el try/catch la
    // excepcion cortaba aca y el canvas se quedaba con la paleta vieja.
    try { localStorage.setItem(CLAVE, oscuro ? 'light' : 'dark'); } catch (e) {}
    pagina.olvidarPaleta();
    sincronizar();
    pagina.repintarTodo();
  };

  // El tema ya quedo aplicado por el script del <head>; aca solo se rotula.
  sincronizar();
}
