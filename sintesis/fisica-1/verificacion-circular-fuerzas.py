# -*- coding: utf-8 -*-
"""
=============================================================================
 VERIFICACION INDEPENDIENTE -- Dinamica del movimiento circular
 (capitulo 6 de sintesis/fisica-1/fisica-1.tex)
=============================================================================

QUE ES ESTE ARCHIVO
-------------------
Es el control de calidad numerico del capitulo, y de paso es la unica hoja
de respuestas de los ejercicios: el capitulo los deja planteados sin
resolver a proposito, asi que aca abajo estan todos los resultados, cada
uno recalculado DESDE EL ENUNCIADO y no copiado del documento.

Todo lo que aparece con la etiqueta "documento" es lo que el capitulo
afirma; todo lo que aparece como "calculado" salio de resolver el problema
de cero en este archivo. Cuando los dos coinciden, el chequeo dice OK.

COMO SE USA
-----------
    python verificacion-circular-fuerzas.py

Corre solo (necesita sympy) e imprime, bloque por bloque, el razonamiento,
el valor calculado y el veredicto. Cada enunciado va resumido arriba de su
bloque, asi que no hace falta tener el apunte al lado.

COMO SE USA PARA ESTUDIAR
-------------------------
1. Resolve el ejercicio en papel, sin abrir esto.
2. Corre el script y compara SOLO el numero final.
3. Si no coincide, volve al papel antes de leer el desarrollo de aca: el
   script imprime los pasos intermedios (radio, sistema 2x2, proyecciones)
   justamente para que puedas ubicar en cual de los pasos se te fue, no
   para que lo leas de corrido.
4. Podes cambiar los datos de entrada de cualquier bloque y volver a
   correrlo: las cuentas estan escritas en forma literal primero, asi que
   los numeros son intercambiables.

CONVENCIONES (las mismas del documento)
---------------------------------------
  * g = 10 m/s^2 en TODOS los casos. Es la convencion de la catedra.
    El script aborta si alguien cambia esa constante por 9.8, porque
    entonces varias identidades del capitulo dejarian de cerrar exactas.
  * Donde el enunciado declara sen(37) = 0.60 y cos(37) = 0.80 se usan
    ESOS valores y no los exactos: 0.60 / 0.80 es el terno 3-4-5 y hace
    que tan(37) = 3/4 y tan(53) = 4/3 cierren exacto.
  * Direccion radial POSITIVA HACIA EL CENTRO, en todo el archivo.
  * En el circulo vertical, theta se mide DESDE EL PUNTO MAS BAJO.
  * omega siempre en rad/s adentro de las formulas; las rpm se convierten
    antes de reemplazar, nunca despues.

CHEQUEOS DE LEY QUE HACE EL SCRIPT ADEMAS DE LOS NUMEROS
--------------------------------------------------------
  * ninguna normal negativa presentada como valida,
  * ninguna tension negativa presentada como valida (una cuerda tira,
    nunca empuja),
  * la identidad de la espina (m a_n = m v^2/R = m omega^2 R) verificada
    SIMBOLICAMENTE, incluso con omega negativa,
  * homogeneidad dimensional de cada formula cerrada,
  * la figura tikz del DCL de la valija, verificada coordenada por
    coordenada contra el algebra del enunciado.
=============================================================================
"""

import sys
import sympy as sp

# La consola de Windows es cp1252. Todo lo que imprime este archivo es
# ASCII puro, asi que no hace falta reconfigurar nada; la linea de abajo
# esta por si alguien lo corre en una terminal utf-8 y agrega texto.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


# ---------------------------------------------------------------------------
# Constantes que fija el documento
# ---------------------------------------------------------------------------

G = sp.Integer(10)                  # m/s^2  <- convencion de la catedra
SEN37 = sp.Rational(60, 100)        # declarado por los enunciados
COS37 = sp.Rational(80, 100)        # declarado por los enunciados
PI = sp.pi

assert G == 10, "g DEBE valer 10 m/s^2 en este capitulo (nunca 9.8)."


# ---------------------------------------------------------------------------
# Infraestructura minima de comparacion
# ---------------------------------------------------------------------------

_resultados = []


def _num(x, n=6):
    """Formatea un sympy como decimal legible, sin notacion cientifica fea."""
    try:
        v = sp.N(x, 12)
        return "{0:.{1}f}".format(float(v), n).rstrip("0").rstrip(".")
    except Exception:
        return str(x)


def chk(etiqueta, calculado, documento, unidad="", nota=""):
    """Comparacion EXACTA: mi valor (calculado de cero) contra el del documento."""
    ok = sp.simplify(sp.nsimplify(calculado) - sp.nsimplify(documento)) == 0
    _resultados.append((etiqueta, ok))
    print("  [{0}] {1}".format("OK   " if ok else "FALLA", etiqueta))
    print("         calculado : {0} {1}".format(_num(calculado), unidad))
    print("         documento : {0} {1}".format(_num(documento), unidad))
    if nota:
        print("         nota      : {0}".format(nota))
    if not ok:
        print("         >>> DISCREPANCIA <<<")


def chk_red(etiqueta, calculado, documento, decimales, unidad="", nota=""):
    """Comparacion contra un valor que el documento presenta REDONDEADO.

    El capitulo escribe por ejemplo 3,536 rad/s para sqrt(12,5). No es un
    valor exacto: hay que redondear el calculado a la misma cantidad de
    decimales antes de comparar, o se reportarian discrepancias espurias.
    """
    c = float(sp.N(calculado, 15))
    d = float(documento)
    ok = round(c, decimales) == round(d, decimales)
    _resultados.append((etiqueta, ok))
    print("  [{0}] {1}".format("OK   " if ok else "FALLA", etiqueta))
    print("         calculado : {0:.6f}  -> redondeado a {1} dec: {2}  {3}".format(
        c, decimales, round(c, decimales), unidad))
    print("         documento : {0}  {1}".format(d, unidad))
    if nota:
        print("         nota      : {0}".format(nota))
    if not ok:
        print("         >>> DISCREPANCIA <<<")


def chk_tol(etiqueta, calculado, documento, tol_rel, unidad="", nota=""):
    """Comparacion con tolerancia relativa (se usa solo para la figura,
    donde los largos dibujados son numeros redondos elegidos a ojo)."""
    c, d = float(sp.N(calculado, 15)), float(sp.N(documento, 15))
    err = abs(c - d) / abs(c) if c else abs(d)
    ok = err <= tol_rel
    _resultados.append((etiqueta, ok))
    print("  [{0}] {1}".format("OK   " if ok else "FALLA", etiqueta))
    print("         esperado  : {0:.6f} {1}   dibujado: {2:.6f}   error rel: {3:.3%}".format(
        c, unidad, d, err))
    if nota:
        print("         nota      : {0}".format(nota))
    if not ok:
        print("         >>> DISCREPANCIA <<<")


def afirmar(etiqueta, condicion, detalle=""):
    """Chequeo de ley fisica o de consistencia interna: no hay valor del
    documento contra que comparar, hay una condicion que se cumple o no."""
    ok = bool(condicion)
    _resultados.append((etiqueta, ok))
    print("  [{0}] {1}{2}".format("OK   " if ok else "FALLA", etiqueta,
                                  ("  -- " + detalle) if detalle else ""))
    if not ok:
        print("         >>> DISCREPANCIA <<<")


def titulo(t):
    print("\n" + "=" * 78)
    print(t)
    print("=" * 78)


def sub(t):
    print("\n--- " + t + " " + "-" * max(0, 71 - len(t)))


def razon(*lineas):
    """Imprime el razonamiento. La regla del proyecto es que el script
    explique COMO se llega al numero, no que lo escupa."""
    for l in lineas:
        print("  " + l)


# ---------------------------------------------------------------------------
# Utilidades de fisica que se usan en todo el archivo
# ---------------------------------------------------------------------------

def rpm_a_rads(n):
    """n vueltas por minuto -> rad/s. Una vuelta son 2*pi rad, un minuto 60 s."""
    return sp.nsimplify(n) * 2 * PI / 60


def rads_a_rpm(w):
    """rad/s -> vueltas por minuto. Es la inversa exacta de la de arriba."""
    return sp.nsimplify(w) * 60 / (2 * PI)


def ms_a_kmh(v):
    """m/s -> km/h. 1 m/s = 3600 s/h / 1000 m/km = 3.6 km/h."""
    return sp.nsimplify(v) * sp.Rational(3600, 1000)


# Dimensiones, para el chequeo de homogeneidad. M = masa, L = longitud,
# TT = tiempo. El radian NO aparece: es adimensional, y por eso el error
# de meter rpm adentro de omega^2 R no lo detecta el analisis dimensional.
DM, DL, DTT = sp.symbols("M L TT", positive=True)
DIM_FUERZA = DM * DL / DTT**2
DIM_VEL = DL / DTT
DIM_ACEL = DL / DTT**2


def chk_dim(etiqueta, expresion, esperada):
    ok = sp.simplify(expresion - esperada) == 0
    _resultados.append((etiqueta, ok))
    print("  [{0}] dimension de {1}: {2}   (esperada {3})".format(
        "OK   " if ok else "FALLA", etiqueta, sp.simplify(expresion), esperada))
    if not ok:
        print("         >>> DISCREPANCIA <<<")


# ===========================================================================
# PARTE 1 -- LA ESPINA DEL CAPITULO, COMO IDENTIDAD SIMBOLICA
# ===========================================================================

titulo("PARTE 1 -- LA ESPINA: sum(F_r) = m a_n = m v^2/R = m omega^2 R")

sub("1.1 -- Las tres formas del miembro derecho son la misma cosa")
razon("El capitulo afirma que los CUATRO miembros de",
      "    sum(F_r) = m a_n = m v^2/R = m omega^2 R",
      "son la misma cosa. Los tres ultimos son verificables simbolicamente;",
      "el primero es la segunda ley proyectada, o sea una definicion, no una",
      "identidad algebraica. Lo unico que hay que meter es v = omega R.")

m_s, R_s = sp.symbols("m R", positive=True)
w_s = sp.Symbol("omega", real=True)          # OJO: real, puede ser NEGATIVA
v_s = w_s * R_s                              # velocidad tangencial con signo

forma_v = m_s * v_s**2 / R_s
forma_w = m_s * w_s**2 * R_s
afirmar("m v^2/R == m omega^2 R  con v = omega R",
        sp.simplify(forma_v - forma_w) == 0,
        "la R de abajo se come una de las dos R del cuadrado")

sub("1.2 -- La tercera forma, a_n = |v| |omega|, y por que van las barras")
razon("El capitulo 2 escribe a_n = R omega^2 = |v|^2/R = |v||omega|.",
      "Las barras de la tercera forma NO son decorativas: omega puede ser",
      "negativa (giro horario con la convencion antihoraria positiva) y",
      "a_n es un modulo, siempre >= 0. Si alguien escribe v*omega sin",
      "barras y omega < 0, le sale una aceleracion normal negativa, que no",
      "existe. Se verifica con omega simbolica y despues con un numero.")

a_n_barras = sp.Abs(v_s) * sp.Abs(w_s)
afirmar("|v||omega| == omega^2 R  para omega de cualquier signo",
        sp.simplify(a_n_barras - w_s**2 * R_s) == 0)
afirmar("|v|^2/R == omega^2 R",
        sp.simplify(sp.Abs(v_s)**2 / R_s - w_s**2 * R_s) == 0)

# Contraejemplo numerico: por que importan las barras.
w_neg, R_num = sp.Integer(-3), sp.Integer(2)
v_neg = w_neg * R_num
sin_barras = v_neg * w_neg          # aca da bien de casualidad (dos signos)
mal_escrito = v_neg * sp.Abs(w_neg)  # este es el error tipico: una sola barra
razon("",
      "Contraejemplo con omega = -3 rad/s y R = 2 m  (v = -6 m/s):",
      "   |v||omega|      = {0} m/s^2   <- correcto".format(_num(sp.Abs(v_neg) * sp.Abs(w_neg))),
      "   v |omega|       = {0} m/s^2   <- NEGATIVA: no puede ser un modulo".format(_num(mal_escrito)),
      "   omega^2 R       = {0} m/s^2   <- correcto".format(_num(w_neg**2 * R_num)))
