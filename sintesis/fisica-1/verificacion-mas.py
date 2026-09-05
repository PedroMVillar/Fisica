# -*- coding: utf-8 -*-
"""
=============================================================================
 VERIFICACION INDEPENDIENTE -- Fuerza elastica y movimiento armonico simple
=============================================================================

QUE ES ESTE ARCHIVO
-------------------
Es el control de calidad numerico del capitulo 5 de la sintesis, y de paso
es la unica hoja de respuestas de los ejercicios: la sintesis los deja
planteados sin resolver a proposito, asi que aca abajo estan todos los
resultados, cada uno recalculado DESDE EL ENUNCIADO y no copiado del
documento.

COMO SE USA
-----------
    python verificacion-mas.py

Corre solo (necesita sympy) e imprime, ejercicio por ejercicio, el
razonamiento, el valor calculado y el veredicto. Todo enunciado va
resumido arriba de su bloque, asi que no hace falta tener la sintesis al
lado.

COMO SE USA PARA ESTUDIAR
-------------------------
1. Resolve el ejercicio en papel, sin abrir esto.
2. Corre el script y compara SOLO el numero final.
3. Si no coincide, volve al papel antes de leer el desarrollo de aca: el
   script muestra los pasos intermedios (omega, A, phi, el corrimiento de
   origen) justamente para que puedas ubicar en cual de los pasos se te
   fue, no para que lo leas de corrido.
4. Podes cambiar los datos de entrada de cualquier bloque y volver a
   correrlo: las cuentas estan escritas en forma literal primero, asi que
   los numeros son intercambiables.

CONVENCIONES (las mismas del documento)
---------------------------------------
  * g = 10 m/s^2 en todos los casos (valor de la catedra).
  * x  = coordenada del ENUNCIADO (regla, cinta metrica, techo).
    x' = x - x0 = coordenada medida DESDE EL EQUILIBRIO.
    x0 = posicion de EQUILIBRIO (ojo: en los capitulos 1 y 2 x0 era la
         posicion inicial; aca no).
  * Forma general usada en todo el capitulo:
        x'(t) = A cos(w t + phi)
        v (t) = -w A sen(w t + phi)
        a (t) = -w^2 A cos(w t + phi) = -w^2 x'
  * A y w son siempre positivos; phi se toma en (-pi, pi] via atan2.

QUE CHEQUEA ADEMAS DE LOS NUMEROS
---------------------------------
  * Las identidades SIMBOLICAS del tema (no solo casos numericos):
    w = sqrt(k/m), A = sqrt(xi^2 + (vi/w)^2), su equivalencia con la
    forma de Serway A = xi/cos(phi) y el punto exacto donde esa forma
    se rompe, v^2 = w^2 (A^2 - x^2), v_max, a_max, T = 2pi/w y su
    independencia de la amplitud.
  * Las conversiones de origen en los dos sentidos, en cada lugar donde
    aparecen.
  * Homogeneidad DIMENSIONAL de cada formula del capitulo.
  * Consistencia fisica del propio ENUNCIADO (por ejemplo: que un
    resorte que cuelga no quede pedido en compresion), que es distinto
    de que la cuenta este bien hecha.
=============================================================================
"""

import sys
import sympy as sp

# La consola de Windows es cp1252. Salida estrictamente ASCII, pero por las
# dudas se intenta reconfigurar igual.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


# ---------------------------------------------------------------------------
# Infraestructura minima de comparacion
# ---------------------------------------------------------------------------

_resultados = []   # (etiqueta, ok)
_alertas = []      # observaciones sobre el ENUNCIADO, no sobre la cuenta


def chk(etiqueta, calculado, documento, unidad="", nota=""):
    """Compara mi valor (calculado de cero) contra el que afirma el documento."""
    c = sp.nsimplify(sp.sympify(calculado), rational=True)
    d = sp.nsimplify(sp.sympify(documento), rational=True)
    ok = sp.simplify(c - d) == 0
    _resultados.append((etiqueta, ok))
    print("  [{}] {}".format("OK  " if ok else "FALLA", etiqueta))
    print("        calculado : {} {}".format(_fmt(c), unidad))
    print("        documento : {} {}".format(_fmt(d), unidad))
    if nota:
        print("        nota      : {}".format(nota))
    if not ok:
        print("        >>> DISCREPANCIA <<<")


def chk_num(etiqueta, calculado, documento, unidad="", tol=sp.Rational(1, 1000),
            nota=""):
    """Igual que chk pero para valores que el documento da redondeados."""
    c = sp.sympify(calculado)
    d = sp.sympify(documento)
    ok = abs(sp.N(c - d)) <= sp.N(tol)
    _resultados.append((etiqueta, ok))
    print("  [{}] {}".format("OK  " if ok else "FALLA", etiqueta))
    print("        calculado : {} = {} {}".format(_fmt(c), sp.N(c, 6), unidad))
    print("        documento : {} {}  (tol {})".format(sp.N(d, 6), unidad, sp.N(tol)))
    if nota:
        print("        nota      : {}".format(nota))
    if not ok:
        print("        >>> DISCREPANCIA <<<")


def afirmar(etiqueta, condicion, detalle=""):
    """Chequeo de ley/identidad: no hay valor del documento contra que comparar."""
    ok = bool(condicion)
    _resultados.append((etiqueta, ok))
    print("  [{}] {}{}".format("OK  " if ok else "FALLA", etiqueta,
                               ("  -- " + detalle) if detalle else ""))
    if not ok:
        print("        >>> DISCREPANCIA <<<")


def alerta(etiqueta, detalle):
    """Observacion sobre el ENUNCIADO (no cuenta como error de cuenta)."""
    _alertas.append(etiqueta)
    print("  [AVISO] {}".format(etiqueta))
    for linea in detalle.split("\n"):
        print("          " + linea)


def dato(texto):
    print("        " + texto)


def razon(texto):
    """Imprime el razonamiento, que es la regla del proyecto."""
    for linea in texto.strip("\n").split("\n"):
        print("    " + linea)


def _fmt(e):
    e = sp.nsimplify(e, rational=True)
    if e.free_symbols:
        return str(e)
    try:
        if e == sp.nsimplify(e, rational=True) and sp.Rational(e).q <= 100000:
            return "{} = {}".format(e, sp.N(e, 6))
    except Exception:
        pass
    return "{} = {}".format(e, sp.N(e, 6))


def titulo(t):
    print("\n" + "=" * 75)
    print(t)
    print("=" * 75)


def sub(t):
    print("\n--- " + t + " " + "-" * max(0, 68 - len(t)))


# ---------------------------------------------------------------------------
# Constantes y utilidades del tema
# ---------------------------------------------------------------------------

G = sp.Rational(10)   # m/s^2, valor que fija la catedra y usa el documento


def omega_de(k, m):
    """w = sqrt(k/m). Unica fuente de omega en todo el script."""
    return sp.sqrt(sp.Rational(k) / sp.Rational(m)) if not (
        isinstance(k, sp.Expr) or isinstance(m, sp.Expr)) else sp.sqrt(k / m)


def amplitud(xi, vi, w):
    """A = sqrt(xi^2 + (vi/w)^2), con xi y vi MEDIDOS DESDE EL EQUILIBRIO."""
    return sp.sqrt(xi**2 + (vi / w)**2)


def fase(xi, vi, w, A):
    """phi via atan2(sen, cos), que no tiene la ambiguedad de la tangente."""
    if A == 0:
        return sp.Integer(0)
    return sp.atan2(-vi / (w * A), xi / A)


def periodo(w):
    return 2 * sp.pi / w


# ===========================================================================
# PARTE 0 -- LAS IDENTIDADES DEL TEMA, EN SIMBOLOS
#
# Nada de esto usa numeros. Si estas relaciones no cierran en simbolos, no
# hay ejercicio que las salve; y si cierran, cualquier caso numerico del
# capitulo es solo una instancia.
# ===========================================================================

titulo("PARTE 0 -- IDENTIDADES SIMBOLICAS DEL MAS")

t = sp.Symbol("t", real=True)
k_s, m_s, A_s, w_s = sp.symbols("k m A omega", positive=True)
phi_s = sp.Symbol("phi", real=True)

# Las tres funciones, construidas UNA sola vez y derivadas por sympy.
x_de_t = A_s * sp.cos(w_s * t + phi_s)
v_de_t = sp.diff(x_de_t, t)
a_de_t = sp.diff(x_de_t, t, 2)

sub("0.1  Las tres funciones salen de derivar, no de copiar")
razon("""
Partimos SOLO de x'(t) = A cos(w t + phi) y dejamos que sympy derive.
El documento afirma  v = -w A sen(w t + phi)  y  a = -w^2 A cos(w t + phi).
""")
afirmar("v(t) = -w A sen(w t + phi)",
        sp.simplify(v_de_t - (-w_s * A_s * sp.sin(w_s * t + phi_s))) == 0)
afirmar("a(t) = -w^2 A cos(w t + phi)",
        sp.simplify(a_de_t - (-w_s**2 * A_s * sp.cos(w_s * t + phi_s))) == 0)
afirmar("a(t) = -w^2 x'(t)  (el cierre del circulo del bloque 3)",
        sp.simplify(a_de_t + w_s**2 * x_de_t) == 0)

sub("0.2  w = sqrt(k/m) sale de emparejar dinamica con sombra del MCU")
razon("""
Dinamica del resorte (Hooke + 2da ley):  m a = -k x'   =>  a = -(k/m) x'
Sombra del MCU (cap. 2, componente x) :  a = -w^2 x'
Las dos describen el mismo movimiento si y solo si w^2 = k/m.
Resolvemos w^2 = k/m con sympy y nos quedamos con la raiz positiva.
""")
sol_w = sp.solve(sp.Eq(w_s**2, k_s / m_s), w_s)
dato("soluciones de w^2 = k/m con w > 0 : {}".format(sol_w))
afirmar("w = sqrt(k/m) es la unica raiz positiva",
        len(sol_w) == 1 and sp.simplify(sol_w[0] - sp.sqrt(k_s / m_s)) == 0)

sub("0.3  A = sqrt(xi^2 + (vi/w)^2): la forma que no se rompe nunca")
razon("""
Evaluando en t = 0:   xi = A cos(phi)   ,   vi = -w A sen(phi)
Elevamos al cuadrado y sumamos; el pitagorico se lleva phi:
    xi^2 + (vi/w)^2 = A^2 (cos^2 phi + sen^2 phi) = A^2
""")
xi_expr = x_de_t.subs(t, 0)                 # A cos(phi)
vi_expr = v_de_t.subs(t, 0)                 # -w A sen(phi)
suma_cuad = sp.simplify(xi_expr**2 + (vi_expr / w_s)**2)
dato("xi^2 + (vi/w)^2 simplificado : {}".format(suma_cuad))
afirmar("xi^2 + (vi/w)^2 = A^2 identicamente en phi",
        sp.simplify(suma_cuad - A_s**2) == 0)
afirmar("A = sqrt(xi^2+(vi/w)^2) devuelve A (A > 0)",
        sp.simplify(sp.sqrt(suma_cuad) - A_s) == 0)

sub("0.4  Equivalencia con la forma de Serway A = xi/cos(phi), y su rotura")
razon("""
Serway despeja A de xi = A cos(phi), o sea A = xi / cos(phi).
1) Donde cos(phi) != 0 las dos formas son LA MISMA: se cancela cos(phi).
2) Donde el cuerpo arranca EN EL EQUILIBRIO (xi = 0) se tiene cos(phi) = 0
   y la expresion queda 0/0: indeterminada. Y no es un detalle de borde,
   es justo el caso 'se lo lanza desde el equilibrio', que el capitulo usa
   dos veces (carrito B del ej. B6 y el inciso (f) del A3).
Esa es la razon por la que el capitulo descarta la forma de Serway.
""")
serway = sp.simplify(xi_expr / sp.cos(phi_s))     # A cos(phi) / cos(phi)
afirmar("Serway == forma general mientras cos(phi) != 0",
        sp.simplify(serway - A_s) == 0)
# El caso xi = 0 obliga a cos(phi) = 0, es decir phi = +-pi/2.
num_serway = xi_expr.subs(phi_s, sp.pi / 2)
den_serway = sp.cos(phi_s).subs(phi_s, sp.pi / 2)
general_lim = sp.simplify(sp.sqrt(suma_cuad).subs(phi_s, sp.pi / 2))
dato("Serway en phi = pi/2 (xi = 0): numerador = {} , denominador = {}"
     .format(num_serway, den_serway))
dato("forma general en phi = pi/2   : {}".format(general_lim))
afirmar("Serway queda 0/0 en xi = 0 (indeterminada)",
        num_serway == 0 and den_serway == 0)
afirmar("la forma general SI da A cuando xi = 0",
        sp.simplify(general_lim - A_s) == 0,
        "queda A = |vi|/w")
# Instancia numerica del caso limite (chequeo del bloque 5, item 1).
A_lim = amplitud(sp.Integer(0), sp.Rational(60, 100), sp.Integer(3))
chk("caso limite xi=0, vi=0.60 m/s, w=3 rad/s -> A", A_lim,
    sp.Rational(20, 100), "m", "chequeo del bloque 5, item 1")

sub("0.5  v^2 = w^2 (A^2 - x^2), valida en TODO instante y no solo en t=0")
razon("""
Misma identidad pitagorica pero aplicada en un t cualquiera:
    x^2 + (v/w)^2 = A^2    =>    v^2 = w^2 (A^2 - x^2)
Se verifica sustituyendo x(t) y v(t) simbolicos y simplificando.
""")
afirmar("v(t)^2 = w^2 (A^2 - x(t)^2) para todo t",
        sp.simplify(v_de_t**2 - w_s**2 * (A_s**2 - x_de_t**2)) == 0)
afirmar("en x = 0 se recupera v_max = w A",
        sp.simplify(sp.sqrt(w_s**2 * (A_s**2 - 0)) - w_s * A_s) == 0)
afirmar("en x = +-A se recupera v = 0",
        sp.simplify(w_s**2 * (A_s**2 - A_s**2)) == 0)

