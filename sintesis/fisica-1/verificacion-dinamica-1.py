# -*- coding: utf-8 -*-
"""
============================================================================
VERIFICACION NUMERICA INDEPENDIENTE - Dinamica I (leyes de Newton)
Sintesis "Fisica 1 - Dinamica I: las tres leyes de Newton"
============================================================================

Para que sirve este archivo
---------------------------
Este script resuelve, desde el enunciado y sin mirar ninguna resolucion
previa, todos los ejercicios y ejemplos con resultado calculable de la
sintesis. Se te entrega junto con el documento por dos razones:

  1. Es la fuente de verdad de los resultados: si tu numero no coincide
     con el de aca, el que hay que revisar es el tuyo (o el mio, y en ese
     caso el script esta comentado para que puedas auditarlo).

  2. Es un modelo de autoevaluacion. Cada bloque plantea la fisica primero
     (que ecuacion, en que eje, por que) y recien despues evalua numeros.
     Ese es el orden en el que conviene que resuelvas vos.

Como correrlo
-------------
    python verificacion-dinamica-1.py

Requiere sympy (para las verificaciones algebraicas simbolicas):
    pip install sympy

Convenciones del documento, respetadas aca
------------------------------------------
  * g = 10 m/s^2 en TODOS los casos (la catedra lo declara en cada
    enunciado). No se usa 9.8.
  * En el ejercicio 6.b.3 el enunciado FIJA sen(37) = 0.60 y
    cos(37) = 0.80. Se usan esos valores, no los exactos.
  * Convencion de subindices de tercera ley: en F_12 el primero ejerce,
    el segundo recibe.
============================================================================
"""

import sys
import math

# La consola de Windows es cp1252 y explota con caracteres no-ASCII.
# Esto la fuerza a utf-8 sin depender de variables de entorno.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import sympy as sp

# ---------------------------------------------------------------------------
# Constante global del documento
# ---------------------------------------------------------------------------
g = 10.0  # m/s^2


# ---------------------------------------------------------------------------
# Infraestructura minima de reporte
# ---------------------------------------------------------------------------
_resultados = []


def check(etiqueta, calculado, afirmado, unidad="", tol=None, nota=""):
    """
    Compara un valor calculado independientemente contra el valor que
    afirma el documento.

    tol : tolerancia absoluta. Si es None se usa media unidad del ultimo
          decimal del valor afirmado, que es el criterio correcto para
          juzgar un redondeo ("~104 N" es correcto si el valor real cae
          en [103.5, 104.5)).
    """
    if afirmado is None:
        veredicto = "SIN VALOR EN EL DOC"
        ok = None
    else:
        if tol is None:
            tol = 0.5  # media unidad del ultimo decimal escrito
        ok = abs(calculado - afirmado) <= tol
        veredicto = "COINCIDE" if ok else ">>> DISCREPA <<<"
    _resultados.append((etiqueta, calculado, afirmado, unidad, veredicto, nota))
    linea = f"  [{veredicto}] {etiqueta}: calculado = {calculado:.4g} {unidad}"
    if afirmado is not None:
        linea += f" | documento = {afirmado:g} {unidad}"
    print(linea)
    if nota:
        print(f"      nota: {nota}")
    return ok


def titulo(t):
    print()
    print("=" * 76)
    print(t)
    print("=" * 76)


def sub(t):
    print()
    print(f"--- {t}")


# ===========================================================================
# EJEMPLO RESUELTO 1 - Ascensor con balanza
# ---------------------------------------------------------------------------
# Enunciado: persona de 60 kg parada sobre una balanza dentro de un ascensor
# que SUBE ACELERANDO a 2.0 m/s^2. g = 10. Se pide la marca de la balanza y
# la comparacion con el peso.
#
# Fisica: una sola direccion relevante (vertical). Eje +y hacia arriba.
# Sobre la persona actuan solo dos fuerzas: normal (arriba) y peso (abajo).
# NO hay equilibrio: a_y = +2.0.
#     sum F_y = n - m*g = m*a_y   =>   n = m*(g + a_y)
# ===========================================================================
titulo("EJEMPLO RESUELTO 1 - Ascensor con balanza")

m_asc = 60.0
a_asc = +2.0

n_asc = m_asc * (g + a_asc)          # normal despejada de la 2da ley
peso_asc = m_asc * g                 # peso: NO depende de la aceleracion
marca_kg = n_asc / g                 # la balanza divide por la g de fabrica

