export function crearLienzo({ ancho, alto, xMin, xMax, yMin, yMax, margen }) {
  const m = { L: 0, R: 0, T: 0, B: 0, ...(margen || {}) };
  const kx = (ancho - m.L - m.R) / (xMax - xMin);
  const ky = (alto - m.T - m.B) / (yMax - yMin);
  const px = x => m.L + (x - xMin) * kx;
  const py = y => alto - m.B - (y - yMin) * ky;
  return {
    ancho, alto, xMin, xMax, yMin, yMax, margen: m, px, py,
    p: ([x, y]) => [px(x), py(y)],
    ux: v => (v - m.L) / kx + xMin,
    uy: v => (alto - m.B - v) / ky + yMin,
    escala: { x: kx, y: ky },
  };
}
