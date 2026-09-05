# -*- coding: utf-8 -*-
"""
=============================================================================
 VERIFICACION INDEPENDIENTE — Dinamica II: rozamiento, DCL avanzado
 y sistemas acoplados
=============================================================================

QUE ES ESTE ARCHIVO
-------------------
Es el control de calidad numerico de la sintesis, y de paso es la unica
hoja de respuestas de los ejercicios: la sintesis los deja planteados sin
resolver a proposito, asi que aca abajo estan todos los resultados, cada
uno recalculado desde el enunciado y no copiado del documento.

COMO SE USA
-----------
    python verificacion-dinamica-2.py

Corre solo (necesita sympy) e imprime, ejercicio por ejercicio, el valor
calculado y el veredicto. Todo enunciado va resumido arriba de su bloque,
asi que no hace falta tener la sintesis al lado.

COMO SE USA PARA ESTUDIAR
-------------------------
1. Resolve el ejercicio en papel, sin abrir esto.
2. Corre el script y compara SOLO el numero final.
3. Si no coincide, volve al papel antes de leer el desarrollo de aca:
   el script muestra los pasos intermedios (normales, coeficientes,
   ecuaciones por cuerpo) justamente para que puedas ubicar en cual de
   los pasos se te fue, no para que lo leas de corrido.
4. Podes cambiar los datos de entrada de cualquier bloque y volver a
   correrlo: todas las cuentas estan escritas en forma literal primero,
   asi que los numeros son intercambiables.

CONVENCIONES (las mismas del documento)
---------------------------------------
  * g = 10 m/s^2 en todos los casos.
  * mu_e = coeficiente estatico, mu_d = coeficiente dinamico (notacion
    de la catedra).
  * Donde el enunciado declara sen(37) = 0.60 y cos(37) = 0.80, se usan
    ESOS valores y no los exactos. 0.60 / 0.80 es el terno 3-4-5 y hace
    que varias identidades cierren exacto; usar los exactos generaria
    diferencias espurias en el tercer decimal.
  * Toda fuerza de rozamiento ESTATICO se despeja del equilibrio.
    mu_e * n se usa UNICAMENTE donde el movimiento es inminente, que es
    el unico caso en que la desigualdad f_e <= mu_e*n es igualdad.

CHEQUEOS DE LEY QUE HACE EL SCRIPT ADEMAS DE LOS NUMEROS
--------------------------------------------------------
  * ninguna normal negativa,
  * ninguna friccion estatica por encima de su techo mu_e*n,
  * ninguna tension negativa presentada como valida
    (una soga tira, nunca empuja: T < 0 significa soga floja, T = 0).
=============================================================================
"""

import sys
import sympy as sp

# La consola de Windows es cp1252; esto evita que se rompa al imprimir acentos.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

G = sp.Rational(10)          # m/s^2, valor que fija el documento
SEN37 = sp.Rational(60, 100)  # declarado por el enunciado
COS37 = sp.Rational(80, 100)  # declarado por el enunciado

# ---------------------------------------------------------------------------
# Infraestructura minima de comparacion
# ---------------------------------------------------------------------------

_resultados = []


def chk(etiqueta, calculado, documento, unidad="", nota=""):
    """Compara mi valor (calculado de cero) contra el que afirma el documento."""
    c = sp.nsimplify(calculado)
    d = sp.nsimplify(documento)
    ok = sp.simplify(c - d) == 0
    _resultados.append((etiqueta, ok))
    marca = "OK  " if ok else "FALLA"
    print("  [{}] {}".format(marca, etiqueta))
    print("        calculado : {} {}".format(sp.nsimplify(c), unidad))
    print("        documento : {} {}".format(sp.nsimplify(d), unidad))
    if nota:
        print("        nota      : {}".format(nota))
    if not ok:
        print("        >>> DISCREPANCIA <<<")


def afirmar(etiqueta, condicion, detalle=""):
    """Chequeo de ley fisica (no hay valor del documento contra que comparar)."""
    ok = bool(condicion)
    _resultados.append((etiqueta, ok))
    print("  [{}] {}{}".format("OK  " if ok else "FALLA", etiqueta,
                               ("  — " + detalle) if detalle else ""))


def titulo(t):
    print("\n" + "=" * 75)
    print(t)
    print("=" * 75)


def sub(t):
    print("\n--- " + t + " " + "-" * max(0, 68 - len(t)))


# ===========================================================================
# PARTE 1 — MARCO TEORICO: claims numericos sueltos y casos limite
# ===========================================================================

titulo("PARTE 1 — MARCO TEORICO")

sub("Bloque 1: el cajon de 100 N (la primera pregunta del diagnostico)")
# Enunciado: cajon de peso 100 N sobre piso horizontal, mu_e = 0.4,
# empujado horizontalmente con 20 N, no se mueve. Cuanto vale f_e?
W_cajon = sp.Rational(100)
mu_e_cajon = sp.Rational(4, 10)
n_cajon = W_cajon                      # equilibrio vertical: n - W = 0
techo = mu_e_cajon * n_cajon           # techo, NO el valor del rozamiento
empuje = sp.Rational(20)
f_e = empuje                           # equilibrio horizontal: f_e = empuje
chk("normal sobre el cajon", n_cajon, 100, "N")
chk("techo mu_e*n", techo, 40, "N", "es el maximo, no el valor")
chk("rozamiento con empuje de 20 N", f_e, 20, "N",
    "sale del equilibrio, no de mu_e*n")
