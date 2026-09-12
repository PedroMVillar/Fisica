# Plataforma de Física 1 — Guía 3: trabajo, energía y cantidad de movimiento · Plan de implementación

> **Para trabajadores agénticos:** SUB-SKILL REQUERIDA: usar superpowers:subagent-driven-development (recomendada) o superpowers:executing-plans para implementar este plan tarea por tarea. Los pasos usan sintaxis de casilla (`- [ ]`) para seguimiento.

**Objetivo:** escribir los dos ensayos que cubren la Guía 3 entera —trabajo y energía (ej. 1-8) y cantidad de movimiento (ej. 9-12)—, con siete widgets, una primitiva de motor nueva, y los números concretos que hoy le faltan al script de verificación.

**Arquitectura:** el plan anterior dejó seis ensayos y un motor que sabe dibujar fuerzas. Éste no agrega un tipo de página nuevo: agrega **un idioma de lectura nuevo**. Hasta acá lo que tenía que «dar bien» era una suma de vectores que se cancelaba; de acá en adelante lo que tiene que dar bien es un **total que se reparte y no cambia** —energía en el ensayo 7, cantidad de movimiento en el 8—. Eso pide exactamente una primitiva: una barra apilada contra un total declarado. Todo lo demás sale de lo que ya hay.

**Stack:** ES modules vanilla, canvas 2D, `node --test` de Node 22, GitHub Pages desde `/docs`.

**Spec:** `docs/plataforma/brief.md`

**Autoridad de diseño:** `docs/plataforma/diseno/Tiro parabolico.dc.html`

## Decisiones tomadas antes de escribir este plan

**Separador decimal: coma, en todos lados.** En prosa y en las lecturas de los widgets por igual. El plan de pago de deuda que corre **antes** que éste deja `docs/motor/formato.js` con `num()` y `exp()`, y convierte los 117 usos de `toFixed` que hay hoy. **Las páginas de este plan usan esos helpers desde la primera línea**: en ningún archivo nuevo aparece un `toFixed` suelto. La firma exacta de `num()`/`exp()` se lee del archivo antes de escribir el primer widget —no se adivina—; en los fragmentos de este plan aparecen como `num(valor, decimales)` a modo ilustrativo, y si la firma real difiere, manda el archivo.

**Clases tipográficas en vez de atributos `style`.** El mismo plan de deuda suma **diez clases tipográficas** a `docs/estilos/base.css`, encima de las nueve que ya existen (`.columna`, `.columna-final`, `.banda`, `.marco-widget`, `.encabezado-widget`, `.boton`, `.boton-primario`, `.control`, `.lecturas`). Son `.lectura-valor` (con sus modificadores `.roja`, `.azul` y `.tenue`), `.valor-control`, `.parrafo`, `.parrafo-suelto`, `.titulo-seccion`, `.rotulo-mono`, `.rotulo-campo`, `.titulo-fila`, `.nota-fila` y `.negrita` — leídas de `base.css` al corregir este plan, no adivinadas. **El implementador las vuelve a leer del archivo** y no inventa ninguna.

**Una clase más, agregada durante la ejecución: `.lectura-valor.grafico`.** `.lectura-valor`
traía modificadores `.roja`, `.azul` y `.tenue`, y **ninguno para `--graph`** — que es
justo el color de la energía potencial en la extensión semántica que aprobó el dueño. La
Tarea 4 resolvió esa lectura con un `style="color:var(--graph)"` inline, y la revisión
señaló, con razón, que deja el tercer color de una misma fila de lecturas fuera del patrón
que los otros dos sí usan. El precedente que se había invocado —el `style="color:var(--dim)"`
de `index.html`— no aplicaba: ése es sobre `.titulo-fila`, una clase que no tiene
modificadores de color. Como `--graph` vuelve a aparecer en las Tareas 7, 8 y 9 con el
mismo significado, la clase se agrega una vez y se usa en todas. **Las lecturas en `--graph`
de las tareas siguientes usan `.lectura-valor grafico`, no un `style` inline.**

**Lo que esas diez clases NO cubren, y cómo se resuelve la contradicción.** Medido: `base.css` **no tiene clase** para el `<h1>`, el kicker, la bajada, la `<ol>` de cierre, el pie ni la línea de fuentes. Y el esqueleto de `cuerpo-aislado.html` —que las Tareas 3 y 7 mandan copiar— lleva **28 atributos `style`**, nueve de ellos tipográficos, que son justamente los de esos elementos. Una regla que dijera «ningún `style` tipográfico nuevo en la página» contradiría, en la misma página, la orden de copiar el esqueleto. La regla real, entonces, es:

> **Los `style` tipográficos que se copian del esqueleto se conservan idénticos; ninguno nuevo se inventa.**

Todo elemento que sí tenga clase la usa. Si hace falta un nivel tipográfico que no está ni en el esqueleto ni en `base.css` —el caso concreto es el `<h3>` de las Tareas 4 y 5—, se **reusa una clase existente** antes que escribir un `style` a mano: `.titulo-seccion` sin numerar, que es lo que `cuerpo-aislado.html` ya hace con `Cinco variantes del mismo dibujo` y `Para tener a mano`. Se evaluó y se descartó la alternativa de una Tarea 0 que metiera `.titulo-ensayo`, `.bajada`, `.kicker`, `.subtitulo` y `.lista-reglas` en `base.css`: es más grande que el problema, y deja el sitio con dos convenciones para lo mismo hasta que se migren los seis ensayos viejos. Eso es trabajo de otro plan de deuda, no de éste.

**Numeración de ensayos.** 1 derivada e integral · 2 tiro parabólico · 3 movimiento circular · 4 cuerpo aislado · 5 sistemas acoplados · 6 fuerzas que dependen de la posición · **7 energía · 8 cantidad de movimiento**. La portada tiene hoy una fila sin enlace para el 7 (`docs/index.html:57-60`) y **ninguna** para el 8: la Tarea 10 crea la fila que falta y enlaza las dos.

**Cantidad de movimiento es un ensayo aparte, no la sección final del de energía.** Está argumentado con evidencia en `.superpowers/investigacion-guia-3/cantidad-de-movimiento.md` §3 y se toma como cerrado. En una línea: son dos leyes de conservación con condiciones de validez distintas (el teorema trabajo-energía vale siempre que se cuenten todas las fuerzas; la conservación de *p* exige que no haya fuerzas **externas**, y no le importan las internas), y `sistemas-acoplados.html` ya probó que cuatro ejercicios bien elegidos son un ensayo completo en esta plataforma.

## Global Constraints

Aplican a todas las tareas.

- **Cero dependencias de runtime** salvo KaTeX por CDN. Nada de `npm install`.
- **Cero build.** Lo que está en el repositorio es lo que sirve el navegador.
- **Los tokens de color son exactamente estos**, y no se inventa ninguno:
  claro `--paper:#fbfaf7` `--band:#f2f0ea` `--ink:#16151a` `--dim:#6a6760`
  `--rule:#dcd8ce` `--blue:#1b4fd4` `--blue-soft:#8aa3e6` `--red:#c02a24`
  `--graph:#8e8a80`; oscuro `--paper:#131316` `--band:#191a1e` `--ink:#eceae4`
  `--dim:#948f86` `--rule:#2e2f35` `--blue:#7aa2ff` `--blue-soft:#3f5694`
  `--red:#ef5f52` `--graph:#6f6c66`. Nunca se escriben literales hex en JS.
- **Reparto semántico:** azul para cinemática y velocidad; rojo para aceleración y para
  cada fuerza que actúa; azul para la resultante de las fuerzas; `--graph` para la
  trayectoria. **Extensión aprobada por el dueño el 2026-09-12,
  antes de escribir una línea:** en una barra de energía o de cantidad de movimiento, **azul =
  cinética / cantidad de movimiento** (es cinemática), **`--graph` = potencial**
  (gravitatoria o elástica: es «dónde está», no «cómo se mueve»), **rojo = lo que se
  disipó** (calor de rozamiento, trabajo del freno: sale de una fuerza). No agrega ningún
  color nuevo, pero sí le da un significado nuevo a tres que ya existen, y por eso se
  preguntó en vez de asumirlo.
- **Separador decimal coma, vía `num()`/`exp()` de `docs/motor/formato.js`.** Cero
  `toFixed` en archivos nuevos.
- **Tipografía por clase de `base.css` donde hay clase.** Los `style` tipográficos que se
  copian del esqueleto de `cuerpo-aislado.html` se conservan **idénticos**; **ninguno
  nuevo se inventa**. Ver «Clases tipográficas» arriba: `base.css` no tiene clase para el
  `<h1>`, el kicker, la bajada, la `<ol>` de cierre, el pie ni la línea de fuentes.
- **Una página es un módulo y un espacio de nombres.** Cada ensayo es **un solo**
  `<script type="module">`, así que **los helpers por widget van sufijados** con el prefijo
  de sus ids: `MARGEN_W1`, `HUECO_ROTULO_M1`, `ALTO_PANEL_MINIMO_M2`… Es lo que ya hace
  `cuerpo-aislado.html` con `MARGEN2`/`HUECO_ROTULO2`/`ALTO_PANEL_MINIMO2` y `MARGEN3`
  (líneas 421-423 y 598). Dos `const` con el mismo nombre en el mismo módulo son un
  `SyntaxError` que no deja ni cargar la página. Las constantes **físicas** que comparte
  toda la página (`G`) se declaran una sola vez, arriba de todo, fuera del bloque de
  cualquier widget.
- **Todo rótulo que cuelgue de un cuerpo, una flecha o un punto pasa por
  `colocarEtiqueta`** (`docs/motor/etiqueta.js`) — de preferencia por la opción `rotulo:`
  de `vectorPx`, que la llama por dentro. **`texto()` directo queda para rótulos de
  posición fija dentro de una caja**: los segmentos de `presupuestoPx` y las marcas
  internas de `eje()`, y nada más. El plan de deuda que corre antes que éste existió en
  buena parte para migrar esas llamadas (commit `8a88de6` y siguientes); volver a
  escribirlas sería deshacerlo en la misma semana.
- **El segundo límite documentado de `etiqueta.js`, que este plan pisa tres veces:**
  `crearWidget` le pasa el `{ancho, alto}` del **canvas entero** como límites, también
  para un widget de `panelesApilados` que sólo dibuja en una franja. El recorte de borde y
  el esquive de colisiones no conocen el borde del panel, así que un rótulo cerca de la
  frontera puede terminar empujado **al panel vecino**. Tres de los siete widgets nuevos
  usan `panelesApilados` —Tarea 3, Tarea 7 y Tarea 8—, y el de la Tarea 8 tiene los
  rótulos de las flechas justo contra esa frontera. Si al verificar aparece un rótulo en
  el panel de al lado, es esto y no un error de cuenta: se corrige alejando el `rdy` del
  borde, no tocando el motor.
- **Un deslizador que reescribe el código no repinta su `<output>` ni avisa a nadie.**
  `deslizador()` actualiza la salida sólo dentro de su listener de `'input'`, y asignar
  `.value` desde JS no dispara ningún evento. El patrón del sitio está en
  `movimiento-circular.html:513`: asignar y después `entrada.dispatchEvent(new Event('input'))`.
  Aplica al cambio de modo de la **Tarea 4** (que reescribe el μ por defecto) y a los dos
  botones de preset de la **Tarea 7** (que mueven dos deslizadores de una).
- **Tipografías:** Source Serif 4 para el contenido, JetBrains Mono para la interfaz.
- **Grilla:** columna de texto `max-width:680px` con `padding:0 24px`, widget
  `max-width:880px` dentro de una franja a todo el ancho.
- **Canvas:** `width:100%`, `aspect-ratio:16/8`, `touch-action:none`.
- **Ningún widget se anima solo al cargar.**
- **Ningún número aparece sin respaldo** en `verificacion-practico-3.py`. Los cuatro
  bloques que hoy faltan los agrega la Tarea 1, **antes** de escribir una línea de HTML.
- **Todo widget lleva su frase de «qué mirar»** en su encabezado, en `--dim`.
- **Todo widget lleva al menos una lectura que se rompe si el modelo se rompe**, y esa
  lectura se calcula por un camino **distinto** del que dibuja la escena. En este plan
  casi siempre es una resta que tiene que dar cero; dónde eso no alcanza —y por qué—
  está dicho explícitamente en la tarea.
  **Y la prueba de que un camino es distinto no es que el código lo parezca: es que la
  resta se pueda mover.** Una resta que da cero *por construcción* —porque las dos partes
  vienen de la misma ecuación despejada de dos maneras— no es un canario, es decoración, y
  encima miente diciendo que algo está verificado. El razonamiento está desarrollado en la
  **Tarea 4 Paso 2**, y la **Tarea 6 Paso 4** muestra el caso concreto donde este plan
  cayó en la trampa y cómo se sale: cada chequeo nuevo se acompaña del número que da
  **bajo un modelo plausiblemente equivocado**, corrido, no razonado.
- **Las rutas se verifican sirviendo `docs/` como raíz**, que es lo que hace GitHub
  Pages. Servir el repositorio entero esconde enlaces rotos: así se escapó un defecto
  crítico dos planes atrás.
- **Al comparar bitmaps**, usar `.superpowers/sdd/2026-09-11-plataforma-guia-1/comparar-bitmaps.mjs`,
  que lanza un proceso de Chrome nuevo por medición. Reusar el proceso da falsos
  «idéntico» aunque el código haya cambiado.
- Nombres en español. Las pruebas corren con `node --test "test/**/*.test.js"` desde la
  raíz del worktree. **Línea de base medida en `78822be`, corriendo la suite: 240 pruebas,
  0 fallas.** (El plan se escribió contra 224; el plan de pago de deuda sumó 16 antes de
  que éste empezara.)
- **Los scripts de verificación viven en el repositorio de al lado.** Es
  `../Ejercicios-prácticos/parcial-1/soluciones/verificacion-practico-3.py`, y **la
  Tarea 1** le agrega cuatro bloques. Ese cambio va con su **propio commit**, en ese
  repositorio, y no entra en los commits de la plataforma. Es la única escritura fuera
  de este worktree que el plan autoriza: cualquier otra, se pregunta.

## Estructura de archivos

**Motor, modificados:**

| Archivo | Qué cambia |
|---|---|
| `docs/motor/dibujo.js` | suma `presupuestoPx`: una barra apilada contra un total **declarado** |

**Páginas nuevas:**

| Archivo | Qué es |
|---|---|
| `docs/ensayos/energia.html` | ensayo 7, cuatro widgets, práctico 3 ej. 1-8 |
| `docs/ensayos/cantidad-de-movimiento.html` | ensayo 8, tres widgets, práctico 3 ej. 9-12 |

**Páginas modificadas:**

| Archivo | Qué cambia |
|---|---|
| `docs/index.html` | la fila del ensayo 7 se enlaza; se crea y se enlaza la del 8 |
| `docs/ensayos/fuerzas-de-posicion.html` | nada de contenido: sólo se comprueba que su pie siga cerrando bien la cadena hacia atrás |
| `README.md` | los dos ensayos nuevos en la lista |

**Recursos:**

| Archivo | Qué es |
|---|---|
| `docs/recursos/practico_3_2026.pdf` | copia de `../Ejercicios-prácticos/parcial-1/practicos/Practico 3.pdf`; hoy sólo están los prácticos 1 y 2, y los pies de los dos ensayos nuevos lo enlazan |

**Repositorio de al lado (un commit propio, Tarea 1):**

| Archivo | Qué cambia |
|---|---|
| `../Ejercicios-prácticos/parcial-1/soluciones/verificacion-practico-3.py` | cuatro bloques numéricos nuevos: Ej 2 con θ concreto, Ej 7 con v₀/h/L concretos, Ej 10 y 12 con los valores por defecto del widget, y un choque general de blindaje |

**Pruebas:** se extiende `test/dibujo.test.js` (seis pruebas nuevas para `presupuestoPx`,
y su `ctxFalso` gana `fillRect` y `strokeRect`, que hoy no tiene).

**Lo que este plan NO hace:** no toca el contenido de los seis ensayos existentes; no
rediseña la portada (eso es del dueño); no agrega hoja resumen para la Guía 3 —no existe
todavía en `../Ejercicios-prácticos/parcial-1/preparacion/`, así que los pies citan sólo
el práctico.

## Las diez tareas

| Fase | Tareas | Qué deja |
|---|---|---|
| A — cimientos | 1, 2 | los números que faltan en el script, el PDF del práctico, y `presupuestoPx` en el motor |
| B — ensayo 7 | 3, 4, 5, 6 | `energia.html` con sus cuatro widgets y su cierre |
| C — ensayo 8 | 7, 8, 9 | `cantidad-de-movimiento.html` con sus tres widgets y su cierre |
| D — cerrar | 10 | portada, navegación, README, recorrido completo |

## Qué cubre de la Guía 3, ejercicio por ejercicio

La tabla existe para que la frase «cubre la Guía 3 entera» se pueda auditar en lugar de
creer. **Cada fila fue contrastada contra el contenido que este plan realmente manda
escribir**, no contra la intención: donde dice «widget» hay un widget en una tarea de
este plan, y donde dice «prosa» hay una sección nombrada en un paso concreto. El plan
anterior tuvo una fila que afirmaba cobertura donde no la había; por eso esta tabla se
vuelve a revisar, fila por fila, en el Paso 4 de la Tarea 10.

| Ej. | Tema | Dónde | Tarea |
|---|---|---|---|
| 1 | péndulo que engancha en un clavo | ensayo 7, widget 3 | 5 |
| 2 | trabajo de una fuerza variable a un ángulo | ensayo 7, widget 1 | 3 |
| 3 | plano inclinado con y sin rozamiento | ensayo 7, widget 2, modo «plano» | 4 |
| 4 | resorte horizontal + rozamiento | ensayo 7, widget 2, modo «resorte» | 4 |
| 5 | resorte vertical: apoyar vs. soltar | ensayo 7, prosa de la sección 02, subtítulo «Apoyar no es soltar» | 4 |
| 6 | embalaje colgado y apartado de la vertical | ensayo 7, prosa de la sección 03, subtítulo «Lo mismo, sin nada que gire» | 5 |
| 7 | montaña rusa sin fricción con freno | ensayo 7, widget 4, escena «montaña rusa» | 6 |
| 8 | cuadrante circular + tramo con rozamiento | ensayo 7, widget 4, escena «el cuadrante» | 6 |
| 9 | impulso sobre un cuerpo que cae | ensayo 8, widget 1 | 7 |
| 10 | choque elástico frontal, masas iguales | ensayo 8, widget 2, con restitución e = 1 (la posición por defecto del deslizador) | 8 |
| 11 | bala que atraviesa dos bloques | ensayo 8, widget 3 | 9 |
| 12 | cuerpo que se parte en dos en el espacio | ensayo 8, widget 2, modo «explosión» | 8 |

Doce de doce. Diez tienen widget; dos (5 y 6) están en prosa, con todos sus números,
dentro de la sección del ensayo que trata su mismo hecho físico.

## Qué se verificó corriendo y qué no

Este plan se escribió con la regla de que **ninguna afirmación numérica o geométrica se
anota sin haberla ejecutado antes**. Lo que sigue dice hasta dónde llegó esa ejecución,
para que la revisión sepa dónde apretar.

**Verificado corriendo, y los números de las tareas son salida real:**

- `verificacion-practico-3.py` completo (`python verificacion-practico-3.py`).
- Los cuatro bloques nuevos de la Tarea 1: escritos, corridos con sympy, y su salida está
  transcripta literal en el Paso 3 de esa tarea.
- `presupuestoPx`: implementada, sus seis pruebas corridas en verde, y además **mutada**:
  seis implementaciones plausiblemente equivocadas (normalizar por la suma en vez de por
  el total, clipear en silencio, estirar para llenar, sin guarda de total cero, sin
  guarda de negativos, rotular siempre) y **las seis las caza la suite**. La que
  normaliza por la suma rompe tres pruebas de seis.
- Todos los encuadres: medidos llamando al `crearWidget` **real** con un canvas y un
  contexto falsos, a 880 px (franja de widget en escritorio) y a 350 px (la misma franja
  en un viewport de 390), leyendo `l.escala` y `l.margen` de vuelta. Los px/unidad de
  cada widget salen de ahí.
- Todas las escalas de flecha y de barra: evaluadas en la posición por defecto **y en los
  dos extremos** de cada deslizador.
- Las duraciones de las tres animaciones (plano, resorte, montaña rusa): integradas
  numéricamente.
- Los límites físicos de los deslizadores: el ángulo donde el bloque del Ej 2 deja de
  llegar a x = 20 m (80,89°), el θ_A donde la cuerda del Ej 1 se afloja (60°), el μ donde
  el bloque del Ej 3 ya no arranca (tan 30° = 0,5774).

**Agregado al corregir este plan (2026-09-12), también corrido:**

- **La marcha de Newton del widget 4** (Tarea 6 Paso 2 y Paso 4): implementada y corrida.
  Reproduce los cinco números que el perfil ya tenía verificados por el otro camino
  (v_B = 2,0000 · v_C = 5,7793 · v_D = 7,9246 m/s · s = 11,6561 m · t = 2,6146 s), su
  residuo contra la forma cerrada es 1,7 × 10⁻⁵ m/s barriendo los dos deslizadores
  enteros, y **bajo un modelo plausiblemente equivocado** (seno por tangente) salta a
  2,3141 m/s. El chequeo del freno, ídem: 3,1 × 10⁻⁵ m/s² contra 2,5434 m/s².
- **El encuadre del cuadrante** (Tarea 6 Paso 5), medido de nuevo contra el `crearWidget`
  real con `xMax: 4.5`: 154,55 px/m a 880 y 60,41 px/m a 350, con el punto de detención
  adentro del marco en los dos.
- **La cadena de flechas del panel 3 de la Tarea 8**, medida contra el `crearWidget` y el
  `panelesApilados` reales en las dos esquinas del rango de deslizadores.
- **La resta del «rompelo a propósito» de la Tarea 4** (0,788 J, no 0,682).
- **La línea de base de la suite** (240) y los nombres de las diez clases de `base.css`.

**NO verificado, y hay que verificarlo al implementar:**

- **Nada se abrió en un navegador.** Ningún número de este plan salió de una captura.
  Todo lo medido es aritmética del motor, no pintura real: los pasos de «verificar» de
  cada tarea piden abrir la página y medir, y esa medición manda sobre lo escrito acá.
- **La firma exacta de `num()`/`exp()`** de `docs/motor/formato.js`: el archivo ya existe
  en `78822be`, pero este plan no leyó sus firmas línea por línea. Se leen antes de usarlas.
- **Los nombres de las diez clases tipográficas** de `base.css`: leídos del archivo al
  corregir este plan y transcriptos arriba. Se vuelven a leer antes de escribir HTML.
