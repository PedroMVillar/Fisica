// Calculo numerico para los widgets. Nada de esto pretende ser un metodo de referencia:
// pretende ser estable a la vista, que es un requisito distinto. Una derivada ruidosa
// se nota como un temblor en el grafico aunque el error sea chico.

export function derivar(f, t, h = 1e-4) {
  return (f(t + h) - f(t - h)) / (2 * h);
}

export function integrar(f, t0, t1, n = 400) {
  const m = n % 2 ? n + 1 : n;            // Simpson necesita un numero par de tramos
  const h = (t1 - t0) / m;
  let s = f(t0) + f(t1);
  for (let i = 1; i < m; i++) s += f(t0 + i * h) * (i % 2 ? 4 : 2);
  return (s * h) / 3;
}

export function muestrear(f, t0, t1, n) {
  const pts = [];
  for (let i = 0; i <= n; i++) {
    const t = t0 + ((t1 - t0) * i) / n;
    pts.push([t, f(t)]);
  }
  return pts;
}

export function derivarMuestras(puntos) {
  const n = puntos.length;
  if (n < 2) return puntos.map(([t]) => [t, 0]);
  return puntos.map(([t], i) => {
    if (i === 0) {
      const [t1, x1] = puntos[0], [t2, x2] = puntos[1];
      return [t, (x2 - x1) / (t2 - t1)];
    }
    if (i === n - 1) {
      const [t1, x1] = puntos[n - 2], [t2, x2] = puntos[n - 1];
      return [t, (x2 - x1) / (t2 - t1)];
    }
    const [ta, xa] = puntos[i - 1], [tb, xb] = puntos[i + 1];
    return [t, (xb - xa) / (tb - ta)];
  });
}

export function suavizar(puntos, ventana = 5) {
  // Promedio movil con ventana simetrica tambien en los bordes: en vez de recortar
  // la ventana contra el borde (lo que sesga el promedio y curva una recta), se
  // extiende la serie por reflexion impar alrededor del punto extremo. El pliegue
  // es recursivo (no se acota al primer rebote) porque con pocos puntos frente al
  // radio pedido un solo rebote no alcanza a volver al rango valido: hay que seguir
  // reflejando hasta caer dentro. Con el pliegue recursivo la extension es exacta
  // para una recta sea cual sea la relacion entre el radio de ventana y n.
  const n = puntos.length;
  const r = Math.floor(ventana / 2);
  const valor = i => {
    if (n === 1) return puntos[0][1];
    if (i < 0) return 2 * puntos[0][1] - valor(-i);
    if (i > n - 1) return 2 * puntos[n - 1][1] - valor(2 * (n - 1) - i);
    return puntos[i][1];
  };
  return puntos.map(([t], i) => {
    let suma = 0;
    for (let k = i - r; k <= i + r; k++) suma += valor(k);
    return [t, suma / (2 * r + 1)];
  });
}
