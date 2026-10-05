# Provable / Aleo

Notes on the Aleo network and the software Provable builds for it: Leo, snarkVM, snarkOS and the SDKs. Aleo is a Layer 1 where users prove their own transactions with zero-knowledge proofs and validators only verify them, so data is private by default.

## Start here

1. **[tech-stack.md](./tech-stack.md)**: what each Provable repository does and how they fit together.
2. **[snarkvm/](./snarkvm/)**: the zkVM, from first principles to the codebase. Begin with *Inside snarkVM*; *KZG to Varuna* explains the proof system itself.
3. **[concepts/](./concepts/)**: short explainers that cut across the stack.

## Contents

| Path | What's inside |
| --- | --- |
| [tech-stack.md](./tech-stack.md) | Map of the stack: core repos, tooling, who runs what |
| [snarkvm/](./snarkvm/) | *Inside snarkVM* (intro guide), *Learning Notes 01* (curves, pairings, KZG, Varuna, state models), *KZG to Varuna* (the proof system in seven parts, with worked numbers), *Codebase Atlas* |
| [concepts/hash-encryption-signature-proof.md](./concepts/hash-encryption-signature-proof.md) | Which cryptographic tool answers which question, traced through one transaction |
| [concepts/aleo-vs-ethereum-vs-aztec.md](./concepts/aleo-vs-ethereum-vs-aztec.md) | Execution models, Ethereum's ZK roadmap, Aztec comparison, adoption |
| [concepts/post-quantum-aleo.md](./concepts/post-quantum-aleo.md) | Every elliptic-curve dependency in Aleo and its post-quantum replacement |

## Online versions

Everything here was first written as claude.ai artifacts. The **[snarkVM Study Hub](https://claude.ai/artifact/VxQK8XXTzui3YVPdE2hvzb)** links to all of them. Those links are private to the owner's account; the files in this folder are the shareable copies.

## Adding more

- A new component gets its own folder next to `snarkvm/` (for example `snarkos/`, `leo/`, `sdk/`) with a `README.md` that says where to start.
- A cross-cutting explainer goes in `concepts/`.
- Number learning notes in each folder (`learning-notes-02-….md`) so the reading order stays obvious.
- Open topics are listed at the end of [tech-stack.md](./tech-stack.md#not-covered-yet).
