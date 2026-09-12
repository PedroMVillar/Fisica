# Plataforma interactiva de Física 1 — especificación

Especificación de la plataforma: qué se construye, qué contenido lleva, de dónde sale
la información y con qué sistema visual se arma.

El diseño está **cerrado** (sección 6) y su fuente de verdad es
`docs/plataforma/diseno/Tiro parabolico.dc.html`. La implementación lo sigue al pie de
la letra: no inventa colores, tamaños ni espaciados.

Las decisiones del dueño que se toman después de este brief —y que no ameritan
reabrirlo— viven, con su fecha y su porqué, en
[`docs/plataforma/decisiones.md`](decisiones.md).

Fecha: 2026-09-11 · Parcial I: 2026-09-24

---

## 1. Qué es

Un sitio estático con **seis ensayos**, uno por concepto. Cada ensayo es una página
larga que se lee scrolleando, con **simulaciones interactivas incrustadas cada pocos
párrafos**. El texto y el widget se necesitan mutuamente: el texto dice qué mover, el
widget muestra qué pasa, y el párrafo siguiente explica por qué.

El modelo es [ciechanow.ski](https://ciechanow.ski/). No es un simulador con texto al
costado ni un apunte con animaciones decorativas: es una explicación donde la
interacción **es** el argumento.

### Para qué existe

Para construir intuición la primera vez que se enfrenta un concepto. Ese es su único
trabajo, y es lo que ni el apunte ni las hojas resumen hacen bien.

Convive con dos cosas que ya existen y que **no** reemplaza:

| Artefacto | Función | Cuándo se usa |
|---|---|---|
| Apunte (`sintesis/fisica-1/`, 108 pp.) | Referencia formal y completa, con deducciones | Cuando hace falta el detalle o la demostración |
| Hojas resumen (`parcial-1/preparacion/`) | Repaso rápido, papel, al lado del ejercicio | Mientras resolvés, y la noche anterior |
| **Ensayos web** | **Construir la intuición** | **La primera vez que el concepto no cierra** |

La duplicación es deliberada. El costo asumido es que una corrección conceptual hay
que propagarla a mano a los tres.

### Para quién

Un solo lector: alguien que ya leyó el tema y no lo terminó de entender. No es
material de divulgación ni de primer contacto. Puede asumir que el lector sabe qué es
una derivada, conoce la notación de la cátedra y está por rendir.

---

## 2. Los seis ensayos

El criterio de selección fue estricto: **sólo entran conceptos donde mover un
parámetro enseña algo que una figura estática no puede**. Si un tema se entiende bien
con un dibujo fijo, se queda en la hoja resumen.

Cada ensayo tiene una **idea central** — la única cosa que el lector tiene que
llevarse. Todo lo demás está al servicio de eso.

---

### Ensayo 1 — Derivada e integral, vistas

> **Idea central:** la velocidad es la pendiente y el desplazamiento es el área.
> Las dos son la misma relación leída en dos direcciones.

Es el más importante de los seis. El capítulo 1 del apunte construye el cálculo desde
cero porque sin eso la mitad de la Guía 1 no se puede resolver, y es exactamente el
tipo de contenido donde ver la construcción vale más que leerla.

**Cubre:** Guía 1, ejercicios 1 a 8.
**Fuente principal:** apunte, capítulo 1 (pp. 3–24), 14 bloques teóricos.

**Widgets:**

1. **De la secante a la tangente.** Una curva $x(t)$ y un punto $P$ fijo. Un slider
   controla $\Delta t$. Al achicarlo, el segundo punto se acerca y la secante gira
   hasta apoyarse en la tangente. El número $\Delta x/\Delta t$ se actualiza y
   converge. *Lo que enseña:* que el límite es un proceso, no una notación.

2. **Los tres paneles sincronizados.** $x(t)$, $v(t)$ y $a(t)$ apilados con el eje
   temporal alineado y un cursor vertical compartido. Arrastrás el cursor y los tres
   se leen juntos. *Lo que enseña:* que un máximo en $x$ es un cero en $v$, y que la
   concavidad de $x$ es el signo de $a$.

3. **Dibujá tu $x(t)$.** El lector traza una curva con el mouse y abajo aparecen
   $v(t)$ y $a(t)$ calculadas en vivo. *Lo que enseña:* más que ningún otro. Es el
   widget que convierte la relación en algo que se siente. También es el más difícil
   de implementar bien (suavizado, derivada numérica estable).

4. **El área es el desplazamiento.** Un $v(t)$ cualquiera; al arrastrar $t$ se va
   pintando el área bajo la curva y un contador muestra $\Delta x$. Con $v$ negativa
   el área se pinta de otro color y resta. *Lo que enseña:* por qué desplazamiento y
   camino recorrido no son lo mismo.

---

### Ensayo 2 — Tiro parabólico

> **Idea central:** son dos movimientos independientes que sólo comparten el reloj.

**Cubre:** Guía 1, ejercicios 9, 10 y 15.
**Fuentes:** apunte cap. 2 (pp. 25–47); hoja `resumen-tiro-parabolico.pdf`;
`practico-1-cinematica.pdf` ej. 9, 10, 15; prototipo existente
`parcial-1/preparacion/tiro-parabolico.html`.

**Widgets:**

1. **Las dos sombras.** El proyectil vuela y sobre cada eje se mueve su proyección.
   La sombra horizontal avanza con paso constante; la vertical frena, se detiene y
   vuelve. *Lo que enseña:* la independencia, que es toda la idea del tema. Es el
   widget insignia del ensayo.

2. **Galileo.** Dos cuerpos lado a lado: uno lanzado horizontalmente, otro soltado
   desde la misma altura. Caen sincronizados, con líneas punteadas uniendo las
   alturas iguales. *Lo que enseña:* que la componente horizontal no afecta a la
   vertical. Es contraintuitivo hasta que se ve.

3. **El triángulo de $\vec v_0$.** Arrastrás la punta del vector y se actualizan
   $v_0\cos\alpha$ y $v_0\sen\alpha$. Un toggle cambia el ángulo de medirse desde la
   horizontal a desde la vertical, y seno y coseno se intercambian. *Lo que enseña:*
   de dónde sale el seno, que es la Duda 3 del archivo de dudas.

4. **Con viento.** Un slider agrega $a_x$. La trayectoria deja de ser simétrica y el
   vértice se corre. El eje $y$ no cambia. *Lo que enseña:* el ejercicio 15, y de
   paso refuerza la independencia por contraste.

---

### Ensayo 3 — Movimiento circular

> **Idea central:** la aceleración tiene dos trabajos distintos, y sólo uno de ellos
> cambia la rapidez.

**Cubre:** Guía 1, ejercicios 11 a 14.
**Fuentes:** apunte cap. 2 (pp. 25–47), que es donde vive la cinemática del
movimiento circular; el cap. 6 (pp. 96–108) es la *dinámica* del mismo tema y
corresponde a la Guía 2, no a este ensayo. Hoja
`resumen-movimiento-circular.pdf`; `practico-1-cinematica.pdf` ej. 11–14.

**Widgets:**

1. **Los versores que giran.** Una partícula recorre la circunferencia con $\hat r$ y
   $\hat\theta$ dibujados y rotando con ella, más $\vec v$ tangente. *Lo que enseña:*
   que $\vec r \perp \vec v$ siempre, y por qué.

2. **$a_t$ y $a_n$.** Sliders de $\omega$ y $\gamma$. Con $\gamma=0$ la aceleración
   apunta exactamente al centro; al subir $\gamma$ se inclina hacia adelante. Un
   indicador muestra el ángulo entre $\vec v$ y $\vec a$. *Lo que enseña:* que
   $\vec v \perp \vec a$ sólo en el MCU — los incisos (d) y (e) del ejercicio 11.

3. **De las ecuaciones al círculo.** Dos campos de texto con $x(t)$ e $y(t)$; abajo,
   la trayectoria que generan. Viene precargado con el ejercicio 14
   ($x=\sen\omega t$, $y=\cos\omega t+1$). *Lo que enseña:* a reconocer una
   circunferencia escrita en paramétricas.

4. **Período y frecuencia.** Dos partículas con $\omega$ distinta girando a la par,
   con sus períodos marcados en una línea de tiempo. *Lo que enseña:* qué miden $T$ y
   $f$, que es el inciso (c) del ejercicio 11.

---

### Ensayo 4 — Diagrama de cuerpo aislado

> **Idea central:** casi todo el problema se decide antes de escribir la primera
> ecuación.

**Cubre:** Guía 2, ejercicios 1 a 4, 6, 8, 9 y 10.
**Fuentes:** apunte cap. 3 (pp. 48–60) y cap. 4 (pp. 61–77); hojas
`resumen-cuerpo-aislado.pdf` y `resumen-rozamiento.pdf`;
`practico-2-dinamica.pdf`.

**Widgets:**

1. **El plano inclinado vivo.** Un slider de $\alpha$. Al moverlo, el bloque rota, el
   peso se mantiene vertical y sus dos componentes cambian de largo; $N$ y $f$ se
   ajustan. Los valores numéricos se leen al costado. *Lo que enseña:* que el ángulo
   del plano reaparece entre el peso y la normal, y que $N \ne mg$.

2. **Armá el diagrama.** Una situación dibujada y una lista de fuerzas candidatas,
   algunas reales y otras no (la "fuerza del movimiento", la centrífuga). El lector
   elige cuáles van y el widget le dice cuáles sobran o faltan, con el motivo. *Lo
   que enseña:* el error más caro de la guía, por la vía de cometerlo sin costo.

3. **El roce, los dos regímenes.** Un slider de fuerza aplicada. Mientras no desliza,
   la flecha de roce crece igualando a la aplicada; al pasar $\mu_e N$ el bloque
   arranca y el roce cae a $\mu_d N$. En paralelo se dibuja la curva $f$ contra $F$.
   *Lo que enseña:* que el estático es una desigualdad, no una fórmula.

---

### Ensayo 5 — Sistemas acoplados

> **Idea central:** la cuerda es una ecuación, no un objeto.

**Cubre:** Guía 2, ejercicios 4, 5, 7, 10 y 19.
**Fuentes:** apunte cap. 4 (pp. 61–77); hoja `resumen-sistemas-acoplados.pdf`;
`practico-2-dinamica.pdf`.

**Widgets:**

1. **Dos cuerpos, dos diagramas.** El sistema de bloque sobre mesa más colgante con
   polea. A los costados, los dos diagramas de cuerpo aislado dibujados en vivo. Al
   mover las masas cambian $a$ y $T$, y las flechas de los dos diagramas se
   reescalan a la vez. *Lo que enseña:* que la misma $T$ aparece en los dos con
   sentidos opuestos.

2. **Los casos límite.** Presets que llevan el sistema a los bordes: $m_B \to 0$
   (no arranca), $m_A \to 0$ (caída libre), $\mu_A = \mu_B$ en el plano inclinado
   (la cuerda queda floja y $T=0$). *Lo que enseña:* a auditar un resultado
   simbólico mirando sus extremos.

---

### Ensayo 6 — Energía

> **Idea central:** la energía no se pierde de vista; cambia de casillero.

**Cubre:** Guía 3, ejercicios 1, 3, 4, 5, 7 y 8.
**Fuentes:** apunte cap. 5 (pp. 78–95); `practico-3-trabajo-energia.pdf`;
`verificacion-practico-3.py`.

**Widgets:**

1. **Las barras de energía.** Un cuerpo se mueve y al costado tres barras apiladas:
   cinética, potencial y disipada. Sin rozamiento, la suma es una línea horizontal
   que no se mueve; con rozamiento, la barra de disipada crece y se come a las otras.
   *Lo que enseña:* la conservación, vista como un trasvase.

2. **La montaña rusa.** El circuito del ejercicio 7 de la Guía 3, con las barras al
   costado y un slider de $v_0$. Por debajo de cierta velocidad el carro no pasa la
   segunda loma y vuelve. *Lo que enseña:* que la altura máxima alcanzable es una
   cuestión de energía y no de fuerza.

3. **El resorte.** Un cuerpo oscilando contra un resorte, con el intercambio entre
   cinética y elástica. Toggle de rozamiento para ver la amplitud caer.
   *Lo que enseña:* el ejercicio 4 de la Guía 3 y el enganche con el MAS.

---

## 3. Resumen del catálogo

| # | Ensayo | Widgets | Guía | Ejercicios que sirve |
|---|---|---|---|---|
| 1 | Derivada e integral, vistas | 4 | 1 | 1 a 8 |
| 2 | Tiro parabólico | 4 | 1 | 9, 10, 15 |
| 3 | Movimiento circular | 4 | 1 | 11 a 14 |
| 4 | Diagrama de cuerpo aislado | 3 | 2 | 1 a 4, 6, 8, 9, 10 |
| 5 | Sistemas acoplados | 2 | 2 | 4, 5, 7, 10, 19 |
| 6 | Energía | 3 | 3 | 1, 3, 4, 5, 7, 8 |

**Total: 6 ensayos, 20 widgets.**

Orden sugerido de construcción: 2 → 1 → 4 → 3 → 6 → 5. El ensayo 2 primero porque ya
hay un prototipo del que partir y porque valida el formato con el tema más visual; el
1 segundo porque es el más valioso; el 5 último porque es el más acotado.

---

## 4. Fuentes de información

Todo el contenido conceptual ya existe dentro del repositorio. No hay que investigar
nada desde cero.

| Fuente | Qué aporta | Dónde |
|---|---|---|
| Apunte propio | El texto base de los seis temas, ya pasado por control de calidad y con la notación de la cátedra | `sintesis/fisica-1/fisica-1.pdf` y `.tex` |
| Prácticos resueltos | Los ejemplos concretos y los números verificados | `parcial-1/soluciones/practico-{1,2,3}-*.pdf` |
| Scripts de verificación | Los valores numéricos de cada widget, ya chequeados con sympy | `parcial-1/soluciones/verificacion-*.py` |
| Hojas resumen | La selección de qué es lo importante y los errores típicos | `parcial-1/preparacion/resumen-*.pdf` |
| Apunte de cátedra | La versión oficial, para no contradecirla | `bibliografia/apunte-catedra/` |
| Sears & Zemansky | Referencia de figuras y de tratamiento visual | `bibliografia/bibliografia-extra/` |
| NotebookLM | Consultas puntuales; cuaderno "Fisica 1" ya cargado con todo lo anterior | CLI `notebooklm ask` |
| Archivo de dudas | Las confusiones reales que ya aparecieron | `parcial-1/preparacion/dudas-y-consultas.pdf` |

**Regla de oro para los números:** ningún valor aparece en un widget sin estar
respaldado por un script de verificación. Si un widget introduce un caso nuevo, se
agrega al script correspondiente antes de publicarlo.

---

## 5. Arquitectura técnica

Decidido: **vanilla, sin framework, sin build.**

- Un archivo `.html` por ensayo, más un `index.html` de portada.
- Un módulo compartido con el motor de escenas y uno de estilos.
- Publicación estática por GitHub Pages desde el mismo repositorio.
- Única dependencia externa: **KaTeX** por CDN, para las fórmulas.
- Dibujo con **canvas 2D**. Sin WebGL, sin 3D.

### El motor de escenas

Es la pieza que hace viables 20 widgets. Todo widget se arma con este vocabulario, así
que el diseño visual se define **una vez acá** y se propaga solo.

**Primitivas de dibujo disponibles:**

| Primitiva | Para qué |
|---|---|
| `eje` | Ejes con marcas, rótulos y unidades |
| `grilla` | Cuadrícula de fondo, opcional |
| `vector` | Flecha con punta, desde un punto, con rótulo |
| `cuerpo` | El móvil: punto, bloque o esfera |
| `trayectoria` | La curva que recorre |
| `traza` | Rastro histórico, con desvanecido |
| `angulo` | Arco acotado entre dos direcciones, con rótulo |
| `componentes` | Descomposición punteada de un vector en dos ejes |
| `suelo` | Superficie rayada |
| `resorte` | Zigzag entre dos puntos |
| `polea` | Círculo con cuerda |
| `barra` | Barra de magnitud, para las de energía |
| `cursor` | Línea vertical compartida entre paneles |

**Controles disponibles:**

| Control | Notas |
|---|---|
| Slider | Rótulo, mínimo, máximo, paso, unidad, valor actual visible |
| Toggle | Encendido/apagado, para agregar o quitar un efecto |
| Presets | Botones que cargan un escenario ("ejercicio 9", "sin rozamiento") |
| Transporte | Reproducir, pausar, reiniciar |
| Scrubber | Línea de tiempo arrastrable |
| Lectura | Valor numérico que se actualiza solo, no editable |
| Campo | Entrada de texto, sólo para el widget de ecuaciones paramétricas |

**Estados que todo widget puede tener:** en reposo (antes de tocarlo), reproduciendo,
pausado, y siendo arrastrado. Los cuatro necesitan verse distintos.

### Restricciones

- **Se lee en notebook**, y debería ser usable en celular. En pantalla angosta los
  controles pasan debajo del dibujo y el ancho del canvas se adapta.
- **Interacción por mouse y por teclado.** Los sliders tienen que responder a flechas.
- **Sin cuenta, sin servidor, sin persistencia.** Nada se guarda entre visitas, salvo
  quizás la preferencia de tema en el navegador.
- **Carga rápida.** Las tipografías se traen de Google Fonts por CDN, como en el
  diseño. Si más adelante hace falta que funcione sin conexión, se autoalojan sin
  tocar nada más.
- **Nada de animación automática al entrar.** Un widget que se mueve solo mientras se
  lee el texto distrae. Arrancan quietos, en un estado representativo.

---

## 6. Sistema de diseño — CERRADO

Definido en `docs/plataforma/diseno/Tiro parabolico.dc.html`, que es la **fuente de
verdad**. Los valores de abajo están transcriptos de ahí y **se siguen al pie de la
letra**: ninguna implementación inventa un color, un tamaño ni un espaciado que no
esté en esta sección.

Ante cualquier discrepancia entre este documento y el archivo de diseño, **manda el
archivo de diseño**.

### 6.1 Tokens de color

Nueve variables CSS, con modo claro y oscuro completos. El tema se conmuta con el
atributo `data-theme` en el elemento raíz.

| Token | Claro | Oscuro | Rol |
|---|---|---|---|
| `--paper` | `#fbfaf7` | `#131316` | fondo de página |
| `--band` | `#f2f0ea` | `#191a1e` | franja del widget |
| `--ink` | `#16151a` | `#eceae4` | texto principal |
| `--dim` | `#6a6760` | `#948f86` | texto secundario, rótulos, auxiliares |
| `--rule` | `#dcd8ce` | `#2e2f35` | filetes y bordes |
| `--blue` | `#1b4fd4` | `#7aa2ff` | acento, cinemática, velocidad |
| `--blue-soft` | `#8aa3e6` | `#3f5694` | acento suave, subrayado de enlaces |
| `--red` | `#c02a24` | `#ef5f52` | aceleración y fuerza |
| `--graph` | `#8e8a80` | `#6f6c66` | trazos de gráfico |

**Reparto semántico:** azul para cinemática y velocidad, rojo para aceleración y
fuerza. Es el mismo criterio que ya usan las hojas resumen impresas, así que el color
significa lo mismo en papel y en pantalla.

Reglas globales que van con los tokens:

- `html` y `body` con fondo `--paper`, texto `--ink`.
- Enlaces en `--blue` con `border-bottom: 1px solid var(--blue-soft)`, sin subrayado;
  en hover pasan a `--red` con el borde del mismo color.
- `input[type=range]` con `accent-color: var(--blue)` y fondo transparente.
- `button` siempre en JetBrains Mono.

### 6.2 Tipografía

Dos familias, traídas de Google Fonts:

- **Source Serif 4** (fallbacks `Charter`, `Georgia`, `serif`) para todo el contenido.
  Pesos 400 y 600, con itálica.
- **JetBrains Mono** (fallbacks `ui-monospace`, `monospace`) para toda la interfaz:
  rótulos de sección, etiquetas de control, botones y lecturas numéricas. Pesos 400 y
  500.

La regla es: **serif para lo que se lee, mono para lo que se opera.**

| Elemento | Estilo exacto |
|---|---|
| Kicker de portada | `500 11px/1` mono, tracking `.16em`, mayúsculas, `--dim` |
| H1 | `600 52px/1.05` serif, tracking `-.02em`, margen `18px 0 0` |
| Bajada | `400 20px/1.45` serif, `--dim`, margen `14px 0 0`, ancho máximo `36em` |
| H2 de sección | `600 13px/1` mono, tracking `.14em`, mayúsculas, `--dim`, margen `52px 0 0` |
| Párrafo | `400 19px/1.62` serif, `text-wrap: pretty` |
| Cita o aparte | `400 18px/1.7` serif, con barra `2px solid var(--rule)` a la izquierda y `padding: 4px 0 4px 20px` |

Los márgenes superiores de párrafo varían según la posición: `30px` después de la
bajada, `22px` entre párrafos corridos, `18px` después de un H2, `26px` después de un
aparte.

Los números usan `font-variant-numeric: tabular-nums` para que no bailen al cambiar.

### 6.3 Grilla

Dos anchos, y la diferencia entre ambos es lo que hace que el widget se lea como otra
cosa:

- **Columna de texto: `max-width: 680px`**, centrada, con `padding: 56px 24px 0` en el
  primer bloque y `0 24px` en los siguientes.
- **Widget: `max-width: 880px`**, dentro de una franja que ocupa el ancho completo.

### 6.4 Anatomía del widget

El widget **rompe la columna**. No lleva borde ni caja: se distingue por una franja a
todo el ancho de la ventana con fondo `--band` y un filete arriba y otro abajo.

```
section  width:100%; background:var(--band);
         border-top:1px solid var(--rule);
         border-bottom:1px solid var(--rule);
         padding:26px 20px 28px; margin:30px 0 0;
         display:flex; justify-content:center
  └ div  width:100%; max-width:880px;
         display:flex; flex-direction:column; gap:14px
```

Adentro, y en este orden:

**1. Encabezado de tres partes**, en una fila con `align-items: baseline` y `gap: 10px`
que envuelve en pantalla angosta:

- `SIMULACIÓN N` — `500 10.5px/1` mono, tracking `.14em`, mayúsculas, `--dim`
- El nombre — `600 15px/1.2` serif
- **Una frase que dice qué mirar** — `400 13px/1.3` serif, `--dim`, precedida de raya

Esa tercera parte no es decorativa: es la que evita que el lector scrollee de largo
sin entender qué tiene que observar. **Todo widget la lleva.**

**2. El canvas** — `width: 100%`, `aspect-ratio: 16/8`, `display: block`,
`touch-action: none`. Si el widget se arrastra, suma `cursor: grab`.

**3. Los controles, debajo del canvas**, en una fila con `flex-wrap: wrap`,
`gap: 20px` y `align-items: flex-end`, en este orden:

- **Transporte** primero, agrupado con `gap: 8px`:
  - *Reproducir*: `11px`, tracking `.08em`, mayúsculas, texto `--paper` sobre fondo
    `--blue`, sin borde, `border-radius: 2px`, `padding: 9px 16px`, `cursor: pointer`
  - *Reiniciar*: mismo tamaño, texto `--dim`, fondo transparente,
    `border: 1px solid var(--rule)`, `padding: 9px 13px`
- **Sliders**, cada uno un `<label>` en columna con `gap: 5px` y
  `flex: 1 1 170px; min-width: 150px`. La etiqueta es mono `500 10.5px/1`, tracking
  `.1em`, mayúsculas, `--dim`, y **contiene el valor actual** en un `<output>` con
  color `--ink` y `tabular-nums`.
- **Checkboxes**, `<label>` en fila con `gap: 8px`, misma tipografía de etiqueta,
  `accent-color: var(--blue)`.

**4. Pie de lecturas**, opcional: una fila con `border-top: 1px solid var(--rule)`,
`padding-top: 12px`, `gap: 0 26px`, en mono `400 12px/1.5` y color `--dim`. Es donde
van los valores derivados que no son controles.

### 6.5 Qué invita a tocar

Resuelto con una animación de pulso sobre el control:

```css
@keyframes tp-pulse{
  0%,100%{ box-shadow:0 0 0 0 rgba(27,79,212,0) }
  50%    { box-shadow:0 0 0 7px rgba(27,79,212,.16) }
}
```

Un halo azul que late y se apaga cuando el lector interactúa. Es el único recurso
para esto: no se agregan íconos de mano, tooltips ni carteles de "arrastrame".

### 6.6 Estructura de un ensayo

La del diseño, que se replica en los seis:

1. Kicker, H1 y bajada.
2. Uno o dos párrafos de encuadre.
3. Secciones numeradas `01 ·`, `02 ·`, `03 ·`, `04 ·`, cada una con su párrafo de
   entrada, su widget y el texto que lo explota.
4. Sección de cierre **"Para resolver 9, 10 y 15"**, que conecta el ensayo con los
   ejercicios concretos de la guía.

### 6.7 Referencias de origen

- **ciechanow.ski** — la alternancia texto/widget y la sobriedad.
- **Eugene Khutoryansky** — cada magnitud con su color, siempre el mismo.
- **MinutePhysics** — quitar todo lo que no explica.
- **Physics with Elliot** — rigor de notación, respeto por el lector que ya sabe algo.

---

## 7. Fuera de alcance

Para que quede explícito, no entra en esta versión:

- Cuentas de usuario, progreso guardado en servidor, sincronización.
- Ejercicios corregidos automáticamente o cualquier forma de evaluación.
- Video o audio.
- 3D.
- Los temas que se resuelven bien con una figura estática: vectores y unidades
  (Guía 0), gravitación, resortes en serie y paralelo, colisiones.
- Traducción a otros idiomas.
- Generación del contenido desde una fuente única compartida con el apunte.

---

## 8. Criterio de terminado

Un ensayo está listo cuando alguien que no entendía el tema lo lee, toca los widgets,
y puede resolver los ejercicios de la guía que ese ensayo cubre sin volver al apunte.

Ése es el único criterio. Si un widget es lindo pero no mueve esa aguja, sale.