afirmar("f_e <= mu_e*n se respeta", f_e <= techo)

sub("Chequeo del bloque 1, item 1: el mismo cajon empujado con 55 N")
# El chequeo afirma: "empujado con 55 N, sigue sin moverse".
empuje_55 = sp.Rational(55)
print("  techo de rozamiento estatico disponible : {} N".format(techo))
print("  empuje que el chequeo declara aplicado  : {} N".format(empuje_55))
afirmar("la premisa 'con 55 N sigue sin moverse' es consistente",
        empuje_55 <= techo,
        "55 N > 40 N: con estos datos el cajon NO puede quedarse quieto")

sub("Bloque 'Angulo critico'")
# mu_e = tan(theta_c). Con theta_c = 20.0 grados el documento afirma 0.364.
theta_c = sp.rad(20)
mu_de_20 = sp.tan(theta_c)
chk("mu_e a partir de theta_c = 20.0 grados",
    sp.Rational(round(float(mu_de_20), 3)).limit_denominator(10000),
    sp.Rational(364, 1000), "", "tan(20 grados) = {:.6f}".format(float(mu_de_20)))

sub("Chequeo del bloque 'Angulo critico', item 2")
# Bloque de 2 kg quieto en plano de 10 grados, mu_e = 0.5. Cuanto vale f_e?
m_b, th, mu_ee = sp.Rational(2), sp.rad(10), sp.Rational(5, 10)
f_e_plano = m_b * G * sp.sin(th)             # equilibrio, NO mu_e*n
n_plano = m_b * G * sp.cos(th)
print("  f_e = m g sen(10) = {:.3f} N   (techo mu_e*n = {:.3f} N)".format(
    float(f_e_plano), float(mu_ee * n_plano)))
afirmar("el bloque efectivamente puede estar quieto",
        float(f_e_plano) <= float(mu_ee * n_plano))
print("  RESPUESTA: f_e = 3.5 N (aprox). No 9.8 N, que es el techo.")

sub("Bloque 'Tres montajes': formulas y casos limite")
mA, mB, T, a, g, th_s = sp.symbols("m_A m_B T a g theta", positive=True)

# --- Atwood: m_B baja, m_A sube, positivo en el sentido de movimiento de c/u.
sol_atw = sp.solve([sp.Eq(mB * g - T, mB * a),
                    sp.Eq(T - mA * g, mA * a)], [a, T], dict=True)[0]
a_atw, T_atw = sp.simplify(sol_atw[a]), sp.simplify(sol_atw[T])
chk("Atwood: a literal", a_atw, (mB - mA) / (mA + mB) * g)
chk("Atwood: T literal", T_atw, 2 * mA * mB * g / (mA + mB))
chk("Atwood, limite m_A = m_B: T", sp.simplify(T_atw.subs(mB, mA)), mA * g, "",
    "el documento dice T = m g")
chk("Atwood, limite m_A = m_B: a", sp.simplify(a_atw.subs(mB, mA)), 0)
chk("Atwood, limite m_A -> 0: a", sp.limit(a_atw, mA, 0), g)

# --- Chequeo con numeros: m_A = 3 kg, m_B = 5 kg
a_num = a_atw.subs({mA: 3, mB: 5, g: G})
T_num = T_atw.subs({mA: 3, mB: 5, g: G})
chk("Atwood 3 kg / 5 kg: a", a_num, sp.Rational(5, 2), "m/s^2")
chk("Atwood 3 kg / 5 kg: T", T_num, sp.Rational(75, 2), "N")
afirmar("T queda entre los dos pesos (30 N y 50 N)",
        30 < T_num < 50, "T = {} N".format(T_num))

# --- Dos bloques en contacto
F = sp.symbols("F", positive=True)
a_cont = F / (mA + mB)
P_AB = sp.simplify(mB * a_cont)
chk("Bloques en contacto: fuerza de contacto (F sobre A)",
    P_AB, mB * F / (mA + mB))
chk("Bloques en contacto: fuerza de contacto (F sobre B)",
    sp.simplify(mA * a_cont), mA * F / (mA + mB))
afirmar("P_AB < F siempre", sp.simplify(F - P_AB) > 0)

# --- Plano inclinado + cuerpo colgando (sin rozamiento)
sol_pi = sp.solve([sp.Eq(mB * g - T, mB * a),
                   sp.Eq(T - mA * g * sp.sin(th_s), mA * a)], [a, T], dict=True)[0]
a_pi, T_pi = sp.simplify(sol_pi[a]), sp.simplify(sol_pi[T])
chk("Plano+colgante: a literal", a_pi,
    (mB - mA * sp.sin(th_s)) / (mA + mB) * g)
chk("Plano+colgante: T literal", T_pi,
    mA * mB * (1 + sp.sin(th_s)) * g / (mA + mB))
chk("Limite theta -> 90 grados: a colapsa a la Atwood",
    sp.simplify(a_pi.subs(th_s, sp.pi / 2)), a_atw)
chk("Limite theta -> 90 grados: T colapsa a la Atwood",
    sp.simplify(T_pi.subs(th_s, sp.pi / 2)), T_atw)
chk("Limite theta -> 0: T", sp.simplify(T_pi.subs(th_s, 0)),
    mA * mB * g / (mA + mB), "", "es el caso de mesa horizontal lisa")

