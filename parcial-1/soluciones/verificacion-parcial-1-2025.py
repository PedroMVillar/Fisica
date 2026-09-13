# -*- coding: utf-8 -*-
"""Verificación numérica independiente del Parcial 1 del 25/09/2025.
Corre con: python verificacion-parcial-1-2025.py   (solo necesita sympy)"""
import math
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

# ============================================================== bloques numericos
# Los tres bloques que siguen son la fuente que citan las notas del sitio: cada
# numero que aparece en una pagina tiene que salir de aca. Conviven con los
# bloques de arriba (P1/P3 numericos ya estaban, P2 solo simbolico); no los
# reemplazan. La numeracion P1/P2/P3 es la del PARCIAL, no la de la guia
# (P1 = guia 1 ej. 15, P2 = guia 3 sin numero de guia, P3 = guia 2 ej. 19).

# ------------------------------------------------------------ P1 (numerico)
v0n, angn_deg, gn = 24, 30, 10
ang_n = math.radians(angn_deg)
title(f"P1 (numerico): g = {gn} m/s^2 POR ENUNCIADO, v0 = {v0n} m/s, {angn_deg} grados, a_x = -2 m/s^2")
tmax_n = v0n * math.sin(ang_n) / gn
hmax_n = v0n * math.sin(ang_n) * tmax_n - 0.5 * gn * tmax_n**2
vx_n = v0n * math.cos(ang_n) - 2 * tmax_n
print(f"  h_max = {hmax_n:.2f} m en t = {tmax_n:.2f} s ; v_x alli = {vx_n:.4f} m/s")
tland_n = v0n * math.sin(ang_n) / 5
xland_n = v0n * math.cos(ang_n) * tland_n - tland_n**2
print(f"  con viento cae en x = {xland_n:.2f} m  -> le faltan {45 - xland_n:.2f} m para el arco")
tb_n = 45 / (v0n * math.cos(ang_n))
yb_n = v0n * math.sin(ang_n) * tb_n - 5 * tb_n**2
print(f"  sin viento, en x = 45 m (t = {tb_n:.4f} s) la pelota esta a y = {yb_n:.3f} m")
print(f"      -> pasa {yb_n - 2.44:.3f} m POR ENCIMA del travesano de 2.44 m")
print("  no convierte de ninguna de las dos maneras")

# ------------------------------------------------------------ P2 (numerico)
# Valores elegidos para el enunciado simbolico de arriba (la atadura del
# enunciado es h = 4 mu L_BC; el resto son elecciones, justificadas en el plan):
# mu_d = 0.25 (la misma del P3, una constante menos), L_BC = 2 m (se ve junto a
# una pista de ~10 m), m = 0.5 kg (una bolita), k = 200 N/m y l0 = 0.6 m (dan
# una compresion de 27 cm sobre un resorte de 60 cm: se ve, y no se cierra del
# todo). h = 2 m no se elige: sale de la atadura.
mu_n, L_n, m_n, k_n, l0_n, g2_n = 0.25, 2, 0.5, 200, 0.6, 9.8
h_n = 4 * mu_n * L_n
title(f"P2 (numerico): mu_d = {mu_n}, L_BC = {L_n} m, h = {h_n:g} m (= 4 mu L), m = {m_n} kg, k = {k_n} N/m")
v2B_n = math.sqrt(8 * g2_n * mu_n * L_n)
v2C_n = math.sqrt(6 * g2_n * mu_n * L_n)
print(f"  v_A = v_2B = {v2B_n:.4f} m/s      (cerrada sqrt(8 g mu L) = {math.sqrt(8*g2_n*mu_n*L_n):.4f})")
print(f"  v_2C = {v2C_n:.4f} m/s            (cerrada sqrt(6 g mu L) = {math.sqrt(6*g2_n*mu_n*L_n):.4f})")
xc_n = math.sqrt(m_n * v2C_n**2 / k_n)
l_n = l0_n - xc_n
print(f"  compresion x = {xc_n:.4f} m -> longitud l = {l_n:.4f} m sobre l0 = {l0_n} m")
Wres_n = -0.5 * k_n * xc_n**2
print(f"  W_resorte = {Wres_n:.4f} J        (cerrada -3 mu g L m = {-3*mu_n*g2_n*L_n*m_n:.4f} J)")
KB_n = 0.5 * m_n * v2B_n**2
disip_n = mu_n * m_n * g2_n * L_n
KC_n = 0.5 * m_n * v2C_n**2
residuo_n = KB_n - disip_n - KC_n
print(f"  balance: K_B {KB_n:.4f} - disipado {disip_n:.4f} = K_C {KC_n:.4f}  (residuo {residuo_n:+.1e})")