check("Ej1 (c) normal sobre la persona", n_asc, 720.0, "N")
check("Ej1 (d) marca de la balanza", marca_kg, 72.0, "kg",
      nota="la balanza mide la normal (3ra ley) y la divide por g=10")
check("Ej1 (d) peso de la persona", peso_asc, 600.0, "N",
      nota="mg no cambia por estar en un ascensor; lo que cambio es n")

sub("Casos limite que el documento analiza cualitativamente")
n_v_const = m_asc * (g + 0.0)
check("Ej1 (e) a=0 -> n", n_v_const, 600.0, "N")
check("Ej1 (e) a=0 -> marca", n_v_const / g, 60.0, "kg")
n_caida = m_asc * (g + (-g))
check("Ej1 (e) caida libre a=-g -> n", n_caida, 0.0, "N",
      nota="ingravidez aparente: n=0, no ausencia de gravedad")
print("  [COHERENCIA] n > 0 en todos los casos salvo la caida libre, "
      "donde n=0 (no negativa): correcto, una superficie no puede tirar.")


# ===========================================================================
# EJEMPLO RESUELTO 2 - Rampa lisa (parcial)
# ---------------------------------------------------------------------------
# Enunciado: caja de 4.0 kg soltada desde el reposo sobre rampa lisa a 30
# grados. g = 10. Se piden la aceleracion y la reaccion de la rampa.
#
# Fisica: ejes rotados (x paralelo al plano, positivo cuesta abajo;
# y perpendicular). El peso se descompone:
#     a lo largo:      mg*sen(theta)
#     perpendicular:   mg*cos(theta)
#     sum F_x = mg*sen = m*a_x  =>  a_x = g*sen(theta)   (la masa se cancela)
#     sum F_y = n - mg*cos = 0  =>  n = mg*cos(theta)
# ===========================================================================
titulo("EJEMPLO RESUELTO 2 - Rampa lisa a 30 grados")

m_r, th_r = 4.0, math.radians(30.0)

a_rampa = g * math.sin(th_r)
n_rampa = m_r * g * math.cos(th_r)

check("Ej2 aceleracion cuesta abajo", a_rampa, 5.0, "m/s^2",
      nota="a = g*sen(theta); independiente de la masa")
check("Ej2 normal (reaccion de la rampa)", n_rampa, None, "N",
      nota="el documento deja este calculo al lector (ejemplo parcial); "
           "el valor de referencia es 34.6 N")

sub("Chequeos cualitativos que el documento pide al lector")
print(f"  n = {n_rampa:.2f} N  vs  peso = {m_r*g:.1f} N  ->  "
      f"n < peso: {n_rampa < m_r*g}")
print(f"  theta -> 0   : n -> {m_r*g*math.cos(math.radians(0.01)):.2f} N "
      f"(tiende a mg = {m_r*g:.1f} N)  OK")
print(f"  theta -> 90  : n -> {m_r*g*math.cos(math.radians(89.99)):.4f} N "
      f"(tiende a 0)  OK")
print("  [COHERENCIA] La masa se cancela en a_x pero NO en n: correcto, "
      "solo la aceleracion es independiente de m.")


# ===========================================================================
# EJEMPLO RESUELTO 3 - Resorte horizontal (parcial)
# ---------------------------------------------------------------------------
# Enunciado: bloque sobre mesa lisa unido a resorte horizontal k = 200 N/m,
# origen en el resorte sin deformar, positivo alejandose de la pared.
#     F_s = -k*x
# ===========================================================================
titulo("EJEMPLO RESUELTO 3 - Resorte horizontal, k = 200 N/m")

k_h = 200.0

F_estirado = -k_h * (+0.050)   # x = +5.0 cm
F_comprimido = -k_h * (-0.030)  # x = -3.0 cm

check("Ej3 fuerza en x=+5.0 cm", F_estirado, -10.0, "N",
      nota="signo negativo = apunta hacia la pared (restauradora)")
check("Ej3 fuerza en x=-3.0 cm", F_comprimido, None, "N",
      nota="lo deja al lector; referencia = +6.0 N, apunta alejandose "
           "de la pared")

