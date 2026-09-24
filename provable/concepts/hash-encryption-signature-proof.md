# Hash, encryption, signature, proof: which one, when

Each primitive answers exactly one question. Aleo uses all four in every transaction, and the proof wraps the other three.

| Question | Tool | Analogy | Reversible? |
| --- | --- | --- | --- |
| "What is this, exactly?" | **Hash** | A fingerprint | No, one-way |
| "Who can read this?" | **Encryption** | A locked box only the recipient opens | Yes, with the right key |
| "Who approved this?" | **Signature** | A handwritten signature or stamp | Anyone verifies; only you can make it |
| "Was everything done correctly?" | **Proof** (zkSNARK) | A notary certificate that reveals nothing else | Anyone verifies |

Three things that are really hashes used a particular way:

- **Commitment** = hash(data + randomness): a sealed envelope that hides now and can't be changed later.
- **Merkle tree** = hashes of hashes: one root stands for millions of items, with short inclusion proofs.
- **Serial number / tag** = a keyed hash: a fingerprint only the owner can compute.

## The key insight: the proof wraps the others

```
┌──────────────── PROOF (Varuna) ────────────────────────────┐
│  "I proved, without showing you:"                          │
│    ✓ the signature on this request is valid     ← signature│
│    ✓ the record I spend exists in the tree      ← hash     │
│    ✓ its serial number is computed correctly    ← hash     │
│    ✓ the new records are encrypted to the owner ← encryption│
│    ✓ the new commitments are correct            ← hash     │
│    ✓ the program logic ran (e.g. 250 − 100 = 150)          │
└────────────────────────────────────────────────────────────┘
```

On Ethereum, validators check your signature directly, so they see who signed. On Aleo the signature is checked **inside** the proof, which is how the sender stays hidden.

## One private payment, step by step

Alice sends 100 private tokens to Bob.

| # | Step | Where | Tool |
| --- | --- | --- | --- |
| 1 | Find her coins | Alice's device | Encryption (decrypt with view key) |
| 2 | Build the request (input IDs) | Alice's device | Hash |
| 3 | Approve it | Alice's device | Signature |
| 4 | Mark the old record spent (serial number, tag) | Alice's device | Keyed hash |
| 5 | Show the old record exists (Merkle path) | Alice's device | Hash |
| 6 | Create new records for Bob and change | Alice's device | Commitment + encryption |
| 7 | Certify steps 2–6 | Alice's device | **Proof** (prove) |
| 8 | Name the transaction (ID = Merkle root) | Alice's device | Hash |
| 9 | Check it | Every validator | **Proof** (verify) |
| 10 | Prevent double spends (is the serial number new?) | Every validator | Compare hashes |
| 11 | Agree on ordering (batch certificates) | Validators | Signature |
| 12 | Seal the block (block hash, header roots) | Validators | Hash |
| 13 | Bob finds his money | Bob's device | Encryption (decrypt) |

Pattern: **hash is the glue** (everywhere), **encryption is at the edges** (writing for and reading by a person), **signatures are permission** (user approval, validator votes), **the proof runs exactly twice** per transaction: prove once, verify on each validator.

## Where each lives in snarkVM

| Tool | Code |
| --- | --- |
| Hash | `console/algorithms` (Poseidon, BHP, Pedersen, Keccak, SHA-3); Merkle trees in `console/collections` |
| Commitment, serial number, tag | `console/program/src/data/record/` (`to_commitment.rs`, `serial_number.rs`, `tag.rs`) |
| Encryption | `record/encrypt.rs`, `decrypt.rs`; the `Ciphertext` type |
| Signature | `console/account/src/signature`; request signing in `console/program/src/request/sign.rs` |
| Proof | Prove: `Trace::prove_execution`. Verify: `VM::check_transaction`. Engine: `algorithms/src/snark/varuna` |

**One line:** hash = identity, encryption = secrecy, signature = permission, proof = correctness.
