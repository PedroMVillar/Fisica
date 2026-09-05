# -*- coding: utf-8 -*-
"""Verificación numérica independiente del Parcial 1 del 26/09/2024.
Corre con: python verificacion-parcial-1-2024.py   (solo necesita sympy)"""
import sympy as sp
from sympy import sqrt, sin, cos, tan, pi, rad, deg, atan, symbols, solve, Eq, Rational
import math

def title(s): print("\n" + "=" * 70 + f"\n{s}\n" + "=" * 70)

# ------------------------------------------------------------ Problema 1 (g = 10)
title("P1: golf, v0 = 48, 25 grados, pendiente 5 grados hacia abajo, g = 10")
t = symbols("t", positive=True)
v0, a, b, g = 48, rad(25), rad(5), 10
x = v0 * cos(a) * t
y = v0 * sin(a) * t - g * t**2 / 2
tmax = v0 * sin(a) / g
print(f"  (b) t_max = {float(tmax):.3f} s   h_max = {float(y.subs(t, tmax)):.2f} m")
tl = [s for s in solve(Eq(y, -x * tan(b)), t) if s != 0][0]
xl, yl = float(x.subs(t, tl)), float(y.subs(t, tl))
d = math.hypot(xl, yl)
print(f"  (c) t_llegada = {float(tl):.3f} s   x = {xl:.1f} m   y = {yl:.2f} m   d = {d:.1f} m (= x/cos5 = {xl/math.cos(math.radians(5)):.1f})")
vx, vy = float(v0 * cos(a)), float(v0 * sin(a) - g * tl)
print(f"  (d) v = ({vx:.2f}, {vy:.2f}) m/s   |v| = {math.hypot(vx, vy):.1f} m/s   angulo = {math.degrees(math.atan2(vy, vx)):.1f} grados")

# ------------------------------------------------------------ Problema 2 (g = 9.8)
title("P2: m1 = 1 kg gira con R = 1.5 m, m2 = 0.5 kg colgando")
g = 9.8
T = 0.5 * g
v = math.sqrt(T * 1.5 / 1)
print(f"  T = {T:.2f} N   v = {v:.2f} m/s   omega = {v/1.5:.2f} rad/s")

# ------------------------------------------------------------ Problema 3 (g = 9.8)
title("P3: resorte k = 450, m = 0.5, vB = 12, rizo R = 1, friccion 7 N")
m, k, R, vB, f = 0.5, 450.0, 1.0, 12.0, 7.0
xc = vB * math.sqrt(m / k)
print(f"  (a) x = {xc:.3f} m   (b) W = 1/2 k x^2 = {0.5*k*xc**2:.1f} J = 1/2 m vB^2 = {0.5*m*vB**2:.1f} J")
# energia en funcion del angulo theta desde B (arco R theta)
th = symbols("theta", positive=True)
v2 = vB**2 - 2 * g * R * (1 - cos(th)) - 2 * f * R * th / m
N = m * v2 / R + m * g * cos(th)
vT2 = float(v2.subs(th, pi))
print(f"  (c) v_T^2 = {vT2:.2f} -> v_T = {math.sqrt(vT2):.2f} m/s ; condicion g R = {g*R:.1f} -> {'llega' if vT2 >= g*R else 'se despega'}")
Nmin = min((float(N.subs(th, k_ * pi / 200)), k_ * 0.9) for k_ in range(0, 201))
print(f"  N minima en el rizo = {Nmin[0]:.2f} N en theta = {Nmin[1]:.0f} grados  (N(T) = {float(N.subs(th, pi)):.2f} N)")
