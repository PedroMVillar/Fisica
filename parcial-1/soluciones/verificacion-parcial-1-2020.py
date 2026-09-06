# -*- coding: utf-8 -*-
"""Verificación numérica independiente del Parcial 1 Recuperatorio del 26/11/2020.
Corre con: python verificacion-parcial-1-2020.py   (solo necesita sympy)"""
import math

def title(s): print("\n" + "=" * 70 + f"\n{s}\n" + "=" * 70)
g = 9.8

# ------------------------------------------------------------ Problema 1
title("P1: A 44.5 N sobre mesa (mu_e 0.20), B 22.2 N colgando, C sobre A")
WA, WB, mu = 44.5, 22.2, 0.20
WC = WB / mu - WA
print(f"  T = {WB} N ; N_mesa >= T/mu = {WB/mu:.1f} N -> W_C >= {WC:.1f} N -> m_C >= {WC/g:.2f} kg")

# ------------------------------------------------------------ Problema 2
title("P2: centro de masa de la L (origen en la bisagra, x a la derecha, y arriba)")
m1, m2, m3 = 4.0, 3.0, 2.0
M = m1 + m2 + m3
x0 = (m1 * (-0.75) + m2 * 0 + m3 * 0) / M
y0 = (m1 * 0 + m2 * (-0.9) + m3 * (-1.8)) / M
x1 = (m1 * (-0.75) + m2 * 0.9 + m3 * 1.8) / M
y1 = 0.0
print(f"  antes: ({x0:.3f}, {y0:.3f}) m   despues (barra vertical girada a la derecha): ({x1:.3f}, {y1:.3f}) m")
print(f"  desplazamiento: dx = {x1-x0:.3f} m, dy = {y1-y0:.3f} m")

# ------------------------------------------------------------ Problema 3
title("P3: canion de resorte (x = 0.5 m), proyectil 40 g a 30, pendulo balistico 500 g, L = 2 m, 10 grados")
mp, Mp, L, ang, xc = 0.040, 0.500, 2.0, math.radians(10), 0.50
h = L * (1 - math.cos(ang))
V = math.sqrt(2 * g * h)
K = 0.5 * (mp + Mp) * V**2
print(f"  (b) h = {h:.4f} m, V = {V:.4f} m/s, K despues = {K:.4f} J")
v = (mp + Mp) * V / mp
v0 = v / math.cos(math.radians(30))
print(f"  (d) v antes = {v:.2f} m/s   (e) v0 = {v0:.2f} m/s   K antes = {0.5*mp*v**2:.3f} J (vs {K:.3f} J despues)")
t = v0 * math.sin(math.radians(30)) / g
k = mp * v0**2 / xc**2
print(f"  (f) t = {t:.3f} s (altura max {v0**2*math.sin(math.radians(30))**2/(2*g):.2f} m, distancia horizontal {v*t:.2f} m)   (g) k = {k:.1f} N/m")
