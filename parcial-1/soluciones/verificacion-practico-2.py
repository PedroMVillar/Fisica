# -*- coding: utf-8 -*-
"""Verificación numérica independiente del Práctico 2 (Dinámica).

Corre con: python verificacion-practico-2.py   (solo necesita sympy)
Cada bloque resuelve el ejercicio desde cero, sin copiar del .tex.
"""
import sympy as sp
from sympy import sqrt, sin, cos, tan, pi, rad, deg, atan, acos, Rational, symbols, solve, Eq, N

g = Rational(98, 10)

def title(s):
    print("\n" + "=" * 70 + f"\n{s}\n" + "=" * 70)

# ---------------------------------------------------------------- Ej 1
title("Ej 1: bloque A (100 kg) en plano 30°, cuerda AB paralela (peso P), cuerda AC horizontal (Q=10 kg)")
mA, mQ, al = 100, 10, rad(30)
TC = mQ * g                       # tension horizontal, hacia la izquierda
P, Nn = symbols("P N", positive=True)
# eje u: paralelo al plano hacia arriba; eje n: normal saliente
eq_u = Eq(P - mA * g * sin(al) - TC * cos(al), 0)
eq_n = Eq(Nn - mA * g * cos(al) + TC * sin(al), 0)
sol = solve([eq_u, eq_n], [P, Nn])
print(f"  T_C = {float(TC):.1f} N   P = {float(sol[P]):.1f} N  (m_P = {float(sol[P]/g):.1f} kg)   N = {float(sol[Nn]):.1f} N")

# ---------------------------------------------------------------- Ej 2, 3
title("Ej 2 y 3: soga sin masa / con masa")
print("  Ej 2: a = 20/10 =", 20 / 10, "m/s^2")
M, m, F = symbols("M m F", positive=True)
a3 = F / (M + m)
print("  Ej 3: a =", a3, "  F_BC = M a =", sp.simplify(M * a3), "  F_BC/F =", sp.simplify(M * a3 / F))

# ---------------------------------------------------------------- Ej 4
title("Ej 4: A (8 kg) en plano 37°, B (4 kg) colgando")
mA4, mB4, al4 = 8, 4, rad(37)
print(f"  m_A g sen37 = {float(mA4*g*sin(al4)):.2f} N  vs  m_B g = {float(mB4*g):.2f} N  -> A baja, B sube")
a4 = (mA4 * g * sin(al4) - mB4 * g) / (mA4 + mB4)
T4 = mB4 * (g + a4)
print(f"  a = {float(a4):.3f} m/s^2   T = {float(T4):.2f} N   (con sen37=0.6: a = {float((mA4*g*Rational(6,10)-mB4*g)/12):.3f})")

# ---------------------------------------------------------------- Ej 5
title("Ej 5: bloques en contacto")
m1, m2, F5 = 2, 1, 3
a5 = Rational(F5, m1 + m2)
print(f"  a = {float(a5)} m/s^2   F sobre m1: contacto = m2 a = {float(m2*a5)} N ;  F sobre m2: contacto = m1 a = {float(m1*a5)} N")

# ---------------------------------------------------------------- Ej 6
title("Ej 6: bola 10 kg colgando, T_max 500 N")
m6, T6 = 10, 500
a6 = sqrt(T6**2 - (m6 * g) ** 2) / m6
print(f"  a_max = {float(a6):.2f} m/s^2   phi = {float(deg(acos(m6*g/T6))):.1f} grados")

# ---------------------------------------------------------------- Ej 7
title("Ej 7: tres bloques, T3 = 60 N")
m1_, m2_, m3_ = 20, 20, 30
a7 = Rational(60, m1_ + m2_ + m3_)
print(f"  horizontal: a = {float(a7):.3f}  T1 = {float(m1_*a7):.2f}  T2 = {float((m1_+m2_)*a7):.2f} N")
a7v = (60 - (m1_ + m2_ + m3_) * g) / (m1_ + m2_ + m3_)
print(f"  vertical:   a = {float(a7v):.3f} (hacia abajo)  T1 = {float(m1_*(g+a7v)):.2f}  T2 = {float((m1_+m2_)*(g+a7v)):.2f} N")

# ---------------------------------------------------------------- Ej 8
title("Ej 8: bloque de 5 N contra pared con F = 12 N")
print(f"  f_e,max = 0.6*12 = {0.6*12} N > 5 N -> no se mueve; fuerza de la pared = sqrt(12^2+5^2) = {float(sqrt(144+25))} N")

# ---------------------------------------------------------------- Ej 9
title("Ej 9: angulo optimo")
th, mu = symbols("theta mu", positive=True)
mm, FF = symbols("m F", positive=True)
a9 = (FF * cos(th) - mu * (mm * g - FF * sin(th))) / mm
print("  da/dtheta = 0 ->", sp.simplify(sp.diff(a9, th)), "  -> tan(theta) = mu ->", f"theta = {float(deg(atan(0.4))):.1f} grados")