- **El perfil de la montaña rusa** (Tarea 6) es una invención de este plan: el práctico
  da una figura sin coordenadas. Los nodos que propongo respetan las únicas alturas que
  el enunciado fija (A y B en *h*, C en *h*/2, D-E en 0) y todo lo demás es decisión de
  dibujo, revisable.
- **El aspecto del bloque en la escena del widget 1** a 350 px: con `escalaUniforme:
  false` ese panel es anisótropo (67,00 px/m en x contra 112,14 px/unidad en y, a 880 px),
  así que el bloque se dibuja pidiendo píxeles y dividiendo por la escala de cada eje.
  Está calculado, no visto.
- **Ningún texto de prosa está escrito.** Este plan dice qué tiene que decir cada párrafo
  y con qué números; la redacción es del implementador, con la voz de
  `docs/ensayos/cuerpo-aislado.html`.

---

## Fase A — cimientos

### Tarea 1: Los números que la Guía 3 todavía no tiene

Dos de los ocho ejercicios de energía están **totalmente simbólicos** en el script de
verificación: el Ej 2 no evalúa ningún θ y el Ej 7 no evalúa ningún v₀, h ni L. Dos de
los cuatro de cantidad de movimiento (10 y 12) tienen respuesta simbólica correcta pero
sin masas ni velocidades concretas, y los widgets muestran joules y newton·segundo, que
necesitan las dos cosas. Mientras eso no esté, cualquier widget que los toque estaría
inventando sus números — que es exactamente lo que la Global Constraint prohíbe.

**Archivos:**
- Modificar: `../Ejercicios-prácticos/parcial-1/soluciones/verificacion-practico-3.py`
- Crear: `docs/recursos/practico_3_2026.pdf`

**Interfaces:**
- Produce: cuatro bloques nuevos de salida en el script (`Ej 2 (numerico)`,
  `Ej 7 (numerico)`, `Ej 10 y 12 (numerico)`, `Choque general`), que son la fuente de
  todo número de los siete widgets; y el PDF del práctico dentro de `docs/`, para que los
  pies de los dos ensayos puedan enlazarlo.

- [ ] **Paso 1: elegir los valores, y dejar dicho por qué**

Tres decisiones, ninguna la fija el enunciado:

1. **Ej 2, θ = 30°.** Está lejos de los dos bordes del deslizador (0° y 60°), el coseno y
   el seno pesan los dos, y `N(x)` pasa de 226 N a 256 N a lo largo del tramo — se ve que
   la normal no es constante, que es la mitad del ejercicio.
2. **Ej 7, m = 1 kg, v₀ = 2 m/s, h = 3 m, L = 5 m.** La masa no está en el enunciado, así
   que todo sale **por kilogramo** y hay que decirlo con todas las letras en el ensayo.
   Con esos valores **a = 6,28 m/s²**, un número que se reconoce de un vistazo cuando la
   lectura del widget lo reproduce.
3. **Ej 10 con m = 1 kg y v = 3 m/s; Ej 12 con m = 2 kg y v = 3 m/s.** En el 12 las dos
   mitades quedan de 1 kg, una a 1 m/s y la otra a 5 m/s — enteros los cuatro números.
   El *v* del 10 es 3 y no 1 por una razón de dibujo, medida: con 1 m/s la flecha de
   cantidad de movimiento del caso por defecto mide 41 px a 880 en una escala que tiene
   que llegar hasta 9 kg·m/s; con 3 m/s mide 124 px. El enunciado deja *v* libre, así
   que elegir el que se ve es gratis.

- [ ] **Paso 2: escribir los cuatro bloques**

Van al final del script, después del bloque `Ej 12` y antes del `print` de cierre, para
no mover de lugar nada de lo que ya está. Reusan `W_F`, `Nx`, `W_f`, `x`, `th2` y `m2`
del bloque `Ej 2`, que ya están definidos más arriba en el archivo.

```python
# ---------------------------------------------------------------- Ej 2 (numerico)
title("Ej 2 (numerico): theta = 30 grados, el caso que dibuja el widget")
th30 = rad(30)
W_F30 = W_F.subs(th2, th30)
W_f30 = W_f.subs(th2, th30)
print(f"  W_F = 900 cos(30) = {float(W_F30):.4f} J")
print(f"  N(10) = {float(Nx.subs({x: 10, th2: th30})):.2f} N ; N(20) = {float(Nx.subs({x: 20, th2: th30})):.2f} N")
print(f"  W_roce = {float(W_f30):.4f} J")
print(f"  (b-i)  mu=0    -> K_f = {float(W_F30):.4f} J ; v_f = sqrt(2K/m) = {float(sqrt(2*W_F30/m2)):.4f} m/s")
print(f"  (b-ii) mu=0.05 -> K_f = {float(W_F30 + W_f30):.4f} J ; v_f = {float(sqrt(2*(W_F30+W_f30)/m2)):.4f} m/s")
thlim = sp.nsolve(W_F + W_f, th2, 1.4)
print(f"  el bloque deja de llegar a x=20 (K_f<0) a partir de theta = {float(deg(thlim)):.2f} grados")

# ---------------------------------------------------------------- Ej 7 (numerico)
title("Ej 7 (numerico): m=1 kg, v0=2 m/s, h=3 m, L=5 m")
m7n, v0n, h7n, L7n = 1, 2, 3, 5
E7n = Rational(1, 2) * m7n * v0n**2 + m7n * g * h7n
print(f"  (a) E = {float(E7n)} J")
vCn = sqrt(v0n**2 + g * h7n)
print(f"  (b) v_B = {float(v0n):.4f} m/s (igual a v0) ; v_C = {float(vCn):.4f} m/s")
vDn = sqrt(v0n**2 + 2 * g * h7n)
an = vDn**2 / (2 * L7n)
print(f"  (c) v_D = {float(vDn):.4f} m/s ; a = v_D^2/(2L) = {float(an):.4f} m/s^2")
print(f"      control: el freno disipa m a L = {float(m7n*an*L7n):.4f} J = K_D = {float(Rational(1,2)*m7n*vDn**2):.4f} J")
print(f"      control: K_C + U_C = {float(Rational(1,2)*m7n*vCn**2):.4f} + {float(m7n*g*h7n/2):.4f} = {float(Rational(1,2)*m7n*vCn**2 + m7n*g*h7n/2):.4f} J = E")

# ---------------------------------------------------------------- Ej 10 y 12 (numerico)
title("Ej 10 y 12 (numerico): los casos por defecto del widget de choques")
print("  Ej 10 con m=1 kg y v=3 m/s (la consigna es simbolica; estos son los valores del widget):")
print("    antes: v_A=3, v_B=0 -> despues: v_A'=0, v_B'=3 (intercambio)")
print(f"    p = {1*3 + 1*0} kg m/s antes y despues ; K = {float(Rational(1,2)*1*3**2)} J antes y despues")
mm12, vv12 = 2, 3
u12 = Rational(5, 3) * vv12
Ki12 = Rational(1, 2) * mm12 * vv12**2
Kf12 = Rational(1, 2) * Rational(mm12, 2) * Rational(vv12, 3)**2 + Rational(1, 2) * Rational(mm12, 2) * u12**2
print(f"  Ej 12 con m=2 kg y v=3 m/s: mitades de 1 kg, una a v/3 = {float(Rational(vv12,3))} m/s, la otra a u = {float(u12)} m/s")
print(f"    p = {float(mm12*vv12)} kg m/s antes y despues")
print(f"    K_i = {float(Ki12)} J -> K_f = {float(Kf12)} J ; K_f/K_i = {sp.nsimplify(Kf12/Ki12)} = {float(Kf12/Ki12):.4f}")

# ---------------------------------------------------------------- Choque general
title("Choque general (blindaje de los deslizadores del widget): m1=2, m2=1, u1=3, u2=-1")
m1g, m2g, u1g, u2g = 2, 1, 3, -1
pg = m1g * u1g + m2g * u2g
Kig = Rational(1, 2) * m1g * u1g**2 + Rational(1, 2) * m2g * u2g**2
mured = Rational(m1g * m2g, m1g + m2g)
for nombre, e in (("elastico", 1), ("restitucion e=0.5", Rational(1, 2)), ("perfectamente inelastico", 0)):
    v1g, v2g = symbols("v1 v2")
    s = solve([Eq(m1g * v1g + m2g * v2g, pg), Eq(v2g - v1g, -e * (u2g - u1g))], [v1g, v2g], dict=True)[0]
    a_, b_ = s[v1g], s[v2g]
    Kfg = Rational(1, 2) * m1g * a_**2 + Rational(1, 2) * m2g * b_**2
    dK = -Rational(1, 2) * mured * (1 - e**2) * (u1g - u2g)**2
    print(f"  {nombre:26s}: v1'={float(a_):+.4f}  v2'={float(b_):+.4f}  p={float(m1g*a_+m2g*b_):.4f} (antes {float(pg)})")
    print(f"      K: {float(Kig):.4f} -> {float(Kfg):.4f}  dK={float(Kfg-Kig):+.4f}  formula -mu(1-e^2)v_rel^2/2 = {float(dK):+.4f}")
```

`symbols`, `solve` y `Eq` ya están importados arriba; `sp.nsolve` y `sp.nsimplify` salen
del `import sympy as sp` que ya está.

- [ ] **Paso 3: correrlo y contrastar**

```bash
cd ../Ejercicios-prácticos/parcial-1/soluciones
python verificacion-practico-3.py
```

Los cuatro bloques nuevos tienen que imprimir **exactamente** esto (salida real, ya
corrida al escribir este plan):

```
Ej 2 (numerico): theta = 30 grados, el caso que dibuja el widget
  W_F = 900 cos(30) = 779.4229 J
  N(10) = 226.00 N ; N(20) = 256.00 N
  W_roce = -120.5000 J
  (b-i)  mu=0    -> K_f = 779.4229 J ; v_f = sqrt(2K/m) = 8.8285 m/s
  (b-ii) mu=0.05 -> K_f = 658.9229 J ; v_f = 8.1174 m/s
  el bloque deja de llegar a x=20 (K_f<0) a partir de theta = 80.89 grados

Ej 7 (numerico): m=1 kg, v0=2 m/s, h=3 m, L=5 m
  (a) E = 31.4 J
  (b) v_B = 2.0000 m/s (igual a v0) ; v_C = 5.7793 m/s
  (c) v_D = 7.9246 m/s ; a = v_D^2/(2L) = 6.2800 m/s^2
      control: el freno disipa m a L = 31.4000 J = K_D = 31.4000 J
      control: K_C + U_C = 16.7000 + 14.7000 = 31.4000 J = E

Ej 10 y 12 (numerico): los casos por defecto del widget de choques
  Ej 10 con m=1 kg y v=3 m/s (la consigna es simbolica; estos son los valores del widget):
    antes: v_A=3, v_B=0 -> despues: v_A'=0, v_B'=3 (intercambio)
    p = 3 kg m/s antes y despues ; K = 4.5 J antes y despues
  Ej 12 con m=2 kg y v=3 m/s: mitades de 1 kg, una a v/3 = 1.0 m/s, la otra a u = 5.0 m/s
    p = 6.0 kg m/s antes y despues
    K_i = 9.0 J -> K_f = 13.0 J ; K_f/K_i = 13/9 = 1.4444

Choque general (blindaje de los deslizadores del widget): m1=2, m2=1, u1=3, u2=-1
  elastico                  : v1'=+0.3333  v2'=+4.3333  p=5.0000 (antes 5.0)
      K: 9.5000 -> 9.5000  dK=+0.0000  formula -mu(1-e^2)v_rel^2/2 = +0.0000
  restitucion e=0.5         : v1'=+1.0000  v2'=+3.0000  p=5.0000 (antes 5.0)
      K: 9.5000 -> 5.5000  dK=-4.0000  formula -mu(1-e^2)v_rel^2/2 = -4.0000
  perfectamente inelastico  : v1'=+1.6667  v2'=+1.6667  p=5.0000 (antes 5.0)
      K: 9.5000 -> 4.1667  dK=-5.3333  formula -mu(1-e^2)v_rel^2/2 = -5.3333
```

Si algún dígito difiere, **el que manda es el script** y hay que corregir este plan, no
el script.

Un hallazgo del último bloque que la investigación no traía y que la Tarea 8 usa: la
fórmula de masa reducida para ΔK **con el factor (1 − e²)** vale en los **tres** modos,
no sólo en el perfectamente inelástico. El informe de cantidad de movimiento la propone
como canario en la versión sin ese factor, que sólo sirve para e = 0.

- [ ] **Paso 4: commit en el repositorio de al lado**

```bash
cd ../Ejercicios-prácticos
git add parcial-1/soluciones/verificacion-practico-3.py
git commit -m "feat(soluciones): bloques numericos de los ej. 2, 7, 10 y 12 del practico 3"
```

- [ ] **Paso 5: el PDF del práctico, y commit en la plataforma**

`docs/recursos/` tiene hoy `practico_1_2026.pdf` y `practico_2_2026.pdf` y **no** tiene
el 3, que los dos ensayos nuevos van a enlazar desde el pie.

```bash
cp "../Ejercicios-prácticos/parcial-1/practicos/Practico 3.pdf" docs/recursos/practico_3_2026.pdf
git add docs/recursos/practico_3_2026.pdf
git commit -m "chore(recursos): sumar el practico 3"
```

No hay hoja resumen de la Guía 3 en `../Ejercicios-prácticos/parcial-1/preparacion/`
(están las de cuerpo aislado, circular, sistemas acoplados, tiro, rozamiento y dinámica
circular, y ninguna de energía). Los pies de los dos ensayos citan sólo el práctico.

---

### Tarea 2: `presupuestoPx`, la barra que no miente

La primitiva que este plan existe para agregar. Todo lo demás que dibujan los siete
widgets sale de lo que ya hay; **un total que se reparte entre partes y no cambia**, no.

La decisión de diseño que la hace valer la pena: **`total` se pide explícito y no se
infiere sumando los segmentos**. La distancia entre lo que suman los segmentos y el total
declarado *es* la lectura que la barra existe para mostrar. Una barra que se normaliza a
sí misma siempre se ve llena, y una barra que siempre se ve llena no puede delatar nada.

**Archivos:**
- Modificar: `docs/motor/dibujo.js`
- Prueba: `test/dibujo.test.js`

**Interfaces:**
- Produce: `presupuestoPx(ctx, x, y, ancho, alto, segmentos, { total, colorBorde, colorTexto, minEtiquetaPx = 24 })`.
  `segmentos` es una lista de `{ valor, color, etiqueta }` en las mismas unidades que
  `total`; `x`, `y`, `ancho`, `alto` van en píxeles, como `vectorPx`.

- [ ] **Paso 1: darle a `ctxFalso` los dos métodos que le faltan**

El `ctxFalso` de `test/dibujo.test.js` registra trece métodos y **ninguno de los dos que
esta primitiva usa**. Sin esto la primera prueba falla con `TypeError: ctx.fillRect is
not a function`, que se lee como «la implementación está rota» cuando lo que está
incompleto es el doble.

```js
for (const m of ['beginPath','moveTo','lineTo','stroke','fill','fillRect','strokeRect','arc','closePath','save','restore','translate','rotate','setLineDash','fillText']) {
```

- [ ] **Paso 2: escribir las seis pruebas que fallan**

```js
test('presupuestoPx: el ancho de cada segmento sale del total declarado, no de la suma de los segmentos', () => {
  const c = ctxFalso();
  presupuestoPx(c, 100, 10, 200, 20,
    [{ valor: 20, color: '#1b4fd4' }, { valor: 30, color: '#c02a24' }],
    { total: 100, colorBorde: '#dcd8ce' });
  const rects = c.ops.filter(o => o[0] === 'fillRect');
  assert.equal(rects.length, 2);
  // 20/100*200 = 40. Si se normalizara por la suma (50) darian 80 y 120.
  assert.equal(rects[0][3], 40);
  assert.equal(rects[1][3], 60);
  assert.equal(rects[1][1], 140, 'el segundo arranca donde termina el primero');
});

test('presupuestoPx: lo que falta para llegar al total queda sin pintar', () => {
  const c = ctxFalso();
  presupuestoPx(c, 0, 0, 200, 20, [{ valor: 50, color: '#1b4fd4' }],
    { total: 100, colorBorde: '#dcd8ce' });
  const r = c.ops.filter(o => o[0] === 'fillRect');
  assert.equal(r.length, 1);
  assert.equal(r[0][3], 100, 'el segmento NO se estira para llenar la barra');
  const borde = c.ops.find(o => o[0] === 'strokeRect');
  assert.deepEqual(borde.slice(1), [0, 0, 200, 20]);
});

test('presupuestoPx: un segmento negativo tira TypeError', () => {
  const c = ctxFalso();
  assert.throws(() => presupuestoPx(c, 0, 0, 200, 20,
    [{ valor: -1, color: '#1b4fd4' }], { total: 10, colorBorde: '#dcd8ce' }), TypeError);
});

test('presupuestoPx: total cero no dibuja nada', () => {
  const c = ctxFalso();
  presupuestoPx(c, 0, 0, 200, 20, [{ valor: 0, color: '#1b4fd4' }],
    { total: 0, colorBorde: '#dcd8ce' });
  assert.equal(c.ops.length, 0);
});

test('presupuestoPx: si los segmentos suman mas que el total, la barra se desborda y lleva marca de tope', () => {
  const c = ctxFalso();
  presupuestoPx(c, 0, 0, 200, 20, [{ valor: 150, color: '#1b4fd4' }],
    { total: 100, colorBorde: '#dcd8ce' });
  assert.equal(c.ops.find(o => o[0] === 'fillRect')[3], 300, 'no se clipea en silencio');
  const xs = c.ops.filter(o => o[0] === 'moveTo' || o[0] === 'lineTo').map(o => o[1]);
  assert.ok(xs.length > 0, 'dibuja la marca de tope');
  assert.ok(Math.max(...xs) > 200, 'la marca cae fuera del ancho pedido');
});

test('presupuestoPx: un segmento mas angosto que minEtiquetaPx no lleva rotulo', () => {
  const c = ctxFalso();
  presupuestoPx(c, 0, 0, 200, 20,
    [{ valor: 95, color: '#1b4fd4', etiqueta: 'cinetica' },
     { valor: 5, color: '#c02a24', etiqueta: 'calor' }],
    { total: 100, colorBorde: '#dcd8ce', colorTexto: '#8e8a80', minEtiquetaPx: 24 });
  const rotulos = c.ops.filter(o => o[0] === 'fillText').map(o => o[1]);
  assert.deepEqual(rotulos, ['cinetica'], '5/100*200 = 10 px, menos que 24');
});
```

Estas seis se corrieron contra la implementación del Paso 4 (verde) y contra **seis
mutantes** —normalizar por la suma, clipear en silencio, estirar para llenar, sacar la
guarda de total cero, sacar la guarda de negativos, rotular siempre—, y **cada mutante
rompe al menos una**. La que normaliza por la suma rompe tres. Si al implementar alguna
prueba pasa contra una implementación obviamente rota, la prueba está mal, no el mutante.

- [ ] **Paso 3: correrlas y verificar que fallan**

Ejecutar: `node --test test/dibujo.test.js`
Esperado: FALLAN las seis (`presupuestoPx is not defined`).

- [ ] **Paso 4: implementar**

```js
// Una barra apilada en pixeles: `segmentos` es una lista de {valor, color, etiqueta},
// todos en las mismas unidades que `total`. El ancho de cada uno es proporcional a su
// valor sobre `total` -- NO sobre la suma de los segmentos, y eso es a proposito.
//
// `total` se pide explicito, igual que `color` en las demas primitivas, porque la
// distancia entre "lo que suman los segmentos" y "el total declarado" ES la lectura que
// esta barra existe para mostrar. Una barra normalizada a si misma siempre se ve llena,
// y una barra que siempre se ve llena no delata nada: ni el calor que todavia no se
// disipo (suma < total: queda un tramo sin pintar) ni una energia contada dos veces
// (suma > total: la barra se desborda y lleva `marcaDeTope`). Clipear en silencio
// esconderia justo el error que hay que mostrar.
//
// El calculo del chequeo -- `total - suma`, o la diferencia entre dos energias que
// deberian coincidir -- lo hace el widget, no la primitiva: aca solo se dibuja lo que se
// pasa, igual que `vectorPx` no suma las fuerzas.
export function presupuestoPx(ctx, x, y, ancho, alto, segmentos,
  { total, colorBorde, colorTexto, minEtiquetaPx = 24 } = {}) {
  exigirColor(colorBorde, 'presupuestoPx (colorBorde)');
  for (const s of segmentos) {
    exigirColor(s.color, 'presupuestoPx (segmento)');
    // Un presupuesto de energia no tiene segmentos negativos: si hace falta mostrar el
    // trabajo negativo de un agente externo (la mano del ej. 5), son DOS barras --
    // "entra" y "sale" -- no un segmento al reves dentro de la misma.
    if (!(s.valor >= 0)) {
      throw new TypeError(
        `presupuestoPx: el segmento "${s.etiqueta ?? ''}" vale ${s.valor}. Un presupuesto no admite valores negativos ni NaN: partilo en dos barras.`);
    }
  }
  // Sin total no hay escala que definir; dividir por cero daria NaN en cada ancho.
  if (!(total > 0)) return;
  const k = ancho / total;
  let cursor = x;
  for (const s of segmentos) {
    const w = s.valor * k;
    ctx.fillStyle = s.color;
    ctx.fillRect(cursor, y, w, alto);
    // Mismo criterio que `eje` al no rotular el cero: un rotulo que no entra se
    // superpone con el vecino y se lee peor que no estar.
    if (s.etiqueta && w >= minEtiquetaPx) {
      exigirColor(colorTexto, 'presupuestoPx (colorTexto)');
      texto(ctx, s.etiqueta, cursor + w / 2, y + alto / 2 + 4,
        { color: colorTexto, px: 10, alineacion: 'center' });
    }
    cursor += w;
  }
  ctx.strokeStyle = colorBorde;
  ctx.lineWidth = 1;
  ctx.strokeRect(x, y, ancho, alto);
  // El medio pixel de tolerancia es contra el ruido de punto flotante cuando la suma da
  // exactamente el total, que es el caso normal en los widgets de energia.
  if (cursor > x + ancho + 0.5) {
    marcaDeTope(ctx, cursor, y + alto / 2, 1, 0, { color: colorBorde });
  }
}
```

- [ ] **Paso 5: actualizar el contrato de estado del módulo**

El comentario de cabecera de `dibujo.js` enumera qué deja puesto cada primitiva. Sumar:
`presupuestoPx` deja escritos `fillStyle`, `strokeStyle` y `lineWidth`, no toca
`setLineDash` ni `globalAlpha`, y toca `font`/`textAlign` **sólo si algún segmento llegó
a rotularse** (ahí queda lo que deje `texto`: JetBrains Mono a 10 px y `textAlign` en
`'center'`). Con todos los segmentos más angostos que `minEtiquetaPx` no los toca — o sea
que el estado en que sale depende de los datos, y eso hay que decirlo, no esconderlo.

