# Field Notes

Personal learning repo. Each top-level directory is a topic — notes, references, and working material as I learn it.

## Topics

- **[provable/](./provable/)** — The Aleo network and Provable's stack (Leo, snarkVM, snarkOS, SDK): an intro guide to snarkVM, a codebase atlas, learning notes on curves, pairings, KZG and Varuna, a seven-part walkthrough of the proof system from KZG and Groth16 to PLONK, Marlin and Varuna, and explainers comparing Aleo with Ethereum and Aztec.
- **[ai-inference-verification/](./ai-inference-verification/)** — Proving that an AI model produced an answer: SASH's zk-inference-prover and Pascal Berrang's zero-knowledge model checking, as a long-read primer, an end-to-end prover flow page and a step animation, plus working notes.
- **[zk-and-blockchain/](./zk-and-blockchain/)** — Zero-knowledge proofs, Ethereum rollups, L2 infrastructure (EigenLayer, NEAR, Succinct).
- **[quantum-computing/](./quantum-computing/)** — How quantum computing works, from the qubit to Shor's algorithm, with an interactive HTML animation.
- **[obsidian-claude-graphify/](./obsidian-claude-graphify/)** — Workflow for turning codebases, papers, and notes into a navigable knowledge graph that Claude reads before answering.

## Where to start

- New to zero-knowledge proofs: [zk-and-blockchain/zk-fundamentals/START-HERE.md](./zk-and-blockchain/zk-fundamentals/START-HERE.md).
- Working on Aleo / snarkVM: [provable/README.md](./provable/README.md).
- Curious why quantum computers threaten today's cryptography: [quantum-computing/](./quantum-computing/), then [provable/concepts/post-quantum-aleo.md](./provable/concepts/post-quantum-aleo.md).

## Adding a new topic

Create a new directory at the root with a `README.md` that explains what's inside and where to start. Keep each topic self-contained so it can grow or be split out without touching the others.