# ---------------------------------------------------------------- Ej 10
title("Ej 10: dos bloques bajando por plano con rozamientos distintos")
mA_, mB_, muA, muB, alp = symbols("m_A m_B mu_A mu_B alpha", positive=True)
a10, T10 = symbols("a T")
eqA = Eq(mA_ * a10, mA_ * g * sin(alp) - muA * mA_ * g * cos(alp) - T10)   # A adelante: cuerda tira hacia atras
eqB = Eq(mB_ * a10, mB_ * g * sin(alp) - muB * mB_ * g * cos(alp) + T10)   # B atras: cuerda tira hacia adelante
s10 = solve([eqA, eqB], [a10, T10])
print("  a =", sp.simplify(s10[a10]))
print("  T =", sp.factor(s10[T10]))

# ---------------------------------------------------------------- Ej 11
title("Ej 11: dinamometro")
k11 = 2 / 0.117
print(f"  k = {k11:.2f} N/m   x(0.4 N) = {0.4/k11*100:.2f} cm")

# ---------------------------------------------------------------- Ej 12
title("Ej 12: dos resortes en paralelo, estirados 0.5 m, m = 2.5 kg")
print(f"  F_el = (50+100)*0.5 = {150*0.5} N   a = (75 - 2.5 g)/2.5 = {float((75 - 2.5*g)/2.5):.2f} m/s^2 hacia arriba")

# ---------------------------------------------------------------- Ej 14
title("Ej 14: resorte horizontal como fuerza centripeta")
k14, L0, m14 = 400, 0.5, 2
v14 = sqrt(k14 * (1 - L0) * 1 / m14)
print(f"  (a) v = {float(v14):.2f} m/s")
r = symbols("r", positive=True)
r14 = solve(Eq(k14 * (r - L0), m14 * (2 * v14) ** 2 / r), r)
print(f"  (b) v = {float(2*v14)} -> r = {[float(x) for x in r14]} m")

# ---------------------------------------------------------------- Ej 15
title("Ej 15: punto de fuerza neta nula Tierra-Luna")
MT, ML, d = 5.97e24, 7.35e22, 3.84e8
r15 = d / (1 + (ML / MT) ** 0.5)
print(f"  r = d/(1+sqrt(ML/MT)) = {r15:.3e} m = {r15/d:.3f} d")

# ---------------------------------------------------------------- Ej 16
title("Ej 16: triangulo equilatero")
G, mq, L = symbols("G m L", positive=True)
Fnet = 2 * G * mq**2 / L**2 * cos(pi / 6)
print("  |F| =", sp.simplify(Fnet), " hacia el baricentro;  g en baricentro = 0 por simetria (cada campo vale", sp.simplify(G * mq / (L / sqrt(3)) ** 2), ")")

# ---------------------------------------------------------------- Ej 17
title("Ej 17: MAS k=8, m=2, x0=0.40, x1=0.55")
w17 = sqrt(Rational(8, 2))
A17 = Rational(15, 100)
print(f"  omega = {w17} rad/s   T = {float(2*pi/w17):.3f} s   f = {float(w17/(2*pi)):.3f} Hz   A = {float(A17)} m")
print(f"  x(t) = 0.40 + 0.15 cos(2t);  v_max = A omega = {float(A17*w17)} m/s;  a_max = {float(A17*w17**2)} m/s^2; extremos 0.25 y 0.55 m")

# ---------------------------------------------------------------- Ej 18
title("Ej 18: cono alpha = 60°, l = 0.5 m, m = 0.12 kg, 10 rpm")
m18, l18, al18 = Rational(12, 100), Rational(1, 2), rad(60)
w18 = 10 * 2 * pi / 60
r18 = l18 * sin(al18)
v18 = w18 * r18
T18, N18 = symbols("T N")
s18 = solve([Eq(T18 * cos(al18) + N18 * sin(al18), m18 * g), Eq(T18 * sin(al18) - N18 * cos(al18), m18 * w18**2 * r18)], [T18, N18])
print(f"  omega = {float(w18):.4f} rad/s  r = {float(r18):.4f} m  v = {float(v18):.4f} m/s")
print(f"  T = {float(s18[T18]):.4f} N   N = {float(s18[N18]):.4f} N")
w0 = sqrt(g / (l18 * cos(al18)))
print(f"  N = 0 -> omega = sqrt(g/(l cos a)) = {float(w0):.3f} rad/s = {float(w0*60/(2*pi)):.1f} rpm")

# ---------------------------------------------------------------- Ej 19
title("Ej 19: A (40 N) sobre B (80 N), cuerda por polea, mu_d = 0.25")
fAB = 0.25 * 40
print(f"  f entre bloques = {fAB} N = T ;  (b) F = T + f = {2*fAB} N ;  (c) F = {2*fAB + 0.25*120} N")
