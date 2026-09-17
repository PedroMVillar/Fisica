# Qué ejercicios se repiten en el Parcial I

> Relevamiento de los parciales viejos, hecho el 17 de septiembre de 2026 para
> decidir qué ejercicios valía la pena tener resueltos. **No es una predicción de
> qué va a tomar la cátedra**: es qué tomó antes.
>
> Los cuatro ejemplos que salieron de acá están publicados en
> <https://bitacoradestudio.com/fisica/>.

---

Fuente principal: `examenes-viejos/parciales/` — los nueve archivos "Parcial 1" de 2009 a 2024, leídos en su totalidad.
Fuente secundaria: `examenes-viejos/finales/` — nueve finales, filtrando sólo los ejercicios de temas de Parcial I.
Contexto: `parcial-1/practicos/` (Prácticos 0-3) y `parcial-1/preparacion/` (resúmenes ya escritos por el alumno: cuerpo aislado, rozamiento, sistemas acoplados, movimiento circular, tiro parabólico — confirma qué teoría ya trabajó).

## Nota de honestidad sobre la fuente

Los nueve archivos no son nueve exámenes independientes. `Parcial 1 2017-07-28.pdf` y `Parcial 1 2017-09-28.pdf` contienen **el mismo examen** (ambos encabezan "Parcial 1. 28/09/2017"; el primero es un escaneo parcial de una sola página que corta el problema 3, el segundo tiene las dos páginas completas). Y `Parcial 1 2020-11-26.pdf` (recuperatorio) repite **textualmente** el problema 1 de 2017 (bloque A-B-C). Así que la base real es **8 instancias de examen distintas** (2009, 2014, 2017, 2020, 2021, 2022, 2023, 2024), no 9. Todas las frecuencias de abajo están calculadas sobre esas 8. `Parcial 1 2025-09-25.pdf` existe pero queda fuera del rango que se pidió relevar (2009-2024) y no se leyó.

Los nueve parciales se leyeron completos y sin problemas de OCR/escaneo — todos tienen texto o imagen legible. No hubo que descartar ninguno.

## 1. Tabla de frecuencias (por tipo, sobre las 8 instancias)

| Tipo de ejercicio | Frecuencia | Años |
|---|---|---|
| Sistemas acoplados por cuerda-polea (con/sin rozamiento, plano horizontal y/o inclinado, incluida variante cuña) | 6 de 8 | 2014, 2017, 2020 (repite 2017), 2021, 2022, 2023 |
| Tiro parabólico / proyectil (acantilado, ángulo máximo, terreno inclinado, combinado con choque) | 5 de 8 | 2009, 2017, 2022, 2023, 2024 |
| Colisiones + momento lineal con pregunta explícita de conservación de energía | 4 de 8 | 2014, 2020, 2021, 2022 |
| Trabajo y energía con resorte + rampa/pista con rozamiento (incluye loops y despegue) | 3 de 8 | 2022, 2023, 2024 |
| Movimiento circular (cinemática y/o dinámica angular) | 3 de 8 | 2009, 2017, 2024 |
| Centro de masa de cuerpo rígido | 1 de 8 | 2020 |
| Cuña con bloque (rozamiento cuña-mesa, sin rozamiento bloque-cuña) | 1 de 8 (más 1 en finales: 2026-02-11 es variante distinta, doble plano con polea) | 2021 |
| Movimiento relativo (cambio de marco de referencia) | 0 de 8 en parciales — sólo aparece en Final 2009-02-20 | — |
| Momento angular / campos centrales | 0 de 8 en parciales — sólo aparece en Final 2008-02-20 | — |

Los dos últimos renglones son temas que el alcance 2026 incluye explícitamente pero que **no se repiten en ningún parcial de la muestra** — es un hallazgo, no un olvido: la evidencia directa es débil y hay que decirlo así.