sub("Verificacion de la proporcionalidad que el documento pide comprobar")
print(f"  |F1|/|F2| = {abs(F_estirado)/abs(F_comprimido):.4f}")
print(f"  |x1|/|x2| = {0.050/0.030:.4f}   ->  coinciden (ley lineal)  OK")


# ===========================================================================
# EJERCICIO 6.a.1 - Cajon de fruta: normal y tercera ley
# ---------------------------------------------------------------------------
# Enunciado: cajon de 8.0 kg en el piso. El verdulero empuja verticalmente
# HACIA ABAJO con 25 N. El cajon no se mueve. g = 10.
#
# Fisica: equilibrio vertical, tres fuerzas (n arriba, mg abajo, F abajo).
#     sum F_y = n - mg - F = 0  =>  n = mg + F
# Inciso (e): tirando hacia ARRIBA con 25 N  =>  n = mg - F
# ===========================================================================
titulo("EJERCICIO 6.a.1 - Cajon de fruta (normal y tercera ley)")

m_c, F_c = 8.0, 25.0
peso_c = m_c * g

n_empuja = peso_c + F_c
n_tira = peso_c - F_c

check("6.a.1 (b) normal del piso (empuja hacia abajo)", n_empuja, None, "N",
      nota="referencia = 105 N")
check("6.a.1 (d) peso del cajon", peso_c, 80.0, "N",
      nota="el enunciado lo afirma explicitamente: correcto")
check("6.a.1 (e) normal tirando hacia arriba", n_tira, None, "N",
      nota="referencia = 55 N")

sub("Coherencia fisica")
print(f"  n(empuja) = {n_empuja:.1f} N > peso = {peso_c:.1f} N  -> "
      "correcto, la mano suma carga sobre el piso")
print(f"  n(tira)   = {n_tira:.1f} N > 0  -> el cajon sigue apoyado. "
      f"Se despegaria si F > {peso_c:.0f} N (ahi n=0, nunca negativa).")
print("  Par de 3ra ley del inciso (c): la reaccion a n es la fuerza que el "
      "CAJON hace sobre el PISO, hacia abajo, de 105 N. No es el peso.")


# ===========================================================================
# EJERCICIO 6.a.2 - Caja en rampa sujeta por soga paralela
# ---------------------------------------------------------------------------
# Enunciado: caja de 12 kg en reposo sobre rampa a 30 grados, sujeta por
# soga PARALELA a la rampa, sin rozamiento. g = 10.
#
# Fisica: equilibrio en ambos ejes (rotados).
#     sum F_x = T - mg*sen(theta) = 0  =>  T = mg*sen(theta)
#     sum F_y = n - mg*cos(theta) = 0  =>  n = mg*cos(theta)
# ===========================================================================
titulo("EJERCICIO 6.a.2 - Caja 12 kg en rampa de 30 grados (soga paralela)")

m_2, th_2 = 12.0, math.radians(30.0)
peso_2 = m_2 * g

T_2 = peso_2 * math.sin(th_2)
n_2 = peso_2 * math.cos(th_2)

check("6.a.2 (b) tension de la soga", T_2, 60.0, "N")
check("6.a.2 (c) reaccion de la rampa (normal)", n_2, 104.0, "N",
      nota="valor exacto 103.92 N; el redondeo a ~104 N es correcto")
check("6.a.2 (d) peso de la caja", peso_2, 120.0, "N",
      nota="n=103.92 < peso=120: correcto, la rampa solo soporta la "
           "componente perpendicular")

sub("Inciso (e): rampa mas empinada y limite theta -> 90")
for ang in (30, 45, 60, 89.99):
    t = math.radians(ang)
    print(f"  theta={ang:>6}  T = {peso_2*math.sin(t):7.2f} N   "
          f"n = {peso_2*math.cos(t):7.2f} N")
print("  -> T crece hacia mg=120 N, n decrece hacia 0. Coincide con lo "
      "que afirma el bloque teorico del plano inclinado.  OK")


# ===========================================================================
# EJERCICIO 6.a.3 - Carrito de supermercado: segunda ley y masa inercial
# ---------------------------------------------------------------------------
# Enunciado: carrito vacio 15 kg, piso horizontal liso, F = 30 N horizontal.
# Con el carrito cargado, el mismo empujon da a = 0.75 m/s^2.
#
# Fisica:
#   (b) a_vacio = F/m
#   (c) definicion operacional de masa inercial: m1/m2 = a2/a1
#       => m_cargado = m_vacio * a_vacio / a_cargado   (sin usar F)
#   (d) m_mercaderia = m_cargado - m_vacio
# ===========================================================================
titulo("EJERCICIO 6.a.3 - Carrito de supermercado (masa inercial)")

