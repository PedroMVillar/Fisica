# -*- coding: utf-8 -*-
"""Verificación numérica independiente del Parcial 1 del 25/09/2025.
Corre con: python verificacion-parcial-1-2025.py   (solo necesita sympy)"""
import sympy as sp
from sympy import sqrt, sin, cos, pi, Rational, symbols, solve, Eq

def title(s): print("\n" + "=" * 70 + f"\n{s}\n" + "=" * 70)

# ------------------------------------------------------------ Problema 1 (g = 10)
title("P1: pelota con viento, g = 10 (= Practico 1, Ej. 15)")
t = symbols("t", real=True)
v0, ang, g = 24, pi / 6, 10
x = v0 * cos(ang) * t - t**2
y = v0 * sin(ang) * t - 5 * t**2
tmax = solve(sp.diff(y, t), t)[0]
print(f"  h_max = {float(y.subs(t, tmax)):.2f} m en t = {float(tmax):.2f} s")
tv = [s for s in solve(y, t) if s != 0][0]
print(f"  cae en t = {float(tv):.2f} s, x = {float(x.subs(t, tv)):.2f} m  (< 45 => no gol)")
tb = solve(Eq(v0 * cos(ang) * t, 45), t)[0]
print(f"  sin viento: x=45 en t = {float(tb):.3f} s, y = {float(y.subs(t, tb)):.3f} m (> 2.44 => por arriba, no gol)")

# ------------------------------------------------------------ Problema 2 (simbólico)
title("P2: choque elastico + tramo con rozamiento + resorte, h = 4 mu L")
m, gg, mu, L, k, l0 = symbols("m g mu_d L_BC k l_0", positive=True)
h = 4 * mu * L
vA = sqrt(2 * gg * h)                       # b1 llega a A
# choque elastico masas iguales: intercambio de velocidades
v2B = vA                                    # b2 sale con vA, b1 queda en reposo
print("  v_2B =", sp.simplify(v2B))
v2C_sq = sp.simplify(v2B**2 - 2 * mu * gg * L)
print("  v_2C^2 =", v2C_sq, " -> v_2C =", sp.simplify(sqrt(v2C_sq)))
xc = sp.simplify(sqrt(m * v2C_sq / k))
print("  compresion x =", xc, "   longitud l = l0 - x")
print("  W_resorte = -1/2 k x^2 =", sp.simplify(-Rational(1, 2) * k * xc**2))

# ------------------------------------------------------------ Problema 3
title("P3: A (40 N) sobre B (80 N), mu_d = 0.25 (= Practico 2, Ej. 19)")
f = 0.25 * 40
print(f"  T = f_AB = {f} N ; (b) F = {2*f} N ; (c) F = {2*f + 0.25*120} N")
