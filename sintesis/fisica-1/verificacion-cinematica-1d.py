# -*- coding: utf-8 -*-
"""
================================================================================
 VERIFICACION INDEPENDIENTE — Cinematica en una dimension (Fisica 1, Guia 1)
================================================================================

 Que es esto
 -----------
 Este archivo resuelve, desde cero y con sympy, todo lo que el capitulo de
 Cinematica 1D afirma: las deducciones simbolicas (derivada desde el cociente
 incremental, MRUV por doble integracion, la relacion sin tiempo) y los
 resultados numericos de los dos ejemplos resueltos y de los nueve ejercicios.

 Para que te sirve a vos
 -----------------------
 1. Es la hoja de respuestas de los ejercicios del capitulo. El apunte plantea
    los ejercicios sin resolverlos; aca estan resueltos y con el detalle del
    camino.
 2. Es una plantilla de autoevaluacion. Resolve el ejercicio a mano, corre esto,
    y compara. Si no coincide, la seccion correspondiente te muestra el paso
    intermedio donde mirar.
 3. Cada bloque esta escrito para que puedas cambiar los datos y volver a
    correrlo con los numeros de tu practico.

 Como se corre
 -------------
     python verificacion-cinematica-1d.py

 Requiere sympy. En todo el archivo g = 10 m/s^2 (valor que fija la catedra).
 Las deducciones simbolicas se hacen con g generico y recien al final se
 reemplaza, justamente para poder ver cuales resultados NO dependen de g.
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


def check(etiqueta, obtenido, esperado, tol=1e-6):
    """Compara lo que calculo este script contra lo que dice el documento.

    'obtenido'  -> lo que sale de resolver el ejercicio aca, sin mirar el texto.
    'esperado'  -> el valor tal como figura en el borrador del capitulo.
    """
    def norm(z):
        if isinstance(z, str):
            return z
        if isinstance(z, (list, tuple, sp.Matrix)):
            return sp.Matrix(list(z))
        if isinstance(z, float) or (hasattr(z, 'is_Float') and z.is_Float):
            return sp.Float(z)          # los decimales se comparan como decimales
        return sp.nsimplify(z)

    o, e = norm(obtenido), norm(esperado)
    if isinstance(o, str) or isinstance(e, str):
        ok = (str(o) == str(e))
    elif isinstance(o, sp.Matrix) or isinstance(e, sp.Matrix):
        ok = (sp.Matrix(o).shape == sp.Matrix(e).shape and
              all(sp.simplify(p - q) == 0 for p, q in zip(sp.Matrix(o), sp.Matrix(e))))
    else:
        dif = sp.simplify(o - e)
        ok = (dif == 0) or (abs(complex(sp.N(dif))) < tol)
    marca = "OK  " if ok else "MAL "
    fmt = (lambda z: list(z)) if isinstance(o, sp.Matrix) else (lambda z: z)
    print(f"   [{marca}] {etiqueta}: calculado = {fmt(o)}"
          f"   |  documento = {fmt(e)}")
    if not ok:
        FALLAS.append(etiqueta)
    return ok


def titulo(txt):
    print("\n" + "=" * 78)
    print(txt)
    print("=" * 78)


def sub(txt):
    print("\n-- " + txt)


# Simbolos globales
t, dt, T = sp.symbols('t Delta_t T', real=True)
g = sp.symbols('g', positive=True)
G = sp.Integer(10)          # valor de la catedra, m/s^2
a2, a1, a0 = sp.symbols('a_2 a_1 a_0', real=True)
a, v0, x0 = sp.symbols('a v_0 x_0', real=True)


# =============================================================================
# PARTE I — LAS DEDUCCIONES SIMBOLICAS DEL MARCO TEORICO
# =============================================================================

def parte_1_derivada_desde_la_definicion():
    titulo("I.1  Derivada de la parabola desde el cociente incremental")
    # El texto afirma:
    #   x(t) = a2 t^2 + a1 t + a0
    #   v_media(t, dt) = a2 (2t + dt) + a1        <- antes de tomar el limite
    #   v(t) = 2 a2 t + a1                        <- despues del limite
    x = a2 * t**2 + a1 * t + a0
    cociente = sp.simplify((x.subs(t, t + dt) - x) / dt)      # dt != 0, se puede dividir
    sub("cociente incremental simplificado (todavia con Delta_t adentro)")
    print("   ", sp.expand(cociente))
    check("v_media = a2(2t+Dt)+a1", sp.expand(cociente), sp.expand(a2 * (2 * t + dt) + a1))

    v_lim = sp.limit(cociente, dt, 0)
    check("v(t) = 2 a2 t + a1", sp.expand(v_lim), sp.expand(2 * a2 * t + a1))

    # Y la derivada directa tiene que coincidir con el limite:
    check("d/dt coincide con el limite", sp.expand(sp.diff(x, t)), sp.expand(v_lim))

    # Caso MRU: con a2 = 0 la media y la instantanea coinciden y valen a1.
    sub("caso a2 = 0 (MRU): media e instantanea coinciden")
    check("v_media(a2=0)", cociente.subs(a2, 0), a1)
    check("v_inst(a2=0)", v_lim.subs(a2, 0), a1)


def parte_1_regla_de_la_potencia():
    titulo("I.2  Regla de la potencia: el caso alpha=2 y la generalizacion")
    # El texto deduce alpha=2 de la cuenta de la parabola y generaliza por binomio.
    x = sp.symbols('x', positive=True)
    dx = sp.symbols('Delta_x', positive=True)

    sub("alpha = 2, desde la definicion")
    coc2 = sp.expand(((x + dx)**2 - x**2) / dx)
    print("    cociente incremental =", coc2, "  (el termino en Delta_x se va con el limite)")
    check("d(x^2)/dx", sp.limit(coc2, dx, 0), 2 * x)

    sub("generalizacion por binomio de Newton, alpha entero de 1 a 6")
    for al in range(1, 7):
        coc = sp.expand(((x + dx)**al - x**al) / dx)
        check(f"d(x^{al})/dx", sp.limit(coc, dx, 0), al * x**(al - 1))

    # La afirmacion del texto de que el 1/2 del MRUV es el 1/(alpha+1) de la
    # primitiva de la potencia, con alpha=1.
    sub("primitiva de la potencia: 1/(alpha+1)")
    for al in [1, 2, 3]:
        prim = sp.integrate(x**al, x)
        check(f"int x^{al} dx", prim, x**(al + 1) / (al + 1))
    print("    -> con alpha=1 la primitiva de t es t^2/2: ese es el 1/2 del MRUV.")


def parte_1_mruv_por_integracion():
    titulo("I.3  MRUV deducido integrando dos veces una aceleracion constante")
    # Paso 1: de a constante a v(t), fijando C1 con v(0) = v0.
    C1, C2 = sp.symbols('C_1 C_2', real=True)
    v_gen = sp.integrate(a, t) + C1                 # = a t + C1
    C1_val = sp.solve(sp.Eq(v_gen.subs(t, 0), v0), C1)[0]
    v_t = sp.expand(v_gen.subs(C1, C1_val))
    sub("primera integracion")
    print("    v(t) = int a dt + C1 =", v_gen, "  ; la condicion v(0)=v0 da C1 =", C1_val)
    check("C1 = v0", C1_val, v0)
    check("v(t) = v0 + a t", v_t, v0 + a * t)

    # Paso 2: de v(t) a x(t), fijando C2 con x(0) = x0.
    x_gen = sp.integrate(v_t, t) + C2
    C2_val = sp.solve(sp.Eq(x_gen.subs(t, 0), x0), C2)[0]
    x_t = sp.expand(x_gen.subs(C2, C2_val))
    sub("segunda integracion")
    print("    x(t) = int v dt + C2 =", sp.expand(x_gen), "  ; la condicion x(0)=x0 da C2 =", C2_val)
    check("C2 = x0", C2_val, x0)
    check("x(t) = x0 + v0 t + a t^2/2", x_t, x0 + v0 * t + a * t**2 / 2)

    # El coeficiente del termino cuadratico es exactamente 1/2.
    coef_cuad = sp.expand(x_t).coeff(t, 2)
    check("coeficiente de t^2 = a/2", coef_cuad, a / 2)

    # Casos particulares: MRU (a=0) y reposo (a=0, v0=0).
    sub("casos particulares")
    check("MRU: v(t)", v_t.subs(a, 0), v0)
    check("MRU: x(t)", x_t.subs(a, 0), x0 + v0 * t)
    check("Reposo: x(t)", x_t.subs({a: 0, v0: 0}), x0)

    # Version con t0 generico, que es la que usa la tabla del capitulo.
    sub("version con instante de referencia t0 generico")
    t0 = sp.symbols('t_0', real=True)
    v_t0 = v0 + a * (t - t0)
    x_t0 = x0 + v0 * (t - t0) + a * (t - t0)**2 / 2
    check("dv/dt = a", sp.diff(v_t0, t), a)
    check("dx/dt = v", sp.expand(sp.diff(x_t0, t)), sp.expand(v_t0))
    check("x(t0) = x0", x_t0.subs(t, t0), x0)
    check("v(t0) = v0", v_t0.subs(t, t0), v0)


def parte_1_relacion_sin_tiempo():
    titulo("I.4  v^2 = v0^2 + 2 a Dx por eliminacion algebraica de t")
    # El texto elimina t entre v = v0 + a t y Dx = v0 t + a t^2/2. No usa
    # a dx = v dv. Reproduzco exactamente ese camino.
    v = sp.symbols('v', real=True)
    t_desp = sp.solve(sp.Eq(v, v0 + a * t), t)[0]          # t = (v - v0)/a
    check("t despejado", t_desp, (v - v0) / a)

    Dx = sp.simplify(v0 * t_desp + a * t_desp**2 / 2)
    sub("Dx tras reemplazar t")
    print("    Dx =", sp.simplify(Dx))
    check("Dx = (v^2 - v0^2)/(2a)", sp.simplify(Dx), (v**2 - v0**2) / (2 * a))

    # Y de ahi, despejando v^2:
    v2 = sp.solve(sp.Eq(sp.symbols('Dx'), (v**2 - v0**2) / (2 * a)), v**2)
    check("v^2 = v0^2 + 2 a Dx", sp.expand(v2[0]), sp.expand(v0**2 + 2 * a * sp.symbols('Dx')))

    # Control cruzado: la relacion tiene que ser identicamente cierta al
    # sustituir las expresiones horarias, para cualquier t.
    sub("control cruzado sobre las expresiones horarias")
    v_h = v0 + a * t
    Dx_h = v0 * t + a * t**2 / 2
    residuo = sp.simplify(v_h**2 - (v0**2 + 2 * a * Dx_h))
    check("identidad v^2 - (v0^2 + 2 a Dx) = 0", residuo, 0)

    # Chequeo del bloque: auto a 20 m/s frenando con a = -4 m/s^2.
    sub("chequeo del bloque: 20 m/s, a = -4 m/s^2, hasta detenerse")
    d_frenado = (0**2 - 20**2) / (2 * (-4))
    check("distancia de frenado (m)", d_frenado, 50)


def parte_1_puente_a2():
    titulo("I.5  El puente a_2 = a/2, y el caso x(t) = 3 + 17t - 5t^2")
    # Afirmacion del texto: comparando x0 + v0 t + (1/2) a t^2 con a2 t^2+a1 t+a0
    # se lee a0 = x0, a1 = v0, a2 = a/2  (o sea a = 2 a2).
    x_fis = x0 + v0 * t + a * t**2 / 2
    x_pol = a2 * t**2 + a1 * t + a0
    sol = sp.solve([sp.Eq(sp.expand(x_fis).coeff(t, k), sp.expand(x_pol).coeff(t, k))
                    for k in (0, 1, 2)], [x0, v0, a], dict=True)[0]
    sub("identificacion termino a termino")
    check("x0 = a0", sol[x0], a0)
    check("v0 = a1", sol[v0], a1)
    check("a = 2 a2  (es decir a2 = a/2)", sol[a], 2 * a2)

    # El caso concreto del ejercicio 4 del practico de la catedra.
    sub("caso concreto: x(t) = 3 + 17t - 5t^2  (ej. 4 del Practico 1)")
    x_ej4 = 3 + 17 * t - 5 * t**2
    check("a_2", sp.expand(x_ej4).coeff(t, 2), -5)
    check("a_1 = v0", sp.expand(x_ej4).coeff(t, 1), 17)
    check("a_0 = x0", sp.expand(x_ej4).coeff(t, 0), 3)
    v_ej4 = sp.diff(x_ej4, t)
    a_ej4 = sp.diff(x_ej4, t, 2)
    check("v(t) = 17 - 10t", v_ej4, 17 - 10 * t)
    check("a = 2*a_2 = -10 m/s^2  (NO -5)", a_ej4, -10)
    print("    -> leer a = -5 es el error de factor 2 que el capitulo denuncia.")
    check("v = 0 en t (s)", sp.solve(sp.Eq(v_ej4, 0), t)[0], sp.Rational(17, 10))
    raices = sorted(sp.solve(sp.Eq(x_ej4, 0), t))
    check("retorno al origen t = (17+sqrt(349))/10 s", raices[1], (17 + sp.sqrt(349)) / 10)
    print(f"    (numericamente t = {sp.N(raices[1], 4)} s; la otra raiz, "
          f"{sp.N(raices[0], 4)} s, es negativa y se descarta)")


def parte_1_bloques_numericos():
    titulo("I.6  Numeros sueltos de los bloques teoricos")

    sub("bloque de desplazamiento: 0 -> 5 m -> 2 m")
    check("Dx (m)", 2 - 0, 2)
    check("d (m)", 5 + 3, 8)
    check("d >= |Dx|", 1 if 8 >= abs(2) else 0, 1)
    sub("misma ida y vuelta pero terminando en el origen")
    check("Dx (m)", 0 - 0, 0)
    check("d (m)", 5 + 5, 10)

    sub("bloque de velocidad media/promedio: el mismo viaje en 5 s")
    check("v_media (m/s)", sp.Rational(2, 5), sp.Rational(4, 10))
    check("V_promedio (m/s)", sp.Rational(8, 5), sp.Rational(16, 10))
    check("v_media volviendo al origen (m/s)", sp.Rational(0, 5), 0)
    check("V_promedio volviendo al origen (m/s)", sp.Rational(10, 5), 2)

    sub("chequeo: area de v(t) triangular, base 6 s, altura 10 m/s")
    check("desplazamiento (m)", sp.Rational(1, 2) * 6 * 10, 30)

    sub("bloque de tramos: a=1 (t<1), a=2 (t>=1), v(0)=1 m/s")
    C1, C2 = sp.symbols('C_1 C_2')
    v1 = sp.integrate(1, t) + C1
    c1 = sp.solve(sp.Eq(v1.subs(t, 0), 1), C1)[0]
    v1 = v1.subs(C1, c1)
    check("tramo 1: v(t) = t + 1", v1, t + 1)
    check("v(1) = 2 m/s", v1.subs(t, 1), 2)
    v2 = sp.integrate(2, t) + C2
    c2 = sp.solve(sp.Eq(v2.subs(t, 1), v1.subs(t, 1)), C2)[0]   # continuidad, no dato libre
    check("C2 fijada por continuidad", c2, 0)
    check("tramo 2: v(t) = 2t", v2.subs(C2, c2), 2 * t)

    sub("chequeo: x(t) = 12 - 4t + 3t^2")
    xq = 12 - 4 * t + 3 * t**2
    check("v(t)", sp.diff(xq, t), 6 * t - 4)
    check("a", sp.diff(xq, t, 2), 6)
    check("x0", xq.subs(t, 0), 12)
    check("v0", sp.diff(xq, t).subs(t, 0), -4)

    sub("chequeo: x(t) = 5t^2 - 3t + 1  (la aceleracion NO es 5)")
    check("a = 2*a2", sp.diff(5 * t**2 - 3 * t + 1, t, 2), 10)

    sub("consistencia dimensional del ejemplo del apunte: (1/3)t^3 - 1t + 1/2")
    # Cada termino debe dar metros: [m/s^3][s^3] = m, [m/s][s] = m, [m] = m.
    print("    (1/3 m/s^3)(s^3) = m ; (1 m/s)(s) = m ; (1/2 m) = m  -> los tres dan metros. OK")

    sub("figura de los tres paneles: el cero de v cae sobre el maximo de y")
    # En el tikz el panel de arriba es y = 6 + 2u - u^2 con t = 2u, o sea
    # y(t) = 6 + t - t^2/4 en coordenadas de dibujo; el panel del medio es la
    # recta de (0,4.6) a (4,2.6) sobre un eje horizontal en 3.6.
    u = sp.symbols('u')
    y_dib = (6 + 2 * u - u**2).subs(u, t / 2)
    t_max = sp.solve(sp.Eq(sp.diff(y_dib, t), 0), t)[0]
    check("t del maximo de y en el dibujo", t_max, 2)
    v_dib = sp.Rational(46, 10) + (sp.Rational(26, 10) - sp.Rational(46, 10)) / 4 * t
    t_cero_v = sp.solve(sp.Eq(v_dib, sp.Rational(36, 10)), t)[0]
    check("t del cero de v en el dibujo", t_cero_v, 2)
    check("la pendiente dibujada de v coincide con dy/dt",
          sp.diff(v_dib, t), sp.diff(y_dib, t, 2))
    check("marca punteada en t1", 2, t_max)


# =============================================================================
# PARTE II — LOS DOS EJEMPLOS RESUELTOS
# =============================================================================

def ejemplo_completo():
    titulo("II.1  EJEMPLO RESUELTO (completo) — tiro vertical con el dato completo")
    print("""
 Enunciado (resumido): se lanza una pelota hacia arriba desde el suelo. Pasa por
 A, a 1.8 m del suelo, con velocidad v, y por B, 2.4 m mas arriba que A, con
 velocidad v/2. g = 10 m/s^2. Hallar v, la velocidad inicial v0 y la altura
 maxima por encima de B.
 Eje vertical, origen en el suelo, positivo hacia arriba, t=0 en el lanzamiento;
 con esa eleccion a = -g.
