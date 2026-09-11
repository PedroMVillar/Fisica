// Ajuste de un conjunto de puntos 2D a la circunferencia que mejor los aproxima, por
// minimos cuadrados (metodo algebraico de Kasa). Lo usa el widget "De las ecuaciones
// al circulo" para decidir si una trayectoria escrita como dos funciones parametricas
// x(t), y(t) es o no una circunferencia: si los puntos son colineales (o casi) no hay
// ningun circulo finito que les corresponda, y se devuelve null.
//
// LA TRAMPA DEL UMBRAL ABSOLUTO (hallazgo de revision de la Tarea 18): decidir "hay
// circulo" comparando el determinante del sistema normal contra una constante absoluta
// rompe con datos que no estan cerca de esa escala. Una recta GENERICA (con pendiente y
// ordenada al origen cualesquiera, no la del preset x=t/y=t) puede dar, sin normalizar,
// un determinante de magnitud grande por el solo hecho de que las coordenadas son
// grandes -y entonces "parece" no degenerado, y el ajuste devuelve un centro espurio
// cuya distancia varia con el ruido de punto flotante, no con la geometria-; y al
// reves, un circulo perfecto pero diminuto puede dar un determinante chico en valor
// absoluto y "parecer" degenerado aunque el ajuste sea exacto.
//
// La correccion: centrar los puntos en su centroide y reescalarlos por la raiz
// cuadratica media (RMS) de sus radios antes de plantear el sistema lineal.
//
// - Centrado, las sumas de primer momento se anulan EXACTAMENTE (sum(u) = sum(v) = 0,
//   con u = x - cx0, v = y - cy0), asi que el sistema normal 3x3 de Kasa -que en
//   general acopla (a, b, c)- colapsa a un sistema 2x2 desacoplado en (a, b), el centro
//   en coordenadas normalizadas (la tercera ecuacion, para c = r^2, queda trivial y no
//   hace falta resolverla: no se necesita el radio, solo el centro).
// - Reescalado por RMS, los promedios Mxx = mean(p^2), Myy = mean(q^2) (con
//   p = u/rms, q = v/rms) cumplen Mxx + Myy = 1 por construccion, asi que quedan
//   siempre en el rango [0, 1] sea cual sea la escala, la posicion o la cantidad de
//   puntos de los datos originales. El determinante del sistema 2x2,
//   4*(Mxx*Myy - Mxy^2), quedo entonces ADIMENSIONAL: un umbral absoluto sobre ese
//   numero tiene el mismo significado sin importar de donde vinieron los datos.
// - Por ultimo se desnormaliza el centro (se multiplica por el RMS y se suma el
//   centroide).
//
// Se devuelve null (no hay circulo) cuando: hay menos de 3 puntos, algun punto no es
// finito (NaN o Infinito), todos los puntos coinciden (RMS ~ 0, no hay geometria que
// ajustar), o el determinante normalizado es demasiado chico (puntos colineales o
// casi).
const UMBRAL_DETERMINANTE = 1e-9;

export function ajustarCirculo(puntos) {
  const n = puntos.length;
  if (n < 3) return null;

  let sx = 0, sy = 0;
  for (const [x, y] of puntos) {
    if (!Number.isFinite(x) || !Number.isFinite(y)) return null;
    sx += x;
    sy += y;
  }
  const cx0 = sx / n, cy0 = sy / n;

  const centrados = puntos.map(([x, y]) => [x - cx0, y - cy0]);
  let sumaR2 = 0;
  for (const [u, v] of centrados) sumaR2 += u * u + v * v;
  const rms = Math.sqrt(sumaR2 / n);
  if (!Number.isFinite(rms) || rms < 1e-12) return null;

  let mxx = 0, myy = 0, mxy = 0, mxz = 0, myz = 0;
  for (const [u, v] of centrados) {
    const p = u / rms, q = v / rms;
    const z = p * p + q * q;
    mxx += p * p;
    myy += q * q;
    mxy += p * q;
    mxz += p * z;
    myz += q * z;
  }
  mxx /= n; myy /= n; mxy /= n; mxz /= n; myz /= n;

  const det = 4 * (mxx * myy - mxy * mxy);
  if (!Number.isFinite(det) || Math.abs(det) < UMBRAL_DETERMINANTE) return null;

  const a = (2 * myy * mxz - 2 * mxy * myz) / det;
  const b = (2 * mxx * myz - 2 * mxy * mxz) / det;
  if (!Number.isFinite(a) || !Number.isFinite(b)) return null;

  return [cx0 + a * rms, cy0 + b * rms];
}
