# Plataforma de Física 1 — Pagar la deuda · Plan de implementación

> **Para trabajadores agénticos:** SUB-SKILL REQUERIDA: usar superpowers:subagent-driven-development (recomendada) o superpowers:executing-plans para implementar este plan tarea por tarea. Los pasos usan sintaxis de casilla (`- [ ]`) para seguimiento.

**Objetivo:** dejar el terreno limpio antes de escribir los dos ensayos de la Guía 3: una sola convención de números en todo el sitio, las clases tipográficas que faltan, los dos defectos del motor que quedaron parqueados, y el único ejercicio de la Guía 2 que no está cubierto.

**Arquitectura:** no hay nada conceptualmente nuevo acá. Son cuatro barridos y dos arreglos, todos sobre páginas que ya funcionan, así que **el criterio de aceptación de casi todo es que nada cambie a la vista** salvo exactamente lo que se quiso cambiar. Eso se demuestra midiendo, no afirmando.

**Stack:** ES modules vanilla, canvas 2D, `node --test` de Node 22, GitHub Pages desde `/docs`.

**Spec:** `docs/plataforma/brief.md`

**Autoridad de diseño:** `docs/plataforma/diseno/Tiro parabolico.dc.html`

**Medición de partida:** `.superpowers/investigacion-deuda/medicion.md`, con los scripts que la produjeron al lado. Todo número que aparece en este plan sale de ahí.

## Las dos decisiones del dueño que este plan ejecuta

**1. Separador decimal: coma, en todo el sitio.** Prosa y lecturas de widget, las nueve páginas. Hoy el sitio está partido: los tres ensayos de la Guía 2 escriben la prosa en coma y sus lecturas en punto —el mismo número dos veces distinto en la misma pantalla—, y las otras cinco páginas usan punto en los dos lados.

Lo que estaba roto no era la elección sino la mezcla: las frases de «qué mirar» le piden al lector que contraste la lectura contra el párrafo, y el contraste fallaba en la puntuación.

**2. El camión de `auto-y-camion.html` se queda rojo.** Es una excepción explícita y única al reparto semántico «rojo para aceleración y para cada fuerza»: ahí el rojo distingue un cuerpo y no una magnitud. **No se toca, y este plan la registra por escrito** para que ningún plan futuro la lea como deriva y la «arregle».

## Global Constraints

Aplican a todas las tareas.

- **Cero dependencias de runtime** salvo KaTeX por CDN. Nada de `npm install`. **Cero build.**
- **Los tokens de color son exactamente estos**, y no se inventa ninguno:
  claro `--paper:#fbfaf7` `--band:#f2f0ea` `--ink:#16151a` `--dim:#6a6760`
  `--rule:#dcd8ce` `--blue:#1b4fd4` `--blue-soft:#8aa3e6` `--red:#c02a24`
  `--graph:#8e8a80`; oscuro `--paper:#131316` `--band:#191a1e` `--ink:#eceae4`
  `--dim:#948f86` `--rule:#2e2f35` `--blue:#7aa2ff` `--blue-soft:#3f5694`
  `--red:#ef5f52` `--graph:#6f6c66`. Nunca se escriben literales hex en JS.
- **Reparto semántico:** azul para cinemática y velocidad; rojo para aceleración y para
  cada fuerza que actúa; azul para la resultante; `--graph` para la trayectoria. **Única
  excepción registrada:** el camión de `auto-y-camion.html`.
- **Tipografías:** Source Serif 4 para el contenido, JetBrains Mono para la interfaz.
- **Canvas:** `width:100%`, `aspect-ratio:16/8`, `touch-action:none`, desde la regla de
  elemento de `base.css`.
- **Ningún widget se anima solo al cargar.**
- **Las rutas se verifican sirviendo `docs/` como raíz**, que es lo que hace GitHub Pages.
  Servir el repositorio entero esconde enlaces rotos: así se escapó un defecto crítico.
- **Al comparar bitmaps**, usar `.superpowers/sdd/2026-09-11-plataforma-guia-2/comparar-bitmaps.mjs`,
  que lanza un proceso de Chrome nuevo por medición. Reusar el proceso da falsos
  «idéntico» aunque el código haya cambiado. **Y el control negativo tiene que mutar algo
  que el canvas bajo prueba realmente use**: un control que muta una función que ese canvas
  no llama no prueba nada sobre ese canvas.
- Chrome ignora `--window-size` por debajo de unos 526 px en esta máquina. Para anchos
  angostos, `Emulation.setDeviceMetricsOverride`.
- Nombres en español. Las pruebas corren con `node --test "test/**/*.test.js"` desde la
  raíz del worktree. Al empezar este plan son **224** y pasan.

## Estructura de archivos

| Archivo | Qué cambia |
|---|---|
| `docs/motor/formato.js` | **nuevo** — `num`, `exp` y `marca`, el único lugar donde un número se convierte en texto |
| `docs/motor/dibujo.js` | `eje()` deriva los decimales del paso y rotula con coma |
| `docs/motor/etiqueta.js` | **nuevo** — `colocarEtiqueta`, que ubica un rótulo sin salirse del canvas ni pisar a otro |
| `docs/estilos/base.css` | recibe ocho clases tipográficas |
| las 9 páginas | adoptan las clases, y sus 117 lecturas pasan por `formato.js` |
| `docs/ensayos/sistemas-acoplados.html` | además, la frase del ejercicio 2 |
| `docs/plataforma/decisiones.md` | **nuevo** — las dos decisiones del dueño, por escrito |

