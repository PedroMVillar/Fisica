# -*- coding: utf-8 -*-
"""Verificación numérica independiente del Práctico 1 (Cinemática 1D y 2D).

Corre con: python verificacion-practico-1.py   (solo necesita sympy)
Cada bloque resuelve el ejercicio desde cero, sin copiar del .tex, para
contrastar los resultados de NotebookLM antes de pasarlos en limpio.
"""
import sympy as sp
from sympy import sqrt, Rational, pi, sin, cos, atan2, acos, deg, N

t = sp.symbols("t", real=True)
g = Rational(98, 10)

def title(s):
    print("\n" + "=" * 70 + f"\n{s}\n" + "=" * 70)

# ---------------------------------------------------------------- Ej 1
title("Ej 1: x(t) = -3 + 2 t^3")
x1 = -3 + 2 * t**3
v1 = sp.diff(x1, t)
for a, b in [(-1, Rational(-8, 10)), (Rational(-6, 10), Rational(6, 10)), (-1, 1)]:
    d = x1.subs(t, b) - x1.subs(t, a)  # v>=0 siempre => camino = desplazamiento
    print(f"  [{float(a):+.1f},{float(b):+.1f}]  d = {float(d):.3f} m   v_m = {float(d/(b-a)):.3f} m/s")
print(f"  v(0) = {v1.subs(t,0)}   v(0.8) = {float(v1.subs(t, Rational(8,10))):.2f} m/s")
print("  |x(t)-x(0)| = 1  ->  t =", [float(s) for s in sp.solve(sp.Eq(2*t**3, 1), t) if s.is_real],
      [float(s) for s in sp.solve(sp.Eq(2*t**3, -1), t) if s.is_real])

# ---------------------------------------------------------------- Ej 2
title("Ej 2: x(t) a trozos")
x2 = sp.Piecewise((t, t <= 4), (4, t <= 8), (4 + Rational(1, 2) * (t - 8) ** 2, True))
print("  v =", sp.piecewise_fold(sp.diff(x2, t)))
print("  a =", sp.piecewise_fold(sp.diff(x2, t, 2)))
print("  v(4-) =", sp.limit(sp.diff(x2, t), t, 4, '-'), "  v(4+) =", sp.limit(sp.diff(x2, t), t, 4, '+'))

# ---------------------------------------------------------------- Ej 4
title("Ej 4: x(t) = 3 + 17 t - 5 t^2")
x4 = 3 + 17 * t - 5 * t**2
v4 = sp.diff(x4, t)
print("  x(1,2,3) =", [x4.subs(t, k) for k in (1, 2, 3)])
raices = sp.solve(x4, t)
print("  x=0 en t =", [float(r) for r in raices])
print("  v(t) =", v4, "  v(1,2,3) =", [v4.subs(t, k) for k in (1, 2, 3)])
print("  v=0 en t =", sp.solve(v4, t), "  x_max =", x4.subs(t, sp.solve(v4, t)[0]))
t_or = max(raices)
print(f"  v(origen) = {float(v4.subs(t, t_or)):.3f} m/s")

# ---------------------------------------------------------------- Ej 5
title("Ej 5: auto (1.8) alcanza camion (1.2) cuando el camion recorrio 45 m")
ac, aa = Rational(12, 10), Rational(18, 10)
te = sp.solve(sp.Eq(ac * t**2 / 2, 45), t)[1]
d0 = aa * te**2 / 2 - 45
print(f"  t_enc = {float(te):.3f} s   d0 = {float(d0):.2f} m   v_auto = {float(aa*te):.2f}  v_camion = {float(ac*te):.2f} m/s")

# ---------------------------------------------------------------- Ej 6
title("Ej 6: tren 12 m/s, auto arranca en t=6 con a=2")
xtren = 12 * t
xauto = (t - 6) ** 2  # = 1/2 * 2 * (t-6)^2, valido t>=6
sol = [s for s in sp.solve(sp.Eq(xtren, xauto), t) if s > 6]
te6 = sol[0]
print(f"  t = {float(te6):.2f} s   x = {float(xauto.subs(t, te6)):.1f} m   v = {float(2*(te6-6)):.2f} m/s")

# ---------------------------------------------------------------- Ej 7
title("Ej 7: v en A, v/2 en B (3 m mas alto)")
v = sp.symbols("v", positive=True)
vA = sp.solve(sp.Eq((v / 2) ** 2, v**2 - 2 * g * 3), v)[0]
print(f"  v = {float(vA):.3f} m/s   (v^2 = {vA**2})")
print(f"  h sobre B = {float((vA/2)**2/(2*g)):.3f} m")
hA = sp.symbols("h_A", positive=True)
print("  v0 = sqrt(v^2 + 2 g h_A) =", sp.sqrt(vA**2 + 2 * g * hA), "  (si h_A = 0: v0 = v)")
print(f"  t_A->B = {float((vA - vA/2)/g):.3f} s   t_B->max = {float((vA/2)/g):.3f} s")