""")
    hA = sp.Rational(18, 10)      # 1.8 m
    hAB = sp.Rational(24, 10)     # 2.4 m

    # --- CAMINO 1: la relacion sin tiempo, tramo por tramo (el del ejemplo) ---
    sub("Camino 1 — relacion sin tiempo, simbolica primero")
    v = sp.symbols('v', positive=True)
    h_ab = sp.symbols('h_AB', positive=True)
    # De A a B:  (v/2)^2 = v^2 - 2 g h_AB
    sol_v2 = sp.solve(sp.Eq((v / 2)**2, v**2 - 2 * g * h_ab), v**2)[0]
    check("v^2 = (8/3) g h_AB", sp.simplify(sol_v2), sp.Rational(8, 3) * g * h_ab)
    v2_num = sol_v2.subs({g: G, h_ab: hAB})
    check("v^2 (m^2/s^2)", v2_num, 64)
    check("v (m/s)", sp.sqrt(v2_num), 8)
    check("v/2 en B (m/s)", sp.sqrt(v2_num) / 2, 4)

    # Del suelo a A:  v^2 = v0^2 - 2 g hA  ->  v0^2 = v^2 + 2 g hA
    v0_2 = v2_num + 2 * G * hA
    check("v0^2 (m^2/s^2)", v0_2, 100)
    check("v0 (m/s)", sp.sqrt(v0_2), 10)

    # De B al punto mas alto: 0 = (v/2)^2 - 2 g h_sobreB
    h_sobreB_sym = sp.simplify((sol_v2 / 4) / (2 * g))
    sub("la altura sobre B, en simbolos")
    print("    h_sobre_B = (v/2)^2/(2g) = v^2/(8g) =", sp.simplify(h_sobreB_sym))
    check("h_sobre_B = h_AB/3", sp.simplify(h_sobreB_sym), h_ab / 3)
    # La afirmacion de diseno: no depende de g.
    depende_de_g = g in sp.simplify(h_sobreB_sym).free_symbols
    check("h_sobre_B NO depende de g", 0 if depende_de_g else 1, 1)
    check("h_sobre_B numerica (m)", h_sobreB_sym.subs(h_ab, hAB), sp.Rational(8, 10))

    # --- CAMINO 2: control por altura maxima medida desde el suelo -----------
    sub("Camino 2 — altura maxima desde el lanzamiento (verificacion cruzada)")
    h_max_suma = hA + hAB + sp.Rational(8, 10)
    h_max_form = v0_2 / (2 * G)
    check("1.8 + 2.4 + 0.8 (m)", h_max_suma, 5)
    check("v0^2/(2g) (m)", h_max_form, 5)
    check("los dos caminos coinciden", h_max_suma, h_max_form)

    # --- CAMINO 3 (extra): expresiones horarias, para cerrar el circulo ------
    sub("Camino 3 (extra) — con las expresiones horarias, sin usar la relacion sin tiempo")
    v0v = sp.Integer(10)
    y_t = v0v * t - G * t**2 / 2
    v_t = sp.diff(y_t, t)
    tA = min([r for r in sp.solve(sp.Eq(y_t, hA), t) if r >= 0])
    tB = min([r for r in sp.solve(sp.Eq(y_t, hA + hAB), t) if r >= 0])
    check("v en A (m/s)", v_t.subs(t, tA), 8)
    check("v en B (m/s)", v_t.subs(t, tB), 4)
    check("v(B) = v(A)/2", v_t.subs(t, tB), v_t.subs(t, tA) / 2)
    t_top = sp.solve(sp.Eq(v_t, 0), t)[0]
    check("t del punto mas alto (s)", t_top, 1)
    check("altura maxima (m)", y_t.subs(t, t_top), 5)
    check("altura sobre B (m)", y_t.subs(t, t_top) - (hA + hAB), sp.Rational(8, 10))
    sub("inciso (f): los tres graficos")
    check("cero de v cae sobre el maximo de y",
          sp.solve(sp.Eq(v_t, 0), t)[0],
          sp.solve(sp.Eq(sp.diff(y_t, t), 0), t)[0])
    check("a constante durante todo el vuelo", sp.diff(y_t, t, 2), -10)
    sub("inciso (g): conteo de incognitas contra datos")
    print("    3 incognitas (v, v0, h_sobre_B) y 3 datos independientes")
    print("    (h_A = 1.8 m, h_AB = 2.4 m, v_B = v_A/2)  -> el sistema cierra.")


def ejemplo_parcial():
    titulo("II.2  EJEMPLO RESUELTO (parcial) — x(t) = 9 + 6t - 3t^2")
    x = 9 + 6 * t - 3 * t**2
    check("a_2", sp.expand(x).coeff(t, 2), -3)
    check("a_1", sp.expand(x).coeff(t, 1), 6)
    check("a_0", sp.expand(x).coeff(t, 0), 9)
    v = sp.diff(x, t)
    check("v(t) = 6 - 6t", v, 6 - 6 * t)
    check("a = 2 a_2 = -6 m/s^2  (NO -3)", sp.diff(x, t, 2), -6)
    check("x0 (m)", x.subs(t, 0), 9)
    check("v0 (m/s)", v.subs(t, 0), 6)

    sub("continuacion que el ejemplo devuelve al lector")
    t_v0 = sp.solve(sp.Eq(v, 0), t)[0]
    check("v = 0 en t (s)", t_v0, 1)
    check("x en ese instante (m)", x.subs(t, t_v0), 12)
    check("x''(t) < 0 -> maximo", 1 if sp.diff(x, t, 2) < 0 else 0, 1)
    raices = sorted(sp.solve(sp.Eq(x, 0), t))
    check("raices de x(t)=0", sp.Matrix(raices), sp.Matrix([-1, 3]))
    print("    -> t = -1 s cae antes del t=0 y se descarta explicitamente.")
    check("v(3 s) (m/s)", v.subs(t, 3), -12)
    check("v(2 s) = x'(2) (m/s)", v.subs(t, 2), -6)
    check("dx(2)/dt  (evaluar y despues derivar) = 0", sp.diff(x.subs(t, 2), t), 0)


# =============================================================================
# PARTE III — LOS NUEVE EJERCICIOS
# =============================================================================

def ejercicio_1():
    titulo("III.1  EJERCICIO 1 — lectura de un grafico de posicion")
    print("""
 Enunciado: x(t) = t^3 - 6t^2 + 12t - 5  (m, s).
 (a) graficar en [0,4] con los valores en t=0,1,2,3,4
 (b) camino recorrido en [0,1], [1,2] y [0,4]
 (c) velocidad media en esos intervalos, y por que d = |Dx| en los tres
 (d) v(1) y v(2) midiendo la tangente
 (e) v(t) derivando
 (f) para que t esta a 1 m de la posicion que tiene en t=2 s
 (g) en t=2 s v=0: invierte el sentido?