## Las seis tareas

| Fase | Tarea | Qué deja |
|---|---|---|
| A — el formato | 1 | `formato.js` con sus pruebas |
| B — los barridos | 2 | las ocho clases tipográficas aplicadas a las 9 páginas |
| | 3 | los 117 sitios y la prosa de 5 páginas, convertidos a coma |
| C — el motor | 4 | `eje()` arreglado: decimales del paso, rótulos con coma |
| | 5 | `colocarEtiqueta` y los 18 sitios que rotulan cuerpos |
| D — cerrar | 6 | la frase del ejercicio 2, las decisiones por escrito, el recorrido |

**Las tareas 2 y 3 barren las mismas nueve páginas y no pueden ir en paralelo.** Van en ese
orden a propósito: primero las clases, que no tocan ningún número, y después los números,
que no tocan ningún estilo. Así cada barrido tiene un criterio de aceptación limpio.

---

## Fase A — un solo lugar donde un número se vuelve texto

### Tarea 1: `docs/motor/formato.js`

Hoy hay **117 sitios** en las nueve páginas que convierten un número en texto, todos con
`toFixed`, `toExponential` o `String`, y todos con punto porque es lo que hace JS. Con la
coma como convención del sitio, ese conocimiento tiene que vivir en un lado solo.

**Archivos:**
- Crear: `docs/motor/formato.js`
- Prueba: `test/formato.test.js` (nuevo)

**Interfaces:**
- Consume: nada.
- Produce, y las tareas 3 y 4 consumen:
  - `num(x, decimales)` — como `toFixed` pero con coma.
  - `exp(x, decimales)` — notación científica legible, con coma en la mantisa.
  - `marca(x, paso)` — el rótulo de una marca de eje: los decimales salen del paso, sin
    ceros de más, con coma.

- [ ] **Paso 1: escribir las pruebas que fallan**

```js
import { test } from 'node:test';
import assert from 'node:assert';
import { num, exp, marca } from '../docs/motor/formato.js';

test('num usa coma y respeta los decimales pedidos', () => {
  assert.equal(num(0.388, 3), '0,388');
  assert.equal(num(574.9, 1), '574,9');
  assert.equal(num(2, 2), '2,00');
  assert.equal(num(-1.5, 1), '-1,5');
});

test('num no deja el cero con signo', () => {
  // La cancelacion de una resultante deja a veces -1e-13, y toFixed lo imprime
  // como "-0,00". Es la lectura que varios widgets usan como prueba de su modelo:
  // tiene que decir cero, no menos cero.
  assert.equal(num(-1e-13, 2), '0,00');
  assert.equal(num(-0, 1), '0,0');
  assert.equal(num(0, 1), '0,0');
});

test('exp separa mantisa y exponente de forma legible', () => {
  // Hoy fuerzas-de-posicion.html imprime "1.0808e-2" crudo en pantalla.
  assert.equal(exp(1.0808e-2, 4), '1,0808 × 10⁻²');
  assert.equal(exp(3.456e8, 3), '3,456 × 10⁸');
  assert.equal(exp(-2.5e-3, 1), '-2,5 × 10⁻³');
});

test('exp trata el exponente cero sin ensuciar', () => {
  assert.equal(exp(1.5, 1), '1,5');
});

test('marca saca los decimales del paso y no deja ceros de mas', () => {
  // Es el comportamiento que `eje()` tiene HOY para paso >= 0.1, y que hay que
  // conservar exactamente: un entero se rotula sin coma decimal.
  assert.equal(marca(-1, 0.5), '-1');
  assert.equal(marca(2, 1), '2');
  assert.equal(marca(0.5, 0.5), '0,5');
  assert.equal(marca(0.25, 0.05), '0,25');
  assert.equal(marca(1.2, 0.2), '1,2');
});

test('marca con paso fino no produce rotulos repetidos', () => {
  // El defecto que este plan viene a cerrar: con paso 0.05, redondear a un decimal
  // daba "0,3" dos veces seguidas.
  const rotulos = [0.30, 0.35, 0.40].map(x => marca(x, 0.05));
  assert.deepEqual(rotulos, ['0,3', '0,35', '0,4']);
  assert.equal(new Set(rotulos).size, 3);
});
```

- [ ] **Paso 2: correrlas y verificar que fallan**

Ejecutar: `node --test test/formato.test.js`
Esperado: FALLAN todas, con `Cannot find module`.

- [ ] **Paso 3: implementar**