- [ ] **Paso 6: correr la suite y commitear**

```bash
node --test "test/**/*.test.js"
git add docs/motor/dibujo.js test/dibujo.test.js
git commit -m "feat(motor): presupuestoPx, la barra apilada contra un total declarado"
```

Esperado: **246 pruebas, 0 fallas** (240 de base + 6). Con la séptima prueba que sumó la
ronda de arreglo — la del orden del borde — son **247**.

---

## Fase B — Ensayo 7: Trabajo y energía

Es el ensayo que abre la Guía 3 y el segundo salto conceptual grande del cuatrimestre.
Hasta acá, para saber qué le pasa a un cuerpo había que sumar fuerzas y resolver la
segunda ley instante por instante; de acá en adelante hay un atajo que, cuando se puede
usar, saltea el tiempo entero: comparar dos estados y ver qué energía se movió de un
casillero a otro. La contracara —y lo que cuesta aprender— es que el atajo tiene
condiciones, y saber cuáles son es la mitad del tema.

**La columna vertebral, en el orden en que el ensayo la construye** (sale de
`.superpowers/investigacion-guia-3/energia.md` §2):

1. Qué es el trabajo, literal: la componente en la dirección del desplazamiento,
   **integrada** si la fuerza cambia con la posición (sección 01, Ej 2).
2. El mismo presupuesto con dos depósitos distintos, y una fuerza que se lo roba
   (sección 02, Ej 3 y 4, con el Ej 5 en prosa).
3. Quién no trabaja nunca, y qué se conserva cuando la geometría cambia de golpe
   (sección 03, Ej 1, con el Ej 6 en prosa).
4. Un balance solo para todo un sistema, con varias alturas, y el caso donde μ*N*d ya no
   se puede escribir (sección 04, Ej 7 y 8).

---

### Tarea 3: La página y el widget 1 — el trabajo es un área

**Archivos:**
- Crear: `docs/ensayos/energia.html`

**Interfaces:**
- Consume: `crearPagina`, `crearWidget`, `panelesApilados`, `deslizador`, `casilla`,
  `conectarTema`, y de `dibujo.js`: `eje`, `bloque`, `suelo`, `curva`, `punteado`,
  `vectorPx`, `COLGADO_ROTULO_EJE`. Y `num()` de `docs/motor/formato.js`.
  **No consume `texto`**: el único rótulo que este widget cuelga de algo es el de la
  flecha de F, y va por la opción `rotulo:` de `vectorPx` (que llama a `colocarEtiqueta`
  por dentro). Los rótulos de los ejes los pone `eje()` solo.
- Produce: la página con su encabezado, la sección 01 y el primer widget.

**El ejercicio (práctico 3, ej. 2).** Un bloque de 20 kg es empujado sobre una superficie
horizontal por una fuerza que **llega desde arriba** formando un ángulo θ con la
horizontal, y que crece con la posición: |F(x)| = 6x N. Se pide el trabajo de esa fuerza
entre x = 10 m y x = 20 m, y la energía cinética final con μ = 0 y con μ = 0,05.

Del bloque `Ej 2 (numerico)`, a θ = 30°: **W_F = 779,4229 J**, **N(10) = 226,00 N**,
**N(20) = 256,00 N**, **W_roce = −120,5000 J**, **K_f(μ=0) = 779,4229 J**,
**K_f(μ=0,05) = 658,9229 J**, y las velocidades finales 8,8285 y 8,1174 m/s.

- [ ] **Paso 1: el esqueleto de la página**

Copiar el esqueleto de `docs/ensayos/cuerpo-aislado.html` —el script de tema bloqueante
del `<head>`, la barra de progreso, la columna, la franja, el pie— y cambiar:

- kicker `Ensayo 7 · Física 1`; `<title>` `Trabajo y energía · Física 1`;
  `<h1>` `Trabajo y energía`.
- bajada: `Cuánto se mueve la energía de un casillero a otro, y quién la mueve.`
- pie: a la izquierda `Ensayo 6 · Fuerzas que dependen de la posición`
  (`fuerzas-de-posicion.html`), a la derecha `Portada` (`../index.html`).
- línea de fuentes: `<a href="../recursos/practico_3_2026.pdf">práctico 3, ej. 1 a 8</a>`.
  El capítulo del apunte va **sólo si se confirma cuál es** mirando qué citan los otros
  ensayos y qué cubre ese capítulo; si no se confirma, se omite. No inventar un número.

Todo el texto que tenga clase en `base.css` la usa. Los `style` tipográficos del
esqueleto —el kicker, el `<h1>`, la `<ol>` de cierre, el pie, la línea de fuentes— se
copian **idénticos** de `cuerpo-aislado.html`; **ninguno nuevo se inventa**. Ver la
Global Constraint: no hay clase para esos seis elementos y este plan no la agrega.

Dos párrafos de introducción. El primero: la palabra «trabajo» no significa esfuerzo.
Significa una cosa muy precisa —cuánta energía le entra o le sale a un cuerpo por culpa
de una fuerza— y esa cuenta sólo mira la componente de la fuerza **en la dirección en que
el cuerpo se movió**. Una fuerza perpendicular al movimiento vale lo que valga y no
transfiere nada. El segundo: por qué conviene. Con fuerzas hay que resolver el movimiento
instante por instante; con energía se comparan dos estados y el camino del medio no
importa —mientras todas las fuerzas que actuaron sean conservativas—. Ese «mientras» es
el tema de las cuatro secciones.

- [ ] **Paso 2: la sección 01 y su franja**

`<h2>`: `01 · El trabajo es un área`.

Párrafo previo: casi todo el mundo aprende «trabajo = fuerza por distancia», y eso vale
sólo si la fuerza es constante y paralela al desplazamiento. Acá no pasa ninguna de las
dos: F crece con x (de 60 N a 120 N) y llega inclinada. Lo que hay que sumar es F·cos θ a
lo largo del camino, pedacito por pedacito — o sea, el **área** bajo la curva de la
componente útil. Y hay una segunda trampa: como F llega desde arriba, aprieta al bloque
contra el piso, así que N no vale mg, crece con x, y el rozamiento crece con ella.

La franja:

- `.encabezado-widget`: `Simulación 1` · `El trabajo es un área` ·
  `— el número de la fórmula y el área sombreada tienen que dar lo mismo, θ por θ.`
- `<canvas id="w1-cv">`
- controles: deslizador `w1-theta` (`min="0" max="60" step="1" value="30"`, salida en
  grados) y casilla `w1-roce` con la etiqueta `Hay rozamiento (μ = 0,05)`.
- `.lecturas`: `W de F` (`w1-w`), `N(10) → N(20)` (`w1-n`), `K final` (`w1-k`),
  `v final` (`w1-v`) y `área − fórmula` (`w1-chequeo`) en `--dim`.

El tope del deslizador en 60° no es estético. Del bloque `Ej 2 (numerico)`: **a partir de
80,89° el bloque ni siquiera llega a x = 20** con μ = 0,05 —la energía cinética final
daría negativa—, y ya antes de eso la fuerza tangencial neta se hace negativa en el
arranque del tramo. 60° deja el fenómeno entero adentro del rango válido, con margen.
Comprobado: con μ = 0,05 la fuerza neta a x = 10 vale 50,2 N a 0°, 40,7 N a 30° y 17,6 N
a 60° — positiva en todo el recorrido del deslizador, que es lo que hace que el encuadre
del panel de abajo pueda arrancar en cero.

- [ ] **Paso 3: la física, con dos caminos que no comparten una línea**

```js
/* ---------- widget 1: el trabajo es un area ---------- */

// Practico 3, ej. 2. Bloque de 20 kg empujado sobre un piso horizontal por una fuerza
// F(x) = 6x N que llega DESDE ARRIBA formando un angulo th con la horizontal, de x = 10
// a x = 20 m. Verificado en el bloque "Ej 2 (numerico)" con th = 30 grados:
//   W_F = 779.4229 J   N(10) = 226.00 N   N(20) = 256.00 N   W_roce = -120.5000 J
//   K_f(mu=0) = 779.4229 J   K_f(mu=0.05) = 658.9229 J   v_f = 8.8285 y 8.1174 m/s
// `G` es de la PAGINA, no de este widget: va arriba de todo, fuera del bloque del
// widget 1, porque los widgets 2, 3 y 4 la usan y el modulo es uno solo.
const G = 9.8;

const M = 20, X0 = 10, X1 = 20, MU = 0.05;

const F = x => 6 * x;                                       // N
// F aprieta contra el piso: la normal NO vale mg y crece con x.
const normal = (x, th) => M * G + F(x) * Math.sin(th);
const tangencial = (x, th, mu) => F(x) * Math.cos(th) - mu * normal(x, th);

// Camino A -- la formula cerrada, la que se saca en el papel integrando a mano.
const cerrada = (th, mu) => mu > 0
  ? 900 * Math.cos(th) - 45 * Math.sin(th) - 98
  : 900 * Math.cos(th);

// Camino B -- el area bajo la MISMA curva que el panel de abajo dibuja, por trapecios.
//
// Los dos caminos no comparten una sola linea de codigo, y ese es todo el punto. El
// error clasico de este ejercicio es escribir N = mg (olvidarse de que F aprieta): con
// ese error la formula cerrada de arriba sigue dando el mismo numero y el area se va
// 22.50 J a 30 grados -- medido. Con 400 trapecios sobre un integrando lineal la
// cuadratura es EXACTA (la diferencia medida entre los dos caminos, con el modelo bien,
// es del orden de 1e-13 J en todo el rango del deslizador): lo que la lectura compara
// son las dos EXPRESIONES, no la precision del metodo.
function area(f, a, b, n = 400) {
  const h = (b - a) / n;
  let s = 0;
  for (let i = 0; i < n; i++) s += (f(a + i * h) + f(a + (i + 1) * h)) / 2 * h;
  return s;
}
```

Antes de dibujar nada, comprobalo en la consola: con `th = 30 * Math.PI / 180` y
`mu = 0.05`, `cerrada(th, mu)` y `area(x => tangencial(x, th, mu), 10, 20)` tienen que dar
los dos `658.9229`, y `normal(10, th)` y `normal(20, th)`, `226` y `256`.

- [ ] **Paso 4: el dibujo, en dos paneles**

Dos franjas con `panelesApilados`, que ya sabe darle a cada panel su propio rango
vertical: arriba la escena (el bloque sobre el piso, con la flecha de F), abajo el
gráfico de la fuerza tangencial contra x, con el área rayada.

```js
// Sufijo `_W1` por la Global Constraint del espacio de nombres: `energia.html` es UN
// modulo, y los widgets 2, 3 y 4 declaran sus propios margenes mas abajo.
const MARGEN_W1 = { L: 52, R: 24, T: 18, B: 32 };
const HUECO_ROTULO_W1 = COLGADO_ROTULO_EJE + 8;
const ALTO_PANEL_MINIMO_W1 = 95 + HUECO_ROTULO_W1;

const widget = crearWidget({
  pagina, canvas: el('w1-cv'),
  margen: MARGEN_W1,
  // Metros contra newtons abajo y metros contra "aire de dibujo" arriba: no hay una
  // escala fisica unica que le sirva a los dos.
  escalaUniforme: false,
  altoMin: 2 * ALTO_PANEL_MINIMO_W1 + MARGEN_W1.T + MARGEN_W1.B,
  // El rango horizontal es el mismo para los dos paneles -- el tramo del ejercicio, con
  // un metro de aire a cada lado -- y eso es lo que hace que una columna vertical
  // signifique lo mismo arriba y abajo.
  encuadre: () => ({ xMin: 9, xMax: 21, yMin: 0, yMax: 2 }),
  dibujar: pintar,
});
```

Los paneles: `[{ yMin: -0.35, yMax: 1.05 }, { yMin: 0, yMax: 130 }]`.

**El techo del panel de abajo es fijo en 130 N y no se reescala con θ**, a propósito: es
lo que hace que el área se vea **encogerse** al subir el ángulo, que es el mensaje de la
sección. Medido llamando al `crearWidget` real: a 880 px de franja el canvas sale de
430 px de alto, los dos paneles miden 190 px, y la escala horizontal es 67,00 px/m en los
dos; el gráfico da 1,208 px por newton, así que la curva llega a 144,9 px de alto a θ = 0,
125,5 px a θ = 30° y 72,5 px a θ = 60°. A 350 px (viewport de 390) el canvas cae a 286 px,
los paneles a 118 px, 22,83 px/m, y esos tres altos pasan a 78,5 / 67,9 / 39,2 px. Los
seis son legibles; ninguno se sale del panel.

El bloque de la escena: el panel de arriba es **anisótropo** (67,00 px/m contra 112,14
px/unidad a 880 px), así que un rectángulo pedido en unidades del marco sale deformado y
distinto en cada viewport. Se pide en píxeles y se divide por la escala de cada eje:

```js
// Un cajon de 34 x 22 px en cualquier viewport. En unidades del marco eso son 0.507 m de
// ancho a 880 px y 1.489 m a 350 px -- la escena es esquematica (un tramo de 10 m al lado
// de un cajon sin medida dada no puede estar a escala), asi que lo que se fija es lo que
// el lector ve, no lo que el marco dice.
const ANCHO_PX = 34, ALTO_PX = 22;
const anchoU = ANCHO_PX / esc.escala.x, altoU = ALTO_PX / esc.escala.y;
suelo(ctx, esc, { color: p.rule, desde: 9, hasta: 21, y: 0 });
bloque(ctx, esc, [x, altoU / 2], { ancho: anchoU, alto: altoU, color: p.band, borde: p.ink });
```

La flecha de F, **toda en píxeles**, con la punta apoyada en el vértice de arriba del
bloque y la cola arriba y atrás (la fuerza llega desde arriba):

```js
// La flecha mas larga del widget es F(20) = 120 N a theta = 0: se le da el 60 % del alto
// util del panel de la escena, y de ahi salen los pixeles por newton. Medido: 0.785 px/N
// a 880 (la flecha da 94 px) y 0.425 px/N a 350 (51 px).
const altoUtil = esc.py(-0.35) - esc.py(1.05);
const K_PX = 0.6 * altoUtil / 120;

const [bx, by] = esc.p([x, altoU / 2]);      // el vertice de arriba del bloque
// Componentes EN PIXELES, no en unidades del marco: en pantalla la y crece hacia abajo,
// y la fuerza baja, asi que su componente vertical SUMA a `by`. Escribir aca las
// componentes del marco y usarlas como pixeles es exactamente el defecto que dejo
// flechas que no giraban en el plan anterior: si theta cambia y la flecha no cambia de
// inclinacion, el error es este.
const dxPx = K_PX * F(x) * Math.cos(th);
const dyPx = K_PX * F(x) * Math.sin(th);
// El rotulo va por `rotulo:`, que llama a `colocarEtiqueta` por dentro -- nunca un
// `texto()` a mano al lado de la punta. `rdx`/`rdy` lo corren hacia arriba y a la
// izquierda, del lado de la cola, para que no se meta en el panel de abajo.
vectorPx(ctx, bx - dxPx, by - dyPx, bx, by,
  { color: p.red, grosor: 2, punta: 9, rotulo: 'F', rdx: -18, rdy: -8 });
```

Comprobación de que gira de verdad, medida a 880 px: a θ = 0 las componentes son
(70,6; 0) px; a θ = 30°, (61,2; 35,3); a θ = 60°, (35,3; 61,2). A 350 px: (38,3; 0),
(33,1; 19,1), (19,1; 33,1). Si al mover el deslizador la flecha no se inclina, mirá esas
seis cifras antes que cualquier otra cosa.

**Corregido durante la ejecución, midiendo:** este plan traía (94, 0) / (82, 47) /
(47, 82), calculadas con la fuerza en el extremo del tramo, F(20) = 120 N. Pero el bloque
se dibuja en el **medio** del tramo, x = 15, donde F(15) = 90 N — lo dice el párrafo de
acá abajo—, así que la flecha real mide 0,75 de aquello. Las cifras de arriba son las
medidas instrumentando el canvas, no las calculadas a mano.

`x` es la posición del bloque dentro del tramo. Sin animación: el bloque se dibuja en el
medio del tramo (x = 15) y ahí se queda. Este widget no tiene reproducción — lo que se
manipula es θ, no el tiempo.

El área rayada, con `punteado` cada 6 px, entre el eje y la curva:

```js
// El area se raya, no se rellena: no hay primitiva de relleno en el motor y no hace
// falta una. Las rayitas son la misma convencion que `suelo` usa para el terreno.
for (let xp = gr.px(X0); xp <= gr.px(X1) + 0.01; xp += 6) {
  const xu = gr.ux(xp);
  punteado(ctx, xp, gr.py(0), xp, gr.py(tangencial(xu, th, mu)),
    { color: p.blueSoft, guiones: [2, 3] });
}
curva(ctx, gr, x => [x, tangencial(x, th, mu)], X0, X1, { color: p.red, grosor: 1.8 });
eje(ctx, gr, { color: p.rule, colorTexto: p.dim, etiquetaX: 'x [m]', etiquetaY: 'F∥ [N]' });
```

El rayado en `--blue-soft` y la curva en `--red` es una decisión de color que conviene
mirar: la curva **es** una fuerza (rojo, por la regla global), y el área **es** el trabajo,
que se vuelve energía cinética (azul, por la extensión de las Global Constraints). A 880
px salen 112 rayitas y a 350 px, 39.

Con la casilla **sin** marcar, la curva dibujada es `F(x)·cos θ` (o sea `tangencial` con
`mu = 0`); con la casilla marcada, la fuerza tangencial **neta**. Es la misma función con
otro μ: no se escriben dos.

- [ ] **Paso 5: las lecturas**

```js
const chequeo = area(u => tangencial(u, th, mu), X0, X1) - cerrada(th, mu);
leer('w1-w', num(900 * Math.cos(th), 1) + ' J');
leer('w1-n', num(normal(X0, th), 0) + ' → ' + num(normal(X1, th), 0) + ' N');
leer('w1-k', num(cerrada(th, mu), 1) + ' J');
leer('w1-v', num(Math.sqrt(2 * cerrada(th, mu) / M), 2) + ' m/s');
// Sin guarda de "-0,00": `num()` ya normaliza el cero negativo. El plan de pago de deuda
// borro seis de estas guardas (commit 8a88de6); reescribirlas seria deshacerlo.
leer('w1-chequeo', num(chequeo, 2) + ' J');
```

Con θ = 30° y la casilla marcada, las cinco lecturas tienen que dar `779,4 J`,
`226 → 256 N`, `658,9 J`, `8,12 m/s` y `0,00 J`.

- [ ] **Paso 6: los párrafos de cierre de la sección**

1. Los números a 30°: la fuerza hace 779,4 J, pero al bloque le quedan 658,9 J, porque el
   rozamiento se llevó 120,5 J. Y esos 120,5 J no salen de μ·mg·d: la normal no es mg.
   Empieza en 226 N y termina en 256 N, justamente porque F aprieta cada vez más fuerte
   —crece con x— y el bloque se apoya cada vez con más ganas contra el piso.
2. Movés θ y mirá el área. A 0° la fuerza empuja de lleno hacia adelante y el trabajo es
   máximo (900 J). A 60° el área es la mitad. Lo que se pierde no es «fuerza»: la fuerza
   vale exactamente lo mismo, 120 N al final del tramo en los dos casos. Lo que se pierde
   es **dirección**.
3. Que la lectura de abajo esté clavada en 0,00 J no es una comprobación de que la cuenta
   esté bien: es la definición de trabajo puesta a prueba. Una de las dos cuentas
   integra la curva que ves dibujada; la otra es la fórmula cerrada del papel. Si fueran
   dos cosas distintas, el trabajo no sería el área.

- [ ] **Paso 7: verificar**

1. Lecturas a θ = 30° con rozamiento: `779,4 J`, `226 → 256 N`, `658,9 J`, `8,12 m/s`,
   `0,00 J`. Contra el bloque `Ej 2 (numerico)`.
2. Sin rozamiento a θ = 30°: `K final` tiene que dar `779,4 J` y `v final`, `8,83 m/s`.
3. θ = 0 y θ = 60, los dos extremos: el chequeo sigue en `0,00 J` y la curva no se sale
   del panel por arriba ni cruza el cero por abajo.

   **Pero ojo con qué prueba cada extremo, medido durante la ejecución:** a θ = 0 el
   chequeo **no vigila `normal()`**. Con el modelo roto a `() => M * G` la lectura sigue
   dando `0,00 J` ahí, y no porque el canario falle sino porque `sen 0 = 0` hace que el
   modelo roto y el correcto sean **el mismo número** — a θ = 0 la fuerza es horizontal y
   de verdad no aprieta contra el piso. Lo mismo pasa con la casilla de rozamiento
   destildada, en cualquier θ: sin μ, el término que contiene `normal()` se anula y el
   chequeo no lo ejercita.

   O sea: el canario del Paso 7.6 sólo muerde **con rozamiento y con θ ≠ 0**. Verificar
   «los dos extremos» y quedarse tranquilo es justamente la conclusión equivocada. A
   θ = 30 salta a 22,50 J y a θ = 60 a 38,97 J; a θ = 0, a nada.
4. **Medí la flecha**, no la mires: a 880 px tiene que dar **70,6 px** a θ = 0 y sus
   componentes **(35,3; 61,2)** a θ = 60°, con el bloque en x = 15 (F = 90 N). El módulo
   no cambia con θ: sólo se reparte entre las componentes.
5. 1280 y 390 px, los dos temas, consola limpia, ningún widget animándose solo al cargar.
6. Rompé el modelo a propósito una vez: cambiá `normal` por `() => M * G` y confirmá que
   el chequeo salta a `22,50 J` a θ = 30°. Volvé atrás. Si no saltó, el chequeo no está
   calculado por dos caminos y hay que arreglarlo antes de seguir.

- [ ] **Paso 8: commit**

```bash
node --test "test/**/*.test.js"
git add docs/ensayos/energia.html
git commit -m "feat(ensayos): energia, el trabajo es un area"
```

---

### Tarea 4: Widget 2 — el mismo presupuesto, dos depósitos

**Archivos:**
- Modificar: `docs/ensayos/energia.html`

**Interfaces:**
- Consume: lo de la Tarea 3, más `crearEscena`, `rotuloReproducir`, `boton`,
  `presupuestoPx` (Tarea 2), `bloque`/`suelo` y **`traza`**, que es la primitiva con la
  que se dibuja el zigzag del resorte (una polilínea de puntos del marco; ver
  `dibujo.js:292`). Y `colocarEtiqueta` para los rótulos que cuelgan del bloque.