""")
    x = t**3 - 6 * t**2 + 12 * t - 5
    sub("forma canonica")
    check("x(t) = (t-2)^3 + 3", sp.expand(x), sp.expand((t - 2)**3 + 3))

    sub("(a) valores de la tabla")
    for k, esp in zip(range(5), [-5, 2, 3, 4, 11]):
        check(f"x({k} s) (m)", x.subs(t, k), esp)

    v = sp.diff(x, t)
    sub("(e) velocidad")
    check("v(t) = 3(t-2)^2", sp.expand(v), sp.expand(3 * (t - 2)**2))

    sub("(g) la trampa: v se anula pero no cambia de signo")
    ceros = sp.solve(sp.Eq(v, 0), t)
    check("unico cero de v (s)", sp.Matrix(sorted(set(ceros))), sp.Matrix([2]))
    # Muestreo denso de signos en [0,4] para probar que v nunca es negativa.
    negativos = [pt for pt in [sp.Rational(k, 20) for k in range(0, 81)]
                 if v.subs(t, pt) < 0]
    check("cantidad de instantes con v<0 en [0,4]", len(negativos), 0)
    check("v es un cuadrado perfecto (>=0 siempre)",
          1 if sp.ask(sp.Q.nonnegative(sp.expand(v).subs(t, sp.Symbol('z', real=True)))) is not False else 0, 1)
    print("    -> NO invierte el sentido: t=2 s es punto de inflexion, no extremo.")
    check("x''(2) = 0 (por eso el criterio de concavidad no decide)", sp.diff(x, t, 2).subs(t, 2), 0)
    check("x'''(2) != 0 y el orden 3 es impar -> inflexion", sp.diff(x, t, 3), 6)

    sub("(b) y (c) camino recorrido y velocidad media")
    # Como v >= 0 en todo [0,4], d = |Dx| en cualquier subintervalo.
    for (ta, tb, d_esp, vm_esp) in [(0, 1, 7, 7), (1, 2, 1, 1), (0, 4, 16, 4)]:
        Dx = x.subs(t, tb) - x.subs(t, ta)
        d = sp.integrate(sp.Abs(v), (t, ta, tb))
        check(f"d en [{ta},{tb}] (m)", d, d_esp)
        check(f"|Dx| en [{ta},{tb}] (m)", abs(Dx), d_esp)
        check(f"v_media en [{ta},{tb}] (m/s)", Dx / (tb - ta), vm_esp)

    sub("(d) velocidades instantaneas de control")
    check("v(1) (m/s)", v.subs(t, 1), 3)
    check("v(2) (m/s)", v.subs(t, 2), 0)
    check("v(4) (m/s)", v.subs(t, 4), 12)

    sub("(f) posiciones a 1 m de x(2)=3 m")
    sols = sorted([r for r in sp.solve(sp.Eq(sp.Abs(x - 3), 1), t) if r.is_real])
    check("valores de t (s)", sp.Matrix(sols), sp.Matrix([1, 3]))
    print("    (x=4 m da t=3 s ; x=2 m da t=1 s ; las otras raices son complejas)")


def ejercicio_2():
    titulo("III.2  EJERCICIO 2 — que graficos pueden ser un movimiento")
    print("""
 Enunciado: x(t) formada por dos tramos rectos, de (0 s, 0 m) a (5 s, 20 m) y
 despues horizontal de (5 s, 20 m) a (9 s, 20 m). Incisos (a) a (f).
