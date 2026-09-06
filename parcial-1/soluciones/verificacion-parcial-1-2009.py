# -*- coding: utf-8 -*-
"""Verificación numérica independiente del Parcial 1 del 10/09/2009.
Corre con: python verificacion-parcial-1-2009.py   (solo necesita sympy)"""
import sympy as sp
from sympy import symbols, sqrt, sin, cos, pi, simplify
import math

def title(s): print("\n" + "=" * 70 + f"\n{s}\n" + "=" * 70)

# ------------------------------------------------------------ Problema 1
title("P1: casa-banco-trabajo (km, h)")
tCB = 10 / 40
print(f"  CB: {tCB*60:.0f} min -> llega al banco 8:15; sale 8:45")
a = 2 * (20 - 10 * 0.75) / 0.75**2
vT = 10 + a * 0.75
print(f"  BT: a = {a:.2f} km/h^2 = {a*1000/3600**2:.5f} m/s^2 ; v final = {vT:.2f} km/h ; llega al trabajo 9:30 ; sale 11:30")
tTC = 1.5 / 2
print(f"  TC: 30 km en {tTC} h -> v = {30/tTC:.0f} km/h ; llega a casa 12:15")

# ------------------------------------------------------------ Problema 2
title("P2: plataforma R = 1 m, v = 30 m/s")
w0 = 30.0
ga = (15**2 - w0**2) / (2 * 4 * math.pi)
t = (15 - w0) / ga
print(f"  (a) omega0 = {w0} rad/s   (b) gamma = {ga:.2f} rad/s^2, t = {t:.3f} s   (c) v = 15 m/s, a = {15**2*1:.0f} m/s^2; angulos girados en 0.3 s y 1 s: {15*0.3} rad y {15*1} rad")

# ------------------------------------------------------------ Problema 3
title("P3: tiro a 30 grados a distancia R del borde (simbolico)")
R, g, h = symbols("R g h", positive=True)
v0 = sqrt(g * R / sin(pi / 3))
print("  (a) v_min =", v0)
print("  (b) t (hasta el borde) =", simplify(2 * v0 * sin(pi / 6) / g))
print("  (c) v impacto (al nivel del borde) = (", simplify(v0 * cos(pi / 6)), ",", simplify(-v0 * sin(pi / 6)), ")")
print("  (e)(f) con 45 grados: alcance =", simplify(v0**2 / g), "=", float(1 / math.sin(math.pi / 3)), "R")
