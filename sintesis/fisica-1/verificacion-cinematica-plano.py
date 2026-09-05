# -*- coding: utf-8 -*-
"""
================================================================================
 VERIFICACION INDEPENDIENTE — Cinematica en el plano (Fisica 1, Guia 1)
 vectores, tiro parabolico y movimiento circular
================================================================================

 Que es esto
 -----------
 Este archivo resuelve, desde cero y con sympy, todo lo que el capitulo de
 Cinematica en el plano afirma: las deducciones simbolicas del marco teorico
 (derivada de un vector, descomposicion tangencial/normal, la tabla entera del
 tiro de proyectil, el movimiento circular en cartesianas y en polares), la
 coherencia geometrica de las tres figuras TikZ, y los resultados numericos de
 los tres ejemplos y de los nueve ejercicios.

 Para que te sirve a vos
 -----------------------
 1. Es la hoja de respuestas de los ejercicios del capitulo. El apunte los
    plantea sin resolverlos; aca estan resueltos y con el camino a la vista.
 2. Es una plantilla de autoevaluacion. Resolve el ejercicio a mano, corre esto,
    y compara. Si no coincide, el bloque correspondiente te muestra el paso
    intermedio donde mirar.
 3. Cada bloque esta escrito para que cambies los datos y lo vuelvas a correr
    con los numeros de tu practico.

 Como se corre
 -------------
     python verificacion-cinematica-plano.py

 Requiere sympy y nada mas. Donde el enunciado lo fija, g = 10 m/s^2 (valor de
 la catedra). Las deducciones del marco teorico se hacen con g, v0 y alpha
 genericos y recien despues se reemplaza, para poder ver que resultados NO
 dependen de los numeros.

 Regla de este archivo: se resuelve SIEMPRE desde el enunciado. El valor que
 afirma el borrador entra unicamente como segundo argumento de check(), nunca
 como insumo de la cuenta.
================================================================================
"""

import sys
import sympy as sp

# La consola de Windows no siempre viene en utf-8; esto evita que los acentos
# rompan la salida.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ------------------------------------------------------------------ utilidades

FALLAS = []
AVISOS = []


def check(etiqueta, obtenido, esperado, tol=1e-6):
    """Compara lo que calculo este script contra lo que dice el documento.

    'obtenido'  -> lo que sale de resolver el ejercicio aca, sin mirar el texto.
    'esperado'  -> el valor tal como figura en el borrador del capitulo.
    """
    def nrm(z):
        if isinstance(z, (str, bool)):
            return z
        if isinstance(z, (list, tuple, sp.Matrix)):
            return sp.Matrix(list(z))
        if isinstance(z, float) or (hasattr(z, 'is_Float') and z.is_Float):
            return sp.Float(z)          # los decimales se comparan como decimales
        try:
            return sp.nsimplify(z)
        except Exception:
            return sp.sympify(z)

    def cero(dif):
        """True si 'dif' es cero: primero simbolicamente, y si la expresion no
        es numerica (tiene derivadas o funciones sin evaluar), por tolerancia."""
        d = sp.simplify(dif)
        if d == 0:
            return True
        try:
            return abs(complex(sp.N(d))) < tol
        except (TypeError, ValueError):
            return False            # queda simbolico y no nulo -> es discrepancia

    o, e = nrm(obtenido), nrm(esperado)
    if isinstance(o, (str, bool)) or isinstance(e, (str, bool)):
        ok = (str(o) == str(e))
    elif isinstance(o, sp.Matrix) or isinstance(e, sp.Matrix):
        ok = (sp.Matrix(o).shape == sp.Matrix(e).shape and
              all(cero(p - q) for p, q in zip(sp.Matrix(o), sp.Matrix(e))))
    else:
        ok = cero(o - e)
    marca = "OK  " if ok else "MAL "
    fmt = (lambda z: list(z)) if isinstance(o, sp.Matrix) else (lambda z: z)
    print(f"   [{marca}] {etiqueta}: calculado = {fmt(o)}"
          f"   |  documento = {fmt(e)}")
    if not ok:
        FALLAS.append(etiqueta)
    return ok


def aviso(etiqueta, texto):
    """Observacion que no es un error numerico pero conviene que la vea el
    critico-calidad: notacion, hipotesis implicita, caso degenerado."""
    print(f"   [AVISO] {etiqueta}: {texto}")
    AVISOS.append(f"{etiqueta}: {texto}")


def titulo(txt):
    print("\n" + "=" * 78)
    print(txt)
    print("=" * 78)


def sub(txt):
    print("\n-- " + txt)


def dato(txt):
    print("    " + txt)


# ------------------------------------------------------- algebra vectorial 2D
# Un vector del plano es una tupla (Ax, Ay) de expresiones sympy. Estas cuatro
# funciones son todo lo que hace falta; no se usa nada mas exotico.

def vec(ax, ay):
    return (sp.sympify(ax), sp.sympify(ay))


def dot(A, B):
    """Producto escalar: A.B = Ax Bx + Ay By."""
    return sp.simplify(A[0] * B[0] + A[1] * B[1])


def norm(A):
    """Modulo: |A| = sqrt(A.A), por Pitagoras."""
    return sp.sqrt(sp.simplify(dot(A, A)))


def cruz(A, B):
    """Ax By - Ay Bx. Vale cero exactamente cuando A y B son paralelos:
    es el criterio de paralelismo del bloque de producto escalar."""
    return sp.simplify(A[0] * B[1] - A[1] * B[0])


def esc(k, A):
    return (sp.simplify(k * A[0]), sp.simplify(k * A[1]))


def suma(A, B):
    return (sp.simplify(A[0] + B[0]), sp.simplify(A[1] + B[1]))


def resta(A, B):
    return (sp.simplify(A[0] - B[0]), sp.simplify(A[1] - B[1]))


def descomponer(A, V):
    """Descompone el vector A en su parte paralela a V (tangencial) y su parte
    perpendicular (normal). Es EXACTAMENTE la receta del bloque 5:
        a_t (escalar) = a . v_gorro
        a_t (vector)  = (a . v_gorro) v_gorro
        a_n (vector)  = a - a_t (vector)
    Devuelve (a_t_escalar, a_t_vector, a_n_vector).
    """
    mv = norm(V)
    vgorro = esc(1 / mv, V)
    at_esc = dot(A, vgorro)
    at_vec = esc(at_esc, vgorro)
    an_vec = resta(A, at_vec)
    return sp.simplify(at_esc), at_vec, an_vec


def num(x, d=4):
    return sp.N(x, 15).round(d)


# Simbolos globales
t, tau = sp.symbols('t tau', real=True)
g, v0, h, R = sp.symbols('g v_0 h R', positive=True)
alpha = sp.symbols('alpha', positive=True)
w, gam = sp.symbols('omega gamma', real=True)


# =============================================================================
# PARTE I — LAS DEDUCCIONES SIMBOLICAS DEL MARCO TEORICO
# =============================================================================

def p1_derivar_un_vector():
    titulo("I.1  Derivar un vector es derivar cada componente (bloque 4)")
    dato("El texto lo deduce del cociente incremental sacando factor comun los")
    dato("versores, y avisa que el paso se apoya en que la base NO depende de t.")
    dt = sp.symbols('Delta_t', positive=True)
    # Se toma un par de funciones de movimiento con coeficientes simbolicos:
    # el limite se calcula de verdad y el resultado sigue siendo generico.
    p = sp.symbols('p0:4', real=True)
    q = sp.symbols('q0:4', real=True)
    x = p[0] + p[1] * t + p[2] * t**2 + p[3] * t**3
    y = q[0] + q[1] * t + q[2] * t**2 + q[3] * t**3

    sub("limite del cociente incremental en cada componente")
    coc_x = sp.expand((x.subs(t, t + dt) - x) / dt)
    coc_y = sp.expand((y.subs(t, t + dt) - y) / dt)
    dato("El paso clave del texto es sacar factor comun igorro y jgorro: se puede")
    dato("porque son LOS MISMOS versores en los dos instantes. Hecho eso, quedan")
    dato("dos limites escalares independientes, uno por componente:")
    vx = sp.limit(coc_x, dt, 0)
    vy = sp.limit(coc_y, dt, 0)
    check("vx = dx/dt", sp.expand(vx), sp.expand(sp.diff(x, t)))
    check("vy = dy/dt", sp.expand(vy), sp.expand(sp.diff(y, t)))
    check("a = d2r/dt2 (componente x)", sp.expand(sp.diff(vx, t)),
          sp.expand(sp.diff(x, t, 2)))
    check("a = d2r/dt2 (componente y)", sp.expand(sp.diff(vy, t)),
          sp.expand(sp.diff(y, t, 2)))
    dato("Si la base dependiera de t habria que sumarle a cada componente el")
    dato("termino que sale de derivar el versor. Es exactamente lo que pasa en")
    dato("el bloque 10, con la base polar, y se verifica mas abajo.")

    sub("contraejemplo del bloque 1: dos senos NO hacen un circulo")
    Rr, om = sp.symbols('R_c omega_c', positive=True)
    xs = Rr * sp.sin(om * t)
    ys = Rr * sp.sin(om * t)
    check("y = x (es un segmento, no una circunferencia)", sp.simplify(ys - xs), 0)
    dato("y el segmento va de (-R,-R) a (R,R) porque sen vive entre -1 y 1.")


def p1_tangencial_y_normal():
    titulo("I.2  a_t, a_n, y las dos afirmaciones del bloque 5")
    ax, ay, vx, vy = sp.symbols('a_x a_y v_x v_y', real=True)
    A = vec(ax, ay)
    V = vec(vx, vy)
    at_esc, at_vec, an_vec = descomponer(A, V)

    sub("(1) a_t + a_n reconstruye a, por construccion")
    check("a_t + a_n = a  (x)", suma(at_vec, an_vec)[0], ax)
    check("a_t + a_n = a  (y)", suma(at_vec, an_vec)[1], ay)

    sub("(2) a_n es perpendicular a v (el renglon que hace el texto)")
    check("a_n . v = 0", sp.simplify(dot(an_vec, V)), 0)

    sub("(3) la forma en componentes que el texto escribe para a_t vector")
    #    a_t = (ax vx + ay vy)/(vx^2+vy^2) * (vx, vy)
    forma_texto = esc((ax * vx + ay * vy) / (vx**2 + vy**2), V)
    check("a_t vector, forma del texto (x)", sp.simplify(at_vec[0] - forma_texto[0]), 0)
    check("a_t vector, forma del texto (y)", sp.simplify(at_vec[1] - forma_texto[1]), 0)

    sub("(4) |a| = sqrt(a_t^2 + a_n^2)  <-- afirmacion explicita del bloque 5")
    mod_a = norm(A)
    mod_at = sp.Abs(at_esc)
    mod_an = norm(an_vec)
    dif = sp.simplify(mod_at**2 + mod_an**2 - mod_a**2)
    check("a_t^2 + a_n^2 - |a|^2 = 0 (identico en ax,ay,vx,vy)", dif, 0)
    dato("Se comprueba tambien numericamente en un caso al azar, para descartar")
    dato("que la simplificacion simbolica este escondiendo un signo:")
    sust = {ax: sp.Rational(-3, 2), ay: 7, vx: 5, vy: sp.Rational(-11, 4)}
    check("Pitagoras en un caso numerico",
          sp.simplify((mod_at**2 + mod_an**2).subs(sust)),
          sp.simplify((mod_a**2).subs(sust)))
    dato("y que sumar los modulos da SIEMPRE de mas (salvo si uno es nulo):")
    dato(f"    |a_t|+|a_n| = {num((mod_at + mod_an).subs(sust))}"
         f"   vs   |a| = {num(mod_a.subs(sust))}")

    sub("(5) d|v|/dt = a_t  <-- la otra afirmacion explicita del bloque 5")
    #    Se hace con v(t) generica, no con vx,vy constantes.
    vxt = sp.Function('v_x')(t)
    vyt = sp.Function('v_y')(t)
    rapidez = sp.sqrt(vxt**2 + vyt**2)
    d_rapidez = sp.simplify(sp.diff(rapidez, t))
    # a_t calculado con la definicion: a . v_gorro
    at_def = sp.simplify((sp.diff(vxt, t) * vxt + sp.diff(vyt, t) * vyt) / rapidez)
    check("d|v|/dt = a . v_gorro", sp.simplify(d_rapidez - at_def), 0)
    dato("Corolario que el texto usa: rapidez constante  <=>  a_t = 0.")
    dato("Y trayectoria recta => la direccion de v no cambia => a_n = 0.")