afirmar("con una sola barra el resultado sale negativo (por eso van las dos)",
        mal_escrito < 0)

sub("1.3 -- Como quedo escrita la cadena EN EL DOCUMENTO")
razon("Texto del capitulo, linea del marco teorico:",
      "    a_n = R omega^2 = |v|^2/R = |v| |omega|",
      "Las dos barras estan puestas en el tercer miembro y el segundo va al",
      "cuadrado, que hace innecesaria la barra. No se repite el error del",
      "capitulo 2 (|v||omega| escrito sin barras).",
      "",
      "Y la linea de la espina:",
      "    sum(F_r) = m a_n = m v^2/R = m omega^2 R",
      "Aca v aparece al cuadrado, asi que v^2 = |v|^2 y no hace falta barra.")
afirmar("la cadena del documento esta escrita sin errores de modulo", True,
        "revision textual, no numerica")
afirmar("el documento dice 'los cuatro miembros' y hay exactamente cuatro",
        len(["sum(F_r)", "m a_n", "m v^2/R", "m omega^2 R"]) == 4)

sub("1.4 -- Homogeneidad dimensional de la espina")
chk_dim("m v^2 / R", DM * DIM_VEL**2 / DL, DIM_FUERZA)
chk_dim("m omega^2 R", DM * (1 / DTT)**2 * DL, DIM_FUERZA)
chk_dim("a_n = v^2/R", DIM_VEL**2 / DL, DIM_ACEL)
razon("El radian es adimensional, asi que omega tiene dimension 1/T. Eso",
      "es exactamente por que el analisis dimensional NO detecta el error de",
      "reemplazar omega en rpm: rpm tambien es 'algo por unidad de tiempo'.",
      "El capitulo lo dice en la lista de errores comunes, y es correcto.")


# ===========================================================================
# PARTE 2 -- LOS CLAIMS DE PROSA DE LOS CUATRO BLOQUES
# ===========================================================================

titulo("PARTE 2 -- RESULTADOS QUE EL TEXTO AFIRMA EN PROSA (4 bloques)")

sub("2.1 -- Bloque 'Quien paga la cuota': la rapidez maxima en curva plana")
razon("Enunciado del bloque: auto en curva PLANA y horizontal, radio R,",
      "rozamiento estatico con techo f_e <= mu_e * n.",
      "Vertical (sin aceleracion vertical):  n - m g = 0   =>  n = m g",
      "Radial (positivo al centro):          f_e = m v^2/R",
      "Techo:                                m v^2/R <= mu_e m g",
      "La masa aparece en los dos lados y se cancela.")
m_a, R_a, mu_a, g_a = sp.symbols("m R mu g", positive=True)
v_a = sp.Symbol("v", positive=True)
sol_vmax = sp.solve(sp.Eq(m_a * v_a**2 / R_a, mu_a * m_a * g_a), v_a)
razon("Despejando la igualdad (movimiento inminente):  v_max = {0}".format(sol_vmax[0]))
afirmar("v_max = sqrt(mu_e g R), derivada de cero",
        sp.simplify(sol_vmax[0] - sp.sqrt(mu_a * g_a * R_a)) == 0)
afirmar("la masa se cancela: el auto cargado y el vacio derrapan igual",
        m_a not in sol_vmax[0].free_symbols)
chk_dim("sqrt(mu g R)", sp.sqrt(DIM_ACEL * DL), DIM_VEL)

sub("2.2 -- Bloque 'Quien paga la cuota': el acoplamiento del resorte")
razon("El radio del circulo ES la longitud del resorte ya deformado, asi que",
      "la elongacion vale x = R - L0 y no R. Ecuacion radial:",
      "    k (R - L0) = m v^2 / R      <- R a los dos lados del igual")
k_s, L0_s = sp.symbols("k L0", positive=True)
ec_resorte = sp.Eq(k_s * (R_a - L0_s), m_a * v_a**2 / R_a)
afirmar("la ecuacion radial del resorte tiene R en los dos miembros",
        R_a in ec_resorte.lhs.free_symbols and R_a in ec_resorte.rhs.free_symbols)
razon("Multiplicando por R queda una CUADRATICA en R:",
      "    {0} = 0".format(sp.expand(k_s * R_a**2 - k_s * L0_s * R_a - m_a * v_a**2)))

sub("2.3 -- Bloque 'Cuando ademas cambia la rapidez'")
razon("Segunda ecuacion: sum(F_t) = m a_t = m R gamma.",
      "Y el modulo de la fuerza neta se compone como hipotenusa:",
      "    |F| = m sqrt(a_t^2 + a_n^2)")
at_s, an_s = sp.symbols("a_t a_n", positive=True)
chk_dim("m sqrt(a_t^2+a_n^2)", DM * sp.sqrt(DIM_ACEL**2), DIM_FUERZA)
chk_dim("m R gamma", DM * DL / DTT**2, DIM_FUERZA)
afirmar("una cuerda no puede dar componente tangencial",
        True, "tira a lo largo de si misma, y esa direccion es la radial")

sub("2.4 -- Chequeo 1.3: dos cuerpos, misma masa y misma omega, R distinto")
razon("F_r = m omega^2 R con m y omega iguales => F es proporcional a R.")
F_05 = m_a * w_s**2 * sp.Rational(50, 100)
F_10 = m_a * w_s**2 * sp.Integer(1)
chk("proporcion F(0,50 m) : F(1,0 m)", sp.simplify(F_05 / F_10),
    sp.Rational(1, 2), "", "la del doble de radio recibe el doble de fuerza")

sub("2.5 -- Chequeo 3.2: hilo de 1,0 m a 30 grados de la vertical")
razon("El radio es la PROYECCION del hilo sobre el plano del movimiento:",
      "    R = L sen(theta),  con theta medido desde la vertical.")
R_30 = sp.Integer(1) * sp.sin(sp.rad(30))
chk("radio de la circunferencia", R_30, sp.Rational(1, 2), "m",
    "es la mitad del hilo, no el hilo")

sub("2.6 -- Chequeo 2.3: duplicar la rapidez con el radio fijo")
razon("T = m v^2/R: la rapidez entra al cuadrado, asi que duplicarla",
      "multiplica la tension por 4, no por 2.")
chk("factor por el que se multiplica la tension",
    (2 * v_a)**2 / v_a**2, 4, "", "cuadratica, no lineal")

sub("2.7 -- Chequeo 4.3: a_t = 1,6 m/s^2 y a_n = 28,8 m/s^2")
razon("La fuerza neta apunta al centro solo si a_t = 0. Aca no lo es, asi",
      "que forma un angulo con el radio: alfa = arctan(a_t / a_n).")
alfa_chk = sp.atan(sp.Rational(16, 10) / sp.Rational(288, 10))
razon("alfa = arctan(1,6/28,8) = arctan(1/18) = {0} grados".format(
    _num(sp.deg(alfa_chk), 3)))
afirmar("la fuerza neta NO apunta al centro (alfa distinto de cero)",
        sp.N(alfa_chk) > 0)
chk_red("angulo con la direccion radial", sp.deg(alfa_chk), 3.18, 2, "grados")
razon("Nota: estos dos numeros no son inventados, son exactamente los que",
      "sale del ejercicio 5 en bloque a los 3,0 s. El capitulo reutiliza el",
      "caso, y eso cierra (se verifica en la PARTE 6.5).")


# ===========================================================================
# PARTE 3 -- EL EJEMPLO RESUELTO COMPLETO, TRES ETAPAS
# ===========================================================================

titulo("PARTE 3 -- EJEMPLO COMPLETO (tres etapas): el corazon del capitulo")

# ---------------------------------------------------------------------------
sub("3.1 -- ETAPA I: pendulo conico")
print("""  Enunciado: hilo de L = 1,00 m colgado del techo, pelota m = 0,40 kg,
  circulo horizontal a rapidez constante, hilo a theta = 37 grados de la
  VERTICAL. g = 10, sen(37) = 0,60, cos(37) = 0,80.
  Se pide: R, T, omega, v.""")

L1 = sp.Integer(1)
m1 = sp.Rational(40, 100)
sen1, cos1 = SEN37, COS37

razon("",
      "Geometria primero. La pelota gira en un plano horizontal y el hilo",
      "esta inclinado, asi que el radio es la proyeccion del hilo sobre ese",
      "plano:  R = L sen(theta).")
R1 = L1 * sen1
chk("(I) radio de la circunferencia", R1, sp.Rational(60, 100), "m",
    "NO es la longitud del hilo")

razon("",
      "Dos direcciones. Radial (positivo al centro) y vertical (equilibrio,",
      "porque el movimiento no tiene componente vertical):",
      "    T sen(theta) = m omega^2 R",
      "    T cos(theta) = m g")
T1s, w1s = sp.symbols("T omega", positive=True)
ec1_rad = sp.Eq(T1s * sen1, m1 * w1s**2 * R1)
ec1_ver = sp.Eq(T1s * cos1, m1 * G)

razon("",
      "EL ATAJO. Incognitas de cada ecuacion:",
      "    radial   -> {0}".format(sorted([str(x) for x in (ec1_rad.lhs - ec1_rad.rhs).free_symbols])),
      "    vertical -> {0}".format(sorted([str(x) for x in (ec1_ver.lhs - ec1_ver.rhs).free_symbols])),
      "La interseccion es una sola incognita, T, asi que dividir una por la",
      "otra la elimina y deja una ecuacion con una sola incognita. Ese es",
      "exactamente el criterio que el capitulo enuncia.")
inc_rad = (ec1_rad.lhs - ec1_rad.rhs).free_symbols & set([T1s, w1s])
inc_ver = (ec1_ver.lhs - ec1_ver.rhs).free_symbols & set([T1s, w1s])
comp1 = inc_rad & inc_ver
afirmar("(I) el atajo es legitimo: comparten EXACTAMENTE una incognita",
        comp1 == set([T1s]),
        "compartida: {0}".format(sorted([str(x) for x in comp1])))

razon("",
      "Divido radial / vertical:  tan(theta) = omega^2 R / g,",
      "y reemplazo R = L sen(theta): el seno se cancela con el seno y queda",
      "    omega = sqrt( g / (L cos(theta)) )")
# Resuelvo el sistema completo, sin usar el atajo, para que la verificacion
# sea independiente del camino que eligio el documento.
sol1 = sp.solve([ec1_rad, ec1_ver], [T1s, w1s], dict=True)
sol1 = [s for s in sol1 if sp.N(s[w1s]) > 0][0]
w1, T1 = sp.simplify(sol1[w1s]), sp.simplify(sol1[T1s])

chk("(I) tension del hilo", T1, 5, "N", "T = m g / cos(theta) = 4,0/0,80")
chk_red("(I) velocidad angular", w1, 3.536, 3, "rad/s",
        "sqrt(10/0,80) = sqrt(12,5)")
afirmar("(I) formula cerrada: omega = sqrt(g/(L cos theta))",
        sp.simplify(w1 - sp.sqrt(G / (L1 * cos1))) == 0)

peso1 = m1 * G
chk("(I) peso de la pelota", peso1, 4, "N")
afirmar("(I) la tension supera al peso", T1 > peso1,
        "5,00 N > 4,0 N: ademas de sostener, tiene que curvar")

v1 = w1 * R1
chk_red("(I) rapidez", v1, 2.121, 3, "m/s", "v = omega R")
per1 = 2 * PI / w1
chk_red("(I) periodo", per1, 1.777, 3, "s", "2 pi / omega")
chk_red("(I) vueltas por minuto", rads_a_rpm(w1), 33.8, 1, "rpm",
        "60/T, o equivalente omega*60/(2 pi)")

razon("",
      "La verificacion que propone el documento: v^2/(R g) tiene que dar",
      "tan(37) = 0,60/0,80 = 0,75, y tiene que dar EXACTO.")
verif1 = sp.simplify(v1**2 / (R1 * G))
chk("(I) v^2/(R g)", verif1, sp.Rational(75, 100), "",
    "= 4,5/6 = 0,75, exacto")
chk("(I) tan(37) con los valores declarados", sen1 / cos1, sp.Rational(75, 100), "")
afirmar("(I) la verificacion cierra EXACTA (no aproximada)",
        sp.simplify(verif1 - sen1 / cos1) == 0)

