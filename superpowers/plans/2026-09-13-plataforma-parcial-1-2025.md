# Plataforma de Física 1 — Los tres adicionales · Plan de implementación

> **Para trabajadores agénticos:** SUB-SKILL REQUERIDA: usar superpowers:subagent-driven-development (recomendada) o superpowers:executing-plans para implementar este plan tarea por tarea. Los pasos usan sintaxis de casilla (`- [ ]`) para seguimiento.

**Objetivo:** tres notas de ejemplo en `docs/ejemplos/`, una por guía, que resuelven de punta a punta los tres problemas del Parcial 1 del 25/09/2025 — que son, en las guías 1 y 2, los **ejercicios adicionales oficiales** de la cátedra.

**Arquitectura:** no hay motor nuevo ni tipo de página nuevo. Las dos notas de ejemplo que ya existen (`la-tierra.html`, `auto-y-camion.html`) son el molde: una página, un widget, una sección `Cómo se resuelve` y un pie. Lo que estas tres agregan es **un ejercicio completo del examen real**, con todos sus ítems, en vez de un concepto.

**Stack:** ES modules vanilla, canvas 2D, `node --test` de Node 22, GitHub Pages desde `/docs`.

**Spec:** `plataforma/brief.md`

**Autoridad de diseño:** `plataforma/diseno/Tiro parabolico.dc.html`

---

## De dónde salen los enunciados

**Del PDF oficial de la cátedra, no del sitio ni de las soluciones en LaTeX.** Es una instrucción explícita del dueño. Los tres enunciados se leyeron de:

| Nota | Fuente oficial | Ubicación |
|---|---|---|
| 1 | `parcial-1/practicos/practico_1_2026.pdf`, sección **«Ejercicio adicional»**, ej. **15** | idéntico al Problema 1 del parcial |
| 2 | `parcial-1/practicos/Practico 2_2026.pdf`, sección **«Ejercicios adicionales»**, ej. **19** | idéntico al Problema 3 del parcial |
| 3 | `examenes-viejos/parciales/Parcial 1 2025-09-25.pdf`, **Problema 2** | **no existe en ningún práctico** |

El PDF del parcial es un escaneo sin capa de texto: se leyó rasterizándolo. **Contiene el nombre, el DNI y la nota de un estudiante**, escritos a mano. Está fuera de `docs/`, así que Pages no lo publica, pero vive en el repositorio. Ninguna de las tres notas reproduce ese dato ni nombra a nadie.

**El práctico 3 no tiene sección de adicionales**, y por eso la nota 3 es la única de las tres cuyo enunciado no está en un práctico. Y el práctico 2 tiene **dos** adicionales, el 18 (cono que gira) y el 19: el 18 no fue al parcial y **no** entra en este plan.

## Qué relación tiene cada nota con lo que el sitio ya dice

Medido contra el sitio en `13cd3e0`, archivo por archivo. Esto no es color: define qué hace cada tarea al final.

**Nota 1 — el ensayo de tiro promete algo que no entrega.** El pie de `docs/ensayos/tiro-parabolico.html` dice cubrir `práctico 1, ej. 9, 10 y 15`. El ejercicio 15 es el de la pelota con viento, y **el ensayo no lo trata**: no aparece la aceleración horizontal, ni el arco, ni los 45 m, ni los 2,44 m del travesaño. Verificado con `grep`: ninguno de esos números está en el archivo. Es una **fila de cobertura falsa, publicada** — el mismo defecto que el plan de la Guía 2 cometió una vez y que la auditoría de la Tarea 10 del plan de la Guía 3 existe para evitar, sólo que esa auditoría revisó la tabla de la Guía 3 y nadie volvió sobre las anteriores. La Tarea 5 la corrige.

**Nota 2 — el ensayo de cuerpo aislado sí lo trata, en prosa.** `docs/ensayos/cuerpo-aislado.html` tiene un párrafo que arranca `Ej. 19 — un bloque sobre otro.` con los números correctos (40 N, 80 N, μ_d = 0,25, T = 10 N, F = 20 N, F = 50 N, y los 120 N del piso). La fila de cobertura es honesta. La nota **no la contradice: la anima.** Es el mismo precedente que ya existe en el sitio — `la-tierra.html` resuelve el ej. 12 del práctico 1 mientras `movimiento-circular.html` cubre «ej. 11 a 14», que lo incluye. El ensayo construye el concepto; la nota resuelve un ejercicio entero.

**Nota 3 — no está en ninguna parte.** Ni en un práctico, ni en el sitio.

## Decisiones tomadas antes de escribir el plan

**1. `g = 10 m/s²` en la nota 1, y sólo ahí.** El enunciado oficial del ejercicio 15 termina con «y que la aceleración de la gravedad es igual a 10 m/s²». Todo el resto del sitio usa 9,8. **Manda el enunciado**: la nota 1 usa 10 y lo dice en su pie, con una frase que explique que es del enunciado y no un descuido. Las notas 2 y 3 usan 9,8 como el resto del sitio, porque sus enunciados no fijan `g`.

**2. Las tres van en `docs/ejemplos/`**, junto a las dos que ya están. Decisión del dueño. Va a refactorizar la portada más adelante; hasta entonces, las cinco conviven en la misma sección.

**3. Los nombres siguen el molde de las dos que existen** —`la-tierra.html`, `auto-y-camion.html`: cortos y evocativos, no burocráticos. Son `el-gol-con-viento.html`, `el-bloque-sobre-el-bloque.html` y `la-bolita-y-el-resorte.html`. Que vienen de un parcial se dice en la página, no en la URL.