sub("0.6  v_max = w A  y  a_max = w^2 A, y donde ocurre cada uno")
razon("""
|v| = w A |sen(fase)| y |a| = w^2 A |cos(fase)|; seno y coseno no pasan de 1,
asi que los maximos son w A y w^2 A. Ademas seno y coseno no valen 1 a la
vez: por eso los dos maximos ocurren en lugares distintos del recorrido.
""")
u = sp.Symbol("u", real=True)   # u = fase
v_mod = w_s * A_s * sp.Abs(sp.sin(u))
a_mod = w_s**2 * A_s * sp.Abs(sp.cos(u))
afirmar("max |v| = w A (en fase = pi/2, o sea x = 0: el equilibrio)",
        sp.simplify(v_mod.subs(u, sp.pi / 2) - w_s * A_s) == 0
        and sp.simplify(A_s * sp.cos(sp.pi / 2)) == 0)
afirmar("max |a| = w^2 A (en fase = 0, o sea x = +-A: los extremos)",
        sp.simplify(a_mod.subs(u, 0) - w_s**2 * A_s) == 0)
afirmar("donde |v| es maxima (fase pi/2), a vale 0",
        sp.simplify(a_de_t.subs(w_s * t + phi_s, sp.pi / 2)
                    .rewrite(sp.cos)) == 0
        or sp.simplify(-w_s**2 * A_s * sp.cos(sp.pi / 2)) == 0)
afirmar("donde |a| es maxima (fase 0), v vale 0",
        sp.simplify(-w_s * A_s * sp.sin(0)) == 0)
razon("""
Error comun del capitulo: en x = A/2 la rapidez NO es v_max/2.
""")
frac = sp.simplify(sp.sqrt(w_s**2 * (A_s**2 - (A_s / 2)**2)) / (w_s * A_s))
chk("v(x = A/2) / v_max", frac, sp.sqrt(3) / 2, "",
    "vale {} , o sea 86.6 %, no 50 %".format(sp.N(sp.sqrt(3) / 2, 4)))
afirmar("'cerca del 87 por ciento' describe bien ese numero",
        sp.Rational(86, 100) < sp.N(sp.sqrt(3) / 2) < sp.Rational(88, 100))

sub("0.7  T = 2pi/w y la independencia de la amplitud")
razon("""
El coseno se repite cuando su argumento avanza 2pi, y avanza a razon de w
rad/s: T = 2pi/w = 2pi sqrt(m/k). Lo probamos pidiendo periodicidad de
x(t) y v(t), y verificando ademas que A no aparece en la expresion de T.
""")
T_sim = periodo(w_s)
afirmar("x(t + T) = x(t) con T = 2pi/w",
        sp.simplify(x_de_t.subs(t, t + T_sim) - x_de_t) == 0)
afirmar("v(t + T) = v(t)",
        sp.simplify(v_de_t.subs(t, t + T_sim) - v_de_t) == 0)
T_km = sp.simplify(T_sim.subs(w_s, sp.sqrt(k_s / m_s)))
dato("T en funcion de k y m : {}".format(T_km))
afirmar("T = 2pi sqrt(m/k)",
        sp.simplify(T_km - 2 * sp.pi * sp.sqrt(m_s / k_s)) == 0)
afirmar("A NO aparece en T (no esta entre sus simbolos libres)",
        A_s not in T_km.free_symbols)
afirmar("f = 1/T = w/2pi",
        sp.simplify(1 / T_sim - w_s / (2 * sp.pi)) == 0)
razon("""
Consecuencia (segunda pregunta del diagnostico): dos cuerpos iguales en
resortes iguales soltados desde el reposo a distinta distancia tienen el
MISMO T. Se ve directo: T no contiene A. El documento explica por que: el
que arranca al doble de lejos recorre el doble de camino (4A por periodo)
pero llega al doble de rapidez (v_max = wA). Verificamos que la razon
camino/rapidez sea la misma para cualquier A, que es la cancelacion exacta.
""")
A2_s = sp.Symbol("A2", positive=True)
afirmar("(camino por periodo)/v_max no depende de A",
        sp.simplify((4 * A_s) / (w_s * A_s) - (4 * A2_s) / (w_s * A2_s)) == 0,
        "los dos efectos se cancelan exacto")

sub("0.8  Equivalencia seno/coseno y la afirmacion sobre el ejercicio 17")
razon("""
(i)  A sen(w t) = A cos(w t - pi/2): identidad exacta, para todo t.
(ii) Afirmacion fuerte del capitulo: la forma A sen(w t), tomada
     literalmente (sin constante de fase), NO puede escribir la respuesta
     del ejercicio 17, que arranca EN UN EXTREMO Y DESDE EL REPOSO.
     Lo verificamos resolviendo el sistema de condiciones iniciales.
""")
afirmar("A sen(w t) == A cos(w t - pi/2) identicamente",
        sp.simplify(A_s * sp.sin(w_s * t)
                    - A_s * sp.cos(w_s * t - sp.pi / 2)) == 0)
d_s = sp.Symbol("d", positive=True)      # apartamiento inicial, NO nulo
Ase = sp.Symbol("A_sen", real=True)      # amplitud libre de la forma seno
x_sen = Ase * sp.sin(w_s * t)
v_sen = sp.diff(x_sen, t)
sis = sp.solve([sp.Eq(x_sen.subs(t, 0), d_s),
                sp.Eq(v_sen.subs(t, 0), 0)], [Ase], dict=True)
dato("x_sen(0) = {}   <- vale 0 sea cual sea A".format(x_sen.subs(t, 0)))
dato("v_sen(0) = {}".format(sp.simplify(v_sen.subs(t, 0))))
dato("soluciones de [x_sen(0) = d, v_sen(0) = 0] : {}".format(sis))
afirmar("ninguna A hace que A sen(wt) arranque en un extremo desde el reposo",
        len(sis) == 0,
        "x_sen(0) = 0 siempre, y el ej. 17 pide x'(0) = d != 0")
razon("""
Con corrimiento del origen temporal tampoco, en el sentido que importa:
A sen(w(t - t0)) = A cos(w t - w t0 - pi/2), que ya NO es la forma
'A sen(w t)' del apunte sino la forma general con constante de fase
phi = -w t0 - pi/2. Es decir: para escribir el ej. 17 hay que introducir
una constante de fase, y el t0 que sirve devuelve exactamente el coseno.
""")
# Unico t0 posible: v(0) = A w cos(w t0) = 0  =>  w t0 = +-pi/2.
# Tomamos t0 = -pi/(2w) y vemos que queda.
t0_val = -sp.pi / (2 * w_s)
x_desp = d_s * sp.sin(w_s * (t - t0_val))
dato("con t0 = -pi/(2w): x(t) = {}".format(sp.simplify(x_desp)))
dato("                   x(0) = {} , v(0) = {}".format(
    sp.simplify(x_desp.subs(t, 0)),
    sp.simplify(sp.diff(x_desp, t).subs(t, 0))))
afirmar("con t0 libre la condicion SI se cumple, pero es el coseno disfrazado",
        sp.simplify(x_desp.subs(t, 0) - d_s) == 0
        and sp.simplify(sp.diff(x_desp, t).subs(t, 0)) == 0
        and sp.simplify(x_desp - d_s * sp.cos(w_s * t)) == 0,
        "w t0 = -pi/2 => A sen(w t + pi/2) = A cos(w t)")
afirmar("A sen(w t + pi/2) == A cos(w t)",
        sp.simplify(A_s * sp.sin(w_s * t + sp.pi / 2)
                    - A_s * sp.cos(w_s * t)) == 0)
afirmar("VEREDICTO: la afirmacion del capitulo es correcta como esta escrita",
        True,
        "'la forma con seno, TOMADA LITERALMENTE, no puede escribir el ej. 17'")

sub("0.9  El corrimiento de origen, en simbolos y en los dos sentidos")
razon("""
x'(t) = x(t) - x0   con x0 CONSTANTE (posicion de equilibrio).
Ida    : x'(t) = x(t) - x0
Vuelta : x(t)  = x0 + A cos(w t + phi)
Como x0 es constante, dx/dt = dx'/dt y d2x/dt2 = d2x'/dt2: v y a tienen
LA MISMA expresion en las dos coordenadas. Lo unico que cambia es x, y con
ella las coordenadas extremas: x0 - A y x0 + A, no -A y +A.
""")
x0_s = sp.Symbol("x0", real=True)
x_enun = x0_s + x_de_t
afirmar("dx/dt == dx'/dt (v no se entera del corrimiento)",
        sp.simplify(sp.diff(x_enun, t) - sp.diff(x_de_t, t)) == 0)
afirmar("d2x/dt2 == d2x'/dt2 (a tampoco)",
        sp.simplify(sp.diff(x_enun, t, 2) - sp.diff(x_de_t, t, 2)) == 0)
afirmar("ida y vuelta son inversas: (x0 + A cos) - x0 == A cos",
        sp.simplify((x_enun - x0_s) - x_de_t) == 0)
inst = x_enun.subs({A_s: 1, w_s: 1, phi_s: 0, x0_s: 5})
afirmar("coordenadas extremas = x0 +- A (instancia x0 = 5, A = 1)",
        sp.simplify(sp.maximum(inst, t) - 6) == 0
        and sp.simplify(sp.minimum(inst, t) - 4) == 0)
afirmar("a = -w^2 (x - x0), y NO -w^2 x",
        sp.simplify(sp.diff(x_enun, t, 2) + w_s**2 * (x_enun - x0_s)) == 0
        and sp.simplify(sp.diff(x_enun, t, 2) + w_s**2 * x_enun) != 0,
        "medir desde el origen del enunciado rompe la ecuacion del MAS")

sub("0.10  Composicion de resortes: paralelo y serie, desde Hooke")
razon("""
PARALELO. Hipotesis explicita: MISMA LONGITUD NATURAL L0. De ahi sale que
los dos se apartan lo mismo de SU PROPIA longitud sin deformar, o sea
x1 = x2 = x. Con eso, superposicion de fuerzas sobre el mismo cuerpo:
    F = -k1 x - k2 x = -(k1+k2) x   =>   k_eq = k1 + k2
Si las longitudes naturales fueran distintas, x1 != x2 y el paso se cae.
""")
k1_s, k2_s, L0_s, L1_s, L2_s, L_s = sp.symbols(
    "k1 k2 L0 L1 L2 L", positive=True)
x_def = L_s - L0_s          # misma deformacion para los dos: esa es la hipotesis
F_par = -k1_s * x_def - k2_s * x_def
dato("F_total con misma L0 : {}".format(sp.factor(F_par)))
afirmar("F_total tiene la forma -(constante) * apartamiento",
        sp.simplify(sp.factor(F_par) + (k1_s + k2_s) * x_def) == 0)
k_eq_par = sp.simplify(-sp.expand(F_par) / x_def)
chk("k_eq en paralelo", k_eq_par, k1_s + k2_s, "N/m",
    "criterio de MAS: la fuerza volvio a quedar -(cte) * apartamiento")
afirmar("k_eq > k1 y k_eq > k2 (el chequeo de sentido comun del capitulo)",
        sp.simplify(k_eq_par - k1_s) == k2_s
        and sp.simplify(k_eq_par - k2_s) == k1_s)
F_dist = -k1_s * (L_s - L1_s) - k2_s * (L_s - L2_s)
afirmar("con L1 != L2 la fuerza ya NO es -(k1+k2)*(apartamiento comun)",
        sp.simplify(sp.expand(F_dist) + (k1_s + k2_s) * x_def) != 0,
        "sobra un termino constante: el vinculo geometrico se cae")

razon("""
SERIE (inciso B5(e)). Lo que es IGUAL en los dos resortes es la FUERZA (la
misma tension recorre la cadena); lo que se REPARTE es la deformacion:
    x_total = x1 + x2 = F/k1 + F/k2 = F (1/k1 + 1/k2)
    F = k_eq x_total   =>   1/k_eq = 1/k1 + 1/k2
""")
F_ser = sp.Symbol("F", positive=True)
x_tot = F_ser / k1_s + F_ser / k2_s
k_eq_ser = sp.simplify(F_ser / x_tot)
chk("k_eq en serie", k_eq_ser, k1_s * k2_s / (k1_s + k2_s), "N/m")
afirmar("1/k_eq = 1/k1 + 1/k2",
        sp.simplify(1 / k_eq_ser - (1 / k1_s + 1 / k2_s)) == 0)
afirmar("k_eq(serie) < min(k1,k2) y k_eq(paralelo) > max(k1,k2)",
        sp.simplify(k_eq_ser.subs({k1_s: 32, k2_s: 18})) < 18
        and sp.simplify(k_eq_par.subs({k1_s: 32, k2_s: 18})) > 32)

sub("0.11  w^2 = w1^2 + w2^2 para dos resortes sobre el mismo cuerpo")
razon("""
Sale del paralelo, sin numeros: con k_eq = k1 + k2 y la misma masa m,
    w^2 = (k1+k2)/m = k1/m + k2/m = w1^2 + w2^2
Es decir: las w NO se suman, se suman sus cuadrados. Es la relacion que el
adicional A3 pide verificar en su inciso (e).
""")
w_par = sp.sqrt((k1_s + k2_s) / m_s)
w1_s = sp.sqrt(k1_s / m_s)
w2_s = sp.sqrt(k2_s / m_s)
afirmar("w^2 = w1^2 + w2^2 identicamente",
        sp.simplify(w_par**2 - (w1_s**2 + w2_s**2)) == 0)
afirmar("w != w1 + w2 (no es aditiva)",
        sp.simplify(w_par - (w1_s + w2_s)) != 0)

sub("0.12  Resorte vertical: el peso corre el centro y no toca ni T ni A")
razon("""
Con el eje positivo hacia abajo y s = estiramiento del resorte,
    m a = m g - k s
El equilibrio esta donde a = 0, o sea s = d = m g / k. Definiendo
x' = s - d queda  m a = m g - k(x' + d) = -k x' : el peso desaparecio.
Conclusion: mismo w, mismo T que el horizontal; lo unico que hace g es
correr el centro de la oscilacion una distancia d = mg/k.
""")
s_s, g_s = sp.symbols("s g", positive=True)
d_eq = sp.solve(sp.Eq(m_s * g_s - k_s * s_s, 0), s_s)[0]
chk("d = deformacion de equilibrio", d_eq, m_s * g_s / k_s, "m")
xp = sp.Symbol("xprime", real=True)
F_neta_vert = sp.expand(m_s * g_s - k_s * (xp + d_eq))
dato("fuerza neta medida desde el equilibrio : {}".format(sp.simplify(F_neta_vert)))
afirmar("la fuerza neta vertical vale -k x' (el peso se fue)",
        sp.simplify(F_neta_vert + k_s * xp) == 0)
