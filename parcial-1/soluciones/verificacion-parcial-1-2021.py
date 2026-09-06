# -*- coding: utf-8 -*-
"""Verificación numérica independiente del Parcial 1 del 28/09/2021.
Corre con: python verificacion-parcial-1-2021.py   (solo necesita sympy)"""
import sympy as sp
from sympy import symbols, sin, cos, simplify
import math

def title(s): print("\n" + "=" * 70 + f"\n{s}\n" + "=" * 70)
g = 9.8

# ------------------------------------------------------------ Problema 1
title("P1: saque de Nadal")
m, vy0, h0, J = 0.056, -5.0, 2.5, 2.8
vx = J / m
tred = 11.9 / vx
yred = h0 + vy0 * tred - 0.5 * g * tred**2
print(f"  v_x = {vx:.1f} m/s   en la red (t = {tred:.3f} s): y = {yred:.3f} m vs 0.914 -> {'pasa' if yred > 0.914 else 'no pasa'}")
tland = (-vy0 - math.sqrt(vy0**2 + 2 * g * h0)) / (-g)
xland = vx * tland
print(f"  cae en t = {tland:.4f} s, x = {xland:.2f} m -> {xland-11.9:.2f} m despues de la red (limite 6.4) -> {'valido' if xland-11.9 <= 6.4 else 'afuera'}")

# ------------------------------------------------------------ Problema 2
title("P2: cuña en reposo, bloque sin rozamiento")
M, mm, al = symbols("M m alpha", positive=True)
N = mm * g * cos(al)
mu_min = simplify(N * sin(al) / (M * g + N * cos(al)))
print("  mu_e,min =", mu_min)

# ------------------------------------------------------------ Problema 3
title("P3: pendulo m1 = 2 kg, L = 3 m, choque elastico con m2 = 6 kg")
m1, m2, L = 2.0, 6.0, 3.0
v1 = math.sqrt(2 * g * L)
v1p = (m1 - m2) / (m1 + m2) * v1
v2p = 2 * m1 / (m1 + m2) * v1
print(f"  (b) W_peso = {m1*g*L:.1f} J   v1(B) = {v1:.3f} m/s")
print(f"  (c) v2' = {v2p:.3f} m/s (= v en C)   v1' = {v1p:.3f} m/s   (d) sube h = {v1p**2/(2*g):.3f} m = L/4 = {L/4}")
print(f"  check energia: {0.5*m1*v1**2:.2f} = {0.5*m1*v1p**2 + 0.5*m2*v2p**2:.2f}")