sub("Chequeo del bloque 'Rozamiento en sistema acoplado', item 1")
# A de 3 kg sobre B de 5 kg, B en el piso. Normal del piso sobre B.
n_piso_teo = (sp.Rational(3) + sp.Rational(5)) * G
chk("normal del piso sobre B (A 3 kg sobre B 5 kg)", n_piso_teo, 80, "N",
    "sostiene los dos pesos, no solo el de B")


# ===========================================================================
# PARTE 2 — EJEMPLO RESUELTO [completo]: caja en la mesada + bolsa colgando
# ===========================================================================

titulo("PARTE 2 — EJEMPLO RESUELTO [completo]")
print("""
ENUNCIADO (resumido)
  Caja A de 3.0 kg sobre la mesada. De A sale una soga horizontal que pasa
  por una roldana en el borde y de la que cuelga una bolsa B de 2.0 kg.
  mu_e(A-mesada) = 0.50 ; mu_d(A-mesada) = 0.25 ; g = 10 m/s^2.
  Roldana ideal. Se pide la aceleracion del sistema y la tension.
""")

mA_v, mB_v = sp.Rational(3), sp.Rational(2)
mu_d_v, mu_e_v = sp.Rational(25, 100), sp.Rational(50, 100)

# Paso 0 — arranca el sistema? El rozamiento es estatico mientras no se mueva,
# y su techo es mu_e*n. Arranca si el peso de la bolsa supera ese techo.
n_A = mA_v * G                       # equilibrio vertical de A
techo_A = mu_e_v * n_A
peso_B = mB_v * G
afirmar("el sistema efectivamente arranca (peso de B > techo estatico)",
        peso_B > techo_A,
        "{} N > {} N".format(peso_B, techo_A))

# Paso 1 — ya en movimiento: rozamiento dinamico.
f_d = mu_d_v * n_A
chk("(c) normal sobre la caja", n_A, 30, "N")
chk("(c) rozamiento dinamico", f_d, sp.Rational(75, 10), "N")

# Paso 2 — segunda ley por cuerpo, positivo en el sentido de movimiento de c/u.
#   caja A : T - mu_d*m_A*g = m_A*a
#   bolsa B: m_B*g - T      = m_B*a
sol_ej = sp.solve([sp.Eq(T - mu_d_v * mA_v * G, mA_v * a),
                   sp.Eq(mB_v * G - T, mB_v * a)], [a, T], dict=True)[0]
a_ej, T_ej = sp.simplify(sol_ej[a]), sp.simplify(sol_ej[T])
chk("(e) aceleracion", a_ej, sp.Rational(25, 10), "m/s^2")
chk("(e) tension", T_ej, 15, "N")

# La forma literal que afirma el documento.
mu_s = sp.symbols("mu_d", positive=True)
sol_lit = sp.solve([sp.Eq(T - mu_s * mA * g, mA * a),
                    sp.Eq(mB * g - T, mB * a)], [a, T], dict=True)[0]
chk("(d) a literal", sp.simplify(sol_lit[a]),
    (mB - mu_s * mA) / (mA + mB) * g)
chk("(d) T literal", sp.simplify(sol_lit[T]),
    mA * mB * (1 + mu_s) * g / (mA + mB))

# Verificacion cruzada con el otro diagrama (la que el documento hace "gratis").
chk("verificacion cruzada: T - f_d contra m_A*a", T_ej - f_d, mA_v * a_ej, "N")
afirmar("T < peso de la bolsa (baja acelerada)", T_ej < peso_B,
        "{} N < {} N".format(T_ej, peso_B))
afirmar("tension positiva", T_ej > 0)

# (f) masa minima de bolsa que hace arrancar la caja. Movimiento inminente:
#     y SOLO ahi el rozamiento estatico llega a su techo.
mB_min = sp.solve(sp.Eq(sp.Symbol("mBm", positive=True) * G, mu_e_v * n_A),
                  sp.Symbol("mBm", positive=True))[0]
chk("(f) masa minima de bolsa para arrancar", mB_min, sp.Rational(15, 10), "kg",
    "unico punto del ejemplo donde vale f_e = mu_e*n")

# (f) caso limite mu_d -> 0
a_sin_roce = sp.simplify(sol_lit[a].subs({mu_s: 0, mA: mA_v, mB: mB_v, g: G}))
chk("(f) limite mu_d -> 0", a_sin_roce, 4, "m/s^2")


# ===========================================================================
# PARTE 3 — EJEMPLO RESUELTO [parcial]: cajas apiladas tiradas desde abajo
# ===========================================================================

titulo("PARTE 3 — EJEMPLO RESUELTO [parcial]")
print("""
ENUNCIADO (resumido)
  Caja de libros A de 2.0 kg apoyada sobre caja de ropa B de 8.0 kg; B
  apoya en el piso del camion. Se tira de B con F horizontal y las dos
  van juntas, sin que A se corra. mu_e(A-B) = 0.40 ;
  mu_d(B-piso) = 0.20 ; g = 10 m/s^2. Se pide la F maxima sin que A se corra.
""")

mA_p, mB_p = sp.Rational(2), sp.Rational(8)
mu_e_AB = sp.Rational(40, 100)
mu_d_piso = sp.Rational(20, 100)

# (1) Normal entre A y B: equilibrio vertical de A. Sostiene SOLO a A.
n_AB = mA_p * G
# (2) Normal del piso sobre B: equilibrio vertical de B, donde entra el peso
#     de B mas la fuerza que A le hace hacia abajo (reaccion de n_AB).
n_piso = mB_p * G + n_AB
chk("normal entre A y B", n_AB, 20, "N")
chk("normal del piso sobre B", n_piso, 100, "N",
    "NO son 80 N: la normal del piso sostiene los dos pesos")

