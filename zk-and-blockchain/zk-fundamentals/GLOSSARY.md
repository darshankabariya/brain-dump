# ZK Glossary: A-Z

> **Alphabetical reference for all ZK terms you'll encounter**

## A

**AIR (Algebraic Intermediate Representation)**: Constraint system used in STARKs to represent computation as polynomial equations over execution traces.

**Arithmetic Circuit**: Representation of computation using addition and multiplication gates over a finite field.

**Aztec**: Privacy-focused ZK rollup and creator of Noir programming language.

## B

**Bulletproofs**: ZK proof system with logarithmic proof size and no trusted setup. Used in Monero for range proofs.

**Boojum**: zkSync's custom STARK-based proving system.

## C

**Cairo**: ZK-native programming language for StarkNet, designed specifically for STARK proofs.

**Circom**: Domain-specific language for writing arithmetic circuits, widely used for SNARK development.

**Commitment Scheme**: Cryptographic primitive allowing one to commit to a value while keeping it hidden, with ability to reveal later.

**Completeness**: Property that honest prover can always convince verifier of true statements.

**Constraint System**: Mathematical representation of computation for ZK proofs (e.g., R1CS, PLONK, AIR).

## D

**Dark Forest**: First major ZK game, pioneering private state in blockchain gaming.

**DEEP-FRI**: Improved variant of FRI protocol with better soundness and efficiency.

## E

**EVM Equivalence**: Degree to which a zkEVM matches Ethereum's execution environment.

## F

**Fiat-Shamir Transform**: Technique to convert interactive proofs into non-interactive ones using hash functions.

**Finite Field**: Mathematical structure with finite number of elements, foundation for ZK cryptography.

**FRI (Fast Reed-Solomon IOP)**: Core protocol in STARKs for proving low-degree polynomials.

**Fraud Proof**: Proof that invalid state transition occurred (used in Optimistic rollups, not ZK).

## G

**Groth16**: Most efficient SNARK in terms of proof size and verification time. Requires circuit-specific trusted setup.

## H

**Halo**: Recursive SNARK without trusted setup, using IPA for polynomial commitments.

**Halo2**: Production implementation of Halo, used by Zcash and Scroll.

## I

**Interactive Proof**: Proof system requiring back-and-forth communication between prover and verifier.

**IPA (Inner Product Argument)**: Polynomial commitment scheme without trusted setup, used in Halo2 and Bulletproofs.

## K

**KZG (Kate-Zaverucha-Goldberg)**: Polynomial commitment scheme with constant-size proofs, requires trusted setup.

## L

**Lookup Argument**: Technique to efficiently prove values are in a predefined table (e.g., Plookup, Lasso).

## M

**MACI (Minimal Anti-Collusion Infrastructure)**: ZK voting system preventing bribery and coercion.

**Marlin**: SNARK with universal setup and fast proving time, used by Aleo.

**Merkle Tree**: Tree structure for efficient verification of data inclusion.

## N

**NIZK (Non-Interactive Zero-Knowledge)**: ZK proof requiring no interaction between prover and verifier.

**Noir**: High-level ZK programming language by Aztec, designed for ease of use.

**Nullifier**: Unique identifier preventing double-spending in privacy systems.

## P

**Pairing**: Bilinear map on elliptic curves, enables efficient SNARK verification.

**PLONK**: Universal SNARK with custom gates and copy constraints. One setup works for all circuits.

**Plonky2**: Recursive STARK system with extremely fast recursion (~170ms per level).

**Plonky3**: Next-generation modular proving framework by Polygon.

**Polynomial Commitment**: Cryptographic commitment to a polynomial, enabling efficient opening proofs.

**Prover**: Party generating the ZK proof.

**Public Input**: Data visible to everyone in a ZK proof.

## Q

**QAP (Quadratic Arithmetic Program)**: Way to represent circuits for SNARKs, used in Groth16.

**Quantum Resistance**: Security against attacks by quantum computers. STARKs are quantum-resistant, SNARKs are not.

## R

**R1CS (Rank-1 Constraint System)**: Constraint system where each constraint is of form (A·w) × (B·w) = (C·w).

**Recursive Proof**: Proof that verifies other proofs, enabling infinite scalability.

**Reed-Solomon Code**: Error-correcting code used in FRI protocol.

**RLN (Rate Limiting Nullifier)**: ZK primitive for spam prevention while preserving anonymity.

## S

**Semaphore**: ZK protocol for anonymous signaling and group membership proofs.

**Sequencer**: Entity ordering transactions in a rollup.

**Soundness**: Property that cheating prover cannot convince verifier of false statements.

**SNARK (Succinct Non-interactive ARgument of Knowledge)**: ZK proof with small size and fast verification.

**STARK (Scalable Transparent ARgument of Knowledge)**: ZK proof with no trusted setup and quantum resistance.

**Succinct**: Proof size much smaller than computation being proved.

## T

**Transparent**: No trusted setup required, all parameters publicly verifiable.

**Trusted Setup**: Ceremony to generate public parameters for some SNARKs. If compromised, soundness breaks.

**TurboPLONK**: PLONK variant with custom gates for improved efficiency.

## U

**UltraPLONK**: PLONK variant with lookup tables for efficient table lookups.

**Universal Setup**: Single trusted setup ceremony works for all circuits up to a size bound.

## V

**Validity Proof**: ZK proof that state transition is correct (used in ZK rollups).

**Verifier**: Party checking the ZK proof.

## W

**Witness**: Private input to a ZK proof, the secret being proved about.

## Z

**Zcash**: First major cryptocurrency using ZK (shielded transactions).

**Zero-Knowledge**: Property that proof reveals nothing beyond statement's truth.

**zkEVM**: Ethereum Virtual Machine that generates ZK proofs of execution.

**zkVM**: Virtual machine that generates ZK proofs for general computation.

**zkSync**: Type 4 zkEVM rollup by Matter Labs.

---

## By Category

### Proof Systems
- Groth16, PLONK, Halo2, STARKs, Bulletproofs, Marlin, Plonky2

### Polynomial Commitments
- KZG, FRI, IPA

### Constraint Systems
- R1CS, PLONK gates, AIR, QAP

### Languages
- Circom, Noir, Cairo, Leo, Miden Assembly

### Projects
- zkSync, StarkNet, Polygon zkEVM, Scroll, Aztec, Aleo, Mina

### Applications
- MACI, Semaphore, RLN, Dark Forest, zkPassport, ZK Email

### Properties
- Completeness, Soundness, Zero-Knowledge, Succinctness, Transparency

---

**Use Ctrl+F / Cmd+F to quickly find terms!**