```js
// El unico lugar del sitio donde un numero se vuelve texto. Existe porque la
// convencion del sitio es la COMA -- decision del dueno, ver docs/plataforma/decisiones.md
// -- y JS escribe punto en `toFixed`, `toExponential` y `String`. Tener 117 sitios
// haciendo la conversion a mano garantiza que tarde o temprano uno quede en punto.

const SUPERINDICES = { '-': '⁻', 0: '⁰', 1: '¹', 2: '²', 3: '³', 4: '⁴',
                       5: '⁵', 6: '⁶', 7: '⁷', 8: '⁸', 9: '⁹' };

// Quita el signo de un cero que salio de una cancelacion: varios widgets usan una
// lectura que tiene que dar cero como prueba de su modelo, y "-0,00" se lee como si
// el modelo estuviera roto cuando en realidad esta bien.
function sinCeroNegativo(s) {
  return /^-0(,0*)?$/.test(s) ? s.slice(1) : s;
}

export function num(x, decimales) {
  return sinCeroNegativo(x.toFixed(decimales).replace('.', ','));
}

export function exp(x, decimales) {
  const e = x === 0 ? 0 : Math.floor(Math.log10(Math.abs(x)));
  if (e === 0) return num(x, decimales);
  const mantisa = num(x / Math.pow(10, e), decimales);
  const sufijo = String(e).split('').map(c => SUPERINDICES[c]).join('');
  return `${mantisa} × 10${sufijo}`;
}

// El rotulo de una marca de eje. Los decimales salen del PASO y no de un numero fijo:
// con paso 0.05 hacen falta dos, con paso 1 ninguno. Y se usa `String` sobre el valor
// redondeado en vez de `toFixed`, para que un entero salga "2" y no "2,0" -- que es lo
// que `eje()` hace hoy y hay que conservar.
export function marca(x, paso) {
  const d = Math.max(0, Math.ceil(-Math.log10(paso)));
  const p = Math.pow(10, d);
  return sinCeroNegativo(String(Math.round(x * p) / p).replace('.', ','));
}
```

**Por qué esta fórmula alcanza, y dónde no alcanzaría.** `paso()` de `dibujo.js` devuelve
siempre 1, 2 o 5 por una potencia de diez —nunca otra cosa—, y para esos nueve casos la
fórmula da exactamente los decimales que hacen falta. Verificado corriéndola:

```
paso   0.01  0.02  0.05  0.1  0.2  0.5  1  2  5  10
d         2     2     2    1    1    1  0  0  0   0
```

Un paso de `0.25` **rompería** la fórmula (daría 1 decimal y hace falta 2, así que
rotularía `0,3`), pero `paso()` no puede devolver 0.25. Si alguna vez se cambia `paso()`
para que elija otros escalones, esta función hay que revisarla — dejá eso escrito en el
comentario.

- [ ] **Paso 4: correr las pruebas**

Ejecutar: `node --test test/formato.test.js`
Esperado: PASAN las seis.

- [ ] **Paso 5: comprobar la equivalencia con lo que hay hoy**

Antes de que nadie use esto, hay que probar que `marca(x, paso)` reproduce **exactamente**
el rótulo actual de `eje()` para todo eje del sitio. La medición enumeró los 18 ejes y su
paso mínimo real: **0,1**, en ningún caso menor.

Escribí un script en el workspace que, para cada uno de esos 18 ejes, recorra sus marcas y
compare `String(Math.round(x * 10) / 10)` —lo de hoy— contra `marca(x, paso)` con la coma
revertida a punto. Tienen que coincidir en todos. Guardá la salida.

**Si alguno no coincide, paralo y decilo**: significa que la Tarea 4 va a cambiar rótulos
existentes, y eso hay que decidirlo, no descubrirlo.

- [ ] **Paso 6: correr la suite y commitear**

```bash
node --test "test/**/*.test.js"
git add docs/motor/formato.js test/formato.test.js
git commit -m "feat(motor): formato.js, un solo lugar donde un numero se vuelve texto"
```

---
## Fase B — los dos barridos sobre las nueve páginas

Las tareas 2 y 3 tocan los mismos nueve archivos. **No pueden ir en paralelo**, y van en
este orden a propósito: primero los estilos, que no tocan ningún número, y después los
números, que no tocan ningún estilo. Así cada barrido tiene un criterio de aceptación
limpio y un fallo se atribuye sin ambigüedad.

### Tarea 2: Las diez clases tipográficas

El plan anterior agregó nueve clases de layout y midió que los atributos `style` bajaban
de 391 a 303. Hoy son **587**, porque las cinco páginas nuevas trajeron 284 y lo que las
clases no cubren es justamente la tipografía. Con diez clases más se van **331** y quedan
**256**.

**Archivos:**
- Modificar: `docs/estilos/base.css` y las nueve páginas de `docs/`

**Interfaces:**
- Consume: las nueve clases de layout que ya existen (`.columna`, `.columna-final`,
  `.banda`, `.marco-widget`, `.encabezado-widget`, `.boton`, `.boton-primario`,
  `.control`, `.lecturas`) más la regla de elemento `canvas`.
- Produce: diez clases que la Guía 3 va a usar desde el principio.

- [ ] **Paso 1: capturar la referencia antes de tocar nada**

Idéntico al Paso 1 de la Tarea 2 del plan anterior, que funcionó: con `docs/` servido como
raíz, para las **nueve** páginas y a 1280 y 390 px, guardá fuera del repositorio el hash
del bitmap de cada canvas y el `getBoundingClientRect` + `getComputedStyle` completo de
todos los elementos del `<body>`.

Son 21 canvas y 9 páginas × 2 anchos = 18 capturas de layout. Guardalas como `t2-antes-*`.

