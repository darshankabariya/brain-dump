# Context: what is understood about zk-inference-prover so far (7 Oct 2026)

Purpose of the new session: understand the codebase in depth. This file records what has
been established and what has not, so nothing is re-derived.

## Repos on disk (`/Users/darshan/work/SASH/`)
- `zk-inference-prover/` — the software. Public: github.com/sg-ai-safety-hub/zk-inference-prover,
  published 26 Sep 2026, every commit by Pascal Berrang (485), 30 open issues, no outside PRs.
  - `prover/` — Rust crate, binary `zk-prover` (~38k lines in `prover/src`).
  - `nitroo/` — vendored fork of StarkWare's stwo (Circle STARK) with a CUDA backend, pinned at
    an upstream commit plus four local changes listed in `nitroo/README.md`. Treat as a build input.
  - `harness/` — one uv Python package: `witness/` (deterministic quantised forward pass, greedy
    continuation, witness extraction, shape table, plan file), `eval/` (perplexity, task suite,
    unproved baseline, `predict/` registration), `costmodel/` (cell counting, cost projections).
  - `docs/statement.md` — what the proof binds, edge by edge (16 edges). `docs/decisions/` —
    dated design decisions, never edited after merge. `GLOSSARY.md`, `CLAUDE.md`, `tools/gate/`.
- `zk-inference-results/` — the measurements. `runs/<date>-<driver>-<gpu>/` (manifest + JSON
  outputs, no logs/witnesses/proofs), `constants.json` (every published number, graded
  measured / derived / projected / external / asserted, each naming its run and artifact),
  `REPRODUCE.md`, `tools/drivers/`, `tools/constants/{check,audit,export}.py`, `docs/cost-model.md`,
  `docs/quantization.md`, `docs/statement-gap.md`. Each run pins the prover commit that made it.