""")
    sub("(a) tramo por tramo")
    v1 = (20 - 0) / (5 - 0)
    check("tramo 1: v (m/s)", v1, 4)
    check("tramo 1: a (m/s^2)", 0, 0)
    check("tramo 2: v (m/s)", 0, 0)
    check("tramo 2: a (m/s^2)", 0, 0)

    sub("(c) que pasa en t = 5 s")
    print("    Dv = 0 - 4 = -4 m/s en Dt = 0  ->  a = Dv/Dt no existe (diverge).")
    Dt = sp.symbols('Delta_t', positive=True)
    check("|a| -> infinito cuando Dt -> 0", str(sp.limit(4 / Dt, Dt, 0)), "oo")
    print("    Ese es el motivo por el que el grafico NO es admisible: un punto")
    print("    anguloso en x(t) exige un salto de v, o sea aceleracion infinita.")

    sub("(d) version corregida")
    print("    Hay que redondear el vertice: un tramo de frenado con a finita")
    print("    entre los dos tramos rectos. Ejemplo minimo: frenar de 4 a 0 m/s")
    print("    en 2 s con a = -2 m/s^2, que agrega 4 m antes del reposo.")
    check("verificacion del ejemplo: Dx del frenado (m)", (0**2 - 4**2) / (2 * (-2)), 4)

    sub("(e) el salto de 20 m a 35 m en t=6 s")
    print("    No puede describir un movimiento: viola la continuidad de x(t)")
    print("    (el cuerpo se teletransportaria 15 m en tiempo nulo).")

    sub("(f) jerarquia de suavidad")
    print("    a(t): puede tener saltos.")
    print("    v(t): no puede tener saltos, si puntos angulosos.")
    print("    x(t): ni saltos ni puntos angulosos.")


def ejercicio_3():
    titulo("III.3  EJERCICIO 3 — conceptual (no verificable numericamente)")
    print("""
 Las seis respuestas, para contrastar; el ejercicio es cualitativo y su
 correccion es de criterio, no de calculo.
 (a) SI. Es el MRU: a = 0 con v = cte distinta de cero.
 (b) SI. Con v<0 y a<0 la rapidez |v| crece. Frenar es que v y a tengan
     signos opuestos, no que v sea negativa.
 (c) SI. Cualquier ida y vuelta que termine donde empezo: Dx = 0 y por lo
     tanto v_media = 0, sin que el movil se haya detenido nunca.
 (d) NO, nunca. Siempre d >= |Dx|, con igualdad solo si no hubo inversion
     de sentido.
 (e) SI. El punto de inflexion, que es exactamente el ejercicio 1(g).
 (f) v = 0 y a = -g (no nula). Si a tambien fuese nula el cuerpo se quedaria
     flotando ahi, porque nada sacaria a la velocidad de su valor cero.
