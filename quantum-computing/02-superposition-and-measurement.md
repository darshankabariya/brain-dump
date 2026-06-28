# 02 — Superposition and Measurement

> Superposition is what gives a quantum computer its parallelism. Measurement is the tax you
> pay to extract an answer — and it's a brutal tax. Understanding the trade between them is
> understanding why quantum algorithms are *clever* rather than just *fast*.

## What superposition really means

A qubit in state `α|0⟩ + β|1⟩` is **not** secretly 0 or 1 with you just not knowing which.
It is genuinely *both at once*, in a way that has measurable physical consequences (the
double-slit experiment, interference — see below). "It's really 0 or 1 and we're ignorant"
is the classical *probabilistic* picture, and experiments (Bell tests, note 03) rule it out.

A clean way to feel the difference:

- **Classical coin, spinning:** at any instant it *is* heads or tails; you just can't see it.
- **Quantum coin:** while "spinning" it is in a real superposition. Two such coins can
  interfere; two unknown classical coins cannot.

The `|+⟩` and `|−⟩` states make the realness concrete:

```
|+⟩ = (|0⟩ + |1⟩)/√2        |−⟩ = (|0⟩ − |1⟩)/√2
```

Both give **50/50** when measured in the 0/1 basis — identical probabilities. Yet they are
*different states* (note the minus sign), and a single gate (the Hadamard, note 04) maps
`|+⟩ → |0⟩` and `|−⟩ → |1⟩`, telling them apart with certainty. The sign — the **phase** —
is invisible to one measurement but absolutely physical. Probabilities alone do not capture
the quantum state.

## The Born rule: amplitudes → probabilities

When you measure a qubit `α|0⟩ + β|1⟩` in the computational basis:

```
P(get 0) = |α|²
P(get 1) = |β|²
```

This squaring is the **Born rule**. It's why amplitudes must satisfy `|α|²+|β|²=1`: the
probabilities have to sum to 1. The squaring is also exactly why interference works: if two
paths contribute amplitudes `+a` and `−a` to the same outcome, the *amplitude* there is
`a + (−a) = 0`, so the *probability* is `0² = 0`. The outcome vanishes even though each path
alone had nonzero probability `a²`. Probabilities can't do that; amplitudes can.

## Measurement is destructive (collapse)

Here is the rule that shapes every quantum algorithm:

> **Measuring a superposition collapses it.** You get one outcome (say `0`, with probability
> `|α|²`), and *immediately after*, the qubit's state becomes `|0⟩`. The other amplitude `β`
> is gone forever. Measure again and you get `0` with certainty — the original superposition
> is unrecoverable.

Consequences, each of which constrains how you can build algorithms:

1. **You can't read the amplitudes.** One measurement of one qubit yields one bit. To even
   *estimate* `|α|²` you'd need many identically prepared copies and lots of measurements.
2. **You can't copy an unknown qubit** — the **no-cloning theorem**. If you could, you'd
   clone-and-measure your way to the amplitudes, defeating point 1. (Proof sketch: cloning
   would be a non-linear operation; quantum mechanics is linear.) This is why quantum error
   correction is hard *and* why quantum cryptography is secure.
3. **Looking too early kills the computation.** All the `2ⁿ`-dimensional richness of note 01
   is a resource you can only spend *once*, at the end.

So the entire structure of a quantum algorithm is:

```
prepare  ──►  superpose  ──►  many gates (interfere)  ──►  measure ONCE
 |0…0⟩         spread amplitude     concentrate amplitude       read n bits
               over many states     onto the right answer       (probably correct)
```

## The double-slit experiment — superposition you can see

The canonical demonstration. Fire particles (photons, electrons, even molecules) one at a
time at a barrier with two slits, onto a screen behind.

```
        slit 1
 source   ║     ┌──────────┐
   •───────────►│ ▓ ░ ▓ ░ ▓ │   interference pattern:
   •───────────►│ ░ ▓ ░ ▓ ░ │   bright = amplitudes ADD
        ║       │ ▓ ░ ▓ ░ ▓ │   dark   = amplitudes CANCEL
        slit 2  └──────────┘
```

- Each particle goes through in a **superposition** of "slit 1" and "slit 2".
- The two amplitudes recombine at the screen and **interfere**: bands of bright (constructive)
  and dark (destructive). Dark bands are spots a particle *could* reach through either slit
  alone, but reaches through *neither* when both are open — the amplitudes cancel.
- **Crucially:** if you place a detector to learn *which* slit each particle used, the
  interference pattern **disappears**. Measuring "which path" collapses the superposition.
  Information and interference are mutually exclusive — exactly the collapse rule above, in
  the lab.

This is the physical heart of quantum computing in one experiment: *superposition spreads
amplitude over paths; interference recombines it; measurement destroys it.* A quantum
algorithm is a carefully engineered double-slit with `2ⁿ` "slits".

## Phase: the hidden steering wheel

The amplitude `β = |β|·e^{iφ}` has a magnitude *and* a **phase** `φ`. The phase never shows
up in `|β|²`, so a single measurement can't see it — but gates can turn phase into amplitude
and back. Algorithms work by:

1. Writing problem data into **phases** (invisible, no measurement penalty yet).
2. Using interference to convert "good" phase patterns into **large amplitudes** on the
   answer and "bad" ones into **near-zero** amplitudes.
3. *Then* measuring, so the answer is what you most likely read.

Grover's algorithm and Shor's algorithm (note 05) are both, at heart, phase-manipulation
machines. Keep "phase is the steering wheel, amplitude is the speedometer" in mind.

## See it move

In the **[animation](./animation/index.html)**:

- The **Superposition** panel shows a qubit as a probability bar you can tilt from `|0⟩` to
  `|1⟩`; hit *Measure* repeatedly and watch the collapse statistics build up toward `|α|²`.
- The **Interference** panel shows two amplitude arrows you can rotate; watch the resulting
  probability go to zero when they point opposite (cancel) and to one when aligned (add).

## Mental checklist

- [ ] Superposition is *real*, not "hidden 0/1 we don't know yet".
- [ ] Born rule: probability = `|amplitude|²`. Squaring is why cancellation is possible.
- [ ] Measurement collapses the state to one outcome; the rest is destroyed.
- [ ] No-cloning: you can't copy an unknown state, so you can't cheat the collapse.
- [ ] Phase is invisible to one measurement but is the thing algorithms steer.

**Next:** [03 — Entanglement](./03-entanglement.md), where two qubits become correlated in a
way no classical system can reproduce.
