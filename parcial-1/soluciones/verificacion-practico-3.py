# -*- coding: utf-8 -*-
"""Verificación numérica independiente del Práctico 3 (Trabajo y Energía).

Corre con: python verificacion-practico-3.py   (solo necesita sympy)
Cada bloque resuelve el ejercicio desde cero, sin copiar del .tex.
"""
import sympy as sp
from sympy import (Eq, N, Rational, acos, cos, deg, pi, rad, sin, solve, sqrt,
                   symbols, tan)

g = Rational(98, 10)


def title(s):
    print("\n" + "=" * 74 + f"\n{s}\n" + "=" * 74)


# ---------------------------------------------------------------- Ej 1
title("Ej 1: pendulo L=1.32 m que engancha en un vertice a d=0.66 m del pivote")
L1, d1 = Rational(132, 100), Rational(66, 100)
thA = symbols("theta_A", positive=True)
vB_sym = sqrt(2 * g * L1 * (1 - cos(thA)))
print(f"  simbolico: v_B = sqrt(2 g L (1-cos th_A));  radio tras enganchar: L-d = {float(L1-d1)} m")
# 1-cos(th_C) = L/(L-d) (1-cos th_A) = 2 (1-cos th_A)  porque d = L/2
for grados in (5, 45, 50):
    th = rad(grados)
    vB = sqrt(2 * g * L1 * (1 - cos(th)))
    cthC = 1 - (L1 / (L1 - d1)) * (1 - cos(th))
    thC = acos(cthC)
    # T = m g + m v_B^2 / r , con r = L (antes) y r = L-d (despues)
    T_antes = g * (3 - 2 * cos(th))          # por unidad de masa
    T_desp = g * (5 - 4 * cos(th))           # por unidad de masa
    print(f"  th_A={grados:2d} deg -> v_B = {float(vB):.4f} m/s   th_C = {float(deg(thC)):.2f} deg"
          f"   T/m: antes {float(T_antes):.3f}  despues {float(T_desp):.3f} N/kg")
print("  (la tension salta al enganchar aunque v_B sea continua)")

# ---------------------------------------------------------------- Ej 2
title("Ej 2: bloque 20 kg, F(x) = 6x N a angulo th bajo la horizontal, de x=10 a x=20")
x, th2 = symbols("x theta", positive=True)
m2 = 20
W_F = sp.integrate(6 * x * cos(th2), (x, 10, 20))
print(f"  W_F = int_10^20 6x cos(th) dx = {sp.simplify(W_F)}")
Kf_sin = W_F
print(f"  (b-i)  mu=0    -> K_f = {sp.simplify(Kf_sin)}")
mu2 = Rational(5, 100)
Nx = m2 * g + 6 * x * sin(th2)               # F aprieta contra el piso
W_f = -sp.integrate(mu2 * Nx, (x, 10, 20))
print(f"  N(x) = {sp.simplify(Nx)}")
print(f"  W_roce = {sp.simplify(W_f)}")
print(f"  (b-ii) mu=0.05 -> K_f = {sp.simplify(Kf_sin + W_f)}")

# ---------------------------------------------------------------- Ej 3
title("Ej 3: m=1 kg baja 1 m por un plano de 30 grados")
m3, h3, al3 = 1, 1, rad(30)
s3 = h3 / sin(al3)
va = sqrt(2 * g * h3)
Wf3 = -Rational(3, 10) * m3 * g * cos(al3) * s3
vb = sqrt(2 * (m3 * g * h3 + Wf3) / m3)
print(f"  s sobre el plano = {float(s3)} m")
print(f"  (a) sin roce   v = sqrt(2gh) = {float(va):.4f} m/s")
print(f"  (b) con mu=0.3 W_roce = {float(Wf3):.4f} J -> v = {float(vb):.4f} m/s")
print(f"  (c) caida libre desde 1 m: v = {float(sqrt(2*g*h3)):.4f} m/s  (identico a (a): el peso es conservativo)")
print(f"  (d) perdida = {float(-Wf3):.4f} J   de los {float(m3*g*h3):.2f} J iniciales")

