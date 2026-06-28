# 01 — The Qubit

> The single unit of quantum information. Everything else is built on understanding what
> this object *is* and what you're allowed to do with it.

## From bit to qubit

A classical **bit** is the simplest possible piece of information: it is either `0` or `1`.
You can copy it, read it as many times as you like, and it never surprises you.

A **qubit** (quantum bit) is the quantum generalization. Instead of being *either* 0 or 1,
its state is a **superposition** — a weighted combination of both:

```
|ψ⟩ = α|0⟩ + β|1⟩
```

- `|0⟩` and `|1⟩` are the two "definite" states, called the **computational basis**.
- `α` and `β` are **complex numbers** called **amplitudes**.
- The only rule: `|α|² + |β|² = 1` (the **normalization** condition).

Read `|0⟩` as "ket zero". The bracket notation (Dirac notation) is just a column vector:

```
|0⟩ = [1]      |1⟩ = [0]      |ψ⟩ = [α]
      [0]            [1]            [β]
```

So a qubit is literally a **2-dimensional complex unit vector**. That's the whole definition.
The mystery isn't in the object — it's in what `α` and `β` *mean*, which is note 02.

## Why complex amplitudes, not just probabilities?

A natural guess: "a qubit is just a bit that's 0 with probability `p` and 1 with probability
`1−p`." That's a **probabilistic bit**, and it is *not* a qubit. The difference is the whole
ballgame:

| | probabilistic bit | qubit |
|---|---|---|
| state | one real number `p ∈ [0,1]` | two complex numbers `α, β` |
| can be negative? | no | yes — and complex |
| combining states | only adds | can **cancel** (interference) |

Because amplitudes can be negative (or complex), two paths to the same outcome can **cancel
out**. Probabilities can only ever pile up; they never subtract. This cancellation —
**interference** — is the single resource that makes quantum computers more than fast
classical random number generators. Hold onto that; it returns in note 05.

## The Bloch sphere — a picture of one qubit

Two complex numbers with one constraint (`|α|²+|β|²=1`) plus one irrelevant overall phase
leaves exactly **two real degrees of freedom**. Two real parameters → a point on the surface
of a sphere. That sphere is the **Bloch sphere**, the standard mental model for a single qubit.

```
              |0⟩   (north pole)
               •
              /|\
             / | \
            /  |  \         a qubit state |ψ⟩ is an arrow
           /   •───────►    from the center to a point
          |    |   ψ        on the surface
           \   |  /
            \  | /
             \ |/
              •
              |1⟩   (south pole)
```

- **North pole** = `|0⟩`, **south pole** = `|1⟩`.
- Points on the **equator** are equal superpositions like `|+⟩ = (|0⟩+|1⟩)/√2` — genuinely
  "half 0, half 1".
- **Latitude** controls the *probability* of measuring 0 vs 1.
- **Longitude** is the **phase** — invisible to a single measurement, but it's exactly what
  interference manipulates. (You can see this on the Bloch sphere panel in the animation.)

The key upgrade over a classical bit: a bit is *two points* (the poles). A qubit is the
*entire surface of the sphere*. Quantum gates (note 04) are **rotations** of this sphere.

## Important: a qubit still gives you only one bit out

A qubit holds two continuous parameters, but when you **measure** it you get a single
classical bit — `0` or `1` — and the rich state is gone (note 02). You cannot read off `α`
and `β`. This is why "a qubit stores infinite information" is a myth: you can *put* a
continuum in, but you can only ever *get* one bit out. The power comes from what you do to
the state *before* measuring, not from reading it.

## Multiple qubits: the exponential blow-up

Here's where it stops being a curiosity. The state of `n` qubits is **not** `n` separate
arrows — it's a single vector in a space of dimension `2ⁿ`:

```
1 qubit:   2 amplitudes   →  α₀|0⟩ + α₁|1⟩
2 qubits:  4 amplitudes   →  α₀|00⟩ + α₁|01⟩ + α₂|10⟩ + α₃|11⟩
3 qubits:  8 amplitudes
n qubits:  2ⁿ amplitudes
```

- **10 qubits** → 1,024 amplitudes.
- **50 qubits** → ~10¹⁵ amplitudes (a petabyte just to write the state down).
- **300 qubits** → more amplitudes than there are atoms in the observable universe.

A quantum computer never lists these numbers — *nature* holds the full vector, and gates
transform all `2ⁿ` of them in one physical step. Simulating this on a classical machine is
what gets exponentially expensive, and that gap is the source of any possible quantum
advantage.

> ⚠️ Caveat that matters: holding `2ⁿ` amplitudes does **not** mean you can read `2ⁿ` answers.
> Measurement gives one string. The whole challenge (note 05) is concentrating amplitude onto
> the answer you want *before* you look.

## Mental checklist

- [ ] A qubit is a 2-dimensional complex unit vector `α|0⟩ + β|1⟩`.
- [ ] `|α|²` and `|β|²` are measurement probabilities and sum to 1.
- [ ] Amplitudes can be negative/complex → they can **interfere/cancel**. This is the point.
- [ ] One qubit = a point on the Bloch sphere; gates rotate that sphere.
- [ ] `n` qubits live in a `2ⁿ`-dimensional space — exponential, but you still read out only `n` bits.

**Next:** [02 — Superposition and Measurement](./02-superposition-and-measurement.md), where the
amplitudes turn into probabilities and we see why looking destroys the state.