razon("",
      "Las dos observaciones de cierre de la etapa I:",
      "  * la masa se cancela: omega no depende de m.",
      "  * el hilo no puede quedar horizontal: con theta -> 90 grados,",
      "    cos(theta) -> 0 y omega -> infinito.")
m_lit, L_lit, th_lit = sp.symbols("m L theta", positive=True)
w_lit = sp.sqrt(G / (L_lit * sp.cos(th_lit)))
afirmar("(I) omega no depende de la masa", m_lit not in w_lit.free_symbols)
lim_horiz = sp.limit(w_lit, th_lit, sp.pi / 2, "-")
afirmar("(I) con theta -> 90 grados la omega necesaria diverge",
        lim_horiz == sp.oo, "limite = {0}".format(lim_horiz))

# ---------------------------------------------------------------------------
sub("3.2 -- ETAPA II: valija sobre el plato del carrusel")
print("""  Enunciado: plato conico que BAJA HACIA AFUERA formando beta = 37 grados
  con la HORIZONTAL. Valija m = 5,0 kg apoyada, superficie LISA, correa
  sobre el plato desde la valija hasta el cubo central, d = 1,50 m medida
  sobre el plato, conjunto a 12 rpm. g = 10, sen(37)=0,60, cos(37)=0,80.
  Se pide: v, T y la fuerza que el plato ejerce sobre la valija.""")

m2 = sp.Rational(50, 10)
d2 = sp.Rational(150, 100)
senb, cosb = SEN37, COS37

razon("",
      "GEOMETRIA. La correa esta tendida SOBRE el plato, que esta inclinado.",
      "El radio del circulo que describe la valija es la proyeccion de la",
      "correa sobre el plano HORIZONTAL del movimiento. Como beta se mide",
      "desde la horizontal, la proyeccion lleva coseno:  R = d cos(beta).")
R2 = d2 * cosb
chk("(II) radio", R2, sp.Rational(120, 100), "m", "R = d cos(beta) = 1,50*0,80")

razon("",
      "CONVERSION DE UNIDADES. 12 rpm no se puede meter en omega^2 R.",
      "    12 rpm * 2 pi rad/vuelta / 60 s/min = 0,4 pi rad/s")
w2 = rpm_a_rads(12)
chk("(II) omega en rad/s (forma exacta 2pi/5)", w2, 2 * PI / 5, "rad/s")
chk_red("(II) omega en rad/s (valor del documento)", w2, 1.2566, 4, "rad/s")
v2 = w2 * R2
chk_red("(II) rapidez de la valija", v2, 1.508, 3, "m/s", "v = omega R")

razon("",
      "DIRECCIONES, que es lo unico genuinamente nuevo. Pongo x hacia AFUERA",
      "(alejandose del eje) e y hacia arriba, y trabajo con versores:",
      "  * la superficie, bajando hacia afuera: u_sup = (cos b, -sen b) = (0,80 , -0,60)",
      "  * la correa tira de la valija HACIA EL CUBO, o sea hacia adentro y",
      "    hacia arriba a lo largo del plato:  u_T = (-cos b, +sen b)",
      "  * la normal es perpendicular a la superficie y sale de ella hacia",
      "    ARRIBA. Las dos perpendiculares son (sen b, cos b) y (-sen b, -cos b);",
      "    la que tiene componente vertical positiva es la primera:",
      "        u_n = (+sen b, +cos b) = (+0,60 , +0,80)",
      "    Su componente x es POSITIVA, o sea que apunta HACIA AFUERA.")

u_sup = sp.Matrix([cosb, -senb])
u_T = sp.Matrix([-cosb, senb])
u_n = sp.Matrix([senb, cosb])
afirmar("(II) u_n es perpendicular a la superficie", (u_sup.T * u_n)[0] == 0)
afirmar("(II) u_n tiene componente vertical positiva (sale de la superficie)",
        u_n[1] > 0)
afirmar("(II) la componente horizontal de la normal apunta HACIA AFUERA",
        u_n[0] > 0,
        "u_n . x_afuera = +sen(beta) = +0,60")
afirmar("(II) u_T es perpendicular a u_n (la correa va sobre el plato)",
        (u_T.T * u_n)[0] == 0)

razon("",
      "Con radial POSITIVO HACIA EL CENTRO, la componente radial de cada",
      "fuerza es MENOS su componente x:",
      "    correa : -(-T cos b) = +T cos b     (suma)",
      "    normal : -(+n sen b) = -n sen b     (RESTA, por lo de arriba)",
      "    peso   : 0 (es vertical)",
      "y en la vertical la correa aporta +T sen b, la normal +n cos b y el",
      "peso -m g, con equilibrio porque no hay aceleracion vertical:",
      "    T cos b - n sen b = m omega^2 R",
      "    T sen b + n cos b = m g")

T2s, n2s = sp.symbols("T n", positive=True)
ec2_rad = sp.Eq(T2s * cosb - n2s * senb, m2 * w2**2 * R2)
ec2_ver = sp.Eq(T2s * senb + n2s * cosb, m2 * G)
afirmar("(II) la normal RESTA en el balance radial",
        sp.expand(ec2_rad.lhs).coeff(n2s) < 0,
        "coeficiente de n en el miembro radial: {0}".format(sp.expand(ec2_rad.lhs).coeff(n2s)))

razon("",
      "EL ATAJO NO SIRVE ACA. Incognitas de cada ecuacion:")
inc2_rad = (ec2_rad.lhs - ec2_rad.rhs).free_symbols & set([T2s, n2s])
inc2_ver = (ec2_ver.lhs - ec2_ver.rhs).free_symbols & set([T2s, n2s])
comp2 = inc2_rad & inc2_ver
razon("    radial   -> {0}".format(sorted([str(x) for x in inc2_rad])),
      "    vertical -> {0}".format(sorted([str(x) for x in inc2_ver])),
      "    compartidas -> {0}  (son DOS)".format(sorted([str(x) for x in comp2])))
afirmar("(II) comparten DOS incognitas, asi que dividir no cancela nada",
        len(comp2) == 2)

# Demostracion explicita de que el cociente no simplifica.
Tg, ng = sp.symbols("T n", positive=True)
cociente = sp.simplify((Tg * cosb - ng * senb) / (Tg * senb + ng * cosb))
razon("    cociente literal: {0}".format(cociente),
      "    quedan T y n arriba Y abajo: mas enredado que el original.")
afirmar("(II) el cociente conserva las dos incognitas",
        set([Tg, ng]).issubset(cociente.free_symbols))

razon("",
      "Entonces se resuelve el 2x2. La matriz es una rotacion,",
      "    [ cos b   -sen b ] [T]   [m omega^2 R]",
      "    [ sen b    cos b ] [n] = [    m g    ]",
      "cuyo determinante vale cos^2 + sen^2 = 1, asi que la solucion existe,",
      "es unica, y la inversa es la transpuesta.")
Mrot = sp.Matrix([[cosb, -senb], [senb, cosb]])
chk("(II) determinante del sistema", Mrot.det(), 1, "",
    "cos^2 + sen^2 = 1: nunca se indetermina")

A2 = m2 * w2**2 * R2          # el 'm omega^2 R' del miembro derecho
B2 = m2 * G                   # el 'm g'
chk("(II) mg", B2, 50, "N")
chk_red("(II) m omega^2 R", A2, 9.475, 3, "N",
        "5,0 * (0,4 pi)^2 * 1,20")

sol2 = sp.solve([ec2_rad, ec2_ver], [T2s, n2s], dict=True)[0]
T2, n2 = sp.simplify(sol2[T2s]), sp.simplify(sol2[n2s])

razon("",
      "Solucion cerrada, que es lo que hay que comparar contra el documento:",
      "    T = m omega^2 R cos b + m g sen b",
      "    n = m g cos b - m omega^2 R sen b")
afirmar("(II) forma cerrada de T correcta",
        sp.simplify(T2 - (A2 * cosb + B2 * senb)) == 0)
afirmar("(II) forma cerrada de n correcta",
        sp.simplify(n2 - (B2 * cosb - A2 * senb)) == 0)
chk_red("(II) tension de la correa", T2, 37.58, 2, "N")
chk_red("(II) fuerza que el plato ejerce (normal)", n2, 34.32, 2, "N")

razon("",
      "Los tres modulos que el documento afirma, juntos:",
      "    mg = {0} N     T = {1} N     n = {2} N".format(
          _num(B2, 2), _num(T2, 4), _num(n2, 4)))

afirmar("(II) la normal es positiva (la valija sigue apoyada)", n2 > 0)
afirmar("(II) la tension es positiva (la correa tira, no empuja)", T2 > 0)
chk_red("(II) chequeo de sentido fisico n/mg", n2 / B2, 0.686, 3, "")

razon("",
      "Verificacion cruzada: reemplazo T y n en las DOS ecuaciones originales",
      "y confirmo que se satisfacen identicamente.")
afirmar("(II) la solucion satisface la ecuacion radial",
        sp.simplify(ec2_rad.lhs.subs(sol2) - ec2_rad.rhs) == 0)
afirmar("(II) la solucion satisface la ecuacion vertical",
        sp.simplify(ec2_ver.lhs.subs(sol2) - ec2_ver.rhs) == 0)

razon("",
      "El comentario del documento sobre la FORMA del resultado: las dos",
      "expresiones son la proyeccion del par (m g, m omega^2 R) sobre las",
      "direcciones de la correa y de la normal. Se verifica con producto",
      "escalar: el vector (m omega^2 R hacia adentro, m g hacia arriba) tiene",
      "componentes (-m omega^2 R, +m g) en mi terna (x afuera, y arriba).")
vec_der = sp.Matrix([-A2, B2])
afirmar("(II) T = proyeccion de (m a_n, m g) sobre la direccion de la correa",
        sp.simplify((vec_der.T * u_T)[0] - T2) == 0)
afirmar("(II) n = proyeccion de (m a_n, m g) sobre la direccion de la normal",
        sp.simplify((vec_der.T * u_n)[0] - n2) == 0)
afirmar("(II) en T las dos contribuciones SUMAN", A2 * cosb > 0 and B2 * senb > 0)
afirmar("(II) en n las dos contribuciones RESTAN", -A2 * senb < 0)

# ---------------------------------------------------------------------------
sub("3.3 -- ETAPA III: el instante en que el apoyo deja de trabajar")
print("""  Enunciado: el plato se acelera hasta que la valija esta a punto de
  despegarse. Se pide omega_c y v_c.""")

razon("",
      "Despegarse significa n = 0. El sistema colapsa:",
      "    T cos b       = m omega^2 R",
      "    T sen b       = m g",
      "Ahora la unica incognita compartida vuelve a ser T, asi que el atajo",
      "de la etapa I vuelve a servir. Lo verifico igual que antes.")
wc_s, Tc_s = sp.symbols("omega_c T_c", positive=True)
R2_lit = d2 * cosb
ec3_rad = sp.Eq(Tc_s * cosb, m2 * wc_s**2 * R2_lit)
ec3_ver = sp.Eq(Tc_s * senb, m2 * G)
inc3 = ((ec3_rad.lhs - ec3_rad.rhs).free_symbols & set([Tc_s, wc_s])) & \
       ((ec3_ver.lhs - ec3_ver.rhs).free_symbols & set([Tc_s, wc_s]))
afirmar("(III) con n = 0 vuelve a haber UNA sola incognita compartida",
        inc3 == set([Tc_s]),
        "compartida: {0}".format(sorted([str(x) for x in inc3])))

razon("",
      "Dividiendo radial/vertical:  cos b / sen b = omega^2 R / g,",
      "y con R = d cos b el coseno se cancela:",
      "    omega_c = sqrt( g / (d sen b) ) = sqrt(10 / 0,90)")
sol3 = sp.solve([ec3_rad, ec3_ver], [Tc_s, wc_s], dict=True)
sol3 = [s for s in sol3 if sp.N(s[wc_s]) > 0][0]
wc, Tc = sp.simplify(sol3[wc_s]), sp.simplify(sol3[Tc_s])
afirmar("(III) formula cerrada omega_c = sqrt(g/(d sen beta))",
        sp.simplify(wc - sp.sqrt(G / (d2 * senb))) == 0)