- Produce: la sección 02 con el widget 2 y la prosa del ejercicio 5.

**Los ejercicios.** Ej 3: una masa de 1 kg baja 1 m de altura por un plano de 30° (2 m
sobre el plano); sin rozamiento llega a **4,4272 m/s**, con μ = 0,3 llega a **3,0685 m/s**
y el rozamiento se comió **5,0922 J** de los 9,80 J iniciales. Ej 4: una masa de 1 kg
comprime 0,3 m un resorte de k = 2 N/m, se libera sin fricción (**W_resorte = 0,09 J**,
**v = 0,424264 m/s**) y entra en una zona con μ = 0,2, donde se detiene tras **0,045918 m**
(4,59 cm). Los dos están completos en el script desde antes de este plan.

Son **el mismo ejercicio con otro depósito**: energía guardada en algún lado → cinética →
calor. Por eso es un widget con dos modos y no dos widgets.

- [ ] **Paso 1: la sección 02 y su franja**

`<h2>`: `02 · El mismo presupuesto, dos depósitos`.

Párrafo previo: la contabilidad es siempre la misma. Hay un total, que se fija al
principio; hay casilleros por los que esa energía se reparte —cinética, potencial
gravitatoria, potencial elástica—; y hay un sumidero, el rozamiento, que saca del total y
no devuelve. Mientras nada salga por el sumidero, la suma de los casilleros no cambia
aunque cada uno suba y baje. La barra de arriba del widget es literalmente esa cuenta.

La franja:

- `.encabezado-widget`: `Simulación 2` · `El mismo presupuesto, dos depósitos` ·
  `— la barra nunca cambia de largo; lo único que cambia es de quién es cada pedazo.`
- `<canvas id="w2-cv">`
- controles: `Reproducir` (`w2-play`), `Reiniciar` (`w2-reset`), casilla `w2-modo` con
  la etiqueta `Resorte en vez de plano`, y deslizador `w2-mu`
  (`min="0" max="0.5" step="0.01"`), cuyo **valor por defecto lo fija el modo**: 0,30 en
  plano (Ej 3) y 0,20 en resorte (Ej 4).

Al cambiar de modo hay que **reescribir el `value` del deslizador de μ, y eso no repinta
su `<output>` solo**: `deslizador()` actualiza la salida únicamente dentro de su listener
de `'input'`, y asignar `.value` desde JS no dispara ningún evento. Sin esto el control
queda marcando 0,30 mientras el widget calcula con 0,20 — y el lector no tiene forma de
saber cuál es el número bueno. El patrón del sitio, copiado de
`movimiento-circular.html:513`:

```js
// Mover un deslizador desde codigo es asignar Y despachar: asi es `deslizador` quien
// repinta su <output> y avisa a la pagina, y no queda una segunda copia del cableado.
const fijarDeslizador = (entrada, valor) => {
  entrada.value = String(valor);
  entrada.dispatchEvent(new Event('input'));
};
fijarDeslizador(el('w2-mu'), modoResorte ? 0.20 : 0.30);
```
- `.lecturas`: `cinética` (`w2-k`, azul), `potencial` (`w2-u`, `--graph`),
  `disipado` (`w2-q`, rojo), `v` (`w2-v`) y `suma − total` (`w2-chequeo`, `--dim`).

El tope del deslizador de μ en 0,50 es físico, no estético: con **μ = tan 30° = 0,5774**
el bloque del plano ya no arranca. Medido: la aceleración vale 4,9000 m/s² a μ = 0,
2,3539 a μ = 0,3 y 0,6565 a μ = 0,5 — positiva en todo el rango, y el widget nunca tiene
que dibujar un bloque que retroceda.

- [ ] **Paso 2: la física, con la cinética calculada por fuera del presupuesto**

Éste es el punto delicado de toda la tarea. Si la energía cinética se calcula como
«total − potencial − disipado», entonces `suma − total` da cero **por construcción**, la
lectura no puede moverse nunca, y el widget no prueba nada. La cinética tiene que salir
de la **velocidad** del cuerpo, que sale del movimiento; el potencial, de la posición; y
el disipado, de la fuerza de rozamiento por la distancia. Tres caminos, tres orígenes
distintos, y la suma tiene que dar el total.

```js
/* ---------- widget 2: el mismo presupuesto, dos depositos ---------- */

// Practico 3, ej. 3 y 4. Verificado en los bloques "Ej 3" y "Ej 4":
//   plano:   1 kg, 30 grados, h = 1 m (s = 2 m sobre el plano)
//            mu = 0   -> v = 4.4272 m/s
//            mu = 0.3 -> v = 3.0685 m/s, W_roce = -5.0922 J de los 9.80 J iniciales
//   resorte: 1 kg, k = 2 N/m, comprimido 0.3 m -> W = 0.09 J, v = 0.424264 m/s,
//            y con mu = 0.2 se detiene a 0.045918 m (4.59 cm)
const M2 = 1, ALFA = 30 * Math.PI / 180, H = 1, S_PLANO = H / Math.sin(ALFA);  // 2 m
const K_RES = 2, X_COMP = 0.3;

// --- modo plano: aceleracion constante, y la cinetica sale de la VELOCIDAD.
function plano(t, mu) {
  const a = G * (Math.sin(ALFA) - mu * Math.cos(ALFA));
  const s = Math.min(0.5 * a * t * t, S_PLANO);
  const v = Math.sqrt(2 * a * s);                       // no a*t: asi vale tambien en el tope
  return {
    s, v,
    total: M2 * G * H,
    K: 0.5 * M2 * v * v,                                // de la velocidad
    U: M2 * G * (H - s * Math.sin(ALFA)),               // de la altura
    Q: mu * M2 * G * Math.cos(ALFA) * s,                // de la fuerza por la distancia
  };
}

// --- modo resorte: dos tramos. Empuje del resorte (un cuarto de periodo de un armonico,
// sin friccion) y despues frenado uniforme en la zona rugosa.
function resorte(t, mu) {
  const w = Math.sqrt(K_RES / M2);                      // 1.4142 rad/s
  const tEmpuje = (Math.PI / 2) / w;                    // 1.1107 s
  const vSalida = X_COMP * w;                           // 0.424264 m/s
  const aFreno = mu * G;
  const total = 0.5 * K_RES * X_COMP * X_COMP;          // 0.09 J
  if (t <= tEmpuje) {
    const x = -X_COMP * Math.cos(w * t);                // de -0.3 a 0
    const v = X_COMP * w * Math.sin(w * t);
    return { s: x, v, total, K: 0.5 * M2 * v * v, U: 0.5 * K_RES * x * x, Q: 0 };
  }
  const td = Math.min(t - tEmpuje, vSalida / aFreno);
  const d = vSalida * td - 0.5 * aFreno * td * td;
  const v = vSalida - aFreno * td;
  return { s: d, v, total, K: 0.5 * M2 * v * v, U: 0, Q: mu * M2 * G * d };
}
```

Comprobalo en la consola antes de dibujar: `plano(1.3036, 0.3)` tiene que dar `v` cerca de
`3.0685`, `Q` cerca de `5.0922` y `K + U + Q` exactamente `9.8`; `resorte(1.1107, 0.2)`
tiene que dar `v = 0.424264` y `K = 0.09`; y a `t = 1.3272` el resorte tiene que estar
detenido con `s = 0.045918`.

Las duraciones, integradas al escribir este plan: **plano 1,3036 s** con μ = 0,3 (0,9035 s
con μ = 0 y 2,4684 s con μ = 0,5), **resorte 1,3272 s** (1,1107 s de empuje + 0,2165 s de
frenado). `escena.duracion` se recalcula al cambiar de modo y al mover μ.

- [ ] **Paso 3: la barra de energía**

La barra va en el margen superior del canvas, cruzando todo el ancho, **medida en píxeles
de canvas y no del encuadre** —así no cambia de largo al cambiar de modo, que es
exactamente lo que la barra promete—:

```js
// De 28 px del borde izquierdo a 24 px del derecho, en cualquier viewport y en los dos
// modos: 828 px a 880 de franja, 298 px a 350. El encuadre cambia entre modos (metros de
// plano contra centimetros de resorte); el largo de la barra, no.
const X_BARRA = 28, ALTO_BARRA = 22, Y_BARRA = 16;
presupuestoPx(ctx, X_BARRA, Y_BARRA, l.ancho - X_BARRA - 24, ALTO_BARRA, [
  { valor: e.K, color: p.blue,  etiqueta: 'cinética' },
  { valor: e.U, color: p.graph, etiqueta: 'potencial' },
  { valor: e.Q, color: p.red,   etiqueta: 'disipado' },
], { total: e.total, colorBorde: p.rule, colorTexto: p.paper });
```

Anchos medidos sobre la barra real de 828 px (franja de 880) en modo plano con μ = 0,3:
a s = 0 los tres segmentos dan 0 / 828 / 0; a s = 1 m, 199 / 414 / 215; al pie del plano,
398 / 0 / 430. En modo resorte, sobre los mismos 828 px: al soltar 0 / 828 / 0, a media
compresión 621 / 207 / 0, al salir del resorte 828 / 0 / 0, y detenido 0 / 0 / 828. Ningún
segmento
intermedio cae por debajo de los 24 px de `minEtiquetaPx` en las posiciones que el lector
va a mirar, salvo los que valen cero — que es justo cuando no querés el rótulo.

- [ ] **Paso 4: las dos escenas**

Un `encuadre()` por modo, los dos con `escalaUniforme: true` y `centrar: true`, margen
`{ L: 28, R: 24, T: 54, B: 26 }` (el `T` de 54 es el que reserva el aire de la barra):

- **plano:** `xMin: -0.35, xMax: 2.05, yMin: -0.35, yMax: 1.35`. Medido: 205,88 px/m a 880
  (canvas de 430 px de alto) y 124,12 px/m a 350 (canvas de 291 px). El plano mide 1,732 m
  de base y 1 m de alto, o sea 357 × 206 px a 880. Se dibuja con `suelo` para el piso y una
  recta para el plano; el bloque, con `bloque(..., { angulo: -ALFA })`, que ya acepta
  ángulo propio.
- **resorte:** `xMin: -0.40, xMax: 0.15, yMin: -0.06, yMax: 0.18`. Medido: 1458,33 px/m a
  880 y 541,82 px/m a 350. La compresión de 0,3 m mide 437 px a 880 y 162 px a 350; la
  distancia de frenado de 4,59 cm mide 67 px y 25 px. **Las dos son visibles en los dos
  viewports**, que era la duda: la diferencia de escala entre el empuje y el frenado es
  de 6,5 a 1, no de 100 a 1. El resorte se dibuja a mano con una `traza` en zigzag entre
  la pared y el bloque; la zona rugosa, con `suelo` desde x = 0 hasta el borde.

El lienzo va **sin ángulo** en los dos modos: en el modo plano hay un piso horizontal y un
plano inclinado en el mismo dibujo, y no hay un marco girado que le sirva a los dos.

- [ ] **Paso 5: las lecturas y el chequeo**

```js
const chequeo = (e.K + e.U + e.Q) - e.total;
leer('w2-k', num(e.K, 3) + ' J');
leer('w2-u', num(e.U, 3) + ' J');
leer('w2-q', num(e.Q, 3) + ' J');
leer('w2-v', num(e.v, 4) + ' m/s');
// Sin guarda de "-0,000": `num()` ya lo hace.
leer('w2-chequeo', num(chequeo, 3) + ' J');
```

Tres decimales en vez de dos porque en modo resorte el total es 0,090 J: con dos
decimales la barra entera se leería `0,09` y el chequeo no podría distinguirse de cero
aunque estuviera roto.

- [ ] **Paso 6: los párrafos de cierre de la sección, y el ejercicio 5 en prosa**

1. Los números del plano con μ = 0,3: llega abajo a 3,0685 m/s en vez de 4,4272, y la
   diferencia no es «un poco menos»: de los 9,80 J que había arriba, el rozamiento se
   comió 5,0922 J — **más de la mitad**. Y esa cuenta no depende de cuánto tarde ni de qué
   forma tenga el plano: es la fuerza de rozamiento por la distancia recorrida, nada más.
2. Poné μ en cero y mirá la lectura de velocidad: 4,4272 m/s. Es exactamente lo mismo que
   si el bloque se hubiera dejado caer derecho desde 1 m —el inciso (c) del ejercicio 3—.
   El peso es conservativo: le importa de dónde a dónde, no por dónde. Lo que **sí** cambia
   es el tiempo, la dirección de llegada y la distancia recorrida.
3. Pasá al modo resorte: cambia el depósito y no cambia nada más. La barra hace lo mismo,
   el chequeo sigue en cero, y la única diferencia es que arriba dice «elástica» en vez
   de «gravitatoria». Es el mismo ejercicio, escrito dos veces en el práctico.
4. Y el detalle del inciso (d) del ejercicio 4, que vale por sí solo: cuando el cuerpo
   llega a **la mitad** de su velocidad, no perdió la mitad de su energía, perdió **tres
   cuartos** — de 0,09 J le quedan 0,0225 J, así que el rozamiento le sacó 0,0675 J. La
   energía cinética va con *v*², no con *v*. Frenar un auto de 100 a 50 cuesta tres veces
   más energía que frenarlo de 50 a 0.

`<h3 class="titulo-seccion">`: **`Apoyar no es soltar`** — el ejercicio 5, en prosa, sin
widget. **La clase es `.titulo-seccion`, sin número delante y sin `style` propio.** En
`base.css` no hay clase de subtítulo y este plan no agrega ninguna (ver la Global
Constraint de tipografía); `cuerpo-aislado.html` ya usa `.titulo-seccion` sin numerar para
`Cinco variantes del mismo dibujo` y `Para tener a mano`, así que un título sin número ya
significa, en este sitio, «esto es subordinado». Se apoya **suavemente** una masa de 5 kg sobre un resorte vertical
de k = 2 N/m. El equilibrio está en x_eq = 24,5 m. Bajando hasta ahí el peso entrega
mg·x_eq = 1200,5 J, pero en el resorte quedan guardados sólo kx²/2 = 600,25 J: **la mitad
exacta**. ¿Dónde está la otra mitad? En la mano, que frenó el descenso y por lo tanto hizo
un trabajo de −600,25 J. Y el inciso (c) es la confirmación: si en vez de apoyarla se la
**suelta** desde 1 m de altura, la mano no está para frenar nada, toda la energía entra al
balance, y el resorte se comprime hasta 49,9804 m desde su longitud natural — 25,4804 m
**más allá** del equilibrio. «Comprimirse hasta el equilibrio y quedarse ahí» no es lo que
pasa en general: es lo que pasa cuando alguien te está frenando. No tiene widget propio
porque la interacción sería la misma que la del widget de arriba con otro dibujo; lo que
agrega es conceptual, y entra mejor en un párrafo (y porque `presupuestoPx` no admite
segmentos negativos, y el trabajo de la mano lo es: serían dos barras, «entra» y «sale»,
para una sola idea).

- [ ] **Paso 7: verificar**

1. Modo plano, μ = 0,3, animación al final: `v` = `3,0685 m/s`, `disipado` = `5,092 J`,
   `cinética` = `4,708 J`, `potencial` = `0,000 J`, chequeo `0,000 J`.
2. μ = 0: `v` = `4,4272 m/s` al pie. μ = 0,5: el bloque sigue bajando (tarda 2,47 s) y el
   chequeo sigue en cero.
3. Modo resorte, μ = 0,2: al salir del resorte `v` = `0,4243 m/s` y `cinética` = `0,090 J`;
   al detenerse, `disipado` = `0,090 J` y la posición final a 4,59 cm de donde arrancó la
   zona rugosa. **Medilo con el cursor sobre el canvas**, no de memoria.
4. Cambiá de modo con la animación corriendo: no tiene que quedar ni un segmento de barra
   del modo anterior, y `escena.duracion` tiene que haberse recalculado.
5. Rompelo a propósito: cambiá `Q` por `mu * M2 * G * s` (sin el `cos ALFA`) y confirmá
   que el chequeo se va a **`0,788 J`** al pie del plano con μ = 0,3. Volvé atrás.
   (La diferencia es μ·m·g·s·(1 − cos α) = 0,3 × 9,8 × 2 × 0,133975 = **0,787771 J**,
   corrida al corregir este plan; el `0,682 J` que decía antes no se puede reproducir.
   A mitad del plano, con s = 1 m, da `0,394 J`.)
6. 1280 y 390 px, los dos temas, consola limpia.

- [ ] **Paso 8: commit**

```bash
node --test "test/**/*.test.js"
git add docs/ensayos/energia.html
git commit -m "feat(ensayos): energia, el mismo presupuesto con dos depositos"
```

---

### Tarea 5: Widget 3 — la energía es continua; la tensión, no

**Archivos:**
- Modificar: `docs/ensayos/energia.html`

**Interfaces:**
- Consume: lo anterior, más `crearEscena`, `curva`, `cuerpo`, `vectorPx`, `arco`,
  **`traza`** (la cuerda, que en el segundo tramo es una polilínea de tres puntos:
  pivote → clavo → masa) y `colocarEtiqueta`.
- Produce: la sección 03 con el widget 3 y la prosa del ejercicio 6.

**El ejercicio (práctico 3, ej. 1).** Una masa cuelga de una cuerda de L = 1,32 m y se
suelta desde θ_A = 5°. Al pasar por el punto más bajo, la cuerda engancha en un clavo
puesto a d = 0,66 m del pivote, y el radio de giro pasa de L a L − d. Del bloque `Ej 1`:

| θ_A | v_B | θ_C | T/m antes | T/m después |
|---|---|---|---|---|
| 5° | 0,3138 m/s | 7,07° | 9,875 N/kg | 9,949 N/kg |
| 45° | 2,7528 m/s | 65,53° | 15,541 N/kg | 21,281 N/kg |
| 50° | 3,0400 m/s | 73,41° | 16,801 N/kg | 23,803 N/kg |

La velocidad en B es **la misma** justo antes y justo después de enganchar. La tensión, no
— y salta en el mismo instante, sin que nadie empuje nada. Eso es el widget.

- [ ] **Paso 1: la sección 03 y su franja**

`<h2>`: `03 · La energía es continua; la tensión, no`.

Párrafo previo: hay dos preguntas que parecen la misma y no lo son. «¿Cuánta energía
tiene?» es una pregunta sobre el **estado**: depende de dónde está y a qué velocidad va, y
nada más. «¿Cuánto tira la cuerda?» es una pregunta sobre el **instante**: depende además
de qué curva está describiendo justo ahí. Este ejercicio las separa de la manera más
limpia posible, porque la trayectoria cambia de radio de golpe y la velocidad ni se
entera.

La franja:

- `.encabezado-widget`: `Simulación 3` · `El péndulo y el clavo` ·
  `— la velocidad no se entera de nada; la tensión salta en el mismo instante.`
- `<canvas id="w3-cv">`
- controles: `Reproducir` (`w3-play`), `Reiniciar` (`w3-reset`), deslizador `w3-theta`
  (`min="5" max="50" step="1" value="5"`, salida en grados).
- `.lecturas`: `v en B` (`w3-v`, azul), `θ_C` (`w3-thc`), `T/m antes` (`w3-ta`, rojo),
  `T/m después` (`w3-td`, rojo) y `v antes − v después` (`w3-chequeo`, `--dim`).

El tope en 50° no es arbitrario: **a partir de θ_A = 60° la cuerda se afloja**. Medido:
cos θ_C = 1 − 2(1 − cos θ_A), así que θ_C = 90° exactamente cuando cos θ_A = 0,5, o sea
θ_A = 60°; de ahí para arriba la masa pasaría la horizontal con el hilo tenso, que un hilo
no puede hacer, y las ecuaciones dejan de describir nada. Es el mismo criterio que frena
el deslizador de revoluciones del péndulo cónico en el ensayo 4 cuando N llega a cero. Los
tres valores del script —5°, 45° y 50°— caen dentro, y 50° deja un margen de 10°.

- [ ] **Paso 2: la física**

```js
/* ---------- widget 3: el pendulo y el clavo ---------- */

// Practico 3, ej. 1. Cuerda de L = 1.32 m, clavo a d = 0.66 m del pivote (o sea, la
// mitad justa). Verificado en el bloque "Ej 1":
//   th_A = 5  -> v_B = 0.3138  th_C = 7.07   T/m: 9.875  -> 9.949
//   th_A = 45 -> v_B = 2.7528  th_C = 65.53  T/m: 15.541 -> 21.281
//   th_A = 50 -> v_B = 3.0400  th_C = 73.41  T/m: 16.801 -> 23.803
const L3 = 1.32, D3 = 0.66, R3 = L3 - D3;

// La velocidad en el punto mas bajo, por conservacion: NO depende del radio, porque el
// radio no aparece en el balance de energia. Este es el numero que no se entera del
// clavo, y la razon esta en esta linea: el clavo no le hace trabajo a nada (la tension
// es siempre perpendicular a la velocidad) y la altura de caida es la misma.
const vB = thA => Math.sqrt(2 * G * L3 * (1 - Math.cos(thA)));

// El angulo maximo del otro lado, con el radio NUEVO.
const thC = thA => Math.acos(1 - (L3 / R3) * (1 - Math.cos(thA)));

// La tension por unidad de masa, en cualquier punto de cualquiera de los dos arcos. El
// radio entra ACA y solo aca: T/m = g cos(ang) + v^2 / radio. Es la unica diferencia
// entre "antes" y "despues", y es toda la diferencia.
const tension = (ang, v, radio) => G * Math.cos(ang) + v * v / radio;
```

Comprobación cerrada, que hay que hacer antes de dibujar: `tension(0, vB(thA), L3)` tiene
que dar `G * (3 - 2 * Math.cos(thA))` y `tension(0, vB(thA), R3)` tiene que dar
`G * (5 - 4 * Math.cos(thA))` —las dos expresiones del script— para cualquier θ_A. Si no
coinciden, el `v²/r` está mal escrito. Verificado al escribir este plan para 5°, 45° y 50°.

- [ ] **Paso 3: el dibujo**

Encuadre: `xMin: -1.8, xMax: 1.8, yMin: -1.45, yMax: 0.15`, con
`margen: { L: 30, R: 30, T: 26, B: 26 }`, `escalaUniforme: true`, `centrar: true`.

Medido con el `crearWidget` real: a 880 px el canvas sale de **416 px** de alto con
**227,50 px/m**; a 350 px, de **215 px** con **80,56 px/m**. El recorrido completo, a
θ_A = 50° (el caso más ancho), ocupa x ∈ [−1,011 , 0,633] e y ∈ [−1,320 , −0,848] —
medido barriendo los dos arcos—, así que entra entero con aire de sobra, y el pivote
(0, 0) y el clavo (0, −0,66) quedan los dos dentro del encuadre.

