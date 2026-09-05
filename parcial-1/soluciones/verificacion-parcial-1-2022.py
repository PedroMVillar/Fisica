# -*- coding: utf-8 -*-
"""Verificación numérica independiente del Parcial 1 del 29/09/2022.
Corre con: python verificacion-parcial-1-2022.py   (solo necesita sympy)"""
import sympy as sp
from sympy import symbols, solve, Eq
import math

def title(s): print("\n" + "=" * 70 + f"\n{s}\n" + "=" * 70)
g = 9.8

# ------------------------------------------------------------ Problema 1
title("P1: chicle 10 g a 45 grados desde 1 m, lata 50 g a 3.5 m en la altura maxima")
mc, ml, dy = 0.010, 0.050, 3.5 - 1.0
v0 = math.sqrt(2 * g * dy / math.sin(math.radians(45)) ** 2)
tm = v0 * math.sin(math.radians(45)) / g
xl = v0 * math.cos(math.radians(45)) * tm
print(f"  (b) v0 = {v0:.2f} m/s   (c) t_max = {tm:.3f} s, x_lata = {xl:.2f} m")
vantes = v0 * math.cos(math.radians(45))
vdesp = mc * vantes / (mc + ml)
print(f"  (d) v antes = {vantes:.2f} m/s (horizontal)   v despues = {vdesp:.3f} m/s")
tc = math.sqrt(2 * 3.5 / g)
print(f"  (e) t caida = {tc:.3f} s   x total = {xl + vdesp*tc:.2f} m")
K1, K2 = 0.5 * mc * vantes**2, 0.5 * (mc + ml) * vdesp**2
print(f"  (f) K antes = {K1:.4f} J   K despues = {K2:.4f} J   perdida = {K1-K2:.4f} J ({100*(K1-K2)/K1:.0f}%)")

# ------------------------------------------------------------ Problema 2
title("P2: M1 = 0.5 kg en plano 30 grados, M2 = 0.6 kg colgando, mu_d 0.2, mu_e 0.4")
M1, M2, th, mud, mue = 0.5, 0.6, math.radians(30), 0.2, 0.4
F2, F1 = M2 * g, M1 * g * math.sin(th)
femax = mue * M1 * g * math.cos(th)
print(f"  (a) M2 g = {F2:.2f} N, M1 g sen30 = {F1:.2f} N, diferencia {F2-F1:.2f} N vs f_e,max = {femax:.3f} N -> {'se mueve (M2 baja)' if F2-F1 > femax else 'no se mueve'}")
a = (F2 - F1 - mud * M1 * g * math.cos(th)) / (M1 + M2)
T = M2 * (g - a)
print(f"  (c) a = {a:.3f} m/s^2   (d) T = {T:.3f} N   (check M1: {F1 + mud*M1*g*math.cos(th) + M1*a:.3f})")
print(f"  (e) equilibrio con M1 subiendo: M2/M1 = sen30 + mu_d cos30 = {math.sin(th) + mud*math.cos(th):.3f};  con M1 bajando: {math.sin(th) - mud*math.cos(th):.3f}")

# ------------------------------------------------------------ Problema 3
title("P3: m = 0.1 kg, k = 40, x = 0.10, AB = 2, R = 1, alpha = 30, mu_d = 0.5 despues de C")
m, k, x, R, al, mud = 0.1, 40.0, 0.10, 1.0, math.radians(30), 0.5
W = 0.5 * k * x**2
hC = R * (1 - math.cos(al))
KC = W - m * g * hC
vC = math.sqrt(2 * KC / m)
print(f"  (a) W_resorte = {W:.3f} J   (b) h_C = {hC:.4f} m, v_C = {vC:.3f} m/s")
s = KC / (m * g * (math.sin(al) + mud * math.cos(al)))
hD = hC + s * math.sin(al)
print(f"  (c) s sobre la rampa = {s:.4f} m, h_D = {hD:.4f} m   (d) W_roce = {-mud*m*g*math.cos(al)*s:.4f} J")
vA = math.sqrt(2 * W / m)
print(f"  (e) v_A = v_B = {vA:.2f} m/s -> a_n max en B (entrada al arco) = v^2/R = {vA**2/R:.2f} m/s^2 ; en C: {vC**2/R:.2f}")
