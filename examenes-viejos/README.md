# Exámenes viejos

Parciales y finales de años anteriores. **Doble uso:**

1. **Consulta directa** — ver cómo toma la cátedra antes de rendir.
2. **Calibrar syntheca** — cargarlos con `/nuevo-banco-ejercicios` para que los ejercicios generados imiten el formato real (estructura de enunciado, curva de dificultad), parafraseado, nunca copiado literal.

```
/nuevo-banco-ejercicios examenes-viejos/parciales/<a.pdf>,<b.pdf> fisica-1 --tipo parcial
/nuevo-banco-ejercicios examenes-viejos/finales/<a.pdf>,<b.pdf>   fisica-1 --tipo final
```

Al revés que las fuentes bibliográficas, acá **conviene agrupar varios archivos del mismo tipo en una sola corrida**: lo que se extrae es un patrón de forma, y se calibra mejor viendo varios juntos. Pero cada `--tipo` va por separado, para no mezclar curvas de dificultad.

Lo cargado queda en `skills/banco-ejercicios/fisica-1/{parciales,finales}/`. Los PDFs originales se quedan acá.

## Convención de nombres

```
parciales/parcial-1-2024.pdf
parciales/parcial-2-2023-tema-a.pdf
finales/final-2024-02-turno-diciembre.pdf
```

Lo importante es que el nombre diga **qué examen es y de cuándo**; el resto es libre.
