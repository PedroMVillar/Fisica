// Interprete de expresiones de una variable. Es a proposito un interprete y no un
// eval: lo que se evalua lo escribe el lector en un campo de texto de una pagina
// publicada, y eval le daria acceso a todo el documento.

const FUNCIONES = {
  sen: Math.sin, cos: Math.cos, tan: Math.tan,
  raiz: Math.sqrt, abs: Math.abs, exp: Math.exp, ln: Math.log,
};
const CONSTANTES = { pi: Math.PI, e: Math.E };

function tokenizar(fuente) {
  const tokens = [];
  let i = 0;
  while (i < fuente.length) {
    const c = fuente[i];
    if (/\s/.test(c)) { i++; continue; }
    if (/[0-9.]/.test(c)) {
      let j = i;
      while (j < fuente.length && /[0-9.]/.test(fuente[j])) j++;
      const n = Number(fuente.slice(i, j));
      if (!Number.isFinite(n)) throw new Error(`no entiendo el número «${fuente.slice(i, j)}»`);
      tokens.push({ tipo: 'numero', valor: n });
      i = j;
      continue;
    }
    if (/[a-zA-Z]/.test(c)) {
      let j = i;
      while (j < fuente.length && /[a-zA-Z]/.test(fuente[j])) j++;
      tokens.push({ tipo: 'nombre', valor: fuente.slice(i, j) });
      i = j;
      continue;
    }
    if ('+-*/^()'.includes(c)) { tokens.push({ tipo: c }); i++; continue; }
    throw new Error(`no entiendo el símbolo «${c}»`);
  }
  return tokens;
}

export function compilar(fuente) {
  try {
    const tokens = tokenizar(fuente);
    if (!tokens.length) throw new Error('la expresión está vacía');
    let k = 0;
    const mirar = () => tokens[k];
    const comer = tipo => {
      if (!tokens[k] || tokens[k].tipo !== tipo) throw new Error(`falta «${tipo}»`);
      return tokens[k++];
    };

    // suma := producto (('+' | '-') producto)*
    const suma = () => {
      let izq = producto();
      while (mirar() && (mirar().tipo === '+' || mirar().tipo === '-')) {
        const op = tokens[k++].tipo;
        const der = producto();
        const a = izq;
        izq = op === '+' ? t => a(t) + der(t) : t => a(t) - der(t);
      }
      return izq;
    };
    // producto := unario (('*' | '/') unario)*
    const producto = () => {
      let izq = unario();
      while (mirar() && (mirar().tipo === '*' || mirar().tipo === '/')) {
        const op = tokens[k++].tipo;
        const der = unario();
        const a = izq;
        izq = op === '*' ? t => a(t) * der(t) : t => a(t) / der(t);
      }
      return izq;
    };
    // unario := '-' unario | potencia     (el menos se aplica despues de la potencia)
    const unario = () => {
      if (mirar() && mirar().tipo === '-') { k++; const u = unario(); return t => -u(t); }
      return potencia();
    };
    // potencia := atomo ('^' unario)?     (asocia a derecha)
    const potencia = () => {
      const base = atomo();
      if (mirar() && mirar().tipo === '^') { k++; const exp = unario(); return t => base(t) ** exp(t); }
      return base;
    };
    const atomo = () => {
      const tk = mirar();
      if (!tk) throw new Error('la expresión se corta antes de tiempo');
      if (tk.tipo === 'numero') { k++; return () => tk.valor; }
      if (tk.tipo === '(') { k++; const dentro = suma(); comer(')'); return dentro; }
      if (tk.tipo === 'nombre') {
        k++;
        const nombre = tk.valor;
        if (mirar() && mirar().tipo === '(') {
          k++;
          const arg = suma();
          comer(')');
          const fn = Object.prototype.hasOwnProperty.call(FUNCIONES, nombre) ? FUNCIONES[nombre] : null;
          if (!fn) throw new Error(`no conozco la función «${nombre}»`);
          return t => fn(arg(t));
        }
        if (nombre === 't') return t => t;
        if (Object.prototype.hasOwnProperty.call(CONSTANTES, nombre)) {
          const v = CONSTANTES[nombre];
          return () => v;
        }
        throw new Error(`no conozco «${nombre}»; la única variable es t`);
      }
      throw new Error('esperaba un número, una variable o un paréntesis');
    };

    const f = suma();
    if (k !== tokens.length) throw new Error('sobra texto al final de la expresión');
    return { ok: true, f };
  } catch (e) {
    return { ok: false, error: e.message };
  }
}