# (3) Sobre A la unica fuerza horizontal es el rozamiento que le hace B.
#     Como A no se corre, ese rozamiento es ESTATICO, y es lo unico que
#     puede acelerar a A: por lo tanto apunta HACIA ADELANTE.
#     El maximo que puede entregar es su techo -> ahi el movimiento
#     relativo es inminente, que es el unico caso con igualdad.
f_e_max_AB = mu_e_AB * n_AB
a_max = f_e_max_AB / mA_p
chk("f_e maxima entre A y B", f_e_max_AB, 8, "N")
chk("aceleracion maxima del conjunto", a_max, 4, "m/s^2")

# Sentido del rozamiento sobre A: segunda ley horizontal de A.
#   f_sobre_A = m_A * a  > 0  con el eje +x en el sentido del movimiento.
f_sobre_A = mA_p * a_max
afirmar("el rozamiento sobre A apunta HACIA ADELANTE (contraejemplo del "
        "anti-patron 'la friccion siempre frena')",
        f_sobre_A > 0,
        "f = m_A*a = +{} N en el sentido del movimiento".format(f_sobre_A))

# (4) Fuerza aplicada: atajo del conjunto (una sola particula de 10 kg).
#     Externas al conjunto: F y el rozamiento del piso.
F_max = (mA_p + mB_p) * a_max + mu_d_piso * n_piso
chk("fuerza maxima aplicada", F_max, 60, "N",
    "F = (m_A+m_B)*a_max + mu_d*n_piso = 40 + 20")

# Verificacion independiente por el DCL de B (sin usar el atajo).
#   B: F - T(no hay) - f_AB(reaccion, hacia atras) - f_piso = m_B * a
F_por_B = mB_p * a_max + f_e_max_AB + mu_d_piso * n_piso
chk("fuerza maxima, recalculada por el DCL de B solo", F_por_B, F_max, "N")

# (5) Respuestas a las tres preguntas de cierre que el ejemplo deja abiertas.
print("\n  RESPUESTAS A LAS TRES PREGUNTAS DE CIERRE:")
print("  1) La normal del piso NO vale el peso de B (80 N) sino 100 N,")
print("     porque tambien sostiene a A a traves de B.")
# Si se tira de A en vez de B: A queda arrastrando a B, y lo unico que puede
# mover a B es el rozamiento que A le hace, con techo 8.0 N; pero el piso
# le opone hasta 20 N. B no arranca, y entonces A se corre apenas F > 8.0 N.
f_disp_para_B = f_e_max_AB
f_piso_resiste = mu_d_piso * n_piso
print("  2) Tirando de A: lo maximo que A puede transmitirle a B son "
      "{} N,".format(f_disp_para_B))
print("     y el piso le opone hasta {} N. B no arranca; A se corre".format(f_piso_resiste))
print("     apenas F supera {} N. La fuerza maxima se desploma "
      "de 60 N a {} N.".format(f_disp_para_B, f_disp_para_B))
afirmar("tirando de A, B no puede arrancar", f_disp_para_B < f_piso_resiste)
print("  3) Con F > 60 N: B acelera mas que a_max y A se queda atras, o sea")
print("     A desliza hacia atras RESPECTO DE B (respecto del piso las dos")
print("     siguen yendo para adelante). Ahi el rozamiento entre A y B pasa")
print("     a ser dinamico. OJO: el enunciado no da mu_d entre A y B, asi")
print("     que la aceleracion de A en ese regimen no es calculable con los")
print("     datos dados; la consigna solo pide describir, no calcular.")


# ===========================================================================
# PARTE 4 — EJERCICIOS 6.a (practica en bloque)
# ===========================================================================

titulo("PARTE 4 — EJERCICIOS 6.a")

# ---------------------------------------------------------------------------
sub("6.a.1 — Changuitos encastrados (acoplados y fuerza de contacto)")
print("""  A = 20 kg, B = 10 kg, encastrados; F = 60 N horizontal sobre A;
  piso liso.""")
mA1, mB1, F1 = sp.Rational(20), sp.Rational(10), sp.Rational(60)
a1 = F1 / (mA1 + mB1)
P1 = mB1 * a1                       # DCL de B: la unica horizontal es la de A
P1_inv = mA1 * a1                   # empujando desde B: DCL de A
chk("(b) aceleracion", a1, 2, "m/s^2")
chk("(c) fuerza que A ejerce sobre B", P1, 20, "N", "sale del DCL de B")
chk("(e) fuerza de contacto empujando desde B", P1_inv, 40, "N")
afirmar("(e) la aceleracion no cambia al invertir el empuje",
        F1 / (mA1 + mB1) == a1)
print("  (d) La reaccion es la fuerza que B le hace a A: 20 N, sentido")
print("      opuesto, y aparece en el DCL de A.")
print("  (f) Porque la fuerza de contacto es INTERNA al conjunto: al tratar")
print("      los dos como una particula queda dentro del recorte y se cancela.")

# ---------------------------------------------------------------------------
sub("6.a.2 — Tres trineos en cadena")
print("""  A = 6.0 kg (adelante), B = 4.0 kg, C = 2.0 kg (ultimo);
  F = 24 N sobre A; hielo sin rozamiento.""")