**4. La nota 3 elige valores concretos, porque el enunciado es simbólico.** El enunciado da `m`, `h`, `μ_d`, `L_BC`, `k`, `ℓ₀` como símbolos y una sola atadura: `h = 4·μ_d·L_BC`. Los valores elegidos y su justificación están en la Tarea 1.

## Global Constraints

Aplican a todas las tareas.

- **Cero dependencias de runtime** salvo KaTeX por CDN. Nada de `npm install`. **Cero build.**
- **Los tokens de color son exactamente estos**, y no se inventa ninguno:
  claro `--paper:#fbfaf7` `--band:#f2f0ea` `--ink:#16151a` `--dim:#6a6760`
  `--rule:#dcd8ce` `--blue:#1b4fd4` `--blue-soft:#8aa3e6` `--red:#c02a24`
  `--graph:#8e8a80`; oscuro `--paper:#131316` `--band:#191a1e` `--ink:#eceae4`
  `--dim:#948f86` `--rule:#2e2f35` `--blue:#7aa2ff` `--blue-soft:#3f5694`
  `--red:#ef5f52` `--graph:#6f6c66`. **Nunca se escriben literales hex en JS.**
- **Reparto semántico:** azul para cinemática, velocidad y cantidad de movimiento; rojo para
  aceleración y para cada fuerza que actúa; azul para la resultante; `--graph` para la
  trayectoria y para la **energía potencial** (gravitatoria o elástica); **rojo para lo
  disipado**. Aprobado por el dueño el 2026-09-12; ver `plataforma/decisiones.md`.
- **Separador decimal coma**, vía `num(x, decimales)` y `exp(x, decimales)` de
  `docs/motor/formato.js`. **Cero `toFixed`** en archivos nuevos.
- **Tipografía por clase de `base.css` donde hay clase. La regla es la composición, no el
  número.** Se copia el esqueleto de una nota existente y se comprueba comparando
  **conjuntos**, no contando:
  ```bash
  diff <(grep -o 'style="[^"]*font[^"]*"' docs/ejemplos/la-tierra.html | sort) \
       <(grep -o 'style="[^"]*font[^"]*"' docs/ejemplos/<nueva>.html | sort)
  ```
  Cualquier línea `>` es un `style` inventado. Perseguir un número produjo, en el plan
  anterior, un `style` duplicado teniendo la clase a tres líneas de distancia.
- **Las lecturas van con `.lectura-valor`** y sus modificadores `.roja`, `.azul`, `.tenue` y
  **`.grafico`**. Nunca un `style="color:var(--...)"` inline.
- **Una página es un módulo y un espacio de nombres.** Cada nota es **un solo**
  `<script type="module">`. Dos `const` con el mismo nombre son un `SyntaxError` que no deja
  cargar la página. Como cada nota tiene un widget, alcanza con sufijar `_W1`, pero **las
  constantes físicas propias del ejercicio también van sufijadas**.
- **Todo rótulo que cuelgue de un cuerpo, una flecha o un punto pasa por `colocarEtiqueta`**
  (`docs/motor/etiqueta.js`), de preferencia por la opción `rotulo:` de `vectorPx`.
  `texto()` directo queda para rótulos de posición fija dentro de una caja: los segmentos de
  `presupuestoPx` y las marcas internas de `eje()`, y nada más.
- **Límite conocido del motor:** `crearWidget` le pasa a `colocarEtiqueta` el `{ancho, alto}`
  del **canvas entero** como límites, también para un widget de `panelesApilados` que sólo
  dibuja en una franja. Un rótulo cerca de la frontera puede terminar empujado al panel
  vecino. Ya mordió tres veces. Se corrige alejando el rótulo del borde, **no tocando el
  motor**, y se verifica con un **barrido completo** del rango de los controles llamando al
  `colocarEtiqueta` real, no a una reimplementación. Trampa conocida al medir: aplicar la
  heurística de alto de línea del motor a un **punto** da falsos positivos; usar una caja de
  texto realista.
- **Un deslizador que reescribe el código no repinta su `<output>` ni avisa a nadie.**
  `deslizador()` actualiza la salida sólo dentro de su listener de `'input'`, y asignar
  `.value` desde JS no dispara ningún evento. El patrón del sitio es asignar y después
  `entrada.dispatchEvent(new Event('input'))` (`movimiento-circular.html:513`).
- **Ningún widget se anima solo al cargar.**
- **Todo widget lleva al menos una lectura que se rompe si el modelo se rompe**, calculada por
  un camino **distinto** del que dibuja la escena. Y con ella, **cuatro reglas que esta
  plataforma aprendió a los golpes y que este plan da por sabidas**:
  1. Una resta que da cero **por construcción** no es un canario: es decoración que además
     miente diciendo que algo está verificado.
  2. **Verificar que cada chequeo se separa del modelo roto no prueba que dos chequeos sean
     independientes entre sí.** En el plan anterior, dos lecturas resultaron ser múltiplo
     escalar exacto una de la otra.
  3. **Variar el TIPO de rotura, no la cantidad.** Tres roturas de la misma familia no son una
     verificación: un implementador rompió tres veces términos proporcionales a la posición,
     concluyó «es una identidad» y puso un guion; una rotura de otra familia lo desmintió.
  4. **Ceguera a una familia de errores ≠ identidad.** Sólo lleva `—` una identidad
     **estructural** (los dos lados salen de la misma celda literal) o un caso sin segundo
     camino posible. Y **un `—` mudo es tan opaco como un cero que miente**: la prosa de la
     página tiene que decir por qué.
- **Todo widget lleva su frase de «qué mirar»** en su encabezado, en `--dim`.
- **Ningún número aparece sin respaldo** en `parcial-1/soluciones/verificacion-parcial-1-2025.py`.
  Los bloques numéricos que faltan los agrega la Tarea 1, **antes** de escribir una línea de HTML.
