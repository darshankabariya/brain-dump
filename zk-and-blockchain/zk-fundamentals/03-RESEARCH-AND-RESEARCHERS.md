# ZK Research: Papers, Researchers, and Foundations

## Table of Contents
1. [Foundational Papers](#foundational-papers)
2. [Key Researchers](#key-researchers)
3. [Modern Research (2020-2024)](#modern-research-2020-2024)
4. [Research by Topic](#research-by-topic)
5. [Academic Institutions](#academic-institutions)
6. [How to Read ZK Papers](#how-to-read-zk-papers)

---

## Foundational Papers

### The Genesis (1985-2000)

#### 1. **The Knowledge Complexity of Interactive Proof Systems** (1985)
- **Authors**: Goldwasser, Micali, Rackoff
- **Significance**: Invented Zero-Knowledge Proofs
- **Key Contribution**: Defined ZK properties (completeness, soundness, zero-knowledge)
- **Link**: [GMR85](https://people.csail.mit.edu/silvio/Selected%20Scientific%20Papers/Proof%20Systems/The_Knowledge_Complexity_Of_Interactive_Proof_Systems.pdf)

**Impact**: 🏆 Turing Award 2012 (Goldwasser & Micali)

#### 2. **How to Prove Yourself: Practical Solutions to Identification and Signature Problems** (1986)
- **Authors**: Fiat, Shamir
- **Significance**: Made ZK non-interactive
- **Key Contribution**: Fiat-Shamir transform (interactive → non-interactive)
- **Application**: Foundation for all blockchain ZK

**The Transform**:
```
Interactive Protocol + Hash Function = Non-Interactive Proof
```

#### 3. **Proofs that Yield Nothing But Their Validity** (1986)
- **Authors**: Goldreich, Micali, Wigderson
- **Significance**: ZK for all NP problems
- **Key Contribution**: Proved ZK is universal (any NP statement can have ZK proof)

---

### The SNARK Era (2010-2020)

#### 4. **Succinct Non-Interactive Zero Knowledge for a von Neumann Architecture** (2013)
- **Authors**: Ben-Sasson, Chiesa, Genkin, Tromer, Virza
- **Significance**: First practical SNARK system
- **System**: Pinocchio
- **Key Contribution**: Quadratic Arithmetic Programs (QAP)

**Innovation**: Made ZK practical for general computation

#### 5. **On the Size of Pairing-based Non-interactive Arguments** (2016)
- **Authors**: Jens Groth
- **Significance**: Most efficient SNARK to date
- **System**: Groth16
- **Key Contribution**: 3 group elements proof, 3 pairing checks

**Impact**: Still the most used SNARK in production (2024)

#### 6. **Scalable Zero Knowledge via Cycles of Elliptic Curves** (2014)
- **Authors**: Ben-Sasson, Chiesa, Tromer, Virza
- **Significance**: Enabled recursive proofs
- **Key Contribution**: Cycle of curves for recursion
- **Application**: Mina Protocol (recursive blockchain)

#### 7. **Bulletproofs: Short Proofs for Confidential Transactions** (2017)
- **Authors**: Bünz, Bootle, Boneh, Poelstra, Wuille, Maxwell
- **Significance**: No trusted setup
- **Key Contribution**: Logarithmic-size proofs without setup
- **Application**: Monero, confidential transactions

---

### The STARK Revolution (2018-2020)

#### 8. **Scalable, transparent, and post-quantum secure computational integrity** (2018)
- **Authors**: Ben-Sasson, Bentov, Horesh, Riabzev
- **Significance**: Introduced STARKs
- **Key Contribution**: Transparent, quantum-resistant proofs
- **System**: libSTARK

**Properties**:
- No trusted setup
- Quantum resistant
- Scales to billions of gates

#### 9. **Fast Reed-Solomon Interactive Oracle Proofs of Proximity** (2017)
- **Authors**: Ben-Sasson, Bentov, Horesh, Riabzev
- **Significance**: Core STARK primitive
- **Key Contribution**: FRI protocol
- **Application**: All STARK systems

---

### Modern Breakthroughs (2019-2024)

#### 10. **PLONK: Permutations over Lagrange-bases for Oecumenical Noninteractive arguments of Knowledge** (2019)
- **Authors**: Gabizon, Williamson, Ciobotaru
- **Significance**: Universal trusted setup
- **Key Contribution**: One setup for all circuits
- **Impact**: Aztec, zkSync, many others

**Innovation**: Copy constraints + custom gates

#### 11. **Recursive Proof Composition without a Trusted Setup** (2019)
- **Authors**: Bowe, Grigg, Hopwood
- **Significance**: Recursion without trusted setup
- **System**: Halo
- **Key Contribution**: Accumulation schemes

**Impact**: Zcash Orchard, Scroll zkEVM

#### 12. **Halo 2** (2020)
- **Authors**: Daira Hopwood, Sean Bowe, et al.
- **Significance**: Production-ready recursive SNARKs
- **Key Contribution**: Practical implementation of Halo
- **Application**: Zcash, Scroll, Axiom

#### 13. **Plonky2: Fast Recursive Arguments with PLONK and FRI** (2022)
- **Authors**: Polygon Zero team
- **Significance**: Fastest recursive proofs
- **Key Contribution**: 170ms recursion time
- **Application**: Polygon zkEVM

**Performance**:
```
Traditional recursion: ~30 seconds
Plonky2 recursion: ~170 milliseconds
```

---

## Key Researchers

### 🏆 Pioneers (Turing Award Winners)

#### Shafi Goldwasser
- **Affiliation**: MIT, UC Berkeley
- **Contributions**: Co-invented ZK proofs (GMR85)
- **Awards**: Turing Award 2012, Gödel Prize
- **Current**: Director of Simons Institute
- **Twitter**: [@shafiGoldwasser](https://twitter.com/shafigoldwasser)

#### Silvio Micali
- **Affiliation**: MIT
- **Contributions**: Co-invented ZK proofs, founder of Algorand
- **Awards**: Turing Award 2012, Gödel Prize
- **Current**: Algorand blockchain
- **Twitter**: [@silviomicali](https://twitter.com/silviomicali)

---

### 🔬 Modern ZK Leaders

#### Dan Boneh
- **Affiliation**: Stanford University
- **Contributions**: Bulletproofs, pairing-based crypto, BLS signatures
- **Impact**: Foundational work in cryptographic protocols
- **Courses**: [CS 251: Cryptocurrencies and Blockchain](https://cs251.stanford.edu/)
- **Twitter**: [@danboneh](https://twitter.com/danboneh)

**Key Papers**:
- Bulletproofs (2017)
- Aggregate and Verifiably Encrypted Signatures (2003)
- Short Signatures from the Weil Pairing (2001)

#### Justin Thaler
- **Affiliation**: Georgetown University, a16z crypto research
- **Contributions**: Sum-check protocol, GKR protocol, Proofs, Arguments, and Zero-Knowledge (textbook)
- **Impact**: Accessible ZK education
- **Book**: [Proofs, Arguments, and Zero-Knowledge](https://people.cs.georgetown.edu/jthaler/ProofsArgsAndZK.pdf) (free)
- **Twitter**: [@jthaler](https://twitter.com/jthaler)

**Must-Read**: His textbook is the best modern introduction to ZK

#### Eli Ben-Sasson
- **Affiliation**: Technion, StarkWare (co-founder)
- **Contributions**: STARKs, Zcash co-founder, FRI protocol
- **Impact**: Brought ZK from theory to practice
- **Company**: StarkWare (StarkNet, StarkEx)
- **Twitter**: [@EliBenSasson](https://twitter.com/elibenSasson)

**Key Innovations**:
- STARKs (2018)
- FRI protocol (2017)
- Zerocash (2014)

#### Alessandro Chiesa
- **Affiliation**: UC Berkeley, EPFL
- **Contributions**: SNARKs, Zcash co-founder, libsnark
- **Impact**: Practical SNARK implementations
- **Projects**: Zcash, Aleo
- **Twitter**: [@alexch1](https://twitter.com/alexch1)

#### Ariel Gabizon
- **Affiliation**: Aztec Network (formerly Zcash)
- **Contributions**: PLONK co-inventor, KZG commitments
- **Impact**: Universal setup SNARKs
- **Twitter**: [@relgabizon](https://twitter.com/relgabizon)

**Key Work**: PLONK (2019) - revolutionized SNARK flexibility

#### Jens Groth
- **Affiliation**: DFINITY, formerly UCL
- **Contributions**: Groth16 (most efficient SNARK)
- **Impact**: Enabled practical ZK applications
- **Awards**: Multiple best paper awards

**Legacy**: Groth16 is still the gold standard for proof size

#### Sean Bowe
- **Affiliation**: Electric Coin Company (Zcash)
- **Contributions**: Halo, Halo 2, Sapling
- **Impact**: Recursive proofs without trusted setup
- **Twitter**: [@ebfull](https://twitter.com/ebfull)

#### Daira Hopwood
- **Affiliation**: Electric Coin Company (Zcash)
- **Contributions**: Halo 2 design, Zcash protocol
- **Impact**: Production ZK systems
- **Twitter**: [@feministPLT](https://twitter.com/feministPLT)

---

### 🌟 Rising Stars & Industry Leaders

#### Pratyush Mishra
- **Affiliation**: Aleo, formerly UC Berkeley
- **Contributions**: arkworks (Rust ZK library), Marlin
- **Impact**: Open-source ZK infrastructure
- **Twitter**: [@zkproofs](https://twitter.com/zkproofs)

#### Mary Maller
- **Affiliation**: Ethereum Foundation, PQShield
- **Contributions**: Sonic, Halo, polynomial commitments
- **Impact**: Advanced SNARK constructions

#### Kobi Gurkan
- **Affiliation**: Geometry, cLabs
- **Contributions**: Trusted setup ceremonies, ZK tooling
- **Impact**: Making ZK accessible
- **Twitter**: [@kobigurk](https://twitter.com/kobigurk)

#### Barry WhiteHat
- **Affiliation**: Ethereum Foundation (PSE)
- **Contributions**: Privacy on Ethereum, MACI, Semaphore
- **Impact**: ZK applications for Ethereum
- **Twitter**: [@barrywhitehat](https://twitter.com/barrywhitehat)

#### Vitalik Buterin
- **Affiliation**: Ethereum Foundation
- **Contributions**: ZK-EVM research, ZK-rollup advocacy
- **Impact**: Driving ZK adoption in Ethereum
- **Blog**: [vitalik.ca](https://vitalik.ca)
- **Twitter**: [@VitalikButerin](https://twitter.com/VitalikButerin)

**Key Posts**:
- [The Different Types of ZK-EVMs](https://vitalik.ca/general/2022/08/04/zkevm.html)
- [An Approximate Introduction to How zk-SNARKs Are Possible](https://vitalik.ca/general/2021/01/26/snarks.html)

---

## Modern Research (2020-2024)

### Proof System Improvements

#### **Plonky3** (2024)
- **Team**: Polygon Zero
- **Contribution**: Modular STARK framework
- **Impact**: Customizable proof systems
- **Link**: [Plonky3 GitHub](https://github.com/Plonky3/Plonky3)

#### **Binius** (2024)
- **Authors**: Benjamin Diamond, Jim Posen
- **Contribution**: Binary field SNARKs
- **Impact**: Potentially 100x faster proofs
- **Status**: Early research

#### **Lasso & Jolt** (2023-2024)
- **Authors**: Thaler, Setty, et al.
- **Contribution**: Lookup arguments, zkVM
- **Impact**: Efficient table lookups in ZK
- **Application**: RISC-V zkVM

---

### ZK-EVM Research

#### **Type 1 zkEVM** (2023-2024)
- **Team**: PSE (Privacy & Scaling Explorations)
- **Goal**: Fully Ethereum-equivalent ZK proofs
- **Status**: Research/testnet
- **Link**: [PSE zkEVM](https://github.com/privacy-scaling-explorations/zkevm-circuits)

#### **Scroll zkEVM** (2023)
- **Team**: Scroll
- **Contribution**: Halo2-based Type 2 zkEVM
- **Status**: Mainnet
- **Link**: [Scroll Docs](https://docs.scroll.io/)

#### **Polygon zkEVM** (2023)
- **Team**: Polygon
- **Contribution**: Plonky2-based Type 2.5 zkEVM
- **Status**: Mainnet
- **Link**: [Polygon zkEVM Docs](https://docs.polygon.technology/zkEVM/)

---

### Application-Specific Research

#### **MACI** (Minimal Anti-Collusion Infrastructure)
- **Authors**: Barry WhiteHat, Koh Wei Jie
- **Contribution**: Collusion-resistant voting
- **Application**: Quadratic funding, governance
- **Link**: [MACI](https://github.com/privacy-scaling-explorations/maci)

#### **Semaphore**
- **Authors**: Barry WhiteHat, Kobi Gurkan
- **Contribution**: Anonymous signaling
- **Application**: Private group membership
- **Link**: [Semaphore](https://semaphore.appliedzkp.org/)

#### **ZK Email**
- **Authors**: Aayush Gupta, Sora Suegami
- **Contribution**: Prove email contents without revealing
- **Application**: Identity, attestations
- **Link**: [ZK Email](https://prove.email/)

#### **TLSNotary**
- **Contribution**: Prove web data authenticity
- **Application**: Verifiable web scraping
- **Link**: [TLSNotary](https://tlsnotary.org/)

---

## Research by Topic

### Polynomial Commitments

| Scheme | Paper | Year | Authors |
|--------|-------|------|---------|
| **KZG** | Constant-Size Commitments to Polynomials | 2010 | Kate, Zaverucha, Goldberg |
| **FRI** | Fast Reed-Solomon IOP | 2017 | Ben-Sasson et al. |
| **IPA** | Bulletproofs | 2017 | Bünz et al. |
| **Dory** | Transparent Polynomial Commitments | 2020 | Lee |
| **Hyrax** | Doubly-efficient zkSNARKs | 2017 | Wahby et al. |

### Recursive Proofs

| System | Paper | Year | Key Innovation |
|--------|-------|------|----------------|
| **Halo** | Recursive Proof Composition | 2019 | Accumulation |
| **Halo 2** | Halo 2 | 2020 | Practical recursion |
| **Plonky2** | Plonky2 | 2022 | Fast FRI recursion |
| **Nova** | Recursive SNARKs without Trusted Setup | 2021 | Folding schemes |
| **SuperNova** | SuperNova | 2022 | Multi-circuit folding |

### Lookup Arguments

| System | Paper | Year | Application |
|--------|-------|------|-------------|
| **Plookup** | Plookup | 2020 | Table lookups in PLONK |
| **Lasso** | Lasso | 2023 | Efficient lookups |
| **LogUp** | LogUp | 2023 | Logarithmic lookups |
| **cq** | cq | 2022 | Cached quotients |

### ZK-VMs

| System | Paper | Year | Architecture |
|--------|-------|------|--------------|
| **Cairo** | Cairo Whitepaper | 2021 | STARK-based VM |
| **Miden** | Polygon Miden | 2022 | STARK-based VM |
| **RISC Zero** | RISC Zero | 2022 | RISC-V zkVM |
| **Jolt** | Jolt | 2024 | RISC-V with Lasso |
| **SP1** | SP1 | 2024 | RISC-V zkVM |

---

## Academic Institutions

### Leading ZK Research Groups

#### **UC Berkeley**
- **Lab**: RDI (Research, Development, Innovation)
- **Researchers**: Alessandro Chiesa, Dan Boneh (Stanford collab)
- **Focus**: SNARKs, ZK-EVMs
- **Projects**: Aleo, Zcash

#### **MIT**
- **Lab**: CSAIL
- **Researchers**: Shafi Goldwasser, Silvio Micali
- **Focus**: Foundational cryptography
- **Projects**: Algorand

#### **Stanford**
- **Lab**: Applied Crypto Group
- **Researchers**: Dan Boneh, David Mazières
- **Focus**: Cryptographic protocols, Bulletproofs
- **Courses**: CS 251, CS 355

#### **Technion (Israel)**
- **Researchers**: Eli Ben-Sasson
- **Focus**: STARKs, algebraic complexity
- **Spinoff**: StarkWare

#### **EPFL (Switzerland)**
- **Researchers**: Alessandro Chiesa
- **Focus**: SNARKs, proof systems

#### **Georgetown University**
- **Researchers**: Justin Thaler
- **Focus**: Interactive proofs, sum-check protocol
- **Resources**: Free textbook

---

### Industry Research Labs

#### **Ethereum Foundation - PSE**
- **Focus**: Privacy & Scaling Explorations
- **Projects**: zkEVM, MACI, Semaphore
- **Team**: Barry WhiteHat, et al.

#### **a16z Crypto Research**
- **Researchers**: Justin Thaler, Tim Roughgarden
- **Focus**: ZK theory, applications
- **Resources**: Research papers, tutorials

#### **StarkWare**
- **Focus**: STARK research, Cairo
- **Team**: Eli Ben-Sasson, et al.
- **Products**: StarkNet, StarkEx

#### **Polygon Zero (now Toposware)**
- **Focus**: Plonky2, Plonky3
- **Innovation**: Fast recursive proofs

#### **Electric Coin Company (Zcash)**
- **Focus**: Privacy, Halo 2
- **Team**: Sean Bowe, Daira Hopwood
- **Products**: Zcash protocol

---

## How to Read ZK Papers

### Reading Strategy

#### Level 1: High-Level Understanding
1. **Abstract**: What problem does it solve?
2. **Introduction**: Why does it matter?
3. **Conclusion**: What are the results?
4. **Skip**: Detailed proofs (for now)

#### Level 2: Technical Understanding
1. **Preliminaries**: Understand definitions
2. **Construction**: How does the system work?
3. **Security**: What are the guarantees?
4. **Performance**: Benchmarks and comparisons

#### Level 3: Deep Dive
1. **Proofs**: Verify security claims
2. **Implementation**: Code review
3. **Optimizations**: Understand trade-offs

### Essential Background

**Mathematics**:
- Finite fields
- Polynomials
- Elliptic curves (for SNARKs)
- Linear algebra

**Computer Science**:
- Complexity theory (P, NP)
- Cryptographic primitives
- Circuit design

**Recommended Prep**:
1. [Proofs, Arguments, and Zero-Knowledge](https://people.cs.georgetown.edu/jthaler/ProofsArgsAndZK.pdf) - Justin Thaler
2. [A Graduate Course in Applied Cryptography](http://toc.cryptobook.us/) - Boneh & Shoup
3. [ZK Whiteboard Sessions](https://zkhack.dev/whiteboard/) - Video series

---

### Paper Reading List (Ordered)

#### Beginner
1. Vitalik's blog posts (accessible)
2. Thaler's textbook (comprehensive)
3. ZK Whiteboard Sessions (visual)

#### Intermediate
1. Groth16 paper (practical SNARK)
2. PLONK paper (modern SNARK)
3. STARK paper (alternative approach)

#### Advanced
1. Halo paper (recursion)
2. Plonky2 paper (performance)
3. Nova paper (folding schemes)

---

## Key Takeaways

1. **GMR85**: Started it all - ZK proofs are possible
2. **Fiat-Shamir**: Made ZK non-interactive (blockchain-ready)
3. **Groth16**: Made ZK practical (smallest proofs)
4. **STARKs**: Transparent alternative (no setup)
5. **PLONK**: Universal setup (flexibility)
6. **Halo/Plonky2**: Fast recursion (scalability)

**Research is ongoing**: New breakthroughs every year!

---

## Next Steps

- **Industry**: Read `04-COMPANIES-AND-PROJECTS.md` to see research in action
- **Applications**: Check `05-APPLICATIONS-AND-USE-CASES.md` for real-world use
- **Hands-on**: Try implementing circuits (tutorials coming)

---

**Resources**:
- [ZKProof Community](https://zkproof.org/) - Standards and workshops
- [ZKHack](https://zkhack.dev/) - Puzzles and learning
- [Awesome ZK](https://github.com/matter-labs/awesome-zero-knowledge-proofs) - Curated list
- [IACR ePrint](https://eprint.iacr.org/) - Cryptography preprints