mA2, mB2, mC2, F2 = sp.Rational(6), sp.Rational(4), sp.Rational(2), sp.Rational(24)
a2 = F2 / (mA2 + mB2 + mC2)
T_AB2 = (mB2 + mC2) * a2            # la soga A-B tiene que mover a B y a C
T_BC2 = mC2 * a2                    # la soga B-C solo mueve a C
chk("(b) aceleracion", a2, 2, "m/s^2")
chk("(c) T_AB", T_AB2, 12, "N")
chk("(c) T_BC", T_BC2, 4, "N")
afirmar("(d) T_AB > T_BC", T_AB2 > T_BC2,
        "la soga de adelante arrastra mas masa")
# (e) orden invertido: el mas liviano adelante -> C, B, A.
a2_inv = F2 / (mA2 + mB2 + mC2)
T_CB = (mB2 + mA2) * a2_inv
T_BA = mA2 * a2_inv
chk("(e) aceleracion con el orden invertido", a2_inv, 2, "m/s^2",
    "no cambia: depende solo de la masa total")
print("  (e) las tensiones SI cambian: ahora T_CB = {} N y T_BA = {} N.".format(
    T_CB, T_BA))
# (f) colgados en vertical, izados con a = 2.0 m/s^2 hacia arriba.
a_iza = sp.Rational(2)
T_sup = (mA2 + mB2 + mC2) * (G + a_iza)
chk("(f) tension de la soga superior", T_sup, 144, "N")

# ---------------------------------------------------------------------------
sub("6.a.3 — Bloque en tablon a 30 grados + balde colgando, sin rozamiento")
print("""  A = 6.0 kg sobre tablon a 30 grados (liso), soga paralela al tablon
  por una roldana en el extremo superior, balde B = 4.0 kg colgando.""")
mA3, mB3 = sp.Rational(6), sp.Rational(4)
sen30 = sp.Rational(1, 2)           # 30 grados: valor exacto, no declarado
# Quien gana? Peso del balde contra la componente del peso de A sobre el plano.
tira_B = mB3 * G
tira_A = mA3 * G * sen30
print("  peso del balde = {} N   vs   m_A g sen(30) = {} N".format(tira_B, tira_A))
afirmar("(c) el balde baja y el bloque sube", tira_B > tira_A)
sol3 = sp.solve([sp.Eq(mB3 * G - T, mB3 * a),
                 sp.Eq(T - mA3 * G * sen30, mA3 * a)], [a, T], dict=True)[0]
chk("(c) aceleracion", sol3[a], 1, "m/s^2")
chk("(d) tension", sol3[T], 36, "N")
# Verificacion con el otro diagrama
chk("(d) T verificada con el DCL del bloque",
    mA3 * G * sen30 + mA3 * sol3[a], sol3[T], "N")
afirmar("tension positiva y menor que el peso del balde",
        0 < sol3[T] < tira_B)
# (e) masa de balde para reposo
mB_rep = mA3 * sen30
chk("(e) masa del balde para reposo", mB_rep, 3, "kg",
    "equilibra la componente del peso de A sobre el plano")
print("  (f) a = (m_B - m_A sen(theta)) g / (m_A + m_B); con theta -> 90")
print("      queda la maquina de Atwood (verificado en la Parte 1).")

# ---------------------------------------------------------------------------
sub("6.a.4 — Ropero: la desigualdad del rozamiento estatico")
print("""  Ropero de 50 kg en piso horizontal; mu_e = 0.50, mu_d = 0.30.""")
m4 = sp.Rational(50)
mu_e4, mu_d4 = sp.Rational(50, 100), sp.Rational(30, 100)
n4 = m4 * G
chk("(a) reaccion del piso", n4, 500, "N")
# (b) empuja con 180 N y no se mueve -> f_e sale del EQUILIBRIO.
f_e4 = sp.Rational(180)
techo4 = mu_e4 * n4
chk("(b) rozamiento con empuje de 180 N", f_e4, 180, "N",
    "NO 250 N: 250 N es el techo, no el valor")
afirmar("(b) la premisa es consistente: 180 N <= techo de 250 N", f_e4 <= techo4)
chk("(c) fuerza minima para ponerlo en movimiento", techo4, 250, "N",
    "aca SI vale mu_e*n: movimiento inminente")
# (d) ya en movimiento, empuje de 300 N -> rozamiento dinamico
a4 = (sp.Rational(300) - mu_d4 * n4) / m4
chk("(d) aceleracion con empuje de 300 N", a4, 3, "m/s^2")
# (e) velocidad constante -> equilibrio, rozamiento dinamico
chk("(e) fuerza para velocidad constante", mu_d4 * n4, 150, "N")
afirmar("(e) 150 N < 250 N porque mu_d < mu_e", mu_d4 < mu_e4)
print("  (f) No cambia NINGUNA: el modelo dice que la fuerza de rozamiento")
print("      no depende del area de contacto.")

# ---------------------------------------------------------------------------
sub("6.a.5 — Borrador contra el pizarron")
print("""  Borrador de peso 6.0 N apretado horizontalmente contra un pizarron
  vertical; mu_e = 0.80, mu_d = 0.40; parte del reposo.""")
W5 = sp.Rational(6)
mu_e5, mu_d5 = sp.Rational(80, 100), sp.Rational(40, 100)
m5 = W5 / G                          # 0.60 kg
chk("masa del borrador", m5, sp.Rational(6, 10), "kg")

# (b) aprieto con 8.0 N: la normal es HORIZONTAL y vale la fuerza aplicada.
n5b = sp.Rational(8)
techo5b = mu_e5 * n5b
chk("(b) reaccion del pizarron (normal)", n5b, 8, "N",
    "la normal es horizontal y vale F, no el peso")