# ---------------------------------------------------------------- Ej 4
title("Ej 4: m=1 kg lanzada por resorte k=2 N/m comprimido 0.3 m, luego mu_d=0.2")
m4, k4, x4, mu4 = 1, 2, Rational(3, 10), Rational(2, 10)
W_el = Rational(1, 2) * k4 * x4**2
v4 = sqrt(2 * W_el / m4)
print(f"  (b) W_resorte = k x^2/2 = {float(W_el)} J")
print(f"  (c) v = {float(v4):.6f} m/s  (= 0.3*sqrt(2))")
K_i, K_f = W_el, Rational(1, 2) * m4 * (v4 / 2) ** 2
print(f"  (d) K_i = {float(K_i)} J ; K(v/2) = K_i/4 = {float(K_f)} J -> W_roce = {float(K_f-K_i)} J")
d4 = W_el / (mu4 * m4 * g)
print(f"  (e) f = mu m g = {float(mu4*m4*g)} N ; d = {float(d4):.6f} m = {float(d4*100):.2f} cm")

# ---------------------------------------------------------------- Ej 5
title("Ej 5: m=5 kg sobre resorte vertical k=2 N/m")
m5, k5, h5 = 5, 2, 1
xeq = m5 * g / k5
W_res = Rational(1, 2) * k5 * xeq**2
print(f"  x_eq = m g / k = {float(xeq)} m")
print(f"  (b) W sobre el resorte = k x_eq^2/2 = {float(W_res)} J")
print(f"      trabajo del peso = m g x_eq = {float(m5*g*xeq)} J ; la mano aporta {float(W_res - m5*g*xeq)} J")
xs = symbols("x", positive=True)
sol5 = solve(Eq(m5 * g * (h5 + xs), Rational(1, 2) * k5 * xs**2), xs)
xmax = max(sol5)
print(f"  (c) m g (h+x) = k x^2/2  ->  x = {float(xmax):.4f} m (desde la longitud natural)")
print(f"      medido desde el equilibrio: x - x_eq = {float(xmax - xeq):.4f} m")

# ---------------------------------------------------------------- Ej 6
title("Ej 6: embalaje 250 kg colgado de L=10 m, apartado l=1 m de la vertical")
m6, L6, l6 = 250, 10, 1
F6 = m6 * g * l6 / sqrt(L6**2 - l6**2)
dh6 = L6 - sqrt(L6**2 - l6**2)
print(f"  sen th = l/L = {float(Rational(l6,L6))} -> th = {float(deg(sp.asin(Rational(l6,L6)))):.2f} deg")
print(f"  (a) F = m g tan(th) = {float(F6):.2f} N")
print(f"  (b) sostenerlo: desplazamiento nulo -> W = 0")
print(f"  (c) subio dh = L - sqrt(L^2-l^2) = {float(dh6):.6f} m -> W = m g dh = {float(m6*g*dh6):.2f} J")
print(f"      (ojo: F*l = {float(F6*l6):.1f} J NO es la respuesta: F no es constante)")
print(f"  (d) la tension es perpendicular a la velocidad en todo instante -> W_T = 0")

# ---------------------------------------------------------------- Ej 7
title("Ej 7: montana rusa sin friccion, A y B a altura h, C a h/2, frenado en L")
m7, v0, h7, L7 = symbols("m v_0 h L", positive=True)
E7 = Rational(1, 2) * m7 * v0**2 + m7 * g * h7
print(f"  (a) E = {E7}")
vB7 = sp.sqrt(sp.solve(Eq(Rational(1,2)*m7*symbols('vB')**2 + m7*g*h7, E7), symbols('vB')**2)[0]) \
      if False else v0
print(f"  (b) v_B = v_0 (misma altura)   v_C = sqrt(v_0^2 + g h)")
vC7 = sqrt(v0**2 + g * h7)
print(f"      v_C = {vC7}")
vD7sq = v0**2 + 2 * g * h7
a7 = vD7sq / (2 * L7)
print(f"  (c) v_D^2 = {vD7sq} ;  a = v_D^2/(2L) = {a7}")

