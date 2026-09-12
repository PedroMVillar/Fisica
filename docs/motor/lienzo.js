export function crearLienzo({ ancho, alto, xMin, xMax, yMin, yMax, margen, angulo = 0 }) {
  const m = { L: 0, R: 0, T: 0, B: 0, ...(margen || {}) };
  const kx = (ancho - m.L - m.R) / (xMax - xMin);
  const ky = (alto - m.T - m.B) / (yMax - yMin);
  const cos = Math.cos(angulo), sen = Math.sin(angulo);

  // Del marco girado al mundo y del mundo al marco. Son solo direccion: no hay
  // traslacion, porque los dos marcos comparten el origen. Es justo lo que necesita una
  // fuerza -- el peso apunta abajo en el mundo, y sobre un plano inclinado hay que
  // leerlo en el marco del plano.
  const aMundo = ([x, y]) => [x * cos - y * sen, x * sen + y * cos];
  const aMarco = ([X, Y]) => [X * cos + Y * sen, -X * sen + Y * cos];

  // El mapeo de un punto del marco a pixeles. Con angulo distinto de cero un punto NO se
  // puede mapear eje por eje: cada pixel depende de las dos coordenadas. Por eso `p` es
  // la forma correcta, y `px`/`py` toman la coordenada que les falta como segundo
  // argumento, igual que ya lo hacian.
  const aPixel = ([x, y]) => {
    const [X, Y] = aMundo([x, y]);
    return [m.L + (X - xMin) * kx, alto - m.B - (Y - yMin) * ky];
  };
  // Y la vuelta: de pixeles a coordenadas del marco.
  const aUnidades = (vx, vy) =>
    aMarco([(vx - m.L) / kx + xMin, (alto - m.B - vy) / ky + yMin]);

  return {
    ancho, alto, xMin, xMax, yMin, yMax, margen: m, angulo,
    aMundo, aMarco,
    p: aPixel,
    px: (x, y = 0) => aPixel([x, y])[0],
    py: (y, x = 0) => aPixel([x, y])[1],
    ux: (vx, vy = 0) => aUnidades(vx, vy)[0],
    uy: (vy, vx = 0) => aUnidades(vx, vy)[1],
    escala: { x: kx, y: ky },
  };
}
