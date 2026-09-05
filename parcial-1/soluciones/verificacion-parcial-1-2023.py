# -*- coding: utf-8 -*-
"""Verificación numérica independiente del Parcial 1 del 28/09/2023.
Corre con: python verificacion-parcial-1-2023.py   (solo necesita sympy)"""
import sympy as sp
from sympy import sqrt, sin, cos, pi, rad, symbols, solve, Eq
import math

def title(s): print("\n" + "=" * 70 + f"\n{s}\n" + "=" * 70)

# ------------------------------------------------------------ Problema 1 (g = 10)
title("P1: canion 250 m/s a 30 grados, muralla 5 m a 5 km, g = 10")
t = symbols("t", positive=True)
v0, a, g = 250, rad(30), 10
x = v0 * cos(a) * t
y = v0 * sin(a) * t - g * t**2 / 2
print(f"  (b) h_max = {float((v0*sin(a))**2/(2*g)):.2f} m")
tv = solve(y, t)[0]
print(f"  (c) t_vuelo = {float(tv):.1f} s   alcance = {float(x.subs(t, tv)):.1f} m")
tm = solve(Eq(x, 5000), t)[0]
print(f"  (d) en x = 5000: t = {float(tm):.2f} s, y = {float(y.subs(t, tm)):.1f} m  (>> 5 m: pasa por encima, no impacta)")

# ------------------------------------------------------------ Problema 2 (g = 10)
title("P2: A (2 kg, 45 grados, mu 0.05) - B (5 kg, 30 grados, mu 0.1), g = 10")
mA, mB, al, be, muA, muB = 2, 5, rad(45), rad(30), 0.05, 0.1
FA, FB = float(mA * g * sin(al)), float(mB * g * sin(be))
print(f"  (a) m_A g sen45 = {FA:.2f} N  vs  m_B g sen30 = {FB:.2f} N -> B baja, A sube")
fA, fB = float(muA * mA * g * cos(al)), float(muB * mB * g * cos(be))
acc = (FB - FA - fA - fB) / (mA + mB)
T = FA + fA + mA * acc
print(f"  (c) f_A = {fA:.3f} N  f_B = {fB:.3f} N  a = {acc:.3f} m/s^2   T = {T:.2f} N   (check B: {FB - fB - mB*acc:.2f} = T)")

# ------------------------------------------------------------ Problema 3 (g = 9.8)
title("P3: plano 30 grados, k = 500, m = 2.5, d = 0.30, v = 0.75 hacia abajo")
g = 9.8
m, k, d, v, th = 2.5, 500.0, 0.30, 0.75, math.radians(30)
v1 = math.sqrt(v**2 + 2 * g * math.sin(th) * d)
W = m * g * math.sin(th) * d
print(f"  (a) v1 = {v1:.3f} m/s   W_peso = {W:.3f} J (> 0)")
xx = symbols("x", positive=True)
sol = solve(Eq(0.5 * m * v1**2 + m * g * math.sin(th) * xx, 0.5 * k * xx**2), xx)
xm = float(sol[0])
print(f"  (b) x_max = {xm:.4f} m   W_resorte = {-0.5*k*xm**2:.3f} J (< 0)   W_peso en la compresion = {m*g*math.sin(th)*xm:.3f} J")