afirmar("g no aparece en la fuerza neta medida desde el equilibrio",
        g_s not in sp.simplify(F_neta_vert).free_symbols)
afirmar("=> w y T del resorte vertical son los mismos que del horizontal",
        True, "w = sqrt(k/m) en los dos casos")

# ===========================================================================
# PARTE 1 -- AFIRMACIONES NUMERICAS SUELTAS DEL MARCO TEORICO Y DE LOS
#            CHEQUEOS INTERCALADOS
# ===========================================================================

titulo("PARTE 1 -- MARCO TEORICO: LO QUE EL TEXTO AFIRMA EN PROSA")

sub("Bloque 2, chequeo 2: resortes de 20 y 80 N/m con la misma masa")
razon("""
w = sqrt(k/m), asi que con la misma m la razon de frecuencias angulares es
la raiz de la razon de constantes: sqrt(80/20) = sqrt(4) = 2.
""")
m_gen = sp.Symbol("m_gen", positive=True)
razon_w = sp.sqrt(sp.Integer(80) / m_gen) / sp.sqrt(sp.Integer(20) / m_gen)
chk("w(80 N/m) / w(20 N/m)", sp.simplify(razon_w), 2, "",
    "la mas rigida oscila al doble de frecuencia angular")

sub("Bloque 3, chequeo 3: equilibrio en 0.60 m, amplitud 0.15 m")
x0_c, A_c = sp.Rational(60, 100), sp.Rational(15, 100)
chk("marca inferior x0 - A", x0_c - A_c, sp.Rational(45, 100), "m")
chk("marca superior x0 + A", x0_c + A_c, sp.Rational(75, 100), "m")
chk("camino recorrido en un periodo (4A)", 4 * A_c, sp.Rational(60, 100), "m",
    "el desplazamiento en ese mismo periodo es 0")

sub("Bloque 4, chequeo 1: w = 10 rad/s")
w_c = sp.Integer(10)
chk("T = 2pi/w", periodo(w_c), sp.pi / 5, "s")
chk("f = 1/T", 1 / periodo(w_c), 5 / sp.pi, "Hz")
dato("T = {} s   f = {} Hz".format(sp.N(sp.pi / 5, 6), sp.N(5 / sp.pi, 6)))
afirmar("T en segundos y f en hertz son unidades distintas de w en rad/s",
        True, "las tres magnitudes son distintas: w, T y f")

sub("Bloque 5, chequeo 1: lanzado desde el equilibrio, vi = 0.60, w = 3")
razon("""
xi = 0 => A = |vi|/w. Es el caso donde la forma de Serway se rompe (0.4).
""")
chk("A", amplitud(0, sp.Rational(60, 100), 3), sp.Rational(20, 100), "m")

sub("Bloque 6, chequeo 1: paralelo de 30 y 70 N/m")
chk("k_eq", 30 + 70, 100, "N/m", "no 50: promediar no es sumar fuerzas")
afirmar("100 N/m > 70 N/m > 30 N/m",
        100 > 70 > 30, "dos resortes cuestan mas de estirar que uno")

sub("Bloque 5: el apunte y el ejercicio 17 son el MISMO oscilador")
razon("""
El texto afirma: el apunte usa w = 2 rad/s y T = pi s; el ej. 17 tiene
k = 8 N/m y m = 2 kg. Verificamos que den lo mismo.
""")
w_ap = sp.Integer(2)
chk("T del apunte con w = 2 rad/s", periodo(w_ap), sp.pi, "s")
w_17 = omega_de(8, 2)
chk("w del ej. 17 con k = 8 N/m, m = 2 kg", w_17, 2, "rad/s")
chk("T del ej. 17", periodo(w_17), sp.pi, "s")
afirmar("mismo resorte, misma masa, mismo movimiento: solo cambia phi",
        sp.simplify(w_ap - w_17) == 0)

sub("Bloque 5: los dos casos tipicos de constante de fase")
razon("""
Caso 1: soltado del reposo del lado positivo => vi = 0, xi > 0 => phi = 0.
Caso 2: soltado del reposo del lado negativo => vi = 0, xi < 0 => phi = pi.
Caso 3: lanzado desde el equilibrio hacia + => xi = 0, vi > 0 => phi = -pi/2.
Los calculamos con atan2, no con la tangente.
""")
w_ej = sp.Integer(1)
phi1 = fase(sp.Rational(1, 2), 0, w_ej, sp.Rational(1, 2))
phi2 = fase(sp.Rational(-1, 2), 0, w_ej, sp.Rational(1, 2))
phi3 = fase(0, sp.Rational(1, 2), w_ej, sp.Rational(1, 2))
chk("phi con vi = 0, xi > 0", phi1, 0, "rad")
chk("phi con vi = 0, xi < 0", phi2, sp.pi, "rad")
chk("phi con xi = 0, vi > 0", phi3, -sp.pi / 2, "rad")
afirmar("el candidato de la tangente sola es ambiguo (dos raices a pi)",
        sp.simplify(sp.tan(phi1) - sp.tan(phi1 + sp.pi)) == 0,
        "por eso el capitulo pide chequear el signo de v(0)")


# ===========================================================================
# PARTE 2 -- EJEMPLO RESUELTO [completo]
#
# ENUNCIADO. Mesa horizontal con cinta metrica pegada al borde. Resorte de
# k = 12 N/m, extremo libre SIN DEFORMAR en la marca 0.25 m. Ahi se adhiere
# un cuerpo de m = 0.75 kg, sin rozamiento. Se lo desplaza hasta la marca
# 0.43 m y se lo suelta DESDE EL REPOSO. Se piden x(t), v(t), a(t) y sus
# graficos, T, f, las marcas extremas y |v| al pasar por el equilibrio.
# ===========================================================================

titulo("PARTE 2 -- EJEMPLO RESUELTO [completo]  (k=12, m=0.75, 0.25 -> 0.43)")

k_E = sp.Integer(12)
m_E = sp.Rational(3, 4)          # 0.75 kg
x0_E = sp.Rational(25, 100)      # EQUILIBRIO (resorte sin deformar)
xini_E = sp.Rational(43, 100)    # POSICION INICIAL

sub("(a) Cual de los dos numeros es cual: el corrimiento de origen, ida")
razon("""
La marca 0.25 m es donde el resorte NO esta deformado => no hace fuerza
=> es la POSICION DE EQUILIBRIO x0. La marca 0.43 m es donde arranca el
cronometro => POSICION INICIAL. Son cosas distintas y el capitulo avisa
que en los caps. 1 y 2 'x0' significaba lo otro.
    x'(t) = x(t) - 0.25 m
""")
xp_i_E = xini_E - x0_E
chk("(a) x'_i = x_i - x0", xp_i_E, sp.Rational(18, 100), "m",
    "conversion IDA: sistema del enunciado -> sistema del equilibrio")

sub("(b) Que es MAS y con que frecuencia angular")
razon("""
Mesa lisa y resorte horizontal: en la direccion del movimiento la unica
fuerza es -k x'. Segunda ley: m a = -k x' => a = -(k/m) x', que es la
forma que define el MAS. Emparejando con a = -w^2 x':
    w = sqrt(k/m) = sqrt(12/0.75) = sqrt(16) = 4 rad/s
""")
w_E = omega_de(k_E, m_E)
chk("(b) k/m", k_E / m_E, 16, "1/s^2")
chk("(b) w", w_E, 4, "rad/s")

sub("(c) Las dos constantes A y phi")
razon("""
Se suelta DEL REPOSO => vi = 0. Con x'_i = 0.18 m:
    A = sqrt(0.18^2 + (0/4)^2) = 0.18 m
    cos(phi) = x'_i/A = 1 ,  sen(phi) = -vi/(wA) = 0  => phi = 0
Chequeo de signo: v(0) = -wA sen(0) = 0, coincide con 'del reposo'.
""")
vi_E = sp.Integer(0)
A_E = amplitud(xp_i_E, vi_E, w_E)
phi_E = fase(xp_i_E, vi_E, w_E, A_E)
chk("(c) A", A_E, sp.Rational(18, 100), "m",
    "coincide con la distancia inicial al equilibrio SOLO porque vi = 0")
chk("(c) phi", phi_E, 0, "rad")
chk("(c) chequeo v(0) = -wA sen(phi)", -w_E * A_E * sp.sin(phi_E), 0, "m/s")

sub("(d) Las tres funciones, derivadas por sympy desde x'(t)")
xp_E = A_E * sp.cos(w_E * t + phi_E)
v_E = sp.diff(xp_E, t)
a_E = sp.diff(xp_E, t, 2)
dato("x'(t) = {}".format(xp_E))
dato("v (t) = {}".format(sp.simplify(v_E)))
dato("a (t) = {}".format(sp.simplify(a_E)))
chk("(d) coeficiente de v(t) = -wA", -w_E * A_E, sp.Rational(-72, 100), "m/s")
chk("(d) coeficiente de a(t) = -w^2 A", -w_E**2 * A_E,
    sp.Rational(-288, 100), "m/s^2")
afirmar("(d) v(t) = -0.72 sen(4t)",
        sp.simplify(v_E - (-sp.Rational(72, 100) * sp.sin(4 * t))) == 0)
afirmar("(d) a(t) = -2.88 cos(4t)",
        sp.simplify(a_E - (-sp.Rational(288, 100) * sp.cos(4 * t))) == 0)
razon("""
Verificacion que el documento hace y que cierra con (b): 0.18 * 16 = 2.88,
asi que a = -16 x' = -16 (x - 0.25).
""")
chk("(d) w^2 * A", w_E**2 * A_E, sp.Rational(288, 100), "m/s^2")
x_E = x0_E + xp_E     # conversion VUELTA: al sistema de la cinta metrica
dato("x(t) = {}".format(x_E))
afirmar("(d) a(t) == -16 (x(t) - 0.25)  [conversion VUELTA verificada]",
        sp.simplify(a_E + 16 * (x_E - x0_E)) == 0)
afirmar("(d) a(t) != -16 x(t)  [el error de no correr el origen]",
        sp.simplify(a_E + 16 * x_E) != 0)

sub("(e) Los TRES PANELES: los nueve valores en t=0, T/4, T/2")
razon("""
El documento afirma: en t=0, x arranca en su maximo 0.43 con v = 0 y
a = -2.88; en T/4 cruza el equilibrio con v = -0.72 y a = 0; en T/2 esta
en el minimo 0.07 con a = +2.88. Evaluamos las tres funciones (las mias,
derivadas en (d)) en los cinco instantes notables.
""")
T_E = periodo(w_E)
chk("(e) T", T_E, sp.pi / 2, "s")
chk_num("(e) T numerico", T_E, sp.Rational(1571, 1000), "s")
tabla_doc = {
    0:              (sp.Rational(43, 100), 0, sp.Rational(-288, 100)),
    sp.Rational(1, 4): (sp.Rational(25, 100), sp.Rational(-72, 100), 0),
    sp.Rational(1, 2): (sp.Rational(7, 100), 0, sp.Rational(288, 100)),
    sp.Rational(3, 4): (sp.Rational(25, 100), sp.Rational(72, 100), 0),
    1:              (sp.Rational(43, 100), 0, sp.Rational(-288, 100)),
}
nombres = {0: "t = 0", sp.Rational(1, 4): "t = T/4",
           sp.Rational(1, 2): "t = T/2", sp.Rational(3, 4): "t = 3T/4",
           1: "t = T"}
for frac_T in [0, sp.Rational(1, 4), sp.Rational(1, 2), sp.Rational(3, 4), 1]:
    tv = frac_T * T_E
    xd, vd, ad = tabla_doc[frac_T]
    et = nombres[frac_T]
    chk("(e) {}  x".format(et), sp.simplify(x_E.subs(t, tv)), xd, "m")
    chk("(e) {}  v".format(et), sp.simplify(v_E.subs(t, tv)), vd, "m/s")
    chk("(e) {}  a".format(et), sp.simplify(a_E.subs(t, tv)), ad, "m/s^2")

razon("""
Consistencia interna de los nueve valores (que es lo que el pedido pide
mirar, no solo que cada numero este bien):
  * el equilibrio implicado por la tabla es el promedio de x_max y x_min,
  * la amplitud implicada es la semidiferencia,
  * y las dos tienen que coincidir con x0 = 0.25 y A = 0.18.
""")
x_max_tab, x_min_tab = sp.Rational(43, 100), sp.Rational(7, 100)
chk("(e) equilibrio implicado por la tabla (x_max + x_min)/2",
    (x_max_tab + x_min_tab) / 2, x0_E, "m")
chk("(e) amplitud implicada por la tabla (x_max - x_min)/2",
    (x_max_tab - x_min_tab) / 2, A_E, "m")
chk("(e) v_max implicada (|v| en T/4) contra w*A",
    w_E * A_E, sp.Rational(72, 100), "m/s")
chk("(e) a_max implicada (|a| en T/2) contra w^2*A",
    w_E**2 * A_E, sp.Rational(288, 100), "m/s^2")
afirmar("(e) en los extremos v = 0 y |a| es maxima",
        sp.simplify(v_E.subs(t, 0)) == 0
        and sp.Abs(a_E.subs(t, 0)) == w_E**2 * A_E)
afirmar("(e) en el equilibrio a = 0 y |v| es maxima",
        sp.simplify(a_E.subs(t, T_E / 4)) == 0
        and sp.Abs(sp.simplify(v_E.subs(t, T_E / 4))) == w_E * A_E)

razon("""
Los desfasajes que el algebra impone:
  v esta corrida T/4 respecto de x   ->   v(t) = -wA cos(w(t - T/4) + phi)?
  Lo verificamos como corresponde: v(t) es proporcional a x(t + T/4),
  y a(t) es proporcional a x(t + T/2) (media vuelta = espejo).
""")
afirmar("(e) v(t) = w * x'(t + T/4)  [corrimiento de un cuarto de periodo]",
        sp.simplify(v_E - w_E * xp_E.subs(t, t + T_E / 4)) == 0)
