const PUNTA = 9;

export function vector(ctx, l, desde, hasta, { color, grosor = 2 } = {}) {
  const [x1, y1] = l.p(desde);
  const [x2, y2] = l.p(hasta);
  const dx = x2 - x1, dy = y2 - y1;
  const largo = Math.hypot(dx, dy);
  if (largo < 1e-9) return;
  ctx.strokeStyle = color;
  ctx.fillStyle = color;
  ctx.lineWidth = grosor;
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.stroke();
  const ux = dx / largo, uy = dy / largo;
  ctx.beginPath();
  ctx.moveTo(x2, y2);
  ctx.lineTo(x2 - ux * PUNTA - uy * PUNTA * 0.4, y2 - uy * PUNTA + ux * PUNTA * 0.4);
  ctx.lineTo(x2 - ux * PUNTA + uy * PUNTA * 0.4, y2 - uy * PUNTA - ux * PUNTA * 0.4);
  ctx.closePath();
  ctx.fill();
}

export function cuerpo(ctx, l, punto, { radio = 4, color = '#16151a' } = {}) {
  const [x, y] = l.p(punto);
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.arc(x, y, radio, 0, Math.PI * 2);
  ctx.fill();
}

export function huella(ctx, l, punto, { radio = 2.5, color = '#8e8a80' } = {}) {
  cuerpo(ctx, l, punto, { radio, color });
}

export function traza(ctx, l, puntos, { color = '#1b4fd4', grosor = 2 } = {}) {
  if (puntos.length < 2) return;
  ctx.strokeStyle = color;
  ctx.lineWidth = grosor;
  ctx.beginPath();
  const [x0, y0] = l.p(puntos[0]);
  ctx.moveTo(x0, y0);
  for (let i = 1; i < puntos.length; i++) {
    const [x, y] = l.p(puntos[i]);
    ctx.lineTo(x, y);
  }
  ctx.stroke();
}

export function eje(ctx, l, { color = '#dcd8ce' } = {}) {
  ctx.strokeStyle = color;
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(l.px(l.xMin), l.py(0));
  ctx.lineTo(l.px(l.xMax), l.py(0));
  ctx.moveTo(l.px(0), l.py(l.yMin));
  ctx.lineTo(l.px(0), l.py(l.yMax));
  ctx.stroke();
}