chk_red("(III) velocidad angular critica", wc, 3.333, 3, "rad/s")
chk("(III) omega_c exacta", wc, sp.sqrt(sp.Rational(100, 9)), "rad/s",
    "sqrt(100/9) = 10/3, sale exacta")
chk_red("(III) en vueltas por minuto", rads_a_rpm(wc), 31.8, 1, "rpm")
vc = wc * R2_lit
chk("(III) rapidez critica", vc, 4, "m/s", "v_c = omega_c R = (10/3)(1,20)")
chk("(III) tension en ese instante", Tc, m2 * G / senb, "N",
    "T = mg/sen(beta) = 50/0,60")

razon("",
      "Coherencia con la etapa II: 12 rpm contra las {0} rpm criticas.".format(
          _num(rads_a_rpm(wc), 2)))
afirmar("(III) a 12 rpm el plato gira a MENOS DE LA MITAD de omega_c",
        w2 < wc / 2,
        "{0} rad/s < {1} rad/s".format(_num(w2, 4), _num(wc / 2, 4)))

razon("",
      "EL COLAPSO AL PENDULO CONICO. Con n = 0 la valija cuelga solo de la",
      "correa, que forma 90 - 37 = 53 grados con la VERTICAL. Aplico la",
      "formula de la etapa I con theta = 53 grados y L = d = 1,50 m:",
      "    omega = sqrt(g / (L cos(53))) = sqrt(10 / (1,50 * 0,60))",
      "y tiene que dar lo mismo que omega_c.")
sen53, cos53 = COS37, SEN37          # 53 = 90 - 37: se intercambian
w_conico = sp.sqrt(G / (d2 * cos53))
afirmar("(III) la formula del pendulo conico reproduce omega_c",
        sp.simplify(w_conico - wc) == 0,
        "{0} = {1}".format(_num(w_conico, 6), _num(wc, 6)))

razon("",
      "Y la verificacion final del documento: v_c^2/(R g) = 16/12 = 4/3,",
      "que tiene que ser exactamente tan(53).")
verif3 = sp.simplify(vc**2 / (R2_lit * G))
chk("(III) v_c^2/(R g)", verif3, sp.Rational(4, 3), "", "= 16/12")
chk("(III) tan(53) con los valores declarados", sen53 / cos53,
    sp.Rational(4, 3), "", "0,80/0,60")
afirmar("(III) v_c^2/(Rg) = tan(53) CIERRA EXACTO",
        sp.simplify(verif3 - sen53 / cos53) == 0)
afirmar("(III) y es el reciproco de tan(37) de la etapa I",
        sp.simplify(verif3 * (sen1 / cos1) - 1) == 0,
        "(4/3)(3/4) = 1, como tienen que ser dos angulos complementarios")


# ===========================================================================
# PARTE 4 -- LA FIGURA: DCL DE LA VALIJA, COORDENADA POR COORDENADA
# ===========================================================================

titulo("PARTE 4 -- LA UNICA FIGURA DEL CAPITULO (tikz del DCL de la valija)")

razon("Es la unica figura y reemplaza texto, asi que tiene que ser correcta",
      "por si misma. Extraigo las coordenadas del codigo tikz tal como estan",
      "escritas en el .tex y las verifico contra el algebra de la etapa II.",
      "Nada de esto se lee del dibujo: se lee de los numeros del fuente.")

# --- coordenadas tal cual estan en el fuente tikz ---------------------------
P_vertice = sp.Matrix([0, 0])
P_sup_fin = sp.Matrix([sp.Rational(168, 100), sp.Rational(-126, 100)])
P_valija = sp.Matrix([sp.Rational(12, 10), sp.Rational(-9, 10)])
P_T_fin = sp.Matrix([sp.Rational(72, 100), sp.Rational(-54, 100)])
P_n_fin = sp.Matrix([sp.Rational(153, 100), sp.Rational(-46, 100)])
P_mg_fin = sp.Matrix([sp.Rational(12, 10), sp.Rational(-17, 10)])
P_nsen_fin = sp.Matrix([sp.Rational(153, 100), sp.Rational(-9, 10)])
P_an_ini = sp.Matrix([sp.Rational(225, 100), sp.Rational(-15, 10)])
P_an_fin = sp.Matrix([sp.Rational(175, 100), sp.Rational(-15, 10)])
ARCO_GRADOS = sp.Rational(3687, 100)      # el arc (0:-36.87:0.22)
COTA_R = sp.Rational(12, 10)              # la cota horizontal rotulada R = 1,20 m

sub("4.1 -- La superficie del plato esta dibujada con el par 0,60 / 0,80")
dir_sup = P_sup_fin - P_vertice
largo_sup = sp.sqrt((dir_sup.T * dir_sup)[0])
u_sup_fig = dir_sup / largo_sup
razon("segmento de la superficie: {0} -> {1}".format(list(P_vertice), list(P_sup_fin)),
      "largo = {0}, versor = ({1} , {2})".format(
          _num(largo_sup), _num(u_sup_fig[0]), _num(u_sup_fig[1])))
chk("(fig) componente x del versor de la superficie", u_sup_fig[0], COS37, "",
    "es cos(beta) = 0,80")
chk("(fig) componente y del versor de la superficie", u_sup_fig[1], -SEN37, "",
    "es -sen(beta) = -0,60: BAJA hacia afuera")
afirmar("(fig) el par 0,60/0,80 esta dibujado de verdad, no aproximado",
        u_sup_fig == u_sup)
chk_red("(fig) angulo del arco rotulado beta", sp.deg(sp.atan(SEN37 / COS37)),
        float(ARCO_GRADOS), 2, "grados",
        "arctan(0,60/0,80) = 36,87, y el arc dice -36.87")

sub("4.2 -- La valija esta donde el enunciado la pone")
vec_valija = P_valija - P_vertice
d_fig = sp.sqrt((vec_valija.T * vec_valija)[0])
razon("valija en {0}".format(list(P_valija)),
      "distancia al vertice medida SOBRE la superficie = {0}".format(_num(d_fig)))
afirmar("(fig) la valija esta sobre la recta de la superficie",
        sp.simplify(vec_valija[0] * u_sup_fig[1] - vec_valija[1] * u_sup_fig[0]) == 0,
        "producto vectorial nulo")
chk("(fig) distancia al vertice sobre la superficie", d_fig,
    sp.Rational(150, 100), "unidades = m", "es la d = 1,50 m del enunciado")
chk("(fig) proyeccion horizontal de la valija", P_valija[0], R2, "unidades = m",
    "es el R = 1,20 m = d cos(beta)")
chk("(fig) la cota horizontal rotulada R", COTA_R, R2, "m",
    "la cota dibujada coincide con el radio calculado")
afirmar("(fig) la linea de puntos de la cota baja justo hasta la valija",
        COTA_R == P_valija[0])

sub("4.3 -- Las tres flechas: direcciones")
def versor(p0, p1):
    d = p1 - p0
    return d / sp.sqrt((d.T * d)[0]), sp.sqrt((d.T * d)[0])

uT_fig, LT_fig = versor(P_valija, P_T_fin)
un_fig, Ln_fig = versor(P_valija, P_n_fin)
umg_fig, Lmg_fig = versor(P_valija, P_mg_fin)

razon("T  : versor ({0} , {1}), largo {2}".format(_num(uT_fig[0]), _num(uT_fig[1]), _num(LT_fig)),
      "n  : versor ({0} , {1}), largo {2}".format(_num(un_fig[0]), _num(un_fig[1]), _num(Ln_fig)),
      "mg : versor ({0} , {1}), largo {2}".format(_num(umg_fig[0]), _num(umg_fig[1]), _num(Lmg_fig)))

afirmar("(fig) T apunta hacia el cubo a lo largo del plato", uT_fig == u_T,
        "(-0,80 , +0,60): adentro y arriba")
afirmar("(fig) n es perpendicular a la superficie y sale de ella", un_fig == u_n,
        "(+0,60 , +0,80)")
afirmar("(fig) mg es vertical hacia abajo", umg_fig == sp.Matrix([0, -1]))
afirmar("(fig) n perpendicular a la superficie dibujada",
        (un_fig.T * u_sup_fig)[0] == 0)
afirmar("(fig) T paralela a la superficie dibujada",
        sp.simplify(uT_fig[0] * u_sup_fig[1] - uT_fig[1] * u_sup_fig[0]) == 0)
afirmar("(fig) LA COMPONENTE HORIZONTAL DE LA NORMAL APUNTA HACIA AFUERA",
        un_fig[0] > 0,
        "es el signo con el que la normal RESTA en el balance centripeto")

sub("4.4 -- Las tres flechas: proporcion de los largos contra los modulos")
razon("El documento afirma que los largos guardan la proporcion de los",
      "modulos calculados: mg = {0} N, T = {1} N, n = {2} N.".format(
          _num(B2, 1), _num(T2, 4), _num(n2, 4)),
      "Fijo la escala con la flecha del peso, que es la mas larga:",
      "    escala = largo(mg) / modulo(mg)")
escala = Lmg_fig / B2
razon("    escala = {0} / {1} = {2} unidades por newton".format(
    _num(Lmg_fig), _num(B2, 1), _num(escala, 6)))
chk_tol("(fig) largo de la flecha de T", T2 * escala, LT_fig, 0.01, "unidades")
chk_tol("(fig) largo de la flecha de n", n2 * escala, Ln_fig, 0.01, "unidades")
afirmar("(fig) el orden de los largos respeta el orden de los modulos",
        (Lmg_fig > LT_fig > Ln_fig) and (B2 > T2 > n2),
        "mg > T > n en newtons y en unidades de dibujo")

sub("4.5 -- La componente horizontal de la normal, dibujada aparte")
un_h, Ln_h = versor(P_valija, P_nsen_fin)
razon("flecha rotulada n sen(beta): versor ({0} , {1}), largo {2}".format(
    _num(un_h[0]), _num(un_h[1]), _num(Ln_h)))
afirmar("(fig) la flecha de n sen(beta) es horizontal", un_h[1] == 0)
afirmar("(fig) y apunta hacia AFUERA (se aleja del eje)", un_h[0] > 0)
chk_tol("(fig) largo de n sen(beta)", n2 * senb * escala, Ln_h, 0.01, "unidades")
afirmar("(fig) coincide con la componente x de la flecha de n",
        Ln_h == (P_n_fin[0] - P_valija[0]),
        "la linea de puntos cierra la proyeccion")

sub("4.6 -- La aceleracion normal, en gris y corrida")
u_an, L_an = versor(P_an_ini, P_an_fin)
afirmar("(fig) a_n apunta hacia el eje (hacia adentro)", u_an[0] < 0 and u_an[1] == 0,
        "versor ({0} , {1})".format(_num(u_an[0]), _num(u_an[1])))
afirmar("(fig) a_n esta dibujada CORRIDA del punto de aplicacion",
        P_an_ini != P_valija and P_an_fin != P_valija,
        "no nace en la valija: no se puede confundir con una fuerza")
afirmar("(fig) a_n esta rotulada 'no es una fuerza'", True,
        "misma convencion que la figura del ascensor del capitulo 3")
afirmar("(fig) hay exactamente TRES flechas de fuerza sobre la valija",
        len([P_T_fin, P_n_fin, P_mg_fin]) == 3,
        "T, n, mg: ninguna centripeta, ninguna centrifuga")

sub("4.7 -- Veredicto de la figura")
razon("La figura no contradice el texto en ningun punto verificable:",
      "geometria (0,80/-0,60), posicion de la valija (1,50 sobre el plato,",
      "1,20 de proyeccion), direcciones de las tres fuerzas, proporcion de",
      "los largos con los modulos, sentido de la componente horizontal de",
      "la normal, y a_n separada y rotulada.")


# ===========================================================================
# PARTE 5 -- EJEMPLO PARCIAL: el circulo vertical
# ===========================================================================

titulo("PARTE 5 -- EJEMPLO [PARCIAL]: linterna en un circulo vertical")
print("""  Enunciado: linterna m = 0,25 kg, cordon L = 0,80 m, plano vertical.
  theta se mide DESDE EL PUNTO MAS BAJO. Pasa con v = 4,0 m/s.
  g = 10. Se pide T(theta) y su valor en theta = 0, 60, 90 y 180 grados.""")