Refuerzo de finales (sólo ejercicios de temas de Parcial I, filtrando electrostática/circuitos/magnetismo/termodinámica): la familia "sistemas acoplados por polea" reaparece en Final 2017-12-07 (P1), Final 2021-12-07 (P1), Final 2009-02-27 (P2), Final 2008-12-17 (P2) y Final 2026-02-11 (Ej.1); y la familia "péndulo que cae y choca" reaparece en Final 2025-12-16 (P1). Esto confirma que ambas familias no son un capricho de los parciales sino el núcleo real de la materia.

## 2. Los seis candidatos más fuertes, ordenados

1. **Sistema acoplado por polea con rozamiento, decidiendo primero si el sistema se mueve** — 6/8. Enseña a comparar la fuerza motriz contra el rozamiento estático *antes* de plantear ecuaciones dinámicas, a elegir qué aislar (cada cuerpo o el sistema), a fijar un signo de aceleración consistente entre ambos cuerpos, y a distinguir el régimen estático (umbral) del cinético (una vez en movimiento). Ningún otro ejercicio de la lista obliga a este chequeo previo de "¿arranca o no?".

2. **Choque encadenado con conservación selectiva (péndulo balístico)** — 4/8. Es el único tipo que pide justificar, tramo por tramo, cuándo se conserva qué: energía mecánica en la caída del péndulo (sin choque), momento lineal en el choque (instantáneo), y de nuevo energía mecánica después. Es la trampa central del parcial hecha ejercicio.

3. **Tiro parabólico sobre terreno no horizontal o con condición de impacto no trivial** — 5/8. Obliga a plantear la condición de llegada al suelo como una ecuación geométrica (recta del terreno, borde de un acantilado, altura de una muralla) en lugar de aplicar de memoria "y=0". Enseña a razonar la condición de contorno, no la fórmula.

4. **Energía con resorte + pista circular con rozamiento, decidiendo si el cuerpo completa el loop o se despega** — 3/8, concentrado en 2022-2024 (tendencia reciente). Enseña una decisión que no aparece en ningún otro tipo: comparar la velocidad real en el punto crítico contra la velocidad mínima que exige N≥0, en presencia de una fuerza no conservativa (rozamiento) que ya gastó energía en el camino.

5. **Dinámica de movimiento circular con cuerpo colgante en equilibrio (mesa giratoria + peso por un agujero)** — 3/8, pero es el único que es dinámica circular real (no cinemática angular pura): la tensión de la cuerda cumple dos roles simultáneos —peso de un cuerpo y fuerza centrípeta del otro— y hay que plantear Newton en los dos cuerpos a la vez.

6. **(Cobertura, evidencia débil) Momento angular con radio variable / movimiento relativo** — 0/8 en parciales, presentes sólo en finales de 2008/2009. Se incluyen porque el alcance 2026 los lista explícitamente y en la muestra de parciales no hay ningún ejemplo — es una apuesta defensiva, no una repetición comprobada, y hay que decírselo así al alumno.

## 3. Enunciados concretos recomendados, con procedencia

**Candidato 1 — sistemas acoplados con rozamiento.**
Parcial 1, 29/09/2022, Problema 2 (mejor que 2023 porque agrega el freno de la polea, obligando a la pregunta "¿se moverán las masas?" antes de cualquier cuenta, y además pide la condición de equilibrio *durante* el movimiento con rozamiento cinético — dos decisiones en un solo enunciado):
> "Una masa en un plano inclinado está unida a otra masa colgante mediante una cuerda de masa despreciable y una polea. La masa en el plano inclinado es de 500g, la colgante 600g, el ángulo es de 30° y los coeficientes de rozamiento son μd=0,2 y μe=0,4. (a) Si la polea tiene un freno que mantiene quieto al sistema y se lo libera, ¿se moverán las masas? Justifique. (b) DCL de cada masa. (c) Aceleración con el freno liberado. (d) Tensión de la cuerda. (e) Suponiendo el sistema en movimiento, relación entre M1 y M2 para el equilibrio."