def p1_tabla_tiro():
    titulo("I.3  La tabla entera del bloque 7, deducida (no copiada)")
    dato("Punto de partida: a = -g jgorro, r0 = h jgorro, v0 = (v0 cos A, v0 sen A).")
    dato("Todo lo demas sale de integrar dos veces y despejar.")

    A = vec(0, -g)
    v0v = vec(v0 * sp.cos(alpha), v0 * sp.sin(alpha))
    r0v = vec(0, h)

    # Integracion explicita con las CUATRO constantes, como manda el bloque 6.
    C1x, C1y, C2x, C2y = sp.symbols('C_1x C_1y C_2x C_2y', real=True)
    vx = sp.integrate(A[0], t) + C1x
    vy = sp.integrate(A[1], t) + C1y
    solC1 = sp.solve([sp.Eq(vx.subs(t, 0), v0v[0]), sp.Eq(vy.subs(t, 0), v0v[1])],
                     [C1x, C1y], dict=True)[0]
    vx, vy = vx.subs(solC1), vy.subs(solC1)
    xx = sp.integrate(vx, t) + C2x
    yy = sp.integrate(vy, t) + C2y
    solC2 = sp.solve([sp.Eq(xx.subs(t, 0), r0v[0]), sp.Eq(yy.subs(t, 0), r0v[1])],
                     [C2x, C2y], dict=True)[0]
    xx, yy = sp.expand(xx.subs(solC2)), sp.expand(yy.subs(solC2))

    sub("resultado de la doble integracion (4 constantes, 2 por eje)")
    dato(f"    v(t) = ({vx},  {vy})")
    dato(f"    r(t) = ({xx},  {yy})")
    check("x(t) = v0 cos(A) t", xx, v0 * sp.cos(alpha) * t)
    check("y(t) = h + v0 sen(A) t - g t^2/2", yy,
          h + v0 * sp.sin(alpha) * t - g * t**2 / 2)

    sub("fila 1: instante de altura maxima, de imponer v_y = 0")
    tmax = sp.solve(sp.Eq(vy, 0), t)[0]
    check("t_max = v0 sen(A)/g", tmax, v0 * sp.sin(alpha) / g)

    sub("fila 2: altura maxima, reemplazando t_max en y(t)")
    ymax = sp.simplify(yy.subs(t, tmax))
    check("y_max = h + v0^2 sen^2(A)/(2g)", ymax,
          h + v0**2 * sp.sin(alpha)**2 / (2 * g))

    sub("fila 3: ecuacion de la trayectoria, despejando t = x/(v0 cos A)")
    X = sp.symbols('x', real=True)
    t_de_x = sp.solve(sp.Eq(xx, X), t)[0]
    y_de_x = sp.simplify(sp.expand(yy.subs(t, t_de_x)))
    esperado_traj = h + sp.tan(alpha) * X - g * X**2 / (2 * v0**2 * sp.cos(alpha)**2)
    check("y(x) = h + tan(A) x - g x^2/(2 v0^2 cos^2 A)",
          sp.simplify(y_de_x - esperado_traj), 0)

    sub("fila 4: alcance con h = 0 (se descarta la raiz x = 0 del lanzamiento)")
    raices0 = sp.solve(sp.Eq(yy.subs(h, 0), 0), t)
    tf0 = [r for r in raices0 if sp.simplify(r) != 0][0]
    xf0 = sp.simplify(xx.subs(t, tf0))
    check("x_f = v0^2 sen(2A)/g", sp.simplify(xf0 - v0**2 * sp.sin(2 * alpha) / g), 0)
    dato("y el optimo con h=0 es 45 grados porque sen(2A) se maximiza en 2A=90:")
    d_xf0 = sp.diff(xf0, alpha)
    check("d(x_f)/dA = 0 en A = 45 grados", sp.simplify(d_xf0.subs(alpha, sp.pi / 4)), 0)

    sub("fila 5: alcance con h >= 0 (raiz positiva de la cuadratica)")
    raices = sp.solve(sp.Eq(yy, 0), t)
    tf = [r for r in raices
          if sp.simplify(sp.N(r.subs({v0: 25, alpha: sp.rad(37), g: 10, h: 20}))) > 0][0]
    xf = sp.simplify(xx.subs(t, tf))
    esperado_xf = (v0**2 / g) * sp.cos(alpha) * (sp.sin(alpha) +
                  sp.sqrt(sp.sin(alpha)**2 + 2 * g * h / v0**2))
    dif_xf = sp.simplify(sp.N((xf - esperado_xf).subs(
        {v0: 25, alpha: sp.rad(37), g: 10, h: 20})))
    check("x_f (h>=0) coincide con la fila de la tabla", dif_xf, 0)
    #  con h=0 queda sqrt(sen^2 A), que vale sen A solo en el primer cuadrante:
    #  por eso se evalua en angulos concretos de lanzamiento en vez de simplificar.
    for adeg in [15, 30, 45, 60, 75]:
        check(f"la fila 5 se reduce a la fila 4 con h=0  [A={adeg} grados]",
              sp.N((esperado_xf.subs(h, 0) - v0**2 * sp.sin(2 * alpha) / g).subs(
                  {alpha: sp.rad(adeg), v0: 20, g: 10}), 12), 0, tol=1e-9)

    sub("fila 6: angulo optimo con h > 0, maximizando x_f respecto de A")
    #    Se deriva el alcance respecto de alpha y se resuelve numericamente
    #    para un h concreto; despues se compara contra la formula de la tabla.
    for (hh, vv, gg) in [(20, 25, 10), (5, 12, 10), (0, 30, 10)]:
        f_alc = esperado_xf.subs({h: hh, v0: vv, g: gg})
        raiz = sp.nsolve(sp.diff(f_alc, alpha), alpha, 0.7)
        formula = sp.atan(1 / sp.sqrt(1 + 2 * gg * hh / sp.Integer(vv)**2))
        check(f"A_op numerico vs tan(A_op)=1/sqrt(1+2gh/v0^2)  [h={hh}, v0={vv}]",
              sp.N(raiz, 12), sp.N(formula, 12), tol=1e-7)
    dato("Con h=0 la formula da tan(A)=1 -> 45 grados exactos, como dice la tabla.")

    sub("afirmacion suelta del bloque 7: en el angulo optimo, v0 . v_f = 0")
    #    Se verifica simbolicamente: se impone v0.vf=0, se despeja el angulo, y
    #    se compara con la formula del optimo.
    vf = (vx.subs(t, tf), vy.subs(t, tf))
    prod = sp.simplify(dot(v0v, vf))
    prod_op = prod.subs(alpha, sp.atan(1 / sp.sqrt(1 + 2 * g * h / v0**2)))
    for (hh, vv, gg) in [(20, 25, 10), (5, 12, 10), (0, 30, 10), (100, 40, 10)]:
        val = sp.N(prod_op.subs({h: hh, v0: vv, g: gg}), 20)
        check(f"v0 . v_f en el angulo optimo  [h={hh}, v0={vv}]",
              sp.N(val, 10), 0, tol=1e-6)
    dato("Confirmado: la perpendicularidad lanzamiento/llegada y el angulo optimo")
    dato("son la MISMA condicion, tal como afirma el texto.")

    sub("casos limite que el texto pide no leer como errores")
    check("A = 0  =>  t_max = 0", tmax.subs(alpha, 0), 0)
    check("A = 90 grados  =>  v_x = 0 (tiro vertical puro)",
          sp.simplify(vx.subs(alpha, sp.pi / 2)), 0)

    sub("la trampa fina: con viento HORIZONTAL, y_max sigue dando bien")
    axv = sp.symbols('a_x', real=True)
    y_con_viento = h + v0 * sp.sin(alpha) * t - g * t**2 / 2   # el eje y no se entera
    tmax_v = sp.solve(sp.Eq(sp.diff(y_con_viento, t), 0), t)[0]
    check("y_max con a_x != 0 = y_max con a_x = 0",
          sp.simplify(y_con_viento.subs(t, tmax_v) - ymax), 0)
    dato("Funciona porque a_x no aparece en y(t). Con una componente vertical")
    dato("extra la formula se rompe; se verifica al toque:")
    ay_extra = sp.symbols('a_ye', real=True)
    y2 = h + v0 * sp.sin(alpha) * t + (ay_extra - g) * t**2 / 2
    t2 = sp.solve(sp.Eq(sp.diff(y2, t), 0), t)[0]
    y2max = sp.simplify(y2.subs(t, t2))
    check("con a_y extra, y_max YA NO coincide (la diferencia no es cero)",
          sp.simplify(sp.simplify(y2max - ymax).subs(
              {ay_extra: 2, v0: 25, alpha: sp.rad(37), g: 10, h: 20})) != 0,
          True)