# Control genuino de v_2C (no una tautologia): la forma cerrada de arriba sale
# de v_2C^2 = v_2B^2 - 2 mu g L, asi que comprobarla sustituyendo esa misma
# igualdad seria circular. El camino distinto integra el tramo B->C paso a
# paso EN EL TIEMPO -- Euler explicito: v -= mu*g*dt, s += v*dt, arrancando en
# v_2B -- y compara la velocidad de cuando se recorre L_BC contra la v_2C de
# la forma cerrada. Implementacion y validacion de este patron: bloque
# "Ej 7 (numerico)" de verificacion-practico-3.py (rama Ejercicios-practicos).
#
# El residuo que da esto es SESGO del metodo, no ruido de punto flotante: el
# bucle suma v recien DESPUES de decrementarlo (Riemann por derecha), asi que
# en cada paso subcuenta la posicion recorrida en v*dt/2. Por eso a la version
# discreta le cuesta un pelin mas de tiempo llegar a L_BC que a la continua, y
# en ese pelin extra la velocidad sigue bajando: el resultado queda apenas por
# debajo de v_2C. Es O(dt): si alguien achica dt y ve bajar el residuo, eso NO
# prueba que "arreglo" nada -- el sesgo del metodo achica en la misma
# proporcion, nunca desaparece por eleccion de paso.
dt2 = 1e-4

def integrar_BC(mu_efectivo):
    v, s = v2B_n, 0.0
    while s < L_n:
        v -= mu_efectivo * g2_n * dt2
        s += v * dt2
    return v

v2C_euler = integrar_BC(mu_n)
print(f"  control temporal: Euler (dt={dt2}) desde v_2B con a=mu g -> "
      f"v al recorrer L_BC = {v2C_euler:.4f} m/s ; diff contra v_2C = {v2C_euler - v2C_n:+.2e} m/s")

# Diagnostico CORRIDO (no razonado): si el tramo se integrara con el doble del
# rozamiento real, la velocidad al llegar a L_BC ya no se acerca a v_2C -- el
# control se mueve, y mucho (el numero sale de correr el modelo roto, no de un
# comentario estatico, para que se recalcule solo en cada corrida).
v2C_euler_mal = integrar_BC(2 * mu_n)
print(f"  diagnostico (mu incorrecto = 2 mu_d): v al recorrer L_BC = {v2C_euler_mal:.4f} m/s ; "
      f"diff contra v_2C = {v2C_euler_mal - v2C_n:+.4f} m/s (el control se mueve)")

# ------------------------------------------------------------ P3 (numerico)
title("P3 (numerico): A (40 N) sobre B (80 N), mu_d = 0.25")
f_n = 0.25 * 40
print(f"  N_AB = 40.0 N ; f_AB = {f_n:.1f} N ; T = {f_n:.1f} N")
print(f"  (b) solo roce entre bloques: F = {2*f_n:.1f} N")
print(f"  (c) ademas roce con el piso (N = 120.0 N, f = {0.25*120:.1f} N): F = {2*f_n + 0.25*120:.1f} N")