- [ ] **Paso 2: escribir las diez clases**

Cada declaración es **copia textual** del atributo que reemplaza. No es una oportunidad
para mejorar valores: si el resultado difiere en un píxel, el refactor está mal.

```css
/* Las diez clases tipograficas. Salen de medir los 587 atributos `style` de las nueve
   paginas y quedarse con los diez valores mas repetidos que son tipografia y no layout
   (la medicion completa, con el conteo de los 60 valores distintos, esta en
   .superpowers/investigacion-deuda/medicion.md). Cada declaracion es copia textual del
   atributo que reemplaza. */

.lectura-valor { color: var(--ink); font-weight: 500; font-variant-numeric: tabular-nums; }
.lectura-valor.roja { color: var(--red); }
.lectura-valor.azul { color: var(--blue); }
.lectura-valor.tenue { color: var(--dim); }

/* Hermana de .lectura-valor y NO un modificador suyo: el eco en vivo del valor de un
   slider vive en un <output> y va sin negrita; el resultado final vive en un <b> y va
   con negrita. Son dos componentes distintos a proposito, verificado en las ocho
   paginas con widgets. Fusionarlos pondria en negrita los ecos o se la sacaria a los
   resultados -- un cambio visual real. */
.valor-control { color: var(--ink); font-variant-numeric: tabular-nums; }

.parrafo { font: 400 19px/1.62 'Source Serif 4', Georgia, serif; margin: 18px 0 0; text-wrap: pretty; }
.parrafo-suelto { font: 400 19px/1.62 'Source Serif 4', Georgia, serif; margin: 30px 0 0; text-wrap: pretty; }

.titulo-seccion { font: 600 13px/1 'JetBrains Mono', monospace; letter-spacing: .14em; text-transform: uppercase; color: var(--dim); margin: 52px 0 0; }

/* .rotulo-mono titula el widget ("Simulacion 1"); .rotulo-campo etiqueta un control.
   Difieren solo en letter-spacing (.14em vs .1em) y tampoco es descuido: la distincion
   es consistente en las ocho paginas. Dos roles, dos clases. */
.rotulo-mono { font: 500 10.5px/1 'JetBrains Mono', monospace; letter-spacing: .14em; text-transform: uppercase; color: var(--dim); }
.rotulo-campo { font: 500 10.5px/1 'JetBrains Mono', monospace; letter-spacing: .1em; text-transform: uppercase; color: var(--dim); }

.titulo-fila { font: 600 15px/1.2 'Source Serif 4', Georgia, serif; }
.nota-fila { font: 400 13px/1.3 'Source Serif 4', Georgia, serif; color: var(--dim); }

.negrita { font-weight: 600; }
```

- [ ] **Paso 3: aplicarlas, con una trampa que hay que respetar**

Reemplazá el atributo por la clase **sólo donde el valor coincida exactamente**.

**La trampa está en el margen de los párrafos.** El mismo párrafo aparece con cinco
valores de `margin-top`: 18px (40 veces), 30px (27), 22px (15), 26px (1) y 24px (1).
`.parrafo` cubre el de 18 y `.parrafo-suelto` el de 30. Los otros tres valores **no
inventan una clase nueva**: llevan la clase `.parrafo` más su propio `margin-top` en el
atributo, que es lo mismo que el plan anterior hizo con `flex:1 1 200px` sobre `.control`.

Si te encontrás normalizando un 22px a 18px «porque casi es lo mismo», pará: eso mueve
píxeles y este refactor no puede mover ninguno.

Donde un elemento tenga la clase más algo propio —un `color` distinto, un `margin` de
cola—, dejá la clase y conservá lo propio en el atributo.

**No se tocan** en esta tarea: el script bloqueante del `<head>`, los números (son de la
Tarea 3), y el `<canvas>`.

- [ ] **Paso 4: verificar que no se movió nada**

Repetí las dos mediciones del Paso 1 y compará.

- Los 21 hashes de canvas: **idénticos**, con el control negativo corrido.
- Los `rect` y `getComputedStyle` de las 18 capturas: **sin diferencias**, salvo las de
  `box-shadow` de los botones que pulsan, que son ruido de muestreo de una animación en
  vivo y ya están caracterizadas — si aparecen, medí el mismo árbol dos veces para
  confirmarlo, como hizo el plan anterior, y guardá ese control.

**Si aparece cualquier otra diferencia, paralo y decilo** con el elemento y los dos
valores.

- [ ] **Paso 5: contar**

Reportá el conteo de atributos `style` antes y después, por página. Esperado: 587 → 256.
Si te da otro número, decilo — no lo fuerces.

- [ ] **Paso 6: correr la suite y commitear**

```bash
node --test "test/**/*.test.js"
git add docs/estilos/base.css docs/index.html docs/ensayos docs/ejemplos
git commit -m "refactor(plataforma): diez clases tipograficas, 587 atributos style a 256"
```

---

### Tarea 3: La coma, en las nueve páginas

**Archivos:**
- Modificar: las nueve páginas de `docs/`

**Interfaces:**
- Consume: `num`, `exp` y `marca` de `docs/motor/formato.js` (Tarea 1).
- Produce: un sitio con una sola convención de números.

