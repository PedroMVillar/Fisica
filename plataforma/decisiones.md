# Decisiones del dueño

Registro de decisiones de diseño tomadas por el dueño del proyecto, con su fecha y su
porqué. Se agregan acá, nunca se reescriben ni se dan por «corregidas» en una limpieza
futura sin volver a este archivo primero.

---

## 1. Separador decimal: coma, en todo el sitio

**Fecha:** 2026-09-12

**Decisión:** coma como separador decimal en todo el sitio, sin excepción — tanto en
la prosa de los ensayos como en las lecturas numéricas que generan los widgets.

**Por qué:** lo que estaba roto no era la elección del separador, era la mezcla. Cada
widget trae una frase de «qué mirar» que le pide al lector contrastar una lectura en
vivo contra el número que ya apareció en el párrafo — y esa comparación fallaba
cuando la lectura salía con punto y el párrafo con coma, no porque la cuenta estuviera
mal sino porque la puntuación no coincidía. Coma en los dos lados cierra esa
comparación.

---

## 2. El rojo de `auto-y-camion.html` se queda

**Fecha:** 2026-09-12

**Decisión:** el camión de `docs/ejemplos/auto-y-camion.html` sigue en rojo. Es la
única excepción registrada al reparto semántico de color del sitio (azul para
cinemática y velocidad, rojo para aceleración y fuerza).

**Por qué:** ahí el rojo no está representando una magnitud, está distinguiendo un
**cuerpo** del otro. El dueño evaluó las dos alternativas — rojo/azul contra
azul/azul — y decidió que el contraste rojo/azul separa mejor los dos móviles en
pantalla que dos tonos de azul uno al lado del otro. **Esto no es deriva y no se
«arregla» en una limpieza futura.** Cualquier otra página que quiera usar rojo para
algo que no sea aceleración o fuerza tiene que preguntar primero.

La excepción cubre **toda** la página — no sólo el punto que dibuja al camión — y son
exactamente estas cinco apariciones:

| Qué es | Dónde |
|---|---|
| El punto del camión en la ruta | `docs/ejemplos/auto-y-camion.html:178` |
| El punto del camión en el gráfico x(t) | `docs/ejemplos/auto-y-camion.html:211` |
| Su rótulo, la palabra «camión» | `docs/ejemplos/auto-y-camion.html:183` |
| Su curva de posición en el gráfico | `docs/ejemplos/auto-y-camion.html:197` |
| La lectura de `separación` (una distancia, roja por la misma razón: describe al camión) | `docs/ejemplos/auto-y-camion.html:69` |

Todo lo demás de la página — el punto y el rótulo del auto, su curva, el punto del
encuentro — sigue el reparto semántico normal. Si una revisión futura encuentra rojo
en cualquier otra línea de este archivo, o en cualquier otro archivo del sitio, eso sí
es deriva y hay que corregirlo.

---

## 3. Colores de las barras de energía — aprobado antes de escribir el ensayo 7

**Fecha:** 2026-09-12

**Decisión**, para cuando se implemente `docs/ensayos/energia.html` (ensayo 7):

- **Azul = cinética y cantidad de movimiento.** Es cinemática — cómo se mueve el
  cuerpo — y el azul ya es el color de la cinemática en todo el sitio.
- **`--graph` = potencial**, gravitatoria o elástica. Es «dónde está» el cuerpo, no
  «cómo se mueve»: no es cinemática ni es una fuerza, así que no le corresponde ni
  azul ni rojo. Usa el token neutro que ya existe para trazos de gráfico.
- **Rojo = lo disipado** — calor de rozamiento o trabajo de freno. Viene de una
  fuerza (el rozamiento), y rojo ya es el color de las fuerzas.

**Por qué:** ningún token de color nuevo. Los tres — `--blue`, `--graph`, `--red` — ya
existen y ya tienen un rol asignado en el resto del sitio; esta decisión les da un
significado más en el contexto específico de una barra de energía, sin contradecir el
reparto semántico general (azul-cinemática, rojo-fuerza) ni inventar una cuarta
categoría de color para «potencial».

---

*Enlazado desde el [README](../../README.md) y referenciado desde
[`brief.md`](brief.md).*