m_vacio, F_3, a_cargado = 15.0, 30.0, 0.75

a_vacio = F_3 / m_vacio
m_cargado = m_vacio * a_vacio / a_cargado   # solo el COCIENTE de aceleraciones
m_merca = m_cargado - m_vacio

check("6.a.3 (b) aceleracion del carrito vacio", a_vacio, 2.0, "m/s^2")
check("6.a.3 (c) masa del carrito cargado", m_cargado, 40.0, "kg",
      nota="obtenida por m1/m2 = a2/a1, sin usar el valor de F")
check("6.a.3 (d) masa de la mercaderia", m_merca, 25.0, "kg")

sub("Verificacion cruzada del inciso (e): el metodo no necesita conocer F")
F_sym = sp.symbols("F", positive=True)
m1_sym = sp.symbols("m1", positive=True)
a1_sym = F_sym / m1_sym
a2_sym = sp.Rational(3, 4)
m2_sym = sp.simplify(F_sym / a2_sym)
# Sustituyendo a1 = F/m1, el cociente m1*a1/a2 debe dar F/a2 y F debe cancelarse
expr = sp.simplify(m1_sym * a1_sym / a2_sym - m2_sym)
print(f"  m1*a1/a2 - F/a2 = {expr}  ->  identicamente 0: la F se cancela.  OK")
print("  Es decir: el cociente de aceleraciones basta, tal como afirma (e).")


# ===========================================================================
# EJERCICIO 6.a.4 - Maceta con cable inclinado y soga horizontal
# ---------------------------------------------------------------------------
# Enunciado: maceta de 4.0 kg cuelga de un cable que forma 30 grados con la
# VERTICAL; una soga horizontal la mantiene quieta. g = 10.
#
# Fisica: equilibrio en las dos direcciones. Ejes horizontal/vertical.
#   vertical:    T*cos(theta) - mg = 0        =>  T = mg/cos(theta)
#   horizontal:  T*sen(theta) - T_soga = 0    =>  T_soga = mg*tan(theta)
# (theta medido desde la VERTICAL, por eso el coseno acompana al peso.)
# ===========================================================================
titulo("EJERCICIO 6.a.4 - Maceta 4.0 kg, cable a 30 grados de la vertical")

m_4, th_4 = 4.0, math.radians(30.0)
peso_4 = m_4 * g

T_cable = peso_4 / math.cos(th_4)
T_soga = peso_4 * math.tan(th_4)

check("6.a.4 (c) tension del cable", T_cable, 46.0, "N",
      nota="valor exacto 46.19 N; el redondeo a ~46 N es correcto")
check("6.a.4 (d) tension de la soga horizontal", T_soga, None, "N",
      nota="referencia = 23.09 N (~23 N)")
check("6.a.4 (e) peso de la maceta", peso_4, 40.0, "N")

sub("Inciso (e): por que T_cable > peso")
print(f"  T = {T_cable:.2f} N  >  mg = {peso_4:.1f} N  -> {T_cable > peso_4}")
print("  Razon: solo la componente VERTICAL del cable sostiene el peso, y esa")
print("  componente es T*cos(theta) < T. Para que T*cos = mg hace falta T > mg.")
print("  Verificacion algebraica: T/mg = 1/cos(theta) >= 1 para todo theta.")


# ===========================================================================
# EJERCICIO 6.a.5 - Balanza de verduleria (ley de Hooke)
# ---------------------------------------------------------------------------
# Enunciado: el resorte se alarga 4.0 cm con una bolsa de 1.2 kg. g = 10.
#   (a) k = mg/d
#   (b) d' = m'g/k
# ===========================================================================
titulo("EJERCICIO 6.a.5 - Balanza de verduleria (ley de Hooke)")

m_5a, d_5a = 1.2, 0.040
k_5 = m_5a * g / d_5a

m_5b = 2.0
d_5b = m_5b * g / k_5

check("6.a.5 (a) constante elastica", k_5, 300.0, "N/m")
check("6.a.5 (b) alargamiento con 2.0 kg", d_5b * 100, 6.7, "cm",
      tol=0.05,
      nota="valor exacto 6.667 cm; el redondeo a ~6.7 cm es correcto")

