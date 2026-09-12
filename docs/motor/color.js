// `exigirColor` vive en su propio módulo por una razón de dependencias, no de
// organización: `dibujo.js` importa `colocarEtiqueta` de `etiqueta.js`, así que
// `etiqueta.js` no puede importar `exigirColor` de vuelta desde `dibujo.js` sin cerrar
// un ciclo. Sacarlo a un módulo sin dependencias propias deja que los dos lo importen
// de aquí.
//
// `color` es obligatorio en toda primitiva de dibujo y en `colocarEtiqueta`, y no tiene
// valor por defecto. Un default sería una cuarta copia de la paleta —que vive en
// docs/estilos/base.css, copiada del archivo de diseño— escondida en un módulo que no
// sabe que existen los temas: se desviaría en silencio y pintaría colores de tema claro
// sobre una página oscura. El color sale siempre de los tokens CSS leídos por el widget.
export function exigirColor(color, primitiva) {
  if (typeof color !== 'string' || color === '') {
    throw new TypeError(
      `${primitiva}: falta el color. Es obligatorio y sin default: pasalo desde los tokens CSS del widget.`
    );
  }
}