Dos poblaciones, y necesitan tratamientos distintos.

- [ ] **Paso 1: las lecturas de widget — 117 sitios**

Están enumeradas por archivo en `.superpowers/investigacion-deuda/medicion.md`, sección
2.2. Son 115 `toFixed`/`toExponential` en las ocho páginas con widgets, más dos
`String(Math.round(...))` en `dibujo.js` que **no** son tuyos: ésos los hace la Tarea 4.

Cada `x.toFixed(d)` pasa a `num(x, d)`. Cada `x.toExponential(d)` pasa a `exp(x, d)` —
y fijate en el resultado, porque hoy `fuerzas-de-posicion.html` imprime `1.0808e-2` crudo
en pantalla y con `exp` va a decir `1,0808 × 10⁻²`. Eso **no** es un cambio accidental,
es el arreglo de una fealdad que estaba en producción; anotalo en el informe.

Agregá el `import` de `formato.js` a las ocho páginas.

- [ ] **Paso 2: la prosa — cinco páginas**

`derivada-integral`, `movimiento-circular`, `tiro-parabolico`, `auto-y-camion` y
`la-tierra` escriben la prosa con punto: 93 números entre las cinco. Pasan a coma.

Las otras tres (`cuerpo-aislado`, `fuerzas-de-posicion`, `sistemas-acoplados`) ya la
tienen y no se tocan.

- [ ] **Paso 3: los puntos que NO son decimales**

Éste es el paso donde un reemplazo entusiasta rompe el sitio. **No se tocan**, y la
medición los enumera en la sección 2.3:

- los 53 `import ... from '../motor/x.js'` y cualquier otra ruta de archivo;
- los literales numéricos **dentro** del JS — `0.5`, `1e-9`, `Math.PI / 6`. Sólo se
  formatea la **salida**, nunca la fuente;
- las proporciones y relaciones que se escriben con punto o barra en la prosa
  (`aspect-ratio:16/8`, versiones, `ej. 11, 12, 14`);
- los `style` con valores decimales (`letter-spacing:.14em`, `font:400 19px/1.62`).

Trabajá sitio por sitio, no con un reemplazo global. Si usás un script, que liste lo que
va a cambiar y revisalo antes de aplicarlo.

- [ ] **Paso 4: verificar**

1. Con `docs/` servido como raíz, a 1280 y 390 px, en los dos temas: **ningún número
   visible en pantalla usa punto como separador decimal**, en ninguna de las nueve
   páginas. Comprobalo extrayendo el texto visible con el protocolo DevTools y buscando
   `\d\.\d`, no a ojo. Guardá el volcado.
2. Ningún error de consola en ninguna página. Un `import` roto por un reemplazo se ve acá.
3. Las 21 canvas siguen pintando (bitmap no uniforme). Los **rótulos de eje todavía usan
   punto** en esta tarea: los arregla la Tarea 4. Anotalo para que no parezca un olvido.
4. Las lecturas que tienen que dar cero siguen diciendo cero y no «menos cero»: la
   resultante del ensayo 4, la diferencia de tensiones del 5, y `a + ω²(x−x₀)` del 6.

- [ ] **Paso 5: correr la suite y commitear**

```bash
node --test "test/**/*.test.js"
git add docs
git commit -m "refactor(plataforma): coma decimal en las nueve paginas"
```

---

## Fase C — los dos defectos parqueados del motor

### Tarea 4: `eje()` — los decimales salen del paso

`eje()` rotula sus marcas con `String(Math.round(x * 10) / 10)`: un decimal fijo, mientras
`paso()` puede elegir un escalón más fino. Con paso 0,05 eso da **rótulos repetidos** —
«0,3» dos veces seguidas. Hoy no se ve en ninguna página porque `fuerzas-de-posicion.html`
esquiva el problema ensanchando sus paneles a propósito, con el comentario que lo explica.

**Archivos:**
- Modificar: `docs/motor/dibujo.js`
- Prueba: `test/dibujo.test.js`

**Interfaces:**
- Consume: `marca(x, paso)` de `formato.js`.
- Produce: `eje()` con rótulos correctos a cualquier paso, y con coma.

- [ ] **Paso 1: escribir las pruebas que fallan**

```js
test('eje rotula con coma', () => {
  const l = crearLienzo({ ancho: 400, alto: 200, xMin: 0, xMax: 2, yMin: 0, yMax: 1 });
  const c = ctxFalso();
  eje(c, l, { color: '#000', colorTexto: '#666' });
  const rotulos = c.ops.filter(o => o[0] === 'fillText').map(o => o[1]);
  assert.ok(rotulos.some(r => r.includes(',')), 'algun rotulo decimal lleva coma');
  assert.ok(!rotulos.some(r => r.includes('.')), 'ninguno lleva punto');
});

test('eje no repite rotulos cuando el paso es fino', () => {
  // Rango angosto: paso 0.05, que con un decimal fijo daba "0,3" dos veces.
  const l = crearLienzo({ ancho: 400, alto: 200, xMin: 0.25, xMax: 0.55, yMin: 0, yMax: 1 });
  const c = ctxFalso();
  eje(c, l, { color: '#000', colorTexto: '#666' });
  const rotulos = c.ops.filter(o => o[0] === 'fillText').map(o => o[1]);
  assert.equal(new Set(rotulos).size, rotulos.length, 'no hay rotulos repetidos');
});

test('eje sigue rotulando los enteros sin decimales', () => {
  // El comportamiento de HOY, que no puede cambiar: con paso 0.5 el -1 se rotula "-1",
  // no "-1,0". Es la unica forma de que las paginas existentes no se muevan.
  const l = crearLienzo({ ancho: 400, alto: 400, xMin: -2, xMax: 2, yMin: -2, yMax: 2 });
  const c = ctxFalso();
  eje(c, l, { color: '#000', colorTexto: '#666' });
  const rotulos = c.ops.filter(o => o[0] === 'fillText').map(o => o[1]);
  assert.ok(rotulos.includes('-1'), 'el -1 va sin decimales');
  assert.ok(!rotulos.includes('-1,0'), 'y no con un cero de mas');
});
```