El encuadre es más ancho que el recorrido a propósito: ese ancho es lo que hace que la
escala vertical alcance los 227,50 px/m, con los que la cuerda de 1,32 m mide 300 px. Con
un encuadre ajustado al recorrido (2,0 × 1,6) la escala sube apenas a 236,25 px/m y el
canvas se clava en el tope de 430 px — no vale la pena.

Qué se dibuja:

- El pivote y el clavo, dos `cuerpo` chicos en `--ink` y `--dim`.
- **Los dos arcos completos**, con `curva` en `--graph`: el de radio L entre −θ_A y 0
  alrededor del pivote, y el de radio L − d entre 0 y θ_C alrededor del clavo. Es lo que
  hace ver de un vistazo que el radio se achicó a la mitad y que del otro lado sube
  **más abierto** de lo que bajó.
- La cuerda, con **`traza`** (`dibujo.js:292`), que toma una lista de puntos del marco y
  los une: `[pivote, masa]` en el primer tramo y `[pivote, clavo, masa]` en el segundo.
  Ese quiebre —una polilínea de tres puntos en vez de dos— es el momento, y no hace falta
  primitiva nueva para dibujarlo.
- La masa, un `cuerpo` de radio 6 en `--ink`.
- Los arquitos de θ_A y θ_C, con `arco`, rotulados.
- **Las dos flechas de tensión en B, siempre visibles**, ancladas en el punto más bajo
  (0, −L) y apuntando las dos hacia arriba (las dos van a lo largo de la cuerda, que ahí
  es vertical). Como son colineales, se dibujan separadas 10 px a cada lado del eje, una
  rotulada `T antes` y la otra `T después`. **Los dos rótulos van por la opción `rotulo:`
  de `vectorPx`** —no por `texto()`—, con `rdx` de signo opuesto en cada una (`-6` en la
  izquierda con `rAlineacion: 'right'`, `+6` en la derecha) para que `colocarEtiqueta` los
  separe hacia afuera y no uno encima del otro. Este widget no usa `panelesApilados`, así
  que el segundo límite de `etiqueta.js` no lo toca.

La escala de las flechas de tensión, y la advertencia que la acompaña:

```js
// La tension mas grande que este widget puede mostrar es T/m = 23.803 N/kg (th_A = 50).
// Se le dan 0.55 m del marco, y de ahi salen los metros por N/kg. Medido: 5.26 px por
// N/kg a 880 y 1.86 px a 350.
const K_T = 0.55 / 23.803;
```

**Lo que hay que decir en voz alta, porque el dibujo no puede ocultarlo:** a θ_A = 5° —el
valor del enunciado— las dos tensiones difieren en 0,074 N/kg, o sea **0,39 px a 880 y
0,14 px a 350**. Las dos flechas se ven exactamente iguales, y no hay escala que arregle
eso sin volver ridícula la del resto. A θ_A = 50° la diferencia es de **36,80 px a 880 y
13,03 px a 350**, perfectamente visible. Por eso:

- el deslizador arranca en **5°**, que es el caso del enunciado y el que las lecturas
  reproducen;
- el párrafo de cierre manda explícitamente llevarlo a 50° para ver las flechas separarse;
- y el salto de la tensión, en el caso del enunciado, **se lee en los números**, no en el
  dibujo. Un widget que pretendiera mostrar ese 0,7 % con dos flechas estaría mintiendo.

La animación: la masa recorre A → B → C. Para no integrar la ecuación del péndulo, la
escena usa como parámetro el **ángulo**, no el tiempo físico: `escena.duracion` se reparte
entre los dos tramos en proporción a su longitud de arco (L·θ_A y (L−d)·θ_C) y el ángulo
avanza linealmente dentro de cada uno. **Esto no es el movimiento real** —el péndulo va más
rápido cerca de B—, y hay que decirlo en un comentario del código: lo que el widget mide
son la velocidad y la tensión en cada posición, que sí son las reales; el ritmo con que
las recorre es de dibujo. Si el dueño quiere el ritmo real, es integrar
dθ/dt = v(θ)/radio, y es un cambio acotado a esa función.

- [ ] **Paso 4: las lecturas**

```js
const va = vB(thA), vd = vB(thA);   // los dos por el MISMO camino? NO -- ver abajo
```

No: el chequeo tiene que venir de dos caminos. La velocidad «antes» se calcula por
conservación desde A con radio L; la velocidad «después» se calcula **hacia atrás desde
C** con radio L − d, o sea `Math.sqrt(2 * G * R3 * (1 - Math.cos(thC(thA))))`. Las dos
tienen que dar el mismo número, y dan, porque la energía no se enteró del clavo. Si
alguien mete el radio nuevo en el balance de energía —el error clásico de este ejercicio—
esa resta deja de ser cero al instante.

```js
const vAntes = vB(thA);
const vDespues = Math.sqrt(2 * G * R3 * (1 - Math.cos(thC(thA))));
leer('w3-v', num(vAntes, 4) + ' m/s');
leer('w3-thc', num(thC(thA) * 180 / Math.PI, 2) + '°');
leer('w3-ta', num(tension(0, vAntes, L3), 3) + ' N/kg');
leer('w3-td', num(tension(0, vAntes, R3), 3) + ' N/kg');
// Sin guarda de "-0,0000": `num()` ya lo hace.
leer('w3-chequeo', num(vAntes - vDespues, 4) + ' m/s');
```

- [ ] **Paso 5: los párrafos de cierre, y el ejercicio 6 en prosa**

1. Los números a 5°: v_B = 0,3138 m/s, θ_C = 7,07°. Sube **más abierto** de lo que bajó, y
   no porque haya ganado nada: llega a la misma altura que tenía al empezar —eso es lo que
   dice la conservación— pero como ahora gira con la mitad del radio, la misma altura pide
   más ángulo. La energía fija la altura; la geometría decide el ángulo.
2. Y en el mismo instante, sin que nadie toque nada, la cuerda pasa de tirar 9,875 a 9,949
   N/kg. La velocidad no cambió ni un milímetro por segundo. Lo único que cambió es el
   radio, y el radio entra en la tensión (T/m = g cos θ + v²/r) y **no** entra en la
   energía. Llevá el deslizador a 50°: ahí el salto es de 16,801 a 23,803 N/kg —un 42 %— y
   las dos flechas se separan a la vista.
3. Por qué la energía no se entera: la tensión de la cuerda **no hace trabajo, nunca**,
   porque es perpendicular a la velocidad en todo instante. El clavo cambia hacia dónde
   apunta esa tensión, no cuánta energía hay. Si alguna vez un problema parece pedir «la
   energía que aportó la cuerda», la respuesta es cero y la pregunta estaba mal.

`<h3 class="titulo-seccion">` (misma decisión que el subtítulo de la sección 02: clase
existente, sin número y sin `style` propio): **`Lo mismo, sin nada que gire`** — el
ejercicio 6 en prosa. Un embalaje de 250 kg
cuelga de un cable de 10 m y se lo aparta 1 m de la vertical (θ = 5,74°). Cuatro preguntas
y cuatro respuestas que este ensayo ya tiene todas: (a) sostenerlo ahí pide F = mg tan θ =
**246,23 N**; (b) sostenerlo **no hace trabajo**: el desplazamiento es cero, y no importa
cuánto te canses; (c) moverlo de lado **sí** hizo trabajo, porque al apartarse el embalaje
**subió** dh = L − √(L² − l²) = 0,050126 m, así que W = mg·dh = **122,81 J** — y ojo con la
trampa: F·l = 246,2 J **no** es la respuesta, porque F no vale 246,23 N durante el
traslado, vale eso sólo al final (arranca en cero); (d) la tensión del cable **no trabaja
en ningún instante**, por lo mismo que en el péndulo de arriba. Es el ejercicio 1 sin el
clavo y sin nada que gire, y por eso no necesita animación propia: no tiene nada que
mostrar que la simulación de arriba no muestre ya.

- [ ] **Paso 6: verificar**

1. Lecturas a 5°: `0,3138 m/s`, `7,07°`, `9,875 N/kg`, `9,949 N/kg`, `0,0000 m/s`.
   A 45°: `2,7528`, `65,53°`, `15,541`, `21,281`, `0,0000`. A 50°: `3,0400`, `73,41°`,
   `16,801`, `23,803`, `0,0000`. Contra el bloque `Ej 1`.
2. **Medí las dos flechas a 50°**: tienen que dar 88 px y 125 px a 880, con 37 px de
   diferencia. A 5°, las dos alrededor de 52 px y la diferencia bajo 1 px — eso está bien,
   es lo esperado, no un defecto.

   **Y este paso no es cosmético: es el único guardián de la tensión.** Descubierto
   midiendo, durante la ejecución: la lectura de chequeo de este widget compara `v` antes y
   después del enganche, y **nunca llama a la fórmula de la tensión**. Una rotura ahí
   —`v²/r` por `v/r`, o no alternar los radios al enganchar— deja el chequeo en `0,0000`
   para todo θ_A. Se evaluó construir un segundo chequeo y **se descartó con argumento**: el
   tiempo de esta animación es ficticio (el ángulo avanza lineal), así que diferenciar la
   trayectoria dibujada daría una aceleración de dibujo y no una física; un camino genuino
   exigiría integrar la ODE del péndulo en tiempo real, que es justo lo que el diseño evitó,
   y cambiaría una resta exacta por una comparación con tolerancia. No vale la máquina.

   Lo que sí atrapa las dos roturas es **medir estas flechas**: con los radios sin alternar
   quedan idénticas incluso a 50°, donde tienen que diferir 37 px. Así que el guardián de la
   tensión en este widget es manual y vive en este paso. Saltearlo es quedarse sin él.
3. La cuerda se quiebra en el clavo en el segundo tramo. Reproducí y mirá el instante del
   quiebre cuadro por cuadro si hace falta.
4. Rompelo a propósito: cambiá `vB` por `Math.sqrt(2 * G * R3 * (1 - Math.cos(thA)))` (el
   radio nuevo en el balance de energía) y confirmá que el chequeo deja de dar cero.
5. 1280 y 390 px, los dos temas, consola limpia, no se anima solo al cargar.

- [ ] **Paso 7: commit**

```bash
node --test "test/**/*.test.js"
git add docs/ensayos/energia.html
git commit -m "feat(ensayos): energia, el pendulo y el clavo"
```

---

### Tarea 6: Widget 4 — sólo la altura, hasta que deja de serlo, y el cierre del ensayo

**Archivos:**
- Modificar: `docs/ensayos/energia.html`

**Interfaces:**
- Consume: todo lo anterior.
- Produce: la sección 04 con el widget 4 en sus dos escenas, la sección `Para tener a
  mano`, y el ensayo 7 terminado.

**Los ejercicios.** Ej 7: un carro de montaña rusa sin fricción parte de A con v₀; A y B
están a la misma altura *h*, C a *h*/2, y de D a E hay un tramo llano de largo *L* donde
hay que frenarlo hasta detenerlo. Con los valores del bloque `Ej 7 (numerico)` (m = 1 kg,
v₀ = 2 m/s, h = 3 m, L = 5 m): **E = 31,4 J**, **v_B = 2,0000 m/s** (igual a v₀),
**v_C = 5,7793 m/s**, **v_D = 7,9246 m/s**, **a = 6,2800 m/s²**. Ej 8: un bloque de 1 kg se
suelta en A sobre un cuadrante de R = 1,5 m, llega a B con v_B = 3,6 m/s y se detiene tras
d = 2,7 m de piso rugoso: **μ = 0,244898**, **K_B = 6,480 J**, **mgR = 14,700 J**,
**W_roce en el arco = −8,220 J**.

- [ ] **Paso 1: la sección 04 y su franja**

`<h2>`: `04 · Sólo la altura, hasta que deja de serlo`.

Párrafo previo: hasta acá cada balance miraba un tramo. Ahora un sistema entero, con
subidas y bajadas, y una sola cuenta que vale de punta a punta. Y con ella la afirmación
más fuerte —y más fácil de creer de más— del tema: mientras no haya rozamiento, la
velocidad en cualquier punto depende **sólo de la altura de ese punto**, no de qué forma
tuvo el camino para llegar. La segunda escena es donde esa afirmación se acaba.

**Advertencia de honestidad que tiene que estar en la página:** el enunciado del ejercicio
7 no da ninguna masa, así que todas las energías de este widget están **por kilogramo**.
Decirlo en el encabezado del widget, no sólo en el código.

La franja:

- `.encabezado-widget`: `Simulación 4` · `Sólo la altura` ·
  `— la barra no cambia de largo en todo el recorrido, suba o baje; recién el freno le saca.`
- `<canvas id="w4-cv">`
- controles: `Reproducir` (`w4-play`), `Reiniciar` (`w4-reset`), deslizadores `w4-v0`
  (`min="1" max="5" step="0.1" value="2"`, m/s) y `w4-h` (`min="1.5" max="4" step="0.1"
  value="3"`, m), y casilla `w4-escena` con la etiqueta `El cuadrante (ej. 8)`.
- `.lecturas`: `v` (`w4-v`, azul), `v marcha − v(y)` (`w4-chequeo`, `--dim`),
  `a medida − a cerrada` (`w4-chequeo-a`, `--dim`), `v_B` (`w4-vb`), `v_C` (`w4-vc`) y
  `a del freno` (`w4-a`, rojo). Son **seis** y no cinco: los dos tramos tienen física
  distinta —uno sin fricción, otro con una desaceleración constante— y ningún chequeo
  cubre al otro. El Paso 4 dice por qué, y por qué el que había antes no servía.

- [ ] **Paso 2: el perfil, que este plan inventa**

El práctico da una figura sin coordenadas: lo único que fija son las alturas de A, B, C y
D-E. Todo lo demás —dónde caen los valles, qué tan anchas son las lomas— es decisión de
dibujo, y **esta parte del plan es la menos verificada de todas: revisala a ojo cuando la
veas pintada.**

```js
// Perfil de la montana rusa. Las ALTURAS salen del enunciado (A y B en h, C en h/2, D y E
// en 0); las abscisas las elige este dibujo. Entre nodo y nodo se interpola con medio
// coseno, que da lomas y valles con tangente horizontal en los extremos -- sin picos.
//
// OJO CON EL ACOPLAMIENTO: el nodo E codifica la longitud del tramo de freno, y `a` se
// calcula con esa misma longitud. Si una se moviera sin la otra, el carro dejaria de
// detenerse en E y ninguna lectura lo marcaria. Por eso `L` NO es una constante suelta:
// sale de restar las abscisas de los dos nodos, y el perfil las usa a ellas. Asi el
// defecto no puede existir.
const X_D = 8, X_E = 13;
const L = X_E - X_D;                                  // 5 m, el L del enunciado
const NODOS = h => [[0, h], [2, 0.2 * h], [4, h], [6.5, h / 2], [X_D, 0], [X_E, 0]];
function perfil(x, h) {
  const n = NODOS(h);
  for (let i = 0; i < n.length - 1; i++) {
    const [x0, y0] = n[i], [x1, y1] = n[i + 1];
    if (x >= x0 && x <= x1) {
      const u = (x - x0) / (x1 - x0);
      return y0 + (y1 - y0) * (0.5 - 0.5 * Math.cos(Math.PI * u));
    }
  }
  return 0;
}

// La PENDIENTE local del perfil, por diferencia centrada. El `Math.min/Math.max` no es
// decoracion: `perfil` devuelve 0 fuera de [0, X_E], asi que sin acotar el punto de
// evaluacion la pendiente en x = 0 sale (h - 0)/2e-6 = un millon y medio, y la marcha de
// abajo explota en el primer paso. Medido al escribir esta correccion.
const EPS = 1e-6;
const pendiente = (x, h) => {
  const xc = Math.min(Math.max(x, EPS), X_E - EPS);
  return (perfil(xc + EPS, h) - perfil(xc - EPS, h)) / (2 * EPS);
};
```

Comprobado sobre ese perfil con v₀ = 2 y h = 3: en x = 0 y x = 4 (A y B) la velocidad da
**2,000 m/s** las dos veces aunque en el valle del medio (x = 2) llegue a 7,144 m/s; en
x = 6,5 (C) da **5,779 m/s**; en x = 8 (D) da **7,925 m/s**. Los tres coinciden con el
bloque `Ej 7 (numerico)` hasta el último dígito impreso. El tramo A → D mide 11,656 m de
recorrido y se hace en **2,6146 s**; el frenado D → E tarda **1,2619 s** y recorre
exactamente los 5,000 m de L. **Duración total de la animación: 3,8765 s.**

El tramo con freno se resuelve en cerrado (`s(t) = v_D t − ½ a t²`), no integrando, porque
la velocidad llega a cero en E y `ds/v` divergería. El tramo sin fricción sí se integra
numéricamente —`dt = ds / v(s)`— una sola vez por cambio de deslizador, no por cuadro, y
la tabla resultante se invierte por interpolación para sacar x(t).

**Y esa integración es también el segundo camino del chequeo.** Es la misma lección que la
Tarea 4 Paso 2: si la velocidad de la animación sale de la conservación, entonces cualquier
lectura armada con esa velocidad ya sabe la respuesta. Acá el arreglo es gratis, porque el
recorrido en pasos chicos de `ds` que `dt = ds/v` necesita **es** el lugar donde integrar
la segunda ley. En vez de leer `v(s)` de la forma cerrada, se la **acumula**:

```js
// Camino B -- integrar la segunda ley A LO LARGO DE LA PISTA. Proyectada sobre la
// tangente: m dv/dt = -m g sen(theta), y con dv/dt = v dv/ds queda
//
//     v dv/ds = -g sen(theta)      <=>      d(v^2)/ds = -2 g sen(theta)
//
// con sen(theta) = y'(x) / sqrt(1 + y'(x)^2), sacado de la PENDIENTE del perfil. Este
// camino no mira `h` ni una sola vez; el camino A -- la forma cerrada
// v(y) = sqrt(v0^2 + 2 g (h - y)) -- no mira la pendiente ni una sola vez. Por eso la
// resta puede no dar cero, que es todo lo que le pedimos a un canario.
//
// Se corre UNA vez por cambio de deslizador (no por cuadro) y devuelve la tabla que la
// animacion ya necesitaba para invertir x(t): la integracion del tiempo es una
// acumulacion mas dentro del mismo bucle, no un bucle nuevo.
function marchaNewton(h, v0, n = 2000) {
  const dx = X_D / n;
  const senTheta = m => m / Math.hypot(1, m);         // NO `m` a secas: ver el Paso 8
  const f = m => -2 * G * senTheta(m);
  let v2 = v0 * v0, s = 0, t = 0;
  const tabla = [{ x: 0, s: 0, t: 0, v: v0 }];
  for (let i = 0; i < n; i++) {
    const x0 = i * dx, x1 = x0 + dx;
    const m0 = pendiente(x0, h), m1 = pendiente(x1, h);
    const ds0 = Math.hypot(1, m0) * dx, ds1 = Math.hypot(1, m1) * dx;
    const va = Math.sqrt(v2);
    v2 += 0.5 * (f(m0) * ds0 + f(m1) * ds1);          // trapecio sobre el arco
    const vb = Math.sqrt(v2);
    s += 0.5 * (ds0 + ds1);
    t += 0.5 * (ds0 / va + ds1 / vb);                 // dt = ds / v, el mismo trapecio
    tabla.push({ x: x1, s, t, v: vb });
  }
  return tabla;
}
```

**Corrido al corregir este plan, con n = 2000.** La marcha reproduce, dígito por dígito,
los cinco números que este Paso ya tenía verificados por el otro camino: v en A y B
**2,0000 m/s**, en C **5,7793 m/s**, en D **7,9246 m/s**, recorrido A→D **11,6561 m** y
tiempo A→D **2,6146 s**. Y la diferencia contra la forma cerrada, punto por punto: **peor
caso 1,5 × 10⁻⁵ m/s** con v₀ = 2 y h = 3, y **1,7 × 10⁻⁵ m/s** barriendo los dos
deslizadores enteros (h de 1,5 a 4 y v₀ de 1 a 5, de a 0,1). Con cuatro decimales eso
imprime `0,0000 m/s`. Si se bajara `n` a 200 el peor caso sube a 1,1 × 10⁻³ m/s y la
lectura empezaría a titilar en el cuarto decimal: **2000 no es un número redondo elegido a
ojo, es el que deja el ruido dos órdenes por debajo de lo que se muestra.**

- [ ] **Paso 3: el encuadre y la barra**

`xMin: 0, xMax: 13, yMin: -0.3, yMax: 3.4`, con `margen: { L: 30, R: 24, T: 64, B: 26 }`
(el `T` de 64 reserva el aire de la barra) y `escalaUniforme: true`.

Medido: a 880 px el canvas sale de **325 px** de alto con **63,51 px/m**, así que h = 3 m
son 191 px y L = 5 m son 318 px. A 350 px el canvas se clava en el mínimo de 215 px con
**22,77 px/m** (h = 68 px, L = 114 px) y el sobrante vertical se va al margen superior, que
pasa a 104,8 px — la barra, que va a y = 16 px, queda igual en su lugar y con más aire
debajo. El `yMax` de 3,4 tiene que seguir a `h` si el deslizador de `h` se mueve: el
encuadre se recalcula con `yMax: h + 0.4`.

La barra, igual que en el widget 2: de 28 px al borde izquierdo a 24 px del derecho, o sea
828 px a 880 y **298** px a 350 (350 − 28 − 24 = 298; los 296 que decía este plan eran un
error de tipeo, y las Tareas 4 y 9 ya decían 298). Segmentos: cinética (azul), potencial (`--graph`) y, sólo en
el tramo de freno, disipado (rojo). **Cada uno de un origen distinto**, igual que en el
widget 2: la cinética de la velocidad que devolvió `marchaNewton`, la potencial de la
altura del perfil, y el disipado de `a·s`. Que la barra se vea llena en todo el recorrido
es entonces una consecuencia medible —el residuo de la marcha, 10⁻⁵— y no una identidad
algebraica. Anchos medidos sobre esos 828 px, con v₀ = 2 y h = 3: en A, 53 / 775 / 0; en el valle,
673 / 155 / 0; en D, 828 / 0 / 0; a mitad del freno, 414 / 0 / 414; en E, 0 / 0 / 828.

- [ ] **Paso 4: los dos chequeos, y el que NO sirve**