def p1_circular():
    titulo("I.4  Movimiento circular: bloque 8 y bloque 10")
    th = sp.Function('theta')(t)
    r = (R * sp.cos(th), R * sp.sin(th))

    sub("derivando r = R(cos O, sen O) con regla de la cadena")
    v = (sp.diff(r[0], t), sp.diff(r[1], t))
    a = (sp.diff(v[0], t), sp.diff(v[1], t))
    W = sp.diff(th, t)
    Gm = sp.diff(th, t, 2)
    u_rho = (sp.cos(th), sp.sin(th))
    u_th = (-sp.sin(th), sp.cos(th))

    check("u_rho . u_theta = 0", dot(u_rho, u_th), 0)
    check("|u_rho| = 1", norm(u_rho), 1)
    check("|u_theta| = 1", norm(u_th), 1)

    check("v = R w u_theta  (x)", sp.simplify(v[0] - R * W * u_th[0]), 0)
    check("v = R w u_theta  (y)", sp.simplify(v[1] - R * W * u_th[1]), 0)

    a_texto = suma(esc(R * Gm, u_th), esc(-R * W**2, u_rho))
    check("a = R gamma u_theta - R w^2 u_rho  (x)", sp.simplify(a[0] - a_texto[0]), 0)
    check("a = R gamma u_theta - R w^2 u_rho  (y)", sp.simplify(a[1] - a_texto[1]), 0)

    sub("la descomposicion sale YA hecha: la parte con gamma es tangencial")
    at_vec = esc(R * Gm, u_th)
    an_vec = esc(-R * W**2, u_rho)
    check("a_t . v = |a_t||v| (paralelos): a_t x v = 0", cruz(at_vec, v), 0)
    check("a_n . v = 0 (perpendicular)", sp.simplify(dot(an_vec, v)), 0)
    dato("y el signo menos de a_n dice que apunta CONTRA u_rho, o sea al centro.")

    sub("bloque 8: a_n = R w^2 = |v|^2/R = |v| w  son la misma cuenta")
    #    Aca es donde el enunciado del pipeline pide mirar con lupa.
    Wp = sp.symbols('omega_p', positive=True)      # caso w > 0
    modv = sp.simplify(R * Wp)                     # |v| = R|w|
    #  El texto (corregido) escribe la cadena cerrando en |v||w|, y su premisa
    #  como |w| = |v|/R. Se verifica que la cadena vale para CUALQUIER signo de w,
    #  que es justamente lo que la version con w pelada no cumplia.
    check("R w^2  vs  |v|^2/R  (w > 0)", sp.simplify(R * Wp**2 - modv**2 / R), 0)
    check("R w^2  vs  |v| |w|   (w > 0)", sp.simplify(R * Wp**2 - modv * sp.Abs(Wp)), 0)
    check("premisa: |w| = |v|/R  (w > 0)", sp.simplify(sp.Abs(Wp) - modv / R), 0)
    Wn = sp.symbols('omega_n', negative=True)
    modv_n = R * sp.Abs(Wn)
    dato("El caso que decide la correccion es w < 0 (giro horario):")
    dato(f"    R w^2 = {R * Wn**2} ;  |v| |w| = {sp.simplify(modv_n * sp.Abs(Wn))} ;"
         f"  |v| w = {sp.simplify(modv_n * Wn)}")
    check("R w^2 = |v|^2/R  tambien con w < 0",
          sp.simplify(R * Wn**2 - modv_n**2 / R), 0)
    check("R w^2 = |v| |w|  tambien con w < 0  <-- la forma corregida",
          sp.simplify(R * Wn**2 - modv_n * sp.Abs(Wn)), 0)
    check("premisa: |w| = |v|/R  tambien con w < 0",
          sp.simplify(sp.Abs(Wn) - modv_n / R), 0)
    check("en cambio |v| w (sin modulo) FALLA con w < 0: da el signo opuesto",
          sp.simplify((R * Wn**2 - modv_n * Wn).subs({R: 2, Wn: -3})), 36)
    dato("=> la cadena del texto, con |w| en la ultima forma y en el despeje que")
    dato("   la alimenta, es correcta para los dos sentidos de giro.")

    sub("bloque 8: r . v = 0 SOLO con el origen en el centro")
    check("con origen en el centro: r . v = 0", sp.simplify(dot(r, v)), 0)
    #    Ahora se corre el centro a (c, 0) y se ve que deja de valer.
    c = sp.symbols('c', positive=True)
    r2 = (c + R * sp.cos(th), R * sp.sin(th))
    v2 = (sp.diff(r2[0], t), sp.diff(r2[1], t))
    prod2 = sp.simplify(dot(r2, v2))
    dato(f"    con el centro en (c,0):  r . v = {prod2}")
    check("con el centro fuera del origen, r.v = -c R w sen(O)",
          sp.simplify(prod2 + c * R * W * sp.sin(th)), 0)
    dato("que NO es identicamente nulo: se anula solo cuando sen(O) = 0.")

    sub("bloque 10: la base polar depende de t y su derivada no es cero")
    check("d(u_rho)/dt = w u_theta  (x)",
          sp.simplify(sp.diff(u_rho[0], t) - W * u_th[0]), 0)
    check("d(u_rho)/dt = w u_theta  (y)",
          sp.simplify(sp.diff(u_rho[1], t) - W * u_th[1]), 0)
    check("d(u_theta)/dt = -w u_rho  (x)",
          sp.simplify(sp.diff(u_th[0], t) + W * u_rho[0]), 0)
    check("d(u_theta)/dt = -w u_rho  (y)",
          sp.simplify(sp.diff(u_th[1], t) + W * u_rho[1]), 0)
    #  se comparan los CUADRADOS: sympy no colapsa sqrt(D**2) a Abs(D) sin
    #  asumir el signo de D, y aca D = dtheta/dt puede ser de cualquier signo.
    du = (sp.diff(u_rho[0], t), sp.diff(u_rho[1], t))
    check("|d(u_rho)/dt|^2 = w^2  (o sea |w|, no 1: derivar no preserva el modulo)",
          sp.simplify(dot(du, du)), W**2)
    check("|d(u_theta)/dt|^2 = w^2", sp.simplify(dot(
          (sp.diff(u_th[0], t), sp.diff(u_th[1], t)),
          (sp.diff(u_th[0], t), sp.diff(u_th[1], t)))), W**2)

    sub("bloque 9: periodo del circular uniforme")
    w0 = sp.symbols('omega_0', positive=True)
    T_ = 2 * sp.pi / w0
    r_mcu = (R * sp.cos(w0 * t), R * sp.sin(w0 * t))
    check("r(t+T) = r(t)  (x)", sp.simplify(r_mcu[0].subs(t, t + T_) - r_mcu[0]), 0)
    check("r(t+T) = r(t)  (y)", sp.simplify(r_mcu[1].subs(t, t + T_) - r_mcu[1]), 0)
    check("T = 2 pi R / |v|", sp.simplify(T_ - 2 * sp.pi * R / (R * w0)), 0)
    check("f = w0/(2 pi)", sp.simplify(1 / T_ - w0 / (2 * sp.pi)), 0)


# =============================================================================
# PARTE II — COHERENCIA DE LAS TRES FIGURAS TIKZ CON SU ALGEBRA
# =============================================================================

def p2_figuras():
    titulo("II  Las tres figuras TikZ contra el algebra que ilustran")
    X = sp.symbols('x', real=True)

    # --------------------------------------------------------------- figura 1
    sub("FIGURA 1 (bloque 4): r, v y a sobre y = 3 - x^2/4 en x = 2")
    f = 3 - X**2 / 4
    P = (sp.Integer(2), f.subs(X, 2))
    check("el punto marcado (2,2) esta sobre la curva", P[1], 2)
    pend = sp.diff(f, X).subs(X, 2)
    check("pendiente de la tangente en x=2", pend, -1)
    dato("=> la tangente tiene direccion (1,-1), que es lo que el codigo asume.")

    # Lo que el .tex dibuja, leido de las coordenadas del tikzpicture:
    v_fig1 = resta(vec(sp.Rational(278, 100), sp.Rational(122, 100)), P)
    a_fig1 = resta(vec(sp.Rational(180, 100), sp.Rational(80, 100)), P)
    dato(f"    v dibujada = {v_fig1}     a dibujada = {a_fig1}")
    check("v dibujada es paralela a la tangente (1,-1)", cruz(v_fig1, vec(1, -1)), 0)
    check("a dibujada = (-0.2,-1.2) como dice el comentario del .tex",
          sp.Matrix(list(a_fig1)), sp.Matrix([sp.Rational(-2, 10), sp.Rational(-12, 10)]))
    # Y la descomposicion que el encabezado del .tex afirma para esa a:
    at_e, at_v, an_v = descomponer(a_fig1, vec(1, -1))
    check("a_t de la figura 1 = (0.5,-0.5)", sp.Matrix(list(at_v)),
          sp.Matrix([sp.Rational(1, 2), sp.Rational(-1, 2)]))
    check("a_n de la figura 1 = (-0.7,-0.7)", sp.Matrix(list(an_v)),
          sp.Matrix([sp.Rational(-7, 10), sp.Rational(-7, 10)]))
    check("a_t + a_n = a", sp.Matrix(list(suma(at_v, an_v))), sp.Matrix(list(a_fig1)))
    check("a apunta hacia adentro de la concavidad (a_y < pendiente*a_x)",
          sp.sign(sp.simplify(a_fig1[1] - pend * a_fig1[0])), -1)

    # --------------------------------------------------------------- figura 2
    sub("FIGURA 2 (bloque 5): el paralelogramo tangencial/normal en el mismo punto")
    dato("Las tres condiciones se exigen SIMULTANEAMENTE, como pide el gate.")
    v_f2 = resta(vec(sp.Rational(309, 100), sp.Rational(91, 100)), P)
    a_f2 = resta(vec(sp.Rational(172, 100), sp.Rational(32, 100)), P)
    at_f2 = resta(vec(sp.Rational(270, 100), sp.Rational(130, 100)), P)
    an_f2 = resta(vec(sp.Rational(102, 100), sp.Rational(102, 100)), P)
    dato(f"    v  = {v_f2}")
    dato(f"    a  = {a_f2}")
    dato(f"    a_t= {at_f2}")
    dato(f"    a_n= {an_f2}")

    # (i) suman
    check("(i)  a_t + a_n = a", sp.Matrix(list(suma(at_f2, an_f2))), sp.Matrix(list(a_f2)))
    # (ii) a_t paralela a la tangente (1,-1), y v tambien
    check("(ii) v dibujada es paralela a la tangente (1,-1)", cruz(v_f2, vec(1, -1)), 0)
    check("(ii) a_t es paralela a la tangente (1,-1)", cruz(at_f2, vec(1, -1)), 0)
    # (iii) a_n perpendicular a la tangente
    check("(iii) a_n . v = 0", dot(an_f2, v_f2), 0)
    check("(iii) a_n . tangente = 0", dot(an_f2, vec(1, -1)), 0)

    # y ademas: la descomposicion dibujada es LA que sale de la definicion
    at_e2, at_v2, an_v2 = descomponer(a_f2, v_f2)
    check("a_t dibujada = (a . v_gorro) v_gorro", sp.Matrix(list(at_v2)),
          sp.Matrix(list(at_f2)))
    check("a_n dibujada = a - a_t", sp.Matrix(list(an_v2)), sp.Matrix(list(an_f2)))

    # concavidad: la normal de la curva hacia el lado concavo
    # r(x) = (x, f(x)); la componente normal de r'' apunta al lado concavo.
    rpp = vec(0, sp.diff(f, X, 2).subs(X, 2))
    T = vec(1, pend)
    _, _, n_curva = descomponer(rpp, T)
    dato(f"    normal de curvatura de la trayectoria en x=2: {n_curva}  "
         f"(direccion (-1,-1))")
    check("a_n dibujada tiene el MISMO sentido que la normal de curvatura",
          sp.sign(dot(an_f2, n_curva)), 1)
    check("y ademas a_t va con el mismo sentido que v (el movil acelera)",
          sp.sign(dot(at_f2, v_f2)), 1)
    dato("Las tres condiciones se cumplen a la vez. Figura 2: coherente.")

    # el comentario del encabezado del .tex, aparte
    factor = sp.simplify(at_f2[0] / sp.Rational(1, 2))
    dato(f"    Nota: la figura 2 usa a = {factor} veces la a de la figura 1 "
         f"(misma direccion y sentido).")
    check("figura 2 = figura 1 escalada por un factor positivo (direccion identica)",
          cruz(a_f2, a_fig1), 0)
    dato("El comentario de cabecera (corregido) ya declara ese factor 1.4. Se")
    dato("verifica que el factor es exactamente 1.4 en las dos componentes:")
    check("factor de escala figura2/figura1 = 1.4 (componente x)",
          sp.simplify(a_f2[0] / a_fig1[0]), sp.Rational(14, 10))
    check("factor de escala figura2/figura1 = 1.4 (componente y)",
          sp.simplify(a_f2[1] / a_fig1[1]), sp.Rational(14, 10))

    # el paralelogramo punteado
    sub("el paralelogramo punteado cierra")
    P1 = vec(sp.Rational(270, 100), sp.Rational(130, 100))
    P2 = vec(sp.Rational(172, 100), sp.Rational(32, 100))
    P3 = vec(sp.Rational(102, 100), sp.Rational(102, 100))
    check("desde la punta de a_t, sumando a_n, se llega a la punta de a",
          sp.Matrix(list(suma(P1, an_f2))), sp.Matrix(list(P2)))
    check("desde la punta de a_n, sumando a_t, se llega a la punta de a",
          sp.Matrix(list(suma(P3, at_f2))), sp.Matrix(list(P2)))

    # --------------------------------------------------------------- figura 3
    sub("FIGURA 3 (bloque 7): tiro con a constante dibujada en tres puntos")
    p = 1 + sp.Rational(12, 10) * X - sp.Rational(3, 10) * X**2
    check("el lanzamiento (0,1) esta sobre la parabola", p.subs(X, 0), 1)
    xv = sp.solve(sp.Eq(sp.diff(p, X), 0), X)[0]
    check("el vertice esta en x = 2", xv, 2)
    check("el vertice esta en y = 2.2", p.subs(X, xv), sp.Rational(22, 10))
    ximp = max(sp.solve(sp.Eq(p, 0), X))
    check("el impacto esta en x = 4.71 (el domain del \\draw)",
          sp.N(ximp, 6), sp.Float("4.71"), tol=2e-3)
    check("el tercer punto (3.5, 1.525) esta sobre la parabola",
          p.subs(X, sp.Rational(35, 10)), sp.Rational(1525, 1000))

    # los tres vectores v dibujados vs la pendiente en cada punto
    puntos = [(sp.Integer(0), sp.Integer(1), (sp.Rational(54, 100), sp.Rational(165, 100))),
              (sp.Integer(2), sp.Rational(22, 10), (sp.Rational(285, 100), sp.Rational(22, 10))),
              (sp.Rational(35, 10), sp.Rational(1525, 1000),
               (sp.Rational(413, 100), sp.Rational(956, 1000)))]
    for (px, py, punta) in puntos:
        vv = resta(vec(*punta), vec(px, py))
        m_dibujo = sp.simplify(vv[1] / vv[0]) if vv[0] != 0 else sp.oo
        m_curva = sp.diff(p, X).subs(X, px)
        check(f"v dibujada en x={px} es tangente (pendiente)",
              sp.N(m_dibujo, 6), sp.N(m_curva, 6), tol=5e-3)
    dato("y las tres a dibujadas son (0,-0.8): mismo modulo, mismo sentido, hacia")
    dato("abajo, consistente con a = -g jgorro y con el eje +y hacia arriba.")
    for (px, py) in [(0, 1), (2, sp.Rational(22, 10)), (sp.Rational(35, 10), sp.Rational(1525, 1000))]:
        pass
    a_dib = [resta(vec(0, sp.Rational(2, 10)), vec(0, 1)),
             resta(vec(2, sp.Rational(14, 10)), vec(2, sp.Rational(22, 10))),
             resta(vec(sp.Rational(35, 10), sp.Rational(725, 1000)),
                   vec(sp.Rational(35, 10), sp.Rational(1525, 1000)))]
    for i, av in enumerate(a_dib, 1):
        check(f"a dibujada #{i} = (0,-0.8)", sp.Matrix(list(av)),
              sp.Matrix([0, sp.Rational(-8, 10)]))
    check("en el vertice v es horizontal y a vertical => a . v = 0",
          dot(resta(vec(sp.Rational(285, 100), sp.Rational(22, 10)), vec(2, sp.Rational(22, 10))),
              vec(0, sp.Rational(-8, 10))), 0)