**Candidato 2 — choque con conservación selectiva.**
Parcial 1, Recuperatorio, 26/11/2020, Problema 3 (mejor que la versión de 2014 y 2021 porque pregunta *explícitamente* por la conservación, en vez de dejarlo implícito):
> "Con un cañón de resorte (compresión máxima 50cm) se lanza un proyectil de 40g con 30° respecto del horizonte; en su altura máxima impacta contra la masa esponjosa de 500g de un péndulo balístico de 2m y se le queda unido. El ángulo máximo del péndulo es 10°. (a) Dibujo esquemático. (b) Energía cinética del conjunto justo después del impacto. (c) Comparando antes y después del impacto, ¿se conserva el momento lineal? ¿se conserva la energía cinética? Justifique. (d) Velocidad del proyectil justo antes del impacto. (e) Velocidad con la que el proyectil abandonó el cañón. (f) Tiempo de vuelo. (g) Constante del resorte."

**Candidato 3 — proyectil con condición de impacto no trivial.**
Parcial 1, 26/09/2024, Problema 1 (mejor que 2017/2023 porque el terreno inclinado 5° obliga a resolver la intersección con una recta, no con y=0, y pide graficar y vectores en dos instantes):
> "Un golfista golpea una pelota con velocidad inicial de 48 m/s y ángulo de 25° con la horizontal. El terreno tiene una pendiente de 5°. Determinar: (a) vectores a(t), v(t), r(t); (b) tiempo hasta la altura máxima; (c) distancia entre el golfista y el punto donde la pelota toca el piso; (d) velocidad con que la pelota toca el piso; (e) graficar x(t), y(t), y dibujar velocidad y aceleración en el punto más alto y justo antes de chocar. g=10 m/s²."

**Candidato 4 — resorte + loop con rozamiento y despegue.**
Parcial 1, 26/09/2024, Problema 3 (mejor que 2022 porque el rozamiento en la pista circular es un dato explícito en Newtons, y la pregunta de despegue está formulada de manera directa: "¿llega arriba o se desprende antes?"):
> "Un bloque de masa 0,5 kg es empujado contra un resorte (k=450 N/m) hasta comprimirlo x. Se libera y viaja sin rozamiento hasta el punto B, y continúa por una pista circular de radio 1m con vB=12 m/s. En la pista circular sufre una fuerza de fricción de 7N. (a) Longitud de compresión x. (b) Trabajo para comprimir el resorte y trabajo desde que se libera hasta B. (c) ¿El bloque llega a la parte superior de la pista o se desprende antes? Si llega, calcule vT; si no, calcule el punto donde se despega."

**Candidato 5 — dinámica circular con cuerpo colgante.**
Parcial 1, 26/09/2024, Problema 2 (único ejemplo de este tipo en toda la muestra; se usa por default):
> "Una masa m1=1 kg se une a una cuerda de masa despreciable e inextensible y se hace girar en un círculo de radio R=1,5m sobre una mesa sin fricción. La cuerda pasa por un orificio en el centro de la mesa y una masa m2=500 g se une al otro extremo, colgando en equilibrio mientras m1 gira a velocidad angular constante. (a) DCL de cada cuerpo. (b) Tensión T. (c) Velocidad tangencial de m1 para que m2 permanezca suspendida."

**Candidato 6 — momento angular / movimiento relativo (cobertura, evidencia débil).**
Final, 20/02/2008, Problema 5 (único ejemplo de momento angular con radio variable en todo el material relevado):
> "Una partícula de masa m está unida al extremo de un hilo y recorre una trayectoria circular de radio r sobre una mesa horizontal sin rozamiento. El hilo pasa por un orificio y su otro extremo está fijo. (a) Si se tira del hilo disminuyendo el radio, ¿cómo varía la velocidad angular, si vale ω₀ cuando el radio vale r₀? (b) ¿Cuál es el trabajo realizado al pasar lentamente de r₀ a r₀/2?"
Alternativa para movimiento relativo: Final, 20/02/2009, Problema 1 (bombardero que suelta una bomba sobre un camión que se mueve en sentido contrario — cambio de marco de referencia).