Primero el que no sirve, porque es el que sale solo y hay que saber descartarlo. La
tentación es leer `(K + U + Q) − (½v₀² + gh)`, con K sacada de la velocidad de la
animación. **Eso da cero por construcción y no dice absolutamente nada.** La velocidad de
la animación viene *de* la conservación —el Paso 2 integra el tramo sin fricción con
`dt = ds/v(s)`, o sea que `v(s)` es una **entrada** del dibujo, no un resultado—, así que
`K = ½v₀² + g(h−y)` y `U = g·y`, y su suma es `½v₀² + gh` **algebraicamente, para
cualquier perfil, cualquier g y cualquier h**. En el tramo de freno pasa lo mismo: con
`v = v_D − a·t` y `s = v_D·t − ½a·t²`, `K + Q ≡ ½v_D²` para cualquier `a`. Esa resta
detecta exactamente una cosa —que el nodo A del perfil valga `h`— y es ciega al perfil, a
`a`, a `g` y a `h`. Llamarla «la lectura central del widget» y decir que prueba «que lo
que pasó en el medio no importa» sería exactamente lo que la Tarea 4 Paso 2 prohíbe.

Los dos que sí sirven, uno por tramo:

**Tramo sin fricción — `v marcha − v(y)`, en m/s.** La marcha de Newton del Paso 2
integra `v dv/ds = −g·sen θ` usando la **pendiente local del perfil**; la forma cerrada
`v(y) = √(v₀² + 2g(h−y))` usa **la altura y `h`**. Un camino no mira `h`; el otro no mira
la pendiente. Muerde de verdad cuando el perfil y el balance de energía describen curvas
distintas — que es el error que un perfil inventado a mano tiene más chances de tener.

```js
const p = tabla[i];                                  // el punto de la marcha en este cuadro
const vCerrada = Math.sqrt(v0 * v0 + 2 * G * (h - perfil(p.x, h)));
leer('w4-chequeo', num(p.v - vCerrada, 4) + ' m/s');
```

**Tramo de freno — `a medida − a cerrada`, en m/s².** Es lo que el informe de
investigación proponía (`energia.md` líneas 243-244) y que conviene no perder. **La
animación NO frena con la fórmula del enunciado**: frena con la desaceleración que hace
falta para clavar el carro en E, sacada de la `v_D` que dio la marcha y de la longitud del
tramo D-E que sale del perfil. La forma cerrada del papel entra sólo del otro lado de la
resta.

```js
// La animacion: la desaceleracion sale de la MARCHA y del PERFIL.
const vD = tabla[tabla.length - 1].v;
const aAnimacion = vD * vD / (2 * L);                // L = X_E - X_D, del perfil
// El papel: a = (v0^2 + 2 g h) / (2 L). No pasa por la marcha ni por el perfil.
const aCerrada = (v0 * v0 + 2 * G * h) / (2 * L);
// La medida, leida de la animacion como la leeria alguien con un cronometro:
const aMedida = (vD * vD - v * v) / (2 * sFreno);    // = aAnimacion, por su cinematica
leer('w4-a', num(aCerrada, 4) + ' m/s²');
leer('w4-chequeo-a', num(aMedida - aCerrada, 4) + ' m/s²');
```

Esa resta vale `(v_D,marcha² − (v₀² + 2gh)) / (2L)`: da cero **si y sólo si** la marcha
llega a D con la velocidad que la forma cerrada predice y el tramo llano del dibujo mide
lo que `L` dice. Dicho de otro modo: dice que el carro se detiene **exactamente en E**, que
es la pregunta del inciso (c).

Cada lectura muestra `—` en el tramo donde no aplica: `w4-chequeo` durante el freno,
`w4-chequeo-a` antes de D. Fingir un chequeo donde no hay dos caminos es peor que no
tenerlo — el mismo criterio que la Tarea 8 aplica al modo explosión.

**Valores corridos al corregir este plan** (n = 2000, v₀ = 2 m/s, h = 3 m):

| | modelo correcto | roto a propósito (ver Paso 8) |
|---|---|---|
| `v marcha − v(y)`, peor punto | **−1,5 × 10⁻⁵ m/s** → `0,0000` | **+2,3141 m/s** en x ≈ 1,69 |
| `v marcha − v(y)` en D | −1,5 × 10⁻⁵ m/s → `0,0000` | **+1,4687 m/s** |
| `a medida − a cerrada` | **−2,3 × 10⁻⁵ m/s²** → `0,0000` | **+2,5434 m/s²** |

Peor caso barriendo los dos deslizadores enteros con el modelo bueno: **1,7 × 10⁻⁵ m/s** y
**3,1 × 10⁻⁵ m/s²**. Los dos imprimen `0,0000` con cuatro decimales, con dos órdenes de
margen.

Y dos lecturas de contraste que no son chequeos sino el resultado del ejercicio: `v_B`
(que tiene que dar exactamente v₀, sea cual sea la altura del valle intermedio) y
`a del freno`, la forma cerrada `(v₀² + 2gh) / (2L)` = 6,2800 m/s².

- [ ] **Paso 5: la segunda escena — el cuadrante (ej. 8)**

Con la casilla marcada, el widget cambia de escena entera: un cuadrante de circunferencia
de R = 1,5 m que baja hasta B y un tramo horizontal de d = 2,7 m hasta C.

**Dónde está anclado el arco**, que este plan no decía y sin lo cual el encuadre no se
puede calcular. Centro de la circunferencia en (R, R) = (1,5 ; 1,5), con el piso en y = 0:

```js
const R8 = 1.5, D8 = 2.7;
// phi de 0 a pi/2: en 0 el punto es A = (0, R) -con tangente VERTICAL, que es donde se
// suelta el bloque-, y en pi/2 es B = (R, 0), con tangente horizontal.
const arcoPunto = phi => [R8 - R8 * Math.cos(phi), R8 - R8 * Math.sin(phi)];
const X_A8 = 0, X_B8 = R8, X_C8 = R8 + D8;            // 0 , 1.5 , 4.2
```

Con eso la escena ocupa **de x = 0 a x = 4,2 m**: el arco se come 1,5 m y el piso rugoso
otros 2,7. El `xMax: 4.0` que decía este plan **dejaba afuera el punto donde el bloque se
detiene, que es la respuesta del ejercicio** — medido, a 350 px el bloque quedaba en el
píxel 339,5 con el borde útil del marco en el 326.

Encuadre corregido: `xMin: -0.4, xMax: 4.5, yMin: -0.3, yMax: 1.9`, `centrar: true`.
Medido llamando al `crearWidget` real: a 880 px el canvas sale de **430 px** con
**154,55 px/m** (R = 232 px, d = 417 px, y el punto de detención en el píxel 775 contra un
borde útil en el 822) y a 350 px, de **223 px** con **60,41 px/m** (R = 91 px, d = 163 px,
detención en el píxel 308 contra un borde en el 326). Los 0,3 m que sobran a la derecha
son aire a propósito: la flecha o el rótulo del punto de detención necesitan lugar. El
arco se dibuja con `curva` recorriendo φ; el piso rugoso, con `suelo` de X_B8 a X_C8.

Acá los deslizadores no hacen nada —el ejercicio no tiene parámetros libres— y hay que
deshabilitarlos, no dejarlos moviendo una escena que los ignora.

**Y esta escena no tiene chequeo, y hay que decirlo.** Las dos lecturas de chequeo
muestran `—` mientras la casilla esté marcada. No es un descuido: el ejercicio 8 no tiene
ni un parámetro libre, y todos sus números salen de un solo paso algebraico sobre los
datos, así que cualquier «segundo camino» que se escribiera sería el primero despejado al
revés —μ = v_B²/(2gd) y μmgd = K_B son **la misma ecuación**, y su resta da cero por
construcción igual que la que este Paso 4 acaba de descartar—. El canario del widget 4
vive en la escena de la montaña rusa, que es la que tiene deslizadores; esta escena
dibuja un resultado.

La barra, en esta escena, se dibuja contra un total distinto: **mgR = 14,700 J**, la
energía que el bloque tenía arriba de todo. En B los segmentos dan `K = 6,480 J` y
`disipado en el arco = 8,220 J` — o sea 365 px y 463 px sobre los 828. Y el punto entero de
este ejercicio: **esos 8,220 J no salen de μ·N·d**. No se pueden sacar así, porque en el
arco la normal cambia en cada punto (con el ángulo y con la velocidad) y el enunciado ni
siquiera da el μ del arco. Salen de restar: K_B − mgR. El teorema trabajo-energía entre
dos puntos donde sí se conoce todo es la **única** salida.

En el tramo llano, en cambio, μ·N·d sí vale, porque el piso es horizontal y N = mg no
cambia: de ahí sale μ = v_B²/(2gd) = **0,244898**, y el control cruzado
μ·m·g·d = **6,4800 J** = K_B cierra exacto.

- [ ] **Paso 6: los párrafos de cierre de la sección**

1. Los números: con v₀ = 2 m/s y h = 3 m, E = 31,4 J por kilogramo, v_B = 2,0000 m/s,
   v_C = 5,7793 m/s, v_D = 7,9246 m/s, y el freno tiene que dar a = 6,2800 m/s². Mirá v_B:
   es **exactamente** v₀, aunque entre A y B el carro haya bajado a un valle y subido de
   nuevo pasando por 7,14 m/s. Misma altura, misma velocidad. El camino del medio no dejó
   rastro.
2. Movés el deslizador de h y la barra cambia de reparto pero no de largo, en todo el
   recorrido. Eso es la conservación, dibujada. Recién en el tramo D-E aparece el cuarto
   segmento, y ahí el freno se lleva los 31,4 J enteros a lo largo de los 5 m: no es
   casualidad, es lo que significa «detenerse en E».
   Y la lectura que respalda esa frase no es la barra —una barra llena puede estar llena
   por definición— sino `v marcha − v(y)`: una de las dos velocidades sale de integrar la
   segunda ley contra la **pendiente** del perfil, la otra de la **altura** y nada más.
   Que su resta no se despegue de cero en ningún punto del recorrido es lo que dice, con
   un número, que la forma del camino no entró en la cuenta.
3. Marcá la casilla. Acá el mismo truco falla: en el arco no se puede escribir μ·N·d
   porque no se sabe N en cada punto —cambia con el ángulo y con la velocidad— y el
   enunciado ni da el μ del arco. Pero la energía sigue siendo una cuenta, y la cuenta se
   puede cerrar por el otro lado: arriba había 14,700 J, abajo quedan 6,480 J, así que el
   rozamiento del arco se llevó 8,220 J. **No se integró nada.** Es el teorema
   trabajo-energía haciendo lo único que a veces se puede hacer.
4. Y en el tramo llano, donde N sí es constante, la cuenta vuelve a funcionar como en la
   sección 02: μ = v_B²/(2gd) = 0,2449, y μmgd = 6,4800 J = K_B. Las dos maneras conviven
   en el mismo ejercicio: una para donde se puede y otra para donde no.

- [ ] **Paso 7: el cierre del ensayo**

`<div class="columna columna-final">` con `<h2>`: `Para tener a mano`, y una `<ol>` con
seis reglas operativas, en el tono de la de `cuerpo-aislado.html`:

1. El trabajo es la **componente de la fuerza en la dirección del movimiento**, integrada
   a lo largo del camino. *F*·*d* es un caso particular: fuerza constante y paralela.
2. Una fuerza perpendicular a la velocidad no hace trabajo **nunca**: la normal, la
   tensión de una cuerda que gira, la del cable que sostiene. Que toque no significa que
   transfiera.
3. La normal no es *mg* salvo que el piso sea horizontal y nada más empuje ni tire en
   vertical. Si la normal cambia, el rozamiento cambia con ella.
4. El peso y el resorte son conservativos: su trabajo depende sólo del punto inicial y del
   final. Por eso valen como energía potencial, y por eso el camino no importa.
5. El rozamiento no es conservativo: se cuenta aparte, siempre resta, y a veces no se puede
   integrar — ahí se lo despeja del balance entre dos estados donde sí se conoce todo.
6. La energía cinética va con *v*². Bajar la velocidad a la mitad cuesta las **tres
   cuartas partes** de la energía, no la mitad.

Y el pie, con el enlace «siguiente» todavía **sin poner** —la página del ensayo 8 no
existe hasta la Tarea 9; la Tarea 10 lo agrega—.

- [ ] **Paso 8: verificar la página entera**

1. Los cuatro widgets, con sus lecturas por defecto, contra el script. Los chequeos, en
   cero: `0,00 J` en el widget 1, `0,000 J` en el 2, `0,0000 m/s` en el 3, y en el 4
   `0,0000 m/s` antes de D y `0,0000 m/s²` en el tramo de freno.
2. v₀ y h en los dos extremos de cada deslizador: los dos chequeos siguen en cero (peor
   caso medido en todo el rango: 1,7 × 10⁻⁵ m/s y 3,1 × 10⁻⁵ m/s²), el perfil no se sale
   del encuadre por arriba (el `yMax: h + 0.4` acompaña) y el carro no atraviesa el suelo
   en ningún cuadro.
3. **Rompé el widget 4 a propósito, y es el paso que más importa de esta tarea.** En
   `marchaNewton`, cambiá `senTheta` de `m => m / Math.hypot(1, m)` a `m => m` —usar la
   tangente donde va el seno, que es el desliz clásico de este cálculo— y confirmá que
   `v marcha − v(y)` se va a **+2,3141 m/s** en el peor punto (x ≈ 1,69), llega a D con
   **+1,4687 m/s**, y que `a medida − a cerrada` salta a **+2,5434 m/s²**. Volvé atrás.
   Si el chequeo **no** se movió, está calculado por un solo camino y hay que arreglarlo
   antes de seguir: es el defecto exacto que esta corrección del plan vino a sacar.
4. Movéle el nodo A del perfil de `[0, h]` a `[0, 0.9 * h]` y confirmá que
   `v marcha − v(y)` se va a **2,4241 m/s** en el peor punto. Volvé atrás. (Éste es el
   único defecto que cazaba el chequeo viejo, y el nuevo lo sigue cazando.)
5. La casilla del cuadrante deshabilita los dos deslizadores, la barra cambia de total y
   las **dos** lecturas de chequeo pasan a `—`. El bloque se detiene **dentro** del marco,
   no contra el borde ni fuera: medido, píxel 775 a 880 y 308 a 350.
6. El recorrido completo de la página a 1280 y a 390 px, en los dos temas, con la consola
   abierta. Ningún widget se anima solo.
7. Servir `docs/` como raíz y comprobar que el pie enlaza a `fuerzas-de-posicion.html` y a
   `../index.html`, y la línea de fuentes a `../recursos/practico_3_2026.pdf`.

- [ ] **Paso 9: commit**

```bash
node --test "test/**/*.test.js"
git add docs/ensayos/energia.html
git commit -m "feat(ensayos): energia, solo la altura, y el cierre del ensayo"
```

---

## Fase C — Ensayo 8: Cantidad de movimiento

Es el ensayo más corto de la plataforma y el que tiene la idea más filosa: hay una
cantidad que **no puede cambiar** mientras nada de afuera empuje al sistema, y no le
importa nada de lo que le pase a la energía. Puede perderse la mitad de la energía
cinética, o puede aparecer un 44 % de la nada, y la cantidad de movimiento total sigue
siendo exactamente la misma. Cuatro ejercicios, tres widgets, y la misma pareja de
lecturas en los tres: **Δp clavado en cero, ΔK libre**.

---

### Tarea 7: La página y el widget 1 — el impulso no sabe a qué velocidad vas

**Archivos:**
- Crear: `docs/ensayos/cantidad-de-movimiento.html`

**Interfaces:**
- Consume: lo mismo que el ensayo 7, más `panelesApilados`, `cuerpo` y `colocarEtiqueta`
  (los dos `cuerpo` de los extremos del intervalo llevan su velocidad rotulada, y eso
  cuelga de un punto: va por `colocarEtiqueta`, no por `texto()`).
- Produce: la página con su encabezado, la sección 01 y el primer widget.

**El ejercicio (práctico 3, ej. 9).** Un cuerpo de 2 kg cae desde una torre de 100 m. Se
pide el impulso que recibe durante el primer segundo, durante el segundo segundo, y
durante todo el tiempo de caída libre. Del bloque `Ej 9`: **J(1er s) = 19,6 N·s**,
**J(2do s) = 19,6 N·s** (idéntico), **t_cl = 4,5175 s**, **J total = 88,544 N·s**, y el
control independiente **m·v_final = m√(2gh) = 88,544 N·s**.

- [ ] **Paso 1: el esqueleto de la página**

Igual que en la Tarea 3, copiando el esqueleto de `energia.html` —con sus clases de
`base.css` y con los `style` tipográficos del kicker, el `<h1>`, la `<ol>`, el pie y la
línea de fuentes **copiados idénticos**, ninguno nuevo— y cambiando:

- kicker `Ensayo 8 · Física 1`; `<title>` `Cantidad de movimiento · Física 1`;
  `<h1>` `Cantidad de movimiento`.
- bajada: `Lo que un choque no puede cambiar, pase lo que pase con la energía.`
- pie: a la izquierda `Ensayo 7 · Trabajo y energía` (`energia.html`), a la derecha
  `Portada`; línea de fuentes con
  `<a href="../recursos/practico_3_2026.pdf">práctico 3, ej. 9 a 12</a>`.

Dos párrafos de introducción. El primero: todo lo que este ensayo hace sale de la segunda
ley escrita de otra manera. *F* = *ma* es lo mismo que *F* = Δ*p*/Δ*t*, y despejando,
*F*·Δ*t* = Δ*p*. Eso tiene nombre —impulso— y es la herramienta que hace falta antes de
poder hablar de choques, porque en un choque no se conoce la fuerza ni el tiempo por
separado, pero el producto sí. El segundo: y de ahí sale la ley entera. Si dos cuerpos se
empujan entre sí, se empujan con fuerzas iguales y opuestas durante el mismo tiempo, así
que reciben impulsos iguales y opuestos: lo que uno gana de cantidad de movimiento, el
otro lo pierde, y el total no se mueve. **No hace falta saber nada de la fuerza** —cuánto
valió, cuánto duró, si fue elástica o no—, y por eso la conservación de *p* funciona
donde la energía no ayuda.

- [ ] **Paso 2: la sección 01 y su franja**

`<h2>`: `01 · El impulso no sabe a qué velocidad vas`.

Párrafo previo: la intuición dice que en el segundo segundo de caída «pasa más», porque el
cuerpo va más rápido. Y algo sí pasa más: recorre más metros y gana más energía cinética
—eso va con *v*²—. Pero el impulso no: el impulso es la fuerza por el tiempo, y la fuerza
es siempre la misma (el peso) y el tiempo es siempre un segundo. El widget deja elegir
cualquier intervalo de la caída, no sólo los dos del enunciado, y lo que tiene que quedar
claro es que el ancho del intervalo es lo único que manda.

La franja:

- `.encabezado-widget`: `Simulación 1` · `El impulso de una fuerza constante` ·
  `— dos franjas del mismo ancho valen lo mismo, esté el cuerpo lento o rápido.`
- `<canvas id="m1-cv">`
- controles: deslizador `m1-t1` (`min="0" max="3.5" step="0.05" value="0"`, s), deslizador
  `m1-dt` (`min="0.1" max="1.5" step="0.05" value="1"`, s), y dos botones,
  `Primer segundo` (`m1-b1`) y `Segundo segundo` (`m1-b2`), que ponen los deslizadores en
  (0; 1) y (1; 1).

Los dos botones mueven **dos** deslizadores de una, y eso no se hace asignando `.value`:
`deslizador()` repinta su `<output>` sólo dentro de su listener de `'input'`. Hay que
asignar y despachar, exactamente como `movimiento-circular.html:513` —que resuelve este
mismo problema con los presets del ejercicio 13—:

```js
const fijarDeslizador = (entrada, valor) => {
  entrada.value = String(valor);
  entrada.dispatchEvent(new Event('input'));
};
// Primer segundo:
fijarDeslizador(el('m1-t1'), 0); fijarDeslizador(el('m1-dt'), 1);
```

Sin el `dispatchEvent`, el botón mueve la perilla y deja la salida marcando el valor
viejo: el widget dibujaría una cosa y el control diría otra.
- `.lecturas`: `J = mg·Δt` (`m1-j`, rojo), `Δp = m·Δv` (`m1-dp`, azul),
  `J − Δp` (`m1-chequeo`, `--dim`), `v al empezar` (`m1-v1`) y `v al terminar` (`m1-v2`).

`t1 + Δt` se recorta a `t_cl = 4,5175 s`: el cuerpo toca el piso ahí, y un intervalo que
lo pase estaría midiendo el impulso de una caída que no ocurrió. El tope del deslizador de
`t1` en 3,5 y el de `Δt` en 1,5 dejan la suma en 5,0, así que el recorte actúa de verdad
en la esquina del rango — y hay que probarla.

- [ ] **Paso 3: la física, y una advertencia sobre la fuerza de este canario**

```js
/* ---------- widget 1: el impulso de una fuerza constante ---------- */

// Practico 3, ej. 9. Cuerpo de 2 kg que cae desde 100 m. Verificado en el bloque "Ej 9":
//   J(primer segundo) = J(segundo segundo) = 19.6 N s
//   t_cl = 4.5175 s   J total = 88.544 N s = m sqrt(2 g h) = 88.544 N s
// `G` es de la PAGINA (la declara el preambulo del modulo, arriba de todo, fuera del
// bloque de cualquier widget); aca solo van las constantes de ESTE ejercicio.
const M1 = 2, H1 = 100;
const T_CL = Math.sqrt(2 * H1 / G);          // 4.5175 s
const V = t => G * t;                        // la curva que el panel de arriba DIBUJA
const F = () => M1 * G;                      // la recta que el panel de abajo dibuja

// Camino A: el area bajo la recta de F(t) en el intervalo, sumada sobre las MISMAS
// muestras que se dibujan.
function areaF(t1, t2, n = 200) {
  const h = (t2 - t1) / n;
  let s = 0;
  for (let i = 0; i < n; i++) s += (F(t1 + i * h) + F(t1 + (i + 1) * h)) / 2 * h;
  return s;
}
// Camino B: la variacion de cantidad de movimiento leida de los EXTREMOS de la curva
// v(t) que el panel de arriba dibuja.
const deltaP = (t1, t2) => M1 * (V(t2) - V(t1));
```

**Hay que ser honesto sobre qué prueba este chequeo y qué no.** A diferencia de los
widgets del ensayo 7, acá los dos caminos pasan los dos por la misma `g`: si alguien
escribiera `G = 9.81`, las dos cuentas se moverían juntas y la resta seguiría dando cero.
Lo que este chequeo sí caza —y es el error real de este ejercicio— es que la curva v(t)
dibujada **no sea** la que corresponde a la fuerza dibujada: si alguien pone
`V = t => 0.5 * G * t * t` (confundir velocidad con posición, que pasa), `Δp` se rompe y
el área no, y la resta lo canta. Fuera de eso, la lectura que carga el concepto de esta
sección **no es la resta**: es que `J` dé **19,6 N·s en los dos segundos**, con `v al
empezar` pasando de 0,00 a 9,80 m/s. Esa es la que hay que mirar, y el párrafo de cierre
la nombra.

- [ ] **Paso 4: el dibujo, en dos paneles**

