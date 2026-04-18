# ZK Quick Reference Cheat Sheet

> **Use this when reading tweets, blogs, or papers to quickly look up unfamiliar terms**

## Common Terms & Acronyms

| Term | Full Name | What It Means |
|------|-----------|---------------|
| **ZK** | Zero-Knowledge | Prove something without revealing information |
| **SNARK** | Succinct Non-interactive ARgument of Knowledge | Small proofs, fast verification, usually needs trusted setup |
| **STARK** | Scalable Transparent ARgument of Knowledge | Larger proofs, no trusted setup, quantum-resistant |
| **zkEVM** | Zero-Knowledge Ethereum Virtual Machine | Run Ethereum smart contracts with ZK proofs |
| **zkVM** | Zero-Knowledge Virtual Machine | General-purpose VM that generates ZK proofs |
| **PCS** | Polynomial Commitment Scheme | How to commit to polynomials (KZG, FRI, IPA) |
| **R1CS** | Rank-1 Constraint System | Way to represent circuits (used in SNARKs) |
| **AIR** | Algebraic Intermediate Representation | Way to represent computation (used in STARKs) |
| **FRI** | Fast Reed-Solomon IOP | Core STARK protocol |
| **KZG** | Kate-Zaverucha-Goldberg | Polynomial commitment (needs trusted setup) |
| **IPA** | Inner Product Argument | Polynomial commitment (no setup, used in Halo2) |

## Proof Systems Quick Lookup

| System | Size | Speed | Setup | Use Case |
|--------|------|-------|-------|----------|
| **Groth16** | 200B | 1ms | Trusted | Zcash, Tornado Cash |
| **PLONK** | 400B | 2ms | Universal | zkSync, Aztec |
| **Halo2** | 10KB | 10ms | None | Scroll, Zcash Orchard |
| **STARKs** | 100KB | 20ms | None | StarkNet, Miden |
| **Plonky2** | 50KB | 5ms | None | Polygon zkEVM |

## Companies & What They Do

| Company | What They Build | Tech Stack |
|---------|-----------------|------------|
| **zkSync (Matter Labs)** | Type 4 zkEVM rollup | PLONK/Boojum |
| **StarkWare** | StarkNet (rollup) + StarkEx | STARKs, Cairo |
| **Polygon** | zkEVM + Miden VM | Plonky2, STARKs |
| **Scroll** | Type 2 zkEVM | Halo2 |
| **Aztec** | Privacy rollup + Noir language | PLONK |
| **Succinct** | SP1 zkVM (RISC-V) | PLONK |
| **RISC Zero** | zkVM + Bonsai proving network | STARKs |
| **Aleo** | Private smart contracts | Marlin |
| **Mina** | Succinct blockchain (22KB) | Pickles (recursive) |

## zkEVM Types (Vitalik's Classification)

| Type | Compatibility | Speed | Examples |
|------|---------------|-------|----------|
| **Type 1** | 100% (L1 equivalent) | Slowest | Taiko (goal) |
| **Type 2** | 100% (EVM bytecode) | Slow | Scroll, Polygon zkEVM |
| **Type 2.5** | ~99% (minor changes) | Moderate | Polygon zkEVM |
| **Type 3** | ~95% (some differences) | Moderate | - |
| **Type 4** | ~90% (high-level) | Fast | zkSync, StarkNet |

## Key Researchers (Who to Follow)

| Name | Affiliation | Known For |
|------|-------------|-----------|
| **Dan Boneh** | Stanford | Bulletproofs, BLS signatures |
| **Justin Thaler** | Georgetown, a16z | ZK textbook, sum-check |
| **Eli Ben-Sasson** | StarkWare | STARKs, FRI |
| **Vitalik Buterin** | Ethereum | zkEVM research |
| **Shafi Goldwasser** | MIT | Invented ZK (Turing Award) |
| **Silvio Micali** | MIT | Invented ZK (Turing Award) |
| **Jens Groth** | DFINITY | Groth16 |
| **Ariel Gabizon** | Aztec | PLONK |
| **Sean Bowe** | Zcash | Halo, Halo2 |

## Languages & Frameworks

| Language | Used By | Difficulty | Best For |
|----------|---------|------------|----------|
| **Circom** | Many projects | Medium | General circuits |
| **Noir** | Aztec + others | Easy | Easiest to learn |
| **Cairo** | StarkNet | Medium-Hard | StarkNet development |
| **Leo** | Aleo | Medium | Private apps on Aleo |
| **Halo2** | Scroll, Zcash | Hard | Advanced circuits |
| **Miden ASM** | Polygon Miden | Hard | Miden VM |

## Applications by Category

### Scaling
- zkSync, StarkNet, Polygon zkEVM, Scroll, Linea

### Privacy
- Zcash (payments), Aztec (DeFi), Penumbra (DEX), Tornado Cash

### Identity
- zkPassport, ZK Email, Semaphore, Polygon ID

### Gaming
- Dark Forest, Isaac, Loot Realms

### Governance
- MACI, Snapshot X

### Bridges/Interop
- Succinct Telepathy, Axiom, Brevis, Lagrange

## Foundational Papers