- [ ] **Paso 2: correrlas y verificar que fallan**

Ejecutar: `node --test test/dibujo.test.js`
Esperado: FALLAN la primera y la segunda. **La tercera PASA desde el arranque**: fija el
comportamiento actual, y tiene que seguir pasando cuando termines. Si falla al final,
rompiste las páginas existentes.

- [ ] **Paso 3: implementar**

En `eje()`, las dos llamadas a `String(Math.round(x * 10) / 10)` pasan a `marca(x, paso)`,
donde `paso` es el que esa función ya calculó para ese eje. Importá `marca` de
`formato.js`. Dejá un comentario diciendo por qué los decimales salen del paso.

- [ ] **Paso 4: verificar que ningún rótulo existente cambió**

La Tarea 1 dejó un script que compara los 18 ejes del sitio. Corrélo de nuevo, ahora
contra el `eje()` real, y además comparé bitmaps de las **21 canvas**: los rótulos de eje
cambian de punto a coma, así que **los canvas con eje rotulado van a cambiar**, y ése es
el único cambio admisible. Para cada canvas que cambie, comprobá que la diferencia sean
sólo los rótulos y no la posición de un eje o una curva — recortá la zona del rótulo y
mirala.

Control negativo: mutá algo **dentro de `eje()`** y comprobá que el método detecta.

- [ ] **Paso 5: correr la suite y commitear**

```bash
node --test "test/**/*.test.js"
git add docs/motor/dibujo.js test/dibujo.test.js
git commit -m "fix(motor): eje() saca los decimales del paso y rotula con coma"
```

---
### Tarea 5: `colocarEtiqueta` — que un rótulo no se salga ni pise a otro

A 390 px los rótulos se pisan cuando dos cuerpos se acercan, y se cortan cuando el cuerpo
llega al borde. La medición enumeró **18 sitios** que rotulan un cuerpo en movimiento —10
directos y 8 a través del `rotulo` de `vectorPx`— y el peor caso son los tres widgets de
fuerzas de `cuerpo-aislado`, que dibujan **cinco rótulos desde un mismo punto**.

El patrón de fondo es siempre el mismo: un desplazamiento fijo en píxeles que no sabe nada
del ancho del canvas ni de los otros rótulos.

**Archivos:**
- Crear: `docs/motor/etiqueta.js`
- Modificar: `docs/motor/dibujo.js` (que `vectorPx` y `arco` usen la función nueva)
- Prueba: `test/etiqueta.test.js` (nuevo)

**Interfaces:**
- Produce: `colocarEtiqueta(ctx, texto, x, y, { dx, dy, color, px, peso, limites })` y
  `reiniciarEtiquetas(limites)`.

- [ ] **Paso 1: el diseño, antes de escribir nada**

Dos cosas que la medición dejó claras y que gobiernan el diseño:

**(a) Evitar colisiones exige conocer los otros rótulos del mismo cuadro.** No alcanza con
una función sin memoria: cuando `cuerpo-aislado` dibuja cinco flechas desde un punto, cada
rótulo tiene que esquivar a los cuatro anteriores. Entonces `etiqueta.js` lleva un registro
de los rectángulos ya colocados en este repintado, y `reiniciarEtiquetas` lo limpia al
empezar cada cuadro.

Decidí **dónde se llama a `reiniciarEtiquetas`** y dejalo escrito: el lugar natural es
`crearWidget`, que ya envuelve el `dibujar` de cada widget y conoce el tamaño del canvas.
Si lo ponés ahí, ninguna página tiene que acordarse de llamarlo — y eso es lo que hace que
el arreglo no se pudra con el tiempo.

**(b) Hay una convergencia que es intencional y no se debe «arreglar».** En
`derivada-integral.html`, el rótulo `Q` se acerca a `P` porque el ejercicio pide
justamente arrastrar Q hasta P para ver la secante volverse tangente. Si la función
empuja `Q` lejos para no pisar a `P`, rompe la lección.

Resolvelo con una salida explícita —una opción tipo `evitar: false` en ese sitio— y no
con un caso especial escondido dentro de la función. Dejá el porqué en un comentario en
el sitio que la usa, no sólo en el motor.

- [ ] **Paso 2: escribir las pruebas que fallan**