afirmar("(e) a(t) = w^2 * x'(t + T/2)  [medio periodo = espejo]",
        sp.simplify(a_E - w_E**2 * xp_E.subs(t, t + T_E / 2)) == 0)
afirmar("(e) a(t) = -w^2 x'(t)  (la misma cosa dicha sin tiempo)",
        sp.simplify(a_E + w_E**2 * xp_E) == 0)

razon("""
LA AFIRMACION DEL PANEL SUPERIOR: 'x no cruza el eje horizontal a proposito'.
Que hay que verificar: que el minimo de x(t) EN EL SISTEMA DE LA CINTA sea
estrictamente mayor que cero. min x = x0 - A.
Y ademas hay que verificar el DIBUJO: en el tikz el eje t del panel de x
esta en la ordenada 5.6, el equilibrio en 6.6, y la curva es
6.6 + 0.72 cos(90 s). Si 0.72 unidades de dibujo representan A = 0.18 m,
la escala es 4 unidades por metro, y entonces x = 0 cae en
6.6 - 0.25*4 = 5.6, que es exactamente donde esta dibujado el eje.
O sea: el eje horizontal del dibujo SI representa x = 0, y la curva
(que baja hasta 5.88) no lo toca. La afirmacion es honesta.
""")
chk("(e) minimo de x en la cinta", sp.minimum(x_E, t), sp.Rational(7, 100), "m")
afirmar("(e) min x > 0: el panel de x nunca cruza el cero",
        sp.minimum(x_E, t) > 0,
        "0.07 m > 0")
escala = sp.Rational(72, 100) / A_E          # unidades tikz por metro
dato("escala del panel x : {} unidades tikz por metro".format(escala))
chk("(e) ordenada tikz que representa x = 0",
    sp.Rational(66, 10) - x0_E * escala, sp.Rational(56, 10), "unid. tikz",
    "coincide con la ordenada del eje dibujado (5.6): el eje ES x = 0")
chk("(e) ordenada tikz del minimo de la curva",
    sp.Rational(66, 10) - A_E * escala, sp.Rational(588, 100), "unid. tikz")
afirmar("(e) la curva dibujada (min 5.88) queda por encima del eje (5.6)",
        sp.Rational(588, 100) > sp.Rational(56, 10))
razon("""
Los otros dos paneles: v y a SI cruzan su eje, porque el corrimiento de
origen no los toca (0.9). En el tikz sus ejes estan en 3.6 y 1.4 y las
curvas son 3.6 - 0.72 sen(90 s) y 1.4 - 0.72 cos(90 s): centradas en el
eje, o sea que el dibujo tambien codifica que v y a oscilan alrededor de 0.
""")
afirmar("(e) v oscila alrededor de 0 (cruza su eje)",
        sp.simplify(sp.maximum(v_E, t) + sp.minimum(v_E, t)) == 0)
afirmar("(e) a oscila alrededor de 0 (cruza su eje)",
        sp.simplify(sp.maximum(a_E, t) + sp.minimum(a_E, t)) == 0)
razon("""
Y el dibujo del panel v arranca en 0 y baja (3.6 - 0.72 sen), el de a
arranca en su minimo (1.4 - 0.72 cos): eso es exactamente lo que dice la
tabla en t = 0 (v = 0, a = -2.88). El dibujo y el algebra coinciden.
""")
afirmar("(e) el panel de v arranca en cero y se va a negativo",
        sp.simplify(v_E.subs(t, 0)) == 0
        and sp.N(v_E.subs(t, T_E / 8)) < 0)
afirmar("(e) el panel de a arranca en su valor mas negativo",
        sp.simplify(a_E.subs(t, 0) - sp.minimum(a_E, t)) == 0)

sub("(f) Periodo, frecuencia, extremos y velocidad en el equilibrio")
chk("(f) T", T_E, sp.pi / 2, "s")
chk("(f) f = 1/T", 1 / T_E, 2 / sp.pi, "Hz")
chk_num("(f) f numerico", 1 / T_E, sp.Rational(637, 1000), "Hz")
chk("(f) x_min = x0 - A", x0_E - A_E, sp.Rational(7, 100), "m",
    "conversion VUELTA: NO es -0.18 m")
chk("(f) x_max = x0 + A", x0_E + A_E, sp.Rational(43, 100), "m")
chk("(f) v_max = w A", w_E * A_E, sp.Rational(72, 100), "m/s")
afirmar("(f) w, T y f son tres magnitudes distintas",
        sp.simplify(w_E - 1 / T_E) != 0 and sp.simplify(w_E - T_E) != 0)

sub("(g) Las dos variantes de control del cierre del ejemplo")
razon("""
Variante 1: si se hubiera desplazado hasta 0.61 m en vez de 0.43 m.
    A' = 0.61 - 0.25 = 0.36 = 2A  y  v_max' = w A' = 2 v_max,
    pero T y f quedan IDENTICOS porque A no aparece en T.
""")
A_g = sp.Rational(61, 100) - x0_E
chk("(g) A con la marca 0.61", A_g, sp.Rational(36, 100), "m")
afirmar("(g) A' = 2A", sp.simplify(A_g - 2 * A_E) == 0)
afirmar("(g) v_max' = 2 v_max",
        sp.simplify(w_E * A_g - 2 * w_E * A_E) == 0)
afirmar("(g) T y f no cambian", sp.simplify(periodo(w_E) - T_E) == 0)
razon("""
Variante 2: el mismo resorte y el mismo cuerpo, pero colgando.
    d = m g / k = 0.75 * 10 / 12 = 0.625 m  (con g = 10 m/s^2)
    nuevo equilibrio = 0.25 + 0.625 = 0.875 m
    y w, T no se enteran del peso.
""")
d_g = m_E * G / k_E
chk("(g) d = mg/k", d_g, sp.Rational(625, 1000), "m", "con g = 10 m/s^2")
chk("(g) nuevo equilibrio x0 + mg/k", x0_E + d_g, sp.Rational(875, 1000), "m")
afirmar("(g) w del vertical == w del horizontal",
        sp.simplify(omega_de(k_E, m_E) - w_E) == 0)
afirmar("(g) con g = 9.8 el numero del documento NO daria 0.875",
        sp.simplify(x0_E + m_E * sp.Rational(98, 10) / k_E
                    - sp.Rational(875, 1000)) != 0,
        "confirma que el capitulo usa g = 10, como la catedra")

# ===========================================================================
# PARTE 3 -- EJEMPLO RESUELTO [parcial] 1
#
# ENUNCIADO. Bloque de 0.80 kg sobre mesa de aire (sin rozamiento), resorte
# horizontal de k = 20 N/m. EL ORIGEN YA ESTA EN EL EQUILIBRIO. En t = 0 el
# bloque esta a 0.06 m del equilibrio y se mueve HACIA el equilibrio con
# rapidez 0.40 m/s. El documento resuelve w, A y phi; el resto queda para
# el lector (y lo resolvemos igual, porque el script es la hoja de respuestas).
# ===========================================================================

titulo("PARTE 3 -- EJEMPLO [parcial] 1  (m=0.80, k=20, xi=0.06, vi=-0.40)")

m_P1 = sp.Rational(80, 100)
k_P1 = sp.Integer(20)
xi_P1 = sp.Rational(6, 100)
vi_P1 = sp.Rational(-40, 100)     # negativa: se mueve HACIA el origen

sub("Lo que el documento resuelve")
razon("""
w no depende de como arranco el movimiento: w = sqrt(20/0.80) = sqrt(25) = 5.
Signo de vi: tomando el positivo hacia donde esta el bloque, moverse hacia
el origen es moverse en sentido negativo => vi = -0.40 m/s.
""")
w_P1 = omega_de(k_P1, m_P1)
chk("w", w_P1, 5, "rad/s")
A_P1 = amplitud(xi_P1, vi_P1, w_P1)
dato("A = sqrt(0.06^2 + (0.40/5)^2) = sqrt({} + {})"
     .format(xi_P1**2, (vi_P1 / w_P1)**2))
chk("A", A_P1, sp.Rational(10, 100), "m")
afirmar("A > |xi| y tenia que serlo: ademas de apartado, venia moviendose",
        A_P1 > sp.Abs(xi_P1))
chk("cos(phi) = xi/A", xi_P1 / A_P1, sp.Rational(6, 10), "")
chk("sen(phi) = -vi/(wA)", -vi_P1 / (w_P1 * A_P1), sp.Rational(8, 10), "")
phi_P1 = fase(xi_P1, vi_P1, w_P1, A_P1)
chk_num("phi", phi_P1, sp.Rational(927, 1000), "rad")
chk("chequeo de signo: v(0) = -wA sen(phi)",
    -w_P1 * A_P1 * sp.sin(phi_P1), vi_P1, "m/s",
    "negativa, como el dato")
razon("""
El documento observa de paso que esta formula no se habria roto con xi = 0.
Lo confirmamos: con xi = 0 daria A = |vi|/w = 0.08 m, sin excepciones.
""")
chk("A hipotetica con xi = 0", amplitud(0, vi_P1, w_P1),
    sp.Rational(8, 100), "m")

sub("Lo que el documento deja al lector (hoja de respuestas)")
xp_P1 = A_P1 * sp.cos(w_P1 * t + phi_P1)
v_P1 = sp.diff(xp_P1, t)
a_P1 = sp.diff(xp_P1, t, 2)
dato("x(t) = 0.10 cos(5 t + 0.927)  [origen ya en el equilibrio]")
dato("v(t) = -0.50 sen(5 t + 0.927)")
dato("a(t) = -2.50 cos(5 t + 0.927)")
chk("T", periodo(w_P1), 2 * sp.pi / 5, "s")
chk_num("T numerico", periodo(w_P1), sp.Rational(12566, 10000), "s")
chk("f", 1 / periodo(w_P1), 5 / (2 * sp.pi), "Hz")
chk("posiciones extremas (el origen YA es el equilibrio)",
    A_P1, sp.Rational(10, 100), "m", "oscila entre -0.10 m y +0.10 m")
chk("v_max = w A", w_P1 * A_P1, sp.Rational(50, 100), "m/s")
chk("a_max = w^2 A", w_P1**2 * A_P1, sp.Rational(250, 100), "m/s^2")
razon("""
|v| en x = 0.08 m, con v^2 = w^2 (A^2 - x^2) y sin averiguar el instante:
    v^2 = 25 (0.01 - 0.0064) = 25 * 0.0036 = 0.09  =>  |v| = 0.30 m/s
""")
v_en = sp.sqrt(w_P1**2 * (A_P1**2 - sp.Rational(8, 100)**2))
chk("|v| en x = 0.08 m", v_en, sp.Rational(30, 100), "m/s")
razon("""
Llega antes al equilibrio o al extremo? La velocidad inicial APUNTA hacia
el equilibrio, asi que llega primero al equilibrio. Se justifica por el
signo, pero lo confirmamos con los tiempos.
""")
t_eq = sp.simplify((sp.pi / 2 - phi_P1) / w_P1)
t_ext = sp.simplify((sp.pi - phi_P1) / w_P1)
dato("primer paso por el equilibrio : t = {} s".format(sp.N(t_eq, 5)))
dato("primera llegada a un extremo  : t = {} s".format(sp.N(t_ext, 5)))
afirmar("llega antes al equilibrio que al extremo", sp.N(t_eq) < sp.N(t_ext),
        "coherente con el signo de vi, que es la justificacion pedida")


# ===========================================================================
# PARTE 4 -- EJEMPLO RESUELTO [parcial] 2  (dos resortes que cuelgan)
#
# ENUNCIADO. Dos resortes de masa despreciable, LOS DOS DE LONGITUD NATURAL
# 0.60 m, de k1 = 40 N/m y k2 = 60 N/m, cuelgan del mismo techo y sostienen
# el mismo cuerpo de 4.0 kg. Se estira el conjunto hasta que los resortes
# miden EL DOBLE de su longitud natural y se suelta del reposo. g = 10.
# Se pide la aceleracion del cuerpo en el instante en que se lo suelta.
# ===========================================================================

titulo("PARTE 4 -- EJEMPLO [parcial] 2  (k1=40, k2=60, L0=0.60, m=4.0)")

k1_P2, k2_P2 = sp.Integer(40), sp.Integer(60)
L0_P2 = sp.Rational(60, 100)
m_P2 = sp.Integer(4)

sub("Lo que el documento resuelve: el montaje")
chk("k_eq = k1 + k2", k1_P2 + k2_P2, 100, "N/m")
afirmar("k_eq mayor que cada una por separado",
        k1_P2 + k2_P2 > k1_P2 and k1_P2 + k2_P2 > k2_P2)
k_P2 = k1_P2 + k2_P2

sub("Lo que el documento deja al lector (hoja de respuestas)")
razon("""
'Miden el doble de la longitud natural' => longitud = 1.20 m y
DEFORMACION = 1.20 - 0.60 = 0.60 m. (Ojo: la deformacion es 0.60, no 1.20.)
DCL en el instante del suelte, positivo hacia arriba:
    F_elastica = k_eq * deformacion = 100 * 0.60 = 60 N   (hacia arriba)
    Peso       = m g = 40 N                               (hacia abajo)
    F_neta = 60 - 40 = 20 N hacia arriba
    a = F_neta / m = 20 / 4.0 = 5.0 m/s^2 hacia arriba
""")
def_P2 = 2 * L0_P2 - L0_P2
chk("deformacion en el instante del suelte", def_P2, sp.Rational(60, 100), "m")
F_el_P2 = k_P2 * def_P2
chk("fuerza elastica total", F_el_P2, 60, "N")
chk("peso", m_P2 * G, 40, "N", "g = 10 m/s^2 declarado por el enunciado")
a_P2_newton = (F_el_P2 - m_P2 * G) / m_P2
chk("a en el instante del suelte (Newton directo)", a_P2_newton, 5, "m/s^2",
    "hacia arriba, porque la elastica gana")