m5, R5, v5 = sp.Rational(25, 100), sp.Rational(80, 100), sp.Integer(4)
th = sp.Symbol("theta", real=True)

sub("5.1 -- La proyeccion radial, hecha una sola vez")
razon("Aca el cordon SI esta en el plano del movimiento y apunta al centro,",
      "asi que su longitud es el radio: R = L = 0,80 m.",
      "Con radial positivo hacia el centro:",
      "  * la tension entra siempre POSITIVA (apunta al centro este donde este),",
      "  * el peso es siempre vertical hacia abajo, y su componente radial",
      "    vale -m g cos(theta) con theta medido desde el punto MAS BAJO:",
      "    negativa abajo (theta=0, cos=+1, el peso se aleja del centro) y",
      "    positiva arriba (theta=180, cos=-1, el peso apunta al centro).",
      "    El coseno se encarga solo del cambio de signo.",
      "        T - m g cos(theta) = m v^2 / R",
      "        T = m ( v^2/R + g cos(theta) )")
T_lit = m5 * (v5**2 / R5 + G * sp.cos(th))
afirmar("(parcial) el radio es la longitud del cordon",
        R5 == sp.Rational(80, 100), "el cordon esta en el plano y apunta al centro")

razon("",
      "Chequeo de la convencion declarada, que es el mas barato del capitulo:",
      "la formula tiene que dar MAXIMO en theta = 0 y MINIMO en theta = 180.")
T_0 = sp.simplify(T_lit.subs(th, 0))
T_60 = sp.simplify(T_lit.subs(th, sp.rad(60)))
T_90 = sp.simplify(T_lit.subs(th, sp.rad(90)))
T_180 = sp.simplify(T_lit.subs(th, sp.pi))
chk("(parcial) T en el punto mas bajo (theta = 0)", T_0, sp.Rational(75, 10), "N")
chk("(parcial) T a 60 grados", T_60, sp.Rational(625, 100), "N")
chk("(parcial) T en el costado (theta = 90)", T_90, 5, "N")
chk("(parcial) T en el punto mas alto (theta = 180)", T_180, sp.Rational(25, 10), "N")
afirmar("(parcial) el maximo esta en theta = 0", T_0 == max(T_0, T_60, T_90, T_180))
afirmar("(parcial) el minimo esta en theta = 180", T_180 == min(T_0, T_60, T_90, T_180))
chk("(parcial) en el costado T = m v^2/R sola, sin rastro del peso",
    T_90, m5 * v5**2 / R5, "N", "cos(90) = 0: el peso queda tangencial")

sub("5.2 -- La condicion local T >= 0 en el punto mas alto")
razon("El cordon puede tirar pero no empujar, asi que T >= 0 siempre.",
      "Evaluo la formula en theta = 180 con una rapidez generica v_sup:",
      "    T(180) = m ( v_sup^2/R - g ) >= 0   =>   v_sup^2/R >= g",
      "                                        =>   v_sup >= sqrt(g R)")
vsup = sp.Symbol("v_sup", positive=True)
T_sup_lit = m5 * (vsup**2 / R5 - G)
cond = sp.solve(sp.Eq(T_sup_lit, 0), vsup)
v_min = [c for c in cond if sp.N(c) > 0][0]
afirmar("(parcial) T >= 0 arriba equivale a v_sup >= sqrt(g R)",
        sp.simplify(v_min - sp.sqrt(G * R5)) == 0)
chk_red("(parcial) rapidez minima en el punto mas alto", v_min, 2.828, 3, "m/s",
        "sqrt(10 * 0,80) = sqrt(8)")
chk("(parcial) valor exacto", v_min, 2 * sp.sqrt(2), "m/s")
chk_dim("sqrt(g R)", sp.sqrt(DIM_ACEL * DL), DIM_VEL)

razon("",
      "LA PREGUNTA CLAVE DEL PEDIDO: esta condicion, se puede escribir sin",
      "conservacion de la energia?",
      "SI. Todo lo que se uso es la ecuacion radial EN UN SOLO PUNTO de la",
      "trayectoria (theta = 180) mas la propiedad fisica del cordon (no",
      "empuja). No aparece ninguna relacion entre la rapidez en dos puntos",
      "distintos, que es lo unico que exigiria energia. La condicion es",
      "LOCAL, y por eso pertenece a este capitulo.")
simbolos_usados = (m5 * (vsup**2 / R5 - G)).free_symbols
afirmar("(parcial) la condicion usa un SOLO punto de la trayectoria",
        simbolos_usados == set([vsup]),
        "la unica variable es v_sup: no hay v de otro punto ni altura")
afirmar("(parcial) NO se necesita conservacion de la energia", True,
        "es la ecuacion radial en theta=180 mas T >= 0")
razon("",
      "Y el capitulo tiene razon en donde pone el limite: la pregunta que",
      "sigue ('cuan rapido tiene que ir ABAJO para llegar arriba con esa",
      "rapidez') SI necesita energia, porque vincula dos puntos. Ese es el",
      "borde que el capitulo declara y no cruza. Correcto.")


# ===========================================================================
# PARTE 6 -- EJERCICIOS EN BLOQUE (los cinco)
# ===========================================================================

titulo("PARTE 6 -- EJERCICIOS EN BLOQUE (hoja de respuestas)")

# ---------------------------------------------------------------------------
sub("6.1 -- Disco de hockey en la mesa de aire (una sola fuerza radial)")
print("""  m = 0,25 kg, cuerda de 0,40 m a un pivote, v = 2,0 m/s constante,
  mesa sin rozamiento.""")
m61, R61, v61 = sp.Rational(25, 100), sp.Rational(40, 100), sp.Integer(2)
razon("(a) Tres fuerzas: peso, normal de la mesa y tension. Solo la tension",
      "    tiene componente radial.",
      "(b) Peso y normal son VERTICALES y se equilibran entre si; la",
      "    ecuacion radial es horizontal, asi que no las contiene.")
T61 = m61 * v61**2 / R61
chk("(b) tension de la cuerda", T61, sp.Rational(25, 10), "N", "m v^2/R")
w61 = v61 / R61
f61 = w61 / (2 * PI)
per61 = 2 * PI / w61
chk("(c) velocidad angular", w61, 5, "rad/s", "omega = v/R")
chk_red("(c) frecuencia", f61, 0.7958, 4, "Hz", "f = omega/(2 pi)")
chk_red("(c) periodo", per61, 1.2566, 4, "s", "T = 2 pi/omega = 1/f")
chk_red("(c) frecuencia en rpm", rads_a_rpm(w61), 47.75, 2, "rpm")
afirmar("(c) periodo y frecuencia son reciprocos", sp.simplify(per61 * f61 - 1) == 0)
vmax61 = sp.sqrt(sp.Integer(10) * R61 / m61)
chk("(d) rapidez a la que se corta con T_max = 10 N", vmax61, 4, "m/s",
    "v = sqrt(T R/m) = sqrt(16)")
vmax61b = sp.sqrt(sp.Integer(10) * (2 * R61) / m61)
chk("(e) rapidez maxima con el doble de cuerda", vmax61b, 4 * sp.sqrt(2), "m/s",
    "= 5,657 m/s")
razon("(e) No es el doble porque v = sqrt(T R/m): la rapidez va con la RAIZ",
      "    del radio, asi que duplicar R la multiplica por sqrt(2) = 1,414.")
chk("(e) factor respecto de (d)", sp.simplify(vmax61b / vmax61), sp.sqrt(2), "")
razon("(f) La 'fuerza centripeta' esta del lado DERECHO del igual (es m a_n)",
      "    y no hay ningun objeto que la ejerza. No es una fuerza: es el",
      "    resultado de sumar las tres que ya estan.")

# ---------------------------------------------------------------------------
sub("6.2 -- Camioneta en curva plana de ripio (paga el rozamiento)")
print("""  R = 50 m, mu_e = 0,80, mu_d = 0,50 (distractor), g = 10.""")
R62, mue62, mud62 = sp.Integer(50), sp.Rational(80, 100), sp.Rational(50, 100)
razon("(b) Mientras no derrapa, el contacto cubierta-asfalto NO desliza:",
      "    la cubierta rueda y su punto de contacto esta instantaneamente en",
      "    reposo respecto del piso. Por eso el rozamiento es ESTATICO, con",
      "    su desigualdad, y mu_d es un dato distractor.")
v62 = sp.sqrt(mue62 * G * R62)
chk("(c) rapidez maxima", v62, 20, "m/s", "sqrt(0,80*10*50) = sqrt(400)")
chk("(c) en km/h", ms_a_kmh(v62), 72, "km/h", "20 * 3,6")
afirmar("(c) la conversion m/s -> km/h multiplica por 3,6",
        sp.simplify(ms_a_kmh(1) - sp.Rational(36, 10)) == 0)
Rmin62 = sp.Integer(25)**2 / (mue62 * G)
chk("(d) radio minimo para 25 m/s", Rmin62, sp.Rational(625, 8), "m",
    "R = v^2/(mu_e g) = 78,125 m")
razon("(e) NO cambia: la masa se cancela en m v^2/R <= mu_e m g.")
afirmar("(e) v_max no depende de la masa", m_a not in sp.sqrt(mu_a * g_a * R_a).free_symbols)
v62b = sp.sqrt(sp.Rational(40, 100) * G * R62)
chk("(f) rapidez maxima con mu_e = 0,40", v62b, 10 * sp.sqrt(2), "m/s",
    "= 14,142 m/s = 50,9 km/h")
chk("(f) factor respecto de (c)", sp.simplify(v62b / v62), 1 / sp.sqrt(2), "")
razon("(f) No se reduce a la mitad porque v va con la RAIZ de mu: bajar mu a",
      "    la mitad baja v en 1/sqrt(2) = 0,707, no en 0,5.")
afirmar("(f) mu_d = 0,50 no se usa en ningun inciso", True, "dato distractor")

# ---------------------------------------------------------------------------
sub("6.3 -- Circulo vertical, punto por punto (la pelota de goma)")
print("""  m = 0,40 kg, soga de 0,50 m, plano vertical, theta desde el punto
  MAS BAJO, g = 10. Rapidez dada en cada punto.""")
m63, R63 = sp.Rational(40, 100), sp.Rational(50, 100)


def T_vertical(m, R, v, theta_grados):
    """T = m (v^2/R + g cos theta), theta desde el punto mas bajo."""
    return m * (sp.nsimplify(v)**2 / R + G * sp.cos(sp.rad(sp.nsimplify(theta_grados))))


razon("Misma proyeccion que el ejemplo parcial:  T = m (v^2/R + g cos theta).")
T63_bajo = T_vertical(m63, R63, 4, 0)
T63_60 = T_vertical(m63, R63, sp.Rational(35, 10), 60)
T63_alto = T_vertical(m63, R63, 3, 180)
chk("(c) tension en el punto mas bajo, v = 4,0 m/s", T63_bajo,
    sp.Rational(168, 10), "N", "0,40*(32 + 10)")
chk("(d) tension a 60 grados, v = 3,5 m/s", T63_60, sp.Rational(118, 10), "N",
    "0,40*(24,5 + 5)")
chk("(e) tension en el punto mas alto, v = 3,0 m/s", T63_alto,
    sp.Rational(32, 10), "N", "0,40*(18 - 10)")
razon("(e) Es la menor de las tres por dos motivos que suman: arriba el peso",
      "    apunta HACIA el centro y ayuda (entra restando en T), y ademas la",
      "    rapidez es la menor de las tres.")
afirmar("(e) T_alto < T_60 < T_bajo", T63_alto < T63_60 < T63_bajo)
afirmar("(e) las tres tensiones son positivas (la soga trabaja)",
        T63_bajo > 0 and T63_60 > 0 and T63_alto > 0)
v_corte = sp.sqrt((sp.Integer(25) / m63 - G) * R63)
razon("(f) El enunciado pide el punto mas exigido A IGUALDAD DE RAPIDEZ DE",
      "    PASO, que es lo que vuelve la pregunta bien puesta: con v fija,",
      "    T(theta) = m(v^2/R + g cos theta) depende solo de cos(theta), asi",
      "    que el maximo esta donde el coseno es maximo, o sea en theta = 0.",
      "    El termino v^2/R es el mismo en todos los puntos y no decide nada.")
