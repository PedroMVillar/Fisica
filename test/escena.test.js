import { test } from 'node:test';
import assert from 'node:assert/strict';
import { crearEscena } from '../docs/motor/escena.js';

test('arranca en reposo y en t=0', () => {
  const e = crearEscena({ dibujar() {}, duracion: 3 });
  assert.equal(e.estado, 'reposo');
  assert.equal(e.t, 0);
});

test('no avanza el tiempo mientras no se reproduce', () => {
  const e = crearEscena({ dibujar() {}, duracion: 3 });
  e.avanzar(0.5);
  assert.equal(e.t, 0);
});

test('avanza al reproducir y se frena al pausar', () => {
  const e = crearEscena({ dibujar() {}, duracion: 3 });
  e.reproducir();
  e.avanzar(0.5);
  assert.equal(e.t, 0.5);
  e.pausar();
  e.avanzar(0.5);
  assert.equal(e.t, 0.5);
  assert.equal(e.estado, 'pausado');
});

test('al llegar al final se detiene en la duracion', () => {
  const e = crearEscena({ dibujar() {}, duracion: 3 });
  e.reproducir();
  e.avanzar(10);
  assert.equal(e.t, 3);
  assert.equal(e.estado, 'pausado');
});

test('reiniciar vuelve a reposo en cero', () => {
  const e = crearEscena({ dibujar() {}, duracion: 3 });
  e.reproducir(); e.avanzar(1); e.reiniciar();
  assert.equal(e.t, 0);
  assert.equal(e.estado, 'reposo');
});

test('avisa cada vez que cambia de estado', () => {
  const vistos = [];
  const e = crearEscena({ dibujar() {}, duracion: 3, alCambiar: s => vistos.push(s) });
  e.reproducir(); e.pausar(); e.reiniciar();
  assert.deepEqual(vistos, ['reproduciendo', 'pausado', 'reposo']);
});

// --- Cobertura del loop real de requestAnimationFrame -----------------
//
// Node no tiene requestAnimationFrame/cancelAnimationFrame: estas pruebas
// stubean ambos globals con una cola de callbacks controlada a mano, para
// fijar la superficie de seguridad del loop (reproducir idempotente,
// cancelacion exacta en pausar/reiniciar, y la re-verificacion defensiva
// de paso() ante un frame huerfano que llegara a correr igual).

function instalarStubRaf() {
  let siguienteId = 1;
  let llamadas = 0;
  const canceladas = [];
  const callbacksPorId = new Map();
  const original = {
    raf: globalThis.requestAnimationFrame,
    caf: globalThis.cancelAnimationFrame,
  };

  globalThis.requestAnimationFrame = cb => {
    llamadas += 1;
    const id = siguienteId++;
    callbacksPorId.set(id, cb);
    return id;
  };
  globalThis.cancelAnimationFrame = id => {
    canceladas.push(id);
    callbacksPorId.delete(id);
  };

  return {
    get llamadas() { return llamadas; },
    canceladas,
    callbacksPorId,
    restaurar() {
      if (original.raf === undefined) delete globalThis.requestAnimationFrame;
      else globalThis.requestAnimationFrame = original.raf;
      if (original.caf === undefined) delete globalThis.cancelAnimationFrame;
      else globalThis.cancelAnimationFrame = original.caf;
    },
  };
}

test('crear la escena no agenda ningun frame; solo reproducir() lo hace', () => {
  const stub = instalarStubRaf();
  try {
    const e = crearEscena({ dibujar() {}, duracion: 3 });
    assert.equal(stub.llamadas, 0);
    e.reproducir();
    assert.equal(stub.llamadas, 1);
  } finally {
    stub.restaurar();
  }
});

test('reproducir() dos veces seguidas agenda un solo frame', () => {
  const stub = instalarStubRaf();
  try {
    const e = crearEscena({ dibujar() {}, duracion: 3 });
    e.reproducir();
    e.reproducir();
    assert.equal(stub.llamadas, 1);
  } finally {
    stub.restaurar();
  }
});

test('pausar() cancela el frame agendado con su id exacto y un frame huerfano no corrompe la escena', () => {
  const stub = instalarStubRaf();
  try {
    const vistos = [];
    const e = crearEscena({ dibujar: t => vistos.push(t), duracion: 3 });
    e.reproducir();
    const [idAgendado, callbackAgendado] = [...stub.callbacksPorId.entries()][0];

    e.pausar();
    assert.deepEqual(stub.canceladas, [idAgendado]);

    // Simula un frame huerfano que corre igual pese a la cancelacion: paso()
    // se tiene que proteger solo mirando el estado, sin depender de que el
    // navegador haya cancelado a tiempo.
    callbackAgendado(1000);
    assert.equal(e.t, 0);
    assert.equal(e.estado, 'pausado');
    assert.deepEqual(vistos, []);
  } finally {
    stub.restaurar();
  }
});

test('reiniciar() cancela el frame agendado con su id exacto y un frame huerfano no corrompe la escena', () => {
  const stub = instalarStubRaf();
  try {
    const vistos = [];
    const e = crearEscena({ dibujar: t => vistos.push(t), duracion: 3 });
    e.reproducir();
    const [idAgendado, callbackAgendado] = [...stub.callbacksPorId.entries()][0];

    e.reiniciar();
    assert.deepEqual(stub.canceladas, [idAgendado]);
    vistos.length = 0; // limpiar el dibujar(0) que hace el propio reiniciar()

    callbackAgendado(2000);
    assert.equal(e.t, 0);
    assert.equal(e.estado, 'reposo');
    assert.deepEqual(vistos, []);
  } finally {
    stub.restaurar();
  }
});

test('el loop topea el salto de un frame en 0.05 s (pestaña en segundo plano)', () => {
  const stub = instalarStubRaf();
  try {
    const e = crearEscena({ dibujar() {}, duracion: 3 });
    e.reproducir();
    const [, paso] = [...stub.callbacksPorId.entries()][0];

    paso(0);            // primer frame: fija el origen del reloj, dt = 0
    assert.equal(e.t, 0);

    paso(10_000);       // vuelta de un segundo plano de 10 s sin frames
    assert.equal(e.t, 0.05);
    assert.equal(e.estado, 'reproduciendo');
  } finally {
    stub.restaurar();
  }
});