# ---------------------------------------------------------------- Ej 8
title("Ej 8: cuadrante R=1.5 m, m=1 kg, v_B=3.6 m/s, luego d=2.7 m hasta parar")
R8, m8, vB8, d8 = Rational(3, 2), 1, Rational(36, 10), Rational(27, 10)
mu8 = vB8**2 / (2 * g * d8)
print(f"  (a) 1/2 m v_B^2 = mu m g d -> mu = v_B^2/(2 g d) = {float(mu8):.6f}")
W8 = Rational(1, 2) * m8 * vB8**2 - m8 * g * R8
print(f"  (b) K_B = {float(Rational(1,2)*m8*vB8**2):.3f} J ; W_peso = m g R = {float(m8*g*R8):.3f} J")
print(f"      W_roce(arco) = K_B - m g R = {float(W8):.3f} J  ->  contra el roce: {float(-W8):.3f} J")

# ---------------------------------------------------------------- Ej 9
title("Ej 9: m=2 kg cae desde h=100 m")
m9, h9 = 2, 100
J1 = m9 * g * 1
tcl = sqrt(2 * h9 / g)
print(f"  (a) primer segundo:  J = m g Dt = {float(J1)} N s (hacia abajo)")
print(f"  (b) segundo segundo: J = {float(J1)} N s, identico (la fuerza es constante)")
print(f"  (c) t_cl = sqrt(2h/g) = {float(tcl):.4f} s -> J = m g t_cl = {float(m9*g*tcl):.3f} N s")
print(f"      control: m v_final = m sqrt(2 g h) = {float(m9*sqrt(2*g*h9)):.3f} N s")

# ---------------------------------------------------------------- Ej 10
title("Ej 10: choque elastico frontal, masas iguales, se pide v_A' = 0")
v10, u10 = symbols("v u")
vA2, vB2 = symbols("vAp vBp")
sol10 = solve([Eq(v10 + u10, vA2 + vB2),                       # cantidad de movimiento
               Eq(v10**2 + u10**2, vA2**2 + vB2**2)],          # energia cinetica
              [vA2, vB2], dict=True)
print("  soluciones del sistema (descartando la trivial sin choque):")
for s in sol10:
    print(f"    vA' = {sp.simplify(s[vA2])}   vB' = {sp.simplify(s[vB2])}")
print(f"  la solucion no trivial es el intercambio: vA' = u, vB' = v")
print(f"  imponer vA' = 0  ->  u = 0  (B tenia que estar en reposo)")

# ---------------------------------------------------------------- Ej 11
title("Ej 11: bala 10 g atraviesa m1=1.2 kg y se incrusta en m2=1.8 kg")
mb, m1_, m2_ = Rational(1, 100), Rational(12, 10), Rational(18, 10)
v1_, v2_ = Rational(63, 100), Rational(14, 10)
vm = (mb + m2_) * v2_ / mb
vi = (m1_ * v1_ + mb * vm) / mb
print(f"  (a) choque con el bloque 2 (perfectamente inelastico): mb vm = (mb+m2) v2")
print(f"      vm = {float(vm):.2f} m/s")
print(f"  (b) paso por el bloque 1: mb vi = m1 v1 + mb vm")
print(f"      vi = {float(vi):.2f} m/s")
print(f"      control: la bala pierde {float(vi-vm):.2f} m/s -> Dp = {float(mb*(vi-vm)):.4f} kg m/s")
print(f"               el bloque 1 se lleva m1 v1 = {float(m1_*v1_):.4f} kg m/s  (coinciden)")

# ---------------------------------------------------------------- Ej 12
title("Ej 12: cuerpo m con velocidad v se parte en dos mitades, una con v/3")
mm, vv = symbols("m v", positive=True)
uu = symbols("u")
sol12 = solve(Eq(mm * vv, (mm / 2) * (vv / 3) + (mm / 2) * uu), uu)[0]
print(f"  conservacion de p:  u = {sp.simplify(sol12)}")
Ki = Rational(1, 2) * mm * vv**2
Kf = Rational(1, 2) * (mm / 2) * (vv / 3) ** 2 + Rational(1, 2) * (mm / 2) * sol12**2
print(f"  K_i = {Ki}   K_f = {sp.simplify(Kf)}   K_f/K_i = {sp.simplify(Kf/Ki)} = {float(sp.simplify(Kf/Ki)):.4f}")
print("  la energia cinetica aumenta: la aporto la explosion (fuerzas internas)")

print("\n" + "=" * 74)
print("Fin. Todos los bloques resueltos de forma independiente al .tex.")
print("=" * 74)