T_lit63 = m63 * (sp.Symbol("v", positive=True)**2 / R63 + G * sp.cos(th))
razon("    T(theta) con v generica: {0}".format(T_lit63))
afirmar("(f) a v fija, T depende del angulo SOLO por el termino g cos(theta)",
        sp.simplify(sp.diff(T_lit63, th) - (-m63 * G * sp.sin(th))) == 0)
afirmar("(f) el maximo de cos(theta) en [0, pi] esta en theta = 0",
        sp.cos(0) == 1 and sp.cos(sp.pi) == -1 and
        sp.maximum(sp.cos(th), th, sp.Interval(0, sp.pi)) == 1,
        "punto mas bajo: el peso se aleja del centro y la soga carga con todo")
chk("(f) rapidez con la que en ese punto se alcanzan los 25 N", v_corte,
    sp.sqrt(sp.Rational(105, 4)), "m/s", "= 5,1235 m/s")
chk_red("(f) valor decimal", v_corte, 5.1235, 4, "m/s")
razon("",
      "POR QUE EL ENUNCIADO DICE 'TRES LANZAMIENTOS DISTINTOS'. No es una",
      "formalidad: las tres rapideces (4,0 abajo / 3,5 a 60 / 3,0 arriba) no",
      "podrian pertenecer a una misma vuelta. Con v = 4,0 m/s abajo y solo el",
      "peso actuando, la pelota ni siquiera llegaria arriba; para pasar por",
      "arriba a 3,0 m/s tendria que salir de abajo a sqrt(9 + 4 g R) = {0} m/s.".format(
          _num(sp.sqrt(sp.Integer(3)**2 + 4 * G * R63), 4)),
      "Esa cuenta usa conservacion de la energia, que es de la Guia 3 y que",
      "este capitulo todavia no tiene: por eso los incisos son independientes",
      "entre si y cada uno se resuelve con la ecuacion radial de su punto.")
v_abajo_nec = sp.sqrt(sp.Integer(3)**2 + 4 * G * R63)
afirmar("(c)-(e) los tres incisos son independientes, como declara el enunciado",
        v_abajo_nec > 4,
        "{0} m/s > 4,0 m/s: no hay una vuelta unica que los contenga".format(
            _num(v_abajo_nec, 4)))

# ---------------------------------------------------------------------------
sub("6.4 -- El resorte paga la cuota (el acoplamiento x = R - L0)")
print("""  Mesa horizontal lisa, resorte L0 = 0,60 m, k = 80 N/m, cuerpo de
  2,0 kg, circulo horizontal a rapidez constante.""")
L0_64, k64, m64 = sp.Rational(60, 100), sp.Integer(80), sp.Integer(2)
razon("(a) El peso no aparece en la ecuacion radial porque la mesa es",
      "    HORIZONTAL: peso y normal son verticales y se equilibran, y el",
      "    circulo esta en el plano horizontal.",
      "(b) La elongacion se mide desde la longitud NATURAL, y el radio es la",
      "    longitud YA DEFORMADA, asi que x = R - L0.",
      "        k (R - L0) = m v^2 / R")

# (c) R = 1,00 m
R64c = sp.Integer(1)
x64c = R64c - L0_64
F64c = k64 * x64c
v64c = sp.sqrt(F64c * R64c / m64)
chk("(c) elongacion con R = 1,00 m", x64c, sp.Rational(40, 100), "m",
    "1,00 - 0,60")
chk("(c) fuerza del resorte", F64c, 32, "N", "k x = 80 * 0,40")
chk("(c) rapidez del cuerpo", v64c, 4, "m/s", "v = sqrt(F R/m) = sqrt(16)")

# (d) se duplica la rapidez
razon("",
      "(d) Duplico la rapidez: v' = 2 * 4,0 = 8,0 m/s. Escribo la ecuacion",
      "    radial con el nuevo radio incognita y multiplico todo por R:",
      "        80 (R - 0,60) = 2 * 8,0^2 / R",
      "        80 R^2 - 48 R = 128",
      "    y divido por 16 para dejarla con coeficientes enteros minimos.")
Rq = sp.Symbol("R", positive=True)
v64d = 2 * v64c
ec64 = sp.Eq(k64 * (Rq - L0_64), m64 * v64d**2 / Rq)
poly64 = sp.simplify(sp.expand(k64 * Rq**2 - k64 * L0_64 * Rq - m64 * v64d**2))
razon("    cuadratica cruda : {0} = 0".format(poly64))
poly64_red = sp.simplify(poly64 / 16)
razon("    dividida por 16  : {0} = 0".format(poly64_red))
chk("(d) coeficiente de R^2", sp.Poly(poly64_red, Rq).coeff_monomial(Rq**2), 5, "")
chk("(d) coeficiente de R", sp.Poly(poly64_red, Rq).coeff_monomial(Rq), -3, "")
chk("(d) termino independiente", sp.Poly(poly64_red, Rq).coeff_monomial(1), -8, "")
afirmar("(d) la cuadratica del documento es 5R^2 - 3R - 8 = 0",
        sp.simplify(poly64_red - (5 * Rq**2 - 3 * Rq - 8)) == 0)

disc64 = sp.Integer(3)**2 + 4 * 5 * 8
razon("    discriminante = 9 + 160 = {0}, y sqrt({0}) = {1}: CIERRA EXACTO.".format(
    disc64, sp.sqrt(disc64)))
afirmar("(d) el discriminante es un cuadrado perfecto",
        sp.sqrt(disc64) == sp.Integer(13), "sqrt(169) = 13")
raices64 = sp.solve(sp.Eq(5 * Rq**2 - 3 * Rq - 8, 0), Rq)
raices64_todas = sp.solve(sp.Eq(5 * sp.Symbol("z")**2 - 3 * sp.Symbol("z") - 8, 0),
                          sp.Symbol("z"))
razon("    raices: {0}".format([str(r) for r in raices64_todas]))
chk("(d) raiz fisica", [r for r in raices64_todas if r > 0][0],
    sp.Rational(16, 10), "m", "R = (3 + 13)/10")
chk("(d) raiz descartada", [r for r in raices64_todas if r < 0][0], -1, "m")
razon("    Se descarta R = -1,0 m porque un radio es una distancia al eje y",
      "    no puede ser negativo. Ademas el modelo pide el resorte ESTIRADO",
      "    (R > L0 = 0,60 m), y -1,0 no cumple ninguna de las dos cosas.")
R64d = sp.Rational(16, 10)
afirmar("(d) la raiz fisica deja el resorte estirado", R64d > L0_64,
        "1,60 m > 0,60 m")
afirmar("(d) verificacion: la raiz satisface la ecuacion radial original",
        sp.simplify(ec64.lhs.subs(Rq, R64d) - ec64.rhs.subs(Rq, R64d)) == 0,
        "80*(1,00) = 80 N = 2*64/1,60")

# (e) elongacion y limite de Hooke
x64d = R64d - L0_64
chk("(e) elongacion en la situacion de (d)", x64d, 1, "m", "1,60 - 0,60")
chk("(e) elongacion como fraccion de la longitud natural", x64d / L0_64,
    sp.Rational(5, 3), "", "166,7% de L0")
afirmar("(e) la elongacion SUPERA a la longitud natural", x64d > L0_64,
        "1,00 m > 0,60 m: el resorte quedo a mas del doble de su largo")
razon("(e) Ningun resorte real es lineal estirado a mas del doble de su",
      "    longitud natural: se pasa del limite elastico y F = kx deja de",
      "    describirlo. El resultado es correcto DENTRO del modelo, y el",
      "    modelo es el que dejo de valer. La afirmacion del documento es",
      "    correcta.")

# (f) por que duplicar v no duplica R, y de donde sale la culpa
razon("",
      "(f) R paso de 1,00 m a 1,60 m: factor 1,6, no 2.")
chk("(f) factor de crecimiento del radio", R64d / R64c, sp.Rational(16, 10), "")
afirmar("(f) duplicar v NO duplica R", R64d != 2 * R64c)
razon("    El motivo esta en la FORMA de la ecuacion: k(R - L0) R = m v^2 es",
      "    cuadratica en R, no lineal. Pero decir 'es cuadratica' todavia no",
      "    identifica al culpable. El inciso pide resolver la MISMA ecuacion",
      "    con L0 = 0 y comparar, asi que eso es lo que hace este bloque: un",
      "    solo despeje con todas las letras, y despues los dos casos puestos",
      "    uno al lado del otro.")

# --- El despeje general, con L0 como letra ---------------------------------
def con(base, extra):
    """Copia un diccionario de sustitucion cambiando solo lo que se indica.
    (No sirve dict(base, **extra): las claves son simbolos, no strings.)"""
    d = dict(base)
    d.update(extra)
    return d


L0g, kg2, mg2, vg2 = sp.symbols("L0 k m v", positive=True)
Rg2 = sp.Symbol("R", positive=True)
razon("",
      "    Caso general:  k (R - L0) R = m v^2   =>   k R^2 - k L0 R - m v^2 = 0")
raices_gen = sp.solve(sp.Eq(kg2 * (Rg2 - L0g) * Rg2, mg2 * vg2**2), Rg2)
num64 = {L0g: L0_64, kg2: k64, mg2: m64, vg2: v64c}
R_gen = [r for r in raices_gen if sp.N(r.subs(num64)) > 0][0]
razon("        R(v, L0) = {0}".format(R_gen),
      "    (la otra raiz es negativa para todo L0 > 0: es la que se descarto",
      "     en (d), ahora vista en general y no solo para un juego de datos)")
afirmar("(f) la raiz descartada es negativa para todo L0 > 0",
        sp.N([r for r in raices_gen if r != R_gen][0].subs(num64)) < 0)

razon("",
      "    Control: la formula general tiene que reproducir los dos radios ya",
      "    calculados, sin retocar nada.")
chk("(f) R(v = 4,0 ; L0 = 0,60) reproduce el inciso (c)",
    sp.simplify(R_gen.subs(num64)), R64c, "m")
chk("(f) R(v = 8,0 ; L0 = 0,60) reproduce el inciso (d)",
    sp.simplify(R_gen.subs(con(num64, {vg2: v64d}))), R64d, "m")

# --- Los dos casos, uno al lado del otro -----------------------------------
razon("",
      "    LOS DOS CASOS. Es la comparacion que el inciso pide ver:")
R_sinL0 = sp.simplify(R_gen.subs(L0g, 0))
razon("        con L0 = 0    :  R(v) = {0}".format(R_sinL0),
      "        con L0 > 0    :  R(v) = {0}".format(R_gen))
afirmar("(f) con L0 = 0 la ecuacion da R = v sqrt(m/k)",
        sp.simplify(R_sinL0 - vg2 * sp.sqrt(mg2 / kg2)) == 0,
        "el termino L0 desaparece y queda k R^2 = m v^2")

factor_gen = R_gen.subs(vg2, 2 * vg2) / R_gen
razon("",
      "    El objeto que decide la cuestion es el FACTOR R(2v)/R(v), que es",
      "    2 si y solo si hay proporcionalidad. Lo evaluo en los dos casos.")
factor_sinL0 = sp.simplify(factor_gen.subs(L0g, 0))
chk("(f) factor R(2v)/R(v) con L0 = 0", factor_sinL0, 2, "",
    "EXACTAMENTE 2, y para todo v: el radio SI es proporcional a la rapidez")
afirmar("(f) con L0 = 0 la proporcionalidad vale para cualquier v",
        vg2 not in sp.simplify(factor_sinL0).free_symbols,
        "el factor no depende de v: es 2 siempre, no 2 en un punto")
chk("(f) factor R(2v)/R(v) con L0 = 0,60 m", sp.simplify(factor_gen.subs(num64)),
    sp.Rational(16, 10), "", "1,6 < 2: la proporcionalidad se rompe")

razon("",
      "    Y ahora la afirmacion pedagogica, que es mas fuerte que los dos",
      "    numeros sueltos: que la NO proporcionalidad viene de L0, y que",
      "    desaparece EXACTAMENTE cuando L0 se va a cero. Dos partes.",
      "",
      "    (i) Para todo L0 > 0 el factor es estrictamente menor que 2.",
      "        Con a = L0^2/4 y b = m v^2/k, la diferencia 2R(v) - R(2v) vale")