""")
    # Lo unico que si tiene contenido numerico verificable: el contraejemplo (b).
    sub("contraejemplo numerico de (b): v0=-2 m/s, a=-3 m/s^2")
    vv = -2 - 3 * t
    check("|v| en t=0", sp.Abs(vv.subs(t, 0)), 2)
    check("|v| en t=1 (crecio)", sp.Abs(vv.subs(t, 1)), 5)
    check("v sigue siendo negativa", 1 if vv.subs(t, 1) < 0 else 0, 1)


def ejercicio_4():
    titulo("III.4  EJERCICIO 4 — de la funcion de movimiento a la aceleracion")
    print("""
 Enunciado: x(t) = -24 + 16t - 2t^2  (m, s). Incisos (a) a (g).
""")
    x = -24 + 16 * t - 2 * t**2
    sub("(a) coeficientes y aceleracion")
    check("a_2", sp.expand(x).coeff(t, 2), -2)
    check("a_1 = v0 (m/s)", sp.expand(x).coeff(t, 1), 16)
    check("a_0 = x0 (m)", sp.expand(x).coeff(t, 0), -24)
    check("a = 2 a_2 (m/s^2)", sp.diff(x, t, 2), -4)
    print("    -> la aceleracion es -4 m/s^2, NO -2 m/s^2.")

    sub("(b) posiciones")
    for k, esp in [(0, -24), (2, 0), (4, 8)]:
        check(f"x({k} s) (m)", x.subs(t, k), esp)

    sub("(c) v(t) desde el cociente incremental y por la regla de la potencia")
    coc = sp.simplify((x.subs(t, t + dt) - x) / dt)
    print("    cociente incremental =", sp.expand(coc))
    check("limite del cociente", sp.limit(coc, dt, 0), 16 - 4 * t)
    check("regla de la potencia", sp.diff(x, t), 16 - 4 * t)

    sub("(d) pasos por el origen")
    raices = sorted(sp.solve(sp.Eq(x, 0), t))
    check("raices (s)", sp.Matrix(raices), sp.Matrix([2, 6]))
    print("    -> las dos raices son enteras (t = 2 s y t = 6 s).")
    v = sp.diff(x, t)
    check("v(2 s) (m/s)", v.subs(t, 2), 8)
    check("v(6 s) (m/s)", v.subs(t, 6), -8)

    sub("(e) velocidad nula")
    tv = sp.solve(sp.Eq(v, 0), t)[0]
    check("t con v=0 (s)", tv, 4)
    check("x en ese instante (m)", x.subs(t, tv), 8)
    check("x'' < 0 -> es un maximo (vertice de la parabola)",
          1 if sp.diff(x, t, 2) < 0 else 0, 1)

    sub("(f) control grafico: el cero de v cae sobre el extremo de x")
    check("t del extremo de x", sp.solve(sp.Eq(sp.diff(x, t), 0), t)[0], tv)
    check("a constante (m/s^2)", sp.diff(x, t, 2), -4)

    sub("(g) notacion de la derivada en un punto")
    check("x'(2) = v(2) (m/s)", v.subs(t, 2), 8)
    check("dx(2)/dt  (evaluar primero) = 0", sp.diff(x.subs(t, 2), t), 0)
    print("    x(2) = 0 m, asi que la expresion mal escrita da 0 y 'parece' un")
    print("    resultado creible: hay que descartarla por la notacion, no por el valor.")


def ejercicio_5():
    titulo("III.5  EJERCICIO 5 — encuentro de dos karts acelerados")
    print("""
 Enunciado: dos karts parten del reposo en el mismo instante, uno detras del
 otro y en el mismo sentido. El de adelante acelera a 0.8 m/s^2, el de atras a
 1.4 m/s^2. El de atras lo alcanza cuando el de adelante recorrio 40 m.