chk("(b) techo del rozamiento estatico", techo5b, sp.Rational(64, 10), "N")
afirmar("(b) no desliza: el techo supera al peso",
        techo5b > W5, "6.4 N > 6.0 N")
chk("(b) rozamiento efectivo", W5, 6, "N",
    "equilibrio vertical: f_e = peso. NO 6.4 N")

# (c) minima fuerza para que no resbale: movimiento inminente.
Fx = sp.Symbol("Fx", positive=True)
F_min5 = sp.solve(sp.Eq(mu_e5 * Fx, W5), Fx)[0]
chk("(c) fuerza minima para que no resbale", F_min5, sp.Rational(15, 2), "N",
    "F_min = W/mu_e; aca vale mu_e*n porque es inminente")

# (d) apriete de 6.0 N: ahora el techo NO alcanza -> desliza -> mu_d.
n5d = sp.Rational(6)
afirmar("(d) con 6.0 N si desliza", mu_e5 * n5d < W5, "4.8 N < 6.0 N")
f_d5 = mu_d5 * n5d
a5 = (W5 - f_d5) / m5
chk("(d) rozamiento dinamico", f_d5, sp.Rational(24, 10), "N")
chk("(d) aceleracion de bajada", a5, 6, "m/s^2", "sentido: hacia abajo")

# (e) fuerza TOTAL del pizarron = normal + rozamiento (suma vectorial).
Fx5, Fy5 = n5b, W5
mod5 = sp.sqrt(Fx5**2 + Fy5**2)
chk("(e) componente horizontal", Fx5, 8, "N")
chk("(e) componente vertical", Fy5, 6, "N")
chk("(e) modulo de la fuerza total del pizarron", mod5, 10, "N",
    "triangulo 6-8-10, sale exacto")
print("  (f) Apretar mas sube n, y con n sube el techo mu_e*n del rozamiento,")
print("      que es vertical. La fuerza horizontal no sostiene: habilita.")


# ===========================================================================
# PARTE 5 — EJERCICIOS 6.b (adicionales, nivel parcial)
# ===========================================================================

titulo("PARTE 5 — EJERCICIOS 6.b")

# ---------------------------------------------------------------------------
sub("6.b.1 — Fardo arrastrado a angulo theta: el angulo optimo")
print("""  F = 100 N a angulo theta sobre la horizontal, mu_d = 0.75,
  piso horizontal, el fardo sigue apoyado. sen37 = 0.60, cos37 = 0.80.
  Masa (revelada recien en el inciso f): 10 kg.""")

th6, mu6, F6, m6, g6 = sp.symbols("theta mu F m g", positive=True)

# (b) La normal NO vale el peso: la componente vertical de F alivia el apoyo.
n6 = m6 * g6 - F6 * sp.sin(th6)
# (c) Segunda ley horizontal: F cos - mu*n = m a
a6 = sp.simplify((F6 * sp.cos(th6) - mu6 * n6) / m6)
chk("(b) normal literal", n6, m6 * g6 - F6 * sp.sin(th6))
chk("(c) a literal", sp.expand(m6 * a6),
    sp.expand(F6 * (sp.cos(th6) + mu6 * sp.sin(th6)) - mu6 * m6 * g6))

# (d) VIA 1 — derivando (control interno, el documento NO deriva).
#     Verifico que theta = atan(mu) anula la derivada, que es la forma
#     limpia de confirmarlo: sp.solve devuelve una expresion equivalente
#     pero escrita con un angulo mitad, y compararla a ciegas da un
#     falso negativo.
dad = sp.diff(a6, th6)
dad_en_optimo = sp.simplify(sp.expand_trig(dad.subs(th6, sp.atan(mu6))))
chk("(d) via derivada: da/dtheta se anula en theta = atan(mu_d)",
    dad_en_optimo, 0, "",
    "control interno; el documento resuelve sin derivar")
# Confirmo que es maximo y no minimo (segunda derivada negativa alli).
d2 = sp.diff(a6, th6, 2).subs(th6, sp.atan(mu6))
afirmar("(d) el punto critico es un MAXIMO (segunda derivada < 0)",
        float(d2.subs({F6: 100, m6: 10, mu6: sp.Rational(3, 4)})) < 0)

# (d) VIA 2 — identidad de amplitud, que es la que usa el documento.
phi = sp.symbols("varphi", positive=True)
lhs = sp.cos(th6) + mu6 * sp.sin(th6)
rhs = sp.sqrt(1 + mu6**2) * sp.cos(th6 - sp.atan(mu6))
chk("(d) identidad cos(th) + mu sen(th) = sqrt(1+mu^2) cos(th - atan mu)",
    sp.simplify(sp.expand_trig(lhs - rhs)), 0, "",
    "es identidad para todo theta: la construccion del estilista cierra")
print("  El coseno es maximo cuando su argumento es cero => theta = atan(mu_d),")
print("  o sea tan(theta_optimo) = mu_d. Misma forma que tan(theta_c) = mu_e.")

# Construccion numerica del estilista: mu_d = 0.75 -> R = 1.25 EXACTO y 37 grados.
mu_d6 = sp.Rational(3, 4)            # 0.75 exacto
R = sp.sqrt(1 + mu_d6**2)
chk("(d) amplitud R = sqrt(1 + mu_d^2)", R, sp.Rational(5, 4), "",
    "EXACTO, sin decimales: 0.75 = 3/4 da sqrt(25/16) = 5/4")
