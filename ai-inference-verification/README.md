# AI inference verification

Notes and interactive pages made while studying how a zero-knowledge proof can show that an
AI model really produced an answer, built around SASH's open `zk-inference-prover`
(github.com/sg-ai-safety-hub/zk-inference-prover) and Pascal Berrang's paper
"Zero-Knowledge Model Checking" (arXiv 2605.00487).

Each page is a single HTML file. Download it and open it in a browser; the figures are
interactive. The "Ask Claude" box on the primer only works when the page is opened inside
claude.ai; elsewhere it saves notes locally and says so.

## What's inside

- **[berrang-primer.html](./berrang-primer.html)** — the long read. The problem (who needs to
  verify an AI system, and when), what SASH is, why proving is slow (measured phase split),
  formal verification as a black box with a testing-versus-proving figure, the paper's sealed
  non-membership proof, Farkas' lemma and folding, what Berrang is building, and where the work
  is heading.
- **[zk-inference-flow.html](./zk-inference-flow.html)** — the end-to-end flow of the prover:
  from the witness dump through the grid of segments, the five committed trees, the gadgets
  and seams of one layer, the trust boundary and the numbers, with a glossary and a self-check.
- **[decode-and-prove.html](./decode-and-prove.html)** — a step animation: an LLM decoding on
  the left, the prover on the right, over three real Llama-3.1-8B prompts, twenty steps each,
  with the gadget, edge and tree status at every step.
- **[handoff.md](./handoff.md)** — working notes: repo layout, reading order, what is
  established, measured numbers, repo rules, open issues grouped, SASH's stated roadmap, and
  what is not yet understood.
- **[data/](./data/)** — the real numbers behind the animation. `llama31-8b-tokens.json` is
  the three prompts tokenised with the Llama-3.1 tokenizer; `llama31-8b-decode-run.json` is
  the output of running `unsloth/Llama-3.1-8B-Instruct` in bf16 (Apple M4 Pro, MPS, 7 Oct
  2026): four greedy tokens per prompt with top-5 logits, per-layer residual RMS, attention
  rows for layers 0, 15 and 31 head 0, and the layer-0 norm output with its int8
  requantisation under the harness's rule.
- **[tools/](./tools/)** — how those numbers and the animation were made. `tokenize.py` and
  `infer.py` produce the two data files (they need `torch`, `transformers` and
  `huggingface_hub`, and download the 16 GB weights into `HF_HOME`); `build.py` injects the
  run data into `decode-and-prove.template.html` and writes `decode-and-prove.html`. Run all
  three from this directory.

## Where to start

1. Read `berrang-primer.html` sections 1 to 3 for the problem and the cost.
2. Open `decode-and-prove.html` and step through one prompt.
3. Use `zk-inference-flow.html` when reading the code; `handoff.md` lists the reading order.

## Sources

- SASH research note: https://www.aisafety.sg/research/what-proving-llm-inference-actually-costs-research-note
- SASH ZKP intro: https://www.aisafety.sg/blog/zkp-intro
- Paper: https://arxiv.org/abs/2605.00487
- Code: https://github.com/sg-ai-safety-hub/zk-inference-prover and https://github.com/sg-ai-safety-hub/zk-inference-results