```js
test('una etiqueta sola va donde le dicen', () => {
  reiniciarEtiquetas({ ancho: 400, alto: 200 });
  const c = ctxFalso();
  colocarEtiqueta(c, 'v', 100, 100, { dx: 8, dy: -6, color: '#000' });
  const t = c.ops.find(o => o[0] === 'fillText');
  assert.equal(t[2], 108);
  assert.equal(t[3], 94);
});

test('una etiqueta contra el borde derecho entra en el canvas', () => {
  reiniciarEtiquetas({ ancho: 400, alto: 200 });
  const c = ctxFalso();
  colocarEtiqueta(c, 'se alcanzan', 396, 100, { dx: 8, dy: -6, color: '#000' });
  const t = c.ops.find(o => o[0] === 'fillText');
  const ancho = c.medirTexto('se alcanzan');
  assert.ok(t[2] + ancho <= 400, 'no se sale por la derecha');
  assert.ok(t[2] >= 0, 'ni por la izquierda');
});

test('dos etiquetas en el mismo punto no se superponen', () => {
  reiniciarEtiquetas({ ancho: 400, alto: 200 });
  const c = ctxFalso();
  colocarEtiqueta(c, 'auto', 200, 100, { dx: 8, dy: -6, color: '#000' });
  colocarEtiqueta(c, 'camion', 200, 100, { dx: 8, dy: -6, color: '#000' });
  const ts = c.ops.filter(o => o[0] === 'fillText');
  assert.equal(ts.length, 2);
  const [a, b] = ts;
  const altoLinea = 12;
  const seSolapan = Math.abs(a[3] - b[3]) < altoLinea &&
    Math.abs(a[2] - b[2]) < Math.max(c.medirTexto(a[1]), c.medirTexto(b[1]));
  assert.ok(!seSolapan, 'la segunda se corrio');
});

test('cinco etiquetas desde un punto caen las cinco dentro y sin pisarse', () => {
  // Es el peor caso real del sitio: las cuatro fuerzas mas la resultante del
  // widget 1 de cuerpo-aislado, todas naciendo del mismo bloque.
  reiniciarEtiquetas({ ancho: 400, alto: 200 });
  const c = ctxFalso();
  for (const s of ['P', 'N', 'T', 'Q', 'R']) {
    colocarEtiqueta(c, s, 200, 100, { dx: 8, dy: -6, color: '#000' });
  }
  const ts = c.ops.filter(o => o[0] === 'fillText');
  assert.equal(ts.length, 5);
  for (const t of ts) {
    assert.ok(t[2] >= 0 && t[2] + c.medirTexto(t[1]) <= 400, `${t[1]} entra a lo ancho`);
    assert.ok(t[3] >= 0 && t[3] <= 200, `${t[1]} entra a lo alto`);
  }
  for (let i = 0; i < 5; i++) for (let j = i + 1; j < 5; j++) {
    const solapan = Math.abs(ts[i][3] - ts[j][3]) < 12 &&
      Math.abs(ts[i][2] - ts[j][2]) < c.medirTexto(ts[i][1]);
    assert.ok(!solapan, `${ts[i][1]} y ${ts[j][1]} no se pisan`);
  }
});

test('con evitar:false la etiqueta se queda donde le dicen aunque pise', () => {
  // La convergencia de Q sobre P en derivada-integral es el punto del ejercicio.
  reiniciarEtiquetas({ ancho: 400, alto: 200 });
  const c = ctxFalso();
  colocarEtiqueta(c, 'P', 200, 100, { dx: 8, dy: -6, color: '#000' });
  colocarEtiqueta(c, 'Q', 200, 100, { dx: 8, dy: -6, color: '#000', evitar: false });
  const ts = c.ops.filter(o => o[0] === 'fillText');
  assert.equal(ts[0][2], ts[1][2]);
  assert.equal(ts[0][3], ts[1][3]);
});
```

`ctxFalso` tiene que saber medir texto para estas pruebas. Mirá cómo lo arma
`test/dibujo.test.js` y extendelo con un `measureText` que devuelva un ancho proporcional
al largo de la cadena — no hace falta métrica real, hace falta que sea consistente.

- [ ] **Paso 3: correrlas y verificar que fallan**

Ejecutar: `node --test test/etiqueta.test.js`
Esperado: FALLAN las cinco.

- [ ] **Paso 4: implementar**

El algoritmo mínimo que pasa esas pruebas: probar la posición pedida; si se sale del
canvas, espejar el desplazamiento hacia adentro; si pisa un rectángulo ya colocado,
probar posiciones alternativas alrededor del punto —arriba, abajo, izquierda, derecha, y
las diagonales— y quedarse con la primera libre; si ninguna está libre, usar la pedida y
seguir, porque un rótulo mal puesto es mejor que ninguno.

Registrá el rectángulo elegido. Con `evitar: false`, saltá la búsqueda pero registrá igual.

- [ ] **Paso 5: migrar los 18 sitios**

`vectorPx` y `arco` pasan a usar `colocarEtiqueta` internamente, con lo que los ocho
sitios que rotulan a través de ellos quedan migrados sin tocarlos. Los diez directos se
cambian uno por uno.

El de `derivada-integral` va con `evitar: false` y su comentario.

