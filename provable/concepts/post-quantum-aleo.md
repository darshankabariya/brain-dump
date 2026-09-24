# Post-quantum Aleo: what would have to change

Aleo is not post-quantum secure today, and neither is Ethereum or nearly any major L1. Swapping KZG for a hash-based commitment (FRI) would fix only one of at least seven curve dependencies.

## Every elliptic-curve dependency

| # | Component | Today | What a quantum attacker does | Post-quantum replacement | Difficulty |
| --- | --- | --- | --- | --- | --- |
| 1 | Proof system (Varuna's commitments) | KZG on BLS12-377 (pairings) | Forge proofs, e.g. mint credits | FRI / WHIR / Basefold (hash-based) or lattice commitments | Medium (Marlin-style + FRI has been studied as "Fractal") |
| 2 | Signatures (`Request`) | Schnorr-style on Edwards-BLS12, **checked inside the circuit** | Derive the private key from the address and spend | ML-DSA, Falcon, or hash-based XMSS/SPHINCS+ | Hard: lattice signatures are very expensive in circuits |
| 3 | Record encryption | ECDH: `(address · r).x` | Decrypt every past record | Lattice KEM (ML-KEM / Kyber) | Hard: proven in-circuit, and Kyber's modulus (q = 3329) isn't Aleo's field |
| 4 | Addresses and keys | `address = G · view_key` | Recover keys from any address | New post-quantum account format | Medium technically, hard socially (everyone migrates) |
| 5 | Record commitments, Merkle trees | BHP, Pedersen (curve-based) | Break binding: re-open commitments, forge paths | Hash-based (Poseidon, SHA-3) | Easy–medium |
| 6 | Serial numbers | `sk_sig · HashToGroup(commitment)` | Link spends to records, or forge | Hash-based PRF, e.g. `Poseidon(sk, commitment)` | Easy–medium |
| 7 | Consensus signatures (batch certificates) | Aleo curve signatures | Forge validator votes | Post-quantum signatures (larger) | Medium (bandwidth) |

Also language-level: the `group` type, ECDSA opcodes, and `snark.verify` (which verifies Varuna proofs inside programs).

## Why it's more than a component swap

1. **The field would probably change.** Hash-based provers prefer small fields (Goldilocks, BabyBear, Mersenne-31), but Aleo's `field` type *is* BLS12-377's 253-bit scalar field. Changing it changes program semantics.
2. **Every deployed program needs new keys.**
3. **Proofs grow** from a few KB to ~50–200+ KB, on user devices and in blocks.
4. **Old data stays exposed.** Upgrading protects future records only.
5. **It's a hard fork,** gated by a `ConsensusVersion`, with a migration window.

In practice, close to a "snarkVM v2".

## Threat comparison with Ethereum

| Threat | Ethereum | Aleo |
| --- | --- | --- |
| Harvest now, decrypt later | Mostly no: data is already public (applies to Ethereum privacy systems like Aztec) | **Yes**: every private record is an EC ciphertext, public forever |
| Key theft | Yes, milder: the address is a hash of the public key until first use | Yes, worse: the address *is* the public point |
| Forged proofs / signatures | Yes: BLS validator signatures, KZG blobs, zk-rollup SNARKs | Yes: Varuna (pairings + KZG) |

Threats 2 and 3 can be fixed by migrating in time. **Threat 1 can't be fixed retroactively**, and it matters more for a privacy chain.

## How post-quantum ZK is done today

| Building block | Options | Notes |
| --- | --- | --- |
| Proof systems | Hash-based: STARK/FRI (StarkWare, RISC Zero, SP1, Plonky3), Binius, WHIR, STIR, Basefold, Ligero/Brakedown | Transparent, larger proofs |
| | Lattice-based: LaBRADOR, Greyhound, LatticeFold | Smaller proofs, mostly research |
| Signatures | ML-DSA (Dilithium), FN-DSA (Falcon), SLH-DSA (SPHINCS+); in-ZK: Poseidon2-based XMSS | Lean Ethereum uses the XMSS route |
| Encryption | ML-KEM (Kyber) | Costly to prove in-circuit |
| Hashes | SHA-2/3, Poseidon2 | Grover only halves preimage security; 256-bit outputs are fine |

Catch: many STARK zkVMs wrap their final proof in **Groth16 on BN254** for cheap Ethereum verification, which is pairing-based and **not** post-quantum.