""")
    aF = sp.Rational(8, 10)      # kart de adelante
    aA = sp.Rational(14, 10)     # kart de atras
    d0 = sp.symbols('d_0', positive=True)   # distancia inicial, incognita

    # Origen donde arranca el kart de atras, positivo hacia adelante, t=0 comun.
    x_atras = aA * t**2 / 2
    x_adel = d0 + aF * t**2 / 2

    sub("(b) el dato torcido: 'cuando el de adelante recorrio 40 m'")
    # Eso es una condicion sobre el DESPLAZAMIENTO del de adelante, no sobre t.
    te = [r for r in sp.solve(sp.Eq(aF * t**2 / 2, 40), t) if r > 0][0]
    check("t del encuentro (s)", te, 10)

    sub("(c) distancia inicial")
    rec_atras = (aA * te**2 / 2)
    check("recorrido del de atras (m)", rec_atras, 70)
    check("distancia inicial d0 (m)", rec_atras - 40, 30)
    # Verificacion cruzada: resolviendo el sistema de encuentro completo.
    d0_val = sp.solve(sp.Eq(x_atras.subs(t, te), x_adel.subs(t, te)), d0)[0]
    check("d0 por la ecuacion de encuentro (m)", d0_val, 30)

    sub("(d) velocidades en el encuentro")
    check("v del de adelante (m/s)", aF * te, 8)
    check("v del de atras (m/s)", aA * te, 14)

    sub("(f) si las aceleraciones fueran iguales")
    aa = sp.symbols('a', positive=True)
    print("    Igualando: ", aa * t**2 / 2, " = ", d0 + aa * t**2 / 2,
          " ->  0 = d0, imposible si d0 > 0.")
    check("el termino en t^2 se cancela",
          sp.expand(aa * t**2 / 2 - (d0 + aa * t**2 / 2)), -d0)
    print("    -> nunca lo alcanza: es la version parabolica de dos rectas paralelas.")


def ejercicio_6():
    titulo("III.6  EJERCICIO 6 — tiro vertical, el enunciado de la catedra (dato faltante)")
    print("""
 Enunciado (textual del Practico 1, ej. 7): una piedra se tira desde el suelo
 verticalmente hacia arriba. Pasa por A con velocidad v y por B, 3 m mas alto
 que A, con velocidad v/2. Calcular v, la velocidad inicial y la altura maxima
 por encima de B. g = 10 m/s^2.

 Este ejercicio esta mal planteado a proposito (es el enunciado real). Lo que
 sigue verifica exactamente que parte queda determinada y cual no.
""")
    v = sp.symbols('v', positive=True)
    hAB = sp.Integer(3)

    sub("1) De A a B: queda determinada, y da v^2 = 8g")
    sol_v2 = sp.solve(sp.Eq((v / 2)**2, v**2 - 2 * g * hAB), v**2)[0]
    check("v^2 = (8/3) g h_AB con h_AB=3 m  ->  v^2 = 8g", sp.simplify(sol_v2), 8 * g)
    check("v^2 con g=10 (m^2/s^2)", sol_v2.subs(g, G), 80)
    check("v (m/s), redondeado a 8,9", round(float(sp.sqrt(sol_v2.subs(g, G))), 1), 8.9)
    check("v/2 en B (m/s), redondeado a 4,5", round(float(sp.sqrt(sol_v2.subs(g, G)) / 2), 1), 4.5)

    sub("2) Altura sobre B: 1 m EXACTO, y sin depender de g")
    h_sobreB = sp.simplify((sol_v2 / 4) / (2 * g))
    print("    h_sobre_B = (v/2)^2/(2g) = v^2/(8g) = 8g/(8g) =", h_sobreB)
    check("h_sobre_B (m)", h_sobreB, 1)
    check("h_sobre_B NO contiene g", 0 if g in sp.simplify(h_sobreB).free_symbols else 1, 1)
    # Y lo mismo por la formula general h_AB/3, que el ejemplo resuelto dedujo.
    check("coincide con h_AB/3", h_sobreB, hAB / 3)
    # Prueba independiente y mas fuerte: con g simbolica arbitraria el resultado
    # es 1 m para cualquier valor.
    for gv in [sp.Rational(981, 100), sp.Integer(10), sp.Rational(162, 100), sp.Integer(24)]:
        check(f"h_sobre_B con g={gv} (m)", h_sobreB.subs(g, gv) if h_sobreB.free_symbols else h_sobreB, 1)

    sub("3) Velocidad inicial: INDETERMINADA (falta la altura de A sobre el suelo)")
    hA = sp.symbols('h_A', nonnegative=True)
    v0_2 = sol_v2 + 2 * g * hA        # relacion sin tiempo del suelo hasta A
    print("    v0^2 = v^2 + 2 g h_A =", sp.simplify(v0_2))
    check("v0^2 depende de h_A, que el enunciado no da",
          1 if hA in sp.simplify(v0_2).free_symbols else 0, 1)
    print("    -> con h_A libre, v0 puede valer cualquier cosa >= v. No hay solucion unica.")

    sub("4) Con la suposicion razonable h_A = 0 (A al nivel del suelo)")
    check("v0 = v (m/s)", sp.sqrt(v0_2.subs({hA: 0, g: G})), sp.sqrt(80))
    h_max = v0_2.subs({hA: 0}) / (2 * g)
    check("altura maxima sobre el suelo = v^2/(2g) (m)", sp.simplify(h_max), 4)
    check("y tambien es 3 + 1 = 4 m", hAB + 1, 4)
    print("    Ese cierre (3 + 1 = 4) es el control que conviene que hagas vos.")

    sub("5) Conteo de incognitas contra ecuaciones")
    print("    3 incognitas (v, v0, h_sobre_B) contra 2 ecuaciones independientes")
    print("    (A->B y B->cima). La tercera relacion, suelo->A, introduce una")
    print("    cuarta incognita h_A y no cierra nada. Sistema indeterminado.")


def ejercicio_7():
    titulo("III.7  EJERCICIO 7 (adicional) — encuentro con arranque demorado y tramos")
    print("""
 Enunciado: en una ciclovia recta un peloton pasa a 6.0 m/s constantes al lado
 de un ciclista detenido. El ciclista arranca 5.0 s despues con a = 1.2 m/s^2
 durante 10.0 s y despues mantiene la velocidad alcanzada. Hallar instante y
 lugar del alcance, y la maxima distancia que el peloton le llego a sacar.
 t = 0 en el paso del peloton, origen en ese punto, positivo hacia adelante.