- [ ] **Paso 6: verificar con los ojos, que es lo único que sirve acá**

Las pruebas fijan la geometría; que se lea bien es otra cosa.

Con `docs/` servido como raíz, a **390 px** —el ancho donde el problema aparece— capturá
los casos que la medición nombró como peores y mirá los bitmaps:

1. `auto-y-camion`, los rótulos `auto` y `camión` al arrancar y cerca del cruce.
2. `auto-y-camion`, el rótulo `se alcanzan` cuando el encuentro cae alto en el gráfico.
3. `la-tierra`, el rótulo `sin gravedad` en los dos extremos del deslizador.
4. Los tres widgets de fuerzas de `cuerpo-aislado`, barriendo el ángulo, con sus cinco
   rótulos.
5. `movimiento-circular`, widget 1, con el punto dando la vuelta entera.

Guardá las capturas. **Ningún rótulo cortado por el borde, ninguno ilegible por
superposición**, y en `derivada-integral` la `Q` tiene que seguir acercándose a la `P`.

Y comparé bitmaps de las 21 canvas: **muchas van a cambiar**, porque los rótulos se
mueven. Eso es lo esperado. Para cada una que cambie, confirmá que lo que se movió son
rótulos y no geometría.

- [ ] **Paso 7: correr la suite y commitear**

```bash
node --test "test/**/*.test.js"
git add docs/motor test
git commit -m "feat(motor): colocarEtiqueta, rotulos que no se salen ni se pisan"
```

---

## Fase D — cerrar

### Tarea 6: El ejercicio que faltaba, las decisiones por escrito, y el recorrido

**Archivos:**
- Modificar: `docs/ensayos/sistemas-acoplados.html`, `README.md`
- Crear: `docs/plataforma/decisiones.md`

- [ ] **Paso 1: la frase del ejercicio 2**

El ejercicio 2 de la Guía 2 —un bloque de 10 kg sobre una superficie lisa, tirado con 20 N
por una soga sin masa, `a = 2 m/s²`, del bloque «Ej 2 y 3» de
`../Ejercicios-prácticos/parcial-1/soluciones/verificacion-practico-2.py`— **no está
tratado en ninguna página del sitio**. La tabla de cobertura del plan anterior decía que
sí; era falso, y el pie de la página declara hoy la cobertura real.

Su lugar natural es la sección 01 de `sistemas-acoplados`, que ya habla de la cuerda sin
masa y ya trata el ejercicio 3. La medición dejó una propuesta de redacción en
`.superpowers/investigacion-deuda/medicion.md`, sección 5, con el lugar exacto.

Escribila en la voz del ensayo, con el número saliendo del script. Y actualizá el pie de
esa página y su fila en el README para que digan `ej. 2, 3, 4, 5 y 7`.

- [ ] **Paso 2: las decisiones del dueño, por escrito y versionadas**

Creá `docs/plataforma/decisiones.md` con las dos decisiones, su fecha y su porqué:

1. **Separador decimal: coma en todo el sitio**, prosa y lecturas. El problema no era la
   elección sino la mezcla: las frases de «qué mirar» piden contrastar la lectura contra
   el párrafo.
2. **El rojo de `auto-y-camion.html` se queda** — la única excepción registrada al
   reparto semántico. Ahí el rojo distingue un cuerpo y no una magnitud, y el dueño
   decidió que el contraste rojo/azul separa los dos móviles mejor que dos azules. **No es
   deriva y no se «arregla» en una limpieza futura.** Cualquier otra página que quiera
   rojo para algo que no sea aceleración o fuerza tiene que preguntar.

   La excepción cubre **toda** la página, no sólo el punto del camión: su rótulo, su curva
   de posición en el gráfico, y la lectura de `separación`, que es una distancia y va en
   rojo por la misma razón. Nombralas las cuatro, con su línea, para que quede claro qué
   entra en la excepción y qué no — una revisión futura va a encontrar cada una por
   separado y tiene que poder confirmar de un vistazo que están adentro.

Enlazalo desde el README, y agregá a `docs/plataforma/brief.md` una línea que lo apunte:
el brief es la autoridad y tiene que saber dónde viven las decisiones posteriores.

- [ ] **Paso 3: el recorrido completo**

El mismo de la Tarea 16 del plan anterior, que funcionó: `docs/` servido como raíz, Chrome
fresco, las 9 páginas × 2 anchos × 2 temas, con los seis chequeos —sin 404 incluidos todos
los PDF, sin errores de consola, sin desborde horizontal medido con `scrollWidth`, ningún
widget animándose solo, las 21 canvas con bitmap no uniforme, y el tema sobreviviendo la
navegación.

Más dos propios de este plan:

7. **Ningún número visible usa punto como separador decimal**, en ninguna página, ancho ni
   tema. Extraé el texto visible y buscá `\d\.\d`.
8. **Ningún rótulo cortado por el borde** a 390 px en los cinco casos de la Tarea 5.

Tabla, página por página. «Recorrí todo y anda» sin la tabla no es una verificación.

- [ ] **Paso 4: commit**

```bash
node --test "test/**/*.test.js"
git add docs README.md
git commit -m "docs(plataforma): ejercicio 2, decisiones del dueno y recorrido final"
```
