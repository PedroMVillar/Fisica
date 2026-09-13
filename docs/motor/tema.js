// Alternar el tema claro/oscuro, persistirlo y rotular el boton que lo controla.
// Los tres primeros ensayos repetian este bloque de ~20 lineas letra por letra
// (docs/ensayos/tiro-parabolico.html, derivada-integral.html, movimiento-circular.html);
// con seis ensayos en el brief del proyecto ya conviene un solo lugar.
//
// El script bloqueante del <head> que aplica el tema ANTES del primer pintado (para que
// no haya flash de tema claro) no se muda aca: tiene que seguir corriendo de forma
// sincronica y no puede depender de un modulo diferido como este.
//
// SON TRES ESTADOS, NO DOS. `data-theme="dark"` y `data-theme="light"` son elecciones
// explicitas del lector y mandan siempre; la AUSENCIA del atributo significa «no elegi
// nada» y ahi manda el sistema operativo, via la media query de base.css. Antes habia
// solo dos —atributo puesto o no— y por eso «claro» y «no elegi» eran indistinguibles:
// con ese modelo, respetar al sistema implicaba pisarle la eleccion a quien habia
// pedido claro. Por eso aca nunca se borra el atributo: se escribe siempre un valor.

const CLAVE = 'tp-theme';

const consultaOscuro = () =>
  (typeof globalThis.matchMedia === 'function'
    ? globalThis.matchMedia('(prefers-color-scheme: dark)')
    : null);

export function conectarTema({ pagina, boton, documento = globalThis.document }) {
  const raiz = documento.documentElement;

  // El tema EFECTIVO no es el atributo. Sin eleccion, el atributo no esta y la pagina
  // se ve como diga el sistema; rotular por el atributo dejaba el boton ofreciendo
  // «Oscuro» sobre una pagina que ya estaba oscura.
  const esOscuro = () => {
    const elegido = raiz.getAttribute('data-theme');
    if (elegido === 'dark' || elegido === 'light') return elegido === 'dark';
    return consultaOscuro()?.matches === true;
  };

  const sincronizar = () => { boton.textContent = esOscuro() ? 'Claro' : 'Oscuro'; };

  boton.onclick = () => {
    const nuevo = esOscuro() ? 'light' : 'dark';
    raiz.setAttribute('data-theme', nuevo);
    // Si el almacenamiento esta bloqueado, la preferencia no se recuerda, pero
    // el tema de esta visita tiene que cambiar igual: sin el try/catch la
    // excepcion cortaba aca y el canvas se quedaba con la paleta vieja.
    try { localStorage.setItem(CLAVE, nuevo); } catch (e) {}
    pagina.olvidarPaleta();
    sincronizar();
    pagina.repintarTodo();
  };

  // Si el lector no eligio nada y cambia el tema del sistema con la pagina abierta,
  // el CSS se actualiza solo pero los canvas NO: leen la paleta una vez y la cachean,
  // asi que se quedarian con los colores del tema anterior sobre el fondo nuevo.
  consultaOscuro()?.addEventListener?.('change', () => {
    if (raiz.getAttribute('data-theme')) return;   // hubo eleccion: no nos metemos
    pagina.olvidarPaleta();
    sincronizar();
    pagina.repintarTodo();
  });

  // El tema ya quedo aplicado por el script del <head>; aca solo se rotula.
  sincronizar();
}
