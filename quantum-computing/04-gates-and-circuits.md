# 04 — Gates and Circuits

> Gates are the quantum computer's instruction set. A quantum program is a **circuit**:
> qubits as horizontal wires, gates applied left-to-right in time, a measurement at the end.
> The one surprising rule — every gate is **reversible** — shapes everything.

## A gate is a unitary matrix

A quantum gate on `k` qubits is a `2ᵏ × 2ᵏ` **unitary** matrix `U`. "Unitary" means
`U†U = I` (its conjugate-transpose is its inverse). Two consequences you need:

1. **Length-preserving.** Unitaries preserve the length of the state vector, so
   `|α|²+|β|²=1` stays true — probabilities remain valid after every gate.
2. **Reversible.** Every gate has an inverse (`U⁻¹ = U†`), so you can always run a quantum
   computation *backwards*. There is no quantum "erase" or "AND" that throws information away.

That second point is a real constraint. Classical AND (`(a,b) → a∧b`) destroys information —
from output `0` you can't recover the input. Quantum gates can't do that. To compute
irreversible-looking functions you keep extra qubits around so nothing is ever erased
(reversible computing). It sounds limiting; it isn't — reversible circuits are universal.

## The single-qubit gates (rotations of the Bloch sphere)

Every single-qubit gate is a **rotation of the Bloch sphere** (note 01). The essential ones:

### X — the quantum NOT (bit flip)
```
X = [0 1]      X|0⟩ = |1⟩,  X|1⟩ = |0⟩       (180° rotation about the X-axis)
    [1 0]
```

### Z — the phase flip
```
Z = [1  0]     Z|0⟩ = |0⟩,  Z|1⟩ = −|1⟩      (180° rotation about the Z-axis)
    [0 −1]
```
Z does nothing visible to `|0⟩` or `|1⟩` probabilities — it only flips the **phase** of `|1⟩`.
Useless alone (you can't measure phase), decisive in combination. This is the "steering wheel"
from note 02.

### H — the Hadamard (the superposition gate)
```
H = 1/√2 [1  1]    H|0⟩ = (|0⟩+|1⟩)/√2 = |+⟩
         [1 −1]    H|1⟩ = (|0⟩−|1⟩)/√2 = |−⟩
```
**The most important gate in the toolbox.** It turns a definite state into an even
superposition — it *opens the slits*. Apply H to each of `n` qubits starting from `|00…0⟩` and
you get an equal superposition of **all `2ⁿ` bit-strings at once**:

```
H⊗n |00…0⟩ = (1/√2ⁿ) Σ over all x of |x⟩      ← every input, simultaneously
```

This is the "quantum parallelism" everyone quotes. Note carefully: it's free to *create*, but
note 02 says you still measure only one string out. H also *undoes itself* (`H·H = I`) — it's
both how you spread amplitude out and, at the end, how you fold it back to read interference.

### Rotation / phase gates (continuous knobs)
`Rx(θ), Ry(θ), Rz(θ)` rotate by an arbitrary angle `θ` about each axis; `S` and `T` are
specific small phase rotations. These give you *fine* control over a qubit's point on the
sphere, which you need for real algorithms.

## The two-qubit gate: CNOT (the entangler)

A single-qubit gate can never create entanglement — you need a gate that lets one qubit
**condition** another. The workhorse is **CNOT** (controlled-NOT):

```
              control ──●──
                        │            "flip the target IF the control is 1"
              target  ──⊕──

CNOT |00⟩ = |00⟩      CNOT |10⟩ = |11⟩
CNOT |01⟩ = |01⟩      CNOT |11⟩ = |10⟩      (control unchanged; target XORed with control)
```

As a matrix on the basis `{|00⟩,|01⟩,|10⟩,|11⟩}`:
```
       [1 0 0 0]
CNOT = [0 1 0 0]
       [0 0 0 1]
       [0 0 1 0]
```

Feed CNOT a control that's *in superposition* and it entangles (note 03's Bell circuit). Other
two-qubit gates (CZ, SWAP) and three-qubit gates (Toffoli/CCNOT) exist, but CNOT + single-qubit
gates already get you everywhere.

## Universality: a tiny instruction set runs everything

You don't need infinitely many gate types. A small set is **universal** — it can approximate
*any* unitary on any number of qubits to arbitrary precision:

```
{ H, T, CNOT }        ← one common universal set
{ any single-qubit rotations + CNOT }   ← another
```

This is the quantum analogue of NAND being universal for classical logic. The
**Solovay–Kitaev theorem** guarantees you can hit any target gate efficiently with a short
sequence from the universal set. So hardware only has to implement a handful of gates well.

## Reading a circuit diagram

Time flows **left to right**. Each wire is a qubit. The Bell-state circuit from note 03:

```
        t=0      t=1     t=2      t=3
 q0: |0⟩ ──────[ H ]─────●─────── M  ╤═  (classical bit)
                         │
 q1: |0⟩ ────────────────⊕─────── M  ╤═

 step 1:  start in |00⟩
 step 2:  H on q0      → (|00⟩ + |10⟩)/√2
 step 3:  CNOT         → (|00⟩ + |11⟩)/√2     ← entangled (Bell state)
 step 4:  measure both → 00 or 11, 50/50, always matching
```

Everything *before* the measurement is reversible unitary evolution. The measurement (the `M`
boxes / meters) is the one irreversible step, and it happens once, at the end. That's the
universal shape of a quantum program.

## Why "gates on the whole 2ⁿ vector" is the magic and the catch

A gate like `H⊗n` acts on all `2ⁿ` amplitudes **in a single physical operation** — nature does
the bookkeeping, not you. That's the magic: exponential-sized transformations at constant cost.

The catch (again): the *output* is still one measured string. A gate that touches `2ⁿ`
amplitudes hasn't helped unless the amplitudes were arranged so the right answer dominates.
Designing that arrangement is note 05.

## See it move

The animation's **Gates / Circuit** panel lets you drop H, X, Z, and CNOT onto two wires and
watch the 4 amplitudes (and the resulting measurement statistics) update live. Build the Bell
circuit and watch `01`/`10` go to zero.

## Mental checklist

- [ ] Gates are unitary → length-preserving and **reversible** (no information erased).
- [ ] X = bit flip, Z = phase flip, **H = make superposition** (opens the slits, self-inverse).
- [ ] CNOT conditions one qubit on another → the source of entanglement.
- [ ] A small set (e.g. `{H, T, CNOT}`) is **universal**; hardware needs only a few gates.
- [ ] Circuits run left→right, fully reversible, with a single measurement at the end.

**Next:** [05 — Algorithms](./05-algorithms.md), where interference turns all this machinery into
an actual computational speed-up.
