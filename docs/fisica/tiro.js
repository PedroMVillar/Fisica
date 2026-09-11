export function crearTiro({ v0, alfaGrados, x0 = 0, y0 = 0, g = 9.8, ax = 0 }) {
  const a = (alfaGrados * Math.PI) / 180;
  const v0x = v0 * Math.cos(a);
  const v0y = v0 * Math.sin(a);

  const pos = t => [x0 + v0x * t + 0.5 * ax * t * t, y0 + v0y * t - 0.5 * g * t * t];
  const vel = t => [v0x + ax * t, v0y - g * t];

  const tMax = v0y / g;
  const yMax = y0 + (v0y * v0y) / (2 * g);
  // y(t) = 0  ->  (g/2) t^2 - v0y t - y0 = 0
  const tVuelo = (v0y + Math.sqrt(v0y * v0y + 2 * g * y0)) / g;
  const alcance = pos(tVuelo)[0];

  return { pos, vel, tMax, yMax, tVuelo, alcance, v0x, v0y };
}
