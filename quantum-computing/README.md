# Quantum Computing

How quantum computers actually work — built up from the qubit, through superposition,
entanglement, gates and circuits, to the algorithms that make them worth building.

The goal here is *intuition first*, then enough math to make the intuition precise.
Every abstract idea is paired with a picture, and most of them have a moving picture:
see the interactive **[animation/](./animation/index.html)** (open `index.html` in any
browser — no install, no internet needed).

## Start here

Read in order. Each note assumes the previous one.

1. **[01-the-qubit.md](./01-the-qubit.md)** — bits vs. qubits, the Bloch sphere, what a quantum state *is*.
2. **[02-superposition-and-measurement.md](./02-superposition-and-measurement.md)** — amplitudes, probabilities, why measurement is destructive.
3. **[03-entanglement.md](./03-entanglement.md)** — correlations with no classical explanation; Bell states.
4. **[04-gates-and-circuits.md](./04-gates-and-circuits.md)** — the quantum "instruction set"; how computation is unitary rotation.
5. **[05-algorithms.md](./05-algorithms.md)** — interference as the engine: Deutsch, Grover, Shor, and *why* they win.
6. **[06-hardware-and-challenges.md](./06-hardware-and-challenges.md)** — real qubits, decoherence, error correction, the NISQ era.

If you only read one thing, read note 02 and then open the animation — superposition and
interference are the whole game, and they're much easier to *see* than to read.

## The one-paragraph version

A classical bit is 0 or 1. A **qubit** is a unit vector in a 2-dimensional complex space —
a blend `α|0⟩ + β|1⟩` of both, called **superposition**. With `n` qubits you get a vector
in a `2ⁿ`-dimensional space, so the state of 300 qubits has more components than there are
atoms in the universe. Quantum **gates** rotate that giant vector (reversibly, all at once),
and **interference** is engineered so that wrong answers cancel and right answers add up.
You only get to **measure** once — that collapses the whole vector to a single classical
string — so the art of a quantum algorithm is arranging the interference so the string you
read out is probably the answer. That's it. Everything else is detail.

## How the pieces connect

```
        qubit  ──superposition──►  many states at once
          │                              │
     entanglement ──► correlations no classical machine can fake
          │                              │
        gates  ──► reversible rotations of the whole 2ⁿ-dim state
          │                              │
    interference ──► amplify right answers, cancel wrong ones
          │                              │
      measurement ──► collapse to ONE classical answer (probably correct)
```

## Conventions used in these notes

- `|ψ⟩` ("ket psi") is a quantum state — just a column vector of complex numbers.
- `|0⟩ = [1,0]ᵀ` and `|1⟩ = [0,1]ᵀ` are the two classical "computational basis" states.
- Amplitudes are complex numbers `α, β`; **probabilities** are `|α|²`, `|β|²`, and must sum to 1.
- Gates are **unitary** matrices `U` (they preserve length, so probabilities stay normalized).
- "Measure in the Z basis" = the ordinary `0/1` readout unless stated otherwise.

## Further reading

- Nielsen & Chuang, *Quantum Computation and Quantum Information* — the standard text.
- Andy Matuschak & Michael Nielsen, *Quantum Country* — spaced-repetition essays, excellent intuition.
- Scott Aaronson, *Quantum Computing Since Democritus* — the "why", with attitude.
- IBM Quantum / Qiskit textbook — hands-on, runs on real hardware.