- **Las rutas se verifican sirviendo `docs/` como raíz**, que es lo que hace GitHub Pages.
  Servir el repositorio entero esconde enlaces rotos.
- **`docs/` contiene exactamente el sitio.** Los planes viven en `superpowers/plans/` y los
  documentos de diseño en `plataforma/`, los dos **en la raíz del repositorio**, justamente
  para que Pages no los publique. Ninguna tarea crea archivos nuevos dentro de `docs/` que no
  sean parte del sitio.
- **Capturas y scripts de medición** van a `.superpowers/sdd/<plan>/` (gitignorado) o a la
  carpeta temporal del sistema, **nunca a la raíz del repositorio**.
- **Al commitear, rutas explícitas.** Nunca `git add -A` ni `git add .`.
- Nombres en español. Las pruebas corren con `node --test "test/**/*.test.js"` desde la raíz.
  **Línea de base medida en `13cd3e0`: 248 pruebas, 0 fallas.** Ninguna tarea de este plan
  agrega pruebas: el motor no cambia.

## Estructura de archivos

**Páginas nuevas:**

| Archivo | Qué es |
|---|---|
| `docs/ejemplos/el-gol-con-viento.html` | Ejemplo 3 · práctico 1 adicional (ej. 15) · Parcial 1 2025, problema 1 |
| `docs/ejemplos/el-bloque-sobre-el-bloque.html` | Ejemplo 4 · práctico 2 adicional (ej. 19) · Parcial 1 2025, problema 3 |
| `docs/ejemplos/la-bolita-y-el-resorte.html` | Ejemplo 5 · Parcial 1 2025, problema 2 |

**Modificados:**

| Archivo | Qué cambia |
|---|---|
| `parcial-1/soluciones/verificacion-parcial-1-2025.py` | tres bloques numéricos (Tarea 1) |
| `docs/index.html` | tres filas nuevas de ejemplo |
| `docs/ensayos/tiro-parabolico.html` | el pie deja de reclamar el ej. 15 y enlaza la nota |
| `docs/ensayos/cuerpo-aislado.html` | el párrafo del ej. 19 enlaza la nota |
| `README.md` | las tres notas en la grilla de ejemplos, con miniatura |

**Lo que este plan NO hace:** no toca el motor, no agrega pruebas, no rediseña la portada
—el dueño la va a refactorizar—, y no escribe una nota para el ejercicio 18 del práctico 2
(el cono), que es adicional pero no fue al parcial.

## Las cinco tareas

| Fase | Tareas | Qué deja |
|---|---|---|
| A — cimientos | 1 | los números de los tres, corridos |
| B — las notas | 2, 3, 4 | las tres páginas |
| C — cerrar | 5 | portada, pies, README, miniaturas y auditoría |

---

## Fase A — cimientos

### Tarea 1: Los números de los tres, corridos

**Archivos:**
- Modificar: `parcial-1/soluciones/verificacion-parcial-1-2025.py`

**Interfaces:**
- Produce: tres bloques de salida (`P1 (numerico)`, `P2 (numerico)`, `P3 (numerico)`) que son
  la fuente de todo número de las tres notas.

El script ya existe, tiene 39 líneas y resuelve los tres problemas — el 1 y el 3 con números,
el 2 **en símbolos**. Lo que falta es fijar los valores concretos del problema 2 y dejar los
tres bloques con la forma que las notas van a citar.

- [ ] **Paso 1: elegir los valores del problema 2, y dejar dicho por qué**

El enunciado da `m`, `h`, `μ_d`, `L_BC`, `k`, `ℓ₀` como símbolos, con una sola atadura:
`h = 4·μ_d·L_BC`. Los valores elegidos:

| Símbolo | Valor | Por qué |
|---|---|---|
| `μ_d` | 0,25 | el mismo del problema 3 del parcial: una constante menos que explicar |
| `L_BC` | 2 m | el tramo se ve a escala junto a una pista de ~10 m |
| `h` | **2 m** | no se elige: sale de `h = 4·0,25·2` |
| `m` | 0,5 kg | una bolita, no un bloque |
| `k` | 200 N/m | da una compresión de 27 cm sobre un resorte de 60 cm: se ve, y no se cierra del todo |
| `ℓ₀` | 0,6 m | ídem |

**La atadura `h = 4 μ_d L_BC` no es decorativa**: es lo que hace que el resultado salga
redondo en símbolos, y por eso el enunciado la da. Con ella, `v_2C² = 6 μ g L` y
`W_resorte = −3 μ g L m` — sin `h` ni `k` a la vista. Eso se dice en la nota.

- [ ] **Paso 2: escribir los tres bloques**

Respetando el estilo que el archivo ya tiene (separador de comentario con guiones, `title(...)`,
`print(f"...")`), y **conviviendo** con los bloques simbólicos que ya están, no reemplazándolos.

- [ ] **Paso 3: correrlo y contrastar**

```bash
cd parcial-1/soluciones && python verificacion-parcial-1-2025.py
```

Los tres bloques nuevos tienen que imprimir **exactamente** esto (salida real, corrida al
escribir este plan):