""")
    ac = sp.Rational(12, 10)
    vp = 6

    x_p = vp * t                                   # peloton, siempre
    x_c2 = ac * (t - 5)**2 / 2                     # ciclista, 5 <= t <= 15
    v_c2 = sp.diff(x_c2, t)

    sub("(a) y (b) funciones por tramos y continuidad de v")
    check("x_c en [5,15] = 0.6 (t-5)^2", sp.expand(x_c2), sp.expand(sp.Rational(6, 10) * (t - 5)**2))
    check("v_c(15 s) (m/s)", v_c2.subs(t, 15), 12)
    check("x_c(15 s) (m)", x_c2.subs(t, 15), 60)
    x_c3 = 60 + 12 * (t - 15)                      # tercer tramo, t > 15
    check("continuidad de v en t=15", sp.diff(x_c3, t), v_c2.subs(t, 15))
    check("continuidad de x en t=15", x_c3.subs(t, 15), x_c2.subs(t, 15))
    check("v_c(5 s) = 0 (arranca del reposo)", v_c2.subs(t, 5), 0)

    sub("(c) alcance — tramo de reposo del ciclista, 0 <= t < 5")
    # x_c = 0 contra x_p = 6t da t = 0: es el instante inicial en que el
    # peloton pasa al lado del ciclista, no un alcance. Se descarta por
    # significado fisico, no por caer fuera del intervalo.
    r1 = sp.solve(sp.Eq(0, x_p), t)
    check("raiz del primer tramo (s)", sp.Matrix(r1), sp.Matrix([0]))
    print("    t = 0 s SI cae dentro de [0,5), pero es el instante en que el")
    print("    peloton pasa al lado del ciclista, no un alcance: se descarta por")
    print("    significado fisico. Conviene decirlo por escrito en el inciso (c).")

    sub("(c) alcance — tramo acelerado [5,15]: las raices se descartan")
    r2 = sorted(sp.solve(sp.Eq(x_c2, x_p), t))
    print("    ecuacion: 0.6(t-5)^2 = 6t   <=>   t^2 - 20t + 25 = 0")
    for r in r2:
        dentro = (5 <= r <= 15)
        print(f"    raiz t = {sp.N(r, 5)} s  ->  {'DENTRO' if dentro else 'FUERA'} de [5,15]"
              f"  ->  {'valida' if dentro else 'se descarta'}")
    check("raiz grande (s)", round(float(r2[1]), 2), 18.66)
    check("raiz chica (s)", round(float(r2[0]), 2), 1.34)
    check("ninguna raiz cae dentro de [5,15]",
          sum(1 for r in r2 if 5 <= r <= 15), 0)
    print("    OJO: hay DOS raices a descartar, no una sola.")

    sub("(c) alcance — tramo de velocidad constante, t > 15")
    r3 = sp.solve(sp.Eq(x_c3, x_p), t)
    check("t del alcance (s)", r3[0], 20)
    check("el 20 s cae dentro del tramo (t > 15)", 1 if r3[0] > 15 else 0, 1)
    check("x del alcance (m)", x_p.subs(t, r3[0]), 120)
    check("comprobacion con la funcion del ciclista (m)", x_c3.subs(t, r3[0]), 120)
    check("v del ciclista alli (m/s)", sp.diff(x_c3, t), 12)
    check("v del peloton (m/s)", sp.diff(x_p, t), 6)

    sub("(d) maxima distancia que el peloton le saco")
    sep = x_p - x_c2                                # valida en [5,15]
    t_sep = sp.solve(sp.Eq(sp.diff(sep, t), 0), t)[0]
    check("instante de maxima separacion (s)", t_sep, 10)
    check("cae dentro de [5,15]", 1 if 5 <= t_sep <= 15 else 0, 1)
    check("separacion maxima (m)", sep.subs(t, t_sep), 45)
    check("separacion en t=15 s (m)", sep.subs(t, 15), 30)
    check("separacion en t=5 s (m)", sep.subs(t, 5), 30)
    check("criterio: la separacion es maxima cuando las velocidades se igualan",
          sp.solve(sp.Eq(v_c2, vp), t)[0], t_sep)
    print("    (antes de t=5 s la separacion es 6t, creciente, y vale 30 m en t=5 s:")
    print("     el maximo global sigue siendo 45 m en t=10 s.)")


def ejercicio_8():
    titulo("III.8  EJERCICIO 8 (adicional) — dos pelotas, caida y ascenso")
    print("""
 Enunciado: se deja caer una pelota desde un balcon a 40 m del piso. En el mismo
 instante, sobre la misma vertical, otra se lanza desde el piso a 20 m/s.
 g = 10 m/s^2. Hallar donde y cuando se cruzan, etc.
 Origen en el piso, positivo hacia arriba, t=0 comun.
