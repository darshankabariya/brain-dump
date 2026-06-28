# 05 — Algorithms

> This is where it pays off. A quantum algorithm is an arrangement of gates that uses
> **interference** to make the right answer's amplitude large and the wrong answers' amplitudes
> small — *before* the single measurement. Speed-ups come from clever interference, never from
> "trying all answers and reading them all" (you can't — note 02).

## The universal recipe

Almost every quantum algorithm has the same three-act shape:

```
1. SUPERPOSE   Hadamards put the register in an equal mix of all 2ⁿ inputs.
2. COMPUTE +   A unitary writes problem structure into amplitudes/phases, then more gates
   INTERFERE   make wrong answers cancel (destructive) and right ones reinforce (constructive).
3. MEASURE     One readout. With high probability you get the answer (or info that yields it).
```

Act 2 is the art. "Quantum parallelism" (evaluating a function on all inputs at once via
superposition) is *necessary but worthless on its own* — you'd just measure a random input.
The win is the **interference** that follows.

## Warm-up: Deutsch's algorithm (why interference, not parallelism, wins)

The toy problem that isolates the trick. You're given a black-box function
`f: {0,1} → {0,1}` and asked: **is `f` constant** (`f(0)=f(1)`) **or balanced** (`f(0)≠f(1)`)?

- **Classically:** you must evaluate `f` **twice** (check both `f(0)` and `f(1)`).
- **Quantum:** **one** evaluation suffices.

How? Put the input qubit in superposition with H, apply `f` in a way that writes its result
into a **phase** (phase kickback), then apply H again. The two H's create an interference:

```
if f is constant  →  the |1⟩ amplitudes cancel  →  you measure 0 with certainty
if f is balanced  →  the |0⟩ amplitudes cancel  →  you measure 1 with certainty
```

You never learned `f(0)` or `f(1)` individually — that information cancelled out. You learned a
**global property** of `f` from a single query, because interference let the two cases steer
amplitude to *different* measurement outcomes. That's the entire game, in miniature. Its
generalization, **Deutsch–Jozsa**, separates 1 quantum query from `2ⁿ⁻¹+1` classical queries.

## Grover's algorithm — quadratic speed-up for search

**Problem:** find the one marked item in an unsorted database of `N` items (equivalently, find
the input that makes a black-box function output 1).

- **Classically:** no structure to exploit → on average `N/2` checks, worst case `N`. `O(N)`.
- **Grover:** `O(√N)`. For a million items, ~1000 steps instead of ~1,000,000.

### How it works — amplitude amplification

Start in the equal superposition of all `N` candidates (amplitude `1/√N` each). Then repeat a
two-step **Grover iteration** about `√N` times:

```
1. ORACLE     Flip the PHASE of the marked item:  its amplitude  +1/√N → −1/√N
              (everything else unchanged). Invisible to measurement so far — pure phase.

2. DIFFUSION  "Reflect about the average amplitude." Geometrically this rotates the whole
              state vector slightly toward the marked item, GROWING its amplitude and
              shrinking the rest.
```

Picture the amplitudes as bars; `★` is the marked item:

```
start:     ▁ ▁ ▁ ▁ ★▁ ▁ ▁       all equal (1/√N)
oracle:    ▁ ▁ ▁ ▁ ★▔ ▁ ▁       marked bar flipped below the line (phase −)
diffuse:   ▁ ▁ ▁ ▁ ★▃ ▁ ▁       reflect about average → marked bar grows, others shrink
…repeat √N times…
end:       . . . . ★█ . . .      almost all amplitude on the marked item → measure it
```

Each iteration rotates the state by a fixed small angle (~`1/√N`) toward the answer; after
~`(π/4)√N` iterations it's nearly aligned, and you measure the marked item with high
probability. (Watch out: too *many* iterations rotate *past* the target and the success
probability drops again — interference cuts both ways.) Grover is provably optimal:
**no** quantum algorithm beats `O(√N)` for unstructured search.

## Shor's algorithm — exponential speed-up for factoring

The headline result, and the reason governments fund quantum computing. **Factor a large
integer `N`** (e.g. the product of two ~1024-bit primes behind RSA).

- **Classically:** best known (general number field sieve) is **sub-exponential** —
  effectively intractable for big keys; this hardness is what RSA security rests on.
- **Shor:** **polynomial** time. It breaks RSA.

### The clever reduction

Shor doesn't attack factoring head-on. It reduces it to **period-finding**:

```
1. (classical) Factoring N reduces to finding the PERIOD r of the function
               f(x) = aˣ mod N,  for a random a.   (Once you know r, simple
               classical math extracts a factor of N with good probability.)

2. (quantum)   Find the period r FAST using the Quantum Fourier Transform (QFT).
```

The QFT is the quantum engine. Prepare a superposition over many `x`, compute `aˣ mod N` into
a second register (entangling input and output), and the **periodic structure** of `f` shows
up as a periodic pattern in the amplitudes. The QFT is an interference operation that converts
"period in the amplitudes" into a **sharp peak at a frequency related to `r`**. Measure, get
the frequency, do classical post-processing (continued fractions) to recover `r`, and factor.

```
 superposition over x  ──compute aˣ mod N──►  amplitudes are PERIODIC in x (period r)
        │                                                │
        └──────── QFT (interference) ──────────────►  sharp peaks at multiples of N/r
                                                         │
                                              measure → frequency → r → factor of N
```

The QFT runs in `O((log N)²)` gates — exponentially faster than any known classical Fourier
attack on this structure. **Period-finding is the source of the exponential speed-up.** The
same machinery (the *hidden subgroup problem*) underlies the discrete-log break, which also
kills Diffie–Hellman and elliptic-curve crypto. Hence **post-quantum cryptography** — new
classical schemes believed safe against Shor — is being standardized *now*, years before a
big enough quantum computer exists, because encrypted data harvested today could be decrypted
later ("harvest now, decrypt later").

## Other important families

- **Quantum simulation** (Feynman's original 1981 motivation): simulate quantum *physics* —
  molecules, materials, chemistry. Quantum systems are exponentially hard to simulate
  classically but *natural* for a quantum computer. Likely the **first** truly useful
  application (drug design, catalysts, batteries).
- **HHL / quantum linear algebra:** solve certain linear systems with exponential speed-up —
  but with heavy fine print (the answer is a quantum state, not a readable vector). Caveat-laden.
- **Variational / NISQ algorithms (VQE, QAOA):** hybrid quantum-classical loops designed to do
  *something useful on noisy, small machines* before full error correction exists (note 06).
  Speed-up is heuristic, not proven.

## The honest scorecard — where quantum actually helps

Quantum computers are **not** "faster at everything." They help only where a problem has
structure that interference can exploit:

| Problem | Classical | Quantum | Speed-up | Real-world status |
|---|---|---|---|---|
| Factoring / discrete log | sub-exponential | polynomial (Shor) | **exponential** | breaks RSA/ECC — needs large fault-tolerant machine |
| Unstructured search | `O(N)` | `O(√N)` (Grover) | quadratic | modest; useful as a subroutine |
| Simulating quantum systems | exponential | polynomial | **exponential** | likely first killer app |
| Linear systems (HHL) | `O(N)` | `O(log N)`* | exponential* | *huge caveats on I/O |
| Sorting, most everyday tasks | optimal already | no better | **none** | classical wins |

Key honesty: for the vast majority of computing — databases, web, ML training as we do it
today, sorting, arithmetic — quantum offers **no advantage**. It's a specialized accelerator
for a few structured problems, not a faster CPU.

## See it move

The animation's **Grover** panel runs amplitude amplification on a small search space: watch
the marked item's bar grow each iteration, peak, and (if you over-iterate) shrink again — the
geometry of "rotate toward the answer" made visible.

## Mental checklist

- [ ] Recipe: superpose → interfere (cancel wrong, reinforce right) → measure once.
- [ ] Quantum *parallelism* alone is useless; **interference** is what extracts an answer.
- [ ] Deutsch: one query for a global property — the interference trick in miniature.
- [ ] Grover: `O(√N)` search via amplitude amplification (provably optimal; don't over-iterate).
- [ ] Shor: polynomial factoring via period-finding + QFT → **exponential**, breaks RSA.
- [ ] Quantum helps only on structured problems; for most tasks, classical is as good or better.

**Next:** [06 — Hardware and Challenges](./06-hardware-and-challenges.md): why building one is so
hard, decoherence, error correction, and the NISQ era we're actually in.