Dos franjas con `panelesApilados`: arriba `v(t)` en azul, abajo `F(t)` en rojo con la
franja del intervalo rayada, las dos compartiendo el eje de tiempos, que es lo que hace
que el ancho del intervalo se lea igual arriba y abajo.

```js
// Sufijo `_M1` por la Global Constraint del espacio de nombres: `cantidad-de-movimiento.html`
// es UN modulo, y las Tareas 8 y 9 declaran sus propios margenes mas abajo. Sin el sufijo
// los tres `const MARGEN` de esta pagina son un SyntaxError y la pagina no carga.
const MARGEN_M1 = { L: 56, R: 24, T: 18, B: 34 };
const HUECO_ROTULO_M1 = COLGADO_ROTULO_EJE + 8;       // 23 px
const ALTO_PANEL_MINIMO_M1 = 95 + HUECO_ROTULO_M1;    // 118 px

const widget = crearWidget({
  pagina, canvas: el('m1-cv'),
  margen: MARGEN_M1, escalaUniforme: false,
  altoMin: 2 * ALTO_PANEL_MINIMO_M1 + MARGEN_M1.T + MARGEN_M1.B,
  encuadre: () => ({ xMin: 0, xMax: 4.6, yMin: 0, yMax: 2 }),
  dibujar: pintar,
});
```

Paneles: `[{ yMin: 0, yMax: 48 }, { yMin: 0, yMax: 24 }]` — 48 m/s deja aire sobre los
44,27 m/s finales, y 24 N sobre los 19,6 N del peso.

Medido con el `crearWidget` real: a 880 px el canvas sale de **430 px**, los dos paneles
miden 189 px, la escala horizontal es **173,91 px/s** en los dos, el panel de velocidad da
3,250 px por (m/s) y el de fuerza 6,500 px por newton, así que la recta del peso queda a
**127,4 px** de altura. A 350 px: canvas de 288 px, paneles de 118 px, 58,70 px/s, y la
recta del peso a 69,4 px.

**La medición que es el widget entero:** la franja [1 s, 2 s] mide **173,9 px de ancho a
880 px** y la franja [3,5 s, 4,5 s] mide **exactamente los mismos 173,9 px**. Dos
rectángulos idénticos, uno donde el cuerpo va despacio y otro donde va rápido. A 350 px
las dos miden 58,7 px. Eso no es una casualidad del dibujo: es que el área bajo una fuerza
constante sólo depende del ancho.

La franja se raya con `punteado` vertical cada 6 px entre el eje y la recta, igual que en
el widget 1 del ensayo 7; en el panel de arriba, el intervalo se marca con dos verticales
punteadas en `--dim` y dos `cuerpo` sobre la curva en los extremos, con sus velocidades
rotuladas **por `colocarEtiqueta`** —cuelgan de un punto que se mueve con el deslizador, y
pueden juntarse cuando Δt baja a 0,1 s: es justo el caso para el que `etiqueta.js` existe—.
Ojo con el segundo límite del módulo: este widget es de `panelesApilados`, así que un
rótulo pegado al piso del panel de arriba puede terminar empujado al de abajo. Colgarlos
**hacia arriba** (`dy` negativo) mantiene el esquive lejos de esa frontera. Sin animación: este widget no tiene reproducción, lo que se mueve es el
intervalo.

- [ ] **Paso 5: los párrafos de cierre**

1. Apretá `Primer segundo` y después `Segundo segundo`, y mirá las dos franjas: el mismo
   ancho, la misma área, **19,6 N·s las dos**. Y mirá las velocidades: en la primera el
   cuerpo va de 0,00 a 9,80 m/s; en la segunda, de 9,80 a 19,60 m/s. Va al doble de
   velocidad y recibe exactamente el mismo impulso, porque el impulso no mira la
   velocidad: mira la fuerza y el reloj.
2. Estirá `Δt` hasta el final: el impulso total de la caída es **88,544 N·s**, y ese
   número se puede sacar de dos maneras que no se parecen en nada —mg·t_cl, o
   m·√(2gh)— y dan lo mismo hasta el cuarto decimal. Eso es el teorema impulso-cantidad
   de movimiento: no es una fórmula nueva, es la segunda ley integrada en el tiempo.
3. Y la advertencia que hace falta antes de la sección siguiente: nada de esto dice una
   palabra sobre la energía. La energía cinética en el segundo segundo crece mucho más
   que en el primero (va con *v*²), y al impulso no le importa. Son dos contabilidades
   distintas sobre el mismo movimiento.

- [ ] **Paso 6: verificar**

1. `Primer segundo`: `19,6 N·s`, `19,6 N·s`, `0,0 N·s`, `0,00 m/s`, `9,80 m/s`.
   `Segundo segundo`: `19,6`, `19,6`, `0,0`, `9,80`, `19,60`. Contra el bloque `Ej 9`.
2. `t1 = 0`, `Δt` al máximo: el intervalo se recorta en `t_cl = 4,5175 s` y `J` da
   `88,5 N·s`. `v al terminar` da `44,27 m/s`.
3. La esquina del rango: `t1 = 3,5` y `Δt = 1,5` — la suma da 5,0, hay que ver el recorte
   actuando y `J` dando `mg·(4,5175 − 3,5) = 19,94 N·s`, no `29,4`.
4. **Medí las dos franjas**: 173,9 px a 880 px las dos.
5. 1280 y 390 px, los dos temas, consola limpia.

- [ ] **Paso 7: commit**

```bash
node --test "test/**/*.test.js"
git add docs/ensayos/cantidad-de-movimiento.html
git commit -m "feat(ensayos): cantidad de movimiento, el impulso de una fuerza constante"
```

---

### Tarea 8: Widget 2 — lo que un choque no puede cambiar

**Archivos:**
- Modificar: `docs/ensayos/cantidad-de-movimiento.html`

**Interfaces:**
- Consume: lo anterior, más `bloque`, `acotarFlecha`, `marcaDeTope`, `punteado`,
  `cuerpo` y `colocarEtiqueta`. **No consume `presupuestoPx`**: los tres paneles de este
  widget son escenas de flechas, no barras — la que sí la usa es la Tarea 9.
- Produce: la sección 02 con el widget 2.

**Los ejercicios.** Ej 10: dos bolas de igual masa chocan de frente; ¿qué velocidad tenía
que traer B para que A quede quieta, siendo el choque perfectamente elástico? Respuesta:
para masas iguales el choque elástico es un **intercambio** de velocidades, así que
v'_A = 0 exige u = 0 — **B estaba en reposo**, y la premisa «chocan de frente» era
incompatible con lo que se pedía. Ej 12: un cuerpo en el espacio se parte en dos mitades y
una sale con v/3; la otra sale con **5v/3**, en el mismo sentido, y la energía cinética
**aumenta** un 44 % (K_f/K_i = 13/9).

Del bloque `Ej 10 y 12 (numerico)`: con m = 1 kg y v = 3 m/s, p = 3 kg·m/s y K = 4,5 J
antes y después; con m = 2 kg y v = 3 m/s, las dos mitades de 1 kg salen a 1 y a 5 m/s,
p = 6 kg·m/s antes y después, y K pasa de 9,0 a 13,0 J.

- [ ] **Paso 1: la sección 02 y su franja**

`<h2>`: `02 · Lo que un choque no puede cambiar`.

Párrafo previo: en un choque pasan cosas espantosas —se deforma, se calienta, hace ruido—
y ninguna de ellas se puede calcular. Lo bueno es que no hace falta. Mientras las únicas
fuerzas en juego sean las que los cuerpos se hacen entre sí, la cantidad de movimiento
total del par es la misma antes y después, y punto. La energía cinética, en cambio, es
libre: puede quedarse igual, puede caer, y —esto es lo que casi nadie espera— puede
**subir**.

La franja:

- `.encabezado-widget`: `Simulación 2` · `Antes y después` ·
  `— la aguja de arriba nunca se mueve; la de abajo hace lo que quiera.`
- `<canvas id="m2-cv">`
- controles: deslizadores `m2-m1`, `m2-m2` (`min="0.5" max="3" step="0.1" value="1"`, kg),
  `m2-u1` (`min="-3" max="3" step="0.1" value="3"`, m/s), `m2-u2`
  (`min="-3" max="3" step="0.1" value="0"`, m/s), `m2-e`
  (`min="0" max="1" step="0.1" value="1"`, coeficiente de restitución), y casilla
  `m2-explosion` con la etiqueta `Explosión (ej. 12)`.
- `.lecturas`: `p antes` (`m2-pa`), `p después` (`m2-pd`),
  `p antes − p después` (`m2-chequeo-p`, `--dim`), `ΔK` (`m2-dk`, rojo o azul según el
  signo) y `ΔK por fórmula − ΔK` (`m2-chequeo-k`, `--dim`).

El deslizador de restitución es una decisión de este plan, en vez del selector de tres
modos que propone la investigación: **e = 1 es el choque elástico, e = 0 el perfectamente
inelástico, y todo lo del medio es real** (una pelota que rebota a media altura). No
agrega ningún control fuera del vocabulario que la plataforma ya usa —no hay `select` en
`controles.js`— y de paso deja la explosión como lo que es, un modo aparte, en su casilla.
Los tres valores que el bloque `Choque general` verifica (e = 1, 0,5 y 0) son tres
posiciones de ese mismo deslizador.

- [ ] **Paso 2: la física, y el canario de energía corregido**

```js
/* ---------- widget 2: antes y despues ---------- */

// Practico 3, ej. 10 y 12. Verificado en "Ej 10 y 12 (numerico)" y "Choque general":
//   defecto (m1=m2=1, u1=3, u2=0, e=1) -> v1'=0, v2'=3 : el intercambio del ej. 10
//   explosion (m=2, v=3)               -> mitades de 1 kg a 1 y a 5 m/s, K de 9 a 13 J
//   blindaje (m1=2, m2=1, u1=3, u2=-1) -> e=1: 0.3333 y 4.3333 ; e=0.5: 1 y 3 ;
//                                         e=0: 1.6667 y 1.6667, con dK de 0, -4 y -5.3333

// Las dos ecuaciones: conservacion de p, y la definicion del coeficiente de restitucion
// (la velocidad de separacion es e veces la de aproximacion). Con e=1 esto es
// EQUIVALENTE a conservar la energia cinetica, pero no hace falta escribirla: sale sola.
function choque(m1, m2, u1, u2, e) {
  const p = m1 * u1 + m2 * u2;
  const v1 = (p - m2 * e * (u1 - u2)) / (m1 + m2);
  const v2 = (p + m1 * e * (u1 - u2)) / (m1 + m2);
  return { v1, v2 };
}

// El otro camino para dK, que NO pasa por las velocidades finales: la formula de la masa
// reducida. Ojo con el factor (1 - e^2): la investigacion la propone sin el, y asi solo
// vale para e = 0. Con el factor vale para los tres casos -- verificado en el bloque
// "Choque general": da +0.0000, -4.0000 y -5.3333 para e = 1, 0.5 y 0, exactamente lo
// mismo que restar las energias cineticas.
const deltaKFormula = (m1, m2, u1, u2, e) =>
  -0.5 * (m1 * m2 / (m1 + m2)) * (1 - e * e) * (u1 - u2) ** 2;
```

Comprobación cerrada antes de dibujar: `choque(1, 1, 3, 0, 1)` tiene que dar
`{ v1: 0, v2: 3 }`; `choque(2, 1, 3, -1, 0.5)` tiene que dar `{ v1: 1, v2: 3 }`;
`choque(2, 1, 3, -1, 0)` tiene que dar las dos velocidades iguales a `1.6667`.

En **modo explosión** el coeficiente de restitución no significa nada y la fórmula de masa
reducida no aplica: la energía que aparece la puso la explosión, no la geometría del
choque. Ahí la lectura `ΔK por fórmula − ΔK` muestra `—`, no un número. Fingir un chequeo
donde no hay dos caminos es peor que no tenerlo.

El modo explosión usa **m = 2 kg y v = 3 m/s** (del script) y no tiene deslizadores de
masa independientes: las dos partes son mitades iguales por enunciado, y una sale con v/3.

**Y por lo tanto se deshabilitan CINCO deslizadores, no uno.** La regla la fija el Paso 5
de la Tarea 6 —un control que la escena ignora se deshabilita, no se deja moviéndose sin
efecto— y en modo explosión la escena ignora `m2-e`, `m2-m1`, `m2-m2`, `m2-u1` **y**
`m2-u2`: los cinco quedan fuera del cálculo, porque las masas son mitades por enunciado y
la velocidad inicial es la del cuerpo entero. Deshabilitar sólo `m2-e` sería peor que no
deshabilitar nada: sugeriría que los otros cuatro sí hacen algo.

- [ ] **Paso 3: el dibujo, en tres paneles**

```js
// Sufijo `_M2`: ver la Global Constraint del espacio de nombres. El piso de panel es el
// mismo numero del widget 1 y se REUSA -- no se redeclara, que seria el SyntaxError.
const MARGEN_M2 = { L: 30, R: 24, T: 18, B: 26 };
const widget = crearWidget({
  pagina, canvas: el('m2-cv'),
  margen: MARGEN_M2, escalaUniforme: false,
  altoMin: 3 * ALTO_PANEL_MINIMO_M1 + MARGEN_M2.T + MARGEN_M2.B,
  encuadre: () => ({ xMin: -6, xMax: 6, yMin: 0, yMax: 3 }),
  dibujar: pintar,
});

// `hueco: 0`, y no `HUECO_ROTULO_M1`: esos 23 px son el aire que el rotulo del eje Y de
// `eje()` necesita para colgar por encima de su techo, y NINGUNO de estos tres paneles
// dibuja un `eje()` -- son escenas de flechas. Reservarlo aca seria regalar 69 px de
// alto util a nada. (El `altoMin` de arriba sigue calculado con el piso de 118 px a
// proposito: es el que hace que a 350 px el canvas salga de 398 px, medido, y bajarlo
// apretaria los tres paneles sin necesidad.)
const franjas = panelesApilados({
  lienzo: l, margen: { L: MARGEN_M2.L, R: MARGEN_M2.R }, hueco: 0,
  paneles: [{ yMin: -1, yMax: 1 }, { yMin: -1, yMax: 1 }, { yMin: -1, yMax: 1 }],
});
```

Paneles: `[{ yMin: -1, yMax: 1 }, { yMin: -1, yMax: 1 }, { yMin: -1, yMax: 1 }]` —
**los tres con el mismo rango vertical y el mismo rango horizontal**, que es toda la
disciplina que hace falta para que una flecha del mismo largo signifique lo mismo en
«antes» y en «después». No hay que tocar el motor para conseguirlo: `panelesApilados` ya
hereda el rango horizontal del lienzo exterior, y el vertical lo elige quien llama.

Medido: a 880 px el canvas sale de **430 px** con **68,83 px por unidad de marco**; a 350
px, de **398 px** con **24,67 px/u**. (A 350 px el canvas queda alto y angosto; es el
precio de tres paneles y es el mismo precio que paga el widget de tres gráficos de
`derivada-integral.html`.)

- **Panel 1 — ANTES:** los dos cuerpos como `bloque`, con ancho proporcional a la raíz de
  la masa, y su flecha de velocidad en azul. Escala: **1 m del marco por cada m/s**, o sea
  68,83 px por (m/s) a 880 y 24,67 a 350. Medido: v = 1 m/s da 69 px, v = 3 m/s da 207 px.
- **Panel 2 — DESPUÉS:** lo mismo, con las velocidades finales. El caso extremo del rango
  de deslizadores (m₁ = 3, m₂ = 0,5, u₁ = 3, u₂ = −3, e = 1) da v₂' = **7,2857 m/s**, o sea
  501 px a 880 — más que el panel—, así que la flecha pasa por `acotarFlecha` con tope de
  5,0 m del marco (**344 px a 880, 123 px a 350**) y lleva `marcaDeTope`. Medido. Sin ese
  tope la flecha se sale del canvas en silencio.
- **Panel 3 — CANTIDAD DE MOVIMIENTO: las DOS cadenas, antes y después.** Este plan
  decía «las cantidades de movimiento individuales, encadenadas punta a cola» sin decir
  **de qué instante**, y la diferencia es todo: con una sola cadena lo que se dibuja es
  una **suma**, no una conservación. Van las dos, desde el mismo origen, en dos filas del
  mismo panel:

  - fila `y = +0.45`, en `--blue-soft`: p_A y p_B **antes**, encadenadas.
  - fila `y = -0.45`, en `--blue`: p_A' y p_B' **después**, encadenadas.
  - una vertical `punteado` en `--dim` en la punta de `p_total`, calculada por su cuenta
    (`m1*u1 + m2*u2`), cruzando las dos filas y rotulada `p total`.

  **Que las dos cadenas terminen en la misma vertical es la conservación, dibujada.** Una
  sola cadena no puede decir eso. Medido a 880 px: las dos filas quedan separadas 53,4 px
  (el panel da 59,3 px por unidad de marco vertical) y 48,6 px a 350 px — aire de sobra
  para dos flechas de 2 px con su rótulo.

  Escala: **0,9 m del marco por cada kg·m/s**, con tope en 5,5 m del marco. Elegida para
  que los dos casos del enunciado entren sin acotar: a 880 px, p = 3 (el ejercicio 10) da
  **186 px** y p = 6 (la explosión del ejercicio 12) da **372 px**; el tope recién actúa
  por encima de 6,11 kg·m/s. A 350 px: 67 px, 133 px y tope de 136 px.

  **El tope se aplica a la PUNTA ACUMULADA, no a cada flecha por separado.** Este plan
  decía «cada flecha acotada a 5,5 m del marco» y concluía que el extremo del deslizador
  «queda acotado». No queda: las flechas están **encadenadas**, así que dos flechas
  acotadas dan una cadena de 11,00 m del marco. Medido, con `m1 = m2 = 3` y
  `u1 = u2 = 3` (p_A = p_B = 9 kg·m/s, una esquina que los deslizadores alcanzan):

  | | cada flecha acotada | punta acumulada acotada |
  |---|---|---|
  | largo de la cadena a 880 px | 11,00 u = **757 px** | 5,50 u = **379 px** |
  | dónde termina | píxel **1200** | píxel **822** |
  | borde útil del marco | píxel 856 | píxel 856 |
  | a 350 px, dónde termina | píxel **449** (el canvas mide 350) | píxel **314** |

  O sea que con el tope por flecha la cadena se va del canvas, en silencio, en los dos
  viewports. El arreglo es llevar un cursor y acotar **contra el origen**:

  ```js
  // Encadenar es aritmetica del que llama -- sin primitiva nueva, igual que el vector
  // resultante de sistemas-acoplados.html. Lo que NO es del que llama es olvidarse de
  // que el tope tiene que mirar la punta acumulada: acotar flecha por flecha deja una
  // cadena de 2 x 5.5 = 11 u de largo en un panel donde entran 6.
  const TOPE_U = 5.5, ESC_U = 0.9;
  const acotar = v => Math.max(-TOPE_U, Math.min(TOPE_U, v));
  let cursor = 0;
  for (const { p, letra } of tramos) {
    const fin = acotar(cursor + p * ESC_U);
    vectorPx(ctx, lp.px(cursor), yFila, lp.px(fin), yFila,
      { color, grosor: 2, rotulo: letra, rdy: -8 });
    cursor = fin;
  }
  if (Math.abs(cursor) >= TOPE_U - 1e-9) marcaDeTope(ctx, lp.px(cursor), yFila, 1, 0, { color });
  ```

  **El mismo criterio para `p_total`**: se acota con la misma función y al mismo tope, así
  que en la esquina las tres puntas —cadena de antes, cadena de después y total— caen en el
  mismo píxel con su marca, que sigue siendo la lectura correcta.

  **Qué letra lleva cada flecha**, decidido acá para que no se improvise al escribir:
  fila de arriba `p₁` y `p₂`; fila de abajo `p₁′` y `p₂′`; la vertical, `p total`. Los
  cinco rótulos van por la opción `rotulo:` de `vectorPx` y por `colocarEtiqueta` en el
  caso de la vertical — **ningún `texto()` directo**. Y la advertencia del segundo límite
  de `etiqueta.js` pega justo acá: son tres paneles apilados y estos rótulos viven contra
  la frontera entre el panel 2 y el 3, así que si alguno aparece en el panel de arriba, es
  eso. Colgarlos con `rdy: -8` (hacia arriba, dentro del propio panel) y verificarlo a
  390 px, que es donde el panel es más bajo.

Cuidado con el cero: `vectorPx` descarta en silencio cualquier flecha de menos de 1 px, así
que un cuerpo detenido (B en el caso por defecto, o los dos en e = 0 con p = 0) no dibuja
nada y eso se lee como «no hay dato» en vez de «vale cero». Donde la magnitud sea menor
que 1 px, **dibujar un punto** con `cuerpo` de radio 3 y rotularlo `0`.

- [ ] **Paso 4: las lecturas**

```js
const pAntes = m1 * u1 + m2 * u2;
const pDespues = m1 * v1 + m2 * v2;          // de las velocidades finales, no de pAntes
const dK = (0.5 * m1 * v1 * v1 + 0.5 * m2 * v2 * v2) - (0.5 * m1 * u1 * u1 + 0.5 * m2 * u2 * u2);
```

`pDespues` **no** se copia de `pAntes`: se suma otra vez, de las velocidades que salieron
de `choque()`. Es la misma clase de lectura que las dos tensiones de
`sistemas-acoplados.html`, y por el mismo motivo: si `choque()` estuviera mal, la resta
dejaría de dar cero.

- [ ] **Paso 5: los párrafos de cierre**

1. La posición por defecto **es** el ejercicio 10: masas iguales, A viene a 3 m/s, B está
   quieta, y después del choque A queda clavada y B sale a 3 m/s. El choque elástico entre
   masas iguales es un intercambio de velocidades, siempre. Y ahí está la respuesta a la
   pregunta del enunciado: para que A quede quieta, B tenía que estar quieta — o sea que
   la premisa «chocan de frente» no se podía cumplir. Si B viniera de frente con velocidad
   no nula, A saldría con esa velocidad y no podría quedarse quieta.
2. Bajá el deslizador de restitución de 1 a 0 y mirá las dos lecturas de abajo. `p antes −
   p después` no se mueve de cero ni una sola vez, en ninguna posición del deslizador. `ΔK`
   baja hasta −5,33 J en el caso de blindaje. Ésa es la asimetría entera del tema: la
   cantidad de movimiento es una promesa, la energía cinética es una consecuencia.