- `notes/berrang-primer.html` — source of the published study page
  (https://claude.ai/artifact/KmBRGQDSRaoUVx3UymADet).
- The ZK Model Checking paper PDF in the folder is unrelated to this code (KZG, Pedersen,
  Farkas; no STARKs).

## Recommended reading order
`README.md` → `CLAUDE.md` → `GLOSSARY.md` → `docs/statement.md` → `prover/README.md` →
`harness/README.md` → `zk-inference-results/docs/cost-model.md` → `docs/statement-gap.md`.
Then `prover/src/lib.rs` for the module map, and one gadget directory
(`prover/src/gadgets/freivalds/` is a good first one).

## What the system does (established)
- Statement: greedy decoding of a quantised Llama-3.1-8B. For published prompt ids and a
  published 512-token continuation, every layer of every position is proved from the embedding
  row to the argmax, with the residual stream bound between layers and the key/value cache bound
  between token blocks. Verifier inputs: the prompt ids, the model commitment (root of the
  weight tree, from the publisher's manifest), and the per-layer calibration from which the
  verifier rebuilds the "shape tree" itself and compares roots.
- Unit of proof: a segment = one transformer layer (or the output head) applied to a block of
  S = 512 positions against a context of C earlier positions. A request is a grid of segments
  (c4096 request: 9 token blocks × 32 layers + head segments = 290 proofs; c16384: 1,058).
  `boundary-grid` checks adjacent segments agree on the Merkle roots of the residual stream
  (layer to layer) and of the keys/values (block to block). No recursion.
- Trees committed per segment: shape tree (preprocessed; selectors, masks, lookup tables;
  verifier-derivable), model tree (preprocessed; weights; publisher's commitment), base trace,
  interaction columns (LogUp), boundary trees (residual out, K/V out).
- Gadgets (`prover/src/gadgets/`): `freivalds` (weight matmuls via r^T W check against
  preprocessed weights), `dequant` (accumulator → bf16, chain of roundings), `requant`
  (bf16 → int8 with per-token scale), `attention` (key tiles, integer softmax; grows with C),
  `attn_out`, `rope` (rotation), `residual_stream` (norms, residual adds, SwiGLU, bf16 tables),
  `embed` (layer 0), `argmax` (head segment). Edge table in `docs/statement.md`; each
  `--unsound-skip-<name>` flag unbinds one edge and marks the run a control.
- Proof system: Circle STARK over M31 / QM31 (stwo fork), Blake2s Merkle channel, FRI with
  log_blowup 1, 100 queries, 0 PoW bits = 100 conjectured bits (`prover/src/util.rs`), LogUp
  lookups, five GKR reductions that prove the LogUp running sums instead of committing them
  (flags on by default; the paper configuration), Freivalds for matmuls.
- Not zero-knowledge in the hiding sense: SASH states the proof system "adds no random
  blinding to the committed trace". Weights are hidden only behind the commitment root.
- Quantisation (`y-delay-vw12`, `harness/witness/common.py`): int8 activations per token with
  dynamic scale, int8 weights per output channel, exact field accumulation, bf16 dequant chain
  (round half to even), bf16 nonlinearities, integer softmax (q 12 bits, k 11 bits, 9-bit
  numerator, exp lookup), 12-bit attention output, delayed V requantisation. Quality cost:
  +6.96 % perplexity vs fp32; task scores unchanged within error.
- Two backends, one cargo feature: SIMD (reference) and `--features cuda`. Both share witness
  and trace construction, hash channel, serialisation, digest. Rule: any change reproduces the
  pinned proof digests (`prover/README.md`, `prover/tests/`) on both backends before merge, or
  records new digests in the same PR. CI (`.github/workflows/ci.yml`) installs CUDA 12.9,
  builds both backends, runs SIMD tests; no GPU in CI, so CUDA digests are run by hand
  (`tools/gate/`; a 24 GB card suffices, the 8B reference needs 80 GB).
- Build facts: even the SIMD build needs the CUDA 12.9 toolkit (nitroo's build.rs runs cmake
  over 174 .cu files; `/usr/local/cuda/lib64` hardcoded). No GPU needed to build. macOS only
  type-checks (`cargo check`), does not link. Repeated CLI flags: last occurrence wins.
- Harness runs on CPU: `cd harness && uv sync`; CI runs six self-tests: `witness.selftest`,
  `eval.selftest --cpu`, `witness.extract --selftest`, `eval.baseline.decode_bench --selftest`,
  `costmodel.key_tile --selftest`, `costmodel.exact_cells --selftest`. `exact_cells` rebuilds a
  segment's trace layout from a `params` block and must reproduce every recorded chunk's
  `cells.base/interaction/fresh` exactly (points in `costmodel/exact_chunks.json`).
- Witness path: HF Transformers forward pass in fixed arithmetic → dump per layer → extractor
  (`harness/witness/extract.py`) → plan file (`plan.py`, `shapes.py` compute shared pins such
  as `--kmax --ao-rem-bits --fold-rem-bits --fold-alpha` as the worst case over a loop) →
  `zk-prover compose-chunks` loop. Baseline: vLLM and HF with nothing proved.

## Measured numbers (Llama-3.1-8B, one H100, 4,096-token prompt + 512 generated)
- Proving: loop 3,683 s (61 min), whole-wall 5,485 s (91 min); 1.25 positions/s;
  $0.73–$1.09 per 1,000 positions ($3.37–$5.01 per request at $3.29/GPU-h).
- Cells: ~79 M committed per position (105 M at C = 16,384). Commit rate ~2.1 Gcell/s;
  loop rate ~99 Mcell/s.
- Phase split of a serial loop over 32 layer segments (748 s, `secs.phase.c4096.kernels.*`):
  LogUp interaction columns + GKR 41.8 %, base trace 35.4 %, load/decode/check/build 11.8 %,
  other host 6.4 %, STARK commit + prove 4.6 %. With constraint kernels left on the CPU the
  STARK part alone is 3,984 s: that optimisation is done; the remaining host-side witness
  generation is the ceiling (issue #2).
- Proof: 18.5 GiB serialised (~65 MiB per segment), 7.2 GiB compressed. Verification ~2 min
  on CPU per SASH's note (repo's consumer-machine figure: 43 s per segment, dominated by
  rebuilding the shape tree).
- Baseline: vLLM ~42,000 prompt positions/s, ~153 generated/s, ~1,340 for the whole request;
  HF ~33,000 / ~57. Overhead 400–1,100× depending on prompt share.
- Projections (repo cost model, "projected" grade): 70B 5–8 h, 405B 16–24 h, 1T dense
  32–48 h per request; loop could drop to ~30 min (measured port factors) or ~12 min
  (assumed 8× on host work, unmeasured).

## Repo rules (`CLAUDE.md`, binding)
- Read only your issue and the files it names; nothing else unless named.
- Standard words, no new nouns; `tools/words.py` checks prose, CI runs it.
- Never append to a document; the PR is the record: what changed, digest gate result on both
  backends, binding table if it moved. Decisions go in `docs/decisions/` as dated files.
- `--unsound-skip` in a shown command is a red flag. Never commit weights, witnesses,
  results or logs. Commit only when asked.

## Open issues, grouped (all unassigned, all created 26 Sep 2026)
- Gadget refactor, tracking #28 with sub-issues #14–#29 (one column schema per gadget,
  row-level constraint tests, per-gadget digests #24, census test #23, per-family timing #26,
  second architecture #27). Owner is mid-refactor (open PR #1 on Freivalds readability).
- Defects: #2 host witness gen → GPU; #4 unexplained digest moves; #6 one attention shape on
  CPU; #7 memory without GKR at long C; #8 greedy decode non-determinism in baseline;
  #9 `family_cells` lacks an argmax counter (131,727,360 base cells unattributed per head
  segment); #10 no bias site, so Qwen cannot be proved; #11 `gen_ids` corpus cut at 20,480
  tokens and power-of-two assert; #12 build memory; #13 counted registration short five cells
  per table row because `witness_fields.py` uses each dump's own `ao_rem_bits` while the loop
  proves the shared pin (answer key: `runs/2026-09-13-block-length-c4096-s256-h100`, counted
  25,448,257,392 vs measured 25,608,247,152, short 159,989,760).
- Soundness: #3 negative-control suite must cover the model tree; #5 attention-output seam
  control panics on a real dump; #30 promote `claimed_h` tie to an assert.
- GPU-free entry points: #13 and #11 (Python harness), #9 partly (Rust JSON output; digest
  should not move but the gate must be run).

## SASH's stated status and roadmap (research note + ZKP intro post, Sep 2026)
- "The prototype is a measurement tool, not something anyone should rely on yet."
  "Nobody outside our team has checked the correctness of our implementation."
- Roadmap: prover optimisation (1.25 → 16 positions/s; commitment alone could do 27), real
  70B/405B runs, closing the gap to real serving (bf16/fp8 arithmetic, tokenisation,
  non-determinism, batching, architecture hiding, binding to traffic records), sub-sampling of
  segments after the provider commits to boundary roots, streaming for long contexts,
  restructuring into small auditable gadgets.
- Sampling argument: proving a random fraction p of requests; a provider cheating m times
  escapes with probability (1−p)^m; at p = 1 % about 460 cheats before 99 % detection.
- Public goods they ask for: a specification of what an inference proof must cover, a corpus
  of negative controls, machine-checked constraint systems.

## Not yet understood
- Internals of `compose.rs` (8.8k lines), `gkrlink.rs`, `gkr_key_tile.rs`, `layer.rs`,
  `boundary.rs`, `cudagen.rs` (kernel generator), `devacc.rs`/`devpre.rs`/`devlogup.rs`
  (device witness generation): only the module map and docstrings have been read.
- How the five GKR reductions link into the AIR (`gkrlink`) and what `claimed_h` is (#30).
- The exact layout arithmetic in `harness/costmodel/exact_cells.py` (1,903 lines) and the
  registration path in `harness/eval/predict/` (`witness_fields.py`, `predict.py`, `compare.py`).
- The full text of the suggested fix at the end of issue #13 (cut off when read).
- Whether other shared pins (`kmax`, `fold-rem-bits`, `fold-alpha`) have the same mismatch
  as `ao_rem_bits` in a counted registration.
- How `predicted.json` / `card.json` are produced by `tools/drivers/block-length-c4096.sh`
  and checked by `tools/constants/audit.py`.
- `tools/gate/*.sh` in detail; how CI treats a first-time fork PR.
- nitroo's four local changes beyond their README descriptions.

## Sources
- https://github.com/sg-ai-safety-hub/zk-inference-prover and .../zk-inference-results
- https://www.aisafety.sg/research/what-proving-llm-inference-actually-costs-research-note
- https://www.aisafety.sg/blog/zkp-intro