## 4. Trampas recurrentes

- **Masa vs. peso**: varios enunciados dan el peso en Newtons directamente (Parcial 2017/2020, bloque A "pesa 44.5 N") — hay que dividir por g antes de usarlo en F=ma o en μN, y es fácil mezclar kg con N sin darse cuenta.
- **Rozamiento estático vs. cinético como decisión, no como dato**: 2022 y 2023 preguntan explícitamente "¿se moverán las masas?" antes de dar μd — la trampa es usar μd para decidir si arranca, cuando el umbral de arranque lo fija μe.
- **Signo y justificación del trabajo**: 2023 P3 pide explícitamente "justifique el signo del trabajo" — la trampa es asumir que todo trabajo es positivo, o no distinguir el trabajo neto del trabajo de una fuerza en particular.
- **Cuándo se conserva momento lineal y cuándo energía**: la trampa central de toda la muestra. Se conserva momento lineal en choques (instante), y sólo en el elástico también la energía cinética; fuera del choque (antes/después) se conserva energía mecánica si no hay rozamiento. Aplicar conservación de energía *durante* un choque inelástico es el error más repetido de la materia.
- **La dirección del movimiento no se lee del DCL**: trampa señalada explícitamente en el cuestionario de 2021 — un diagrama de cuerpo libre con una fuerza hacia la derecha no dice que el cuerpo se esté moviendo hacia la derecha (podría estar frenando yendo hacia la izquierda).
- **Aceleración en movimiento circular no siempre es puramente centrípeta**: si la rapidez cambia, hay componente tangencial además de la centrípeta — trampa explícita en el cuestionario de 2021 y relevante para 2009 P2 y 2017 P3.
- **Proyectil sobre terreno no horizontal**: usar y=0 en vez de la ecuación de la recta del terreno (o del borde/altura dados) es el error más común en los problemas de tiro parabólico de 2017, 2023 y 2024.
- **Conversión rad ↔ vueltas**: aparece mal manejada en los ejercicios de movimiento circular de 2009 y 2017 (contar "vueltas hasta detenerse" a partir de una desaceleración angular).

## 5. Lo que NO conviene resolver

- **Parcial 2009, Problema 1** (viaje en tramos CB-BT-TC): aplicación iterada de v=d/t y MRUV sin ninguna decisión conceptual nueva. Es práctico 1 puro, no aporta razonamiento adicional si ya se resolvió un ejercicio de colisiones o de sistemas acoplados.
- **Parcial 2023, Problema 1** (proyectil hacia una muralla a 5 km): tiro parabólico sin condición geométrica interesante, sólo "llega o no llega" por cuenta directa. Redundante frente al Candidato 3 (2024 P1), que sí agrega la dificultad del terreno inclinado.
- **Final 2008-12-17, Problema 1** (avión que frena en la pista) y **Final 2008-12-05, Problema 2** (bloque + polea sin rozamiento, tensión directa): pura aplicación de fórmula de MRUV o de F=ma en un Atwood simple, sin ninguna decisión. No enseñan nada que Candidato 1 no enseñe mejor.
- **Parcial 2020 (recuperatorio), Problema 2** (centro de masa de una barra en bisagra): aparece una sola vez en las 8 instancias y el tema "centro de masa" no figura explícitamente en el alcance de Parcial I 2026 que se definió. No es prioridad.
- **El cuestionario de opción múltiple de Parcial 2021 (primera parte)**: no es un "ejercicio resuelto" en el sentido pedido — es una batería de preguntas conceptuales cortas. Su valor ya está incorporado en la sección de trampas recurrentes; no hace falta resolverlo como nota aparte.