```
P1 (numerico): g = 10 m/s^2 POR ENUNCIADO, v0 = 24 m/s, 30 grados, a_x = -2 m/s^2
  h_max = 7.20 m en t = 1.20 s ; v_x alli = 18.3846 m/s
  con viento cae en x = 44.12 m  -> le faltan 0.88 m para el arco
  sin viento, en x = 45 m (t = 2.1651 s) la pelota esta a y = 2.543 m
      -> pasa 0.103 m POR ENCIMA del travesano de 2.44 m
  no convierte de ninguna de las dos maneras

P2 (numerico): mu_d = 0.25, L_BC = 2 m, h = 2 m (= 4 mu L), m = 0.5 kg, k = 200 N/m
  v_A = v_2B = 6.2610 m/s      (cerrada sqrt(8 g mu L) = 6.2610)
  v_2C = 5.4222 m/s            (cerrada sqrt(6 g mu L) = 5.4222)
  compresion x = 0.2711 m -> longitud l = 0.3289 m sobre l0 = 0.6 m
  W_resorte = -7.3500 J        (cerrada -3 mu g L m = -7.3500 J)
  balance: K_B 9.8000 - disipado 2.4500 = K_C 7.3500  (residuo +0.0e+00)

P3 (numerico): A (40 N) sobre B (80 N), mu_d = 0.25
  N_AB = 40.0 N ; f_AB = 10.0 N ; T = 10.0 N
  (b) solo roce entre bloques: F = 20.0 N
  (c) ademas roce con el piso (N = 120.0 N, f = 30.0 N): F = 50.0 N
```

Si algún dígito difiere, **manda el script** y hay que corregir este plan, no el script.

- [ ] **Paso 4: un control que no sea una tautología**

El bloque `P2` tiene que imprimir además **un control genuino**, y el plan dice cuál porque el
proyecto ya se quemó con esto: integrar el tramo `B→C` **paso a paso en el tiempo** —Euler
explícito, `v -= mu*g*dt`, `s += v*dt`— desde `v_2B` y comprobar que al recorrer `L_BC` la
velocidad da `v_2C`. Un camino es una forma cerrada; el otro avanza en el tiempo.

Está implementado y validado en el bloque `Ej 7 (numerico)` de
`parcial-1/soluciones/verificacion-practico-3.py` — **leelo antes de escribir el tuyo**. Y de
ahí sale también la advertencia que hay que repetir: **el residuo de un Euler así es sesgo del
método, no ruido** (el bucle suma `v` después de decrementarlo, así que subcuenta `v·dt/2`).
Decilo en un comentario, o alguien va a achicar el paso, ver bajar el residuo y creer que
arregló algo.

**Y el diagnóstico corrido, no razonado:** imprimí también cuánto da ese control con el modelo
roto a propósito —por ejemplo integrando con `2·mu` en vez de `mu`— para que se vea que se
mueve. Si no se mueve, el control no sirve y hay que avisar.

- [ ] **Paso 5: commit**

```bash
git add parcial-1/soluciones/verificacion-parcial-1-2025.py
git commit -m "feat(soluciones): bloques numericos de los tres problemas del parcial 1 2025"
```

---

## Fase B — las tres notas

Las tres comparten el molde. **Antes de la primera, leer `docs/ejemplos/la-tierra.html`
entero** (244 líneas): de ahí sale el esqueleto, el encabezado, la franja del widget, la
sección `Cómo se resuelve` y el pie. `auto-y-camion.html` (303 líneas) es el segundo ejemplo
y muestra cómo queda con dos móviles.

**El pie de cada nota** cita la fuente oficial y enlaza el PDF del práctico que corresponde,
con la misma forma que usan las dos notas existentes, más el `· código` que todas las páginas
del sitio llevan desde `13cd3e0`.

---

### Tarea 2: `el-gol-con-viento.html` — la nota que además tapa un agujero

**Archivos:**
- Crear: `docs/ejemplos/el-gol-con-viento.html`

**Interfaces:**
- Consume: `crearPagina`, `crearWidget`, `deslizador`, `casilla`, `conectarTema`, y de
  `dibujo.js`: `eje`, `curva`, `punteado`, `vectorPx`, `cuerpo`, `suelo`. Y `num()` de
  `formato.js`.
- Produce: la página completa.

**El ejercicio, del oficial.** Una jugadora patea desde el piso con `v₀ = 24 m/s` a `30°`. Hay
viento: además de la gravedad, la pelota sufre una aceleración horizontal de `2 m/s²` **en
sentido opuesto a su movimiento**. El arco mide `2,44 m` de alto y está a `45 m`. La cancha es
de arena: al caer, la pelota no rebota ni se desplaza. **`g = 10 m/s²`, por enunciado.**

**El resultado que hace la nota.** Del bloque `P1 (numerico)`: con viento la pelota cae en
`44,12 m` —le faltan **88 cm**—; sin viento llega a los 45 m pero pasando a `2,543 m`,
**10,3 cm por encima** del travesaño. **No convierte de ninguna de las dos maneras, y por
razones opuestas.** Ésa es la nota: la respuesta no es «el viento le costó el gol».

- [ ] **Paso 1: el esqueleto**

Copiar el de `la-tierra.html`. `<h1>`: `El gol con viento`. La bajada, en `--dim`:
`Con viento se queda corta. Sin viento se va por arriba. Las dos cosas, con el mismo tiro.`

- [ ] **Paso 2: el modelo, con dos caminos que no comparten una línea**

```js
const G_W1 = 10;              // POR ENUNCIADO: este ejercicio fija g = 10, no 9,8
const V0_W1 = 24, AX_W1 = -2, ARCO_X_W1 = 45, ARCO_H_W1 = 2.44;

// Camino 1 -- forma cerrada. Es la que DIBUJA la trayectoria.
const posCerrada_W1 = (t, ang, ax) => ({
  x: V0_W1 * Math.cos(ang) * t + 0.5 * ax * t * t,
  y: V0_W1 * Math.sin(ang) * t - 0.5 * G_W1 * t * t,
});

// Camino 2 -- integracion en el tiempo. Es la que CHEQUEA, y no mira la formula de arriba.
function posIntegrada_W1(t, ang, ax, n = 4000) {
  const dt = t / n;
  let x = 0, y = 0, vx = V0_W1 * Math.cos(ang), vy = V0_W1 * Math.sin(ang);
  for (let i = 0; i < n; i++) {
    vx += ax * dt; vy -= G_W1 * dt;
    x += vx * dt;  y += vy * dt;
  }
  return { x, y };
}
```

