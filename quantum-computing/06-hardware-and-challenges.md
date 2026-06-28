# 06 — Hardware and Challenges

> The theory (notes 01–05) is settled and beautiful. The engineering is brutal. This note is
> the reality check: real qubits, why they fall apart, how error correction fights back, and
> honestly where we are (the **NISQ** era) versus where we need to be (fault tolerance).

## What is a physical qubit, really?

A qubit is any quantum system with two cleanly addressable states you can put in superposition,
entangle, and measure. Several physical platforms are in a real race:

| Platform | The "qubit" is… | Pros | Cons |
|---|---|---|---|
| **Superconducting** (IBM, Google) | current/charge in a chip-etched LC circuit | fast gates, leverages chip fab | needs ~15 mK (colder than deep space); short coherence |
| **Trapped ions** (IonQ, Quantinuum) | electronic state of an ion held by EM fields | very long coherence, high fidelity, all-to-all connectivity | slower gates, harder to scale qubit count |
| **Photonic** (PsiQuantum, Xanadu) | a photon (polarization/path) | room temperature, naturally mobile | photons don't interact → two-qubit gates are hard |
| **Neutral atoms** (QuEra, Pasqal) | atoms trapped by laser tweezers | flexible geometry, scales to 100s | younger tech, gate fidelities improving |
| **Topological** (Microsoft) | non-local "anyon" states | error-resistant *by physics* | still largely unproven experimentally |

There's no winner yet. Superconducting and trapped-ion are the most mature; the field is
genuinely uncertain which scales to a million qubits.

## The core enemy: decoherence

A qubit's superposition is exquisitely fragile. Any uncontrolled interaction with the
environment — a stray photon, a vibration, a magnetic fluctuation, heat — leaks information
about the qubit's state into the surroundings. From note 02, leaking "which state" information
is effectively a **measurement**, and it **collapses** the superposition. This is
**decoherence**.

```
 clean superposition  ──environment interacts──►  effectively measured  ──►  collapsed → garbage
 α|0⟩ + β|1⟩                                                                  just 0 or 1, randomly
```

Two clocks define the problem:

- **Coherence time (`T₁`, `T₂`):** how long a qubit keeps its quantum state — microseconds to
  seconds depending on platform. You must finish the computation before this runs out.
- **Gate time:** how long one gate takes — nanoseconds to microseconds.

The ratio (coherence time ÷ gate time) caps how many gates you can run before the state rots:
maybe hundreds to thousands today. Real algorithms (Shor on a meaningful key) need **billions**.
That gap is *the* central challenge of the field.

## Gates are noisy too

Beyond decoherence, every gate is **imperfect** — a rotation is slightly off, a pulse is
slightly miscalibrated. Today's best two-qubit gate error rates are roughly **0.1%–1%** per
gate. Errors **accumulate**: run 1,000 gates at 0.1% each and you expect roughly one error
per run — enough to ruin the answer. You cannot just "be more careful"; you need a way to
*detect and fix* errors mid-computation.

## Quantum error correction (QEC)

Classical computers fix errors by **copying** (majority vote over 3 copies). Quantum can't do
that — **no-cloning** (note 02) forbids copying an unknown state, and you can't even *look* at
a qubit to check it without collapsing it. QEC is the ingenious way around both walls:

```
Idea: spread ONE logical qubit's information across MANY physical qubits via entanglement,
      so no single physical qubit holds the whole state.

Then measure CLEVERLY-CHOSEN combinations ("syndromes" / parity checks) that reveal
      WHETHER an error happened and WHERE — WITHOUT revealing the encoded data itself.
      (You measure relationships between qubits, not the qubits' values.)

Then apply a correcting gate. The logical qubit survives.
```

The catch is the **overhead**. Protecting one good ("logical") qubit can take hundreds to
**thousands** of physical qubits, depending on physical error rate and the code (the
**surface code** is the leading candidate). So a machine that needs ~1,000 *logical* qubits
to run Shor on RSA-2048 might need **millions** of *physical* qubits. That's why current
~100–1000-qubit machines, impressive as they are, can't yet break encryption.

### The threshold theorem (the reason it's possible at all)

QEC only helps if your physical qubits are *already* good enough. The **threshold theorem**
says: if the physical error rate is **below a critical threshold** (~1% for the surface code),
then adding more qubits to the code drives the *logical* error rate **arbitrarily low** — you
can compute reliably for as long as you like. Above the threshold, more qubits make things
*worse*. Hardware has recently crossed below threshold on small codes (Google's 2023–2024
surface-code demonstrations showed the logical error rate *dropping* as the code grew —
"below threshold" experimentally), which is the milestone that makes scaled fault tolerance
plausible rather than hypothetical.

## Where we actually are: the NISQ era

Today's machines are **NISQ** — **N**oisy **I**ntermediate-**S**cale **Q**uantum (a term coined
by John Preskill, 2018):

- **Noisy:** no full error correction yet; errors limit circuit depth.
- **Intermediate-scale:** ~50 to ~1000+ physical qubits — too many to simulate classically by
  brute force, too few (and too noisy) for fault-tolerant algorithms like Shor.

What NISQ can and can't do:

- ✅ **"Quantum supremacy/advantage" demos:** Google (2019) and others ran *specific, contrived*
  sampling tasks faster than the best classical supercomputers. Important proof-of-principle —
  but **not useful** computations, and several have since been partly challenged by improved
  classical methods.
- 🟡 **Hybrid algorithms** (VQE, QAOA — note 05): run a shallow quantum circuit, optimize its
  parameters on a classical computer, repeat. Designed to squeeze value out of noisy hardware.
  Real research, **no proven advantage** on useful problems yet.
- ❌ **Breaking RSA, large-scale Shor, big Grover:** need fault tolerance → **not** NISQ → years
  to decades away.

## Honest timeline and hype-check

- **Real:** the physics works; entanglement and small algorithms run on hardware daily;
  error rates are falling; "below threshold" has been demonstrated. Steady, fundable progress.
- **Hard:** scaling from ~1,000 noisy qubits to ~1,000,000 high-quality ones is a colossal
  engineering problem (wiring, cooling, control electronics, fabrication yield, crosstalk).
- **Hype to distrust:** "quantum will speed up *all* computing / AI / everything soon." No —
  it's a **specialized** accelerator for structured problems (note 05), and useful
  fault-tolerant machines are likely **a decade or more** out. Anyone giving a confident near
  date is guessing.
- **Act-on-it-now:** **post-quantum cryptography**. Because of "harvest now, decrypt later,"
  NIST has already standardized classical PQC algorithms (e.g. **ML-KEM/Kyber**,
  **ML-DSA/Dilithium**) and migration is underway today — the one place the quantum threat
  demands action well before the hardware exists.

## Mental checklist

- [ ] Multiple hardware platforms (superconducting, ion, photonic, neutral-atom, topological); no winner yet.
- [ ] **Decoherence** = environment "measures" the qubit and collapses it; coherence time is the budget.
- [ ] Gates are noisy (~0.1–1% error) and errors **accumulate** over a circuit.
- [ ] **QEC** spreads one logical qubit over many physical ones; measures *syndromes*, not data; huge overhead.
- [ ] **Threshold theorem**: below ~1% physical error, scaling the code drives logical error → 0. Recently demonstrated.
- [ ] We're in the **NISQ** era — useful but noisy; fault-tolerant Shor-scale machines are years/decades away.
- [ ] Act now on **post-quantum cryptography**; distrust "quantum speeds up everything soon."

**Back to:** [README](./README.md) · open the **[animation](./animation/index.html)** to see the
ideas in motion.
