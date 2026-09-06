# -*- coding: utf-8 -*-
"""Verificación numérica independiente del Parcial 1 del 02/10/2014.
Corre con: python verificacion-parcial-1-2014.py   (solo necesita sympy)"""
import sympy as sp
from sympy import symbols, sqrt, simplify, cos, pi, Rational
import math

def title(s): print("\n" + "=" * 70 + f"\n{s}\n" + "=" * 70)

# ------------------------------------------------------------ Problema 1
title("P1: pendulo 2L a 60 grados, choque elastico, tramo L con mu_d = 0.8, caida L")
m, g, L = symbols("m g L", positive=True)
EA = m * g * 2 * L * (1 - cos(pi / 3))
print("  (a) E_A =", simplify(EA))
vB = sqrt(2 * g * L)
print("  (b) E_B =", simplify(Rational(1, 2) * m * vB**2), " v_B =", vB, " (tras el choque: pendulo en reposo, m sale con v_B)")
EC = simplify(EA - Rational(8, 10) * m * g * L)
vC = simplify(sqrt(2 * EC / m))
print("  (c) E_C =", EC, "  v_C =", vC)
tc = sqrt(2 * L / g)
print("  (d) x =", simplify(vC * tc), "=", float(simplify(vC * tc / L)), "L")
vimp = simplify(sqrt(vC**2 + 2 * g * L))
print("  (e) |v| =", vimp, "=", float(vimp / sqrt(g * L)), "sqrt(gL);  angulo bajo la horizontal =", math.degrees(math.atan(math.sqrt(2) / math.sqrt(0.4))), "grados")

# ------------------------------------------------------------ Problema 2
title("P2: doble plano, m1 = 20 (30 grados), m2 = 18 (60 grados), sin rozamiento")
gg = 9.8
m1, m2, al, be = 20.0, 18.0, math.radians(30), math.radians(60)
a = (m2 * math.sin(be) - m1 * math.sin(al)) * gg / (m1 + m2)
T = m1 * (gg * math.sin(al) + a)
print(f"  a = {a:.3f} m/s^2 (m2 baja, m1 sube)   T = {T:.1f} N   (check m2: {m2*gg*math.sin(be) - m2*a:.1f})")
