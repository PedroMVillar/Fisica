// El unico lugar del sitio donde un numero se vuelve texto. Existe porque la
// convencion del sitio es la COMA -- decision del dueno, ver plataforma/decisiones.md
// -- y JS escribe punto en `toFixed`, `toExponential` y `String`. Tener 117 sitios
// haciendo la conversion a mano garantiza que tarde o temprano uno quede en punto.

const SUPERINDICES = { '-': '⁻', 0: '⁰', 1: '¹', 2: '²', 3: '³', 4: '⁴',
                       5: '⁵', 6: '⁶', 7: '⁷', 8: '⁸', 9: '⁹' };

// Quita el signo de un cero que salio de una cancelacion: varios widgets usan una
// lectura que tiene que dar cero como prueba de su modelo, y "-0,00" se lee como si
// el modelo estuviera roto cuando en realidad esta bien.
function sinCeroNegativo(s) {
  return /^-0(,0*)?$/.test(s) ? s.slice(1) : s;
}

export function num(x, decimales) {
  return sinCeroNegativo(x.toFixed(decimales).replace('.', ','));
}

export function exp(x, decimales) {
  const e = x === 0 ? 0 : Math.floor(Math.log10(Math.abs(x)));
  if (e === 0) return num(x, decimales);
  const mantisa = num(x / Math.pow(10, e), decimales);
  const sufijo = String(e).split('').map(c => SUPERINDICES[c]).join('');
  return `${mantisa} × 10${sufijo}`;
}

// El rotulo de una marca de eje. Los decimales salen del PASO y no de un numero fijo:
// con paso 0.05 hacen falta dos, con paso 1 ninguno. Y se usa `String` sobre el valor
// redondeado en vez de `toFixed`, para que un entero salga "2" y no "2,0" -- que es lo
// que `eje()` hace hoy y hay que conservar.
//
// La formula de `d` alcanza para los pasos que `paso()` de dibujo.js puede devolver
// hoy (0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10 -- siempre 1, 2 o 5 por una
// potencia de diez). Rompe para un paso de 0.25 (da 1 decimal y hacen falta 2): si
// `paso()` cambia alguna vez para devolver otros escalones, esta funcion hay que
// revisarla.
export function marca(x, paso) {
  const d = Math.max(0, Math.ceil(-Math.log10(paso)));
  const p = Math.pow(10, d);
  return sinCeroNegativo(String(Math.round(x * p) / p).replace('.', ','));
}
