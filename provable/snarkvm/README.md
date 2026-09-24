# snarkVM

The zkVM at the heart of Aleo: it runs programs, turns them into Varuna proofs, verifies them, and defines what a valid transaction, block and ledger state are. Source: [ProvableHQ/snarkVM](https://github.com/ProvableHQ/snarkVM).

## Read in this order

| # | Material | Format | Time | What you get |
| --- | --- | --- | --- | --- |
| 1 | [Inside snarkVM](./inside-snarkvm.html) ([online](https://claude.ai/artifact/L2Ji3rdrNNuVNGXJbg2rNY)) | Interactive HTML | ~90 min | Prerequisites, Aleo concepts, the execution pipeline, a real transaction end to end |
| 2 | [Learning Notes 01](./learning-notes-01-curves-pairings-kzg-varuna.md) ([live doc](https://claude.ai/code/artifact/2d7e97dc-ad20-4e51-9461-36707dc6913f)) | Markdown | ~60 min | BLS12-377, Edwards-BLS12, pairings, KZG, Varuna step by step, account vs UTXO |
| 3 | [snarkVM Codebase Atlas](./codebase-atlas.html) ([online](https://claude.ai/artifact/Wy1FjidpKnkkNd4N7DwJfG)) | Interactive HTML | ~70 min | Every crate, cross-cutting systems, team priorities, where to contribute |

The HTML files open in any browser (they fetch fonts from Google Fonts when online and fall back to system fonts offline). The "online" links are the original published versions; the live doc may have newer edits than the markdown snapshot here.

## The one-paragraph version

A user runs an Aleo program on their own device. snarkVM executes each function twice, once natively ("console") and once as arithmetic constraints ("circuit"), and proves the constraints with one batched Varuna proof over BLS12-377. Validators never re-run the private part: they verify the proof, check serial numbers aren't reused, then run only the small public `finalize` code in block order and apply the result to the ledger.

## Code landmarks

| Question | Where to look |
| --- | --- |
| How does a function run and get proven? | `synthesizer/process/src/stack/execute.rs`, `synthesizer/process/src/trace/` |
| What does a validator check? | `synthesizer/src/vm/verify.rs`, `synthesizer/src/vm/finalize.rs` |
| How does a block become state? | `ledger/src/check_next_block.rs`, `ledger/src/advance.rs` |
| How do protocol upgrades work? | `console/network/src/consensus_heights.rs` |
| Where is the proof system? | `algorithms/src/snark/varuna/` |