sub("Coherencia: la relacion debe ser lineal")
print(f"  d'/d = {d_5b/d_5a:.4f}   m'/m = {m_5b/m_5a:.4f}  ->  iguales.  OK")
print("  Inciso (d): con k mayor, d = mg/k es menor para la misma masa, asi")
print("  que el mismo rango de masas ocupa menos recorrido -> las marcas de")
print("  graduacion quedan MAS JUNTAS.  Coherente.")


# ===========================================================================
# EJERCICIO 6.b.1 - Mochila en el colectivo (pendulo acelerado)
# ---------------------------------------------------------------------------
# Enunciado: mochila de 5.0 kg colgada del techo de un colectivo que acelera
# a 2.0 m/s^2 en horizontal. Queda desviada un angulo constante respecto de
# la vertical. g = 10.
#
# Fisica: visto desde la vereda (marco inercial). Dos fuerzas: peso y tension.
#   horizontal:  T*sen(theta) = m*a     (NO hay equilibrio, acelera)
#   vertical:    T*cos(theta) - mg = 0  (SI hay equilibrio, no sube ni baja)
# Dividiendo:    tan(theta) = a/g       (la masa se cancela)
#   T = m*sqrt(g^2 + a^2)  =  mg/cos(theta)
# ===========================================================================
titulo("EJERCICIO 6.b.1 - Mochila en colectivo que acelera a 2.0 m/s^2")

m_6, a_6 = 5.0, 2.0

th_6 = math.atan(a_6 / g)
th_6_deg = math.degrees(th_6)
T_6 = m_6 * math.sqrt(g**2 + a_6**2)
T_6_alt = m_6 * g / math.cos(th_6)   # camino alternativo, debe coincidir

check("6.b.1 (c) angulo con la vertical", th_6_deg, 11.0, "grados",
      nota="valor exacto 11.31 grados; el redondeo a ~11 grados es correcto")
check("6.b.1 (d) tension de la correa", T_6, None, "N",
      nota="referencia = 50.99 N (~51 N)")
print(f"  [CRUCE] T por m*sqrt(g^2+a^2) = {T_6:.4f} N ; "
      f"T por mg/cos(theta) = {T_6_alt:.4f} N  ->  coinciden.  OK")

sub("Inciso (e): el angulo no depende de la masa (verificacion simbolica)")
m_s, a_s, g_s = sp.symbols("m a g", positive=True)
T_s, th_s = sp.symbols("T theta", positive=True)
# Las dos ecuaciones de la segunda ley, escritas sin resolver:
ec_horiz = sp.Eq(T_s * sp.sin(th_s), m_s * a_s)   # hay fuerza neta
ec_vert = sp.Eq(T_s * sp.cos(th_s), m_s * g_s)    # hay equilibrio
print(f"  horizontal : {ec_horiz.lhs} = {ec_horiz.rhs}")
print(f"  vertical   : {ec_vert.lhs} = {ec_vert.rhs}")

# La maniobra que recomienda el bloque del plano inclinado: dividir una
# ecuacion por la otra elimina la incognita molesta (aca T) de un saque.
cociente = sp.simplify(ec_horiz.lhs / ec_vert.lhs)   # -> tan(theta)
lado_der = sp.simplify(ec_horiz.rhs / ec_vert.rhs)   # -> a/g, sin m
print(f"  dividiendo :  {cociente} = {lado_der}   ->  la m se cancela.  OK")

# T, en cambio, sale de sumar los cuadrados y SI conserva la masa.
T_general = sp.sqrt(sp.simplify(ec_horiz.rhs**2 + ec_vert.rhs**2))
print(f"  T = {sp.simplify(T_general)}   ->  T SI depende de m.  OK")
print("  Significado: dos pasajeros con mochilas distintas ven el MISMO")
print("  angulo, pero la correa mas cargada soporta mas tension.")

sub("Inciso (f): la correa nunca llega a la horizontal")
for aa in (2, 10, 50, 500, 5000):
    print(f"  a = {aa:>5} m/s^2  ->  theta = "
          f"{math.degrees(math.atan(aa/g)):7.3f} grados")
print("  theta = arctan(a/g) < 90 para toda a finita: tiende a 90 pero no")
print("  lo alcanza. Si fuera exactamente 90, cos(theta)=0 y la componente")
print("  vertical no podria sostener el peso.  Coherente con el documento.")


