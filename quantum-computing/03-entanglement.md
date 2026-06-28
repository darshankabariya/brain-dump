# 03 — Entanglement

> "Spooky action at a distance" (Einstein, unhappily). Entanglement is the correlation
> between qubits that has *no* classical explanation. It's what lets `n` qubits be a single
> `2ⁿ`-dimensional object rather than `n` independent arrows.

## The setup: when is a 2-qubit state "separable"?

Two qubits live in a 4-dimensional space:

```
|ψ⟩ = α|00⟩ + β|01⟩ + γ|10⟩ + δ|11⟩
```

Sometimes this factors into "qubit A's state" ⊗ "qubit B's state":

```
(a|0⟩ + b|1⟩) ⊗ (c|0⟩ + d|1⟩)   ← separable / product state
```

When it factors, the qubits are **independent** — measuring one tells you nothing about the
other. When it **does not factor**, the qubits are **entangled**: their fates are linked.

## The Bell state — the simplest entanglement

The most famous entangled state:

```
|Φ⁺⟩ = (|00⟩ + |11⟩)/√2
```

Try to write this as `(a|0⟩+b|1⟩) ⊗ (c|0⟩+d|1⟩)`. You'd need `ad = 0` (no `|01⟩` term) and
`bc = 0` (no `|10⟩` term), but also `ac ≠ 0` and `bd ≠ 0`. Impossible. **It does not factor.**
The two qubits do not have individual states at all — only the *pair* has a state.

What it predicts when you measure both in the 0/1 basis:

```
|Φ⁺⟩ = (|00⟩ + |11⟩)/√2

  outcome 00 :  probability 1/2
  outcome 11 :  probability 1/2
  outcome 01 :  probability 0      ← never happens
  outcome 10 :  probability 0      ← never happens
```

So: **each qubit alone looks like a fair coin** (50/50), but the two coins *always agree*.
Measure qubit A and get `0` → qubit B is now *instantly* `0`, with certainty, even if it's on
the other side of the galaxy. Measure A and get `1` → B is `1`. Perfect correlation, every time.

## "But that's just like two gloves in two boxes!" — no, it isn't

The classical objection: put a left glove in one box, a right glove in another, ship them
apart. Open one, you instantly "know" the other. Correlated, no spookiness. Surely
entanglement is the same?

It is **not**, and this is provable, not philosophical. The glove story is a **local hidden
variable** model: each box had a definite answer all along, you were just ignorant.
**Bell's theorem** shows entangled qubits violate inequalities that *any* such
"definite-answer-all-along" model must obey.

### Bell's inequality, in one breath

Suppose you measure each qubit along one of two *different* angles (not just the 0/1 axis),
chosen randomly and independently. Tally how often the two outcomes agree. Then:

```
Any local-hidden-variable theory:   |S| ≤ 2     (CHSH inequality)
Quantum mechanics predicts:         |S| = 2√2 ≈ 2.83
Experiments measure:                ≈ 2.8   ✓ quantum wins
```

The qubits agree *more strongly* than the gloves possibly could. There were **no predefined
answers** — the correlation is created at the moment of measurement, jointly, across the pair.
This has been confirmed in ever-tighter "loophole-free" experiments (the 2022 Nobel Prize in
Physics went to Aspect, Clauser, and Zeilinger for exactly this).

> The gloves had answers before you looked. Entangled qubits genuinely did not — and nature
> still keeps them in lockstep.

## No, you can't send signals faster than light

A common misread: "instant correlation across the galaxy = faster-than-light communication."
It does not, and the reason is the collapse rule from note 02:

- Alice measures her qubit and gets `0` or `1` — but she gets a **random** result she can't
  control. To her, B's outcome is also random.
- Bob, looking only at his qubit, sees **pure 50/50 noise**. Nothing in his data changes
  whether or not Alice measured, or what she got.
- The correlation only becomes visible *after* they bring their results together and compare
  — over a classical channel, which is light-speed-limited.

So entanglement gives **correlation without communication**. No information travels; no
relativity is violated. (This is the "no-signalling" principle.)

## Why entanglement is the computational resource

Recall note 01: `n` qubits span a `2ⁿ`-dimensional space. *Product* states only reach a thin
sliver of that space — they're describable with about `2n` numbers, not `2ⁿ`. **Entangled**
states fill the rest. A quantum computer that never entangled its qubits could be simulated
efficiently on a laptop (this is essentially the content of the **Gottesman–Knill theorem**
for an important class of circuits). No entanglement → no quantum advantage.

Entanglement is the glue that makes the exponential state space *one connected object* you
can manipulate as a whole, rather than `n` separate qubits you'd track independently.

## Making one: the Bell circuit

You build `|Φ⁺⟩` from `|00⟩` with exactly two gates (defined in note 04):

```
 |0⟩ ──[ H ]──●──   ┐
              │     ├──►  (|00⟩ + |11⟩)/√2
 |0⟩ ─────────⊕──   ┘

 H  : Hadamard on qubit 0  →  puts it in (|0⟩+|1⟩)/√2, so state is (|00⟩+|10⟩)/√2
 ●⊕ : CNOT (control=q0, target=q1) → flips q1 iff q0 is 1
       (|00⟩+|10⟩)/√2  ──CNOT──►  (|00⟩+|11⟩)/√2   ← entangled
```

That's the entire recipe: **superpose one qubit, then let it control a flip on another.**
The control creates the link. You can step through this in the animation's *Entanglement* /
*Circuit* panel and watch the `01`/`10` outcomes drop to zero.

## Mental checklist

- [ ] Entangled = the joint state does **not** factor into individual qubit states.
- [ ] Bell state `(|00⟩+|11⟩)/√2`: each qubit is 50/50, but they always agree.
- [ ] Bell's theorem rules out "they had answers all along" — confirmed experimentally.
- [ ] No faster-than-light signalling: each side alone sees pure noise.
- [ ] No entanglement → classically simulable → no quantum advantage.

**Next:** [04 — Gates and Circuits](./04-gates-and-circuits.md), the operations that turn these
states into computation.