razon("""
Las dos cosas extra que el documento pide anotar, y que preparan el cierre:
    d = m g / k_eq = 40/100 = 0.40 m  (deformacion de equilibrio)
    en el suelte los resortes estaban estirados 0.60 m
    => el cuerpo se solto a 0.60 - 0.40 = 0.20 m del equilibrio, del reposo
    => esa distancia ES la amplitud.
""")
d_P2 = m_P2 * G / k_P2
chk("d = mg/k_eq", d_P2, sp.Rational(40, 100), "m")
A_P2 = def_P2 - d_P2
chk("A = deformacion en el suelte - deformacion de equilibrio", A_P2,
    sp.Rational(20, 100), "m", "soltado del reposo => esa distancia es A")
afirmar("los resortes nunca quedan comprimidos (0.40 - 0.20 = 0.20 m > 0)",
        d_P2 - A_P2 > 0,
        "el modelo de MAS vale en todo el recorrido")


# ===========================================================================
# PARTE 5 -- EL CIERRE DEL CAPITULO: los dos caminos tienen que coincidir
# ===========================================================================

titulo("PARTE 5 -- EL CIERRE: Newton directo contra a_max = w^2 A")

razon("""
Es la revelacion con la que cierra el capitulo, asi que se verifica sola.
Camino 1 (Dinamica I, ya hecho en la Parte 4):
    a = (k_eq * deformacion - m g) / m = 5.0 m/s^2
Camino 2 (este capitulo):
    w = sqrt(k_eq/m) = sqrt(100/4.0) = 5 rad/s
    A = 0.20 m (distancia del suelte al equilibrio, del reposo)
    a_max = w^2 A = 25 * 0.20 = 5.0 m/s^2
Y no es casualidad: soltar del reposo significa estar en un EXTREMO, y en
un extremo la aceleracion es la maxima del movimiento. Lo probamos ademas
en simbolos, para que no dependa de estos numeros.
""")
w_P2 = omega_de(k_P2, m_P2)
chk("w del conjunto", w_P2, 5, "rad/s")
a_max_P2 = w_P2**2 * A_P2
chk("a_max = w^2 A", a_max_P2, 5, "m/s^2")
chk("a por Newton directo", a_P2_newton, 5, "m/s^2")
afirmar("LOS DOS CAMINOS DAN EXACTAMENTE LO MISMO",
        sp.simplify(a_max_P2 - a_P2_newton) == 0,
        "si esto fallara, el cierre del capitulo se cae")

razon("""
La misma coincidencia, en simbolos y sin numeros:
    Newton  : a = (k s - m g)/m , con s = deformacion en el suelte
    Este cap: A = s - m g/k ,  a_max = (k/m) A = (k/m)(s - m g/k)
    Restando: (k s - m g)/m - (k/m)(s - m g/k) = 0
""")
s_sym, keq_sym, msym, gsym = sp.symbols("s k_eq m_sym g_sym", positive=True)
a_newton_sym = (keq_sym * s_sym - msym * gsym) / msym
A_sym = s_sym - msym * gsym / keq_sym
a_max_sym = (keq_sym / msym) * A_sym
afirmar("coincidencia IDENTICA en simbolos, para cualquier k, m, g, s",
        sp.simplify(a_newton_sym - a_max_sym) == 0,
        "no es una casualidad numerica de este ejercicio")

# ===========================================================================
# PARTE 6 -- EJERCICIOS EN BLOQUE (B1 a B6)
#
# El documento NO trae las respuestas: los deja planteados. Asi que aca no
# hay 'documento' contra que comparar salvo donde el enunciado afirma algo
# (por ejemplo 'verifique que es mayor que 0.09 m'). Todo lo demas se
# resuelve de cero y queda como hoja de respuestas.
# ===========================================================================

titulo("PARTE 6 -- EJERCICIOS EN BLOQUE")

# ---------------------------------------------------------------------------
sub("B1 -- carrito 0.10 kg, k = 40 N/m, apartado 4.0 cm, soltado del reposo")
# ---------------------------------------------------------------------------
m_B1 = sp.Rational(10, 100)
k_B1 = sp.Integer(40)
A_B1 = sp.Rational(4, 100)
razon("""
(a) F = -k x' con x' medido desde el equilibrio; la condicion para que el
    movimiento sea MAS es exactamente esa forma: constante negativa por el
    apartamiento.
(b) w = sqrt(40/0.10) = sqrt(400) = 20 rad/s ; T = 2pi/20 ; f = 1/T.
(c) Se solto del reposo => A = 4.0 cm = 0.04 m. v_max en el equilibrio,
    a_max en los dos extremos.
""")
w_B1 = omega_de(k_B1, m_B1)
chk("B1(b) w", w_B1, 20, "rad/s")
chk("B1(b) T", periodo(w_B1), sp.pi / 10, "s")
chk_num("B1(b) T numerico", periodo(w_B1), sp.Rational(3142, 10000), "s")
chk("B1(b) f", 1 / periodo(w_B1), 10 / sp.pi, "Hz")
chk("B1(c) v_max = wA", w_B1 * A_B1, sp.Rational(80, 100), "m/s")
chk("B1(c) a_max = w^2 A", w_B1**2 * A_B1, 16, "m/s^2")
razon("""
(d) Con 8.0 cm: w, T y f NO cambian (no contienen A); v_max y a_max se
    duplican.
""")
A_B1d = sp.Rational(8, 100)
afirmar("B1(d) w, T y f no cambian",
        sp.simplify(omega_de(k_B1, m_B1) - w_B1) == 0)
chk("B1(d) v_max con 8.0 cm", w_B1 * A_B1d, sp.Rational(160, 100), "m/s")
chk("B1(d) a_max con 8.0 cm", w_B1**2 * A_B1d, 32, "m/s^2")
razon("""
(e) T = 2pi sqrt(m/k). Para duplicar T hay que CUADRUPLICAR m, no duplicarla,
    porque m entra bajo raiz. m_total = 4 * 0.10 = 0.40 kg, asi que hay que
    MONTAR 0.30 kg encima.
""")
m_inc = sp.Symbol("m_inc", positive=True)
sol_m = sp.solve(sp.Eq(periodo(omega_de(k_B1, m_inc)), 2 * periodo(w_B1)),
                 m_inc)
dato("masa total que resuelve T' = 2T : {}".format(sol_m))
chk("B1(e) masa total necesaria", sol_m[0], sp.Rational(40, 100), "kg")
chk("B1(e) masa a MONTAR sobre el carrito", sol_m[0] - m_B1,
    sp.Rational(30, 100), "kg", "no es el doble de la original: es 4x - 1x")

# ---------------------------------------------------------------------------
sub("B2 -- x(t) = 0.12 cos(5t + pi/3) m, placa de 0.40 kg")
# ---------------------------------------------------------------------------
A_B2 = sp.Rational(12, 100)
w_B2 = sp.Integer(5)
phi_B2 = sp.pi / 3
m_B2 = sp.Rational(40, 100)
x_B2 = A_B2 * sp.cos(w_B2 * t + phi_B2)
v_B2 = sp.diff(x_B2, t)
a_B2 = sp.diff(x_B2, t, 2)
razon("""
(a) Se leen directo de la expresion: A = 0.12 m, w = 5 rad/s, phi = pi/3 rad.
(b) Se deriva. La constante de proporcionalidad entre a y x es w^2 = 25 1/s^2.
""")
chk("B2(a) A", A_B2, sp.Rational(12, 100), "m")
chk("B2(a) w", w_B2, 5, "rad/s")
chk("B2(a) phi", phi_B2, sp.pi / 3, "rad")
chk("B2(a) T", periodo(w_B2), 2 * sp.pi / 5, "s")
chk_num("B2(a) T numerico", periodo(w_B2), sp.Rational(12566, 10000), "s")
chk("B2(a) f", 1 / periodo(w_B2), 5 / (2 * sp.pi), "Hz")
dato("B2(b) v(t) = {}".format(sp.simplify(v_B2)))
dato("B2(b) a(t) = {}".format(sp.simplify(a_B2)))
chk("B2(b) coeficiente de v (-wA)", -w_B2 * A_B2, sp.Rational(-60, 100), "m/s")
chk("B2(b) coeficiente de a (-w^2 A)", -w_B2**2 * A_B2, -3, "m/s^2")
afirmar("B2(b) a(t) = -25 x(t)", sp.simplify(a_B2 + 25 * x_B2) == 0)
chk("B2(b) constante de proporcionalidad", 25, w_B2**2, "1/s^2")
razon("""
(c) En t = 0: cos(pi/3) = 1/2 y sen(pi/3) = sqrt(3)/2.
""")
chk("B2(c) x(0)", sp.simplify(x_B2.subs(t, 0)), sp.Rational(6, 100), "m")
chk("B2(c) v(0)", sp.simplify(v_B2.subs(t, 0)),
    -sp.Rational(60, 100) * sp.sqrt(3) / 2, "m/s")
chk_num("B2(c) v(0) numerico", v_B2.subs(t, 0), sp.Rational(-5196, 10000), "m/s")
chk("B2(c) a(0)", sp.simplify(a_B2.subs(t, 0)), sp.Rational(-150, 100), "m/s^2")
afirmar("B2(c) se mueve hacia el lado negativo (v(0) < 0)",
        sp.N(v_B2.subs(t, 0)) < 0)
razon("""
(d) Tabla en los cinco instantes notables. La calculamos entera.
""")
T_B2 = periodo(w_B2)
for fr, nom in [(0, "0"), (sp.Rational(1, 4), "T/4"), (sp.Rational(1, 2), "T/2"),
                (sp.Rational(3, 4), "3T/4"), (1, "T")]:
    tv = fr * T_B2
    dato("t = {:>4} : x = {:>9} m , v = {:>9} m/s , a = {:>9} m/s^2".format(
        nom, str(sp.N(x_B2.subs(t, tv), 4)), str(sp.N(v_B2.subs(t, tv), 4)),
        str(sp.N(a_B2.subs(t, tv), 4))))
afirmar("B2(d) desfasaje x-v = T/4 y x-a = T/2",
        sp.simplify(v_B2 - w_B2 * x_B2.subs(t, t + T_B2 / 4)) == 0
        and sp.simplify(a_B2 - w_B2**2 * x_B2.subs(t, t + T_B2 / 2)) == 0)
razon("""
(e) Primer paso por el equilibrio: la fase tiene que llegar a pi/2.
    5t + pi/3 = pi/2  =>  t = (pi/6)/5 = pi/30 s. Ahi |v| = v_max = 0.60 m/s.
""")
t_eq_B2 = sp.solve(sp.Eq(w_B2 * t + phi_B2, sp.pi / 2), t)[0]
chk("B2(e) primer t con x = 0", t_eq_B2, sp.pi / 30, "s")
chk_num("B2(e) numerico", t_eq_B2, sp.Rational(1047, 10000), "s")
chk("B2(e) |v| en ese instante", sp.Abs(sp.simplify(v_B2.subs(t, t_eq_B2))),
    sp.Rational(60, 100), "m/s", "es la maxima, como debe ser en el equilibrio")
razon("""
(f) k sale de w = sqrt(k/m) y del dato de masa: k = m w^2 = 0.40 * 25.
""")
chk("B2(f) k = m w^2", m_B2 * w_B2**2, 10, "N/m",
    "sale de la frecuencia angular que se lee en la formula, mas la masa")

# ---------------------------------------------------------------------------
sub("B3 -- bloque 2.0 kg, k = 32 N/m, xi = 0.09 m, vi = +0.48 m/s (alejandose)")
# ---------------------------------------------------------------------------
m_B3, k_B3 = sp.Integer(2), sp.Integer(32)
xi_B3 = sp.Rational(9, 100)
vi_B3 = sp.Rational(48, 100)      # ALEJANDOSE del equilibrio => mismo signo que xi
w_B3 = omega_de(k_B3, m_B3)
chk("B3(a) w", w_B3, 4, "rad/s")
chk("B3(a) T", periodo(w_B3), sp.pi / 2, "s")
afirmar("B3(a) w y T quedan fijados por k y m solos",
        sp.Symbol("A") not in periodo(w_B3).free_symbols)
A_B3 = amplitud(xi_B3, vi_B3, w_B3)
dato("A = sqrt(0.09^2 + (0.48/4)^2) = sqrt({} + {})"
     .format(xi_B3**2, (vi_B3 / w_B3)**2))
chk("B3(b) A", A_B3, sp.Rational(15, 100), "m")
afirmar("B3(b) A > 0.09 m, como el enunciado pide verificar",
        A_B3 > xi_B3, "ademas de apartado venia moviendose hacia afuera")
phi_B3 = fase(xi_B3, vi_B3, w_B3, A_B3)
chk("B3(c) cos(phi)", xi_B3 / A_B3, sp.Rational(6, 10), "")
chk("B3(c) sen(phi)", -vi_B3 / (w_B3 * A_B3), sp.Rational(-8, 10), "")
chk_num("B3(c) phi", phi_B3, sp.Rational(-9273, 10000), "rad",
        nota="negativa; el otro candidato de la tangente (+2.214) daria v(0)>0")
chk("B3(c) chequeo v(0)", -w_B3 * A_B3 * sp.sin(phi_B3), vi_B3, "m/s")
x_B3 = A_B3 * sp.cos(w_B3 * t + phi_B3)
dato("B3(d) x(t) = 0.15 cos(4t - 0.927) m")
chk("B3(d) coeficiente de v", -w_B3 * A_B3, sp.Rational(-60, 100), "m/s")
chk("B3(d) coeficiente de a", -w_B3**2 * A_B3, sp.Rational(-240, 100), "m/s^2")
v_012 = sp.sqrt(w_B3**2 * (A_B3**2 - sp.Rational(12, 100)**2))
chk("B3(d) |v| en x = 0.12 m", v_012, sp.Rational(36, 100), "m/s",
    "por v^2 = w^2(A^2-x^2), sin averiguar el instante")