**El chequeo** es `|posCerrada − posIntegrada|` en el instante que el deslizador marca, en
metros. Con el modelo bien queda en el orden de `10⁻³ m` (sesgo de Euler, **no** ruido: el
bucle suma después de incrementar). **Medí y anotá en un comentario** cuánto da rompiendo el
modelo de **dos familias distintas de rotura**:
1. una que toque el término del viento (por ejemplo `ax` con signo cambiado),
2. una que **no** lo toque (por ejemplo `G_W1` en 9,8, o el `0.5` del término cuadrático).

La regla 3 de las Global Constraints existe por esto: tres roturas de la misma familia no son
una verificación.

- [ ] **Paso 3: los controles**

- deslizador `w1-ang` (`min="10" max="80" step="1" value="30"`, grados) — el ángulo del tiro.
- casilla `w1-viento`, **tildada por defecto** — prende y apaga la aceleración horizontal.
- botón `w1-play` y `w1-reset`, con `crearEscena` y `rotuloReproducir`, **como
  `auto-y-camion.html`** — no un deslizador de tiempo como `la-tierra.html`. Los dos patrones
  existen en el sitio y acá manda la comparación: lo que la nota quiere que se vea es la pelota
  cayendo corta contra la pelota yéndose por arriba, y eso se mira, no se raspa con un
  deslizador. La escena tiene que poder **pausarse**: el instante del punto más alto es donde
  se lee el ángulo de 101° entre `v` y `a`.

**Al cambiar la casilla, el encuadre no se toca**: las dos trayectorias tienen que verse en el
mismo cuadro para que la comparación signifique algo.

- [ ] **Paso 4: el dibujo**

Una sola escena, de perfil. El piso con `suelo`. El arco en `x = 45` como dos segmentos (poste
de 2,44 m y travesaño), en `--ink`. La trayectoria **con** viento en `--graph` llena; la
trayectoria **sin** viento en `--graph` punteada, siempre visible aunque la casilla esté
tildada — es la comparación entera de la nota. La pelota como `cuerpo`. Y en el instante
elegido, `vectorPx` para `v` (azul) y para `a` (rojo).

**El detalle que el ensayo de tiro no puede mostrar y ésta sí:** en el punto más alto,
`v` y `a` **no son perpendiculares** — forman unos 101°, porque `a_x` sigue frenando. En el
tiro parabólico común lo son siempre. Que se vea en el dibujo y se diga en la prosa.

- [ ] **Paso 5: las lecturas**

`altura máxima` (azul), `alcance` (azul), `y en x = 45 m`, `chequeo` (`--dim`), y una lectura
`¿gol?` que diga `no` / `sí` — es la pregunta (d) del enunciado.

- [ ] **Paso 6: la sección `Cómo se resuelve`**

Con los ítems (a) a (f) del enunciado oficial, en prosa, y los números del bloque
`P1 (numerico)`. El cierre es el hallazgo: erró de las dos maneras.

- [ ] **Paso 7: verificar**

1. Las lecturas por defecto (30°, con viento) contra el bloque `P1 (numerico)`.
2. Destildar el viento: el alcance pasa a 45 m con la pelota a 2,543 m — por encima.
3. Barré el deslizador de ángulo: **¿hay algún ángulo que convierta?** Anotá la respuesta en el
   informe; si lo hay, va en la prosa, y es la mejor frase de la nota.
4. **Medí** las dos flechas en el punto más alto y confirmá el ángulo de ~101° entre ellas.
5. 1280 y 390 px, los dos temas, consola limpia, ningún widget animándose solo al cargar.
6. Rompé el modelo de las dos familias del Paso 2 y confirmá que el chequeo salta en las dos.
7. `diff` de conjuntos de `style` contra `la-tierra.html`: ninguna línea `>`.

- [ ] **Paso 8: commit**

```bash
node --test "test/**/*.test.js"     # siguen siendo 248
git add docs/ejemplos/el-gol-con-viento.html
git commit -m "feat(ejemplos): el gol con viento, el adicional de la guia 1"
```

---

### Tarea 3: `el-bloque-sobre-el-bloque.html`

**Archivos:**
- Crear: `docs/ejemplos/el-bloque-sobre-el-bloque.html`

**Interfaces:**
- Consume: lo de la Tarea 2, más `bloque` y `arco` de `dibujo.js`, y `colocarEtiqueta`.
- Produce: la página completa.

**El ejercicio, del oficial.** El bloque A pesa `40 N` y está apoyado **sobre** B, que pesa
`80 N`. `μ_d = 0,25` y `μ_e = 0,4` entre superficies. Una cuerda sale de A, pasa por una polea
sujeta a la pared y baja a B. Se arrastra B hacia la izquierda con `F`, a **velocidad
constante**, y se pide: (a) el diagrama de cuerpo aislado de cada bloque, (b) `F` si sólo hay
roce entre los bloques, (c) `F` si además hay roce con el piso. Polea sin rozamiento.

**La geometría importa y se lee de la figura oficial:** la cuerda une A **con B** pasando por
la polea de la pared. Por eso la tensión tira de los dos hacia la pared, y por eso `F` tiene
que vencer `T` **más** el rozamiento, no sólo el rozamiento.

Del bloque `P3 (numerico)`: `N_AB = 40 N`, `f_AB = 10 N`, `T = 10 N`, `F = 20 N` en el caso
(b) y `F = 50 N` en el (c), donde el piso carga con los `120 N` de los dos bloques.