# ===========================================================================
# EJERCICIO 6.b.2 - Resorte vertical, origen en el equilibrio
# ---------------------------------------------------------------------------
# Enunciado: resorte colgado del techo. Con un cuerpo de 0.50 kg se alarga
# 10 cm y queda en reposo. Despues se tira del cuerpo 6.0 cm hacia abajo y
# se lo suelta. g = 10. Se pide la aceleracion en el instante del suelte.
#
# Fisica:
#   (b) en el reposo:  k*d - mg = 0  =>  k = mg/d
#   (c) el origen conviene ponerlo en la NUEVA posicion de equilibrio
#   (d) desde ese origen el peso ya esta absorbido:  F_neta = -k*x
# ===========================================================================
titulo("EJERCICIO 6.b.2 - Resorte vertical, cuerpo de 0.50 kg")

m_7, d_7, x_7 = 0.50, 0.10, 0.060
peso_7 = m_7 * g

k_7 = peso_7 / d_7
F_neta_7 = k_7 * x_7          # modulo, hacia ARRIBA (restauradora)
a_7 = F_neta_7 / m_7

check("6.b.2 (b) constante elastica", k_7, 50.0, "N/m")
check("6.b.2 (d) fuerza neta en el instante del suelte", F_neta_7, None, "N",
      nota="referencia = 3.0 N, hacia arriba")
check("6.b.2 (d) aceleracion en el instante del suelte", a_7, None, "m/s^2",
      nota="referencia = 6.0 m/s^2, hacia arriba")

sub("Cruce por el camino largo (midiendo desde la longitud natural)")
# Estiramiento total en el instante del suelte = d + x = 16 cm
estir_total = d_7 + x_7
F_resorte = k_7 * estir_total          # hacia arriba
F_neta_largo = F_resorte - peso_7      # hacia arriba
print(f"  estiramiento total = {estir_total*100:.1f} cm")
print(f"  fuerza del resorte = {F_resorte:.2f} N (arriba)")
print(f"  peso               = {peso_7:.2f} N (abajo)")
print(f"  fuerza neta        = {F_neta_largo:.2f} N (arriba)  ->  "
      f"coincide con {F_neta_7:.2f} N.  OK")
print(f"  a = {F_neta_largo/m_7:.2f} m/s^2  ->  coincide.  OK")

sub("Inciso (e): el error del companero, cuantificado")
a_mal = (k_7 * estir_total) / m_7
print(f"  Si toma F_neta = k*(d+x) = {k_7*estir_total:.1f} N y OLVIDA restar")
print(f"  el peso, obtiene a = {a_mal:.1f} m/s^2 en vez de {a_7:.1f} m/s^2.")
print("  El paso mal no es medir desde la longitud natural (eso es legitimo),")
print("  sino usar F_s = -kx como si fuera la fuerza NETA con ese origen.")
print("  Desde la longitud natural hay que conservar el termino mg; desde el")
print("  equilibrio, el mg ya esta absorbido y por eso desaparece.")

sub("Verificacion simbolica de esa cancelacion")
k_s, d_s, x_s = sp.symbols("k d x", positive=True)
# En equilibrio: k*d = m*g. Fuerza neta a distancia x por debajo:
F_neta_sym = sp.simplify(k_s * (d_s + x_s) - m_s * g_s)
F_neta_sym = sp.simplify(F_neta_sym.subs(m_s * g_s, k_s * d_s))
print(f"  k(d+x) - mg  con mg = kd  ->  {F_neta_sym}   (queda solo k*x)  OK")


# ===========================================================================
# EJERCICIO 6.b.3 - Caja 20 kg en tabla a 37 grados
# ---------------------------------------------------------------------------
# Enunciado: caja de 20 kg en reposo sobre tabla lisa inclinada 37 grados,
# sujeta por soga paralela a la tabla. g = 10, sen(37)=0.60, cos(37)=0.80.
#   (b) soga paralela:  T = mg*sen,  n = mg*cos
#   (c) soga cortada:   a = g*sen (cuesta abajo), n NO cambia
#   (d) soga HORIZONTAL: hay que redescomponer
#   (e) expresion general de n del caso (d)
#
# Geometria del inciso (d), hecha con vectores para no equivocarse de signo.
# Plano que sube hacia +x. Versor cuesta arriba u = (cos, sen).
# Versor normal saliente         nrm = (-sen, cos).
# Peso W = (0, -mg). Tension horizontal hacia el plano: T_vec = (T, 0).
#   eje paralelo:      T*cos - mg*sen = 0   =>  T = mg*tan
#   eje perpendicular: n - mg*cos - T*sen = 0 =>  n = mg*cos + T*sen
# ===========================================================================
titulo("EJERCICIO 6.b.3 - Caja 20 kg en tabla a 37 grados")

