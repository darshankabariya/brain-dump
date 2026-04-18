# Proof Systems Comparison: Visual Guide

## SNARKs vs STARKs: The Complete Comparison

### Quick Reference Matrix

| Feature | Groth16 | PLONK | Halo2 | STARKs | Bulletproofs |
|---------|---------|-------|-------|--------|--------------|
| **Proof Size** | ~200B | ~400B | ~10KB | ~100KB | ~1-2KB |
| **Verification** | ~1ms | ~2ms | ~10ms | ~20ms | ~50ms |
| **Prover Time** | Medium | Medium | Medium-High | Fast (large) | Medium |
| **Trusted Setup** | Yes (circuit) | Yes (universal) | No | No | No |
| **Recursion** | Hard | Moderate | Native | Good | Hard |
| **Quantum Safe** | No | No | No | Yes | No |
| **Maturity** | High | High | Medium | Medium | Medium |

### Visual Comparison

```
PROOF SIZE (Smaller is Better)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Groth16      ▓ 200 bytes
PLONK        ▓▓ 400 bytes
Bulletproofs ▓▓▓▓▓ 1-2 KB
Halo2        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 10-50 KB
STARKs       ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 100-200 KB

VERIFICATION TIME (Faster is Better)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Groth16      ▓ 1-2 ms
PLONK        ▓▓ 2-3 ms
Halo2        ▓▓▓▓▓ 5-10 ms
STARKs       ▓▓▓▓▓▓▓▓▓▓ 10-20 ms
Bulletproofs ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 50-100 ms

TRANSPARENCY (More is Better)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Groth16      ▓▓▓▓▓ Circuit-specific trusted setup
PLONK        ▓▓▓▓▓▓▓▓ Universal trusted setup
Halo2        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ No trusted setup
Bulletproofs ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ No trusted setup
STARKs       ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ Fully transparent
```

## Decision Tree

```
                    START
                      │
        ┌─────────────┴─────────────┐
        │                           │
   Need smallest     Need transparency
   proof size?       or no setup?
        │                           │
       YES                         YES
        │                           │
        ▼                           ▼
   ┌─────────┐              ┌──────────┐
   │ SNARKs  │              │ STARKs   │
   │         │              │ or       │
   │ Groth16 │              │ Halo2    │
   │ PLONK   │              │          │
   └─────────┘              └──────────┘
```

## Use Case Recommendations

```
┌────────────────────────────────────────────────────────┐
│ PRIVACY PAYMENTS (Zcash, Tornado Cash)                │
│ → Groth16: Smallest proofs, proven security           │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│ ZK ROLLUPS (zkSync, StarkNet, Polygon)                │
│ → PLONK or STARKs: Balance size/transparency           │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│ RECURSIVE SYSTEMS (Mina, Scroll)                      │
│ → Halo2 or Plonky2: Native recursion                  │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│ LARGE COMPUTATION (zkVMs, complex circuits)           │
│ → STARKs: Better scaling for large circuits           │
└────────────────────────────────────────────────────────┘
```