- [ ] **Paso 1: el esqueleto**

`<h1>`: `Un bloque sobre otro`. Bajada: `Arrastrar a B cuesta el doble de lo que parece: el
rozamiento de A aparece dos veces, una como fuerza y otra como tensión.`

- [ ] **Paso 2: el modelo**

Velocidad constante ⇒ suma de fuerzas nula en cada bloque. Con `W_A = 40`, `W_B = 80`,
`μ = 0,25` y la casilla del piso:

```js
const nAB_W1  = () => W_A_W1;                       // A solo apoya su peso sobre B
const fAB_W1  = () => MU_W1 * nAB_W1();             // rozamiento entre los bloques
// `tension_W1` y no `t_W1`: en todo el sitio `t` es el tiempo. Y `fuerzaF_W1` y no `f_W1`:
// `f` es el rozamiento en las otras siete paginas. Un nombre prestado cuesta una relectura
// entera dentro de seis meses.
const tension_W1  = () => fAB_W1();                 // A no acelera: la cuerda equilibra su rozamiento
const nPiso_W1    = () => W_A_W1 + W_B_W1;          // el piso carga con los dos
const fPiso_W1    = conPiso => conPiso ? MU_W1 * nPiso_W1() : 0;
const fuerzaF_W1  = conPiso => tension_W1() + fAB_W1() + fPiso_W1(conPiso);
```

**El chequeo NO puede ser la suma de fuerzas**: se anula por construcción, porque `F` se
despejó de ahí. Da cero pase lo que pase y sería exactamente la decoración que las Global
Constraints prohíben.

**El camino distinto es simular.** Con la `F` calculada, integrar en el tiempo las dos segundas
leyes —`a_B = (F − T − f_AB − f_piso)/m_B` y `a_A = (T − f_AB)/m_A`, con las masas sacadas de
los pesos— arrancando con `v_B = 1 m/s`, y comprobar que después de un segundo `v_B` **sigue
siendo 1 m/s**. Si `F` está mal, el bloque acelera o frena y se ve. La lectura es
`v después − v antes`, en m/s.

**Medí y anotá dónde no muerde**, con roturas de **dos familias**: una que toque el término del
piso y otra que no (por ejemplo `N_AB` mal, o `μ` mal). Y fijate en particular si el chequeo se
vuelve ciego con la casilla del piso destildada.

- [ ] **Paso 3: los controles**

- casilla `w1-piso`, **destildada** por defecto — pasa del caso (b) al (c).
- deslizador `w1-mu` (`min="0.05" max="0.6" step="0.05" value="0.25"`) — para ver que `F`
  crece lineal con μ, que es lo que el ejercicio no pregunta y conviene ver.

Acordate del `dispatchEvent(new Event('input'))` si la casilla reescribe algún deslizador.

- [ ] **Paso 4: el dibujo**

El piso con `suelo`, B apoyado, A encima de B, la pared a la derecha, la polea como un
círculo pequeño con `arco`, y la cuerda con `traza` (A → polea → B). `F` en rojo tirando de B
hacia la izquierda.

**Los dos diagramas de cuerpo aislado son el ítem (a) del enunciado, o sea obligatorios.** Van
al costado o debajo, cada cuerpo con sus flechas rotuladas: en A, `P_A`, `N_AB`, `f_AB` y `T`;
en B, `P_B`, `N_AB` (reacción), `N_piso`, `f_AB` (reacción), `f_piso` si corresponde, `T` y
`F`. Todas las fuerzas en rojo, rotuladas por la opción `rotulo:` de `vectorPx`.

**Cuidado con los rótulos**: son muchas flechas cortas y juntas. Barré el rango de los
controles con el `colocarEtiqueta` real y contá solapamientos; el objetivo es cero, medido a
880 y a 350 px.

- [ ] **Paso 5: las lecturas**

`N entre bloques`, `f entre bloques`, `tensión`, `N del piso`, `F necesaria` (rojo) y
`chequeo` (`--dim`).

- [ ] **Paso 6: la sección `Cómo se resuelve`**

Los ítems (a), (b) y (c) con sus números. El punto que más cuesta y que la nota tiene que
dejar claro: **el rozamiento de A aparece dos veces en la ecuación de B** — una como fuerza de
contacto y otra como tensión de la cuerda —, y por eso `F = 20 N` y no `10 N`.

- [ ] **Paso 7: verificar**

1. Lecturas por defecto contra `P3 (numerico)`: 40 / 10 / 10 / — / 20 N.
2. Tildar el piso: `N del piso` da 120 N y `F` pasa a 50 N.
3. Barrido de rótulos: cero solapamientos y cero cruces, a 880 y 350 px, medido.
4. Rompé el modelo de las dos familias del Paso 2; confirmá que el chequeo salta en las dos.
5. 1280 y 390 px, los dos temas, consola limpia, nada que se anime solo.
6. `diff` de conjuntos de `style` contra `la-tierra.html`: ninguna línea `>`.

- [ ] **Paso 8: commit**

```bash
node --test "test/**/*.test.js"     # 248
git add docs/ejemplos/el-bloque-sobre-el-bloque.html
git commit -m "feat(ejemplos): un bloque sobre otro, el adicional de la guia 2"
```

---

### Tarea 4: `la-bolita-y-el-resorte.html` — las tres guías en un problema

**Archivos:**
- Crear: `docs/ejemplos/la-bolita-y-el-resorte.html`

**Interfaces:**
- Consume: todo lo anterior, más `crearEscena`, `rotuloReproducir`, `boton`, `traza` (el zigzag
  del resorte) y **`presupuestoPx`** (la barra de energía).
- Produce: la página completa.