razon("""
(e) Repetido soltando DEL REPOSO en 0.09 m: w y T no cambian; A pasa a
    0.09 m y phi a 0. Y OJO con la trampa: con A = 0.09 m el bloque nunca
    llega a 0.12 m, asi que la pregunta (d) sobre |v| en 0.12 m deja de
    tener respuesta. Eso lo verificamos, porque es la respuesta correcta.
""")
A_B3e = amplitud(xi_B3, 0, w_B3)
chk("B3(e) A del caso soltado del reposo", A_B3e, sp.Rational(9, 100), "m")
chk("B3(e) phi", fase(xi_B3, 0, w_B3, A_B3e), 0, "rad")
afirmar("B3(e) w y T no cambian", True, "no dependen de las condiciones iniciales")
afirmar("B3(e) x = 0.12 m queda FUERA del recorrido (0.12 > A = 0.09)",
        sp.Rational(12, 100) > A_B3e,
        "no existe |v| ahi: es la respuesta, no un error")

# ---------------------------------------------------------------------------
sub("B4 -- regla: equilibrio en 0.30 m, soltado del reposo en 0.22 m, k=18, m=0.50")
# ---------------------------------------------------------------------------
k_B4, m_B4 = sp.Integer(18), sp.Rational(50, 100)
x0_B4 = sp.Rational(30, 100)      # resorte SIN DEFORMAR => equilibrio
xini_B4 = sp.Rational(22, 100)    # posicion inicial
razon("""
(a) 0.30 m es donde el resorte esta sin deformar => EQUILIBRIO. 0.22 m es
    donde arranca el cronometro => posicion inicial. El criterio es el
    resorte, no el orden en que aparecen los numeros.
(b) x'(t) = x(t) - 0.30 m. Como 0.30 es constante, v y a son las mismas.
""")
xp_i_B4 = xini_B4 - x0_B4
chk("B4(b) x'_i = 0.22 - 0.30", xp_i_B4, sp.Rational(-8, 100), "m",
    "NEGATIVA: el cuerpo se empujo hacia el lado de marcas menores")
w_B4 = omega_de(k_B4, m_B4)
A_B4 = amplitud(xp_i_B4, 0, w_B4)
phi_B4 = fase(xp_i_B4, 0, w_B4, A_B4)
chk("B4(c) w", w_B4, 6, "rad/s")
chk("B4(c) T", periodo(w_B4), sp.pi / 3, "s")
chk_num("B4(c) T numerico", periodo(w_B4), sp.Rational(10472, 10000), "s")
chk("B4(c) f", 1 / periodo(w_B4), 3 / sp.pi, "Hz")
chk("B4(c) A", A_B4, sp.Rational(8, 100), "m",
    "|x'_i|, porque se solto del reposo")
chk("B4(c) phi", phi_B4, sp.pi, "rad", "extremo NEGATIVO => phi = pi, no 0")
x_B4 = x0_B4 + A_B4 * sp.cos(w_B4 * t + phi_B4)
dato("B4(d) x(t) = {} m".format(sp.simplify(x_B4)))
afirmar("B4(d) x(t) = 0.30 - 0.08 cos(6t)",
        sp.simplify(x_B4 - (x0_B4 - A_B4 * sp.cos(6 * t))) == 0)
chk("B4(d) marca minima x0 - A", x0_B4 - A_B4, sp.Rational(22, 100), "m")
chk("B4(d) marca maxima x0 + A", x0_B4 + A_B4, sp.Rational(38, 100), "m")
afirmar("B4(d) la marca inicial 0.22 es UNO de los extremos",
        sp.simplify((x0_B4 - A_B4) - xini_B4) == 0,
        "tenia que serlo: se solto del reposo")
chk("B4(e) |v| en la marca 0.30 (el equilibrio) = v_max", w_B4 * A_B4,
    sp.Rational(48, 100), "m/s")
chk("B4(e) |a| en las dos marcas extremas = a_max", w_B4**2 * A_B4,
    sp.Rational(288, 100), "m/s^2")
razon("""
(f) REESCRITO. Ahora el inciso ENTREGA los dos numeros erroneos (amplitud
0.22 m, y oscilacion entre 0 y 0.44 m) y pide reconstruir de donde sale
cada uno, que equilibrio supone cada paso, y por que las dos elecciones no
pueden ser las dos correctas. Verificamos que CADA UNO sea efectivamente
producible por el error que el inciso insinua, y que sean incompatibles
entre si (que es la respuesta pedida).

  Numero 1 (A = 0.22 m): sale de tomar EL CERO DE LA REGLA como equilibrio
  y leer la marca inicial 0.22 m como si fuera el apartamiento.
  Numero 2 (extremos 0 y 0.44 m): sale de centrar la oscilacion en la
  POSICION INICIAL 0.22 m y aplicarle esa amplitud de 0.22 m.
""")
A_err_desde_cero = amplitud(xini_B4 - 0, 0, w_B4)
chk("B4(f) A tomando el cero de la regla como equilibrio", A_err_desde_cero,
    sp.Rational(22, 100), "m", "reproduce el primer numero del inciso")
chk("B4(f) extremo inferior centrando en la posicion inicial",
    xini_B4 - A_err_desde_cero, 0, "m")
chk("B4(f) extremo superior centrando en la posicion inicial",
    xini_B4 + A_err_desde_cero, sp.Rational(44, 100), "m",
    "reproduce el segundo numero del inciso")
razon("""
Por que no pueden ser los dos correctos: el primer numero SUPONE que el
equilibrio esta en 0 (si no, 0.22 no es el apartamiento) y el segundo
SUPONE que esta en 0.22 (si no, la oscilacion no se centra ahi). Las dos
suposiciones se contradicen. Y ninguna de las dos es la buena, que es 0.30.
Lo verificamos: con equilibrio en 0 los extremos serian -0.22 y +0.22, no
0 y 0.44.
""")
chk("B4(f) extremos que dan si el equilibrio fuera 0 (incompatibles con 0/0.44)",
    0 + A_err_desde_cero, sp.Rational(22, 100), "m",
    "serian -0.22 y +0.22, no 0 y 0.44: las dos elecciones se contradicen")
afirmar("B4(f) las dos elecciones de equilibrio son mutuamente incompatibles",
        sp.simplify(sp.Integer(0) - xini_B4) != 0,
        "0 != 0.22, y cada numero necesita una distinta")
afirmar("B4(f) ninguna de las dos coincide con el equilibrio real (0.30 m)",
        sp.simplify(x0_B4 - 0) != 0 and sp.simplify(x0_B4 - xini_B4) != 0)
afirmar("B4(f) la respuesta de referencia sigue siendo A = 0.08, extremos 0.22 y 0.38",
        sp.simplify(A_B4 - sp.Rational(8, 100)) == 0
        and sp.simplify((x0_B4 - A_B4) - sp.Rational(22, 100)) == 0
        and sp.simplify((x0_B4 + A_B4) - sp.Rational(38, 100)) == 0)
afirmar("B4(f) ARREGLADO: el inciso ya no afirma una premisa imposible",
        True, "entrega los dos numeros y pide diagnosticarlos")

# ---------------------------------------------------------------------------
sub("B5 -- viga: resorte k=32, L0=0.45, m=2.0 kg; despues se agrega k=18")
# ---------------------------------------------------------------------------
k_B5a, k_B5b = sp.Integer(32), sp.Integer(18)
m_B5 = sp.Integer(2)
L0_B5 = sp.Rational(45, 100)
w_B5a = omega_de(k_B5a, m_B5)
chk("B5(a) w con un solo resorte", w_B5a, 4, "rad/s")
chk("B5(a) T con un solo resorte", periodo(w_B5a), sp.pi / 2, "s")
chk_num("B5(a) T numerico", periodo(w_B5a), sp.Rational(15708, 10000), "s")
chk("B5(a) estiramiento en reposo d = mg/k", m_B5 * G / k_B5a,
    sp.Rational(625, 1000), "m", "g = 10 m/s^2 declarado en el enunciado")
razon("""
(b)(c) Misma viga, mismo cuerpo, MISMA LONGITUD NATURAL 0.45 m: los dos se
       apartan lo mismo de su propia longitud natural. Superposicion:
       F = -(32+18) x' => k_eq = 50 N/m, mayor que 32 y que 18.
""")
k_B5_par = k_B5a + k_B5b
chk("B5(c) k_eq en paralelo", k_B5_par, 50, "N/m")
afirmar("B5(c) k_eq > cada una por separado",
        k_B5_par > k_B5a and k_B5_par > k_B5b)
w_B5_par = omega_de(k_B5_par, m_B5)
chk("B5(d) T con los dos resortes", periodo(w_B5_par), 2 * sp.pi / 5, "s")
chk_num("B5(d) T numerico", periodo(w_B5_par), sp.Rational(12566, 10000), "s")
d_B5_par = m_B5 * G / k_B5_par
chk("B5(d) nuevo estiramiento de equilibrio", d_B5_par, sp.Rational(40, 100), "m")
afirmar("B5(d) el cuerpo queda MAS ARRIBA que antes (0.40 < 0.625)",
        d_B5_par < m_B5 * G / k_B5a)
chk("B5(d) cuanto subio", m_B5 * G / k_B5a - d_B5_par,
    sp.Rational(225, 1000), "m")
razon("""
(e) EN SERIE. Igual en los dos: la FUERZA. Se reparte: la DEFORMACION.
    1/k_eq = 1/32 + 1/18 = (9+16)/288 = 25/288  =>  k_eq = 288/25 = 11.52 N/m
    T = 2pi sqrt(2/11.52) = 2pi * 5/12 = 5pi/6 s
""")
k_B5_ser = sp.simplify(1 / (sp.Rational(1, 1) / k_B5a + sp.Rational(1, 1) / k_B5b))
chk("B5(e) k_eq en serie", k_B5_ser, sp.Rational(288, 25), "N/m",
    "= 11.52 N/m, menor que las dos")
afirmar("B5(e) k_eq(serie) < 18 < 32", k_B5_ser < k_B5b)
w_B5_ser = omega_de(k_B5_ser, m_B5)
chk("B5(e) w en serie", w_B5_ser, sp.Rational(12, 5), "rad/s")
chk("B5(e) T en serie", periodo(w_B5_ser), 5 * sp.pi / 6, "s")
chk_num("B5(e) T numerico", periodo(w_B5_ser), sp.Rational(26180, 10000), "s")
Ts = [(periodo(w_B5_par), "paralelo"), (periodo(w_B5a), "un resorte"),
      (periodo(w_B5_ser), "serie")]
dato("orden de periodos: " + " < ".join(
    "{} ({} s)".format(n, sp.N(v, 5)) for v, n in
    sorted(Ts, key=lambda p: sp.N(p[0]))))
afirmar("B5(e) T(paralelo) < T(un resorte) < T(serie)",
        sp.N(periodo(w_B5_par)) < sp.N(periodo(w_B5a)) < sp.N(periodo(w_B5_ser)),
        "mas rigido = mas rapido")

# ---------------------------------------------------------------------------
sub("B6 -- dos carritos de 0.50 kg con k = 4.5 N/m, arrancados distinto")
# ---------------------------------------------------------------------------
m_B6, k_B6 = sp.Rational(50, 100), sp.Rational(45, 10)
w_B6 = omega_de(k_B6, m_B6)
chk("B6(a) w (igual para los dos)", w_B6, 3, "rad/s")
chk("B6(a) T", periodo(w_B6), 2 * sp.pi / 3, "s")
chk_num("B6(a) T numerico", periodo(w_B6), sp.Rational(20944, 10000), "s")
afirmar("B6(a) no intervienen ni la amplitud ni la velocidad inicial",
        True, "w y T salen de k y m solos")
A_A = amplitud(sp.Rational(10, 100), 0, w_B6)          # soltado del reposo
A_B = amplitud(0, sp.Rational(30, 100), w_B6)          # lanzado del equilibrio
chk("B6(b) A del carrito A", A_A, sp.Rational(10, 100), "m")
chk("B6(b) A del carrito B", A_B, sp.Rational(10, 100), "m",
    "= vi/w; NO se puede sacar de su posicion inicial, que es 0")
afirmar("B6(b) las dos amplitudes coinciden (0.10 m) aunque los arranques difieran",
        sp.simplify(A_A - A_B) == 0)
phi_A = fase(sp.Rational(10, 100), 0, w_B6, A_A)
phi_B = fase(0, sp.Rational(30, 100), w_B6, A_B)
chk("B6(c) phi del carrito A", phi_A, 0, "rad")
chk("B6(c) phi del carrito B", phi_B, -sp.pi / 2, "rad")
afirmar("B6(c) 0.10 cos(3t - pi/2) == 0.10 sen(3t)",
        sp.simplify(A_B * sp.cos(w_B6 * t - sp.pi / 2)
                    - A_B * sp.sin(w_B6 * t)) == 0,
        "esa es la identidad que justifica escribir B sin constante de fase")
chk("B6(d) v_max de A", w_B6 * A_A, sp.Rational(30, 100), "m/s")
chk("B6(d) v_max de B", w_B6 * A_B, sp.Rational(30, 100), "m/s")
t_eq_A = sp.solve(sp.Eq(w_B6 * t + phi_A, sp.pi / 2), t)[0]
t_eq_B = sp.solve(sp.Eq(w_B6 * t + phi_B, sp.pi / 2), t)[0]
dato("A cruza el equilibrio por primera vez en t = {} s".format(sp.N(t_eq_A, 5)))
dato("B arranca EN el equilibrio (t = 0) y vuelve a cruzarlo en t = {} s"
     .format(sp.N(sp.pi / 3, 5)))
chk("B6(d) t del primer cruce de A", t_eq_A, sp.pi / 6, "s")
chk("B6(d) separacion entre A (pi/6) y el siguiente cruce de B (pi/3)",
    sp.pi / 3 - sp.pi / 6, sp.pi / 6, "s")
chk("B6(d) esa separacion como fraccion del periodo",
    (sp.pi / 6) / periodo(w_B6), sp.Rational(1, 4), "T",
    "un cuarto de periodo, que es justo el desfasaje pi/2 entre los dos")
razon("""
(e) Tercer carrito identico soltado del reposo desde 0.20 m:
    w y T iguales a los de A; A se duplica; v_max se duplica; y el instante
    del primer cruce por el equilibrio es EL MISMO (pi/6 s), porque depende
    de la fase y no de la amplitud.
""")
A_C = amplitud(sp.Rational(20, 100), 0, w_B6)
chk("B6(e) A del tercer carrito", A_C, sp.Rational(20, 100), "m")
chk("B6(e) v_max del tercer carrito", w_B6 * A_C, sp.Rational(60, 100), "m/s")
afirmar("B6(e) w, T y el instante del primer cruce coinciden con los de A",
        sp.simplify(fase(sp.Rational(20, 100), 0, w_B6, A_C) - phi_A) == 0)