# ---------------------------------------------------------------- Ej 8
title("Ej 8: x = 3 t^2, y = 2 t^3")
r8 = sp.Matrix([3 * t**2, 2 * t**3])
v8, a8 = r8.diff(t), r8.diff(t, 2)
print("  v =", v8.T, "  a =", a8.T)
print(f"  |a(12)| = {float(a8.subs(t,12).norm()):.2f} m/s^2")
cosang = (v8.dot(a8) / (v8.norm() * a8.norm())).subs(t, 12)
print(f"  angulo(v,a) en t=12 = {float(deg(acos(cosang))):.2f} grados")
t1 = sp.solve(sp.Eq(a8[0], a8[1]), t)[0]
t2 = [s for s in sp.solve(sp.Eq(v8[0], v8[1]), t) if s != 0][0]
print(f"  t1 = {t1} s  (a // y=x)    t2 = {t2} s  (v // y=x)")
vm = (r8.subs(t, t2) - r8.subs(t, t1)) / (t2 - t1)
print("  v_media(t1,t2) =", vm.T, " |v_m| =", float(vm.norm()))

# ---------------------------------------------------------------- Ej 9
title("Ej 9: tiro horizontal desde 44 m con 25 m/s")
tv = sp.sqrt(2 * 44 / g)
print(f"  t_vuelo = {float(tv):.3f} s   alcance = {float(25*tv):.2f} m   |vy| = {float(g*tv):.2f} m/s")
print(f"  |v| final = {float(sqrt(25**2 + (g*tv)**2)):.2f} m/s")

# ---------------------------------------------------------------- Ej 12
title("Ej 12: Tierra alrededor del Sol")
vT, RT = 30e3, 150e9
print(f"  a_c = v^2/R = {vT**2/RT:.4e} m/s^2")

# ---------------------------------------------------------------- Ej 13
title("Ej 13: theta = 2 t^2, R = 1.5")
R = Rational(3, 2)
th = 2 * t**2
w, al = sp.diff(th, t), sp.diff(th, t, 2)
at, ac13 = al * R, w**2 * R
print("  omega =", w, "  alpha =", al, "  a_t =", at, "  a_c =", ac13, "  |a| =", sp.sqrt(at**2 + ac13**2))
print(f"  t=5: a_t = {at}  a_c = {ac13.subs(t,5)}  |a| = {float(sp.sqrt(at**2+ac13**2).subs(t,5)):.3f}")
print(f"  vueltas en 20 s = {float(th.subs(t,20)/(2*pi)):.2f}")

# ---------------------------------------------------------------- Ej 14
title("Ej 14: x = sin(wt), y = cos(wt)+1, w = 2 pi")
w14 = 2 * pi
r14 = sp.Matrix([sin(w14 * t), cos(w14 * t) + 1])
v14, a14 = r14.diff(t), r14.diff(t, 2)
print("  |v| =", sp.simplify(v14.norm()), "  |a| =", sp.simplify(a14.norm()))
print("  r.v =", sp.simplify(r14.dot(v14)), "  -> nulo cuando sin(2 pi t)=0: t = k/2")
print("  v.a =", sp.simplify(v14.dot(a14)), "  -> siempre perpendiculares")
print("  T =", 2 * pi / w14, "s")

# ---------------------------------------------------------------- Ej 15
title("Ej 15: pelota con viento, g = 10")
g15 = 10
v0, ang = 24, pi / 6
v0x, v0y = v0 * cos(ang), v0 * sin(ang)
x15 = v0x * t - t**2          # a_x = -2
y15 = v0y * t - 5 * t**2      # a_y = -10
print(f"  v0x = {float(v0x):.3f}  v0y = {float(v0y):.3f}")
tmax = sp.solve(sp.diff(y15, t), t)[0]
print(f"  h_max = {float(y15.subs(t, tmax)):.2f} m en t = {float(tmax):.2f} s")
tsuelo = [s for s in sp.solve(y15, t) if s != 0][0]
print(f"  cae en t = {float(tsuelo):.3f} s, x = {float(x15.subs(t, tsuelo)):.2f} m  (< 45 => no llega al arco)")
t45 = [float(s) for s in sp.solve(sp.Eq(x15, 45), t)]
print(f"  x=45 en t = {t45}  -> y = {[float(y15.subs(t, s)) for s in t45]}")
# sin viento
x15b = v0x * t
t45b = sp.solve(sp.Eq(x15b, 45), t)[0]
print(f"  sin viento: t(45 m) = {float(t45b):.3f} s, y = {float(y15.subs(t, t45b)):.3f} m  (> 2.44 => pasa por arriba)")