# =============================================================================
# PARTE III — LOS TRES EJEMPLOS
# =============================================================================

def ejemplo_completo():
    titulo("III.1  EJEMPLO COMPLETO — pelota desde una terraza de 20 m")
    dato("Datos del enunciado: h = 20 m, v0 = 25 m/s, A = 37 grados,")
    dato("sen37 = 0.60, cos37 = 0.80, g = 10 m/s^2, sin aire.")
    H, V0, G = sp.Integer(20), sp.Integer(25), sp.Integer(10)
    S, C = sp.Rational(6, 10), sp.Rational(8, 10)

    sub("(a) montaje: descomposicion de v0")
    v0v = vec(V0 * C, V0 * S)
    check("v0 = (20, 15) m/s", sp.Matrix(list(v0v)), sp.Matrix([20, 15]))
    check("|v0| = 25 m/s (control del enunciado)", norm(v0v), 25)

    sub("(b)-(c) doble integracion de a = -g jgorro y especializacion")
    C1x, C1y, C2x, C2y = sp.symbols('C1x C1y C2x C2y', real=True)
    vx = sp.integrate(0, t) + C1x
    vy = sp.integrate(-G, t) + C1y
    s1 = sp.solve([sp.Eq(vx.subs(t, 0), v0v[0]), sp.Eq(vy.subs(t, 0), v0v[1])],
                  [C1x, C1y], dict=True)[0]
    vx, vy = vx.subs(s1), vy.subs(s1)
    xx = sp.integrate(vx, t) + C2x
    yy = sp.integrate(vy, t) + C2y
    s2 = sp.solve([sp.Eq(xx.subs(t, 0), 0), sp.Eq(yy.subs(t, 0), H)],
                  [C2x, C2y], dict=True)[0]
    xx, yy = sp.expand(xx.subs(s2)), sp.expand(yy.subs(s2))
    check("x(t) = 20 t", xx, 20 * t)
    check("y(t) = 20 + 15 t - 5 t^2", yy, 20 + 15 * t - 5 * t**2)

    sub("(d) altura maxima")
    tmax = sp.solve(sp.Eq(vy, 0), t)[0]
    check("t_max = 1.5 s", tmax, sp.Rational(3, 2))
    check("y_max = 31.25 m", yy.subs(t, tmax), sp.Rational(125, 4))
    check("v en el vertice = (20, 0) m/s",
          sp.Matrix([vx.subs(t, tmax), vy.subs(t, tmax)]), sp.Matrix([20, 0]))

    sub("(e) tiempo de vuelo y alcance")
    raices = sp.solve(sp.Eq(yy, 0), t)
    dato(f"    raices de y(t)=0: {raices}   (se descarta la negativa)")
    check("las dos raices son 4 y -1 s", sorted([sp.nsimplify(r) for r in raices]),
          [sp.Integer(-1), sp.Integer(4)])
    tf = max(raices)
    check("t_f = 4 s", tf, 4)
    check("alcance x_f = 80 m", xx.subs(t, tf), 80)

    sub("(f) velocidad de llegada")
    vf = (vx.subs(t, tf), vy.subs(t, tf))
    check("v_f = (20, -25) m/s", sp.Matrix(list(vf)), sp.Matrix([20, -25]))
    check("|v_f| = 32.02 m/s", sp.N(norm(vf), 6), sp.Float("32.02"), tol=5e-3)
    ang = sp.deg(sp.atan(sp.Rational(25, 20)))
    check("angulo bajo la horizontal = 51.34 grados", sp.N(ang, 6),
          sp.Float("51.34"), tol=5e-3)

    sub("(g) descomposicion tangencial y normal")
    A = vec(0, -G)
    at_v, _, an_v = descomponer(A, vec(20, 0))
    check("en el vertice a_t = 0", at_v, 0)
    check("en el vertice a_n = g = 10 m/s^2", norm(an_v), 10)
    #  El inciso (reescrito) pide los CUATRO pasos por separado. Se recorren en
    #  ese mismo orden, para que el archivo sirva de control paso a paso.
    dato("paso 1 - versor velocidad:")
    vgorro_f = esc(1 / norm(vf), vf)
    dato(f"    v_gorro = ({num(vgorro_f[0], 5)}, {num(vgorro_f[1], 5)})  (adimensional)")
    check("|v_gorro| = 1", sp.simplify(norm(vgorro_f)), 1)
    dato("paso 2 - componente ESCALAR tangencial, con signo:")
    at_f = dot(A, vgorro_f)
    dato(f"    a_t = a . v_gorro = {num(at_f, 5)} m/s^2  (positiva: gana rapidez)")
    dato("paso 3 - vector tangencial:")
    at_vf = esc(at_f, vgorro_f)
    dato(f"    a_t vector = a_t v_gorro = ({num(at_vf[0], 4)}, {num(at_vf[1], 4)}) m/s^2")
    dato("paso 4 - vector normal, RESTA ENTRE VECTORES:")
    an_vf = resta(A, at_vf)
    dato(f"    a_n vector = a - a_t vector = ({num(an_vf[0], 4)}, {num(an_vf[1], 4)}) m/s^2")
    #  los dos unicos numeros que el inciso reescrito expone:
    check("en el impacto a_t = 7.81 m/s^2 (componente escalar)", sp.N(at_f, 6),
          sp.Float("7.81"), tol=5e-3)
    check("en el impacto |a_n| = 6.25 m/s^2 (modulo)", sp.N(norm(an_vf), 6),
          sp.Float("6.25"), tol=5e-3)
    check("a_t es positiva (la pelota gana rapidez al caer)", sp.N(at_f) > 0, True)
    check("a_t vector + a_n vector = a", sp.Matrix(list(suma(at_vf, an_vf))),
          sp.Matrix(list(A)))
    check("a_n vector es perpendicular a v_f", dot(an_vf, vf), 0)
    check("control a_t^2 + a_n^2 = g^2 = 100 exacto",
          sp.simplify(at_f**2 + norm(an_vf)**2), 100)

    sub("(h) ecuacion de la trayectoria  <-- el punto en disputa: /80 vs /64")
    X = sp.symbols('x', real=True)
    t_de_x = sp.solve(sp.Eq(xx, X), t)[0]
    check("t = x/20", t_de_x, X / 20)
    y_de_x = sp.expand(yy.subs(t, t_de_x))
    dato(f"    y(x) = {y_de_x}")
    check("y(x) = 20 + 0.75 x - x^2/80", y_de_x, 20 + sp.Rational(3, 4) * X - X**2 / 80)
    check("y(80) = 0 con el denominador 80 (control del texto)", y_de_x.subs(X, 80), 0)
    y_alt = 20 + sp.Rational(3, 4) * X - X**2 / 64
    dato(f"    version del estilista con /64 evaluada en x=80: y = {y_alt.subs(X, 80)} m")
    check("el denominador 64 NO anula y en x=80 (da -20 m: 20 m bajo la vereda)",
          y_alt.subs(X, 80), -20)
    x_alt = max(sp.solve(sp.Eq(y_alt, 0), X))
    dato(f"    con /64 la pelota tocaria el suelo en x = {num(x_alt)} m, no en 80 m.")
    dato("VEREDICTO: el redactor tiene razon. El coeficiente es g/(2 v0^2 cos^2 A)")
    dato(f"    = 10/(2*625*0.64) = {sp.Rational(10, 2*625) / sp.Rational(64,100)} = 1/80.")
    check("g/(2 v0^2 cos^2 A) = 1/80",
          G / (2 * V0**2 * C**2), sp.Rational(1, 80))

    sub("(i) cierre: el mismo tiro con el angulo complementario, 53 grados")
    v0b = vec(V0 * S, V0 * C)      # sen53=0.80, cos53=0.60
    yb = H + v0b[1] * t - 5 * t**2
    tfb = max([r for r in sp.solve(sp.Eq(yb, 0), t) if sp.N(r) > 0])
    xfb = sp.simplify(v0b[0] * tfb)
    dato(f"    t_f(53 grados) = {num(tfb)} s ;  alcance = {num(xfb)} m")
    check("el alcance a 53 grados es DISTINTO del de 37 grados",
          sp.simplify(sp.N(xfb) - 80) != 0, True)
    dato("Confirmado lo que pide explicar el texto: con h>0 los complementarios")
    dato("ya no dan el mismo alcance, porque esa propiedad exige h = 0.")