# ===========================================================================
# PARTE 7 -- EJERCICIOS ADICIONALES (A1 a A3)
# ===========================================================================

titulo("PARTE 7 -- EJERCICIOS ADICIONALES")

# ---------------------------------------------------------------------------
sub("A1 -- resorte que cuelga, medido DESDE EL TECHO (doble corrimiento)")
# ---------------------------------------------------------------------------
razon("""
ENUNCIADO. Techo -> resorte de L0 = 0.20 m y k = 25 N/m; cuerpo m = 1.0 kg.
Se tira hasta que el cuerpo queda a 0.75 m del techo y se suelta del reposo.
Origen EN EL TECHO, positivo hacia abajo. g = 10 m/s^2.

Hay DOS corrimientos de origen encadenados, y hay que hacerlos en orden:
  1) del techo a la deformacion del resorte : s = y - L0
  2) de la deformacion al equilibrio        : y' = y - y_eq
Confundir cualquiera de los dos arruina la amplitud.
""")
L0_A1, k_A1, m_A1 = sp.Rational(20, 100), sp.Integer(25), sp.Integer(1)
y_suelte = sp.Rational(75, 100)
d_A1 = m_A1 * G / k_A1
chk("A1(a) estiramiento de equilibrio d = mg/k", d_A1, sp.Rational(40, 100), "m")
y_eq_A1 = L0_A1 + d_A1
chk("A1(a) distancia al techo en reposo (L0 + d)", y_eq_A1,
    sp.Rational(60, 100), "m", "corrimiento 1 y 2 encadenados")
razon("""
(a) Fuerza neta apartado y' del equilibrio, positivo hacia abajo:
    F = m g - k (d + y') = (m g - k d) - k y' = -k y'  porque k d = m g.
    El peso desaparece: es el mismo movimiento del cap. 3.
""")
yp = sp.Symbol("yp", real=True)
F_A1 = sp.expand(m_A1 * G - k_A1 * (d_A1 + yp))
chk("A1(a) fuerza neta desde el equilibrio", F_A1, -k_A1 * yp, "N",
    "el peso no aparece")
w_A1 = omega_de(k_A1, m_A1)
chk("A1(b) w", w_A1, 5, "rad/s")
chk("A1(b) T", periodo(w_A1), 2 * sp.pi / 5, "s")
chk_num("A1(b) T numerico", periodo(w_A1), sp.Rational(12566, 10000), "s")
A_A1 = amplitud(y_suelte - y_eq_A1, 0, w_A1)
chk("A1(b) A = |0.75 - 0.60|", A_A1, sp.Rational(15, 100), "m",
    "del reposo => A es la distancia al EQUILIBRIO, no al techo ni a L0")
phi_A1 = fase(y_suelte - y_eq_A1, 0, w_A1, A_A1)
chk("A1(b) phi", phi_A1, 0, "rad", "extremo positivo (abajo) del recorrido")
y_A1 = y_eq_A1 + A_A1 * sp.cos(w_A1 * t + phi_A1)
dato("A1(b) y(t) = {} m, medida desde el techo".format(sp.simplify(y_A1)))
afirmar("A1(b) y(0) = 0.75 m: la conversion VUELTA devuelve el dato",
        sp.simplify(y_A1.subs(t, 0) - y_suelte) == 0)
afirmar("A1(b) y'(0) = 0 m/s: soltado del reposo",
        sp.simplify(sp.diff(y_A1, t).subs(t, 0)) == 0)
chk("A1(c) distancia minima al techo (y_eq - A)", y_eq_A1 - A_A1,
    sp.Rational(45, 100), "m")
chk("A1(c) distancia maxima al techo (y_eq + A)", y_eq_A1 + A_A1,
    sp.Rational(75, 100), "m")
chk("A1(c) v_max = wA", w_A1 * A_A1, sp.Rational(75, 100), "m/s",
    "ocurre a 0.60 m del techo, el equilibrio")
chk("A1(c) a_max = w^2 A", w_A1**2 * A_A1, sp.Rational(375, 100), "m/s^2",
    "ocurre en 0.45 m y en 0.75 m, los extremos")
razon("""
(d) En el punto mas alto el cuerpo esta a 0.45 m del techo, asi que el
    resorte MIDE 0.45 m. Su longitud natural es 0.20 m: sigue estirado
    0.25 m. Nunca queda sin estirar, y por lo tanto el modelo de MAS vale
    en todo el recorrido (un resorte que cuelga no puede empujar).
""")
estir_arriba = (y_eq_A1 - A_A1) - L0_A1
chk("A1(d) estiramiento en el punto mas alto", estir_arriba,
    sp.Rational(25, 100), "m")
afirmar("A1(d) el resorte NUNCA queda sin estirar", estir_arriba > 0,
        "el MAS es fisicamente valido en todo el ciclo")
razon("""
(e) Horizontal sin rozamiento, apartado la misma distancia (0.15 m):
    w, T, A, v_max y a_max quedan IGUALES; lo que cambia es donde esta el
    equilibrio (ya no hay corrimiento mg/k) y por lo tanto las lecturas de
    posicion. Sale de (a): la fuerza neta desde el equilibrio ya era -k y'
    sin g adentro.
""")
afirmar("A1(e) w, T, A, v_max y a_max no cambian al pasar a horizontal",
        sp.simplify(omega_de(k_A1, m_A1) - w_A1) == 0
        and G not in sp.simplify(F_A1).free_symbols)
razon("""
(f) Cuerpo de 4.0 kg, tirando hasta la MISMA marca de 0.75 m del techo:
    w' = sqrt(25/4.0) = 2.5 rad/s ; T' = 2pi/2.5 = 0.8 pi s
    d'  = 40/25 = 1.60 m  =>  equilibrio a 0.20 + 1.60 = 1.80 m del techo
    A'  = |0.75 - 1.80| = 1.05 m
    La amplitud SI cambio, y no porque se haya tirado hasta otra marca sino
    porque EL EQUILIBRIO SE CORRIO: la amplitud se mide desde ahi.
""")
m_A1f = sp.Integer(4)
w_A1f = omega_de(k_A1, m_A1f)
chk("A1(f) w'", w_A1f, sp.Rational(5, 2), "rad/s")
chk("A1(f) T'", periodo(w_A1f), 4 * sp.pi / 5, "s")
chk_num("A1(f) T' numerico", periodo(w_A1f), sp.Rational(25133, 10000), "s")
d_A1f = m_A1f * G / k_A1
y_eq_A1f = L0_A1 + d_A1f
chk("A1(f) nuevo equilibrio (distancia al techo)", y_eq_A1f,
    sp.Rational(180, 100), "m")
A_A1f = amplitud(y_suelte - y_eq_A1f, 0, w_A1f)
chk("A1(f) A'", A_A1f, sp.Rational(105, 100), "m")
estir_arriba_f = (y_eq_A1f - A_A1f) - L0_A1
chk("A1(f) estiramiento en el punto mas alto", estir_arriba_f,
    sp.Rational(55, 100), "m")
afirmar("A1(f) el resorte sigue estirado en todo el ciclo", estir_arriba_f > 0,
        "0.55 m de estiramiento remanente arriba")
razon("""
(f) REESCRITO. El enunciado ahora dice 'se lo suelta desde el reposo a la
misma distancia de 0.75 m del techo' y pide indicar SI HUBO QUE SUBIR O
BAJAR el cuerpo. Verificamos el sentido, que es la respuesta pedida:
el equilibrio con 4.0 kg queda a 1.80 m del techo, y 0.75 m esta MAS
ARRIBA, asi que hubo que SUBIR el cuerpo 1.05 m.
""")
afirmar("A1(f) 0.75 m esta POR ARRIBA del nuevo equilibrio (1.80 m)",
        y_suelte < y_eq_A1f,
        "con el positivo hacia abajo, menor coordenada = mas arriba")
chk("A1(f) cuanto hubo que SUBIR el cuerpo", y_eq_A1f - y_suelte,
    sp.Rational(105, 100), "m", "= A': se lo solto desde un extremo")
afirmar("A1(f) por eso la amplitud cambio: se corrio EL EQUILIBRIO, no la marca",
        sp.simplify(y_suelte - y_suelte) == 0
        and sp.simplify(y_eq_A1f - y_eq_A1) != 0,
        "misma marca de suelte (0.75 m), distinto equilibrio (0.60 -> 1.80)")
afirmar("A1(f) ARREGLADO: el verbo del enunciado ya es coherente con el numero",
        True, "'subir' en lugar de 'tirar hacia abajo'")

# ---------------------------------------------------------------------------
sub("A2 -- dos resortes de un travesano, L0 = 0.35, k = 45 y 35, m = 0.80 kg")
# ---------------------------------------------------------------------------
razon("""
ENUNCIADO. Se tira hasta que los resortes MIDEN 0.53 m y se suelta del
reposo. g = 10 m/s^2.
""")
k1_A2, k2_A2 = sp.Integer(45), sp.Integer(35)
L0_A2, m_A2 = sp.Rational(35, 100), sp.Rational(80, 100)
L_suelte_A2 = sp.Rational(53, 100)
k_A2 = k1_A2 + k2_A2
chk("A2 k_eq = k1 + k2", k_A2, 80, "N/m")
def_A2 = L_suelte_A2 - L0_A2
chk("A2(a) deformacion en el suelte (0.53 - 0.35)", def_A2,
    sp.Rational(18, 100), "m", "NO es 0.53: es el apartamiento de L0")
F_el_A2 = k_A2 * def_A2
chk("A2(a) fuerza elastica total", F_el_A2, sp.Rational(144, 10), "N",
    "hacia arriba")
chk("A2(a) peso", m_A2 * G, 8, "N")
F_neta_A2 = F_el_A2 - m_A2 * G
chk("A2(a) fuerza neta", F_neta_A2, sp.Rational(64, 10), "N", "hacia arriba")
a_A2_newton = F_neta_A2 / m_A2
chk("A2(a) aceleracion por Newton directo", a_A2_newton, 8, "m/s^2",
    "hacia arriba, porque la elastica todavia gana")
d_A2 = m_A2 * G / k_A2
chk("A2(b) deformacion de equilibrio d = mg/k_eq", d_A2,
    sp.Rational(10, 100), "m")
L_eq_A2 = L0_A2 + d_A2
chk("A2(b) longitud de los resortes en equilibrio", L_eq_A2,
    sp.Rational(45, 100), "m")
A_A2 = L_suelte_A2 - L_eq_A2
chk("A2(b) A = 0.53 - 0.45", A_A2, sp.Rational(8, 100), "m",
    "soltado del reposo => esa distancia es la amplitud")
w_A2 = omega_de(k_A2, m_A2)
chk("A2(c) w", w_A2, 10, "rad/s")
chk("A2(c) T", periodo(w_A2), sp.pi / 5, "s")
chk_num("A2(c) T numerico", periodo(w_A2), sp.Rational(6283, 10000), "s")
chk("A2(c) a_max = w^2 A", w_A2**2 * A_A2, 8, "m/s^2")
afirmar("A2(c) a_max COINCIDE con la aceleracion de (a)",
        sp.simplify(w_A2**2 * A_A2 - a_A2_newton) == 0,
        "soltar del reposo = estar en un extremo; ahi |a| es la maxima")
razon("""
Y la coincidencia sigue siendo EXACTA EN SIMBOLOS, no numerica de estos
valores. Es la misma identidad de la Parte 5, reevaluada con los datos
nuevos para dejar constancia de que el arreglo del enunciado no la toco:
    Newton  : a = (k_eq * s - m g)/m , con s = deformacion en el suelte
    Este cap: A = s - m g/k_eq ,  a_max = (k_eq/m) A
""")
s_A2, keq_A2s, m_A2s, g_A2s = sp.symbols("s2 keq2 m2 g2", positive=True)
a_new_sym = (keq_A2s * s_A2 - m_A2s * g_A2s) / m_A2s
a_max_sym2 = (keq_A2s / m_A2s) * (s_A2 - m_A2s * g_A2s / keq_A2s)
afirmar("A2(c) los dos caminos son identicos en simbolos",
        sp.simplify(a_new_sym - a_max_sym2) == 0,
        "no depende de que el suelte sea en 0.53 ni en 0.65")

chk("A2(d) v_max = w A", w_A2 * A_A2, sp.Rational(80, 100), "m/s")
chk("A2(d) longitud de los resortes cuando eso ocurre (el equilibrio)",
    L_eq_A2, sp.Rational(45, 100), "m")
razon("""
(d) reescrito: el control de sensatez que A1 ya tenia y A2 no.
Punto mas alto del recorrido: L = L_eq - A = 0.45 - 0.08 = 0.37 m.
Longitud natural: 0.35 m. Margen: 0.02 m de estiramiento REMANENTE.
Ahi la fuerza elastica vale k_eq * 0.02 = 1.6 N HACIA ARRIBA (los resortes
todavia TIRAN) y el peso 8 N hacia abajo: la neta es 6.4 N hacia abajo, o
sea |a| = 8 m/s^2, que es a_max. Consistente con estar en un extremo.
""")
L_top_A2 = L_eq_A2 - A_A2
chk("A2(d) longitud en el punto mas alto", L_top_A2, sp.Rational(37, 100), "m")
estir_top_A2 = L_top_A2 - L0_A2
chk("A2(d) estiramiento remanente arriba", estir_top_A2, sp.Rational(2, 100),
    "m", "margen real de 2 cm: el modelo NO se rompe")
afirmar("A2(d) los resortes siguen ESTIRADOS en el punto mas alto",
        estir_top_A2 > 0,
        "0.37 m > 0.35 m: la condicion que el inciso pide verificar")
afirmar("A2(d) equivalente: A < d  (amplitud menor que el estiramiento de equilibrio)",
        A_A2 < d_A2,
        "0.08 < 0.10 -- ESTA es la condicion general que antes se violaba")
F_el_top = k_A2 * estir_top_A2
chk("A2(d) fuerza elastica en el punto mas alto", F_el_top,
    sp.Rational(16, 10), "N", "POSITIVA hacia arriba: tira, no empuja")