m_8 = 20.0
sen37, cos37 = 0.60, 0.80          # FIJADOS POR EL ENUNCIADO
tan37 = sen37 / cos37
peso_8 = m_8 * g

sub("Inciso (b): soga paralela a la tabla")
T_par = peso_8 * sen37
n_par = peso_8 * cos37
check("6.b.3 (b) tension (soga paralela)", T_par, 120.0, "N")
check("6.b.3 (b) reaccion de la tabla", n_par, 160.0, "N")

sub("Inciso (c): se corta la soga")
a_8 = g * sen37
check("6.b.3 (c) aceleracion tras cortar", a_8, 6.0, "m/s^2",
      nota="cuesta abajo; a = g*sen(theta), independiente de la masa")
check("6.b.3 (c) normal tras cortar", peso_8 * cos37, 160.0, "N",
      nota="NO cambia respecto de (b): la soga era paralela al plano y no "
           "tenia componente perpendicular")

sub("Inciso (d): soga HORIZONTAL  <-- punto marcado para revision")
# Resolucion vectorial independiente, sin usar formulas de memoria.
T_sym_d, n_sym_d = sp.symbols("T n", real=True)
S, C = sp.Rational(6, 10), sp.Rational(8, 10)     # sen37, cos37 exactos del enunciado
mg = sp.Integer(200)

u_par = sp.Matrix([C, S])       # versor cuesta arriba
u_prp = sp.Matrix([-S, C])      # versor normal saliente
W = sp.Matrix([0, -mg])         # peso
Tv = sp.Matrix([T_sym_d, 0])    # tension horizontal, hacia el plano (+x)
Nv = n_sym_d * u_prp            # normal

R = W + Tv + Nv                 # resultante; en equilibrio debe ser nula
eq_par = sp.Eq(R.dot(u_par), 0)
eq_prp = sp.Eq(R.dot(u_prp), 0)
sol_d = sp.solve([eq_par, eq_prp], [T_sym_d, n_sym_d], dict=True)[0]

T_d = float(sol_d[T_sym_d])
n_d = float(sol_d[n_sym_d])

print(f"  Ecuacion paralela      : {sp.simplify(R.dot(u_par))} = 0")
print(f"  Ecuacion perpendicular : {sp.simplify(R.dot(u_prp))} = 0")
check("6.b.3 (d) tension horizontal", T_d, 150.0, "N",
      nota="resuelto vectorialmente, sin asumir T = mg*tan")
check("6.b.3 (d) reaccion de la tabla", n_d, 250.0, "N",
      nota="resuelto vectorialmente, sin asumir n = mg*cos + T*sen")

sub("Consistencia algebraica (d) vs (e):  mg*cos + T*sen  ==  mg/cos ?")
# Verificacion SIMBOLICA, valida para todo theta y toda masa, no solo
# para los numeros de este ejercicio.
th_g = sp.symbols("theta", positive=True)
T_gen = m_s * g_s * sp.tan(th_g)
n_gen_d = m_s * g_s * sp.cos(th_g) + T_gen * sp.sin(th_g)
n_gen_e = m_s * g_s / sp.cos(th_g)
diferencia = sp.simplify(n_gen_d - n_gen_e)
print(f"  n(d) = mg*cos + mg*tan*sen = {sp.simplify(n_gen_d)}")
print(f"  n(e) = mg/cos              = {n_gen_e}")
print(f"  n(d) - n(e) = {diferencia}")
if diferencia == 0:
    print("  -> IDENTIDAD verificada para todo theta: mg(cos^2+sen^2)/cos = mg/cos.")
    print("     La afirmacion de consistencia del redactor es CORRECTA.")
else:
    print("  -> NO son identicas: revisar.")