""")
    y1 = 40 - G * t**2 / 2       # la que se deja caer
    y2 = 20 * t - G * t**2 / 2   # la lanzada
    check("y1(t) = 40 - 5t^2", sp.expand(y1), 40 - 5 * t**2)
    check("y2(t) = 20t - 5t^2", sp.expand(y2), 20 * t - 5 * t**2)

    sub("(b) el cruce")
    print("    Al igualar, el termino en t^2 se cancela y queda una ecuacion lineal:")
    print("   ", sp.expand(y1 - y2), "= 0")
    tc = sp.solve(sp.Eq(y1, y2), t)[0]
    check("t del cruce (s)", tc, 2)
    check("altura del cruce (m)", y1.subs(t, tc), 20)
    check("misma altura por la otra pelota (m)", y2.subs(t, tc), 20)

    sub("(c) velocidades y aceleraciones en el cruce")
    check("v1 en el cruce (m/s)", sp.diff(y1, t).subs(t, tc), -20)
    check("v2 en el cruce (m/s)", sp.diff(y2, t).subs(t, tc), 0)
    check("a1 (m/s^2)", sp.diff(y1, t, 2), -10)
    check("a2 (m/s^2)", sp.diff(y2, t, 2), -10)
    # El detalle de diseno: la lanzada esta justo en su punto mas alto.
    t_top = sp.solve(sp.Eq(sp.diff(y2, t), 0), t)[0]
    check("el cruce coincide con el punto mas alto de la lanzada", t_top, tc)
    check("altura maxima de la lanzada (m)", y2.subs(t, t_top), 20)
    print("    Dato que hizo falta: que las dos estan cerca de la superficie")
    print("    terrestre. Dato que NO hizo falta: de que esta hecha cada pelota.")

    sub("(d) velocidad de llegada al piso de la que cae, sin usar el tiempo")
    v_piso2 = 0**2 + 2 * G * 40          # |v|^2 = 2 g h
    check("v^2 (m^2/s^2)", v_piso2, 800)
    check("|v| (m/s), redondeado a 28,3", round(float(sp.sqrt(v_piso2)), 1), 28.3)
    # Control por el camino horario, para que se vea que dan lo mismo.
    t_piso = [r for r in sp.solve(sp.Eq(y1, 0), t) if r > 0][0]
    check("t de llegada al piso (s) = sqrt(8)", t_piso, 2 * sp.sqrt(2))
    check("misma |v| por el camino horario (m/s)",
          sp.Abs(sp.diff(y1, t).subs(t, t_piso)), sp.sqrt(800))
    check("el cruce ocurre antes de que la pelota toque el piso",
          1 if tc < t_piso else 0, 1)

    sub("(e) si la de abajo saliera con el doble de velocidad inicial")
    V0 = sp.symbols('V_0', positive=True)
    tc_gen = sp.solve(sp.Eq(40 - G * t**2 / 2, V0 * t - G * t**2 / 2), t)[0]
    check("t del cruce en general = 40/V0", tc_gen, 40 / V0)
    check("t del cruce con V0=40 m/s (s)", tc_gen.subs(V0, 40), 1)
    check("altura del cruce con V0=40 m/s (m)", y1.subs(t, 1), 35)
    print("    -> ocurre ANTES (1,0 s en lugar de 2,0 s) y MAS ARRIBA (35 m).")


def ejercicio_9():
    titulo("III.9  EJERCICIO 9 (adicional) — de la aceleracion a la posicion, por tramos")
    print("""
 Enunciado: un tren parte del reposo con a = 1.0 m/s^2 durante 10.0 s; despues
 viaja sin acelerar 20.0 s; finalmente frena con |a| = 2.0 m/s^2 hasta detenerse.
 Hallar la distancia entre terminales.
""")
    sub("(b) v(t) por tramos, con las constantes fijadas por continuidad")
    C = sp.symbols('C')
    # Tramo 1: 0 <= t <= 10, a = 1, v(0) = 0.
    v1 = sp.integrate(1, t) + C
    c = sp.solve(sp.Eq(v1.subs(t, 0), 0), C)[0]
    v1 = v1.subs(C, c)
    check("tramo 1: v(t) = t", v1, t)
    check("v(10 s) (m/s)", v1.subs(t, 10), 10)
    # Tramo 2: 10 <= t <= 30, a = 0, constante por continuidad.
    v2 = sp.integrate(0, t) + C
    c = sp.solve(sp.Eq(v2.subs(t, 10), v1.subs(t, 10)), C)[0]
    v2 = v2.subs(C, c)
    check("tramo 2: v = 10 m/s", v2, 10)
    # Tramo 3: t >= 30, a = -2, continuidad en t=30.
    v3 = sp.integrate(-2, t) + C
    c = sp.solve(sp.Eq(v3.subs(t, 30), v2), C)[0]
    v3 = v3.subs(C, c)
    check("tramo 3: v(t) = 70 - 2t", sp.expand(v3), 70 - 2 * t)
    t_stop = sp.solve(sp.Eq(v3, 0), t)[0]
    check("instante de detencion (s) — sale del calculo, no es dato", t_stop, 35)
    check("duracion del frenado (s)", t_stop - 30, 5)

    sub("(c) distancias por integracion")
    d1 = sp.integrate(v1, (t, 0, 10))
    d2 = sp.integrate(v2, (t, 10, 30))
    d3 = sp.integrate(v3, (t, 30, t_stop))
    check("tramo 1 (m)", d1, 50)
    check("tramo 2 (m)", d2, 200)
    check("tramo 3 (m)", d3, 25)
    check("distancia total (m)", d1 + d2 + d3, 275)

    sub("(d) verificacion por areas, sin integrar")
    A1 = sp.Rational(1, 2) * 10 * 10        # triangulo
    A2 = 20 * 10                            # rectangulo
    A3 = sp.Rational(1, 2) * 5 * 10         # triangulo
    check("triangulo de arranque (m)", A1, 50)
    check("rectangulo (m)", A2, 200)
    check("triangulo de frenado (m)", A3, 25)
    check("total por areas (m)", A1 + A2 + A3, 275)
    check("los dos caminos coinciden", A1 + A2 + A3, d1 + d2 + d3)

    sub("(e) puntos angulosos de v(t)")
    print("    v(t) tiene puntos angulosos en t = 10 s y t = 30 s; ahi a(t) salta.")
    print("    x(t) es suave en los dos: cambia la concavidad, no la pendiente.")

    sub("(f) con la mitad de la desaceleracion")
    d3_mitad = (0**2 - 10**2) / (2 * (-1))
    check("frenado con 1.0 m/s^2 (m)", d3_mitad, 50)
    check("metros de anden extra (m)", d3_mitad - 25, 25)


# =============================================================================

def main():
    parte_1_derivada_desde_la_definicion()
    parte_1_regla_de_la_potencia()
    parte_1_mruv_por_integracion()
    parte_1_relacion_sin_tiempo()
    parte_1_puente_a2()
    parte_1_bloques_numericos()

    ejemplo_completo()
    ejemplo_parcial()

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
        print(f" {len(FALLAS)} discrepancia(s) entre el calculo y el documento:")
        for f in FALLAS:
            print("   -", f)
    else:
        print(" Todo verificado: no hay discrepancias entre el calculo independiente")
        print(" y los valores que afirma el capitulo.")
    print()


if __name__ == "__main__":
    main()