def ejemplo_parcial_disco():
    titulo("III.2  EJEMPLO PARCIAL 1 — disco sobre hielo")
    dato("v0 = (6,8) m/s en el origen en t=0 ; a = (1.5,-2) m/s^2 constante.")
    v0v = vec(6, 8)
    A = vec(sp.Rational(3, 2), -2)

    sub("integracion (las cuatro constantes las fija el paso por el origen)")
    v = (v0v[0] + A[0] * t, v0v[1] + A[1] * t)
    r = (sp.integrate(v[0], t), sp.integrate(v[1], t))     # r(0) = 0
    check("v(t) = (6+1.5t, 8-2t)", sp.Matrix(list(v)),
          sp.Matrix([6 + sp.Rational(3, 2) * t, 8 - 2 * t]))
    check("r(t) = (6t+0.75t^2, 8t-t^2)", sp.Matrix(list(r)),
          sp.Matrix([6 * t + sp.Rational(3, 4) * t**2, 8 * t - t**2]))
    check("a NO es paralela a v0 => la trayectoria es una parabola",
          cruz(A, v0v) != 0, True)

    sub("la evaluacion en t = 0 que el texto deja resuelta")
    check("|v0| = 10 m/s", norm(v0v), 10)
    vgorro = esc(1 / norm(v0v), v0v)
    check("v_gorro = (0.6, 0.8)", sp.Matrix(list(vgorro)),
          sp.Matrix([sp.Rational(6, 10), sp.Rational(8, 10)]))
    at0, at0v, an0v = descomponer(A, v0v)
    check("a_t(0) = -0.7 m/s^2 (negativa: esta frenando)", at0, sp.Rational(-7, 10))
    check("|a| = 2.5 m/s^2", norm(A), sp.Rational(5, 2))
    check("a_n(0) = 2.4 m/s^2 por Pitagoras", norm(an0v), sp.Rational(24, 10))

    sub("lo que el texto deja para el lector (respuestas de esta hoja)")
    v2 = sp.expand(dot(v, v))
    dato(f"    |v|^2(t) = {v2}   (se trabaja con el cuadrado, sin raiz)")
    tmin = sp.solve(sp.Eq(sp.diff(v2, t), 0), t)[0]
    check("instante de rapidez minima t = 1.12 s", tmin, sp.Rational(112, 100))
    check("rapidez minima = 9.6 m/s", sp.sqrt(v2.subs(t, tmin)), sp.Rational(96, 10))
    check("en ese instante v . a = 0 (perpendiculares)",
          sp.simplify(dot((v[0].subs(t, tmin), v[1].subs(t, tmin)), A)), 0)
    dato("Razon conceptual: minimizar |v| pide d|v|/dt = 0, y d|v|/dt = a_t;")
    dato("a_t = 0 es exactamente a perpendicular a v. No hace falta la cuenta.")
    rmin = (r[0].subs(t, tmin), r[1].subs(t, tmin))
    dato(f"    posicion en el minimo: ({num(rmin[0])}, {num(rmin[1])}) m")
    raices_y = sp.solve(sp.Eq(r[1], 0), t)
    tx = max(raices_y)
    check("vuelve al eje x en t = 8 s", tx, 8)
    check("y lo hace en x = 96 m", r[0].subs(t, tx), 96)


def ejemplo_parcial_ventilador():
    titulo("III.3  EJEMPLO PARCIAL 2 — ventilador de techo")
    dato("R = 0.60 m ; arranca del reposo ; gamma = 2 rad/s^2 durante 6 s ;")
    dato("despues w constante.")
    Rv = sp.Rational(6, 10)
    C1, C2 = sp.symbols('C1 C2', real=True)

    sub("integracion angular (dos constantes, las dos fijadas por el enunciado)")
    wt = sp.integrate(2, t) + C1
    C1v = sp.solve(sp.Eq(wt.subs(t, 0), 0), C1)[0]      # arranca del reposo
    wt = wt.subs(C1, C1v)
    tht = sp.integrate(wt, t) + C2
    C2v = sp.solve(sp.Eq(tht.subs(t, 0), 0), C2)[0]     # theta(0) = 0 por eleccion
    tht = tht.subs(C2, C2v)
    check("w(t) = 2 t", wt, 2 * t)
    check("theta(t) = t^2", tht, t**2)
    check("w(6) = 12 rad/s", wt.subs(t, 6), 12)
    check("theta(6) = 36 rad", tht.subs(t, 6), 36)

    sub("lo que el texto deja para el lector (respuestas de esta hoja)")
    dato(f"    |v|(6 s) = R w = {Rv * 12} m/s")
    for T0 in [3, 6]:
        W = wt.subs(t, T0)
        at_ = Rv * 2
        an_ = Rv * W**2
        mod = sp.sqrt(at_**2 + an_**2)
        dato(f"    t = {T0} s:  a_t = {num(at_)} m/s^2 ; a_n = {num(an_)} m/s^2 ; "
             f"|a| = {num(mod)} m/s^2")
    dato("Apenas terminan los 6 s, gamma pasa a 0 y a_t cae a 0; a_n no cambia")
    dato("porque w quedo congelada en 12 rad/s. Esa es la que cambia de valor.")
    N_arranque = sp.Rational(36, 1) / (2 * sp.pi)
    dato(f"    vueltas del arranque = 36/(2 pi) = {num(N_arranque)}")
    dato("No se puede con el periodo: con gamma != 0 el movimiento no es periodico")
    dato("y el periodo no existe (no es que este mal aproximado: no esta definido).")
    Tper = 2 * sp.pi / 12
    dato(f"    regimen: T = {num(Tper)} s ; f = {num(1/Tper)} Hz = "
         f"{num(60/Tper)} vueltas/min")
    dato(f"    vueltas en el minuto siguiente al arranque = "
         f"{num(12*60/(2*sp.pi))}")


# =============================================================================
# PARTE IV — LOS NUEVE EJERCICIOS
# =============================================================================

def ejercicio_1():
    titulo("IV.1  EJ 1 — trayectoria y descripcion vectorial")
    dato("x(t) = 2 [m/s^2] t^2 ;  y(t) = 0.25 [m/s^4] t^4 + 1 m ;  t >= 0.")
    X = sp.symbols('x', real=True)
    x = 2 * t**2
    y = sp.Rational(1, 4) * t**4 + 1

    sub("(a) trayectoria: se elimina t")
    t2 = sp.solve(sp.Eq(x, X), t**2)
    dato(f"    de x = 2t^2 sale t^2 = x/2  (y t = +/- sqrt(x/2))")
    y_de_x = sp.expand(y.subs(t**4, (X / 2)**2))
    check("y(x) = x^2/16 + 1", y_de_x, X**2 / 16 + 1)
    dato("Restriccion: t >= 0 y t^2 >= 0 => x >= 0. La ecuacion y = x^2/16 + 1 NO")
    dato("la trae escrita: es una parabola entera y la trayectoria es media.")
    check("x(t) >= 0 para todo t real (minimo alcanzado en t=0)",
          sp.minimum(x, t, sp.S.Reals), 0)
    check("la rama x < 0 de y = x^2/16 + 1 NO se recorre: no hay t real con x<0",
          sp.solveset(sp.Eq(x, -1), t, domain=sp.S.Reals) == sp.EmptySet, True)

    sub("(b) los tres vectores; unidades")
    v = (sp.diff(x, t), sp.diff(y, t))
    a = (sp.diff(v[0], t), sp.diff(v[1], t))
    check("v(t) = (4t, t^3)", sp.Matrix(list(v)), sp.Matrix([4 * t, t**3]))
    check("a(t) = (4, 3t^2)", sp.Matrix(list(a)), sp.Matrix([4, 3 * t**2]))
    dato("Unidades: [x]=(m/s^2)s^2=m OK ; [y]=(m/s^4)s^4+m=m OK ;")
    dato("          [v]=m/s OK ; [a]=m/s^2 OK.")

    sub("(c) modulo de la aceleracion en t = 2 s")
    a2 = (a[0].subs(t, 2), a[1].subs(t, 2))
    check("a(2) = (4, 12) m/s^2", sp.Matrix(list(a2)), sp.Matrix([4, 12]))
    check("|a(2)| = 4 sqrt(10) = 12.649 m/s^2", sp.N(norm(a2), 8),
          sp.N(4 * sp.sqrt(10), 8))

    sub("(d) angulo entre v y a en t = 2 s")
    v2 = (v[0].subs(t, 2), v[1].subs(t, 2))
    check("v(2) = (8, 8) m/s", sp.Matrix(list(v2)), sp.Matrix([8, 8]))
    cosfi = sp.simplify(dot(v2, a2) / (norm(v2) * norm(a2)))
    fi = sp.deg(sp.acos(cosfi))
    dato(f"    cos(fi) = {num(cosfi, 6)}  ->  fi = {num(fi, 4)} grados")
    check("angulo v-a en t=2 s = 26.565 grados", sp.N(fi, 8), sp.Float("26.5650512"),
          tol=1e-4)

    sub("(e) instantes en que v y a son paralelas a y = x  (A_x = A_y)")
    tv = [r for r in sp.solve(sp.Eq(v[0], v[1]), t) if r.is_real and sp.N(r) > 0]
    ta = [r for r in sp.solve(sp.Eq(a[0], a[1]), t) if r.is_real and sp.N(r) > 0]
    check("v paralela a y=x en t = 2 s", tv, [sp.Integer(2)])
    check("a paralela a y=x en t = 2/sqrt(3) = 1.1547 s",
          sp.N(ta[0], 8), sp.N(2 / sp.sqrt(3), 8))
    check("NO son el mismo instante", sp.simplify(tv[0] - ta[0]) != 0, True)

    sub("(f) velocidad media entre t = 1 s y t = 3 s")
    dr = (x.subs(t, 3) - x.subs(t, 1), y.subs(t, 3) - y.subs(t, 1))
    vm = esc(sp.Rational(1, 2), dr)
    check("Delta r = (16, 20) m", sp.Matrix(list(dr)), sp.Matrix([16, 20]))
    check("v_media = (8, 10) m/s", sp.Matrix(list(vm)), sp.Matrix([8, 10]))
    arco = sp.integrate(sp.sqrt(v[0]**2 + v[1]**2), (t, 1, 3))
    dato(f"    |v_media| = {num(norm(vm))} m/s ;  arco/Dt = "
         f"{num(sp.N(arco)/2)} m/s")
    check("|v_media| < arco/Dt (la cuerda es mas corta que el camino)",
          sp.N(norm(vm)) < sp.N(arco) / 2, True)

    sub("(g) no es un tiro parabolico")
    check("a(t) NO es constante", sp.diff(a[1], t) != 0, True)
    dato("La trayectoria es una parabola pero a depende de t: la parabola de un")
    dato("tiro exige a constante. Coincide la forma, no el movimiento.")


def ejercicio_2():
    titulo("IV.2  EJ 2 — lanzamiento horizontal desde un acantilado de 80 m")
    dato("h = 80 m ; v0 = 15 m/s horizontal ; g = 10 m/s^2.")
    x = 15 * t
    y = 80 - 5 * t**2

    sub("(c) tiempo en el aire")
    raices = sp.solve(sp.Eq(y, 0), t)
    dato(f"    raices: {raices}  ->  se descarta t = -4 s (anterior al lanzamiento)")
    check("t_vuelo = 4 s", max(raices), 4)

    sub("(d) alcance horizontal")
    check("x_f = 60 m", x.subs(t, 4), 60)

    sub("(e) velocidad de llegada")
    vf = vec(15, sp.diff(y, t).subs(t, 4))
    check("v_f = (15, -40) m/s", sp.Matrix(list(vf)), sp.Matrix([15, -40]))
    check("|v_f| = 5 sqrt(73) = 42.720 m/s", sp.N(norm(vf), 8), sp.N(5 * sp.sqrt(73), 8))
    check("angulo bajo la horizontal = 69.444 grados",
          sp.N(sp.deg(sp.atan(sp.Rational(40, 15))), 8), sp.Float("69.4439547"), tol=1e-4)

    sub("(f) la misma piedra sin velocidad inicial")
    t_caida = max(sp.solve(sp.Eq(80 - 5 * t**2, 0), t))
    check("t = 4 s, identico", t_caida, 4)
    dato("El tiempo de vuelo depende SOLO de la componente y (h y v0y); no depende")
    dato("de v0x. Es el desacople de ejes del bloque 7 en su forma mas visible.")

    sub("(g) lanzada hacia arriba con 15 m/s")
    tg = max(sp.solve(sp.Eq(80 + 15 * t - 5 * t**2, 0), t))
    check("t = (3 + sqrt(73))/2 = 5.772 s", sp.N(tg, 8), sp.N((3 + sp.sqrt(73)) / 2, 8))
    check("es mayor que 4 s", sp.N(tg) > 4, True)

    sub("(h) el punto mas alto de un lanzamiento horizontal")
    check("t_max = v0 sen(0)/g = 0", sp.Integer(0), 0)
    dato("El punto mas alto es el propio lanzamiento: v_y ya vale 0 ahi y despues")
    dato("solo se hace mas negativa. No es un fallo de la formula.")