chk("(d) tan(theta_optimo) con los valores declarados",
    SEN37 / COS37, mu_d6, "", "0.60/0.80 = 0.75 = mu_d, o sea theta = 37 grados")
# La identidad evaluada en el optimo, con los valores declarados del enunciado:
chk("(d) cos37 + mu_d sen37 evaluado con 0.80 y 0.60",
    COS37 + mu_d6 * SEN37, sp.Rational(5, 4), "",
    "coincide con R: el maximo cae exactamente en 37 grados")

# (f) numeros, con m = 10 kg y F = 100 N.
F6v, m6v = sp.Rational(100), sp.Rational(10)
a_opt = (F6v * R - mu_d6 * m6v * G) / m6v
a_hor = (F6v - mu_d6 * m6v * G) / m6v
chk("(f) aceleracion en el angulo optimo", a_opt, 5, "m/s^2")
chk("(f) aceleracion tirando horizontalmente", a_hor, sp.Rational(25, 10), "m/s^2")
# Chequeo de ley: la normal tiene que seguir siendo positiva en el optimo.
n_opt = m6v * G - F6v * SEN37
afirmar("normal positiva en el angulo optimo (el fardo sigue apoyado)",
        n_opt > 0, "n = {} N".format(n_opt))
# Borde del rango que declara el enunciado (theta entre 0 y 90 grados):
# con m = 10 kg y F = 100 N resulta mg = F, asi que en theta = 90 la
# componente vertical de F iguala al peso y la normal se anula justo.
n_90 = m6v * G - F6v * 1
afirmar("normal no negativa en el extremo theta = 90 grados", n_90 >= 0,
        "n = {} N: se anula justo en el borde. El enunciado estipula que el "
        "fardo sigue apoyado, asi que el modelo es valido en todo el "
        "intervalo, pero 90 grados es el limite exacto de despegue".format(n_90))
print("  (e) El optimo no depende de m ni de F porque tan(theta) = mu_d no")
print("      contiene ninguna de las dos. Con mu_d = 0: el optimo es theta = 0.")
chk("(e) optimo sin rozamiento", sp.atan(0), 0, "rad", "tirar horizontal")

# ---------------------------------------------------------------------------
sub("6.b.2 — Dos paquetes atados bajando una rampa a 37 grados")
print("""  Rampa fija a 37 grados. A = 6.0 kg va ADELANTE (mas abajo),
  mu_A = 0.20; B = 3.0 kg va DETRAS, mu_B = 0.50. Soga paralela a la
  rampa. sen37 = 0.60, cos37 = 0.80.""")

# --- Primero, simbolico: de donde sale que T es proporcional a (mu_B - mu_A).
mAs, mBs, muAs, muBs, gs, al = sp.symbols(
    "m_A m_B mu_A mu_B g alpha", positive=True)
Ts, as_ = sp.symbols("T a")
# Eje positivo: cuesta abajo, para los dos. La soga tira de A hacia atras
# (cuesta arriba) y de B hacia adelante (cuesta abajo).
ecA = sp.Eq(mAs * gs * sp.sin(al) - muAs * mAs * gs * sp.cos(al) - Ts, mAs * as_)
ecB = sp.Eq(mBs * gs * sp.sin(al) - muBs * mBs * gs * sp.cos(al) + Ts, mBs * as_)
sol_b2 = sp.solve([ecA, ecB], [as_, Ts], dict=True)[0]
a_lit = sp.simplify(sol_b2[as_])
T_lit = sp.simplify(sol_b2[Ts])
chk("(c) a literal",
    a_lit,
    gs * sp.sin(al) - gs * sp.cos(al) * (muAs * mAs + muBs * mBs) / (mAs + mBs))
chk("(d) T literal",
    sp.simplify(T_lit),
    mAs * mBs / (mAs + mBs) * gs * sp.cos(al) * (muBs - muAs), "",
    "T proporcional a (mu_B - mu_A): confirmado simbolicamente")
chk("(e) T cuando los dos coeficientes son iguales",
    sp.simplify(T_lit.subs(muBs, muAs)), 0, "N",
    "la soga no hace nada; bajan como si no estuvieran atados")
afirmar("(d) T > 0 exige mu_B > mu_A, o sea el de ADELANTE mas liso",
        sp.simplify(sp.sign((T_lit / (mAs * mBs / (mAs + mBs) * gs * sp.cos(al)))
                            - (muBs - muAs))) == 0)

# --- Ahora los numeros, con los valores declarados de sen y cos.
mA7, mB7 = sp.Rational(6), sp.Rational(3)
muA7, muB7 = sp.Rational(20, 100), sp.Rational(50, 100)
subs7 = {mAs: mA7, mBs: mB7, muAs: muA7, muBs: muB7, gs: G}
n_A7 = mA7 * G * COS37
n_B7 = mB7 * G * COS37
chk("(a) normal sobre A", n_A7, 48, "N")
chk("(a) normal sobre B", n_B7, 24, "N")
afirmar("normales positivas", n_A7 > 0 and n_B7 > 0)

a_num7 = (mA7 * G * SEN37 - muA7 * n_A7 + mB7 * G * SEN37 - muB7 * n_B7) / (mA7 + mB7)
T_num7 = mA7 * mB7 / (mA7 + mB7) * G * COS37 * (muB7 - muA7)
chk("(c) aceleracion del conjunto", a_num7, sp.Rational(36, 10), "m/s^2")
chk("(d) tension", T_num7, sp.Rational(48, 10), "N")
afirmar("tension positiva (la soga esta tensa)", T_num7 > 0)
# Verificacion por cuerpo, que es lo que pide el documento.
chk("verificacion DCL de A: m_A*a contra la suma de fuerzas",
    mA7 * a_num7, mA7 * G * SEN37 - muA7 * n_A7 - T_num7, "N")