# Chequeo adicional: con los valores REDONDEADOS del enunciado la identidad
# pitagorica podria romperse. Aca no se rompe porque 0.6^2+0.8^2 = 1 exacto.
pit = sen37**2 + cos37**2
print(f"  sen^2(37)+cos^2(37) con los valores del enunciado = {pit:.6f}")
print("  -> exactamente 1: los valores fijados por la catedra son un terno")
print("     pitagorico (3-4-5), asi que no introducen error de redondeo.")
check("6.b.3 (e) n = mg/cos(theta) evaluado", peso_8 / cos37, 250.0, "N",
      nota="coincide con el n del inciso (d): consistente")

sub("Comparacion (b) vs (d) que pide el enunciado")
print(f"  soga paralela   : T = {T_par:6.1f} N   n = {n_par:6.1f} N")
print(f"  soga horizontal : T = {T_d:6.1f} N   n = {n_d:6.1f} N")
print("  La soga horizontal tiene una componente perpendicular que EMPUJA la")
print("  caja contra la tabla, y por eso n crece de 160 N a 250 N. Ademas")
print("  hace falta mas tension porque solo la componente paralela (T*cos)")
print("  trabaja contra el peso.  Fisicamente coherente.")

sub("Inciso (e): limite theta -> 0")
for ang_deg in (37, 20, 10, 1, 0.001):
    t = math.radians(ang_deg)
    print(f"  theta={ang_deg:>7}  T = {peso_8*math.tan(t):8.3f} N   "
          f"n = {peso_8/math.cos(t):8.3f} N")
print(f"  -> T -> 0 y n -> mg = {peso_8:.0f} N. Correcto: sin inclinacion no")
print("     hace falta soga y la tabla soporta el peso entero.")
print("  [COHERENCIA] n > 0 en todos los incisos; nunca sale normal negativa.")


# ===========================================================================
# CHEQUEOS NUMERICOS INCRUSTADOS EN EL MARCO TEORICO
# ---------------------------------------------------------------------------
# Los bloques \begin{chequeo} incluyen algunas preguntas con numero. Se
# verifican tambien, porque son parte del material que vas a estudiar.
# ===========================================================================
titulo("CHEQUEOS DEL MARCO TEORICO (preguntas con numero)")

sub("Masa inercial: misma fuerza, a_A = 6 y a_B = 2 m/s^2")
print(f"  m_B/m_A = a_A/a_B = {6.0/2.0:.1f}  ->  B tiene el TRIPLE de masa.")

sub("Peso/normal: caja de 10 kg con ladrillo de 2 kg encima, g=10")
n_mesa = (10.0 + 2.0) * g
check("normal de la mesa sobre la caja", n_mesa, 120.0, "N",
      nota="la mesa sostiene caja + ladrillo; NO son 100 N")

sub("Tercera ley: manzana de 0.2 kg atraida con ~2 N")
check("fuerza de la manzana sobre la Tierra", 0.2 * g, 2.0, "N",
      nota="mismo modulo; la Tierra no se mueve apreciablemente por su masa")

sub("Hooke: k = 400 N/m estirado 3 cm")
check("modulo de la fuerza elastica", 400.0 * 0.03, 12.0, "N",
      nota="apunta hacia la posicion de equilibrio (restauradora)")


# ===========================================================================
# RESUMEN
# ===========================================================================
titulo("RESUMEN DE LA VERIFICACION")

coinciden = sum(1 for r in _resultados if r[4] == "COINCIDE")
discrepan = [r for r in _resultados if r[4].startswith(">>>")]
sin_valor = sum(1 for r in _resultados if r[4] == "SIN VALOR EN EL DOC")

print(f"  Contrastes con valor afirmado que COINCIDEN : {coinciden}")
print(f"  Contrastes que DISCREPAN                    : {len(discrepan)}")
print(f"  Calculos de referencia sin valor en el doc  : {sin_valor}")

if discrepan:
    print()
    print("  DISCREPANCIAS:")
    for etq, calc, af, u, _, _ in discrepan:
        print(f"    - {etq}: calculado {calc:.4g} {u}, documento {af:g} {u}")
else:
    print()
    print("  No se detectaron discrepancias numericas ni incoherencias fisicas.")

print()
print("  Nota: los ejercicios piden ademas diagramas de cuerpo aislado y")
print("  justificaciones en palabras. Eso no es verificable por codigo y")
print("  queda para la revision cualitativa.")
print()