def ejercicio_3():
    titulo("IV.3  EJ 3 — que hace cada eje en un tiro de proyectil (conceptual)")
    dato("No tiene resultado numerico propio: es la lectura de las formulas.")
    dato("Se verifica lo unico verificable, que es (e) y (f).")
    S, Cc = sp.sin(alpha), sp.cos(alpha)

    sub("(e) en el punto mas alto, a_t = 0 y a_n = g")
    A = vec(0, -g)
    V = vec(v0 * Cc, 0)          # en el vertice v es horizontal
    at_, at_v, an_v = descomponer(A, V)
    check("a_t en el vertice = 0", at_, 0)
    check("a_n en el vertice = g", sp.simplify(norm(an_v)), g)
    dato("a es constante y su descomposicion cambia porque la base {v_gorro, n}")
    dato("gira con el movil: no es una propiedad de a sino de la base.")

    sub("(f) alfa y 90-alfa dan el mismo alcance (con h = 0), en distinto tiempo")
    xf = v0**2 * sp.sin(2 * alpha) / g
    check("x_f(90-A) = x_f(A)",
          sp.simplify(xf.subs(alpha, sp.pi / 2 - alpha) - xf), 0)
    tf_ = 2 * v0 * sp.sin(alpha) / g
    dif_t = sp.simplify(tf_.subs(alpha, sp.pi / 2 - alpha) - tf_)
    dato(f"    t_f(90-A) - t_f(A) = {dif_t}")
    check("los tiempos de vuelo NO coinciden (salvo A = 45 grados)",
          sp.simplify(dif_t.subs({v0: 20, g: 10, alpha: sp.rad(30)})) != 0, True)
    check("y sí coinciden exactamente en A = 45 grados",
          sp.simplify(dif_t.subs(alpha, sp.pi / 4)), 0)

    sub("(d) a nunca es nula ni paralela a v en un tiro oblicuo")
    Vt = vec(v0 * Cc, v0 * S - g * t)
    check("a x v = 0 no tiene solucion en t (a nunca es paralela a v si cos A != 0)",
          sp.solve(sp.Eq(cruz(A, Vt), 0), t), [])
    dato("El texto (corregido) acota la frase a A != 90 grados. Se verifica que la")
    dato("acotacion es la correcta, o sea que con A = 90 grados a y v SI son")
    dato("colineales en todo instante:")
    V90 = vec(0, v0 - g * t)
    check("con A = 90 grados, a x v = 0 en todo instante", cruz(A, V90), 0)


def ejercicio_4():
    titulo("IV.4  EJ 4 — que caracteriza a un movimiento circular (conceptual)")
    dato("Sin numeros propios. Se verifica el nucleo de cada inciso.")
    th = sp.Function('theta')(t)
    W = sp.diff(th, t)
    Gm = sp.diff(th, t, 2)
    r = (R * sp.cos(th), R * sp.sin(th))
    v = (sp.diff(r[0], t), sp.diff(r[1], t))
    a = (sp.diff(v[0], t), sp.diff(v[1], t))

    sub("(a) |v| = R |w|, y w tiene que estar en rad/s")
    check("|v|^2 = R^2 w^2, o sea |v| = R |w|", sp.simplify(dot(v, v)), R**2 * W**2)
    dato("Sale de s = R theta, que es la definicion de radian (arco sobre radio).")

    sub("(b) a_n = R w^2 se anula solo si w = 0 ; a_t = R gamma se anula si gamma=0")
    check("a_n = 0  <=>  w = 0", sp.solve(sp.Eq(R * W**2, 0), W), [0])
    check("a_t = 0  <=>  gamma = 0", sp.solve(sp.Eq(R * Gm, 0), Gm), [0])
    dato("=> a_n nula solo en el instante en que el movil esta detenido; a_t nula")
    dato("   en todo el movimiento circular uniforme.")

    sub("(d) el angulo entre r y v, con y sin el origen en el centro")
    check("origen en el centro: r . v = 0 siempre", sp.simplify(dot(r, v)), 0)
    c1, c2 = sp.symbols('c_1 c_2', real=True)
    r_off = (c1 + R * sp.cos(th), c2 + R * sp.sin(th))
    v_off = (sp.diff(r_off[0], t), sp.diff(r_off[1], t))
    prod = sp.simplify(dot(r_off, v_off))
    dato(f"    origen fuera del centro:  r . v = {prod}")
    check("no es identicamente cero salvo c1 = c2 = 0",
          sp.simplify(prod.subs({c1: 3, c2: 0})) != 0, True)
    check("el vector centro->movil SI sigue siendo perpendicular a v",
          sp.simplify(dot(resta(r_off, vec(c1, c2)), v_off)), 0)

    sub("(e) angulo entre v y a")
    check("MCU (gamma=0): v . a = 0", sp.simplify(dot(v, a).subs(Gm, 0)), 0)
    dato("No uniforme: v.a = R^2 w gamma, que no es cero, asi que el angulo deja")
    dato("de ser recto y vale arccos(a_t/|a|).")
    check("no uniforme: v . a = R^2 w gamma", sp.simplify(dot(v, a) - R**2 * W * Gm), 0)


def ejercicio_5():
    titulo("IV.5  EJ 5 — estacion espacial en orbita circular")
    dato("R = 6.8e6 m ; |v| = 7.7e3 m/s constante.")
    Rv = sp.Float("6.8e6")
    Vv = sp.Float("7.7e3")

    sub("(b) velocidad angular")
    W = Vv / Rv
    check("w = |v|/R = 1.1324e-3 rad/s", sp.N(W, 6), sp.Float("1.132353e-3"), tol=1e-8)

    sub("(c) el modulo de a por los tres caminos del bloque 8")
    a1 = Rv * W**2
    a2 = Vv**2 / Rv
    a3 = Vv * W
    dato(f"    R w^2      = {num(a1, 6)} m/s^2")
    dato(f"    |v|^2 / R  = {num(a2, 6)} m/s^2")
    dato(f"    |v| w      = {num(a3, 6)} m/s^2")
    check("R w^2 = |v|^2/R", sp.N(a1, 10), sp.N(a2, 10), tol=1e-8)
    check("|v|^2/R = |v| w", sp.N(a2, 10), sp.N(a3, 10), tol=1e-8)
    check("a = 8.7191 m/s^2", sp.N(a1, 6), sp.Float("8.71912"), tol=1e-4)
    dato("Apunta al centro de la Tierra, que aca es el origen. Es centripeta.")

    sub("(d) periodo y frecuencia")
    T_ = 2 * sp.pi * Rv / Vv
    check("T = 5548.8 s", sp.N(T_, 8), sp.Float("5548.787"), tol=1e-2)
    check("T = 92.48 min", sp.N(T_ / 60, 6), sp.Float("92.4798"), tol=1e-3)
    check("f = 1/T = 1.8023e-4 Hz", sp.N(1 / T_, 6), sp.Float("1.80227e-4"), tol=1e-8)

    sub("(e) r(t) y v(t) completos, con theta(0)=0")
    rr = (Rv * sp.cos(W * t), Rv * sp.sin(W * t))
    vv = (sp.diff(rr[0], t), sp.diff(rr[1], t))
    check("|v(t)| es constante e igual al dato", sp.simplify(sp.N(norm(vv), 8)),
          sp.N(Vv, 8), tol=1e-4)
    check("r . v = 0 en todo t", sp.simplify(dot(rr, vv)), 0)

    sub("(f) otra estacion al doble de radio con la misma rapidez")
    check("a se divide por 2 (a = |v|^2/R)", sp.simplify((Vv**2 / (2 * Rv)) / a2),
          sp.Rational(1, 2))
    check("T se duplica (T = 2 pi R/|v|)",
          sp.simplify((2 * sp.pi * 2 * Rv / Vv) / T_), 2)


def ejercicio_6():
    titulo("IV.6  EJ 6 — pulidora: movimiento circular no uniforme")
    dato("R = 0.25 m ; theta(t) = 2 [rad/s^2] t^2 ; origen en el centro.")
    Rv = sp.Rational(1, 4)
    th = 2 * t**2

    sub("(a)-(b) los angulares")
    W = sp.diff(th, t)
    Gm = sp.diff(W, t)
    check("w(t) = 4 t rad/s", W, 4 * t)
    check("gamma = 4 rad/s^2, constante", Gm, 4)
    dato("gamma constante => MRUV escrito en angulos. Identico al MRUV del cap. 1.")
    r = (Rv * sp.cos(th), Rv * sp.sin(th))
    dato(f"    r(t) = 0.25[cos(2t^2) i + sen(2t^2) j] m = 0.25 u_rho")

    sub("(c) los tres modulos en funcion del tiempo")
    at_ = Rv * Gm
    an_ = Rv * W**2
    mod = sp.sqrt(at_**2 + an_**2)
    check("|a_t| = 1 m/s^2, constante", at_, 1)
    check("|a_n| = 4 t^2 m/s^2", an_, 4 * t**2)
    check("|a| = sqrt(1 + 16 t^4)", sp.simplify(mod), sp.sqrt(16 * t**4 + 1))
    #    control independiente: derivando el vector r dos veces
    v_cart = (sp.diff(r[0], t), sp.diff(r[1], t))
    a_cart = (sp.diff(v_cart[0], t), sp.diff(v_cart[1], t))
    check("control: |a| desde las cartesianas coincide",
          sp.simplify(norm(a_cart) - mod), 0)

    sub("(d) en t = 4 s")
    check("w(4) = 16 rad/s", W.subs(t, 4), 16)
    check("|v|(4) = R w = 4 m/s", Rv * W.subs(t, 4), 4)
    check("|a_t|(4) = 1 m/s^2", at_, 1)
    check("|a_n|(4) = 64 m/s^2", an_.subs(t, 4), 64)
    check("|a|(4) = sqrt(4097) = 64.008 m/s^2", sp.N(mod.subs(t, 4), 8),
          sp.N(sp.sqrt(4097), 8))

    sub("(e) vueltas en los primeros 10 s")
    dth = th.subs(t, 10) - th.subs(t, 0)
    check("Delta theta = 200 rad", dth, 200)
    check("N = 200/(2 pi) = 31.831 vueltas", sp.N(dth / (2 * sp.pi), 8),
          sp.N(100 / sp.pi, 8))
    dato("No se puede con el periodo: gamma != 0, el movimiento no es periodico,")
    dato("el periodo NO existe. La cuenta que vale es N = Delta theta / 2 pi.")

    sub("(f) segundo tramo: gamma1 = -8 rad/s^2 desde t = 10 s")
    K1, K2 = sp.symbols('K1 K2', real=True)
    w2 = sp.integrate(-8, t) + K1
    K1v = sp.solve(sp.Eq(w2.subs(t, 10), W.subs(t, 10)), K1)[0]   # continuidad de w
    w2 = w2.subs(K1, K1v)
    th2 = sp.integrate(w2, t) + K2
    K2v = sp.solve(sp.Eq(th2.subs(t, 10), th.subs(t, 10)), K2)[0]  # continuidad de theta
    th2 = sp.expand(th2.subs(K2, K2v))
    check("w(10) del primer tramo = 40 rad/s", W.subs(t, 10), 40)
    check("w(t) = 120 - 8 t  (segundo tramo)", sp.expand(w2), 120 - 8 * t)
    dato(f"    theta(t) = {th2}   (segundo tramo)")
    tpar = sp.solve(sp.Eq(w2, 0), t)[0]
    check("se detiene en t = 15 s", tpar, 15)
    dth2 = sp.simplify(th2.subs(t, tpar) - th.subs(t, 10))
    check("Delta theta del frenado = 100 rad", dth2, 100)
    check("N = 100/(2 pi) = 15.915 vueltas", sp.N(dth2 / (2 * sp.pi), 8),
          sp.N(50 / sp.pi, 8))
    dato("Las dos constantes las fija la continuidad con el tramo anterior: w y")
    dato("theta no pueden saltar. Ninguna es libre.")

    sub("(g) cuando a es exactamente centripeta y cuando exactamente tangencial")
    dato("exactamente tangencial  <=>  a_n = 0  <=>  w = 0  ->  t = 0 s y t = 15 s.")
    check("w = 0 en t = 0 (tramo 1)", sp.solve(sp.Eq(W, 0), t), [0])
    check("w = 0 en t = 15 (tramo 2)", sp.solve(sp.Eq(w2, 0), t), [15])
    dato("exactamente centripeta  <=>  a_t = 0  <=>  gamma = 0  ->  EN NINGUN")
    dato("instante: gamma vale 4 en el primer tramo y -8 en el segundo.")
    check("gamma nunca se anula en el tramo 1", sp.solve(sp.Eq(Gm, 0), t), [])
    check("gamma nunca se anula en el tramo 2",
          sp.solve(sp.Eq(sp.diff(w2, t), 0), t), [])
    aviso("EJ 6, inciso (g)",
          "la respuesta correcta a 'en que instantes a es exactamente centripeta' "
          "es 'en ninguno', porque gamma nunca vale cero en este movimiento. La "
          "redaccion del inciso presupone que existen ambos casos. Es una trampa "
          "legitima, pero conviene que el gate sepa que la respuesta es el "
          "conjunto vacio y no un olvido del enunciado.")


