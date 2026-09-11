export function crearLienzo({ ancho, alto, xMin, xMax, yMin, yMax }) {
  const kx = ancho / (xMax - xMin);
  const ky = alto / (yMax - yMin);
  const px = x => (x - xMin) * kx;
  const py = y => alto - (y - yMin) * ky;
  return {
    ancho, alto, xMin, xMax, yMin, yMax,
    px, py,
    p: ([x, y]) => [px(x), py(y)],
    ux: v => v / kx + xMin,
    uy: v => (alto - v) / ky + yMin,
    escala: { x: kx, y: ky },
  };
}
