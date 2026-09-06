# -*- coding: utf-8 -*-
"""Verificación numérica independiente del Parcial 1 del 28/09/2017.
Corre con: python verificacion-parcial-1-2017.py   (solo necesita sympy)"""
import sympy as sp
from sympy import symbols, sin, cos, pi, sqrt, solve, Eq, N
import math

def title(s): print("\n" + "=" * 70 + f"\n{s}\n" + "=" * 70)
g = 9.8

# ------------------------------------------------------------ Problema 1
title("P1: v0 = 30 m/s, R = 50 m hasta el borde, h = 20 m")
v0, R, h = 30.0, 50.0, 20.0
s2 = R * g / v0**2
th1, th2 = math.degrees(math.asin(s2)) / 2, (180 - math.degrees(math.asin(s2))) / 2
print(f"  (a) sen(2 theta) = {s2:.4f} -> theta = {th1:.2f} o {th2:.2f} -> theta_m = {th2:.2f} grados")
thm = math.radians(th2)
v = 2 * v0
vx, vy = v * math.cos(thm), v * math.sin(thm)
t = (vy + math.sqrt(vy**2 + 2 * g * h)) / g
print(f"  (b) con 2 v0: t = {t:.3f} s, x_B = {vx*t:.1f} m  (= {vx*t - R:.1f} m mas alla del borde)")
print(f"  (c) h_max 1 = {(v0*math.sin(thm))**2/(2*g):.1f} m   h_max 2 = {vy**2/(2*g):.1f} m")

# ------------------------------------------------------------ Problema 2
title("P2: = 2020 P1")
print(f"  m_C >= {(22.2/0.2 - 44.5)/g:.2f} kg")

# ------------------------------------------------------------ Problema 3
title("P3: theta = 3 t^2 + pi/4, R = 2")
t_ = symbols("t", positive=True)
th = 3 * t_**2 + pi / 4
tA = solve(Eq(th, 5 * pi / 4), t_)[0]
w, ga = sp.diff(th, t_), sp.diff(th, t_, 2)
wA = float(w.subs(t_, tA))
Rr = 2
print(f"  (b) t_A = {float(tA):.4f} s, omega = {wA:.3f} rad/s, gamma = {ga}")
print(f"      r = ({Rr*math.cos(5*math.pi/4):.3f}, {Rr*math.sin(5*math.pi/4):.3f})   v = ({-Rr*wA*math.sin(5*math.pi/4):.3f}, {Rr*wA*math.cos(5*math.pi/4):.3f})  |v| = {Rr*wA:.3f}")
an, at = Rr * wA**2, Rr * float(ga)
ax = -an * math.cos(5*math.pi/4) + at * (-math.sin(5*math.pi/4))
ay = -an * math.sin(5*math.pi/4) + at * math.cos(5*math.pi/4)
print(f"      a_n = {an:.2f}, a_t = {at:.1f}, a = ({ax:.2f}, {ay:.2f}), |a| = {math.hypot(ax, ay):.2f}")
t2 = solve(Eq(th, 2 * pi), t_)[0]
w2 = float(w.subs(t_, t2))
dth = w2**2 / (2 * 0.5)
print(f"  (c) t(2pi) = {float(t2):.4f} s, omega = {w2:.3f} rad/s -> frena en {dth:.2f} rad = {dth/(2*math.pi):.2f} vueltas, en {w2/0.5:.1f} s")