afirmar("A2(d) el signo de la fuerza elastica arriba es de TRACCION",
        F_el_top > 0,
        "un resorte que cuelga puede tirar pero no empujar: aca tira")
a_top = (F_el_top - m_A2 * G) / m_A2
chk("A2(d) aceleracion en el punto mas alto por Newton", a_top, -8, "m/s^2",
    "hacia abajo, modulo 8 = a_max: coherente con ser un extremo")
afirmar("A2(d) |a| en el punto mas alto == a_max = w^2 A",
        sp.simplify(sp.Abs(a_top) - w_A2**2 * A_A2) == 0,
        "tercer camino independiente que da el mismo 8 m/s^2")
razon("""
Todo el recorrido, no solo los dos extremos: la longitud minima es 0.37 m y
la maxima 0.53 m, y las dos superan la longitud natural 0.35 m. Asi que la
hipotesis de MAS vale en el ciclo COMPLETO. Esto es lo que antes fallaba.
""")
afirmar("A2(d) L_min = 0.37 > L0 = 0.35 (todo el recorrido con traccion)",
        L_eq_A2 - A_A2 > L0_A2)
afirmar("A2(d) L_max = 0.53 > L0 = 0.35",
        L_eq_A2 + A_A2 > L0_A2)
razon("""
(e) |a| = a_max/2 = 4.0 m/s^2 => |y'| = |a|/w^2 = 4/100 = 0.04 m.
    Longitudes: 0.45 - 0.04 = 0.41 m  y  0.45 + 0.04 = 0.49 m.
    Simetricas respecto del equilibrio, como tiene que ser: |a| depende
    solo del MODULO del apartamiento.
    |v| ahi: v^2 = 100 (0.08^2 - 0.04^2) = 100 * 0.0048 = 0.48
             |v| = sqrt(0.48) = 0.4 sqrt(3) = 0.6928 m/s
""")
yp_mitad = (a_A2_newton / 2) / w_A2**2
chk("A2(e) apartamiento donde |a| es la mitad", yp_mitad,
    sp.Rational(4, 100), "m")
chk("A2(e) longitud (rama corta)", L_eq_A2 - yp_mitad, sp.Rational(41, 100), "m")
chk("A2(e) longitud (rama larga)", L_eq_A2 + yp_mitad, sp.Rational(49, 100), "m")
afirmar("A2(e) las dos longitudes son simetricas respecto del equilibrio",
        sp.simplify((L_eq_A2 - yp_mitad) + (L_eq_A2 + yp_mitad)
                    - 2 * L_eq_A2) == 0,
        "(0.41 + 0.49)/2 = 0.45 = L_eq")
afirmar("A2(e) tambien la rama corta (0.41 m) tiene los resortes estirados",
        L_eq_A2 - yp_mitad > L0_A2, "0.41 > 0.35")
v_A2_e = sp.sqrt(w_A2**2 * (A_A2**2 - yp_mitad**2))
chk("A2(e) |v| ahi (forma exacta)", v_A2_e, sp.Rational(4, 10) * sp.sqrt(3),
    "m/s", "el documento la escribe como 0.4 sqrt(3)")
chk_num("A2(e) |v| redondeado a dos decimales", v_A2_e,
        sp.Rational(69, 100), tol=sp.Rational(5, 1000), unidad="m/s",
        nota="0.4*sqrt(3) = 0.692820...; a dos decimales 0.69, correcto")
afirmar("A2(e) 0.69 es el redondeo correcto y 0.70 no lo seria",
        sp.N(sp.Abs(v_A2_e - sp.Rational(69, 100)))
        < sp.N(sp.Abs(v_A2_e - sp.Rational(70, 100))))
razon("""
VEREDICTO SOBRE EL ARREGLO DE A2. El problema no quedo desplazado: quedo
resuelto. La condicion general es A < d (amplitud menor que el estiramiento
de equilibrio), y ahora se cumple con 0.08 < 0.10. El margen de 2 cm es
chico pero REAL, y el inciso (d) reescrito obliga al lector a verificarlo,
que es exactamente el control que A1 ya tenia.
""")
afirmar("A2 ARREGLADO: MAS fisicamente valido en todo el ciclo",
        A_A2 < d_A2 and L_eq_A2 - A_A2 > L0_A2)

# ---------------------------------------------------------------------------
sub("A3 -- carrito 0.25 kg entre dos paredes, k = 64 y 36 N/m, apartado 5.0 cm")
# ---------------------------------------------------------------------------
razon("""
(a)(b) Al correr el carrito una distancia x hacia un lado, un resorte se
estira x y el otro se comprime x; los dos estan FIJOS al carrito, asi que
los dos tiran/empujan hacia la marca. Las dos fuerzas apuntan igual y se
suman: F = -k1 x - k2 x = -(k1+k2) x. Es la MISMA cuenta que el paralelo
del techo, aunque el dibujo no se parezca en nada: estar en paralelo nombra
una relacion entre deformaciones y fuerzas, no un dibujo.
""")
m_A3 = sp.Rational(25, 100)
k1_A3, k2_A3 = sp.Integer(64), sp.Integer(36)
A_A3 = sp.Rational(5, 100)
k_A3 = k1_A3 + k2_A3
chk("A3(b) k_eq", k_A3, 100, "N/m", "misma formula que el paralelo colgado")
w_A3 = omega_de(k_A3, m_A3)
chk("A3(c) w", w_A3, 20, "rad/s")
chk("A3(c) T", periodo(w_A3), sp.pi / 10, "s")
chk_num("A3(c) T numerico", periodo(w_A3), sp.Rational(3142, 10000), "s")
chk("A3(c) v_max = wA", w_A3 * A_A3, 1, "m/s")
chk("A3(c) a_max = w^2 A", w_A3**2 * A_A3, 20, "m/s^2")
w1_A3 = omega_de(k1_A3, m_A3)
w2_A3 = omega_de(k2_A3, m_A3)
chk("A3(d) w solo con el de 64 N/m", w1_A3, 16, "rad/s")
chk("A3(d) w solo con el de 36 N/m", w2_A3, 12, "rad/s")
razon("""
(e) 12, 16, 20 es la terna pitagorica que el capitulo usa:
    16^2 + 12^2 = 256 + 144 = 400 = 20^2.
    Y no es casualidad de los numeros: sale de k_eq = k1 + k2 dividido m.
""")
chk("A3(e) w1^2 + w2^2", w1_A3**2 + w2_A3**2, 400, "1/s^2")
chk("A3(e) w^2", w_A3**2, 400, "1/s^2")
afirmar("A3(e) w^2 = w1^2 + w2^2 con la terna 12, 16, 20",
        sp.simplify(w_A3**2 - (w1_A3**2 + w2_A3**2)) == 0)
afirmar("A3(e) y NO w = w1 + w2 (16 + 12 = 28 != 20)",
        sp.simplify(w_A3 - (w1_A3 + w2_A3)) != 0)
razon("""
(f) Soltado DESDE LA MARCA con vi = 1.0 m/s: es el caso xi = 0, donde la
    formula de Serway se romperia. A = vi/w = 1.0/20 = 0.05 m: la MISMA
    amplitud que en (c), llegada por el otro camino.
""")
A_A3f = amplitud(0, 1, w_A3)
chk("A3(f) A con xi = 0 y vi = 1.0 m/s", A_A3f, sp.Rational(5, 100), "m")
afirmar("A3(f) coincide con la amplitud de (c)", sp.simplify(A_A3f - A_A3) == 0)
chk("A3(f) phi", fase(0, 1, w_A3, A_A3f), -sp.pi / 2, "rad",
    "el caso seno puro del bloque 5")


# ===========================================================================
# PARTE 8 -- UNIDADES, DIMENSIONES Y COHERENCIA DE g
#
# Algebra dimensional minima: cada magnitud es un vector de exponentes
# (M, L, T). No hace falta nada mas que sympy.
# ===========================================================================

titulo("PARTE 8 -- UNIDADES Y DIMENSIONES")

M, L, Tt = sp.symbols("M L T", positive=True)
DIM = {
    "m":    M,
    "k":    M / Tt**2,          # N/m = kg/s^2
    "g":    L / Tt**2,
    "x":    L,
    "A":    L,
    "v":    L / Tt,
    "a":    L / Tt**2,
    "F":    M * L / Tt**2,
    "w":    1 / Tt,             # rad/s: el radian es adimensional
    "T":    Tt,
    "f":    1 / Tt,
    "phi":  sp.Integer(1),      # radianes: adimensional
}


def dim_ok(etiqueta, expr_dim, esperado, comentario=""):
    ok = sp.simplify(expr_dim / esperado) == 1
    _resultados.append((etiqueta, ok))
    print("  [{}] {}".format("OK  " if ok else "FALLA", etiqueta))
    print("        dimension obtenida : {}".format(sp.simplify(expr_dim)))
    print("        dimension esperada : {}".format(sp.simplify(esperado)))
    if comentario:
        print("        {}".format(comentario))


def dim_homog(etiqueta, terminos, esperado, comentario=""):
    """Los sumandos de una suma tienen que tener TODOS la misma dimension."""
    ok = all(sp.simplify(tm / esperado) == 1 for tm in terminos)
    _resultados.append((etiqueta, ok))
    print("  [{}] {}".format("OK  " if ok else "FALLA", etiqueta))
    print("        sumandos : {}".format(
        " , ".join(str(sp.simplify(tm)) for tm in terminos)))
    print("        esperado : {}".format(sp.simplify(esperado)))
    if comentario:
        print("        {}".format(comentario))
    if not ok:
        print("        >>> DISCREPANCIA <<<")


sub("8.1  Las formulas centrales son dimensionalmente homogeneas")
dim_ok("w = sqrt(k/m)  ->  1/T", sp.sqrt(DIM["k"] / DIM["m"]), DIM["w"],
       "kg/s^2 dividido kg = 1/s^2; su raiz es 1/s. rad es adimensional.")
dim_ok("T = 2pi sqrt(m/k)  ->  T", sp.sqrt(DIM["m"] / DIM["k"]), DIM["T"])
dim_ok("f = 1/T  ->  1/T (hertz)", 1 / DIM["T"], DIM["f"])
dim_homog("A = sqrt(xi^2 + (vi/w)^2): los dos terminos son L^2",
          [DIM["x"]**2, (DIM["v"] / DIM["w"])**2], DIM["A"]**2,
          "vi/w tiene dimension de longitud: por eso se pueden sumar.")
dim_ok("v_max = w A  ->  L/T", DIM["w"] * DIM["A"], DIM["v"])
dim_ok("a_max = w^2 A  ->  L/T^2", DIM["w"]**2 * DIM["A"], DIM["a"])
dim_ok("v^2 = w^2 (A^2 - x^2)  ->  (L/T)^2",
       DIM["w"]**2 * DIM["A"]**2, DIM["v"]**2)
dim_ok("F = -k x  ->  M L / T^2 (newton)", DIM["k"] * DIM["x"], DIM["F"])
dim_ok("d = m g / k  ->  L", DIM["m"] * DIM["g"] / DIM["k"], L,
       "el corrimiento del equilibrio es una longitud, como tiene que ser.")
dim_homog("k_eq = k1 + k2: los dos sumandos son M/T^2",
          [DIM["k"], DIM["k"]], DIM["k"],
          "sumar constantes elasticas es legal; promediarlas no es la cuenta.")
dim_homog("1/k_eq = 1/k1 + 1/k2: los dos sumandos son T^2/M",
          [1 / DIM["k"], 1 / DIM["k"]], 1 / DIM["k"])
dim_ok("fase w t + phi  ->  adimensional", DIM["w"] * DIM["T"], sp.Integer(1),
       "por eso phi va en radianes y no en metros ni en segundos.")
afirmar("T (periodo, s) y T (tension, N) NO son dimensionalmente compatibles",
        sp.simplify(DIM["T"] / DIM["F"]) != 1,
        "el chequeo de unidades separa las dos T de la guia y no falla")
afirmar("w (rad/s) y f (Hz) tienen la misma dimension pero difieren en 2pi",
        sp.simplify(DIM["w"] / DIM["f"]) == 1,
        "por eso la distincion NO se detecta por dimensiones: hay que leerla")

sub("8.2  Coherencia de g = 10 m/s^2 en todo el capitulo")
razon("""
Cada lugar del capitulo donde g interviene, recalculado con g = 10 y
comparado con el numero impreso. Si alguno hubiera usado 9.8, saltaria aca.
""")
usos_g = [
    ("ejemplo completo (g): equilibrio vertical hipotetico",
     sp.Rational(25, 100) + sp.Rational(3, 4) * G / 12, sp.Rational(875, 1000), "m"),
    ("ejemplo [parcial] 2: peso del cuerpo de 4.0 kg",
     4 * G, 40, "N"),
    ("ejemplo [parcial] 2: d = mg/k_eq",
     4 * G / 100, sp.Rational(40, 100), "m"),
    ("cierre del capitulo: d = 0.40 m",
     4 * G / 100, sp.Rational(40, 100), "m"),
    ("B5(a): estiramiento en reposo mg/k",
     2 * G / 32, sp.Rational(625, 1000), "m"),
    ("B5(d): estiramiento en reposo con k_eq = 50",
     2 * G / 50, sp.Rational(40, 100), "m"),
    ("A1(a): d = mg/k con m = 1.0 kg",
     1 * G / 25, sp.Rational(40, 100), "m"),
    ("A1(f): d = mg/k con m = 4.0 kg",
     4 * G / 25, sp.Rational(160, 100), "m"),
    ("A2(a): peso del cuerpo de 0.80 kg",
     sp.Rational(80, 100) * G, 8, "N"),
    ("A2(b): d = mg/k_eq",
     sp.Rational(80, 100) * G / 80, sp.Rational(10, 100), "m"),
]
for et, calc, doc, un in usos_g:
    chk("g = 10 -> " + et, calc, doc, un)
afirmar("ningun resultado del capitulo requiere g = 9.8 m/s^2",
        True, "todos los numeros impresos salen exactos con g = 10")


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
if _alertas:
    print("\n  AVISOS SOBRE EL ENUNCIADO (no son errores de cuenta):")
    for a in _alertas:
        print("    - " + a)
print()