**El ejercicio, del oficial.** Una bolita `b₁` de masa `m` está en reposo en una loma a altura
`h`. Baja y choca con `b₂`, **idéntica**, en reposo en `A`. El choque es **perfectamente
elástico**. `b₂` atraviesa el tramo `B–C` donde hay rozamiento `μ_d`, y al final de la pista
hay un resorte de constante `k` y longitud natural `ℓ₀`. La pista cumple `h = 4·μ_d·L_BC`. Se
pide: (a) `v_{2,B}` y qué le pasa a `b₁` tras el choque; (b) la longitud del resorte en máxima
compresión, el trabajo del resorte, e interpretarlo.

**Por qué esta nota cierra el plan.** Es el único ejercicio del parcial que encadena las tres
guías: conservación de energía en la bajada (guía 3), choque elástico entre masas iguales
(guía 3), rozamiento que disipa a lo largo de un tramo (guías 2 y 3) y resorte que almacena
(guía 3). Y cada pieza ya tiene su widget en el sitio: ésta las pone en fila.

Valores de la Tarea 1: `μ_d = 0,25`, `L_BC = 2 m`, `h = 2 m`, `m = 0,5 kg`, `k = 200 N/m`,
`ℓ₀ = 0,6 m`, `g = 9,8`. Resultados: `v_2B = 6,2610 m/s`, `v_2C = 5,4222 m/s`, compresión
`0,2711 m` (el resorte queda en `0,3289 m`), `W_resorte = −7,3500 J`.

- [ ] **Paso 1: el esqueleto**

`<h1>`: `La bolita y el resorte`. Bajada: `Un choque, un tramo con rozamiento y un resorte. La
energía cambia de casillero tres veces y sólo una vez se pierde.`

- [ ] **Paso 2: el modelo por tramos**

Cinco tramos, en orden: `b₁` baja de `h` a `A`; el choque en `A`; `b₂` de `A` a `B` sin
rozamiento; `b₂` de `B` a `C` con rozamiento; `b₂` de `C` al resorte y lo comprime.

**El choque elástico entre masas iguales es un intercambio de velocidades**: `b₁` queda
**quieta** en `A` y `b₂` sale con toda la velocidad. Eso es el ítem (a) y el widget lo tiene
que mostrar sin ambigüedad: `b₁` se detiene a la vista.

- [ ] **Paso 3: la barra de energía**

Con `presupuestoPx`, contra el total declarado `E = m·g·h = 9,8 J`, con cuatro segmentos:

| Segmento | Color | Cuándo aparece |
|---|---|---|
| cinética | azul | desde que empieza a bajar |
| potencial gravitatoria | `--graph` | mientras `b₁` baja |
| potencial elástica | `--graph` | mientras comprime el resorte |
| disipado | rojo | desde `B` en adelante |

**Las dos potenciales usan el mismo token y no se pisan**: la gravitatoria se agota al llegar
al pie de la loma y la elástica recién aparece contra el resorte, sobre terreno llano. Nunca
coexisten. Verificalo mirando la barra en el tramo `B–C`: ahí no tiene que haber ni una ni otra.

Firma exacta, del motor en `13cd3e0`:
`presupuestoPx(ctx, x, y, ancho, alto, segmentos, { total, colorBorde, colorTexto, minEtiquetaPx = 24 })`,
con `segmentos` una lista de `{ valor, color, etiqueta }` en las mismas unidades que `total`.
**Mide contra el `total` declarado**: si la suma es menor queda barra sin pintar. Un segmento
negativo, `NaN` o infinito tira `TypeError` a propósito, y desde `13cd3e0` **un `total` ausente
también**. Si te lo tira, es que el modelo te está dando algo imposible: no lo esquives.

- [ ] **Paso 4: el chequeo**

`v_C integrada − v_C cerrada`, en m/s. La cerrada es `√(6·μ·g·L)`; la integrada avanza el tramo
`B–C` paso a paso en el tiempo, exactamente como el control de la Tarea 1 Paso 4, que ya está
corrido y validado en python. Reusá ese método y su paso.

**Anotá dónde no muerde**, con roturas de dos familias distintas: una que toque `μ` (que entra
en las dos ramas por caminos distintos) y otra que toque la masa. Sobre la masa hay un
precedente exacto en este sitio: en el ensayo de energía, un error de masa es invisible al
chequeo **en todo el rango**, porque multiplica por igual a los cuatro términos y se cancela en
la resta. Fijate si acá pasa lo mismo y decilo.

- [ ] **Paso 5: los controles**

- deslizador `w1-mu` (`min="0.1" max="0.4" step="0.05" value="0.25"`). **Ojo:** al mover μ
  cambia `h`, porque el enunciado ata `h = 4 μ L`. Que se vea: la loma sube y baja con el
  deslizador. Eso **es** el ejercicio.
- botón de reproducción y de reinicio, con `crearEscena` y `rotuloReproducir`.

- [ ] **Paso 6: las lecturas**

`v en B` (azul), `v en C` (azul), `compresión` , `trabajo del resorte` (rojo) y `chequeo`
(`--dim`).

- [ ] **Paso 7: la sección `Cómo se resuelve`**

Ítems (a) y (b) con sus números, y **la interpretación que el enunciado pide explícitamente**:
el trabajo del resorte es **negativo** porque la fuerza apunta al revés del movimiento, y su
módulo es exactamente la energía cinética que traía la bolita — el resorte no destruye energía,
la guarda. Y el cierre: la atadura `h = 4 μ L` es lo que hace que el resultado salga limpio en
símbolos, sin `h` ni `k` a la vista.

- [ ] **Paso 8: verificar**