def ejercicio_7():
    titulo("IV.7  EJ 7 — dron con viento de cola (a_x != 0)")
    dato("h = 45 m ; v0 = (18, 0) m/s ; a = (1.5, -10) m/s^2 ;")
    dato("zona de entrega: circulo de radio 1.5 m centrado a 60 m de la baliza.")
    A = vec(sp.Rational(3, 2), -10)
    v0v = vec(18, 0)
    r0v = vec(0, 45)

    sub("(a)-(b) integracion, cuatro constantes")
    v = (v0v[0] + A[0] * t, v0v[1] + A[1] * t)
    r = (r0v[0] + sp.integrate(v[0], t), r0v[1] + sp.integrate(v[1], t))
    check("v(t) = (18 + 1.5 t, -10 t)", sp.Matrix(list(v)),
          sp.Matrix([18 + sp.Rational(3, 2) * t, -10 * t]))
    check("r(t) = (18t + 0.75 t^2, 45 - 5 t^2)", sp.Matrix(list(r)),
          sp.Matrix([18 * t + sp.Rational(3, 4) * t**2, 45 - 5 * t**2]))
    dato("Las cuatro constantes: v(0)=(18,0) fija dos, r(0)=(0,45) fija las otras.")

    sub("(c) tiempo de caida, distancia horizontal, y si cae en la zona")
    tf = max(sp.solve(sp.Eq(r[1], 0), t))
    check("t_caida = 3 s (lo fija SOLO el eje y)", tf, 3)
    xf = r[0].subs(t, tf)
    check("alcance con viento = 60.75 m", xf, sp.Rational(243, 4))
    dist_centro = sp.Abs(xf - 60)
    check("distancia al centro de la zona = 0.75 m", dist_centro, sp.Rational(3, 4))
    check("cae DENTRO de la zona (0.75 < 1.5)", sp.N(dist_centro) < sp.Rational(3, 2), True)

    sub("(d) el poste a 40 m: aca el despeje deja de ser una division")
    sols = sp.solve(sp.Eq(r[0], 40), t)
    dato(f"    la ecuacion 0.75 t^2 + 18 t - 40 = 0 tiene raices {[num(s) for s in sols]}")
    tp = max(sols)
    check("t = 2.0475 s (se descarta la raiz negativa)", sp.N(tp, 6),
          sp.Float("2.04751"), tol=1e-4)
    check("altura en el poste = 24.04 m", sp.N(r[1].subs(t, tp), 6),
          sp.Float("24.0387"), tol=1e-3)
    check("hay DOS raices (con a_x = 0 habria una sola division)", len(sols), 2)

    sub("(e) velocidad de impacto y descomposicion  <-- los numeros redondos")
    vf = (v[0].subs(t, tf), v[1].subs(t, tf))
    check("v_f = (22.5, -30) m/s", sp.Matrix(list(vf)),
          sp.Matrix([sp.Rational(45, 2), -30]))
    check("|v_f| = 37.5 m/s", norm(vf), sp.Rational(75, 2))
    at_, at_v, an_v = descomponer(A, vf)
    check("a_t = 8.9 m/s^2", at_, sp.Rational(89, 10))
    check("a_n = 4.8 m/s^2", norm(an_v), sp.Rational(48, 10))
    check("control: a_t^2 + a_n^2 = |a|^2 = 102.25",
          sp.simplify(at_**2 + norm(an_v)**2), sp.Rational(409, 4))
    dato("Los tres son exactos: 37.5, 8.9 y 4.8. El enunciado esta calibrado.")

    sub("(f) el mismo problema SIN viento: que coincide y que no")
    dato("El inciso pide cuatro comparaciones. Se resuelve el caso sin viento")
    dato("desde cero, con a = (0,-10), y recien despues se compara.")
    A_sv = vec(0, -10)
    v_sv = (v0v[0] + A_sv[0] * t, v0v[1] + A_sv[1] * t)
    r_sv = (r0v[0] + sp.integrate(v_sv[0], t), r0v[1] + sp.integrate(v_sv[1], t))
    check("sin viento: x(t) = 18 t", r_sv[0], 18 * t)
    check("sin viento: y(t) = 45 - 5 t^2", r_sv[1], 45 - 5 * t**2)

    tf_sv = max(sp.solve(sp.Eq(r_sv[1], 0), t))
    vf_sv = (v_sv[0].subs(t, tf_sv), v_sv[1].subs(t, tf_sv))
    xf_sv = r_sv[0].subs(t, tf_sv)

    dato("     magnitud            con viento        sin viento      coinciden?")
    dato(f"     t_f                 {tf} s              {tf_sv} s             SI")
    dato(f"     v_y(t_f)            {vf[1]} m/s          {vf_sv[1]} m/s         SI")
    dato(f"     v_x(t_f)            {vf[0]} m/s        {vf_sv[0]} m/s         NO")
    dato(f"     |v_f|               {num(norm(vf),4)} m/s        "
         f"{num(norm(vf_sv),4)} m/s      NO")
    dato(f"     x_f                 {xf} m         {xf_sv} m           NO")

    sub("(f.1) las DOS que coinciden")
    check("t_f sin viento = 3 s, identico al de con viento", tf_sv, 3)
    check("t_f coincide con el del caso con viento", tf_sv, tf)
    check("v_y(t_f) sin viento = -30 m/s", vf_sv[1], -30)
    check("v_y(t_f) coincide con el del caso con viento", vf_sv[1], vf[1])

    sub("(f.2) las DOS que no coinciden")
    check("v_f sin viento = (18, -30) m/s", sp.Matrix(list(vf_sv)),
          sp.Matrix([18, -30]))
    check("|v_f| sin viento = 34.99 m/s", sp.N(norm(vf_sv), 6),
          sp.Float("34.99"), tol=5e-3)
    check("|v_f| sin viento = sqrt(1224), valor exacto", sp.simplify(norm(vf_sv)),
          sp.sqrt(1224))
    check("y NO coincide con los 37.5 m/s del caso con viento",
          sp.simplify(norm(vf_sv) - norm(vf)) != 0, True)
    check("alcance sin viento = 54 m", xf_sv, 54)
    check("y NO coincide con los 60.75 m del caso con viento",
          sp.simplify(xf_sv - xf) != 0, True)

    sub("(f.3) donde cae, y si entra en la zona de entrega")
    falta = sp.simplify(60 - xf_sv)
    check("cae 6 m CORTO respecto del centro de la zona", falta, 6)
    check("6 m > 1.5 m de radio  =>  cae FUERA de la zona",
          sp.N(falta) > sp.Rational(3, 2), True)
    check("distancia al BORDE de la zona = 4.5 m", falta - sp.Rational(3, 2),
          sp.Rational(9, 2))
    dato("Contraste con (c): con viento caia a 0.75 m del centro, DENTRO de la")
    dato("zona; sin viento cae 6 m corto, FUERA. El viento es lo que decide la")
    dato("entrega, que es justo lo que el inciso quiere que el lector vea.")

    sub("(f.4) la coincidencia NO es un accidente de estos numeros")
    dato("Se rehace todo con a_x SIMBOLICA. Si t_f y v_y no dependen de a_x, la")
    dato("coincidencia es estructural y no de estos datos particulares.")
    ax = sp.symbols('a_x', real=True)
    v_g = (18 + ax * t, -10 * t)
    r_g = (18 * t + ax * t**2 / 2, 45 - 5 * t**2)
    check("y(t) no contiene a_x en ninguna parte", sp.diff(r_g[1], ax), 0)
    check("v_y(t) no contiene a_x en ninguna parte", sp.diff(v_g[1], ax), 0)
    tf_g = max(sp.solve(sp.Eq(r_g[1], 0), t))
    check("t_f generico = 3 s, para CUALQUIER a_x", tf_g, 3)
    check("d(t_f)/d(a_x) = 0", sp.diff(tf_g, ax), 0)
    check("v_y(t_f) generico = -30 m/s, para CUALQUIER a_x",
          v_g[1].subs(t, tf_g), -30)
    check("d(v_y(t_f))/d(a_x) = 0", sp.diff(v_g[1].subs(t, tf_g), ax), 0)
    dato("En cambio las otras dos SI dependen de a_x:")
    xf_g = sp.expand(r_g[0].subs(t, tf_g))
    modv_g = sp.simplify(sp.sqrt(v_g[0].subs(t, tf_g)**2 + v_g[1].subs(t, tf_g)**2))
    dato(f"    x_f(a_x)   = {xf_g}      ->  d/d(a_x) = {sp.diff(xf_g, ax)}")
    dato(f"    |v_f|(a_x) = {modv_g}")
    check("d(x_f)/d(a_x) = 4.5, NO nula", sp.diff(xf_g, ax), sp.Rational(9, 2))
    check("d(|v_f|)/d(a_x) NO es nula en a_x = 1.5",
          sp.simplify(sp.diff(modv_g, ax).subs(ax, sp.Rational(3, 2))) != 0, True)
    dato("VEREDICTO: las dos que coinciden son EXACTAMENTE las que quedan")
    dato("determinadas por el eje y solo, y el eje y no se entera de a_x. Las dos")
    dato("que no coinciden son las que involucran al eje x. La razon es el")
    dato("desacople de ejes del bloque 7, no una casualidad aritmetica.")

    sub("(f.5) por que la coincidencia no habilita la tabla de a_x = 0")
    dato("Aunque t_f y v_y coincidan, a_t y a_n en el impacto NO coinciden, porque")
    dato("dependen de la direccion de v, que si cambio:")
    at_sv, at_vsv, an_vsv = descomponer(A_sv, vf_sv)
    dato(f"    con viento:  a_t = {num(at_,4)} m/s^2 ; a_n = {num(norm(an_v),4)} m/s^2")
    dato(f"    sin viento:  a_t = {num(at_sv,4)} m/s^2 ; a_n = {num(norm(an_vsv),4)} m/s^2")
    check("a_t con viento != a_t sin viento", sp.simplify(at_ - at_sv) != 0, True)
    dato("Y la altura maxima es 45 m en los dos casos, pero de forma degenerada:")
    dato("el paquete se suelta con v0y = 0, asi que y_max ES el punto de suelte.")
    dato("Por eso el inciso reescrito ya no la usa como termino de comparacion.")
    check("y_max = 45 m con viento (el propio suelte)", r[1].subs(t, 0), 45)
    check("y_max = 45 m sin viento (el propio suelte)", r_sv[1].subs(t, 0), 45)