| Year | Paper | Authors | Impact |
|------|-------|---------|--------|
| 1985 | GMR85 | Goldwasser, Micali, Rackoff | Invented ZK |
| 1986 | Fiat-Shamir | Fiat, Shamir | Non-interactive ZK |
| 2013 | Pinocchio | Ben-Sasson et al. | First practical SNARK |
| 2016 | Groth16 | Jens Groth | Most efficient SNARK |
| 2017 | Bulletproofs | Bünz, Boneh et al. | No trusted setup |
| 2018 | STARKs | Ben-Sasson et al. | Transparent, scalable |
| 2019 | PLONK | Gabizon et al. | Universal setup |
| 2019 | Halo | Bowe et al. | Recursive, no setup |
| 2022 | Plonky2 | Polygon Zero | Fast recursion |

## Common Confusion Points

### "Is ZK just for privacy?"
**No.** Main uses: Scaling (rollups), Verification (computation), Privacy (optional)

### "SNARKs vs STARKs - which is better?"
**Neither.** Trade-offs:
- SNARKs: Smaller proofs, faster verification, trusted setup
- STARKs: Transparent, quantum-resistant, larger proofs

### "Do I need math to use ZK?"
**Depends:**
- Using ZK apps: No
- Building ZK apps: Basic understanding
- ZK research: Yes, deep math

### "What's a trusted setup?"
Initial ceremony to generate parameters. Some SNARKs need it, STARKs don't.
- **Circuit-specific** (Groth16): New setup per circuit
- **Universal** (PLONK): One setup, many circuits
- **None** (STARKs, Halo2): No setup needed

## Performance Ballpark Numbers

### Proof Generation (1M constraints)
- Groth16: ~30s (CPU), ~3s (GPU)
- PLONK: ~40s (CPU), ~4s (GPU)
- STARKs: ~20s (CPU), ~2s (GPU)

### Verification
- Groth16: ~1-2ms, ~250K gas
- PLONK: ~2-3ms, ~300K gas
- Halo2: ~5-10ms, ~500K gas
- STARKs: ~10-20ms, ~2M gas

### Proof Size
- Groth16: ~200 bytes
- PLONK: ~400 bytes
- Halo2: ~10-50 KB
- STARKs: ~100-200 KB

## When You See These Terms in Tweets...

### "Recursive proofs"
Proofs that verify other proofs. Enables infinite scalability.

### "Proof aggregation"
Combining multiple proofs into one. Saves verification cost.

### "Trusted setup ceremony"
Community event to generate parameters for SNARKs. If done correctly, secure.

### "Quantum resistant"
Safe against quantum computers. STARKs are, SNARKs aren't.

### "Succinct"
Very small proof size (constant, regardless of computation size).

### "Transparent"
No trusted setup needed. Anyone can verify security.

### "Universal setup"
One setup ceremony works for all circuits (up to size limit).

### "Prover time"
How long to generate a proof. Usually seconds to minutes.

### "Verifier time"
How long to check a proof. Usually milliseconds.

### "Circuit"
How computation is represented for ZK. Like a program.

### "Witness"
Private input to the proof. The secret you're proving about.

### "Constraint"
A rule the circuit must satisfy. More constraints = larger circuit.

## Funding Tiers (Rough Guide)

- **$500M+**: None yet
- **$400M+**: zkSync ($458M), Polygon
- **$200M+**: StarkWare ($273M), Aleo ($298M)
- **$100M+**: Aztec, Mina
- **$50M+**: Scroll, Succinct, RISC Zero
- **$20M+**: Axiom, Taiko

## Market Segments by Size

1. **Scaling (Largest)**: ZK rollups, $500M+ TVL
2. **Privacy (Growing)**: Zcash, Aztec, $1B+ market cap
3. **Identity (Emerging)**: zkPassport, ZK Email, early stage
4. **Infrastructure (Enabling)**: zkVMs, languages, $100M+ funding
5. **Emerging (Future)**: ZK ML, oracles, compliance

## Quick Decision Trees

### "Which ZK rollup should I use?"
- **Need EVM compatibility**: Scroll (Type 2) or Polygon zkEVM (Type 2.5)
- **Need performance**: zkSync Era or StarkNet
- **Need decentralization**: Taiko
- **Need privacy**: Aztec

### "Which proof system for my app?"
- **Need smallest proofs**: Groth16
- **Need no setup**: STARKs or Halo2
- **Need flexibility**: PLONK
- **Need recursion**: Halo2 or Plonky2

### "Which language to learn?"
- **Easiest**: Noir
- **Most jobs**: Cairo (StarkNet) or Circom
- **Most powerful**: Halo2
- **General purpose**: RISC Zero or SP1 (write Rust)

## Resources by Learning Level

### Beginner
- This repository (start with 00-ZK-ECOSYSTEM-OVERVIEW.md)
- Vitalik's blog posts
- ZK Whiteboard Sessions (first 5)

### Intermediate
- Justin Thaler's textbook (free PDF)
- ZK Whiteboard Sessions (all)
- Framework docs (Circom, Noir, Cairo)

### Advanced
- Original research papers
- Implement proof systems
- Contribute to ZK projects

## Community Links

- **Discord**: ZKProof, PSE, project-specific servers
- **Twitter**: Follow researchers and projects
- **Podcast**: Zero Knowledge Podcast
- **Events**: ZK Summit, ZKHack, ZKProof workshops
- **Learning**: learn.0xparc.org, zkhack.dev

---

**Bookmark this page for quick reference when reading ZK content!**