1. Las lecturas en los cinco tramos contra el bloque `P2 (numerico)`.
2. **Medí los anchos de la barra** interceptando `fillRect`, en al menos cuatro instantes: arriba
   de la loma, en `A`, en `C` y en máxima compresión. En `A` la barra tiene que estar entera en
   azul; en máxima compresión, entera entre `--graph` y rojo, sin azul.
3. Mové μ y confirmá que la loma cambia de altura.
4. Barrido de rótulos: cero cruces y cero solapamientos, medido a 880 y 350 px.
5. Rompé el modelo de dos familias distintas y confirmá que el chequeo salta en las dos.
6. 1280 y 390 px, los dos temas, consola limpia, nada que se anime solo al cargar.
7. `diff` de conjuntos de `style` contra `la-tierra.html`: ninguna línea `>`.

- [ ] **Paso 9: commit**

```bash
node --test "test/**/*.test.js"     # 248
git add docs/ejemplos/la-bolita-y-el-resorte.html
git commit -m "feat(ejemplos): la bolita y el resorte, el problema que encadena las tres guias"
```

---

## Fase C — cerrar

### Tarea 5: Portada, pies, README y la auditoría

**Archivos:**
- Modificar: `docs/index.html`, `docs/ensayos/tiro-parabolico.html`,
  `docs/ensayos/cuerpo-aislado.html`, `README.md`
- Crear: `assets/miniaturas/el-gol-con-viento.png`, `assets/miniaturas/el-bloque-sobre-el-bloque.png`,
  `assets/miniaturas/la-bolita-y-el-resorte.png`

**Interfaces:**
- Consume: las tres notas nuevas.
- Produce: la navegación cerrada y la cobertura honesta.

- [ ] **Paso 1: la portada**

`docs/index.html` lista hoy dos ejemplos (`Ejemplo 1`, `Ejemplo 2`). Agregar tres filas
—`Ejemplo 3`, `4` y `5`— copiando la estructura de las dos que están, sin `style` propio:
`.encabezado-widget`, `.rotulo-mono` y `.titulo-fila`.

- [ ] **Paso 2: la fila de cobertura falsa del ensayo de tiro**

Éste es el paso que justifica media tarea. El pie de `docs/ensayos/tiro-parabolico.html` dice:

```
Apunte cap. 2, pp. 25–47 · hoja resumen · práctico 1, ej. 9, 10 y 15 · g = 9,8 m/s² · código
```

**y el ensayo no trata el ejercicio 15.** Comprobalo vos antes de tocar: buscá en ese archivo
la aceleración horizontal, el arco, los 45 m o los 2,44 m. No están.

El arreglo: que el pie deje de reclamar el 15 —pasa a `ej. 9 y 10`— y que **enlace la nota
nueva**, que sí lo trata. Mirá cómo enlazan otras páginas del sitio antes de inventar una
forma.

- [ ] **Paso 3: el ensayo de cuerpo aislado**

Ese sí trata el ejercicio 19, en prosa, en un párrafo que arranca `Ej. 19 — un bloque sobre
otro.` con todos sus números. **No le saques la cobertura.** Agregale un enlace a la nota, que
es la versión animada del mismo ejercicio — el mismo vínculo que existe entre
`movimiento-circular.html` y `la-tierra.html`.

- [ ] **Paso 4: el README**

Las tres notas entran en la grilla de tarjetas de `Ejemplos resueltos`, que hoy tiene dos y
pasa a cinco. La grilla es hoy de **dos** columnas (`width="50%"`); con cinco tarjetas pasa a
**tres por fila** (`width="33%"`), o sea una fila de tres y una de dos. Tres por fila es lo que
ya usa la grilla de ensayos —que es de cuatro— llevado a un número que no deja una tarjeta
sola en su propio renglón. Y la prosa del `<details>` correspondiente suma sus tres filas.

**Las miniaturas se generan igual que las diez que ya están:** Chrome headless por CDP,
recortando el primer canvas, a `assets/miniaturas/` y **no** a `docs/`. El script que se usó
está descrito en el commit `8bb30ab`. Dos de las diez existentes se capturaron con un control
encendido porque su estado por defecto no mostraba el tema: **mirá cada una de las tres
capturas antes de darlas por buenas**, y si alguna no muestra de qué trata la nota, capturala
con el control que corresponda y decí cuál.

- [ ] **Paso 5: la auditoría de cobertura**

Para **cada una** de las tres notas: abrí la página, buscá el ítem del enunciado oficial, y
comprobá que está tratado ahí con sus números y no mencionado al pasar. Si una no está,
corregí este plan, no la memoria.

Y una fila más, que este plan hereda y no puede dejar pasar: **el ejercicio 18 del práctico 2**
(el cono que gira) también es un adicional oficial, y `cuerpo-aislado.html` dice cubrirlo.
Comprobá si lo trata de verdad, como se hizo con el 15 y el 19. Si no lo trata, **no lo
arregles en este plan**: anotalo en el informe, porque es material de otro.

- [ ] **Paso 6: el recorrido completo**

1. Servir **`docs/` como raíz** —no el repositorio— y recorrer: portada → los ocho ensayos →
   los **cinco** ejemplos → volver. Ningún 404.
2. Los tres widgets nuevos a 1280 y 390 px, en los dos temas, con la consola abierta.
3. Ningún widget se anima solo al cargar.
4. `grep -rn "toFixed" docs/ejemplos/` no devuelve nada.
5. `node --test "test/**/*.test.js"`: **248 pruebas, 0 fallas**.

- [ ] **Paso 7: commit**

```bash
git add docs/index.html docs/ensayos/tiro-parabolico.html docs/ensayos/cuerpo-aislado.html \
        README.md assets/miniaturas
git commit -m "feat(plataforma): enlazar las tres notas del parcial y corregir la cobertura del ej. 15"
git status --short    # limpio
```