3. Marcá la casilla de explosión. Un cuerpo de 2 kg a 3 m/s se parte en dos mitades, una
   sale a 1 m/s y la otra a 5 m/s. La cantidad de movimiento total sigue siendo 6 kg·m/s,
   exactamente. Y la energía cinética pasó de 9,0 a 13,0 J: **subió un 44 %**. No es un
   error de cuenta ni una violación de nada: esa energía estaba guardada en la química del
   explosivo y las fuerzas internas la soltaron. La conservación de *p* nunca prometió
   nada sobre la energía — sólo dice que **nada de afuera** empujó.

- [ ] **Paso 6: verificar**

1. Por defecto: `p antes` = `3,00`, `p después` = `3,00`, chequeo `0,00`, `ΔK` = `0,00 J`,
   chequeo de K `0,00 J`, y las velocidades finales 0 y 3 m/s.
2. `m1 = 2`, `m2 = 1`, `u1 = 3`, `u2 = -1` en los tres valores de restitución del script:
   e = 1 → `0,3333` y `4,3333`, ΔK `0,00`; e = 0,5 → `1,00` y `3,00`, ΔK `−4,00`;
   e = 0 → `1,6667` las dos, ΔK `−5,3333`. Contra el bloque `Choque general`.
3. La esquina del rango (`m1=3, m2=0.5, u1=3, u2=-3, e=1`): v₂' = 7,2857 m/s, la flecha
   **acotada a 344 px con su marca de tope**, y el chequeo de *p* sigue en cero.
4. **La otra esquina, la del panel 3** (`m1=m2=3, u1=u2=3`): la cadena tiene que terminar
   en el **píxel 822** a 880 px y en el **314** a 350 px, con su marca de tope, y
   **dentro** del canvas. Si termina cerca del 1200 (o simplemente no se ve), el tope se
   está aplicando por flecha y no a la punta acumulada.
5. Explosión: `p` = `6,00` de los dos lados, `ΔK` = `+4,00 J`, la lectura de chequeo de K
   en `—` y los **cinco** deslizadores (`m2-e`, `m2-m1`, `m2-m2`, `m2-u1`, `m2-u2`)
   deshabilitados.
6. Un caso con `p` total cero (`m1=m2=1, u1=1, u2=-1`): los puntos de magnitud cero se
   dibujan y se rotulan, no desaparecen.
7. Los cinco rótulos del panel 3 (`p₁`, `p₂`, `p₁′`, `p₂′`, `p total`) están **en su
   panel**, no en el de arriba. Es el caso que el segundo límite de `etiqueta.js`
   predice; verificalo a 390 px, que es donde el panel es más bajo.
8. 1280 y 390 px, los dos temas, consola limpia.

- [ ] **Paso 7: commit**

```bash
node --test "test/**/*.test.js"
git add docs/ensayos/cantidad-de-movimiento.html
git commit -m "feat(ensayos): cantidad de movimiento, antes y despues"
```

---

### Tarea 9: Widget 3 — la cantidad de movimiento cambia de dueño, y el cierre

**Archivos:**
- Modificar: `docs/ensayos/cantidad-de-movimiento.html`

**Interfaces:**
- Consume: todo lo anterior, más `presupuestoPx` (las dos barras) y `colocarEtiqueta`
  (los rótulos de velocidad que cuelgan de cada cuerpo — ver el Paso 3).
- Produce: la sección 03, la sección `Para tener a mano`, y el ensayo 8 terminado.

**El ejercicio (práctico 3, ej. 11).** Una bala de 10 g atraviesa un bloque de 1,2 kg y se
incrusta en otro de 1,8 kg; los bloques quedan a 0,63 y 1,4 m/s. Del bloque `Ej 11`: la
bala sale del bloque 1 a **253,40 m/s** y entró a **329,00 m/s**; el control cruzado es que
la bala perdió 75,60 m/s, o sea Δp = 0,7560 kg·m/s, que es exactamente lo que se llevó el
bloque 1 (m₁v₁ = 0,7560 kg·m/s).

- [ ] **Paso 1: la sección 03 y su franja**

`<h2>`: `03 · La cantidad de movimiento cambia de dueño`.

Párrafo previo: acá hay tres cuerpos y dos choques encadenados, y el ejercicio se resuelve
**de atrás para adelante**, lo cual es raro la primera vez. El último choque es el más
simple —la bala se queda adentro del bloque 2, así que los dos terminan con la misma
velocidad— y de ahí sale con qué velocidad venía la bala. Con ese número se resuelve el
choque anterior. Y en ningún momento se puede escribir una ecuación de energía: los dos
choques son inelásticos, la energía se fue en calor y en agujero, y nadie sabe cuánta.

La franja:

- `.encabezado-widget`: `Simulación 3` · `La bala y los dos bloques` ·
  `— la barra de arriba no cambia de largo; la de abajo se vacía en dos golpes.`
- `<canvas id="m3-cv">`
- controles: deslizador `m3-instante` (`min="0" max="2" step="1" value="0"`), con la
  salida escribiendo `antes de todo` / `la bala dejó el bloque 1` / `final`.
- `.lecturas`: `p de la bala` (`m3-pb`), `p del bloque 1` (`m3-p1`),
  `p del bloque 2` (`m3-p2`), `p total − p inicial` (`m3-chequeo`, `--dim`) y
  `K total` (`m3-k`, rojo).

- [ ] **Paso 2: la física y los tres instantes**

```js
/* ---------- widget 3: la bala y los dos bloques ---------- */

// Practico 3, ej. 11. Verificado en el bloque "Ej 11":
//   v_m (bala al dejar el bloque 1) = 253.40 m/s ; v_i (al entrar) = 329.00 m/s
//   control: Dp de la bala = 0.7560 kg m/s = m1 v1 = 0.7560 kg m/s
const MB = 0.01, MB1 = 1.2, MB2 = 1.8, V1 = 0.63, V2 = 1.4;
const VM = (MB + MB2) * V2 / MB;              // 253.40 m/s
const VI = (MB1 * V1 + MB * VM) / MB;         // 329.00 m/s

// Tres instantes, cada uno como la lista de cantidades de movimiento de los tres cuerpos.
// Cada numero sale de multiplicar una masa por una velocidad -- ninguno se copia de otro
// instante, que es lo que hace que la suma pueda no dar y delatarlo.
const INSTANTES = [
  { nombre: 'antes de todo',            p: [MB * VI, 0, 0],                   v: [VI, 0, 0] },
  { nombre: 'la bala dejó el bloque 1', p: [MB * VM, MB1 * V1, 0],            v: [VM, V1, 0] },
  { nombre: 'final',                    p: [0, MB1 * V1, (MB + MB2) * V2],    v: [0, V1, V2] },
];
```

Valores medidos de los tres instantes (kg·m/s): `[3,2900 · 0 · 0]`,
`[2,5340 · 0,7560 · 0]`, `[0 · 0,7560 · 2,5340]`. **La suma da 3,290000 en los tres**, con
la cantidad de movimiento individual de la bala cayendo a cero.

Y la energía cinética total, medida: **541,205 J → 321,296 J → 2,012 J**. Queda el
**0,37 %** de la que había.

- [ ] **Paso 3: por qué este widget NO dibuja flechas de velocidad**

Es la decisión de dibujo central de la tarea y conviene tenerla por escrito, porque el
instinto es dibujar la bala con una flecha larga.

Las cuatro velocidades del ejercicio son 329,0 · 253,4 · 0,63 · 1,4 m/s: una razón de
**522 a 1** entre la mayor y la menor. Medido: si la flecha más larga se dibuja a 300 px,
la del bloque 1 mide **0,574 px** — y `vectorPx` descarta en silencio todo lo que mida
menos de 1 px, así que el bloque 1 simplemente **no se dibujaría**, sin error visible. No
hay escala lineal que sirva.

En cantidad de movimiento, en cambio, los mismos cuatro cuerpos dan 3,2900 · 2,5340 ·
0,7560 · 2,5340 kg·m/s: una razón de **4,35 a 1**, todas dibujables en la misma barra. Ése
es, además, el mensaje del ejercicio: la bala es rapidísima y liviana, el bloque es lento y
pesado, y en cantidad de movimiento **pesan casi lo mismo**. El widget muestra la magnitud
que hace comparables a los tres cuerpos, no la que los vuelve incomparables.

Las velocidades van en el texto de las lecturas y en rótulos junto a cada cuerpo, con sus
números; no en flechas. **Esos rótulos cuelgan de un cuerpo, así que van por
`colocarEtiqueta`** —no por `texto()`—: son tres, y en el instante 1 la bala y el bloque 1
están al lado uno del otro, que es justo el caso de colisión para el que el módulo existe.
Los rótulos **de adentro** de las dos barras los pone `presupuestoPx` con `texto()`, y eso
está bien: son de posición fija dentro de una caja.

- [ ] **Paso 4: el dibujo**

Un solo lienzo, sin `panelesApilados`: arriba la escena (la bala y los dos bloques en el
instante elegido, con sus velocidades rotuladas) y abajo dos barras de `presupuestoPx`.

```js
// Sufijo `_M3`: ver la Global Constraint del espacio de nombres. Es el tercer `MARGEN`
// de esta pagina y sin sufijo ninguno de los tres carga.
const MARGEN_M3 = { L: 30, R: 24, T: 20, B: 96 };  // los 96 de abajo son las dos barras
const widget = crearWidget({
  pagina, canvas: el('m3-cv'),
  margen: MARGEN_M3, escalaUniforme: false, altoMin: 320,
  // La escena es esquematica -- no hay distancias en el enunciado -- asi que el encuadre
  // es la unidad, y todo se ubica en fracciones de ancho.
  encuadre: () => ({ xMin: 0, xMax: 1, yMin: 0, yMax: 1 }),
  dibujar: pintar,
});
```

Medido: a 880 px el canvas sale de **430 px** con 314 px de alto útil para la escena; a
350 px, de **320 px** con 204 px. Las dos barras van a `y = alto − 88` y `y = alto − 52`,
de `x = 28` a `x = ancho − 24` (**828 px a 880, 298 px a 350**).

- **Barra de arriba — cantidad de movimiento**, con `total = 3.29` (el valor inicial) y
  tres segmentos: bala (`--ink`), bloque 1 (azul), bloque 2 (`--blue-soft`).
  **Está llena en los tres instantes**, y al mover el deslizador lo único que cambia es
  dónde caen las divisiones. Anchos medidos sobre 828 px: instante 0 → 828/0/0;
  instante 1 → 638/190/0; instante 2 → 0/190/638.
- **Barra de abajo — energía cinética**, con `total = 541.205` (la inicial) y un solo
  segmento en rojo. Anchos medidos sobre los 828 px reales: **828 px → 491,6 px →
  3,1 px**. El último es una astilla, y **está bien que lo sea**: es el 0,37 %. Como 3,1 px
  es menos que `minEtiquetaPx`, la primitiva no le pone rótulo — por eso el número va
  también en `.lecturas`.

La barra de energía es el único lugar del plan donde un segmento queda por debajo del
umbral de rótulo en una posición que el lector va a mirar seguro. Está previsto, no es un
descuido.

- [ ] **Paso 5: los párrafos de cierre de la sección**

1. Mové el deslizador por los tres instantes y mirá la barra de arriba: no cambia de largo
   ni una vez. Lo que cambia es de quién es cada pedazo. La bala entra con los 3,29
   kg·m/s enteros, le pasa 0,756 al bloque 1 al atravesarlo, y le entrega los 2,534 que le
   quedaban al bloque 2 al quedarse adentro. **La cantidad de movimiento no se crea ni se
   destruye: cambia de dueño.**
2. Y mirá la barra de abajo en el mismo recorrido: de 541,2 J quedan 2,0 J. Se fue el
   **99,6 %** de la energía cinética — en calor, en deformar el plomo, en hacer los dos
   agujeros—. Si alguien hubiera intentado resolver este ejercicio escribiendo «la energía
   se conserva», habría planteado una ecuación falsa y el sistema no habría tenido
   solución física.
3. El control que cierra el ejercicio: la bala perdió 75,60 m/s al atravesar el bloque 1,
   lo que en cantidad de movimiento son 0,010 × 75,60 = **0,7560 kg·m/s**. Y el bloque 1
   quedó con 1,2 × 0,63 = **0,7560 kg·m/s**. Lo que uno perdió es exactamente lo que el
   otro ganó, hasta el cuarto decimal, sin que haga falta saber cuánta fuerza hizo la bala
   ni cuánto duró el paso.

- [ ] **Paso 6: el cierre del ensayo**

`<div class="columna columna-final">` con `<h2>`: `Para tener a mano`, y una `<ol>` de
cinco reglas:

1. Impulso = fuerza × tiempo = Δ*p*. Depende de cuánto empuja y de cuánto dura, **no** de
   a qué velocidad va el cuerpo.
2. La cantidad de movimiento de un sistema se conserva si no hay fuerzas **externas**. Las
   internas —por más violentas que sean— no cuentan, porque vienen de a pares opuestos.
3. Es una magnitud con **signo** sobre cada eje. Perder el signo es el error más caro de
   este tema; «de frente» significa signos opuestos.
4. La energía cinética es una cuenta **aparte**: baja en un choque inelástico, se mantiene
   en uno elástico, y **sube** en una explosión. Nada de eso afecta a la conservación de *p*.
5. Un choque perfectamente inelástico da **una** ecuación (la de *p*) y una incógnita
   menos, porque los cuerpos salen juntos. Uno elástico da **dos** (p y K), o
   equivalentemente la de *p* más la de restitución con e = 1.

Y el pie, con `Ensayo 7 · Trabajo y energía` a la izquierda y `Portada` a la derecha.

- [ ] **Paso 7: verificar**

1. Los tres instantes, contra el bloque `Ej 11`: `3,2900 / 0 / 0`, `2,5340 / 0,7560 / 0`,
   `0 / 0,7560 / 2,5340`, con el chequeo en `0,0000 kg·m/s` en los tres.
2. `K total`: `541,21 J`, `321,30 J`, `2,01 J`.
3. **Medí la barra de arriba** en los tres instantes: el borde exterior tiene que caer en
   el mismo píxel las tres veces.
4. La astilla roja del instante final tiene que estar dibujada (3,1 px sobre 828), no
   ausente. Si desapareció, `presupuestoPx` está redondeando a cero en algún lado.
5. 1280 y 390 px, los dos temas, consola limpia.

- [ ] **Paso 8: commit**

```bash
node --test "test/**/*.test.js"
git add docs/ensayos/cantidad-de-movimiento.html
git commit -m "feat(ensayos): cantidad de movimiento, la bala y los dos bloques"
```

---

## Fase D — cerrar

### Tarea 10: Portada, navegación, README y la auditoría de cobertura

**Archivos:**
- Modificar: `docs/index.html`, `docs/ensayos/energia.html`, `README.md`

**Interfaces:**
- Consume: las dos páginas nuevas.
- Produce: la cadena de navegación cerrada y la tabla de cobertura auditada.

- [ ] **Paso 1: la portada**

Hoy `docs/index.html` lista siete ensayos y el séptimo, `Energía`, es un `<span>` en
`--dim` sin enlace (líneas 57-60). Dos cambios:

1. Esa fila pasa a ser un `<a href="ensayos/energia.html">`, con el mismo texto y la misma
   estructura que las seis de arriba. El título que muestra es **`Trabajo y energía`**, no
   `Energía` a secas: es el nombre del ensayo y el del tema del práctico.
2. **Se agrega una fila que no existe**: `ENSAYO 8` · `Cantidad de movimiento`, con enlace
   a `ensayos/cantidad-de-movimiento.html`. Copiala de la del ensayo 6, cambiando sólo el
   número, el texto y el `href`.

Ninguna de las dos filas lleva atributo `style`: van con `.encabezado-widget`,
`.rotulo-mono` y `.titulo-fila`, que es lo que usan las seis de arriba. El único `style`
que hay hoy en esa zona es el `style="color:var(--dim)"` del `<span>` del ensayo 7
(`docs/index.html:58`), y **desaparece** al convertirse en enlace — no se conserva.

- [ ] **Paso 2: cerrar la cadena de los pies**

Los pies de los ensayos encadenan «anterior → Portada». Con las dos páginas nuevas la
cadena es: `fuerzas-de-posicion.html` ← `energia.html` ← `cantidad-de-movimiento.html`.

El único agregado pendiente es el enlace **hacia adelante** en el pie de `energia.html`,
que la Tarea 6 dejó sin poner porque la página del ensayo 8 no existía todavía. Revisá
cómo lo hacen los otros ensayos antes de inventar una forma nueva: si hoy ninguno enlaza
hacia adelante, **no lo agregues** — dejá la cadena como está en el resto del sitio y
anotalo, en vez de introducir un patrón que sólo tendría una página.

- [ ] **Paso 3: el README**

Sumar los dos ensayos nuevos a la tabla de ensayos (`README.md:87` y siguientes), en el
mismo formato que los seis que ya están, y actualizar cualquier conteo o afirmación que
haya quedado vieja.

`grep -n "ensayo" README.md` **no sirve**: es sensible a mayúsculas y no encuentra ni las
filas de la tabla (que dicen `Ensayo`) ni —lo que más importa— la línea 101, que hoy
afirma que la Guía 3 todavía no está:

> Todavía no está la Guía 3 completa —trabajo, energía y cantidad de movimiento— ni el
> diseño de la portada, que lo hace el dueño del repositorio directamente.

Esa frase queda **falsa** en cuanto este plan termine, y es la que más hay que tocar. El
grep que la encuentra:

```bash
grep -niE "ensayo|gu[ií]a 3|seis|siete|ocho|completa" README.md
```

Verificado al corregir este plan: devuelve las líneas 45, 84, 87 y **101**.

- [ ] **Paso 4: auditar la tabla de cobertura, fila por fila**

Éste es el paso que el plan anterior no tuvo, y por eso publicó una fila falsa.

Abrí este plan en la tabla «Qué cubre de la Guía 3», y para **cada una de las doce filas**:

1. Abrí la página que la fila nombra.
2. Buscá la sección que la fila nombra, por su título exacto.
3. Comprobá que el ejercicio está **efectivamente tratado ahí**, con sus números, y no
   sólo mencionado de pasada.
4. Si no está, o está en otro lado, **corregí la tabla de este plan**, no la memoria.

Las dos filas que más fácil se caen son las de prosa: el ejercicio 5 (que tiene que estar
bajo `Apoyar no es soltar`, con los 1200,5 J, los 600,25 J y los 49,9804 m) y el ejercicio
6 (bajo `Lo mismo, sin nada que gire`, con los 246,23 N, los 122,81 J y la advertencia de
que F·l = 246,2 J no es la respuesta). Si alguno de esos párrafos se recortó al redactar,
la fila es falsa.

- [ ] **Paso 5: el recorrido completo**

1. Servir `docs/` como raíz —**no** el repositorio entero— y recorrer: portada → los ocho
   ensayos → los dos ejemplos → volver. Ningún 404.
2. Los siete widgets nuevos, a 1280 y a 390 px, en los dos temas, con la consola abierta.
   Cero errores, cero advertencias.
3. Ningún widget se anima solo al cargar.
4. Los ocho chequeos en cero, o en `—` donde el plan dice que no hay chequeo. Son ocho y
   no siete porque el widget 4 lleva dos (uno por tramo, Tarea 6 Paso 4); los que muestran
   `—` a propósito son el de energía de la Tarea 8 en modo explosión y los dos del
   widget 4 en la escena del cuadrante.
5. `grep -rn "toFixed" docs/ensayos/energia.html docs/ensayos/cantidad-de-movimiento.html`
   tiene que no devolver nada.
6. Los `style` tipográficos: los que vienen del esqueleto se conservan, y **ninguno
   nuevo**. El patrón tiene que ser `grep -c 'style="[^"]*font'`, no `grep -c 'style="font'`:
   la mitad de ellos aparecen como `style="display:flex;...;font:500..."`, con el `font`
   en el medio, y el patrón viejo no los ve.

   ```bash
   grep -c 'style="[^"]*font' docs/ensayos/energia.html docs/ensayos/cantidad-de-movimiento.html
   grep -c 'style="[^"]*font' docs/ensayos/cuerpo-aislado.html   # la referencia: 9
   ```

   Los dos archivos nuevos tienen que dar **9** cada uno —los mismos nueve del esqueleto,
   ni uno más—. Si dan más, hay un `style` inventado y hay que cambiarlo por una clase de
   `base.css`. Si dan menos, se perdió algo del esqueleto al copiarlo.

   **Corregido durante la ejecución: el número correcto es 8, y 9 nunca fue un objetivo.**
   Dos cosas se midieron al cerrar el ensayo 7:

   - El noveno `style` del esqueleto es `style="font-weight:500;font-variant-numeric:tabular-nums"`
     sobre un `<b>` de las lecturas (`cuerpo-aislado.html:62`), y esa declaración es
     **palabra por palabra `.lectura-valor`** (`base.css:51`). O sea: el noveno del
     esqueleto es deuda del esqueleto, un inline que duplica una clase que ya existe. Una
     página nueva que use la clase ahí hace lo correcto y da **8**. (Migrar ese inline en
     `cuerpo-aislado.html` es trabajo de un plan de deuda, no de éste.)
   - Perseguir el 9 como objetivo hace daño: la Tarea 6 llegó a nueve **duplicando** el
     `style` inline de una casilla que ya tenía su clase `.rotulo-campo` a tres líneas de
     distancia en el mismo archivo. El conteo daba bien y la composición estaba mal.
     Corregido: la casilla usa la clase, el archivo da 8, y sus ocho son un subconjunto
     exacto de los del esqueleto.

   **La regla es la composición, no el número.** El grep sirve para *encontrar* un `style`
   inventado, no para certificar que no lo hay: lo que hay que comparar es el conjunto
   contra el del esqueleto —`diff <(grep -o 'style="[^"]*font[^"]*"' esqueleto | sort)
   <(... página nueva | sort)`—, y la única diferencia admisible es que a la página nueva le
   falte el inline de `tabular-nums` porque usa la clase. Y el conteo va subiendo mientras
   la página se escribe: no es un número que tenga que cerrar en cada tarea.
7. `node --test "test/**/*.test.js"`: **247 pruebas, 0 fallas** (240 de base + 7 de
   `presupuestoPx`: las seis que este plan dictaba más la del orden del borde, que sumó la
   revisión de la Tarea 2 al encontrar un mutante que sobrevivía a las seis).

- [ ] **Paso 6: commit**

Esta tarea cierra la cadena de pies de **los dos** ensayos nuevos, así que los dos van al
commit. Dejar afuera `cantidad-de-movimiento.html` —como decía este plan— habría publicado
la portada con un enlace a una página sin commitear.

```bash
git add docs/index.html docs/ensayos/energia.html docs/ensayos/cantidad-de-movimiento.html README.md docs/superpowers/plans/2026-09-12-plataforma-guia-3.md
git commit -m "feat(plataforma): enlazar los ensayos de la guia 3 y cerrar la navegacion"
```

```bash
git status --short    # tiene que quedar limpio: nada sin commitear en docs/
```