def ejercicio_8():
    titulo("IV.8  EJ 8 — circunferencia con el origen fuera del centro")
    dato("x(t) = 3 + 4 cos(w t) ; y(t) = 4 sen(w t) ; w = pi/2 rad/s.")
    W = sp.pi / 2
    x = 3 + 4 * sp.cos(W * t)
    y = 4 * sp.sin(W * t)
    X, Y = sp.symbols('x y', real=True)

    sub("(a) trayectoria")
    ident = sp.simplify(((X - 3)**2 + Y**2).subs({X: x, Y: y}))
    check("(x-3)^2 + y^2 = 16 para todo t", ident, 16)
    dato("=> circunferencia de centro (3,0) y radio 4. El origen queda ADENTRO,")
    dato("   a 3 m del centro, pero NO es el centro.")

    sub("(b) los vectores y sus modulos")
    r = (x, y)
    v = (sp.diff(x, t), sp.diff(y, t))
    a = (sp.diff(v[0], t), sp.diff(v[1], t))
    check("|v| = 2 pi = 6.2832 m/s, constante", sp.simplify(norm(v)), 2 * sp.pi)
    check("|a| = pi^2 = 9.8696 m/s^2, constante", sp.simplify(norm(a)), sp.pi**2)
    check("|v| = R w", sp.simplify(norm(v) - 4 * W), 0)
    check("|a| = R w^2", sp.simplify(norm(a) - 4 * W**2), 0)
    dato("Modulos constantes => movimiento circular UNIFORME.")

    sub("(c) instantes en que r es perpendicular a v  <-- la afirmacion t = 2n")
    prod = sp.simplify(sp.expand_trig(dot(r, v)))
    dato(f"    r . v = {prod}")
    check("r . v = -12 w sen(w t) = -6 pi sen(pi t/2)",
          sp.simplify(prod + 6 * sp.pi * sp.sin(sp.pi * t / 2)), 0)
    n = sp.symbols('n', integer=True)
    sols = sp.solveset(sp.Eq(prod, 0), t, domain=sp.S.Reals)
    dato(f"    solucion general: {sols}")
    check("se anula exactamente en t = 2n s",
          all(sp.simplify(prod.subs(t, 2 * k)) == 0 for k in range(-3, 6)), True)
    check("y NO se anula en instantes intermedios (t = 1, 3, 0.5)",
          all(sp.simplify(prod.subs(t, k)) != 0
              for k in [1, 3, sp.Rational(1, 2)]), True)
    dato("CONFIRMADO: r perp v solo en t = 2n s, no en todo instante.")
    check("el vector CENTRO->movil si es perpendicular a v siempre",
          sp.simplify(dot(resta(r, vec(3, 0)), v)), 0)

    sub("(d) instantes en que v es perpendicular a a")
    check("v . a = 0 en TODO instante (es circular uniforme)",
          sp.simplify(dot(v, a)), 0)
    dato("La diferencia con (c) es la hipotesis: a apunta al centro y v es")
    dato("tangente, siempre; r apunta desde el ORIGEN, que no es el centro.")

    sub("(e) hacia donde apunta a")
    check("a = -(w^2)(r - centro): apunta siempre a (3,0)",
          sp.Matrix(list(suma(a, esc(W**2, resta(r, vec(3, 0)))))),
          sp.Matrix([0, 0]))
    for tt in [sp.Rational(1, 3), sp.Rational(7, 5)]:
        av = (a[0].subs(t, tt), a[1].subs(t, tt))
        hacia = resta(vec(3, 0), (r[0].subs(t, tt), r[1].subs(t, tt)))
        check(f"en t={tt}, a es paralela a (centro - r)", cruz(av, hacia), 0)

    sub("(f) periodo, frecuencia, y distancias extremas al ORIGEN")
    T_ = 2 * sp.pi / W
    check("T = 4 s", T_, 4)
    check("f = 0.25 Hz", 1 / T_, sp.Rational(1, 4))
    d2 = sp.simplify(sp.expand_trig(dot(r, r)))
    dato(f"    |r|^2 = {d2}")
    check("|r|^2 = 25 + 24 cos(pi t/2)",
          sp.simplify(d2 - (25 + 24 * sp.cos(sp.pi * t / 2))), 0)
    check("distancia maxima al origen = 7 m (en t = 4n)", sp.sqrt(d2.subs(t, 0)), 7)
    check("distancia minima al origen = 1 m (en t = 2 + 4n)",
          sp.sqrt(sp.simplify(d2.subs(t, 2))), 1)
    dato("Las dos distancias son enteras: 7 m y 1 m. Consistente con centro a 3 m")
    dato("del origen y radio 4 (3+4 = 7, 4-3 = 1).")

    sub("(g) a y a_n coinciden en un circular uniforme")
    at_, at_v, an_v = descomponer(a, v)
    check("a_t = 0 siempre", sp.simplify(at_), 0)
    check("a_n = a", sp.Matrix([sp.simplify(an_v[0] - a[0]),
                                sp.simplify(an_v[1] - a[1])]), sp.Matrix([0, 0]))


def ejercicio_9():
    titulo("IV.9  EJ 9 — tiro sobre una ladera que baja 37 grados")
    dato("v0 = 20 m/s a 53 grados sobre la horizontal ; ladera a -37 grados ;")
    dato("g = 10 m/s^2 ; sen37 = 0.60, cos37 = 0.80 (=> sen53 = 0.80, cos53 = 0.60).")
    S37, C37 = sp.Rational(6, 10), sp.Rational(8, 10)
    S53, C53 = C37, S37          # complementarios: sen53 = cos37, cos53 = sen37
    check("control: sen^2(53) + cos^2(53) = 1", S53**2 + C53**2, 1)

    sub("(a) ecuaciones de movimiento y recta de la ladera")
    v0v = vec(20 * C53, 20 * S53)
    check("v0 = (12, 16) m/s", sp.Matrix(list(v0v)), sp.Matrix([12, 16]))
    x = v0v[0] * t
    y = v0v[1] * t - 5 * t**2
    check("x(t) = 12 t", x, 12 * t)
    check("y(t) = 16 t - 5 t^2", y, 16 * t - 5 * t**2)
    X = sp.symbols('x', real=True)
    m_lad = -S37 / C37
    ladera = m_lad * X
    check("ladera: y = -0.75 x", ladera, -sp.Rational(3, 4) * X)

    sub("(b)-(c) la condicion de impacto NO es y = 0 sino y(t) = -0.75 x(t)")
    eq = sp.Eq(y, ladera.subs(X, x))
    raices = sp.solve(eq, t)
    dato(f"    raices: {raices}  ->  se descarta t = 0 (el propio lanzamiento)")
    tf = max(raices)
    check("t_f = 5 s", tf, 5)
    xf = x.subs(t, tf)
    yf = y.subs(t, tf)
    check("distancia horizontal = 60 m", xf, 60)
    check("desnivel descendido = 45 m", -yf, 45)
    check("distancia SOBRE la ladera = 75 m", sp.sqrt(xf**2 + yf**2), 75)
    dato("60-45-75 es un triangulo 3-4-5 escalado x15: los tres son enteros.")
    check("el punto de impacto esta sobre la recta de la ladera",
          sp.simplify(yf - ladera.subs(X, xf)), 0)

    sub("(d) altura maxima sobre el punto de lanzamiento")
    tmax = sp.solve(sp.Eq(sp.diff(y, t), 0), t)[0]
    check("t_max = 1.6 s", tmax, sp.Rational(8, 5))
    check("y_max = 12.8 m", y.subs(t, tmax), sp.Rational(64, 5))
    check("t_max NO es la mitad del tiempo de vuelo (2.5 s)",
          sp.simplify(tmax - tf / 2) != 0, True)
    dato("La simetria mitad-de-vuelo exige que la llegada este a la MISMA altura")
    dato("que el lanzamiento; aca la llegada esta 45 m mas abajo.")

    sub("(e) velocidad de llegada")
    vf = vec(12, 16 - 10 * tf)
    check("v_f = (12, -34) m/s", sp.Matrix(list(vf)), sp.Matrix([12, -34]))
    check("|v_f| = sqrt(1300) = 36.056 m/s", sp.N(norm(vf), 8),
          sp.N(sp.sqrt(1300), 8))
    dato(f"    angulo bajo la horizontal = "
         f"{num(sp.deg(sp.atan(sp.Rational(34,12))))} grados")

    sub("(f) alcance sobre terreno horizontal, y el optimo de 45 grados")
    tf_h = max(sp.solve(sp.Eq(y, 0), t))
    check("t_f horizontal = 3.2 s", tf_h, sp.Rational(16, 5))
    check("alcance horizontal = 38.4 m", x.subs(t, tf_h), sp.Rational(192, 5))
    check("la ladera da mucho mas alcance horizontal (60 > 38.4)",
          sp.N(60) > sp.N(sp.Rational(192, 5)), True)
    #    optimo sobre una ladera que baja un angulo phi
    ph = sp.rad(37)
    al = sp.symbols('al', positive=True)
    #  alcance sobre la ladera R(al) = 2 v0^2 cos(al) sen(al+phi) / (g cos^2 phi)
    Ral = 2 * 20**2 * sp.cos(al) * sp.sin(al + ph) / (10 * sp.cos(ph)**2)
    al_op = sp.nsolve(sp.diff(Ral, al), al, 0.5)
    check("el optimo sobre la ladera es 45 - phi/2 = 26.5 grados",
          sp.N(sp.deg(al_op), 6), sp.N(45 - 37 / sp.Integer(2), 6), tol=1e-3)
    check("y por lo tanto 45 grados NO es el optimo aca",
          sp.N(sp.deg(al_op)) < 45, True)
    dato("Sobre una ladera que baja el optimo es MENOR que 45 grados. El texto")
    dato("solo pide justificarlo cualitativamente; el numero es 26.5 grados.")
    aviso("EJ 9, enunciado",
          "el enunciado da sen37 = 0.60 y cos37 = 0.80 pero el lanzamiento es a 53 "
          "grados, asi que el lector tiene que deducir sen53 = 0.80 y cos53 = 0.60 "
          "por complementariedad. Es correcto y hasta deseable, pero conviene "
          "verificar que la guia de la catedra lo plantee igual.")


# =============================================================================

def main():
    print(__doc__)

    p1_derivar_un_vector()
    p1_tangencial_y_normal()
    p1_tabla_tiro()
    p1_circular()

    p2_figuras()

    ejemplo_completo()
    ejemplo_parcial_disco()
    ejemplo_parcial_ventilador()

    ejercicio_1()
    ejercicio_2()
    ejercicio_3()
    ejercicio_4()
    ejercicio_5()
    ejercicio_6()
    ejercicio_7()
    ejercicio_8()
    ejercicio_9()

    titulo("RESUMEN")
    if FALLAS:
        print(f" {len(FALLAS)} discrepancia(s) NUMERICA(s) entre el calculo y el documento:")
        for f in FALLAS:
            print("   -", f)
    else:
        print(" Sin discrepancias numericas: todos los resultados que afirma el")
        print(" capitulo coinciden con el calculo independiente de este archivo.")
    print()
    if AVISOS:
        print(f" {len(AVISOS)} observacion(es) no numerica(s) para revision cualitativa:")
        for a in AVISOS:
            print("   -", a)
    else:
        print(" Sin observaciones cualitativas.")
    print()


if __name__ == "__main__":
    main()