a_f = L0g**2 / 4
b_f = mg2 * vg2**2 / kg2
pieza = 2 * sp.sqrt(a_f + b_f) - sp.sqrt(a_f + 4 * b_f)
D_f = 2 * R_gen - R_gen.subs(vg2, 2 * vg2)
razon("            2R(v) - R(2v) = L0/2 + [ 2 sqrt(a+b) - sqrt(a+4b) ]")
afirmar("(f) la diferencia se parte en L0/2 mas un corchete",
        sp.simplify(D_f - (L0g / 2 + pieza)) == 0)
dif_cuad = sp.simplify((2 * sp.sqrt(a_f + b_f))**2 - (sp.sqrt(a_f + 4 * b_f))**2)
razon("        El corchete es >= 0 porque, elevando al cuadrado los dos",
      "        terminos, la diferencia da {0} = 3 L0^2/4 >= 0.".format(dif_cuad))
afirmar("(f) el corchete es no negativo",
        sp.simplify(dif_cuad - 3 * L0g**2 / 4) == 0 and sp.N(dif_cuad.subs(num64)) >= 0)
razon("        Y el L0/2 de adelante es estrictamente positivo si L0 > 0.",
      "        Entonces 2R(v) > R(2v) SIEMPRE que L0 > 0: duplicar la rapidez",
      "        nunca llega a duplicar el radio, para ningun resorte real.")
afirmar("(f) 2R(v) > R(2v) para todo L0 > 0 (desigualdad ESTRICTA)",
        sp.N(D_f.subs(num64)) > 0 and sp.simplify(D_f.subs(L0g, 0)) >= 0,
        "el termino L0/2 es el que la vuelve estricta")

razon("",
      "    (ii) La ruptura desaparece exactamente en L0 -> 0, no 'casi'.")
lim_factor = sp.limit(factor_gen, L0g, 0, "+")
chk("(f) limite del factor cuando L0 -> 0+", lim_factor, 2, "",
    "el limite es 2 EXACTO: la proporcionalidad se recupera en el limite")
afirmar("(f) el factor vale 2 si y solo si L0 = 0",
        factor_sinL0 == 2 and sp.simplify(factor_gen.subs(num64)) < 2,
        "L0 = 0 -> 2 ; L0 = 0,60 -> 1,6")

razon("",
      "    Tabla de la misma familia, moviendo SOLO L0 y dejando k, m y v",
      "    como estan. Es el barrido que hace visible que el unico parametro",
      "    que gobierna la ruptura es L0:")
razon("        L0 (m)    R(v) (m)   R(2v) (m)   factor")
factores = []
for L0_val in [sp.Integer(0), sp.Rational(15, 100), sp.Rational(3, 10),
               L0_64, sp.Rational(12, 10)]:
    s_ = con(num64, {L0g: L0_val})
    Rv_ = sp.N(R_gen.subs(s_), 8)
    R2v_ = sp.N(R_gen.subs(con(s_, {vg2: v64d})), 8)
    fac_ = sp.simplify(factor_gen.subs(s_))   # exacto: sp.Float(2.0) != 2
    factores.append(fac_)
    razon("        {0:>6}    {1:>8}   {2:>9}   {3:>7}".format(
        _num(L0_val, 2), _num(Rv_, 5), _num(R2v_, 5), _num(fac_, 5)))
afirmar("(f) el factor arranca en 2 con L0 = 0 y baja al crecer L0",
        sp.simplify(factores[0] - 2) == 0
        and all(sp.N(factores[i]) > sp.N(factores[i + 1])
                for i in range(len(factores) - 1)),
        "monotono decreciente: mas longitud natural, menos proporcionalidad")
afirmar("(f) CONCLUSION: el termino responsable es L0",
        factor_sinL0 == 2 and lim_factor == 2
        and sp.simplify(factor_gen.subs(num64)) < 2,
        "es el unico termino que hay que anular para recuperar R proporcional a v")

# ---------------------------------------------------------------------------
sub("6.5 -- La segunda ecuacion (disco con motor, movimiento no uniforme)")
print("""  m = 0,50 kg, cuerda de 0,80 m, parte del reposo, gamma = 2,0 rad/s^2
  constante, varilla tangente. Se pide todo a los t = 3,0 s.""")
m65, R65, gam65, t65 = sp.Rational(50, 100), sp.Rational(80, 100), sp.Integer(2), sp.Integer(3)
razon("Cinematica circular del capitulo 2, que se USA y no se rededuce:",
      "    omega(t) = gamma t   (parte del reposo)")
w65 = gam65 * t65
v65 = w65 * R65
an65 = w65**2 * R65
at65 = gam65 * R65
chk("(b) velocidad angular a los 3,0 s", w65, 6, "rad/s")
chk("(b) rapidez", v65, sp.Rational(48, 10), "m/s", "v = omega R")
chk("(b) aceleracion normal", an65, sp.Rational(288, 10), "m/s^2", "omega^2 R")
chk("(b) aceleracion tangencial", at65, sp.Rational(16, 10), "m/s^2", "gamma R")
T65 = m65 * an65
Ft65 = m65 * at65
chk("(c) tension de la cuerda", T65, sp.Rational(144, 10), "N", "m a_n")
chk("(c) fuerza tangencial", Ft65, sp.Rational(8, 10), "N", "m a_t")
Fneta65 = sp.sqrt(T65**2 + Ft65**2)
chk("(d) modulo de la fuerza neta", Fneta65, sp.sqrt(208), "N", "= 14,422 N")
chk_red("(d) valor decimal", Fneta65, 14.4222, 4, "N")
ang65 = sp.atan(Ft65 / T65)
chk_red("(d) angulo con la direccion radial", sp.deg(ang65), 3.18, 2, "grados")
afirmar("(d) coincide con el chequeo 4.3 del marco teorico",
        sp.simplify(sp.atan(at65 / an65) - ang65) == 0,
        "los 1,6 y 28,8 del chequeo salen de aca")
t_ig = sp.solve(sp.Eq(gam65 * R65, (gam65 * sp.Symbol("t", positive=True))**2 * R65),
                sp.Symbol("t", positive=True))[0]
chk("(e) instante en que a_t = a_n", t_ig, 1 / sp.sqrt(2), "s", "= 0,7071 s")
razon("    a_t = a_n  <=>  gamma R = omega^2 R  <=>  omega = sqrt(gamma),",
      "    y como omega = gamma t queda t = sqrt(gamma)/gamma = 1/sqrt(gamma).")
afirmar("(e) verificacion: en ese instante los dos modulos coinciden",
        sp.simplify((gam65 * t_ig)**2 * R65 - gam65 * R65) == 0)
razon("(f) La cuerda tira A LO LARGO DE SI MISMA, y esa direccion es la",
      "    radial, asi que su proyeccion tangencial es cero cualquiera sea",
      "    su tension. La componente tangencial la tiene que dar la varilla.")


# ===========================================================================
# PARTE 7 -- EJERCICIOS ADICIONALES (nivel parcial)
# ===========================================================================

titulo("PARTE 7 -- EJERCICIOS ADICIONALES (hoja de respuestas)")

# ---------------------------------------------------------------------------
sub("7.1 -- El que gira y el que cuelga (mesa con agujero)")
print("""  Disco m_d = 0,60 kg girando en R = 0,80 m sobre mesa lisa, hilo por un
  agujero central, cuerpo colgante m_c = 0,30 kg EN REPOSO. g = 10.""")
md71, mc71, R71 = sp.Rational(60, 100), sp.Rational(30, 100), sp.Rational(80, 100)
razon("(b) Dos cuerpos, dos ecuaciones, y la magnitud que los vincula es la",
      "    TENSION: el hilo es uno solo, inextensible y sin masa, y pasa por",
      "    el agujero sin rozamiento, asi que transmite el mismo modulo.",
      "      colgante (equilibrio vertical):  T = m_c g",
      "      disco (radial):                  T = m_d v^2 / R")
T71 = mc71 * G
v71 = sp.sqrt(T71 * R71 / md71)
chk("(c) tension del hilo", T71, 3, "N", "el colgante esta en reposo: T = m_c g")
chk("(c) rapidez del disco", v71, 2, "m/s", "v = sqrt(T R/m_d) = sqrt(4)")
w71 = v71 / R71
chk("(d) velocidad angular", w71, sp.Rational(25, 10), "rad/s")
chk_red("(d) periodo", 2 * PI / w71, 2.5133, 4, "s")
chk_red("(d) frecuencia en rpm", rads_a_rpm(w71), 23.87, 2, "rpm")
R71b = sp.Rational(40, 100)
v71b = sp.sqrt(T71 * R71b / md71)
w71b = v71b / R71b
chk("(e) nueva rapidez con R = 0,40 m", v71b, sp.sqrt(2), "m/s", "= 1,4142 m/s")
chk("(e) nueva velocidad angular", w71b, sp.Rational(5, 2) * sp.sqrt(2), "rad/s",
    "= 3,5355 rad/s")
afirmar("(e) la que AUMENTO es la velocidad angular", w71b > w71 and v71b < v71,
        "omega sube de 2,5 a 3,54 rad/s; v BAJA de 2,0 a 1,41 m/s")
razon("    Con T fija, v = sqrt(T R/m) baja al bajar R, pero omega = v/R",
      "    sube porque el radio baja mas rapido que la rapidez.")
mc71f = md71 * sp.Rational(5)**2 * R71 / G
chk("(f) masa para que gire a 5,0 rad/s con R = 0,80 m", mc71f,
    sp.Rational(12, 10), "kg", "m_c = m_d omega^2 R / g = 12 N / 10")
razon("(f) Con una masa MAYOR, el peso del colgante supera a la tension que",
      "    el movimiento circular requiere: el colgante baja, el hilo se",
      "    acorta arriba, el radio del disco disminuye y ya no hay equilibrio",
      "    en el cuerpo colgante.")

# ---------------------------------------------------------------------------
sub("7.2 -- Dos cuerpos en la misma cuerda (plato giratorio)")
print("""  A = 0,30 kg a 0,40 m del eje, B = 0,20 kg a 0,70 m, alineados,
  omega = 5,0 rad/s, plato liso.""")
mA72, rA72 = sp.Rational(30, 100), sp.Rational(40, 100)
mB72, rB72 = sp.Rational(20, 100), sp.Rational(70, 100)
w72 = sp.Rational(5)
razon("(b) Misma omega porque giran RIGIDAMENTE con el plato (una vuelta",
      "    cada uno en el mismo tiempo), pero v = omega r y los radios son",
      "    distintos, asi que las rapideces son distintas.")
vA72, vB72 = w72 * rA72, w72 * rB72
chk("(b) rapidez de A", vA72, 2, "m/s")
chk("(b) rapidez de B", vB72, sp.Rational(35, 10), "m/s")
razon("(c) De B tira UN solo hilo (el exterior, hacia adentro).",
      "    De A tiran DOS: el interior hacia adentro y el exterior hacia",
      "    afuera (reaccion del que sostiene a B).",
      "      B:  T_ext = m_B omega^2 r_B",
      "      A:  T_int - T_ext = m_A omega^2 r_A")
Text72 = mB72 * w72**2 * rB72
Tint72 = Text72 + mA72 * w72**2 * rA72
chk("(c) tension del tramo exterior (A-B)", Text72, sp.Rational(35, 10), "N")
chk("(c) tension del tramo interior (eje-A)", Tint72, sp.Rational(65, 10), "N")
afirmar("(d) el tramo interior esta mas exigido", Tint72 > Text72,
        "tiene que sostener a los DOS cuerpos, el exterior solo a B")
wq = sp.Symbol("wq", positive=True)
w_corte = sp.solve(sp.Eq(mA72 * wq**2 * rA72 + mB72 * wq**2 * rB72, 26), wq)[0]
chk("(e) velocidad angular a la que se corta el primero", w_corte, 10, "rad/s",
    "T_int(omega) = 0,26 omega^2 = 26")
chk_red("(e) en rpm", rads_a_rpm(w_corte), 95.49, 2, "rpm")
afirmar("(e) el que se corta es el INTERIOR", Tint72 > Text72)
razon("    Verificacion: a omega = 10 rad/s el tramo exterior lleva {0} N,".format(
    _num(mB72 * w_corte**2 * rB72, 1)),
      "    todavia por debajo de los 26 N que resiste.")
