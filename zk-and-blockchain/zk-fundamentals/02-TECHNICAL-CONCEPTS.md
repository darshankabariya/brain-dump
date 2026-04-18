# Technical Deep Dive: ZK Proof Systems

## Table of Contents
1. [SNARKs vs STARKs: The Great Divide](#snarks-vs-starks-the-great-divide)
2. [SNARK Variants Explained](#snark-variants-explained)
3. [STARK Variants Explained](#stark-variants-explained)
4. [ZK-EVMs: Type 1 through Type 4](#zk-evms-type-1-through-type-4)
5. [Polynomial Commitment Schemes](#polynomial-commitment-schemes)
6. [Recursion and Aggregation](#recursion-and-aggregation)
7. [Performance Characteristics](#performance-characteristics)

---

## SNARKs vs STARKs: The Great Divide

### ZK-SNARKs (Succinct Non-interactive ARguments of Knowledge)

**Core Idea**: Use elliptic curve pairings to create tiny proofs

```
Key Properties:
✅ Proof size: ~200-300 bytes (extremely small)
✅ Verification: ~1-2 milliseconds (very fast)
✅ Mature ecosystem: More tooling and libraries
❌ Trusted setup: Most require ceremony (security assumption)
❌ Quantum vulnerable: Based on elliptic curves
❌ Prover time: Can be slow for large circuits
```

**Mathematical Foundation**:
- Elliptic curve cryptography
- Pairing-based cryptography (e.g., BLS12-381 curve)
- Polynomial commitments via KZG

**When to Use SNARKs**:
- Need minimal proof size (on-chain storage)
- Fast verification is critical
- Quantum resistance not a concern (near-term)
- Willing to accept trusted setup

### ZK-STARKs (Scalable Transparent ARguments of Knowledge)

**Core Idea**: Use hash functions and algebraic techniques (no elliptic curves)

```
Key Properties:
✅ Transparent: No trusted setup needed
✅ Quantum resistant: Based on hash functions
✅ Scalable prover: Better for very large computations
✅ Simpler assumptions: Only relies on hash security
❌ Proof size: ~100-200 KB (much larger)
❌ Verification: Slower than SNARKs
❌ Less mature: Fewer production implementations
```

**Mathematical Foundation**:
- Hash functions (e.g., Poseidon, Rescue)
- Reed-Solomon codes
- FRI (Fast Reed-Solomon Interactive Oracle Proof)

**When to Use STARKs**:
- Transparency is critical
- Quantum resistance matters
- Very large computations (millions of gates)
- Proof size less important (off-chain verification)

---

## SNARK Variants Explained

### 1. Groth16

**Status**: Most widely used SNARK (as of 2024)

```
Characteristics:
• Proof size: ~200 bytes (smallest)
• Verification: ~1 ms (fastest)
• Setup: Circuit-specific trusted setup
• Prover time: Moderate
```

**How It Works**:
1. Trusted setup generates proving key (pk) and verification key (vk)
2. Prover uses pk to create proof from witness
3. Verifier uses vk to check proof (3 pairing checks)

**Trusted Setup**:
```
Phase 1: Powers of Tau (universal, one-time)
    ↓
Phase 2: Circuit-specific (per application)
```

**Use Cases**:
- Zcash (shielded transactions)
- Tornado Cash (privacy mixer)
- Filecoin (proof of storage)

**Limitations**:
- New circuit = new trusted setup
- Not updatable
- No recursion support

### 2. PLONK (Permutations over Lagrange-bases for Oecumenical Noninteractive arguments of Knowledge)

**Status**: Modern, flexible SNARK

```
Characteristics:
• Proof size: ~400-800 bytes
• Verification: ~2-3 ms
• Setup: Universal trusted setup (reusable!)
• Prover time: Moderate
• Custom gates: Supported
```

**Key Innovation**: Universal setup
```
One setup → Use for ANY circuit (up to size limit)
```

**How It Works**:
1. Universal setup (one-time, size-bounded)
2. Circuit compiled to PLONK gates
3. Copy constraints enforce wire connections
4. Polynomial commitments via KZG

**Advantages over Groth16**:
- ✅ Universal setup (reusable)
- ✅ Custom gates (more efficient circuits)
- ✅ Updatable setup
- ✅ Easier to audit

**Use Cases**:
- Aztec Network (privacy rollup)
- Mina Protocol (recursive proofs)
- zkSync Era (some components)

**Variants**:
- **TurboPLONK**: Custom gates
- **UltraPLONK**: Lookup tables
- **HyperPLONK**: Multivariate polynomials

### 3. Halo2

**Status**: Cutting-edge, no trusted setup

```
Characteristics:
• Proof size: ~10-50 KB
• Verification: ~10-50 ms
• Setup: None! (transparent)
• Prover time: Moderate to high
• Recursion: Native support
```

**Key Innovation**: IPA (Inner Product Argument) instead of KZG
```
No trusted setup + Recursion = Infinite scalability
```

**How It Works**:
1. No setup phase needed
2. Polynomial commitments via IPA (Bulletproofs-style)
3. Recursive proof composition built-in
4. Amortized verification via accumulation

**Advantages**:
- ✅ No trusted setup
- ✅ Native recursion
- ✅ Flexible circuit design
- ✅ Updatable circuits

**Trade-offs**:
- ❌ Larger proofs than Groth16/PLONK
- ❌ Slower verification
- ❌ More complex to implement

**Use Cases**:
- Zcash (Orchard protocol)
- Scroll (zkEVM)
- Axiom (ZK coprocessor)

### 4. Marlin

**Status**: Academic, high-performance

```
Characteristics:
• Proof size: ~600 bytes
• Verification: ~2-3 ms
• Setup: Universal, updatable
• Prover time: Fast
```

**Key Features**:
- Preprocessing SNARK
- Universal setup
- Fast prover (better than PLONK)

**Use Cases**:
- Aleo (privacy-focused blockchain)
- Research implementations

### 5. Bulletproofs

**Status**: No setup, but slower

```
Characteristics:
• Proof size: ~1-2 KB (logarithmic in circuit size)
• Verification: ~50-100 ms (slower)
• Setup: None
• Prover time: Moderate
```

**Key Feature**: Logarithmic proof size without trusted setup

**Use Cases**:
- Monero (range proofs)
- Confidential transactions
- When setup is unacceptable but proof size matters

**Limitations**:
- Slower verification than pairing-based SNARKs
- Not ideal for very large circuits

---

## STARK Variants Explained

### 1. FRI-based STARKs (Original)

**Status**: Production-ready (StarkWare)

```
Characteristics:
• Proof size: ~100-200 KB
• Verification: ~10-20 ms
• Setup: None
• Prover time: Fast for large circuits
• Quantum resistant: Yes
```

**How It Works**:
1. Execution trace → Polynomial
2. Extend polynomial (Reed-Solomon encoding)
3. FRI protocol proves low-degree
4. Verifier checks via random sampling

**FRI Protocol** (Fast Reed-Solomon IOP):
```
Prover commits to polynomial
    ↓
Verifier sends random challenge
    ↓
Prover "folds" polynomial (reduces degree)
    ↓
Repeat until degree is small
    ↓
Verifier checks consistency
```

**Use Cases**:
- StarkNet (L2 rollup)
- StarkEx (application-specific rollups)
- Polygon Miden (ZK-VM)

### 2. DEEP-FRI

**Status**: Improved FRI variant

**Improvements**:
- Better soundness analysis
- Smaller proof size (optimization)
- More efficient queries

### 3. Plonky2

**Status**: Recursive STARK system

```
Characteristics:
• Proof size: ~50-100 KB
• Verification: ~5-10 ms
• Recursion: Very fast (~170ms per level)
• Setup: None
```

**Key Innovation**: Combines PLONK-style gates with FRI
```
PLONK gates (flexibility) + FRI (transparency) = Best of both
```

**Recursion Performance**:
```
Traditional SNARKs: ~30 seconds per recursion level
Plonky2: ~170 milliseconds per recursion level
```

**Use Cases**:
- Polygon zkEVM (Type 3)
- Recursive proof systems
- High-throughput applications

### 4. Plonky3

**Status**: Next-generation framework (2024)

**Improvements**:
- Modular design (swap components)
- Multiple field support
- Better performance
- Easier to customize

**Architecture**:
```
┌─────────────────────────────────────┐
│  Frontend (Circuit Definition)     │
├─────────────────────────────────────┤
│  AIR (Constraint System)            │
├─────────────────────────────────────┤
│  PCS (Polynomial Commitment)        │
│  • FRI                              │
│  • KZG                              │
│  • Other options                    │
└─────────────────────────────────────┘
```

---

## ZK-EVMs: Type 1 through Type 4

**Goal**: Run Ethereum smart contracts with ZK proofs

### Type 1: Fully Ethereum-Equivalent

```
Compatibility: 100% (even consensus layer)
Performance: Slowest
Example: None in production yet (research)
```

**Characteristics**:
- Proves entire Ethereum protocol
- No modifications to EVM
- Can verify Ethereum L1 blocks

**Challenge**: EVM not designed for ZK (very expensive to prove)

**Projects**:
- PSE zkEVM (research)
- Taiko (aims for Type 1)

### Type 2: Fully EVM-Equivalent

```
Compatibility: 100% (EVM level)
Performance: Slow
Example: Scroll, Polygon zkEVM (Type 2.5)
```

**Characteristics**:
- Identical EVM execution
- Same gas costs
- Different data structures (Merkle Patricia Trie → Poseidon tree)

**Trade-off**: Slower proving for perfect compatibility

**Projects**:
- Scroll (Halo2-based)
- Polygon zkEVM (Plonky2-based, Type 2.5)

### Type 3: Almost EVM-Equivalent

```
Compatibility: ~99% (minor differences)
Performance: Moderate
Example: Polygon zkEVM, Scroll (hybrid)
```

**Modifications**:
- Different hash functions (Keccak → Poseidon)
- Simplified precompiles
- Modified gas costs

**Benefit**: Faster proving, minimal compatibility loss

### Type 4: High-Level Language Equivalent

```
Compatibility: ~95% (source code level)
Performance: Fast
Example: zkSync Era, StarkNet
```

**Characteristics**:
- Compiles Solidity to custom bytecode
- Different VM architecture
- Optimized for ZK proving

**zkSync Era**:
```
Solidity → zkSync compiler → zkEVM bytecode → ZK proof
```

**StarkNet**:
```
Solidity → Cairo → CairoVM execution → STARK proof
```

**Trade-offs**:
- ✅ Much faster proving
- ✅ Lower costs
- ❌ Some incompatibilities
- ❌ Tooling differences

### Comparison Table

| Type | Compatibility | Proving Time | Gas Cost | Example |
|------|---------------|--------------|----------|---------|
| **Type 1** | 100% (L1) | Very Slow | High | Research |
| **Type 2** | 100% (EVM) | Slow | Medium-High | Scroll |
| **Type 2.5** | ~99.9% | Moderate | Medium | Polygon zkEVM |
| **Type 3** | ~99% | Moderate | Medium | Hybrid approaches |
| **Type 4** | ~95% | Fast | Low | zkSync Era, StarkNet |

---

## Polynomial Commitment Schemes

**Purpose**: Commit to a polynomial without revealing it, then prove evaluations

### KZG (Kate-Zaverucha-Goldberg)

```
Properties:
• Proof size: O(1) - constant (48 bytes)
• Verification: O(1) - 2 pairing checks
• Setup: Trusted setup required
• Opening: Single group element
```

**How It Works**:
```
Setup: Generate [g^(τ^i)] for i = 0 to n (τ is secret, discarded)
Commit: C = g^(p(τ)) for polynomial p(x)
Open: Prove p(z) = y by providing π = g^((p(τ)-y)/(τ-z))
Verify: Check pairing equation
```

**Used In**: Groth16, PLONK, Proto-Danksharding (EIP-4844)

### FRI (Fast Reed-Solomon IOP)

```
Properties:
• Proof size: O(log n) - logarithmic
• Verification: O(log n) - query-based
• Setup: None (transparent)
• Opening: Multiple Merkle proofs
```

**How It Works**:
```
1. Commit polynomial via Merkle tree
2. Iteratively "fold" polynomial
3. Prove low-degree via random sampling
4. Verifier checks consistency
```

**Used In**: STARKs, Plonky2, Plonky3

### IPA (Inner Product Argument)

```
Properties:
• Proof size: O(log n)
• Verification: O(n) naive, O(log n) amortized
• Setup: None
• Opening: Recursive argument
```

**How It Works**:
```
Reduce polynomial opening to inner product
Recursively halve the problem
Base case: trivial verification
```

**Used In**: Halo2, Bulletproofs

### Comparison

| Scheme | Proof Size | Verification | Setup | Quantum Safe |
|--------|------------|--------------|-------|--------------|
| **KZG** | O(1) ~48B | O(1) ~2ms | Trusted | ❌ |
| **FRI** | O(log n) ~100KB | O(log n) ~10ms | None | ✅ |
| **IPA** | O(log n) ~10KB | O(n) or O(log n) | None | ❌ |

---

## Recursion and Aggregation

### Why Recursion Matters

**Problem**: Verifying many proofs is expensive
```
1000 transactions × 2ms verification = 2 seconds
```

**Solution**: Prove that you verified proofs correctly
```
1000 proofs → 1 recursive proof → 2ms verification
```

### Proof Aggregation

**Concept**: Combine multiple proofs into one

```
Proof₁ (tx 1-100)  ┐
Proof₂ (tx 101-200)├─→ Aggregated Proof → Single verification
Proof₃ (tx 201-300)┘
```

**Techniques**:
1. **Batch Verification**: Verify multiple proofs together (faster)
2. **Proof Aggregation**: Create new proof that proves "all these proofs are valid"
3. **Recursive Composition**: Proof of proof verification

### Recursive Proof Composition

**Level 0**: Base proofs (individual transactions)
```
[Proof₁] [Proof₂] [Proof₃] [Proof₄] ... [Proof₁₀₀₀]
```

**Level 1**: Aggregate 10 proofs each
```
[Proof₁₋₁₀] [Proof₁₁₋₂₀] ... [Proof₉₉₁₋₁₀₀₀]
```

**Level 2**: Aggregate 10 level-1 proofs
```
[Proof₁₋₁₀₀] [Proof₁₀₁₋₂₀₀] ... [Proof₉₀₁₋₁₀₀₀]
```

**Level 3**: Final proof
```
[Proof₁₋₁₀₀₀] → Verify on-chain
```

**Result**: 1000 proofs → 3 recursion levels → 1 final proof

### Systems with Good Recursion

| System | Recursion Speed | Method |
|--------|-----------------|--------|
| **Halo2** | Moderate | Native IPA recursion |
| **Plonky2** | Very Fast (~170ms) | FRI + custom gates |
| **Groth16** | Slow (not native) | Prove pairing checks in circuit |
| **PLONK** | Moderate | Prove KZG checks in circuit |

---

## Performance Characteristics

### Proof Generation Time

**Factors**:
1. Circuit size (number of constraints)
2. Proof system (SNARK vs STARK)
3. Hardware (CPU, GPU, FPGA)

**Typical Times** (for 1M constraints):

| System | CPU | GPU | FPGA |
|--------|-----|-----|------|
| **Groth16** | ~30s | ~3s | ~1s |
| **PLONK** | ~40s | ~4s | ~1.5s |
| **Halo2** | ~50s | ~5s | ~2s |
| **STARKs** | ~20s | ~2s | ~0.5s |

**Note**: STARKs scale better for very large circuits

### Verification Time

**On-chain verification** (Ethereum):

| System | Gas Cost | Time |
|--------|----------|------|
| **Groth16** | ~250K gas | ~1-2ms |
| **PLONK** | ~300K gas | ~2-3ms |
| **Halo2** | ~500K gas | ~5-10ms |
| **STARKs** | ~2M gas | ~10-20ms |

### Memory Requirements

**Prover Memory**:
```
Groth16: ~2GB for 1M constraints
PLONK:   ~3GB for 1M constraints
Halo2:   ~4GB for 1M constraints
STARKs:  ~5GB for 1M constraints
```

**Verifier Memory**:
```
All systems: <100MB (very light)
```

### Scalability Curves

**Proof Size vs Circuit Size**:
```
SNARKs: O(1) - constant
STARKs: O(log² n) - polylogarithmic
Bulletproofs: O(log n) - logarithmic
```

**Prover Time vs Circuit Size**:
```
All systems: O(n log n) to O(n²)
STARKs: Better constants for large n
```

**Verifier Time vs Circuit Size**:
```
SNARKs: O(1) - constant
STARKs: O(log² n) - polylogarithmic
```

---

## Choosing the Right System

### Decision Tree

```
Need smallest proofs? → Groth16
    ↓ No
Need no trusted setup? → STARKs or Halo2
    ↓ No
Need fast recursion? → Plonky2
    ↓ No
Need EVM compatibility? → Type 2/3 zkEVM
    ↓ No
Need flexibility? → PLONK or Halo2
    ↓ No
Need quantum resistance? → STARKs
```

### Use Case Recommendations

| Use Case | Recommended System | Why |
|----------|-------------------|-----|
| **Privacy coins** | Groth16 | Smallest proofs, proven security |
| **ZK Rollups** | PLONK/STARKs | Balance of size and transparency |
| **Identity** | Groth16/PLONK | Small proofs for mobile |
| **Large computation** | STARKs | Scales better |
| **Recursive systems** | Plonky2/Halo2 | Native recursion |
| **EVM compatibility** | Type 2-4 zkEVM | Depends on compatibility needs |

---

## Key Takeaways

1. **SNARKs vs STARKs**: Size vs transparency trade-off
2. **No perfect system**: Every choice has trade-offs
3. **Recursion is crucial**: Enables infinite scalability
4. **zkEVM types**: Compatibility vs performance spectrum
5. **Polynomial commitments**: Core primitive with different properties
6. **Hardware matters**: GPUs/FPGAs dramatically improve proving time

---

## Next Steps

- **Research**: Read `03-RESEARCH-AND-RESEARCHERS.md` for academic foundations
- **Projects**: See `04-COMPANIES-AND-PROJECTS.md` for who uses what
- **Applications**: Check `05-APPLICATIONS-AND-USE-CASES.md` for real-world examples

---

**Further Reading**:
- [Comparing ZK-SNARKs](https://www.zeroknowledgeblog.com/index.php/zk-snarks) - Technical comparison
- [STARKs vs SNARKs](https://consensys.net/blog/blockchain-explained/zero-knowledge-proofs-starks-vs-snarks/) - Consensys guide
- [The Different Types of ZK-EVMs](https://vitalik.ca/general/2022/08/04/zkevm.html) - Vitalik Buterin
