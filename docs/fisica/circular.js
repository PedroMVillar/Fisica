// Movimiento circular, uniforme y uniformemente acelerado. El angulo crece en sentido
// antihorario desde theta0; para recorrer el circulo al reves basta con omega0 negativa.

export function crearCircular({ R, omega0, gamma = 0, theta0 = 0, centro = [0, 0] }) {
  const [cx, cy] = centro;

  const theta = t => theta0 + omega0 * t + 0.5 * gamma * t * t;
  const omega = t => omega0 + gamma * t;

  const versorR = t => [Math.cos(theta(t)), Math.sin(theta(t))];
  const versorTheta = t => [-Math.sin(theta(t)), Math.cos(theta(t))];

  const pos = t => {
    const [ux, uy] = versorR(t);
    return [cx + R * ux, cy + R * uy];
  };
  const vel = t => {
    const [ux, uy] = versorTheta(t);
    const v = omega(t) * R;
    return [v * ux, v * uy];
  };
  const rapidez = t => Math.abs(omega(t)) * R;

  // La tangencial cambia la rapidez; la normal cambia la direccion. Es toda la idea
  // del ensayo, y aca son dos lineas distintas a proposito.
  const aT = () => gamma * R;
  const aN = t => omega(t) ** 2 * R;
  const aTotal = t => Math.hypot(aT(t), aN(t));
  const aTotalVector = t => {
    const [rx, ry] = versorR(t);
    const [tx, ty] = versorTheta(t);
    return [aT(t) * tx - aN(t) * rx, aT(t) * ty - aN(t) * ry];
  };

  const uniforme = gamma === 0 && omega0 !== 0;
  const periodo = uniforme ? (2 * Math.PI) / Math.abs(omega0) : null;

  return {
    R, centro, theta, omega, pos, vel, rapidez,
    versorR, versorTheta, aT, aN, aTotal, aTotalVector,
    periodo,
    frecuencia: periodo === null ? null : 1 / periodo,
    vueltasEn: t => Math.abs(theta(t) - theta0) / (2 * Math.PI),
  };
}