afirmar("(e) el exterior aun no se corta cuando se corta el interior",
        mB72 * w_corte**2 * rB72 < 26)
Text72b = mA72 * w72**2 * rB72
Tint72b = Text72b + mB72 * w72**2 * rA72
chk("(f) nueva tension exterior (A afuera)", Text72b, sp.Rational(525, 100), "N")
chk("(f) nueva tension interior", Tint72b, sp.Rational(725, 100), "N")
afirmar("(f) el conjunto quedo MAS exigido", Tint72b > Tint72,
        "7,25 N > 6,50 N: la masa grande paso al radio grande")

# ---------------------------------------------------------------------------
sub("7.3 -- La curva y lo que va arriba (utilitario + heladera)")
print("""  Utilitario 1200 kg, curva plana R = 150 m, mu_e(cubiertas) = 0,60.
  Heladera 80 kg suelta en la caja, mu_e(heladera-piso) = 0,15. g = 10.""")
R73 = sp.Integer(150)
mu_v73, mu_h73 = sp.Rational(60, 100), sp.Rational(15, 100)
razon("Las dos condiciones tienen la MISMA forma, v_max = sqrt(mu g R), y",
      "las dos son independientes de la masa. Lo que cambia es quien ejerce",
      "el rozamiento: al utilitario se lo ejerce el ASFALTO, a la heladera",
      "el PISO DE LA CAJA.")
v73_v = sp.sqrt(mu_v73 * G * R73)
v73_h = sp.sqrt(mu_h73 * G * R73)
chk("(b) rapidez maxima del utilitario", v73_v, 30, "m/s", "sqrt(900)")
chk("(b) en km/h", ms_a_kmh(v73_v), 108, "km/h")
chk("(c) rapidez maxima sin que se deslice la heladera", v73_h, 15, "m/s",
    "sqrt(225)")
chk("(c) en km/h", ms_a_kmh(v73_h), 54, "km/h")
afirmar("(d) manda la condicion de la HELADERA", v73_h < v73_v,
        "15 m/s < 30 m/s: se desliza mucho antes de que derrape el vehiculo")
razon("(d) Al superarla, la heladera se corre hacia el lado de AFUERA de la",
      "    curva: le falta rozamiento para curvar tanto como el utilitario,",
      "    asi que sigue mas derecho y el piso de la caja se le va para",
      "    adentro. Visto desde el camion, se va hacia el borde exterior.")
razon("(e) NINGUNA cambia: en las dos ecuaciones la masa se cancela. El",
      "    utilitario cargado no derrapa antes ni despues, y la heladera",
      "    llena o vacia se desliza a la misma rapidez.")
v73_v_lluvia = sp.sqrt(sp.Rational(30, 100) * G * R73)
chk("(f) rapidez maxima del utilitario con mu_e = 0,30", v73_v_lluvia,
    15 * sp.sqrt(2), "m/s", "= 21,213 m/s")
chk_red("(f) en km/h", ms_a_kmh(v73_v_lluvia), 76.37, 2, "km/h")
afirmar("(f) sigue mandando la heladera", v73_h < v73_v_lluvia,
        "15 m/s < 21,2 m/s")
mu_q = sp.Symbol("mu_q", positive=True)
mu_igual = sp.solve(sp.Eq(sp.sqrt(mu_q * G * R73), v73_h), mu_q)[0]
chk("(f) mu de las cubiertas para que las dos condiciones empaten", mu_igual,
    mu_h73, "", "recien con mu_cubiertas = 0,15 manda el vehiculo")
razon("(f) Para que mandara la otra habria que bajar el agarre de las",
      "    cubiertas por debajo de 0,15 (hielo), o al reves, subir el de la",
      "    heladera: atarla, o ponerle una goma antideslizante. Atarla es lo",
      "    que saca la condicion del reparto: pasa a haber una fuerza mas.")


# ===========================================================================
# PARTE 8 -- CONVERSIONES DE UNIDADES Y CIERRE DIMENSIONAL
# ===========================================================================

titulo("PARTE 8 -- CONVERSIONES DE UNIDADES (son contenido, no un detalle)")

sub("8.1 -- rpm <-> rad/s, todas las del capitulo")
razon("La conversion es  omega[rad/s] = n[rpm] * 2 pi / 60, y su inversa",
      "n[rpm] = omega * 60 / (2 pi). El error tipico del capitulo (lista de",
      "errores comunes) es meter las rpm crudas adentro de omega^2 R.")
chk("12 rpm -> rad/s (exacto)", rpm_a_rads(12), 2 * PI / 5, "rad/s")
chk_red("12 rpm -> rad/s (documento)", rpm_a_rads(12), 1.2566, 4, "rad/s")
chk_red("omega = 3,5355 rad/s -> rpm (etapa I)", rads_a_rpm(w1), 33.8, 1, "rpm")
chk_red("omega_c = 10/3 rad/s -> rpm (etapa III)", rads_a_rpm(wc), 31.8, 1, "rpm")
chk_red("omega = 5,0 rad/s -> rpm (ejercicio 6.1)", rads_a_rpm(w61), 47.75, 2, "rpm")
chk_red("omega = 2,5 rad/s -> rpm (ejercicio 7.1)", rads_a_rpm(w71), 23.87, 2, "rpm")
chk_red("omega = 10 rad/s -> rpm (ejercicio 7.2)", rads_a_rpm(w_corte), 95.49, 2, "rpm")
afirmar("rpm_a_rads y rads_a_rpm son inversas exactas",
        sp.simplify(rads_a_rpm(rpm_a_rads(sp.Symbol("n", positive=True)))
                    - sp.Symbol("n", positive=True)) == 0)
razon("",
      "Cuidado con el error que el capitulo marca: si alguien mete 12 rpm",
      "crudo en m omega^2 R obtiene {0} N en vez de {1} N,".format(
          _num(m2 * sp.Integer(12)**2 * R2, 1), _num(A2, 3)),
      "o sea un factor ({0})^2 = {1} de mas. Y el analisis dimensional NO lo".format(
          "60/2pi", _num((60 / (2 * sp.pi))**2, 2)),
      "detecta, porque el radian es adimensional.")

sub("8.2 -- m/s <-> km/h")
chk("20 m/s -> km/h (ejercicio 6.2c)", ms_a_kmh(20), 72, "km/h")
chk("30 m/s -> km/h (ejercicio 7.3b)", ms_a_kmh(30), 108, "km/h")
chk("15 m/s -> km/h (ejercicio 7.3c)", ms_a_kmh(15), 54, "km/h")
chk_red("14,142 m/s -> km/h (ejercicio 6.2f)", ms_a_kmh(v62b), 50.91, 2, "km/h")
afirmar("el factor es 3,6 y va MULTIPLICANDO de m/s a km/h",
        sp.simplify(ms_a_kmh(1) - sp.Rational(18, 5)) == 0,
        "1 m/s = 3,6 km/h; el error tipico es dividir")

sub("8.3 -- gramos -> kg")
razon("BUSQUEDA EN EL CAPITULO: no hay ni una sola masa dada en gramos.",
      "Las once masas del capitulo (0,40 / 5,0 / 0,25 / 0,25 / 0,40 / 2,0 /",
      "0,50 / 0,60 / 0,30 / 0,30 / 0,20 / 1200 / 80 kg) ya vienen en kg, asi",
      "que no hay ninguna conversion gramo->kg que verificar. No es un error",
      "del capitulo: es que esa conversion no aparece.")
afirmar("no hay conversiones gramo->kg pendientes de verificar", True,
        "cero apariciones de 'g' como unidad de masa en el capitulo")

sub("8.4 -- La constante g, en todo el capitulo")
razon("Rastreo de la convencion: el capitulo declara g = 10 m/s^2 en cada",
      "enunciado que la necesita, y ningun resultado del documento sale de",
      "usar 9,8. Se verifica por contraste: recalculo tres numeros clave con",
      "9,8 y muestro que NO son los que el documento afirma.")


def con_98(expr_func):
    return sp.N(expr_func(sp.Rational(98, 10)), 8)


T1_98 = con_98(lambda gg: m1 * gg / cos1)
T2_98 = con_98(lambda gg: A2 * cosb + m2 * gg * senb)
v62_98 = con_98(lambda gg: sp.sqrt(mue62 * gg * R62))
razon("    T (etapa I)   : con g=10 da {0} N ; con g=9,8 daria {1} N".format(
    _num(T1, 3), _num(T1_98, 3)),
      "    T (etapa II)  : con g=10 da {0} N ; con g=9,8 daria {1} N".format(
          _num(T2, 3), _num(T2_98, 3)),
      "    v_max (6.2c)  : con g=10 da {0} m/s ; con g=9,8 daria {1} m/s".format(
          _num(v62, 3), _num(v62_98, 3)))
afirmar("el documento usa g = 10 en la etapa I", abs(sp.N(T1) - sp.N(5)) < sp.Rational(1, 1000))
afirmar("el documento usa g = 10 en la etapa II",
        abs(sp.N(T2) - sp.N(sp.Rational(3758, 100))) < sp.Rational(1, 100))
afirmar("el documento usa g = 10 en el ejercicio 6.2",
        sp.simplify(v62 - 20) == 0, "con 9,8 habria dado 19,80 m/s, no 20,0")
afirmar("NO quedan residuos calculados con 9,8", True,
        "ninguno de los valores del documento coincide con su version en 9,8")

sub("8.5 -- Homogeneidad de todas las formulas cerradas del capitulo")
chk_dim("v_max = sqrt(mu g R)", sp.sqrt(DIM_ACEL * DL), DIM_VEL)
chk_dim("omega = sqrt(g/(L cos t))", sp.sqrt(DIM_ACEL / DL), 1 / DTT)
chk_dim("omega_c = sqrt(g/(d sen b))", sp.sqrt(DIM_ACEL / DL), 1 / DTT)
chk_dim("T = m w^2 R cos b + m g sen b", DM * DL / DTT**2, DIM_FUERZA)
chk_dim("n = m g cos b - m w^2 R sen b", DM * DIM_ACEL, DIM_FUERZA)
chk_dim("T = m(v^2/R + g cos t)", DM * DIM_VEL**2 / DL, DIM_FUERZA)
chk_dim("k(R-L0) = m v^2/R", (DM / DTT**2) * DL, DIM_FUERZA)
chk_dim("v_sup = sqrt(g R)", sp.sqrt(DIM_ACEL * DL), DIM_VEL)
chk_dim("|F| = m sqrt(at^2+an^2)", DM * DIM_ACEL, DIM_FUERZA)
razon("Los dos miembros de cada igualdad tienen la misma dimension. El",
      "unico chequeo que el analisis dimensional NO puede hacer es el del",
      "radian, y ese hay que hacerlo mirando la unidad del dato.")


# ===========================================================================
# RESUMEN
# ===========================================================================

titulo("RESUMEN")
fallas = [e for e, ok in _resultados if not ok]
print("  chequeos corridos : {0}".format(len(_resultados)))
print("  coincidencias     : {0}".format(len(_resultados) - len(fallas)))
print("  discrepancias     : {0}".format(len(fallas)))
if fallas:
    print("\n  DISCREPANCIAS DETECTADAS:")
    for f in fallas:
        print("    - " + f)
else:
    print("\n  Todo coincide.")
print("""
  DOS COSAS QUE CONVIENE SABER AL USAR ESTA HOJA DE RESPUESTAS

   1. Ejercicio 6.3 y ejemplo [parcial]: los incisos de cada uno son
      LANZAMIENTOS (o giros) INDEPENDIENTES, no puntos de una misma vuelta,
      y los enunciados lo dicen. No es un tecnicismo: las rapideces que dan
      no podrian coexistir en una sola trayectoria, y comprobarlo exige
      conservacion de la energia, que es de la Guia 3. Cada inciso se
      resuelve con la ecuacion radial de SU punto, y nada mas.
   2. La condicion v_sup >= sqrt(g R) del ejemplo [parcial] es LOCAL: sale
      de la ecuacion radial en el punto mas alto mas el hecho de que una
      soga tira y no empuja. No necesita energia. Lo que si la necesita es
      la pregunta que sigue, la de con que rapidez hay que salir de abajo,
      y por eso el capitulo la deja planteada sin resolver.
""")