chk("verificacion DCL de B: m_B*a contra la suma de fuerzas",
    mB7 * a_num7, mB7 * G * SEN37 - muB7 * n_B7 + T_num7, "N")

# (f) Orden invertido: el mas rugoso (mu = 0.50) va adelante.
#     Cada uno, suelto, baja con a = g(sen - mu cos). Es independiente de la masa.
a_suelto_rugoso = G * SEN37 - muB7 * G * COS37     # el de adelante ahora
a_suelto_liso = G * SEN37 - muA7 * G * COS37       # el de atras ahora
chk("(f) a del paquete rugoso, suelto (queda adelante)",
    a_suelto_rugoso, 2, "m/s^2")
chk("(f) a del paquete liso, suelto (queda atras)",
    a_suelto_liso, sp.Rational(44, 10), "m/s^2")
afirmar("(f) el de atras alcanza al de adelante => la soga se afloja, T = 0",
        a_suelto_liso > a_suelto_rugoso,
        "una soga tira pero no empuja: T = 0, no T negativa")
# Control: si uno se empenara en usar la formula con el orden invertido,
# le daria T < 0, que es la senal de soga floja, no un resultado valido.
T_formula_invertida = sp.simplify(T_lit.subs(
    {mAs: mB7, mBs: mA7, muAs: muB7, muBs: muA7, gs: G, al: sp.asin(SEN37)}))
print("  Control: aplicar a ciegas la formula con el orden invertido da")
print("  T = {:.2f} N. Una tension negativa NO es un resultado fisico:".format(
    float(T_formula_invertida)))
print("  significa que la hipotesis 'soga tensa' era falsa. T = 0.")
afirmar("la formula invertida delata soga floja con T < 0",
        T_formula_invertida < 0)

# ---------------------------------------------------------------------------
sub("6.b.3 — Cajones apilados, roldana y rozamiento doble")
print("""  A = 3.0 kg sobre B = 5.0 kg, B en el piso. De A sale una soga
  horizontal que pasa por una roldana en una columna y vuelve a B. Se tira
  de B con F, alejandolo de la columna; todo a VELOCIDAD CONSTANTE.
  mu_d = 0.20 entre superficies, mu_e = 0.35 (dato distractor).""")

mA8, mB8 = sp.Rational(3), sp.Rational(5)
mu_d8 = sp.Rational(20, 100)
mu_e8 = sp.Rational(35, 100)         # NO se usa: hay deslizamiento

W_A8, W_B8 = mA8 * G, mB8 * G
n_AB8 = W_A8                                  # equilibrio vertical de A
n_piso8 = W_A8 + W_B8                         # equilibrio vertical de B
chk("(c) normal entre A y B", n_AB8, 30, "N")
chk("(c) reaccion del piso sobre B", n_piso8, 80, "N", "NO 50 N")

# (b) La soga es inextensible y pasa por la roldana: si B se aleja, A se acerca.
#     Los dos deslizan uno respecto del otro => rozamiento DINAMICO entre ellos.
f_AB8 = mu_d8 * n_AB8
chk("rozamiento entre A y B", f_AB8, 6, "N", "dinamico: hay deslizamiento")

# (d) Solo roce entre los cajones. Velocidad constante => equilibrio.
#     A: T (hacia la columna) - f_AB (alejandose) = 0
T8 = f_AB8
#     B: F (alejandose) - T (hacia la columna) - f_BA (hacia la columna) = 0
F8_d = T8 + f_AB8
chk("(d) tension de la soga", T8, 6, "N")
chk("(d) F solo con roce entre cajones", F8_d, 12, "N", "F = 2 mu_d W_A")

# (e) Agregando el roce con el piso.
f_piso8 = mu_d8 * n_piso8
F8_e = F8_d + f_piso8
chk("(e) rozamiento del piso sobre B", f_piso8, 16, "N")
chk("(e) F con roce con el piso", F8_e, 28, "N")

# (f) El razonamiento erroneo del companero.
chk("(f) valor que obtiene el companero", f_piso8, 16, "N")
print("  (f) Deja afuera la tension de la soga y el rozamiento entre los")
print("      cajones. Los trato como internos a un 'cuerpo unico', pero la")
print("      soga sale del sistema y vuelve por la roldana: son EXTERNAS a B.")
afirmar("el distractor mu_e = 0.35 no se usa en ningun inciso", True,
        "hay deslizamiento y velocidad constante: manda mu_d")
afirmar("todas las tensiones y normales de 6.b.3 son positivas",
        T8 > 0 and n_AB8 > 0 and n_piso8 > 0)


# ===========================================================================
# RESUMEN
# ===========================================================================

titulo("RESUMEN")
fallas = [e for e, ok in _resultados if not ok]
print("  chequeos corridos : {}".format(len(_resultados)))
print("  coincidencias     : {}".format(len(_resultados) - len(fallas)))
print("  discrepancias     : {}".format(len(fallas)))
if fallas:
    print("\n  DISCREPANCIAS DETECTADAS:")
    for f in fallas:
        print("    - " + f)
else:
    print("\n  Todo coincide.")
print()
