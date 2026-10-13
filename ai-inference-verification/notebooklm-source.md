# zk-inference-prover: study source for NotebookLM

Compiled 10 October 2026 from four sources: two study pages built in this study ("ZK Inference Prover Flow" and "Decode and Prove"), the public repositories `sg-ai-safety-hub/zk-inference-prover` and `sg-ai-safety-hub/zk-inference-results` (their documents are quoted verbatim in Part 4), a real run of `unsloth/Llama-3.1-8B-Instruct` on an Apple M4 Pro (Part 3), and the working notes (Part 5). Numbers labelled "measured" come from the results repository's constants; "projected" numbers come from its cost model. The author of the repositories is Pascal Berrang (GitHub `paberr`), who made all 485 commits between 19 August and 26 September 2026.

Vocabulary used throughout: a **segment** (the code says "chunk") is one transformer layer, or the output head, applied to one block of S = 512 token positions against a context of C earlier positions, proved as one STARK. A **cell** is one committed field element of one trace column at one row. An **edge** is a seam between two gadgets that the verifier checks by comparing claims; there are 16 per layer segment. A **gadget** is one step of the decode stated on its own with its own columns, constraints and published claims.

---

# Part 1. Orientation: what the system proves and how

## The statement

Greedy decoding of a quantised Llama-3.1-8B. For published prompt ids and a published 512-token continuation, every layer of every position is proved, from the embedding row to the argmax, with the residual stream bound between layers and the key/value cache bound between token blocks. The verifier's inputs are the prompt ids, the model commitment (the root of the weight tree, from the publisher's manifest) and the per-layer calibration, from which the verifier rebuilds the shape tree itself and compares roots. The verifier holds no weights and needs no GPU.

The arithmetic proved is a fixed quantisation configuration named y-delay-vw12: int8 activations per token with a dynamic scale, int8 weights per output channel, exact integer accumulation, a chain of correctly rounded bf16 steps for dequantisation, bf16 nonlinearities, an integer softmax (queries 12 bits, keys 11 bits, a 9-bit numerator from an exp lookup table), a 12-bit attention output, and the value projection's requantisation delayed to its consumer. Its cost against fp32: +6.96 % perplexity on the 8B model, task scores unchanged within error.

The proof is not zero-knowledge in the hiding sense: no random blinding is added to the committed trace. Weights are hidden only behind the Merkle root of the model tree.

## The unit of proof and the grid

A request is a grid of segments: for a 4,096-token prompt plus 512 generated tokens, 9 token blocks times 32 layers plus 2 output-head segments = 290 proofs. There is no recursion. Adjacent segments are tied by Merkle roots: a layer's residual-stream output root must equal the next layer's residual-stream input root (281 layer links), and a block's key/value output root must equal the next block's committed key/value prefix (256 token links). The head is proved over the last prompt block and over the generated block so that every emitted id is backed by a proved argmax for the position before it. `boundary-grid --verify --prompt --verify-calibration` performs these checks after the run.

## The five kinds of Merkle tree in one segment

| Tree | Holds | Why it is separate |
|---|---|---|
| 0, shape tree | selectors, the causal mask, the marker for real key rows, lookup tables (exp, bf16 NORM/FRAC/POW, ranges), RoPE angles for this block's absolute positions | a pure function of the statement parameters plus the per-layer calibration; the verifier rebuilds it and rejects on root mismatch; cached per (layer, shape) |
| 1, model tree | int8 weights and per-channel scales, the embedding matrix, lm_head | the verifier cannot derive it; its root is compared with the publisher's manifest; committed once per layer |
| 2, base trace | every value the prover chose for this segment: activations, accumulators, bf16 patterns, scores, numerators, ids, lookup multiplicities | the prover's claim; committed before any challenge so lookups and Freivalds are binding |
| 3, interaction | the LogUp fractions and running sums that remain after the five GKR reductions | depends on the challenges, so it can only be committed after they are drawn |
| 4+, boundary | residual stream in, residual stream out, keys and values out, and nothing else | a neighbouring segment compares against exactly these roots; bound to base columns by plain equality constraints checked at the out-of-domain point, so they can be committed after the interaction tree |

## The transcript of one segment proof, in order

1. Commit tree 0, tree 1, tree 2; mix each root into a Blake2s channel.
2. Draw the relation elements (z and alpha per lookup table) and the Horner challenges r, s, rv, and the binding pair w, lambda.
3. Build every LogUp fraction and running sum; run the five GKR sumchecks (key tiles, dequant, residual stream, Freivalds, attention output); commit tree 3.
4. Commit the boundary trees.
5. stwo: draw the out-of-domain point, evaluate the composition polynomial (generated CUDA kernels), FRI with log blowup 1 (blowup 2), 100 queries, 0 proof-of-work bits = 100 conjectured bits.
6. Serialise three files: Fixed (the statement), Claims (every published sum and fold), Proof (about 65 MiB).

## The measured numbers (Llama-3.1-8B, one H100, 4,096 prompt + 512 generated)

| Quantity | Value |
|---|---|
| Segments | 290 |
| Proving loop | 3,683 s (61 min); whole wall 5,485 s (91 min) |
| Throughput | 1.25 positions/s |
| Cost per request | $3.37 to $5.01 at $3.29 per GPU-hour |
| Cells per position | about 79 million (105 million at C = 16,384) |
| Commit rate / loop rate | about 2.1 Gcell/s / about 99 Mcell/s |
| Phase split of a serial 32-layer loop (748 s) | LogUp interaction + GKR 41.8 %; base trace 35.4 %; load/decode/check/build 11.8 %; other host 6.4 %; STARK commit + prove 4.6 % |
| Proof size | 18.5 GiB serialised, 7.2 GiB compressed |
| Verification | about 43 s per segment on four consumer CPU cores, dominated by rebuilding the shape tree |
| Baseline | vLLM about 42,000 prompt positions/s, 153 generated/s, about 1,340 for the whole request; overhead 400 to 1,100x |
| Projections | 70B: 5 to 8 h per request; 405B: 16 to 24 h; 1T dense: 32 to 48 h |

## Where the time goes and what is left

Constraint evaluation already runs on the GPU through generated kernels; with those kernels left on the CPU the STARK part alone took 3,984 s, so that optimisation is done. The ceiling now is host-side witness generation: building the columns and the lookup bookkeeping on the CPU (issue #2). The five GKR reductions replaced committed lookup columns: at C = 16,384 the interaction tree went from 93,184 columns to 5,600.

---

# Part 2. The "ZK Inference Prover Flow" page, full text

ZK Inference Prover Flow

ZK Inference Prover Flow v2 · 7 Oct 2026

Study notes · sg-ai-safety-hub / zk-inference-prover · read against the code on disk

# How one proved decode is built, end to end
The whole flow of the SASH prototype, from a prompt to a verified grid of STARK proofs, with every component placed where it really sits in the code. Written so you can see which parts you own and which parts are still fog.
Subject Llama-3.1-8B, greedy decode, 4,096 + 512 positions Proof system Circle STARK over M31 (stwo fork), LogUp, 5 GKR reductions, Freivalds Sources prover and results repositories at their 7 Oct 2026 state

Abstract
A ZK inference proof is a receipt that one specific computation happened. This note follows the SASH prototype from the user's prompt to a verified grid of 290 STARK proofs. The prompt is tokenised outside the proof; the ids are the public input. The model is rerun in fixed arithmetic and every intermediate value is dumped as the witness. Each layer-by-block segment becomes a table of columns over the Mersenne-31 field, committed as five Merkle trees whose roots seed the challenges; the constraints are checked and a STARK is written. A CPU verifier checks each proof alone, then checks that neighbouring segments agree on their boundary roots and that each emitted id is the argmax the head proved. Two things it does not do: it is not hiding in the zero-knowledge sense, and nothing in it is formally verified.
prover-chosen, committed public, verifier-derived or checked outside the statement (not proved)

0 · The whole flow on one screen

## From a prompt to a verified grid, as a directed graph
Read top to bottom. Plum is outside every proof, teal is public or verifier-side, amber is what the prover chooses and commits. Every arrow is a real data dependency in the code.

1 – 2 · IN THE OPEN, NOT INSIDE ANY PROOF
Prompt
text from the user
tokeniser + template
(not proved)
Token ids
public input of every proof
The verifier is handed these ids.
The text itself is never inside a proof.
next id appended, one per step, 512 steps
3 – 4 · THE MODEL, RERUN IN FIXED ARITHMETIC, EVERY STEP RECORDED
residual stream flows left to right →
Every op is written out:
int8 matmul, exact int32 sum,
bf16 norm and SwiGLU,
integer softmax, RoPE tables.
No fused kernel hides an order.
Embedding
row lookup
Layer 0
norm · attn · mlp
Layer 1
same constraints
…
Layer 31
32 layers in all
Head
logits, 128k wide
argmax
greedy
dump
Witness: every intermediate value, per layer, per 512-token block
int8 activations · int32 accumulators · bf16 bit patterns · attention scores · K/V · residual in and out — your step 4, kept rather than thrown away
5 · ONE SEGMENT (ONE LAYER × 512 POSITIONS) BECOMES ONE PROOF, 290 TIMES
Witness tables
one layer
one block
encode
Columns
rows × cols over M31
the polynomial table
commit
Merkle trees
5 trees → 5 roots
32 bytes each
shape · model · trace
interaction · boundary
mix
Hash channel
Blake2s
Fiat–Shamir
draw
Challenges
random r, s, z, α
after commitment
check
Constraints
lookups · Freivalds
softmax · roundings
prove
STARK proof
OODS + FRI
~65 MiB
Order is the point: each challenge is a hash of everything committed before it, so the prover cannot fit its values to the randomness.
6 · VERIFY EACH PROOF, THEN CHECK THE DEPENDENCIES BETWEEN PROOFS
proof
statement + claims
token ids
calibration + roots
Verifier
CPU only, holds no weights
· replays the hash channel
· rebuilds the shape tree, root must match
· model root = published commitment
· stwo verify, then the application identities
· argmax id = the next published id
accept or reject, per segment
then every root equality between neighbours
The dependency graph between segments
head
head
L2 · B0
L2 · B1
L2 · B2
L1 · B0
L1 · B1
L1 · B2
L0 · B0
L0 · B1
L0 · B2
residual
root =
K/V root =
→ emitted ids
layer 2
layer 1
layer 0 + embed
block 0
block 1
block 2 (generated)
Every arrow is one Merkle-root equality the grid checks.
Acyclic by construction: layers go up, blocks go right. 32 × 9 in the real run.
Figure caption: One request end to end. The prompt is tokenised outside the proof; the ids are the public input. The model is rerun in explicit fixed arithmetic and every intermediate value is kept as the witness. Each layer-by-block segment becomes a table of columns over the Mersenne-31 field, committed as Merkle trees; the roots seed the challenges, the constraints are checked, and a STARK proof is written. A CPU verifier checks each proof alone, then checks that neighbouring segments agree on their boundary roots, and that each emitted id is the argmax the head proved for the position before it.

### Your six steps, mapped onto the picture
- The user sends the prompt. Top-left plum box. Text never enters a proof.
- It creates the tokens. The teal box. The ids are the one public input the verifier is handed; the tokeniser itself is unproved.
- It goes to the model. The row of boxes: embedding, 32 layers, head, argmax. Each emitted id is appended and the row runs again, 512 times.
- The model has many intermediate steps. Every one of them is dumped into the amber witness bar. That is what makes the next band possible.
- The table and the Merkle tree. Band 5. The witness becomes columns over the field (the "polynomial table"), committed as five Merkle trees. The roots are hashed into challenges, the constraints are checked under those challenges, and the STARK compresses the result. This happens once per segment, 290 times.
- Verify the dependencies. Band 6. Each proof is checked on its own, and then the grid: every vertical arrow is a residual-stream root equality, every horizontal arrow a K/V root equality, and the head's argmax must equal the next published id. That graph is acyclic by construction, so there is no recursion anywhere.

1 · The intuition in one paragraph

## A proof that a specific arithmetic happened, not that a model is smart
A ZK inference proof is a receipt for a computation. The provider says: "with these token ids, under this committed model, I ran a greedy decode and got these 512 tokens." The verifier wants to check that claim without rerunning an 8-billion-parameter model and without seeing the weights. The whole machine exists to turn "I ran the model honestly" into a set of polynomial equations that a dishonest prover cannot satisfy, plus a short randomised test that those equations hold.
Three ideas carry everything:
- Commit first, then get challenged. The prover writes every intermediate value of the forward pass into tables, hashes them into Merkle trees, and only then receives random challenges derived from those hashes. Nothing can be changed after the fact.
- Constrain every row. Each table row must satisfy small algebraic rules (an int8 times int8 accumulates correctly, a bf16 rounding is the correctly rounded one, a softmax numerator comes from the exp table). Rules are the "circuit", here called the AIR.
- Check at random points. A STARK does not check every row. It checks that the constraint polynomials are low-degree at a handful of random points. If the prover cheated on even one row, the polynomial is no longer low-degree and the test fails with overwhelming probability.

What "zero knowledge" means here
The repository is honest that it is not hiding in the cryptographic sense: no random blinding is added to the committed trace. What is hidden is only the weights behind a Merkle root. So the word "ZK" in the name is the proof-system family, not a privacy guarantee. Keep that distinction sharp in an interview.

2 · Your six questions, placed

## Where each thing you named actually lives

Formal verificationnot present
There is no formal verification in this system. Nothing machine-checks that the constraint system equals the model's arithmetic. What exists instead is empirical: a digest gate (every change must reproduce byte-identical proofs on both backends), negative controls (tamper one value, confirm the verifier rejects), and self-tests that rebuild cell counts from the layout. SASH lists "machine-checked constraint systems" as a public good they want. If you say "formal verification" about this code, that is a weak spot.

The ZK proof systemstage 6 · prover/
The proof system is the thing that turns a committed trace plus constraints into a short argument. Here it is a Circle STARK from StarkWare's stwo, vendored as nitroo/ with a CUDA backend. The prover crate (compose.rs) states one segment as an AIR over it. "Proof system" and "STARK" are the same component seen at two levels.

STARKstage 6, last step
The STARK is the last thing that happens in a segment proof: after every tree is committed and every challenge drawn, stwo's prove() does out-of-domain sampling and FRI over the whole constraint set. It is about 4.6 percent of loop time. The expensive part is building the trace the STARK proves, not the STARK itself.

Merkle treeseverywhere, five roles
A Merkle tree is how a table of field elements becomes one 32-byte commitment. One segment commits five kinds of tree: the shape tree, the model tree, the base trace, the interaction columns, and the boundary trees. Two of those roots have a life outside the proof: the model root is the publisher's weight commitment, and the boundary roots are what make adjacent segments chain. See section 5.

Prefill and precomputationstages 1 to 3, and tree 0
Two different things hide behind this word. (a) Prefill in the LLM sense: the prompt's 4,096 positions are proved too, as 8 blocks of 32 layer segments; nothing is "just cached". (b) Preprocessed trees in the STARK sense: the shape tree and the model tree hold columns that do not depend on the input (selectors, lookup tables, quantised weights). They are committed once per (layer, shape) and reused across segments via a device-side cache.

The proving partstage 6 · compose-chunks
"Proving" is one Rust process looping over a plan file, one segment per line. Each segment is generate() (build every column, on GPU where a kernel exists) then prove_gen() (commit, challenge, interaction, GKR, boundary, STARK). 290 segments for the c4096 request; 61 minutes of loop on one H100.

3 · The flowchart, as the sequence job runs it

## Seven stages from prompt to verdict
This is the order tools/drivers/lib/sequence-job.sh executes on the GPU host. Amber stages are the prover's side (they choose values and commit to them). Teal stages are the verifier's side or are derivable by anyone from public data.

1
Harnesspython · GPU

Generate the statement's token ids. Take a 4,096-token prompt from the fixed corpus, run the quantised model greedily for 512 new tokens, write prompt ∥ continuation. This decode is itself the thing being proved. Greedy means argmax, so the emitted token is a deterministic function of the logits.
python -m harness.witness.gen_ids --prefix 4096 --new 512 --spec y-delay-vw12
ids_512.npy

2
Harnesspython · GPU

Extract the witness. Rerun the forward pass in explicit fixed arithmetic (every op written out, no fused kernels) and dump, per layer and per 512-token block, every value a constraint will read: int8 activations, exact int32 accumulators, bf16 scales and patterns, attention scores, K/V tiles, the residual stream in and out. Layer 0 also dumps the embedding rows. This is the single most expensive host step and the data is ~27 GB for a 14B model.
python -m harness.witness.extract --tokens 4608 --chunk 512 --layers 0..31 --blocks all --residual-stream --diagonal-block
witness_B<b>_L<k>/ (arrays + manifest.json) shared/ (weights, tables)

3
Harnesspython · CPU

Shape table and plan file. Read every dump's manifest, compute the model-wide worst case for the pins every segment must share (--kmax, --ao-rem-bits, fold widths), refuse early if a layer would not fit the field's 31 bits, and write one plan line per segment: 9 blocks × 32 layers + 2 head segments = 290 lines.
python -m harness.witness.shapes … ; python -m harness.witness.plan --dir W --blocks 9 --head-blocks 7,8
shapes_all.json plan.txt

4
Setuprust · once per shape

Emit and install CUDA kernels. For each distinct constraint shape in the plan, lower the AIR to straight-line IR, check that lowering against the CPU evaluator on random data, generate .cu files, and rebuild the CUDA backend with them. Without this step the GPU build still works but evaluates constraints on the CPU, and the proof digest does not change either way.
zk-prover cudaemit … ; zk-prover genemit … ; python kernels/install_constraint_kernels.py
prover/kernels/ store (fingerprinted)

5
Publisherrust · once per model

Commit the model. For every (layer, context) cell, build only the preprocessed trees and read off two roots: the shape root (verifier can recompute it) and the model root (commits the int8 weights and per-channel scales; only the publisher can make it, anyone can compare against it). The manifest also carries the per-layer attention calibration the verifier needs.
zk-prover model-roots --out model-roots.json
model-roots.json (shape root, model root, frac_per_head per layer)

6
Proverrust · GPU · the loop

Prove every segment. One process per 64 plan lines, pipelined so segment k+1 is generated while segment k is proved. Each segment: load and decode its dump → build every gadget's columns → commit the five trees → draw challenges → build LogUp interaction columns and run the five GKR sumchecks → commit boundary trees → stwo STARK prove → serialise three files. Section 5 opens this box.
ZK_PIPELINE=1 zk-prover compose-chunks $SHARED --plan plan.txt --plan-slice 0:64 --ser-dir SER
<tag>.fixed.json (statement) <tag>.claims.json <tag>.proof.json (~65 MiB)

7
Verifierrust · CPU only

Boundary grid: verify and chain. On the SIMD build, with no card: for each segment replay the transcript, rebuild the shape tree from public parameters and compare its root, compare the model root with the manifest, run stwo's verify(), and check every application identity. Then check every link: residual-stream roots between consecutive layers (layer axis) and K/V roots between consecutive blocks (token axis). Finally chain the ids: each prompt id against the published prompt, each generated id against the argmax a head segment proved for the previous position.
zk-prover boundary-grid --dir SER --plan plan.txt --verify --prompt prompt.json --verify-calibration model-roots.json --expect-layer-links 281 --expect-token-links 256
grid.json: links_passed / links_run, all_chain, per-segment verify_secs
Figure caption: The seven stages of a headline run, in the order sequence-job.sh executes them. Stages 1 to 3 and 6 are the prover's side; 4, 5 and 7 are derivable or checkable by anyone holding the public inputs.
A gate script then refuses the run if any segment lists an --unsound-skip, any edge is unbound, any kernel fell back to the CPU, or any link failed. Only then does the run become a row in constants.json.

4 · The unit of proof

## A request is a grid, not one proof
There is no recursion and no single proof of the whole request. The statement is cut into segments: one transformer layer applied to one block of S = 512 positions, against a context of C earlier positions. The c4096 request below is 9 token blocks (8 prompt blocks and 1 generated block) times 32 layers, plus the output head proved twice.

B0
B1
B2
B3
B4
B5
B6
B7
B8
head

argmax
argmax
L31

…

L1

L0
emb
emb
emb
emb
emb
emb
emb
emb
emb
layer 0 also binds the embedding row (edge 15) B8 is the 512 generated positions head segment binds logits to the emitted id (edge 16)
Figure caption: Columns are token blocks of 512 positions; rows are layers. Vertical neighbours share a residual-stream boundary root (layer links: 9 × 31 + 2 = 281, which the driver computes as NBLOCK × (NLAY−1) + NHEAD). Horizontal neighbours share a K/V boundary root at that layer (token links: 8 × 32 = 256). The head sits on B7 as well as B8 because the first generated token's argmax was computed at the last prompt position.
Why this shape? Attention at block b reads keys from blocks 0 to b. So every segment proves "my 512 queries against the C committed keys", and the K/V boundary root is what ties "the keys I attended over" to "the keys the previous block actually wrote". Without that root each segment could be honest while the sequence lies.

5 · Inside one segment proof

## The transcript: five trees, then challenges, then the STARK
This is compose::generate followed by compose::prove_gen_to. The order matters because it is the Fiat-Shamir transcript: each root is mixed into a Blake2s channel, and every random challenge is drawn from that channel after the things it must not be able to influence have been committed. The serialised proof's SHA-256 is the digest gate, so even the column order inside a tree is load-bearing.

tree 0
Shape treepreprocessed · verifier rebuilds it
Every column the AIR reads as a fact: selectors, the causal mask, the marker for real key-grid rows, range-table row indices, the exp and norm and fraction lookup tables, RoPE cos/sin for this block's absolute positions. A pure function of the statement's params plus the per-layer calibration. No weight enters, so the verifier derives the root itself and rejects on mismatch (decision of 2026-09-09).

tree 1
Model treepreprocessed · publisher's commitment
The int8 weights of this layer's seven matmuls (and the lm_head and embedding matrix on the segments that need them), plus per-channel scales. The verifier cannot derive this root; it compares it with the published manifest. Cached on the device per (layer, shape) so the loop pays the commit once per layer, not once per segment.

tree 2
Base tracecommitted · the witness
Everything the prover chose: int8 activations, accumulators, bf16 patterns of the residual stream, attention scores and numerators, requantised K/Q/V, the token ids, the lookup multiplicities for every table. This is where the 79 million cells per position mostly live. Committed before any challenge, which is what makes the lookups and the Freivalds checks binding.

draw
Challengesfrom the channel
Relation elements for every lookup table (the z and α of each LogUp relation), then the Horner weights r, s, rv that compress whole matrices into one field element, the binding challenge for the residual-stream claims, and the diagonal-block challenge. Only now can the prover compute interaction columns.

GKR
Five sumcheck reductionsproved, not committed
The LogUp running sums for the key tiles, dequant, residual stream, Freivalds and attention output are proved with a GKR sumcheck instead of being committed as columns. It shrinks the interaction tree from 93,184 columns to 5,600 at C = 16,384. The gkrlink module then ties the GKR's final claims to the committed base columns with one MLE-evaluation IOP per distinct height, so the sumcheck is about the real data and not about numbers the prover made up.

tree 3
Interaction treecommitted · LogUp columns
What remains of the lookup argument after GKR: the fractions and partial sums that make every table lookup (range checks, exp table, bf16 unary tables, the (q, nz) pair table, the embedding scan) a sound multiset argument. 41.8 percent of loop time is spent building this plus the GKR.

tree 4+
Boundary treescommitted · the chain links
Two small trees per axis: residual stream in and out, K/V written by this block. Bound to the base columns by a plain equality constraint (no lookup, no challenge), which is why they can be committed after the interaction tree. Their roots are the only thing another segment's proof ever compares against. A shared challenge would have been unsound, because knowing the challenge before committing makes "my image equals yours" one linear equation to solve.

STARK
stwo prove()OODS + FRI · 4.6 % of loop
Draw the out-of-domain point, evaluate every constraint's quotient there (the generated CUDA kernels do this), commit the composition polynomial, then FRI with log blowup 1, 100 queries, 0 proof-of-work bits = 100 conjectured bits of security. Output: ~65 MiB per segment, serialised with the Fixed statement and the prover's Claims.
Figure caption: The transcript of one segment proof, top to bottom. Each root is mixed into the Blake2s channel before the next challenge is drawn, so the serialised byte order is the soundness argument and the proof's SHA-256 is the gate.
The verifier (verify_composed) takes exactly three byte strings, replays this transcript, recomputes every challenge from its own channel, runs stwo's verify(), checks the claimed LogUp sums cancel to zero, and then checks the application identities: for each key tile the Q·Kᵀ and denominator claims, for the attention output the A·V fold, and for each matmul the Freivalds equality h_m == acc_m. No prover-side struct ever crosses into the accept path.

6 · What is inside the base trace

## One layer, as gadgets and the seams between them
A gadget is one step of the decode stated on its own: it owns its column layout, its constraints and the claims it publishes. Composition is the act of comparing one gadget's published output claim with the next gadget's input claim, under the same challenge. Edge numbers are the binding table in docs/statement.md.

13 in
residual stream in
boundary tree, equality to gn1 leaves
root link

1
RMSNorm 1
residual_stream: bf16 square, tree-sum, rsqrt table, mul
bound

2
requantise → int8
requant: max argument + ceil-divide table + division table
seam

12
q, k, v matmuls
freivalds: rᵀW·x check against tree-1 weights, shared input
own AIR

—
dequantise → bf16
dequant: NORM + FRAC lookups, correctly rounded chain
bound

3
RoPE + quantise
rope: bf16 rotate with preprocessed cos/sin, pow-2 requantise per head
seam

4
attention
attention: Q·Kᵀ over key tiles, integer softmax via exp table, causal mask from tree 0; grows with C
own AIR

5
attention out → int8
attn_out: A·V fold, rounding identity with ao_rem_bits window
seam

12
o matmul
freivalds
own AIR

6
residual add 1
residual_stream: bf16 add (POW, NORM, FRAC)
bound

7, 8
RMSNorm 2 → int8
residual_stream + requant
seam

12
gate, up matmuls
freivalds, shared input
own AIR

9
SwiGLU
residual_stream: silu unary table × bf16 mul
bound

10
requantise → int8
requant
seam

12
down matmul
freivalds
own AIR

11
residual add 2
residual_stream
bound

13 out
residual stream out
boundary tree, equality to gn2 outputs
root link

14
K, V written
boundary tree on the token axis (diagonal block only)
root link
Figure caption: One layer segment as the gadgets that state it and the seams between them. Highlighted rows are the matmuls, each proved by a Freivalds check against the weights in the model tree. Edge numbers follow the binding table in docs/statement.md.
Layer 0 adds edge 15 (embed: a lookup scan over the whole V × d embedding matrix in tree 1, binding the residual-stream input to the committed ids). The head segment adds edge 16 (argmax: a monotone indicator proving the emitted id is the lowest-indexed maximum, which is what torch.argmax returns; 15 of 512 rows have ties, so lax vs strict is not academic).

### The Freivalds trick, because it is the one most worth being able to derive on a whiteboard
Proving Y = W·X cell by cell for an 8B model would be hopeless. Instead the verifier draws random r after everything is committed, and the prover shows rᵀ·Y == (rᵀ·W)·X. The left side is a Horner fold of the committed accumulators (the dequant gadget already holds them, so nothing is committed twice). The right side is computed in the Freivalds gadget from the preprocessed weights and the committed int8 activations. If Y ≠ W·X anywhere, the two sides agree with probability about 1/p over the choice of r. The cost is linear in the number of weights rather than cubic, which is why the cost model charges a fixed number of cells per weight.

7 · The trust boundary

## What this proof says, and what it does not
A proof here says: "these prompt ids, under the model whose root is R, produce these 512 ids under greedy decoding in the y-delay-vw12 quantised arithmetic." Everything in the plum column is outside that sentence. zk-inference-results/docs/statement-gap.md has the row-by-row version.

Arithmeticgap Proved: int8 weights, int8 activations, bf16 nonlinearities, integer softmax. Served: bf16 or fp8 on whatever kernels vLLM picks. Cost of the gap: +6.96 % perplexity on 8B. No one has counted what a bf16 statement would cost.
Decodinggap Proved: greedy, no stop at EOS. Served: temperature and top-p sampling with early stop.
Determinismgap · issue #126 The proof is about one decode. Rerunning the same prompt on the HF backend did not reproduce the same ids three times out of three. So "verify by rerunning" is not a check anyone can make.
Tokenisationgap The public input is ids, not text. Tokeniser and chat template are outside every proof.
Batchinggap No batch index in the statement. A provider batches 16 requests and pages the KV cache.
Traffic bindinggap No proof names a request, a client, or a time. It proves that ids map to ids under a commitment, not that anyone was served this.
Architecturegap · issue #174 Dense Llama only. No site for a projection bias (Qwen has one), no sliding window, no QK-norm, no MoE. The shape is public, so the architecture cannot be hidden.

How to say this in an interview
"The prototype proves a quantised stand-in for the model, segment by segment, and chains the segments by Merkle roots. It is sound about that statement and silent about the serving stack around it. The two biggest open problems are closing the arithmetic gap and moving witness generation off the host."

8 · The numbers that anchor the story

## Llama-3.1-8B, one H100, 4,096 prompt + 512 generated

| Quantity | Value | Why it matters | |
| Segments | 290 | 9 blocks × 32 layers + 2 head segments | |
| Proving loop | 3,683 s | 61 min; whole wall 91 min with extraction | |
| Throughput | 1.25 pos/s | vs ~1,340 pos/s unproved on vLLM: 400 to 1,100× overhead | |
| Cost per request | $3.37 – $5.01 | at $3.29 per GPU-hour | |
| Cells per position | ~79 M | committed field elements; 105 M at C = 16,384 | |
| LogUp + GKR share | 41.8 % | the largest phase; base trace 35.4 %; STARK itself 4.6 % | |
| Proof size | 18.5 GiB | ~65 MiB per segment; 7.2 GiB compressed | |
| Verify per segment | 43 s | on 4 consumer cores; dominated by rebuilding the shape tree | |
| Security | 100 bits | conjectured; blowup 2, 100 queries, 0 PoW | |
Every number above is graded in zk-inference-results/constants.json as measured, derived, projected, external or asserted, and names the run that produced it. Quote the grade with the number.

9 · Words that collide

## Terms with a precise local meaning

Segment / chunk One layer (or the head) over 512 positions at context C, proved as one STARK. "Chunk" is the identifier the code kept.
Cell One committed field element in one column at one row. The unit of prover work.
Statement Two serialised documents: Fixed (shape and gadget parameters, security config, tree sizes, the two preprocessed roots) and Claims (every Horner claim and LogUp sum the prover publishes).
Seam A requantise step between a bf16 producer and an int8 consumer, proved as its own component so the matmul multiplies exactly the integers the producer made.
Binding / edge A verifier-side equality between two gadgets' claims. 16 edges per layer segment; each --unsound-skip-* flag unbinds one and marks the run a control.
Key tile A group of attention heads packed onto one column set, over a slice of the C keys. The attention AIR is instantiated per key tile.
Diagonal block The 512 × 512 block where queries attend to keys in their own block, so the causal mask applies. Only this block writes K/V to the token-axis boundary tree.
Pin A flag that must take one value across the whole loop (kmax, ao-rem-bits, fold widths) and is set to the model-wide worst case by the shape table.
Digest gate SHA-256 of the proof bytes must reproduce on SIMD and CUDA before any change merges. The one place "correctness" is enforced mechanically.
Negative control A tamper (one row flipped, one byte of proof changed, a skip flag) that the verifier must reject. A control that is accepted fails the run.

10 · Where you stand

## Self-check: which of these can you explain without the page?
Tick what you can reconstruct from memory. Ticks are stored in this browser only, so this is for you. Untouched items are the next reading list.
0 / 14 tickedClear all
Why challenges must be drawn after commitment, and what breaks if they are not (the boundary-tree argument). The Freivalds identity, and why it costs linear rather than cubic work. What a LogUp lookup is and why a "running sum" column exists. What the five GKR reductions replace, and what gkrlink must do to keep that sound. The difference between the shape tree and the model tree, and who can derive each root. Why the request is a grid of segments and what the two kinds of boundary link are. What "edge 3 refuses Qwen" means and where a bias site would go. Why the argmax gadget needs the strict (lowest-indexed) form. What the witness extractor dumps and why it reruns the model instead of reading the real forward pass. What a pin is, why ao-rem-bits is model-wide, and how that caused issue #13's miscount. What OODS and FRI do inside stwo's prove(), at the level of one sentence each. Why the proof is not hiding, and what would have to change for it to be. Why "formal verification" is the wrong phrase here and what the digest gate gives instead. The phase split, and why host witness generation is the ceiling (issue #2).

11 · Extension slots

## Open questions to fill in later sessions
Each block below is a placeholder with the file to read. When a later conversation answers one, replace the slot body with the answer and add a line to the version log at the end of the page.LogUp from scratch: what the fraction, the multiplicity and the cancellation are

to read: prover/src/plogup.rs (229 lines), prover/src/logup_run.rs, prover/src/relations.rs
answer: not yet writtenHow the GKR sumcheck is linked back to the committed columns

to read: prover/src/gkr_key_tile.rs (2,011 lines), prover/src/gkrlink.rs (2,213 lines); what claimed_h is (issue #30)
answer: not yet writtenThe attention gadget's three row axes and the integer softmax

to read: prover/src/gadgets/attention/layout.rs, witness.rs, air.rs; docs/quantization.md in the results repo
answer: not yet writtenCircle STARK specifics: M31, the circle domain, why log blowup 1 forces degree-2 constraints

to read: nitroo/README.md (the four local changes), prover/src/util.rs, the residual_stream docstring on degree
answer: not yet writtenDevice witness generation: which gadgets build columns on the GPU and why the rest are the ceiling

to read: prover/src/device_witness.rs, devpre.rs, devlogup.rs, cudagen.rs; issue #2
answer: not yet writtenExact cell counting and the issue #13 miscount

to read: harness/costmodel/exact_cells.py (1,903 lines), harness/eval/predict/witness_fields.py; the fix text at the end of issue #13
answer: not yet writtenInterview answers drafted from this page

status: empty. Candidate prompts: "walk me through one segment", "why no recursion", "what would you fix first", "where does soundness come from".

Version log
v2 · 7 Oct 2026 paper layout: wide sheet, figures break out to full width, sticky top nav, abstract, numbered figures v1.2 · 7 Oct 2026 section 0: one-screen flow map and segment dependency graph; white ground in light mode v1 · 7 Oct 2026 first pass: flow, transcript, gadgets, gaps, self-check, seven empty slots
Companion page: the Berrang primer covers the person and the research programme; this page covers the machine.
Sources: the two repositories on disk at ~/work/SASH/ (prover commit as of 7 Oct 2026), docs/statement.md, prover/README.md, harness/README.md, the module docstrings of compose.rs, boundary.rs, shaperoot.rs, gkr_key_tile.rs, gkrlink.rs, each gadget's mod.rs, and tools/drivers/lib/sequence-job.sh in the results repository. SASH's research note and ZKP intro post for the roadmap and the "not hiding" statement.

---

# Part 3. The "Decode and Prove" page: every step, what the model does and how it is proved

## Model constants (Llama-3.1-8B, from its config)

hidden size 4,096; 32 layers; 32 query heads and 8 key/value heads of 128 channels (grouped-query attention, four query heads per key/value head); MLP width 14,336; vocabulary 128,256; RoPE theta 500,000 with Llama 3 frequency scaling; RMSNorm epsilon 1e-5; no projection bias. Weights per layer: q 16.8M, k 4.2M, v 4.2M, o 16.8M, gate 58.7M, up 58.7M, down 58.7M, total 218M; embedding and lm_head 525M each; about 8.03B in all.

## The 18 step cards

Each card: what the model does (as a black box), input to output, how the prover proves it, and what fails if the prover lies there.

### Step 0: Prompt (model)

**What the model does.** Text arrives. The model does nothing with characters; nothing has run yet.

**In to out.** characters → (nothing yet)

**How it is proved.**
1. Nothing is committed. The text never enters any table.
2. The tokeniser and the chat template run outside the statement; the gap table in the results repo lists this row as unclosed.

**If the prover lies here.** Nothing. A proof here speaks only about ids, so a lie about the text is undetectable by design.

### Step 1: Tokenise (model)

**What the model does.** A fixed dictionary of 128,256 pieces turns the text into a list of integers, with a start marker (128000) first.

**In to out.** string → N ids in 0 … 128,255

**How it is proved.**
1. The ids are the statement's public input. Every layer-0 segment commits them as the column tok_in in the base trace (tree 2), whose root is hashed before any challenge is drawn.
2. The verifier receives the same ids on its own command line (--prompt) and compares them against the committed column of every block's layer-0 segment.
3. A generated position's id is compared against the argmax a head segment proved for the position before it.

**If the prover lies here.** Swapping an id after the fact changes tree 2's root, so every challenge derived from it changes and the proof no longer replays.

### Step 2: Embed (model)

**What the model does.** Each id selects one row of a 128,256 × 4,096 table. The N rows form the residual stream, N × 4,096 bf16 values.

**In to out.** N ids → N × 4,096 bf16

**How it is proved.**
1. The table E is preprocessed into the model tree (tree 1): 525 million cells the publisher committed once.
2. Use side: one row per (token, channel block) commits the id and that block's channels as (sm, ef) pairs. Table side: one row per (vocabulary entry, channel block) with a committed multiplicity column.
3. A LogUp lookup argument proves the use rows are a sub-multiset of the table: Σ_uses 1/(z − combine(row)) must equal Σ_table mult/(z − combine(row)) for a random z drawn after both sides are committed.
4. The use side also publishes a Horner fold over the stream values and one over the ids; the stream fold must equal the layer's stream-in claim, so the looked-up row is the row the layer consumed.

**If the prover lies here.** A wrong row makes the two LogUp sums differ for every z but a vanishing fraction; a right row wired to a different stream makes the Horner folds differ.

### Step 3: Norm 1 (model)

**What the model does.** RMSNorm: mean of squares, add epsilon, reciprocal square root, scale by a learned gain. Same shape in and out.

**In to out.** N × 4,096 bf16 → N × 4,096 bf16

**How it is proved.**
1. A bf16 value is two field cells (signed significand, exponent), so every constraint stays degree 2 and a blowup of 2 suffices.
2. The square and the balanced tree sum are the bf16 multiply and add gadgets. An add decomposes the exact sum as mag = M2·ph + r and looks up NORM(M2, ph, st) and FRAC(ph, r, st) in preprocessed tables.
3. rsqrt is a unary lookup: one preprocessed table of all 65,536 bf16 inputs with their correctly rounded outputs.
4. Component gn1 publishes the reduction's level-2 roots and gn1b consumes them; the verifier checks gn1.roots == gn1b.in as an equality of Horner claims under the binding challenge.

**If the prover lies here.** A norm over anything but the committed residual changes the input claim; an incorrectly rounded value has no row in NORM.

### Step 4: Requantise (model)

**What the model does.** One scale per token (max magnitude over 127), then every value divided by it and rounded to an int8.

**In to out.** N × 4,096 bf16 → N × 4,096 int8 + N scales

**How it is proved.**
1. Committed per token: the max's magnitude pattern pm, a selector bit per element, the scale, the int8 values.
2. pm − pat_i is range-checked in [0, 2^15) for every element; the selector is boolean (s² = s), s·(pm − pat) = 0, and a running sum of selectors closes to 1, so pm is an attained value.
3. (pm, s_x) is one lookup into the preprocessed scale table, which is bf16_ceil(v / 127) row by row.
4. For q ≠ 0, one lookup into a division table keyed by the exponent difference proves q = round(x / s); for q = 0 a pattern comparison against s/2 is one range lookup. A (q, nz) pair table makes exactly one of the two apply.
5. Three Horner accumulators close to published claims: the input fold (must equal the producer's output claim), the output fold (must equal the Freivalds fold over the same int8 values) and the scale fold.

**If the prover lies here.** An integer that is not the rounding of the producer's value has no division-table row; a different producer gives a different input fold.

### Step 5: q, k, v matmul (model)

**What the model does.** Three integer matrix multiplies: 4,096 → 4,096 for q, 4,096 → 1,024 for k and v. Exact int32 sums.

**In to out.** N × 4,096 int8 → q N × 4,096, k and v N × 1,024 (int32)

**How it is proved.**
1. Weights are preprocessed in the model tree; the int8 activations and the accumulators are committed. The accumulators are committed once and read by both this gadget and the dequant gadget.
2. After r, s, rv are drawn: per input channel k the gadget folds v = Σ_t s^t·qx[k, t] and, per matmul, u_m = Σ_i rv^i·W_m[i, k], then accumulates acc_m += u_m·v down the rows. Each step is one degree-2 constraint with a running Horner column.
3. The dequant side folds the same committed accumulators the other way: h_m = Σ_t,i s^t rv^i·acc[t, i].
4. The verifier requires acc_m == h_m for every matmul. That equality is rᵀ·(W·X) == (rᵀ·W)·X at a random r: Freivalds' check, one pass over the weights instead of one check per output cell.
5. Every int8 activation is also range-checked by a lookup into the 8-bit range table.

**If the prover lies here.** If any accumulator cell is wrong, the two folds agree only when the random point hits a root of a nonzero polynomial over QM31: roughly 1 in 2^124.

### Step 6: Dequantise (model)

**What the model does.** Multiply each accumulator by the token scale and the weight scale and round to bf16, as a chain of three roundings.

**In to out.** int32 accumulators → bf16

**How it is proved.**
1. |acc| = M2·ph + r with M2 in [256, 512) and ph = 2^k. The decomposition is injective below 2^kmax+9 < p, so acc + p has no valid (M2, ph, r): the field cannot be used to wrap.
2. One arity-6 lookup NORM(M2, ph, st) → (m7, ef, nz) does the normalisation, the rounding and the bf16 encoding; FRAC(ph, r, st) proves r < ph and the sticky bit in one lookup.
3. Each of the three chain steps is one such rounding; a power-of-two scale collapses the chain to one.
4. The gadget publishes an output claim, a Horner fold of its bf16 outputs under the binding challenge; the consumer publishes its own fold over what it read; the verifier compares the two.

**If the prover lies here.** A value that is not the correctly rounded result has no NORM row; a consumer that read different values produces a different fold.

### Step 7: RoPE + quantise (model)

**What the model does.** Rotate pairs of channels of q and k by position-dependent angles, then round q, k, v to 12-, 11- and 8-bit integers with fixed scales.

**In to out.** bf16 q, k, v → integer q, k, v

**How it is proved.**
1. cos and sign-folded sin for every absolute position block·512 + t are preprocessed in the shape tree, so the shape root depends on the block; pos0 is written into the statement and checked against it.
2. The rotation is two residual-stream programs per side (a multiply and an add), the same bf16 gadgets as the norm.
3. The quantise component is the requant gadget with a preprocessed per-slot power-of-two scale instead of a committed per-token one; its division and (q, nz) tables are sized by that side's bit width.
4. Bound on the way in by a Horner comparison against the q and k dequant outputs, and on the way out against the key tiles' own committed Q, K, V columns. Rows padded for an odd head count must be zero, or the weighted sum changes.

**If the prover lies here.** Key-tile values that are not the rotated, quantised dequant outputs fail the out-side comparison.

### Step 8: Attention (model)

**What the model does.** Integer scores q·kᵀ over the keys so far, causal mask, subtract the row max, an exp lookup gives 9-bit numerators, sum them for the denominator.

**In to out.** q, k → per head, N × N numerators and N denominators

**How it is proved.**
1. Per key tile (a group of heads over a slice of the keys) the prover commits qq, qk, the score accumulators, the shift d = max − S, the numerators n and the sums Z. The causal mask and the marker for real key rows come from the shape tree, which the verifier rebuilds, not from the prover.
2. Every (shifted score → numerator) pair is a LogUp lookup into the exp table in the shape tree; range lookups bound d and n.
3. Q·Kᵀ and A·V are exact integer identities inside the AIR. Per key tile the verifier checks r_sum·am_b − hs_b == chan_b (the scores) and sn_b == az_b (the denominator).
4. The LogUp running sums for these lookups are not committed as columns. A GKR sumcheck proves the fractional sums, and the link module ties the sumcheck's final claims to the committed columns with one multilinear-evaluation IOP per distinct height. That is why the interaction tree is 5,600 columns instead of 93,184 at long context.

**If the prover lies here.** A numerator not in the table, a masked key that leaks in, or a denominator that is not the sum of its numerators breaks a lookup or an identity.

### Step 9: Attention out (model)

**What the model does.** Weighted sum of values per head, then one rounding to a 12-bit integer per element.

**In to out.** numerators × v → N × 4,096 (12-bit ints)

**How it is proved.**
1. One row per (head, token, channel chunk) commits acc = A·V, denp = Z·2^max(−e,0), the quotient, the remainder and the 12-bit result; num = 2^max(e,0) and a selector are preprocessed per slot.
2. The rounding identity is stated over the integers inside a 31-bit window pinned by --ao-rem-bits; denp is range-checked on its own so the identity cannot wrap modulo p.
3. Two Horner accumulators reproduce what the key tiles' identities need: Σ_b rv^hd·off_b·av_b == h_ao and Σ_b r^C·off_b·az_b == dz_ao.
4. Because this component commits the rounded output and pins it by the exact-rounding identity, it is also the o matmul's input seam: no second requant gadget is needed.

**If the prover lies here.** A rounding by a denominator nothing pinned was the historical hole; the range check on denp is what closed it.

### Step 10: o + residual (model)

**What the model does.** One more matrix multiply (4,096 → 4,096), then add the result to the residual stream.

**In to out.** N × 4,096 → N × 4,096

**How it is proved.**
1. o is one more Freivalds group and one more dequant, as in steps 5 and 6.
2. Component gn1 proves norm 1's first tree levels and this residual add on the same rows, so the stream is committed once and read by both.
3. Two equalities of Horner claims: the o dequant's output claim equals the add's input claim (edge 6), and gn1's xmid equals gn2's input (edge 7).

**If the prover lies here.** Adding any vector other than the dequant's output changes the input claim the dequant published.

### Step 11: MLP + residual (model)

**What the model does.** Norm, requantise, two matmuls 4,096 → 14,336, gate times up, requantise, one matmul 14,336 → 4,096, add to the stream.

**In to out.** N × 4,096 → N × 4,096

**How it is proved.**
1. Two more requant seams (into gate/up, into down), exactly as step 4; gate and up share one Freivalds input fold.
2. silu is a unary table lookup; the SwiGLU product is the bf16 multiply gadget and reads the gate and up dequant claims (edge 9).
3. gn2 proves norm 2's tree levels and the second add; gn2.roots == gn2b.in; down's dequant claim equals the add's input claim (edge 11).

**If the prover lies here.** The same two failure shapes as before: no table row for a wrong rounding, mismatched Horner folds for wrong wiring.

### Step 12: Segment proof (prover)

**What the model does.** The layer's output goes to the next layer and K, V go to the cache. For the prover, one layer over one block of 512 positions is a segment, and its proof is made now.

**In to out.** one layer × one block → statement, claims, proof (≈ 65 MiB)

**How it is proved.**
1. Commit tree 0 (shape: selectors, mask, tables, angles; the verifier rebuilds it), tree 1 (model: weights and scales; cached per layer) and tree 2 (base trace). Each root is mixed into a Blake2s channel in that order.
2. Draw from the channel: the relation elements z and α for every lookup table, then the Horner challenges r, s, rv and the binding pair w, λ. Nothing committed so far can depend on them.
3. Build every LogUp fraction num/(z − combine) and the running sums; run the five GKR sumchecks for the lookup families that use them; commit the interaction tree (tree 3).
4. Commit the boundary trees: residual in, residual out, K/V out. Each is bound to its base column by a plain equality constraint checked at the out-of-domain point, which is why they may be committed after the interaction tree.
5. stwo: draw the OODS point, evaluate the composition polynomial (generated CUDA kernels), FRI with blowup 2 and 100 queries, 100 conjectured bits. Serialise Fixed, Claims, Proof.

**If the prover lies here.** Any changed cell changes a root, hence every later challenge, hence the out-of-domain evaluations: the proof fails to verify.

### Step 13: Layers 1 to 31 (model)

**What the model does.** The same block of operations 31 more times with different weights.

**In to out.** N × 4,096 → N × 4,096, 31 times

**How it is proved.**
1. Each layer is its own segment with its own base trace; the shape tree is cached per (layer, shape) on the device and the model tree per layer.
2. Afterwards boundary-grid compares the residual-out root of segment L_k with the residual-in root of L_k+1: first the integer facts that make two roots comparable (block length, layout, blowup, tree sizes), then one root equality.
3. No recursion anywhere: a root is 32 bytes and the comparison is constant time.

**If the prover lies here.** A layer fed a residual nobody produced has an in-root that matches no out-root.

### Step 14: Head (model)

**What the model does.** Final norm, then one matrix multiply 4,096 → 128,256: one score per vocabulary piece.

**In to out.** 4,096 → 128,256 logits

**How it is proved.**
1. The head is its own segment. lm_head sits in the model tree (about 570 million preprocessed cells); the head input is one requant seam from the final norm; the power-of-two dequant is a single rounding.
2. Edges 3 to 11 and 14 are absent: no attention and no MLP of its own. The residual it consumed is committed as the in side of the last layer link.
3. It is proved over the last prompt block and over the generated block, so every generated id has a proved argmax for the position before it.

**If the prover lies here.** Logits that are not W·h fail the Freivalds equality.

### Step 15: Argmax (model)

**What the model does.** Take the highest score; on a tie, the lowest index.

**In to out.** 128,256 logits → one id

**How it is proved.**
1. Committed: the maximum's pattern pm, a boolean indicator b_i = [i < tok] (b² = b) and the token.
2. A range lookup on pm − k_i − b_i ≥ 0 for every vocabulary entry: strictly below the max before tok, at most the max from tok on.
3. Monotonicity b_i·(1 − b_i−1) = 0 is one degree-2 constraint; the running sum of b closes against the committed token, which is the binding itself.
4. The selector b_i − b_i+1 is derived, is 1 exactly at tok, and s·(pm − k_i) = 0 pins pm to the value attained there. A Horner fold over the logits closes to the dequant's claim, and a fold over the ids closes to the token claim.

**If the prover lies here.** A token that is not the first maximum: either an earlier entry is not strictly below pm, or pm is not attained at tok. The lax flag admits either co-maximal token and marks the run a control.

### Step 16: Next tokens (model)

**What the model does.** Append the id and run all layers for the new position only; earlier keys and values come from the cache.

**In to out.** N ids → N + 1 ids per pass

**How it is proved.**
1. A generated position is one more row in the same 512-position block; the same segments cover it. Nothing is proved per token.
2. boundary-grid --verify --prompt checks that the id committed at position p equals the argmax the head segment proved at p − 1.
3. Keys and values of earlier blocks enter as a committed boundary root (edge 14): the consumer's context must be the producer's plus one block, then the roots must match.

**If the prover lies here.** An id that is not the previous position's proved argmax fails the chain.

### Step 17: Verify (prover)

**What the model does.** The decode is finished. A verifier on a CPU, holding no weights, checks everything.

**In to out.** 290 proofs + ids + model root + calibration → accept or reject

**How it is proved.**
1. Parse Fixed, Claims and Proof; reject if the claim shapes do not match the plan or the security parameters drifted.
2. Replay the transcript: mix the roots in order, re-draw every challenge, verify the GKR sumchecks, run stwo's verifier (out-of-domain sampling and FRI).
3. Check the LogUp sums cancel, every Freivalds equality, the attention and denominator identities, and every binding equality between gadgets.
4. Derive the shape root from the statement's parameters and the published calibration and compare it with the declared root; compare the model root with the published manifest.
5. Then the grid: 281 layer links, 256 token links, every id chained to the prompt or to a proved argmax.

**If the prover lies here.** Each check is one field of the verdict; accept requires all of them, and a single changed byte in a proof body is refused.

## The animation's 20 steps on the prompt "The capital of France is"

For each step: the left pane (the model), then the right pane (the prover): gadget card, visual text, explanation, which trees are in which state, and which of the 16 edges are bound so far.

### Animation step 1 (stage 0: Prompt)

**Model: The user types a prompt**

“The capital of France is”

characters24

what the model will seenot this text. A list of integers.

Nothing has been computed. The model never reads characters; the first thing that happens is a tokeniser turning this string into ids.

**Prover: Not involved yet**

- gadget: none; the prover has no role at this step

statement so far:  (nothing)

The tokeniser and any chat template run outside every proof.
The verifier will never see this text, only the ids.

This is the first row of the gap table in docs/statement-gap.md: both ends of a request, the text in and the text out, are outside the statement. A proof will say "these ids produce those ids under this model", nothing about words.

- trees (shape, model, trace, interaction, boundary): idle, idle, idle, idle, idle
- edges bound so far: none

### Animation step 2 (stage 1: Tokenise)

**Model: Tokenise: 6 ids**

<|begin_of_text|>128000
The791
 capital6864
 of315
 France9822
 is374

vocabulary128,256 entries, byte-pair encoding

first id128000 is the begin-of-text marker, added by the tokeniser

Each piece becomes one integer. From here on the model works only on these 6 integers and their order. The prompt occupies positions 0 to 5.

**Prover: The ids become the public input**

- gadget: the statement's public input (prover/src/compose.rs · Fixed)
- commits: layer 0 will commit tok_in (the ids) in the base trace, before any challenge is drawn
- checks: boundary-grid --verify --prompt compares every committed prompt id against this list

public input = [128000, 791, 6864, 315, 9822, 374]

verifier is handed:  these ids · the model root · the per-layer calibration
verifier is NOT handed: weights, activations, the text

Everything the verifier will ever learn hangs off these integers. The prover cannot change them later: they are committed in a tree whose root is hashed into the transcript before any randomness exists.

- trees (shape, model, trace, interaction, boundary): idle, idle, building, idle, idle
- edges bound so far: none
- log: [in] public input: 6 prompt ids

### Animation step 3 (stage 2: Embed)

**Model: Embedding lookup: one row of E per id**

E
128,256 × 4,096bf16 table, 525M entries
row 374 →
x[5]-0.0030.0010.0000.004-0.005-0.003-0.0010.004… 4,088 more · bf16

residual stream6 positions × 4,096 channels. This vector is what every layer will read and add to.

The id selects row 374 of a 128,256 × 4,096 table. No arithmetic yet, just a lookup. The result for the last token,  is, is shown.

**Prover: Edge 15: the embedding gadget binds the row to the id**

- gadget: embed (prover/src/gadgets/embed/)
- edge: 15 · embedding row into the first segment's residual stream
- commits: the ids, and the residual-stream input as (sign·significand, exponent) pairs
- pre: the whole embedding matrix E, V × d = 525M cells, in the model tree (tree 1)
- checks: a LogUp scan over the entire table proves bin[t][c] == E[tok[t]][c] for every position and channel; the Horner claim over the stream must equal the layer's stream-in claim
- cost: preprocessed V·d; fresh ≈ 5·V·d / pe cells per block (one multiplicity cell and one LogUp column per table row)

for every position t, channel c:
    bin[t][c] == E[tok[t]][c]

why a scan of all 128,256 rows?  selecting one row by a committed index
with no positional opening costs one pass over the table; a cheaper digest
would have to be challenge-dependent, and a challenge-dependent value
cannot be committed before the challenge that binds it.

Only a layer-0 segment carries this gadget. Without it the first segment's residual input would be an unchecked value the prover could choose; the record used to call that "bin is the embedding's output, unchecked".

- trees (shape, model, trace, interaction, boundary): building, building, building, idle, idle
- edges bound so far: 15
- log: [L0] embed: tok_in committed; E in tree 1 | [v] edge 15 bound (embedding row)

### Animation step 4 (stage 3: norm 1)

**Model: Layer 0 · RMSNorm 1**

ms = mean( bf16(x_i²) )      balanced tree of bf16 adds over 4,096 channels
r  = rsqrt( ms + 1e-5 )     one bf16 unary op
h  = bf16( bf16(x·r) · w )  w is the learned norm gain

rms of x at layer 0 input0.006

channels4,096

Every value between ops is a bf16 pattern, so each op is a correctly rounded bf16 op. The reduction over 4,096 squares is a balanced binary tree, which is what makes it provable as a chain of small adds.

**Prover: Edge 1: the norm reads the committed residual, not a copy**

- gadget: residual_stream (gn1, gn1b) (prover/src/gadgets/residual_stream/)
- edge: 1 · residual stream into the first norm's reduction
- commits: the residual stream as (sm, ef) pairs; every intermediate bf16 of the tree sum; the level-2 roots
- pre: bf16 tables: NORM, FRAC, POW, a 2^16-row unary table for rsqrt, a multiply table
- checks: gn1.roots == gn1b.in as an equality of Horner claims; the mean of squares each norm took the reciprocal square root of is the published answer
- cost: one bf16 add ≈ 12 to 15 cells; d adds per norm, two norms per layer

bf16 value = sm · 2^(ef − 134)      sm ∈ {0} ∪ ±[128, 256), ef ∈ [1, 255)

add:  acc = sm_a·pa + sm_b·pb   (pa, pb from a POW lookup)
      mag = M2·ph + r  →  NORM(M2, ph, st) → (m7, ef, nz)   FRAC(ph, r, st)

kept at degree 2 so blowup 2 suffices — that is why values are (sm, ef) pairs.

A unary bf16 op is exactly a 65,536-row lookup table, so rsqrt costs one LogUp lookup per value. The square, the tree sum and the two multiplies are the add and multiply gadgets. Unbound, the prover could normalise any vector and call it the norm of the residual.

- trees (shape, model, trace, interaction, boundary): building, building, building, idle, idle
- edges bound so far: 1, 15
- log: [L0] norm1: tree-sum roots published | [v] edge 1 bound

### Animation step 5 (stage 4: requantise)

**Model: Requantise h to int8 for the matmul**

s_x = bf16_ceil( max_i |h_i| / 127 )   one scale per token, rounded UP so nothing clamps
q_i = round_half_away( h_i / s_x )     |q_i| ≤ 127
h-0.0170.0200.0150.009-0.320-0.01000.002… bf16
÷ s_x = 0.03173828125 (max |h| = 4.0312), round
q-1100-10000… int8, 4,096 of them

The matmul that follows multiplies integers. These int8 values for position 5 are the harness's rule applied to the real bf16 norm output. One scale per token is what "dynamic int8 per token" means.

**Prover: Edge 2: the seam proves q is the requantisation of h**

- gadget: requant (prover/src/gadgets/requant/)
- edge: 2 · first norm's output into the q, k, v matmul inputs
- commits: the max's magnitude pattern pm per token, a selector bit per element, the scale, the int8 values
- pre: the (pm → bf16_ceil(pm/127)) scale table; a division table keyed by exponent difference; the (q, nz) pair table; the 15-bit range
- checks: pm − pat_i in [0, 2^15) for every element and sel_i·(pm − pat_i) = 0 with Σ sel_i = 1 pins the max; one (pm, scale) lookup pins the scale; one division lookup per nonzero q, one range lookup per zero
- cost: model_constants.requant_cells_per_value, per distinct matmul input

max argument:   pm − pat_i ≥ 0  ∀i       sel_i (pm − pat_i) = 0,   Σ sel_i = 1
scale:          (pm, s_x) ∈ SCALE_TABLE          the table IS bf16_ceil(v / 127)
requant, q≠0:   (tt, m7, q) ∈ DIV_TABLE          tt = exponent difference
requant, q=0:   |x| < s_x / 2  as a pattern comparison, one range lookup

Why it matters: the Freivalds check multiplies exactly these integers. If this seam were unbound, the prover could feed the matmul any activation and the matmul's proof would faithfully multiply the wrong input. The --unsound-skip-residual-stream flag unbinds it and marks the run a control.

- trees (shape, model, trace, interaction, boundary): building, building, building, idle, idle
- edges bound so far: 1, 2, 15
- log: [L0] requant: s_x = 0.03173828125 for position 5 | [v] edge 2 bound

### Animation step 6 (stage 5: q k v matmul)

**Model: q, k, v projections: three int8 matmuls**

W_q
4,096 × 4,09616.8M int8
W_k
4,096 × 1,0244.2M int8
W_v
4,096 × 1,0244.2M int8

acc[t, j] = Σ_i q[t, i] · w[j, i]      exact int32, no rounding
weights: int8 per output channel, s_w[j] = max_i |W[j,i]| / 127
W_q[0]0.005-0.029-0.006-0.018-0.0030.026-0.001-0.002… bf16 weights, channel 0
int811-65-14-40-759-2-5… s_w = 0.00045

heads32 query heads, 8 key/value heads (grouped-query attention), 128 channels each

The same int8 input feeds all three. The accumulation is exact, so a wrong accumulator is a wrong integer, not a rounding question. Seven matmuls per layer: q, k, v, o, gate, up, down, 218M weights in all.

**Prover: Edge 12: Freivalds, the trick that makes 8B weights affordable**

- gadget: freivalds (prover/src/gadgets/freivalds/)
- edge: 12 · each matmul's input times the pinned weights into its accumulator
- commits: the int8 activations qx (four to a word) and the accumulators acc (shared with the dequant gadget, committed once)
- pre: the int8 weights of this layer, in the model tree; their root is the publisher's commitment
- checks: after r, s, rv are drawn: u_m = Σ_i rv^i W_m[i,k], v = Σ_t s^t qx[k,t], acc_m = Σ_k u_m v, and the verifier requires acc_m == h_m where h_m is the dequant's own Horner fold of the committed accumulators
- cost: a fixed number of cells per weight (12 QM31 accumulator cells per row of p weights); linear in the parameter count

claim:  Y = W · X                 (per layer, per matmul, mod p)
test:   rᵀ Y  ==  (rᵀ W) · X        r drawn AFTER X, Y, W are committed

left side:  Horner fold of the committed accumulators (dequant already holds them)
right side: computed in this gadget from preprocessed W and committed X

a wrong Y survives only if r happens to hit a root of (Y − W X): about 1 in |QM31| ≈ 2^124

Checking Y = W·X cell by cell for 8 billion weights is hopeless. Checking one random linear combination costs one pass over the weights. The weights never leave the model tree; the verifier only compares the tree's root with the manifest.

- trees (shape, model, trace, interaction, boundary): building, committed, building, idle, idle
- edges bound so far: 1, 2, 12, 15
- log: [L0] q k v: 25.2M weights read from tree 1 | [v] edge 12 (Freivalds) will be checked once r, s, rv are drawn

### Animation step 7 (stage 6: dequantise)

**Model: Dequantise the accumulators back to bf16**

y = bf16( bf16( bf16(acc · s_x) · s_w ) )     three correctly rounded steps, round half to even

example scales for this position:  s_x = 0.03173828125   s_w[0] = 0.00045

why a chaina general bf16 scale cannot be folded into one rounding; a power-of-two scale can (the output head uses that)

The integer accumulator becomes a bf16 activation again. Each rounding is a specific, deterministic operation, so the proof can state exactly which bf16 pattern comes out.

**Prover: The dequant gadget: one lookup normalises, rounds and encodes**

- gadget: dequant (prover/src/gadgets/dequant/)
- edge: publishes the output claims that edges 6, 9 and 11 compare
- commits: acc as two limbs, M2, ph, r, the sticky bit, and the output (m7, ef, nz)
- pre: NORM(M2, ph, st) → (m7, ef, nz) and FRAC(ph, r, st): 2^(kmax+1) preprocessed rows
- checks: |acc| = M2·ph + r with M2 in [256, 512) and r < ph in one arity-6 lookup; the output claim of the consumer (a residual add, the SwiGLU) equals this gadget's
- cost: dequant_chain_cells_per_acc on the seven layer matmuls; one cell less for pow2 scales on the head

|acc| = M2 · 2^k + r        M2 ∈ [256, 512),  0 ≤ r < 2^k
NORM(M2, ph, st)  →  (m7, ef, nz)      the correctly rounded bf16 of |acc|
FRAC(ph, r, st)                        r < ph  and  st = [r ≠ 0]  in one lookup

the decomposition is injective below 2^(kmax+9) < p, so acc + p has no valid (M2, ph, r)

The accumulators are committed once and read by two gadgets: the dequant rounds them, the Freivalds check folds them. Nothing is committed twice, and the same cells are what both identities are about.

- trees (shape, model, trace, interaction, boundary): building, committed, building, idle, idle
- edges bound so far: 1, 2, 12, 15
- log: [L0] dequant: output claims published for q, k, v

### Animation step 8 (stage 7: RoPE + quantise)

**Model: RoPE, then integer q, k, v for the attention**

for channel pair (i, i+64) of each head, angle = pos · θ_i,   θ_i = 500000^(−2i/128), low frequencies stretched by Llama 3's rope scaling
  q' = bf16( q·cos ) + bf16( q_rot·sin )          same for k;  v is not rotated

position of this token = 5:   θ_0 = 1 → angle 5 rad,   θ_63 ≈ 2.46e-6 → angle 1.23e-5 rad

then:  qq = round(q' / s_q)  12-bit, one power-of-two scale per head (calibrated)
       qk = round(k' / s_k)  11-bit, one scale per (layer, head)
       qv = round(v  / s_v)   int8, one scale per (layer, head, channel)

Rotation encodes the absolute position into q and k so the dot product depends on relative distance. The scales for k and v are fixed offline from a calibration slice, which is what lets the softmax that follows be an integer statement.

**Prover: Edge 3: rotation and quantise components, with a block-dependent shape tree**

- gadget: rope (two residual_stream programs + QuantEval) (prover/src/gadgets/rope/)
- edge: 3 · q, k, v outputs into the attention block
- commits: the rotated bf16 values and the quantised integers per (token, head)
- pre: cos and sign-folded sin for every absolute position block·512 + t, in the shape tree; per-slot power-of-two scales
- checks: Horner comparison on the way in against the q and k dequant outputs, and on the way out against the key tiles' own committed Q, K, V columns; a padded row (odd head counts) must be zero or the comparison fails
- cost: two bf16 ops per rotated value; 37.5 % padding when the head count has an odd factor (Qwen2.5-14B), none for Llama's 32

the shape tree is a function of (params, calibration, block index)
because rope(pos) reads block · S + t.  pos0 is written into the statement and
verify_composed checks it against Fixed.block.

no site for a projection bias exists:  dequant states acc · s_x · s_w and nothing else,
so Qwen2.5's q/k/v biases make edge 3 refuse every layer (issue #174).

Before this component existed the seam between the projections and the attention was a hole: the key tiles' committed Q, K, V were not the dequant outputs. This is the stream that closed it.

- trees (shape, model, trace, interaction, boundary): building, committed, building, idle, idle
- edges bound so far: 1, 2, 3, 12, 15
- log: [L0] rope: angles for position 5 come from the shape tree | [v] edge 3 bound

### Animation step 9 (stage 8: attention)

**Model: Attention scores: an integer softmax**

S = qq · qkᵀ                 exact integers, one row per query, one column per key (6 keys now)
causal mask: key j > query t is hidden
m = max_j S[t, j]            d = m − S ≥ 0
n = round( 511 · exp(−d · s_q s_k / √128) )    9-bit numerator, ONE lookup table keyed by the bf16 input
Z = Σ_j n[t, j]              exact integer denominator
what the last position attends to · layer 0 head 0 (left) and layer 15 head 0 (right), the bf16 model's softmax, for intuition<|begin_of_text|> :  0.463
The :  0.219
 of :  0.160
 capital :  0.086
 France :  0.046
 is :  0.026

<|begin_of_text|> :  0.289
 of :  0.275
 is :  0.167
 capital :  0.129
 France :  0.110
The :  0.030

Subtracting the row max first keeps every exponent argument non-positive, so the table only needs exp on [−big, 0]. Each probability is an integer n over an integer Z; no division happens here.

**Prover: Edge 4: the attention component, the one that grows with context**

- gadget: attention (key tiles: chan, key, row evaluators) (prover/src/gadgets/attention/ + gkr_key_tile.rs)
- edge: 4 · scores and values into the attention output: not a seam, the component itself, no skip exists
- commits: qq, qk, the score accumulators, the shift d, the numerators n, the sums Z, per key tile (a group of heads over a slice of the C keys)
- pre: the exp table (up to 2^22 rows under --tight-table), the causal mask, the marker for real key-grid rows, range tables: all in the shape tree
- checks: per key tile b: r_sum·am_b − hs_b == chan_b (Q·Kᵀ) and sn_b == az_b (denominator); every exp lookup lands in the table; mask and marker are derived from public parameters, not chosen
- cost: cells per (head, key, token): this is why a position costs ~79M cells at C = 4,096 and ~105M at C = 16,384

lookups are LogUp: Σ_uses 1/(z − key)  must cancel  Σ_table mult/(z − row)

the running sums for these lookups are NOT committed as columns here:
five GKR sumchecks prove them instead (--gkr-key-tiles and friends).
at C = 16,384 that takes the interaction tree from 93,184 columns to 5,600.
gkrlink.rs then ties the sumcheck's final claims back to the committed
columns with one MLE-evaluation IOP per distinct height.

The mask invariant the component rests on, "the mask is clear on every row of padding", holds because the verifier rebuilds the shape tree itself and compares roots. A verifier that read the root off the statement would accept any shape the prover named.

- trees (shape, model, trace, interaction, boundary): building, committed, building, idle, idle
- edges bound so far: 1, 2, 3, 4, 12, 15
- log: [L0] attention over 6 keys; exp lookups collected for GKR | [v] edge 4 is the component itself

### Animation step 10 (stage 9: attention out)

**Model: A·V, then one rounding to a 12-bit integer**

O = n · qv                       exact integers (numerators times int8 values)
out = round( O · s_v / (Z · s_o) )   the softmax division, the value scale and the
                                    next requantise, folded into ONE rounding
s_o = power of two per token, chosen so |out| ≤ 2047  (12 bits, not 8)

why 12 bitsthe o projection consumes a wider value and one rounding is saved; perplexity cost of the whole configuration: +6.96 % vs fp32

shape32 heads × 128 = 4,096 values per token

The harness deletes the bf16 waypoint, the reciprocal lookup and the requantise that a textbook softmax would need. The division is exact because O and Z are integers and the rounding happens once, at the end.

**Prover: Edge 5: the attention-output fold is itself the o matmul's seam**

- gadget: attn_out (AttnOutEval) (prover/src/gadgets/attn_out/)
- edge: 5 · attention output into the o matmul input
- commits: acc (the A·V outputs), denp = Z · 2^max(−e,0), the quotient and remainder of the rounding, the 12-bit result
- pre: num = 2^max(e,0) and the pj selector, per slot; the exponent window pinned by --ao-rem-bits
- checks: the rounding identity as an integer identity inside a 31-bit window; two Horner claims the key tiles' identities need: Σ_b rv^(hd·off_b)·av_b == h_ao and Σ_b r^(C·off_b)·az_b == dz_ao
- cost: attnout_int8_cells_per_acc; 9 cells against 15 + 4 + 15 for the unfolded form

the fold's window:  1 + lo + hi + e_hi ≤ 31   and   q_bits + rem_bits ≤ 31

--ao-rem-bits is ONE number for the whole loop (the model-wide worst case),
so the shape table checks every layer against it before any proof is made.
the recorded 4,096-token run sits at 11 + 20 = 31 of 31: it composes and admits nothing wider.

issue #13: a counted registration used each dump's own ao_rem_bits instead of the shared pin
and came out 5 cells per table row short (159,989,760 cells).

Because this component commits the rounded int output and pins it by the exact-rounding identity, the o matmul needs no second requantise gadget: a claim on this component is its input seam.

- trees (shape, model, trace, interaction, boundary): building, committed, building, idle, idle
- edges bound so far: 1, 2, 3, 4, 5, 12, 15
- log: [L0] attn_out: h_ao and dz_ao published | [v] edge 5 bound

### Animation step 11 (stage 10: o + residual)

**Model: o projection, then the first residual add**

W_o
4,096 × 4,09616.8M int8

o_out = bf16-chain( W_o · out )        Freivalds + dequant again
x_mid = bf16( x + o_out )              the residual stream grows by the attention's contribution

The residual stream is the layer's memory: every sub-block reads it and adds to it. This add is the first of two per layer.

**Prover: Edges 6 and 7: the add reads the dequant's claim and feeds norm 2**

- gadget: freivalds + dequant + residual_stream (gn1 add) (prover/src/gadgets/residual_stream/)
- edge: 6 · o output into the first residual add; 7 · the add into the second norm's reduction
- commits: x_mid as (sm, ef) pairs on the same rows that hold norm 1's first tree levels
- pre: the bf16 add's POW, NORM, FRAC tables
- checks: the dequant's output claim equals the add's input claim (6); gn1.xmid == gn2.in (7)
- cost: one bf16 add per channel: residual_stream_add_cells_per_op

gn1   xin, o_out  →  norm1's level-1 roots, and xmid
gn1b  those roots  →  norm1's mean of squares
gn2   xmid, d_out  →  norm2's level-1 roots, and xout
gn2b  those roots  →  norm2's mean of squares

three equalities:  gn1.roots == gn1b.in,   gn1.xmid == gn2.in,   gn2.roots == gn2b.in

gn1 proves the reduction's first levels and the residual add on the same row, so the residual stream is committed once and read by both. Unbound, the prover could add any vector to the stream.

- trees (shape, model, trace, interaction, boundary): building, committed, building, idle, idle
- edges bound so far: 1, 2, 3, 4, 5, 6, 7, 12, 15
- log: [L0] o: dequant claim read by the add | [v] edges 6, 7 bound

### Animation step 12 (stage 11: MLP + residual)

**Model: The MLP: norm 2, gate and up, SwiGLU, down, second add**

h2 = RMSNorm(x_mid)  → int8 (new per-token scale)
g  = W_gate · h2,   u = W_up · h2         4,096 → 14,336 each
y  = bf16( silu(g) · u )                  silu is one bf16 unary table
y  → int8 (per-token scale)
d  = W_down · y                           14,336 → 4,096
x  = bf16( x_mid + d )                    layer 0 output
W_gate
14,336 × 4,09658.7M int8
W_up
14,336 × 4,09658.7M int8
W_down
4,096 × 14,33658.7M int8

Three of the seven matmuls and 176M of the layer's 218M weights are here. Gate and up share one int8 input, exactly like q, k, v did.

**Prover: Edges 8 to 11: two more seams, one product, one add**

- gadget: requant · freivalds · dequant · residual_stream (SwiGLU, gn2 add) (prover/src/gadgets/{requant,freivalds,dequant,residual_stream}/)
- edge: 8 · norm 2 → gate/up inputs; 9 · gate/up outputs → SwiGLU; 10 · SwiGLU → down input; 11 · down output → second add
- commits: the second norm, two int8 inputs with their scales, the SwiGLU's bf16 product, x_out
- pre: the silu unary table (2^16 rows), the shared bf16 tables, the gate/up/down weights in tree 1
- checks: two requant seams (8, 10) exactly as edge 2; the SwiGLU reads the gate and up dequant claims (9); the add reads down's (11); gn2.roots == gn2b.in
- cost: one unary table application = one committed bf16 value + one lookup; one multiply; one add per channel

the layer's seven Freivalds groups:
   { q, k, v }   share input h          { gate, up }  share input h2
   { o }         input = attn_out       { down }      input = y

a group of n matmuls shares one accumulator fold and costs (4 + 8n)/(n·p) cells per weight

At this point every seam inside the layer is bound: each matmul multiplies exactly the integers its producer made, and each consumer reads exactly the bf16 its producer rounded. What is left is the two boundaries of the segment.

- trees (shape, model, trace, interaction, boundary): building, committed, building, idle, idle
- edges bound so far: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15
- log: [L0] gate up down: 176M weights read from tree 1 | [v] edges 8, 9, 10, 11 bound

### Animation step 13 (stage 12: Segment proof)

**Model: Layer 0 is done: the residual goes up, K and V go into the cache**

x_out[t]  (4,096 bf16 per position)   →   layer 1's input
K, V for these 6 positions, 8 heads × 128   →   the key/value cache every later position attends over

rms of x after layer 00.013

in the paper's runthis is one block of 512 positions, not 6; a layer over one block is one segment

For the model this is just the next layer. For the prover this is the end of a segment, so now the whole proof for "layer 0 over this block" is made.

**Prover: One segment becomes one STARK: the transcript, in order**

- gadget: compose (generate, then prove_gen_to) + boundary (prover/src/compose.rs · boundary.rs)
- edge: 13 · residual out into the next layer; 14 · K, V out into the next block
- commits: two small trees per axis holding only the boundary values: residual in (tree 3), residual out (tree 4), K/V out
- pre: nothing new
- checks: each boundary column equals the component column by a plain equality constraint (no lookup, no challenge), so the trees can be committed after the interaction tree; boundary-grid compares roots between neighbours
- cost: the whole segment: ~2.1 Gcell/s to commit, ~99 Mcell/s for the loop; proof ≈ 65 MiB

0shape treeselectors, mask, tables, RoPE angles · verifier rebuilds it
1model treeint8 weights, scales, E, lm_head · publisher's root
2base traceevery committed witness column
—challengesr, s, rv, z, α drawn from the roots
GKR5 sumchecksLogUp sums proved, not committed
3interactionwhat remains of the lookup columns
4+boundaryresidual in/out, K/V out · plain equality
STARKOODS + FRI100 queries, blowup 2 · ~65 MiB

Why roots and not a shared challenge: a challenge drawn inside one proof cannot be reused by another, and a challenge known before the values are committed makes "my image equals yours" one linear equation the prover can solve. So the exposed value is a Merkle root.

- trees (shape, model, trace, interaction, boundary): committed, committed, committed, committed, committed
- edges bound so far: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15
- log: [p] segment L0·B0: trees 0,1,2 → challenges → GKR → tree 3 → boundary → STARK | [p] proof serialised: fixed.json, claims.json, proof.json | [v] edges 13, 14 bound by boundary roots

### Animation step 14 (stage 13: Layers 1 – 31)

**Model: Layers 1 to 31: the same seven matmuls with different weights**

rms of the residual stream at position 5, after each layer (real, bf16 model)
embedlayer 15layer 31 · rms 2.176

Each layer reads the stream and adds to it; the magnitude grows down the stack. Each layer has its own 218M weights, its own K/V cache rows, the same arithmetic.

**Prover: 32 segments per block, chained by roots**

- gadget: compose-chunks --plan (prover/src/chunks.rs · precache.rs · shaperoot.rs)
- edge: 13 between every pair of consecutive layers
- commits: each layer's own witness; dropped from host memory as soon as its proof is made
- pre: the shape tree is cached on the device per (layer, shape); the model tree per layer comes from the same cache; the verifier pays about 32 shape-root derivations for 290 segments, not 290
- checks: residual-out root of layer k equals residual-in root of layer k+1, for all 31 pairs, on the verifier side after the run
- cost: c4096 run: 3,683 s of loop for 290 segments on one H100, 1.25 positions/s

segment L0·B0 proved · link L0→L1 pending
segment L1·B0 proved · link L1→L2 pending
segment L2·B0 proved · link L2→L3 pending
segment L3·B0 proved · link L3→L4 pending
segment L4·B0 proved · link L4→L5 pending
segment L5·B0 proved · link L5→L6 pending
segment L6·B0 proved · link L6→L7 pending
segment L7·B0 proved · link L7→L8 pending
segment L8·B0 proved · link L8→L9 pending
segment L9·B0 proved · link L9→L10 pending
segment L10·B0 proved · link L10→L11 pending
segment L11·B0 proved · link L11→L12 pending
segment L12·B0 proved · link L12→L13 pending
segment L13·B0 proved · link L13→L14 pending
segment L14·B0 proved · link L14→L15 pending
segment L15·B0 proved · link L15→L16 pending
segment L16·B0 proved · link L16→L17 pending
segment L17·B0 proved · link L17→L18 pending
segment L18·B0 proved · link L18→L19 pending
segment L19·B0 proved · link L19→L20 pending
segment L20·B0 proved · link L20→L21 pending
segment L21·B0 proved · link L21→L22 pending
segment L22·B0 proved · link L22→L23 pending
segment L23·B0 proved · link L23→L24 pending
segment L24·B0 proved · link L24→L25 pending
segment L25·B0 proved · link L25→L26 pending
segment L26·B0 proved · link L26→L27 pending
segment L27·B0 proved · link L27→L28 pending
segment L28·B0 proved · link L28→L29 pending
segment L29·B0 proved · link L29→L30 pending
segment L30·B0 proved · link L30→L31 pending
segment L31·B0 proved · link L31→L32 (head)

No recursion anywhere. A segment is proved alone, one thread generates the next while this one proves, and the only thing one proof shares with the next is a 32-byte root.

- trees (shape, model, trace, interaction, boundary): committed, committed, committed, committed, committed
- edges bound so far: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15
- log: [p] segments L1 … L31 proved (31 more STARKs) | [v] 31 residual links L_k → L_{k+1} compared

### Animation step 15 (stage 14: Head)

**Model: Final norm, then the output head: 128,256 logits**

lm_head
128,256 × 4,096525M int8, pow2 scales

top-5 logits for position 5 (real) a :  16.00
 Paris :  15.94
 known :  15.06
 home :  14.88
 the :  14.31

One more RMSNorm, then the largest matmul of all: 4,096 → 128,256. The output is one score per vocabulary entry for the next token. The head uses power-of-two scales, so its dequant is a single rounding.

**Prover: The head segment: Freivalds over the largest matrix, no attention**

- gadget: head segment (compose with --synth-head / a head dump) (prover/src/compose.rs · gadgets/freivalds · gadgets/dequant (pow2))
- edge: 1, 2 (final norm and its seam), 12 (lm_head), 13 (the residual it consumed)
- commits: the final norm, the int8 head input, the logits' accumulators
- pre: lm_head, 128,256 × 4,096: about 570M preprocessed cells in the model tree
- checks: the same Freivalds equality over lm_head; edges 3 to 11 and 14 are absent here (no attention, no MLP of its own)
- cost: one head segment per block that emits tokens; the paper run proves it over the last prompt block and the generated block

head segment = { final RMSNorm, requantise seam, lm_head Freivalds, pow2 dequant, argmax }

proved twice in a run:  over the last prompt block (so the FIRST generated id is backed)
                        and over the generated block (so every later id is backed)

issue #9: family_cells has no argmax counter, so 131,727,360 base cells per head segment
are unattributed in the cost breakdown (the proof itself is fine).

The head is its own segment, placed at the layer coordinate after layer 31. Its residual input is committed as the in side of the last layer link, so the chain from embedding to logits has no gap.

- trees (shape, model, trace, interaction, boundary): committed, committed, building, idle, idle
- edges bound so far: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15
- log: [p] head segment: lm_head Freivalds over 525M weights

### Animation step 16 (stage 15: Argmax)

**Model: Greedy decoding: take the argmax**

aid 264 · logit 16.00 · tie with another logit: no
tok = argmax_v logits[v]        torch.argmax returns the FIRST maximal index on a tie

Greedy decoding has no sampling: the token is a deterministic function of the logits. That is what makes it a provable statement; a sampled token would need the whole softmax and a committed seed.

**Prover: Edge 16: the argmax gadget, in its strict form**

- gadget: argmax (prover/src/gadgets/argmax/)
- edge: 16 · logits into the emitted token
- commits: the maximum's pattern pm, a monotone indicator b_i = [i < tok], the emitted token
- pre: range tables
- checks: pm − k_i − b_i ≥ 0 for every vocabulary entry: strictly below the max before tok, at most the max from tok on; b non-increasing with Σ b_i = tok; the derived selector b_i − b_{i+1} is 1 exactly at tok and pins pm to an attained value
- cost: one comparison per vocabulary entry per token: argmax_marginal_cells_per_comparison

lax   (--unsound-argmax-lax):  tok attains the maximum
strict (default):              tok is the LOWEST-INDEXED maximum   ← the model's own rule

on the real 512-token continuations, 15 of 512 rows (C = 4,096) have two or three
co-maximal logits, so the two statements really differ. a lax run is marked a control.

The strict statement is the lax one with the selector replaced by a monotone indicator and one extra degree-2 constraint. It costs almost nothing more and it is the only sound one.

- trees (shape, model, trace, interaction, boundary): committed, committed, committed, committed, committed
- edges bound so far: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16
- log: [v] edge 16 bound: emitted id 264 is the lowest-indexed maximum

### Animation step 17 (stage 16: Next tokens)

**Model: Append the token and run again: position 6**

The capital of France is a city
top-5 logits at position 6 (real) · emitted:  city city :  18.00
 must :  16.50
 beautiful :  16.00
 place :  15.31
 popular :  15.31

The emitted id is appended and all 32 layers run for the new position. Attention now spans 7 keys; the earlier positions' K and V come from the cache, they are not recomputed.

**Prover: Not a new proof: one block of 512 positions is proved together**

- gadget: the block axis (harness/witness/plan.py · prover/src/boundary.rs)
- edge: 14 along the token axis; 16 at every emitted position
- commits: each segment covers S = 512 positions of one layer at once; a generated position is one more row in the same tables
- pre: the K/V cache of earlier blocks enters as a committed boundary root (edge 14), never recomputed
- checks: boundary-grid --verify --prompt: the id committed at position p must equal the argmax the head segment proved for position p − 1
- cost: the paper's request: 4,096 prompt + 512 generated = 9 blocks × 32 layers + 2 head segments = 290 proofs, 61 minutes

headargmaxargmaxL31…L0embembembB0B7B8 gen
vertical neighbours: residual-stream root equality (281 links)
horizontal neighbours: K/V root equality (256 links)
head on B7 and B8: every generated id is backed by a proved argmax

This is why the request is a grid and why there is no recursion: layers go up, blocks go right, and every arrow is one root comparison. A head on the generated block alone would leave the first generated id backed by nothing, so the head is proved on the last prompt block too.

- trees (shape, model, trace, interaction, boundary): committed, committed, committed, committed, committed
- edges bound so far: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16
- log: [v] position 6: id 3363 == head's argmax at 5

### Animation step 18 (stage 16: Next tokens)

**Model: Append the token and run again: position 7**

The capital of France is a city of
top-5 logits at position 7 (real) · emitted:  of of :  18.88
 that :  18.63
 like :  18.00
 steep :  17.00
 known :  16.50

The emitted id is appended and all 32 layers run for the new position. Attention now spans 8 keys; the earlier positions' K and V come from the cache, they are not recomputed.

**Prover: Not a new proof: one block of 512 positions is proved together**

- gadget: the block axis (harness/witness/plan.py · prover/src/boundary.rs)
- edge: 14 along the token axis; 16 at every emitted position
- commits: each segment covers S = 512 positions of one layer at once; a generated position is one more row in the same tables
- pre: the K/V cache of earlier blocks enters as a committed boundary root (edge 14), never recomputed
- checks: boundary-grid --verify --prompt: the id committed at position p must equal the argmax the head segment proved for position p − 1
- cost: the paper's request: 4,096 prompt + 512 generated = 9 blocks × 32 layers + 2 head segments = 290 proofs, 61 minutes

headargmaxargmaxL31…L0embembembB0B7B8 gen
vertical neighbours: residual-stream root equality (281 links)
horizontal neighbours: K/V root equality (256 links)
head on B7 and B8: every generated id is backed by a proved argmax

This is why the request is a grid and why there is no recursion: layers go up, blocks go right, and every arrow is one root comparison. A head on the generated block alone would leave the first generated id backed by nothing, so the head is proved on the last prompt block too.

- trees (shape, model, trace, interaction, boundary): committed, committed, committed, committed, committed
- edges bound so far: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16
- log: [v] position 7: id 315 == head's argmax at 6

### Animation step 19 (stage 16: Next tokens)

**Model: Append the token and run again: position 8**

The capital of France is a city of romance
top-5 logits at position 8 (real) · emitted:  romance romance :  15.69
 grand :  15.44
 beauty :  15.06
 love :  14.75
 great :  14.44

The emitted id is appended and all 32 layers run for the new position. Attention now spans 9 keys; the earlier positions' K and V come from the cache, they are not recomputed.

**Prover: Not a new proof: one block of 512 positions is proved together**

- gadget: the block axis (harness/witness/plan.py · prover/src/boundary.rs)
- edge: 14 along the token axis; 16 at every emitted position
- commits: each segment covers S = 512 positions of one layer at once; a generated position is one more row in the same tables
- pre: the K/V cache of earlier blocks enters as a committed boundary root (edge 14), never recomputed
- checks: boundary-grid --verify --prompt: the id committed at position p must equal the argmax the head segment proved for position p − 1
- cost: the paper's request: 4,096 prompt + 512 generated = 9 blocks × 32 layers + 2 head segments = 290 proofs, 61 minutes

headargmaxargmaxL31…L0embembembB0B7B8 gen
vertical neighbours: residual-stream root equality (281 links)
horizontal neighbours: K/V root equality (256 links)
head on B7 and B8: every generated id is backed by a proved argmax

This is why the request is a grid and why there is no recursion: layers go up, blocks go right, and every arrow is one root comparison. A head on the generated block alone would leave the first generated id backed by nothing, so the head is proved on the last prompt block too.

- trees (shape, model, trace, interaction, boundary): committed, committed, committed, committed, committed
- edges bound so far: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16
- log: [v] position 8: id 30363 == head's argmax at 7

### Animation step 20 (stage 17: Verify the grid)

**Model: The output, and what a verifier can conclude from it**

The capital of France is a city of romance

emitted ids264, 3363, 315, 30363

statement"ids [128000, 791, 6864, 315, 9822, 374] under the model with root R, decoded greedily in the y-delay-vw12 arithmetic, emit 264, 3363, 315, 30363"

not in the statementthe text, the tokeniser, sampling, batching, who was served, when

The model is done. What the proof adds is that nobody has to trust the provider's word for the decode: the computation is checkable from the ids, the model root and the calibration alone.

**Prover: Verify every segment, then every link, on a CPU with no weights**

- gadget: boundary-grid --verify (verify_composed per segment) (prover/src/compose.rs · boundary.rs)
- edge: all 16, per segment; 13 and 14 between segments
- commits: nothing: the verifier commits nothing
- pre: the verifier rebuilds the shape tree itself from params + calibration and compares the root; the model root is compared with the published manifest
- checks: replay the transcript; stwo verify (OODS + FRI, 100 queries, 100 conjectured bits); the LogUp sums cancel; every application identity; every root link; every id chained
- cost: about 43 s per segment on four consumer cores, dominated by rebuilding the shape tree; the whole c4096 proof is 18.5 GiB (7.2 GiB compressed)

statement parses · security parameters not drifted
shape root derived == pre_root declared
model root == published manifest
stwo verify: constraints low-degree at the OODS point, FRI accepts
LogUp sums cancel (GKR sums stand in for the key tiles)
Freivalds h_m == acc_m for all seven matmuls · attention and denominator identities
281 layer links + 256 token links: root equalities hold
every generated id == the head's argmax for the position before it

What this does not say: that the provider served this to anyone, that bf16 serving would give the same tokens (+6.96 % perplexity gap), or that a rerun reproduces it (issue #126). And nothing here is formally verified; the correctness evidence is the digest gate and the negative controls.

- trees (shape, model, trace, interaction, boundary): committed, committed, committed, committed, committed
- edges bound so far: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16
- log: [v] 290 / 290 segments accept · all_chain true | [v] run gate: no unsound skip, every edge bound, no kernel fallback

## The real run data behind the animation

Run on 7 October 2026: `unsloth/Llama-3.1-8B-Instruct`, bf16, Apple M4 Pro via MPS, 28 seconds for all three prompts, greedy decoding of four tokens each, no chat template, begin-of-text id 128000 prepended by the tokenizer. The int8 numbers below apply the harness's own rule (per-token scale = bf16_ceil(max|h| / 127), round half away from zero) to the bf16 model's layer-0 norm output; they are not a witness dump.

### Prompt: "The capital of France is"

- token ids: [128000, 791, 6864, 315, 9822, 374]
- pieces: ['<|begin_of_text|>', 'The', ' capital', ' of', ' France', ' is']
- greedy continuation: [264, 3363, 315, 30363] = [' a', ' city', ' of', ' romance'] (text: " a city of romance")
- step 0 top-5 logits: " a" 16, " Paris" 15.938, " known" 15.062, " home" 14.875, " the" 14.312; argmax id 264 (" a"); tie: False
- step 1 top-5 logits: " city" 18, " must" 16.5, " beautiful" 16, " place" 15.312, " popular" 15.312; argmax id 3363 (" city"); tie: False
- step 2 top-5 logits: " of" 18.875, " that" 18.625, " like" 18, " steep" 17, " known" 16.5; argmax id 315 (" of"); tie: False
- step 3 top-5 logits: " romance" 15.688, " grand" 15.438, " beauty" 15.062, " love" 14.75, " great" 14.438; argmax id 30363 (" romance"); tie: False
- residual-stream RMS at the last prompt position after the embedding and after each of the 32 layers: [0.006, 0.013, 0.022, 0.031, 0.051, 0.064, 0.07, 0.086, 0.091, 0.099, 0.111, 0.116, 0.12, 0.137, 0.145, 0.154, 0.169, 0.198, 0.221, 0.243, 0.273, 0.305, 0.343, 0.383, 0.424, 0.466, 0.512, 0.557, 0.609, 0.671, 0.747, 0.835, 2.176]
- attention of the last prompt token over the prompt, layer 0 head 0: "<|begin_of_text|>" 0.4629, "The" 0.2188, " capital" 0.0859, " of" 0.1602, " France" 0.0459, " is" 0.0261
- attention of the last prompt token over the prompt, layer 15 head 0: "<|begin_of_text|>" 0.2891, "The" 0.0304, " capital" 0.1289, " of" 0.2754, " France" 0.1104, " is" 0.167
- attention of the last prompt token over the prompt, layer 31 head 0: "<|begin_of_text|>" 0.2539, "The" 0.0083, " capital" 0.0168, " of" 0.015, " France" 0.1953, " is" 0.5117
- layer-0 norm-1 output for the last token: max |h| = 4.0312, per-token int8 scale s_x = 0.03173828125, first 8 values [-0.0171, 0.0201, 0.0152, 0.0093, -0.3203, -0.0099, 0, 0.0022] -> int8 [-1, 1, 0, 0, -10, 0, 0, 0]
- W_q row 0 (layer 0): first 8 bf16 weights [0.00516, -0.0293, -0.00644, -0.01819, -0.00327, 0.02637, -0.0007, -0.0023], per-channel scale s_w = 0.00045, int8 [11, -65, -14, -40, -7, 59, -2, -5]

### Prompt: "2 + 2 ="

- token ids: [128000, 17, 489, 220, 17, 284]
- pieces: ['<|begin_of_text|>', '2', ' +', ' ', '2', ' =']
- greedy continuation: [220, 19, 13, 1115] = [' ', '4', '.', ' This'] (text: " 4. This")
- step 0 top-5 logits: " " 14.125, " ?\n" 12.75, " ?" 12.375, " ?\n\n" 11.125, " (" 10.562; argmax id 220 (" "); tie: False
- step 1 top-5 logits: "4" 18.375, "5" 16.125, "6" 15.125, "3" 14.688, "8" 14.375; argmax id 19 ("4"); tie: False
- step 2 top-5 logits: "." 11.688, " (" 11.5, "," 11.312, ":" 10.812, "\n" 10.812; argmax id 13 ("."); tie: False
- step 3 top-5 logits: " This" 13.188, " " 12.375, " The" 12.062, " That" 12.062, " It" 12; argmax id 1115 (" This"); tie: False
- residual-stream RMS at the last prompt position after the embedding and after each of the 32 layers: [0.007, 0.015, 0.024, 0.041, 0.05, 0.06, 0.077, 0.086, 0.098, 0.107, 0.112, 0.117, 0.118, 0.132, 0.143, 0.152, 0.168, 0.194, 0.205, 0.23, 0.255, 0.269, 0.295, 0.317, 0.351, 0.377, 0.418, 0.464, 0.503, 0.553, 0.61, 0.692, 2.12]
- attention of the last prompt token over the prompt, layer 0 head 0: "<|begin_of_text|>" 0.3867, "2" 0.0649, " +" 0.3301, " " 0.1465, "2" 0.0205, " =" 0.0508
- attention of the last prompt token over the prompt, layer 15 head 0: "<|begin_of_text|>" 0.5469, "2" 0.0342, " +" 0.1001, " " 0.0505, "2" 0.126, " =" 0.1445
- attention of the last prompt token over the prompt, layer 31 head 0: "<|begin_of_text|>" 0.3555, "2" 0.0138, " +" 0.0737, " " 0.0146, "2" 0.2578, " =" 0.2832
- layer-0 norm-1 output for the last token: max |h| = 3.4531, per-token int8 scale s_x = 0.0272216796875, first 8 values [0.0047, -0.1855, -0.0027, 0.0127, 0.3145, 0.0117, 0, 0.0072] -> int8 [0, -7, 0, 0, 12, 0, 0, 0]
- W_q row 0 (layer 0): first 8 bf16 weights [0.00516, -0.0293, -0.00644, -0.01819, -0.00327, 0.02637, -0.0007, -0.0023], per-channel scale s_w = 0.00045, int8 [11, -65, -14, -40, -7, 59, -2, -5]

### Prompt: "Roses are red, violets are"

- token ids: [128000, 49, 20274, 527, 2579, 11, 348, 822, 10145, 527]
- pieces: ['<|begin_of_text|>', 'R', 'oses', ' are', ' red', ',', ' v', 'io', 'lets', ' are']
- greedy continuation: [6437, 11, 323, 279] = [' blue', ',', ' and', ' the'] (text: " blue, and the")
- step 0 top-5 logits: " blue" 20.5, " purple" 15.75, " green" 14.875, " too" 14.812, " violet" 14.5; argmax id 6437 (" blue"); tie: False
- step 1 top-5 logits: "," 19.75, "..." 16.625, ",\n" 16.5, "\n" 15.938, "." 15.812; argmax id 11 (","); tie: False
- step 2 top-5 logits: " and" 12.5, " but" 11.312, " I" 10.75, " this" 9.562, " the" 9.438; argmax id 323 (" and"); tie: False
- step 3 top-5 logits: " the" 10.375, " this" 10.188, " our" 9.875, " so" 9.812, " if" 9.625; argmax id 279 (" the"); tie: False
- residual-stream RMS at the last prompt position after the embedding and after each of the 32 layers: [0.007, 0.013, 0.022, 0.035, 0.047, 0.06, 0.066, 0.079, 0.104, 0.108, 0.11, 0.115, 0.122, 0.132, 0.141, 0.154, 0.171, 0.186, 0.197, 0.228, 0.248, 0.267, 0.294, 0.32, 0.355, 0.383, 0.432, 0.471, 0.522, 0.584, 0.677, 0.763, 2.152]
- attention of the last prompt token over the prompt, layer 0 head 0: "<|begin_of_text|>" 0.2373, "R" 0.0242, "oses" 0.0364, " are" 0.1396, " red" 0.0386, "," 0.2773, " v" 0.1191, "io" 0.0544, "lets" 0.0376, " are" 0.0364
- attention of the last prompt token over the prompt, layer 15 head 0: "<|begin_of_text|>" 0.2715, "R" 0.0006, "oses" 0.0215, " are" 0.0305, " red" 0.1138, "," 0.0128, " v" 0.026, "io" 0.03, "lets" 0.4609, " are" 0.033
- attention of the last prompt token over the prompt, layer 31 head 0: "<|begin_of_text|>" 0.1953, "R" 0.0054, "oses" 0.0806, " are" 0.1084, " red" 0.0742, "," 0.0317, " v" 0.0095, "io" 0.0022, "lets" 0.2109, " are" 0.2812
- layer-0 norm-1 output for the last token: max |h| = 3.8438, per-token int8 scale s_x = 0.0302734375, first 8 values [0.0272, -0.012, 0.103, -0.0121, -0.4121, -0.0052, 0, 0.0036] -> int8 [1, 0, 3, 0, -14, 0, 0, 0]
- W_q row 0 (layer 0): first 8 bf16 weights [0.00516, -0.0293, -0.00644, -0.01819, -0.00327, 0.02637, -0.0007, -0.0023], per-channel scale s_w = 0.00045, int8 [11, -65, -14, -40, -7, 59, -2, -5]

---

# Part 4. Repository documents, verbatim

## docs/statement.md (what the proof binds, edge by edge)

# What the proof binds

A proof made by this prover is about one **segment**: one transformer layer
applied to one block of `S` token positions with a context of `C` earlier
positions, or the language-model head applied to one block. A sequence is
proved as a grid of such segments, and `boundary-grid` checks that the segments
fit together. This page says, edge by edge, what one segment's proof binds and
what an unbound edge would let a dishonest prover do.

Every run prints its own copy of this table as `provenance.binding` (folded
over every proof the run made) and as `result.point.binding` per proof. The
table below is that report for a layer segment under the default flags with a
witness that carries everything the defaults need. The `state` column has
three values: **bound** (the verifier compares the producer's claim with the
consumer's, or both sides are columns of one AIR component), **unbound** (the
consumer reads a value nothing binds to its producer) and **absent** (neither
side is in this statement).

| # | edge | default | turned off by |
|---|---|---|---|
| 1 | residual stream into the first norm's reduction | bound | `--unsound-skip-residual-stream` |
| 2 | first norm's output into the q, k, v matmul inputs | bound | `--unsound-skip-residual-stream` |
| 3 | q, k, v outputs into the attention block | bound | `--unsound-skip-residual-stream`, or a dump without rotation parameters |
| 4 | attention scores and values into the attention output | bound | nothing: it is the attention component itself |
| 5 | attention output into the o matmul input | bound | `--unsound-skip-residual-stream` |
| 6 | o output into the first residual add | bound | `--unsound-skip-residual-stream` |
| 7 | first residual add into the second norm's reduction | bound | `--unsound-skip-residual-stream` |
| 8 | second norm's output into the gate and up matmul inputs | bound | `--unsound-skip-residual-stream` |
| 9 | gate and up outputs into the SwiGLU product | bound | `--unsound-skip-residual-stream` |
| 10 | SwiGLU output into the down matmul input | bound | `--unsound-skip-residual-stream` |
| 11 | down output into the second residual add | bound | `--unsound-skip-residual-stream` |
| 12 | each matmul's input times the pinned weights into its accumulator | bound | nothing: it is the Freivalds check itself |
| 13 | residual stream out of this segment into the next layer's segment | bound | `--unsound-skip-layer-boundary` |
| 14 | keys and values out of this token block into the next block | bound | `--unsound-skip-kv-boundary`, or a dump without its own block |
| 15 | embedding row into the first segment's residual stream | bound on layer 0, absent elsewhere | `--unsound-skip-embedding` |
| 16 | logits into the emitted token | bound on the head segment, absent elsewhere | `--unsound-skip-argmax`, or weakened past bound by `--unsound-argmax-lax` |

A head segment has no attention and no MLP of its own, so edges 3 to 11 and 14
are absent there. Absent says this segment states none of those seams, not that
its witness holds no such matmuls: a head dump carries its layer's eight
matmuls, and the head segment proves each of them against the pinned weights
(edge 12) while binding the input of none and reading the output of none. The
one requantize seam it states is the final norm's output into the head matmul.
Its edge 1 is the final norm's reduction, its edge 2 that seam, and its edge 13
the residual it consumed, committed as the in side of the last layer link.

## What each bound edge means

**The residual stream and the norms (1, 7).** The two RMSNorm reductions read
the residual stream the segment committed, not a copy: the norm's reduction
tree and the residual add are bound by an equality the verifier checks from
the claims. Unbound, the prover could normalise any vector it liked and
present the result as the norm of the residual. Each reduction's second level
publishes its answer, the mean of squares, and that list of equalities is the
only thing that reads it: one entry says the value the norm took the reciprocal
square root of is that answer, and a proof is accepted only if every entry
holds. An answer no entry named would be a value the prover could choose, so
the plan refuses to state one. The lookup tables this arithmetic reads are
padded to a power of two by repeating their last real row, so a row past a
table's real ones carries the same key and the same value as a real one; that a
proof puts no use on such a row is asserted by the prover and checked by
nothing, and it needs no check, because a use there would be answered with the
value of the row it copies.

**The requantize seams (2, 8, 10).** Every matmul consumes an int8
activation. The seam proves that activation is the requantization of the
producer's bf16 output under a per-token scale pinned to that output's own
maximum, and that the Freivalds check multiplied exactly those integers.
Unbound, the prover could feed a matmul any activation, and the matmul's
proof would faithfully multiply the wrong input.

**The dequant outputs (6, 9, 11).** A matmul's accumulator is dequantized to
bf16 and the component that consumes it (a residual add, the SwiGLU product)
reads the same values: the dequant publishes an output claim and the consumer
publishes the claim over what it read, and the two are compared. Unbound, the
prover could add any vector to the residual stream, or gate any product.

**The attention seams (3, 5).** Edge 3 says the q, k, v that the attention
component reads are the projections' outputs, rotated and rounded exactly as
the model does it: the rotation is its own component built from the
statement's rotation parameters, the per-head power-of-two quantize is
another, and the key tiles' columns are bound to their outputs. A site for a
projection's bias is **not built**: the dequant states `acc s_x s_w` and
nothing else, so a model that gives q, k or v a bias -- Qwen2.5 does, Llama
does not -- puts values in the key tiles that no component here derives, and
edge 3 refuses every layer of it. Edge 5 says the o matmul's input is the
attention output's requantization. Unbound, the attention would be over values
of the prover's choosing while the projections and the o matmul each prove the
wrong thing correctly.

The rotation holds one row per (token, head) and the quantize one per block of
channels inside a head, so both of their row counts have the head count as a
factor. A model whose head count has an odd factor -- Qwen2.5-14B has 40 query
heads -- therefore gives row counts that are a power of two at no block length.
Each component rounds its row count up to the next power of two and puts the
difference at the front as **unconstrained padding**:
rows whose every committed value is zero, on which the rotation is a product
and a sum of zeros and the quantize rounds a zero to a zero, so no constraint
of either component says anything about what they hold. What checks them is the
comparison the real rows are already bound by. Each component folds all of its
rows, the padded ones included, into one weighted sum, and that sum is compared
with the producer's -- the q and k matmuls' dequantized outputs on the way in,
the key tiles' own columns on the way out -- and the producer's runs over the
real values alone. A padded row carries weights no real value carries, so
anything but zero in one changes one side of that comparison and nothing else,
and the comparison fails. Nothing else in the segment reads a padded row. On a
model whose head count is already a power of two there is no padding and the
proof is the one it always was; at 40 heads the rotation holds 64 rows per token
for 40 real ones, and 37.5% of those two components' committed cells is
padding.

**The attention component (4) and the Freivalds checks (12).** These are not
seams but the components themselves: the softmax identities and the
accumulation are constraints of one AIR, and each matmul is a Freivalds check
against the committed weights. They have no skip; a statement without them
is not a statement about a transformer. The causal mask and the marker for the
rows a key grid really holds are both derived from the public parameters rather
than chosen by the prover, and the component subtracts the one from the other,
which is the same as gating on both only while the mask is clear on every row of
unconstrained padding. The code that builds the two columns asserts that, over
exactly those rows and with the predicate that writes them, on the one path that
builds them for either backend.

**The shape tree.** Those two columns are not the prover's, and neither is any
other column the AIR reads as a fact: every selector, the marker for the rows a
key grid really holds, the range tables' row indices, the rotation's angles.
They are committed as a tree of their own, and what says they are the columns
the public parameters give is that the verifier **builds that tree itself** and
compares its root with the root the statement declares. It needs two things to
do it and holds both: the statement's own parameters, and the per-layer
calibration the model manifest publishes beside the model commitment. No weight
enters the shape tree, so no dump is needed. A verifier given no calibration
derives nothing, and then the shape root is asserted by the prover and checked
by nothing -- a run says which of the two it was. The other preprocessed tree is
the model's, and its root is not derivable by anyone but the publisher: it
commits the weights, and the verifier compares it with the published manifest.

**The boundaries (13, 14).** The residual stream leaving a segment and the
keys and values a block writes are committed as their own trees, and
`boundary-grid` compares each such root with the root the consuming segment
committed for its input. Unbound, the segments could each be honest while
the sequence they form is not: a layer fed a residual nobody produced, or a
block attending to a cache nobody wrote.

**The ends (15, 16).** The embedding gadget binds a layer-0 segment's
residual stream to the rows of the embedding matrix that its published ids
select; the argmax binds the token a head segment emits to the **lowest-indexed**
maximum of the logits it computed, which is the rule the model itself decodes
by. Unbound, the sequence could start from any vector, or emit any token, and
`boundary-grid --verify --prompt` would have nothing to compare the published
ids with.

Edge 16 has a second, weaker form. `--unsound-argmax-lax` proves that the
emitted token attains the maximum instead of that it is the first token to
attain it. Where two logits are co-maximal -- 15 of 512 positions at a context
of 4096 on the real continuations -- the weaker statement admits either of them
and the strict one admits only the first, so a lax proof holds for a token the
model would not have emitted. The table marks edge 16 unbound while it is on
and says so in the row, and `provenance.unsound_skips` lists `argmax-lax`: the
run is a control, exactly as one with a skip is.

## The unbound configuration

Every skip flag names one of these edges, and `--unsound-argmax-lax` weakens
edge 16 rather than dropping it. A run whose `provenance.unsound_skips`
is not empty is a control or a measurement of cost, never a statement about a
forward pass, and `zk-results` refuses to tag a release that cites one. The
digests recorded before the sound defaults reproduce with the skips set, and
`prover/README.md` lists both configurations.

## zk-inference-results/docs/quantization.md

# The quantization configuration

The harness runs the model in a fixed integer and bf16 arithmetic and writes
the witness the prover constrains, so the quality numbers describe exactly
the arithmetic that is proved. The configurations are named presets in
`harness/witness/common.py` of `zk-prover`; the numbers that will back this
page are the constants named in parentheses, none of which exists yet in
this repository.

## What the paper reports: `y-delay-vw12`

- Linear layers: activations quantized to int8 per token with a dynamic
  scale, weights to int8 per output channel; the accumulation is exact in
  the field.
- Dequantization after the seven layer matmuls: a chain of three
  correctly-rounded bf16 steps, rounding half to even, so a general bf16
  scale can be proved; the output head uses power-of-two scales instead,
  which collapse the chain to one rounding.
- Nonlinear operations in bf16, with the normalisation's reduction as a
  balanced tree in bf16.
- Attention scores as an integer softmax: queries at 12 bits, keys at 11,
  power-of-two attention scales with one query scale per head, a 9-bit
  softmax numerator; the exponential is a lookup table keyed by the bf16
  input.
- The attention output rounded straight to an integer with a power-of-two
  output scale, at 12 bits rather than 8, so the output projection consumes
  a wider value and one rounding is saved.
- The value projection's requantization delayed to its consumer, which
  removes the chain's roundings on that path; only the key/value cache sits
  between the two.

Its perplexity against the fp32 model (`quality.8b.ppl_y_delay_vw12_delta_pct`)
and its scores on the three tasks (`quality.8b.gpqa_d_y_delay_vw12`,
`quality.8b.mmlu_pro_y_delay_vw12`, `quality.8b.ifeval_prompt_strict_y_delay_vw12`)
are measured against a byte-identical fp32 control on the same items; each
task carries its own paired standard error, since the item counts differ
(`quality.8b.gpqa_d_paired_se_vs_fp32_y_delay_vw12`,
`quality.8b.mmlu_pro_paired_se_vs_fp32_y_delay_vw12`,
`quality.8b.ifeval_prompt_strict_paired_se_vs_fp32_y_delay_vw12`).

## Variants measured beside it

- `fp32`: the reference forward pass.
- `dynamic-int8`: dynamic int8 linear layers, bf16 nonlinear operations, no
  integer softmax; the published system's configuration as far as it is known.
- `static`: static per-tensor W8A8 with a calibrated activation scale, the
  weakest int8 there is (`quality.8b.ppl_static_w8a8`).
- `w8a16`: weight-only per-channel int8 with float activations, the int8
  variant a reader would actually deploy (`quality.8b.ppl_w8a16`).
- `b6-design-p2o`, `b10-design`, `b10-residual-stream`, `b10-final`: the sequence of
  configurations that led to the reported one, each adding one choice; the
  perplexity of each is a measured row (`quality.8b.ppl_b10_final`).
- `y-attnout-w10`, `-w11`, `-w12`, `-w16` and `y-delay-v`, `y-delay-up`,
  `y-delay-all`: one change each on `b10-final`, the probes from which the
  reported variant was composed.

A second, smaller model (`quality.gemma270m.*`) checks that the configuration
transfers across architectures, including a sliding-window attention.

## zk-inference-results/docs/statement-gap.md

# The gap between the statement proved and a request as served

The prover proves one end-to-end statement about one request: every position of
a prompt and of a 512-token greedy continuation, from the embedding up through
every layer and through the output head, under one fixed quantization
configuration, with the residual stream bound between layers and the keys and
values bound between token blocks
(`docs/decisions/2026-09-03-end-to-end-statements-only.md`; the prover's
`prover/README.md` in `zk-prover` says which gadget binds which edge and which
switch gives one up).

A request a provider serves is not that. This page states the difference row by
row: what is proved today, what a provider does instead, and what closing the
row would take. It closes nothing, and where a row names a design it names it in
one sentence. A number appears only where `constants.json` holds one, with the
key beside it.

| row | tracked by |
|---|---|
| Arithmetic | no issue |
| Decoding | none open; `zk-prover` #179 closed by the owner |
| Determinism | `zk-prover` #126 |
| Tokenization and the chat template | no issue |
| Batching and the serving stack | `zk-prover` #12 for the prover's ceiling; nothing for a batch dimension |
| Binding to the traffic record | no issue |
| The architecture | `zk-prover` #174 for the bias site; nothing for the rest |
| Tool calls, system prompts, multi-turn | no issue |

## Arithmetic

**Proved today.** The fixed quantization configuration `y-delay-vw12`, which
`docs/quantization.md` states in full: int8 activations per token with a dynamic
scale, int8 weights per output channel, accumulation exact in the field,
dequantization as correctly-rounded bf16 steps, the nonlinear operations in
bf16, and an integer softmax with queries at 12 bits and keys at 11. The
statement is about that arithmetic and about no other.

**A provider instead.** Serves bf16, or fp8, on whichever kernels its stack
picks. The measured stand-in for a published system is the `dynamic-int8`
variant (`quality.8b.ppl_dynamic_int8_delta_pct`).

**What the difference costs.** Against a byte-identical fp32 control on the same
items: perplexity `quality.8b.ppl_y_delay_vw12_delta_pct`, +6.96 per cent, with
the paired standard error in `quality.8b.ppl_y_delay_vw12_se_nats`; the paired
task differences `quality.8b.mmlu_pro_paired_delta_y_delay_vw12` and
`quality.8b.gpqa_d_paired_delta_y_delay_vw12` are both 0.0, and
`quality.8b.ifeval_prompt_strict_paired_delta_y_delay_vw12` is -0.006. On a
second, smaller architecture the same configuration costs
`quality.gemma270m.ppl_y_delay_vw12_delta_pct`, +14.6 per cent.

**To close it.** A statement over bf16 matmuls and a bf16 softmax, in place of
the int8 product and the integer softmax. What that would cost in committed
cells is in no constant and in no count: it has not been counted, and no figure
in this repository stands in for it.

**Tracked by.** No issue.

## Decoding

**Proved today.** Greedy decoding. The head segment proves that the emitted
token is the lowest-indexed maximum of the logits computed for the position
before it, which is the rule the model decodes by; `--unsound-argmax-lax`
weakens that to any maximum and marks the run a control. The decode a witness is
extracted from does not stop at an end-of-text: `harness/witness/gen_ids.py`
records a stop and passes it through, so the statement is 512 decoded tokens
whatever the model would have done.

**A provider instead.** Samples from the softmax under a temperature and a
top-p, and stops at the end-of-sequence token.

**To close it.** Either a statement over the softmax of the whole vocabulary
with a seed committed before decoding, or VerInf's bound on the information the
committed model does not explain (`verinf.maverick.bound_bits_per_token`, 0.88
bits per token), which bounds information and does not prove which token was
drawn.

**Tracked by.** `zk-prover` #179 asked for both designs, costed; the owner
closed it, because the post names the two ways and leaves them open. No open
issue.

## Determinism

**Proved today.** One decode. The ids of that decode are an input to every
segment of the sequence, and the proof binds the tokens to the logits computed
for them.

**A provider instead.** Reruns the same prompt. `zk-prover` #126 records three
repetitions of one greedy point on the `hf` backend at context 4,096 -- same
process, same weights, same prompt, sampling off, no early stop -- whose
generated-token digests do not all agree: the first and third do, the second
does not.

So the proof is honest about the decode it was made from and says nothing about
whether the model would produce that decode again: a verifier who checked it by
re-running the model would be comparing against an output the serving path does
not reproduce.

**To close it.** A serving path whose reductions are pinned, so that a rerun is
a check. #126 is neither diagnosed nor fixed, and it lists what to rule out
first.

**Tracked by.** `zk-prover` #126, open, labelled `defect`.

## Tokenization and the chat template

**Proved today.** The statement's public input is a sequence of token ids. The
verifier is given them -- `boundary-grid --verify` demands `--prompt` as it
demands the calibration manifest -- and the layer-0 embedding gadget (edge 15)
proves that the residual stream the first layer reads is the committed embedding
matrix's row for the committed id. The ids the measured runs prove are a slice
of a corpus token array, cut by `harness/witness/gen_ids.py --prefix/--offset`;
no chat template is applied to them.

**A provider instead.** Receives text: a system prompt, a user turn, sometimes
tool definitions. It applies a tokenizer and a chat template to get ids, and
detokenizes ids to get the text it returns.

**To close it.** The tokenizer and the template inside the statement, or a
commitment to both with the check left outside the proof. Neither exists. Both
ends of a request -- the text in and the text out -- are outside every proof
this repository records.

**Tracked by.** No issue.

## Batching and the serving stack

**Proved today.** One request, one segment at a time: 512 output positions
against a committed key prefix, 32 layer segments to a token block, and an
output head segment over the last prompt block and the generated one
(`segments.headline.c16384` over `positions.headline.c16384`). There is no batch
index in the statement.

**A provider instead.** Batches requests and paginates the key/value cache
across them. The baseline campaign records what that is worth, per request, at
batch 1 through 16 on both backends: `pos_s.unproved.vllm.c4096.b1.end_to_end`
against `pos_s.unproved.vllm.c4096.b16.end_to_end`, where the host's own figure
is sixteen times the second.

**To close it.** A batch index in the statement, or a per-request proof taken
while the server batches, under which the other requests' rows of a batched
matmul are in the witness and not in the statement.

**Tracked by.** `zk-prover` #12 tracks the prover's own ceiling, which is
host-side witness generation. No issue for a batch index or for the paginated
cache.

## Binding to the traffic record

**Proved today.** Nothing. A proof names its prompt ids, the model root it was
made against and the shape root the verifier derives; no proof here names a
request, a client, a time or a served response. What a verifier learns is that
these ids produce these tokens under this model commitment, not that this is
what anybody was served.

**A provider instead.** Serves over an API, records the request and the
response, and can hand a client a transcript of both.

**To close it.** An anchor that commits the served transcript and a proof that
the ids it proves are that transcript's ids. Issue #117 names VerInf's
transcript anchor as the precedent; nothing in this repository records what that
anchor commits to, and the `verinf.*` constants are that work's measurements and
not its anchor.

**Tracked by.** No issue. `zk-prover` #179 put this row out of its scope by
name.

## The architecture

**Proved today.** Dense Llama-shaped decoder blocks: seven matmuls to a layer,
RMS norms, SwiGLU, a rotation, grouped-query attention, and a causal mask on the
diagonal block over a prefix whose key tiles carry no mask columns at all. The
shape is public, by construction: the verifier rebuilds the shape tree from the
statement's own `params` and the per-layer calibration the model manifest
publishes, so layer count, head counts, widths and context are things the
verifier knows rather than things the proof hides.

**A provider instead.** Serves models the statement cannot state. A projection
bias is the measured case: Qwen2.5 gives `q_proj`, `k_proj` and `v_proj` one,
the dequant component states the product and nothing else, and the extractor
refuses such a dump by name (`zk-prover` #174, with #172 the rejection it
measured on layer 0 of the 14B witness). Beside it: sliding-window and
alternating local-global attention, QK-norm, a logit softcap, and mixtures of
experts. Providers also do not publish the architecture at all, which the
statement's public shape does not allow for.

**To close it.** A component for each site: a per-channel add between the
dequantization and the rotation, which is #174's list of four sites; mask
columns on the prefix key tiles, so that a key outside a window can be excluded;
a norm between the projection and the rotation. The quantization configuration
was checked on a sliding-window model in the harness
(`quality.gemma270m.ppl_y_delay_vw12_delta_pct`), and the cost model prices a
mixture-of-experts shape, so both exist as arithmetic and as a projection; what
neither has is a statement.

**Tracked by.** `zk-prover` #174 for the bias site. No issue for the window, for
QK-norm, for the softcap, for mixtures of experts, or for hiding the
architecture.

## Tool calls, system prompts, multi-turn

**Proved today.** One prompt and one continuation. Within a sequence, a
generated position's id is bound to the argmax proved for the position before
it, which is why a headline run proves an output head segment over the last
prompt block as well as over the generated one. Across turns there is no such
binding: each turn is a new prompt, proved by itself.

**A provider instead.** Runs a conversation. A system prompt the user never
sees, several turns, a key/value cache reused between them, and tool calls whose
results the server writes into the context -- content that the model did not
produce and that the next turn is conditioned on.

**To close it.** A binding from one proof's emitted ids into the next proof's
prompt ids, and a statement for the content the server inserts between the two.
Neither exists; a multi-turn session is as many unrelated proofs as it has
turns.

**Tracked by.** No issue.

## GLOSSARY.md

# Glossary

Identifiers kept although a standard word exists. Prose uses the standard word;
code and flags use the identifier. Each entry is one sentence; the list shrinks
when a rename is cheap.

- **chunk** — a segment: the computation of one layer (or of the output head)
  for `S` freshly decoded tokens against the committed key/value cache at
  context `C`, proved as one STARK; every recorded run has `S = 512`.
- **cell** — one committed field element of a trace column, the unit in which
  prover work is counted (columns times rows).

## prover/README.md, the sections on the verifier and the soundness switches

## What the verifier derives

`verify_composed` -- the only accept path, and what `boundary-grid --verify`
runs on every chunk -- rebuilds the shape tree from the statement it verifies
and compares the root it gets with the `pre_root` that statement declares
(issue #95). Its two inputs are the statement's own `params` and the per-layer
calibration the model manifest publishes, and the second is a command line of
the verifier's own:

```sh
zk-prover boundary-grid --dir SER --verify --prompt IDS --verify-calibration MANIFEST
zk-prover compose <flags> --verify-calibration FILE
```

`FILE` is the manifest `zk-prover model-roots --out` writes, whose row for the
chunk's `(layer, c)` carries `frac_per_head` beside the model root; for one
segment it is also the `result.shape.calibration` block every run publishes, or
a dump's `manifest.json`. `boundary-grid --verify` demands it, as it demands
`--prompt`. Without it a run derives nothing, `verdict.shape_root_ok` is null,
and the shape root is asserted by the prover and checked by nothing, which is
what every verifier had before this.

The derivation costs the preprocessed build of one shape tree, paid once per
`(layer, shape)` in a process: a grid pays one derivation per cell of the
`(layer, context)` table and not one per proof. The model root is not
derivable -- it is the publisher's commitment to weights the verifier does not
hold -- and stays a comparison against the same manifest
(`boundary-grid --expect-model-roots`).

## The digest gate

Any change that is not meant to alter the proof reproduces every digest below
on both backends before it merges. A change that alters the proof records the
new digests here, in the same pull request, and says why. The digest is
`result.point.proof_sha256` in the JSON the binary prints on stdout.

The scripts that run this are in `tools/gate/`: one ships a tree to a GPU box,
one runs the gate there, one prepares a fresh box. The gate builds both
backends, generates and installs the kernels for the synthetic shapes in
between, checks that the vendored library was really built for the card it is
about to use, and runs the test suite on each backend. Any CUDA card runs it;
24 GB is enough. The 8B reference proof is the exception -- it needs an 80 GB
card, so it runs at the points the refactor's tracking issue (#211) lists and
not per pull request. `tools/gate/README.md` says how to run both and when.

## Soundness switches

Every binding gadget is on by default wherever the witness lets it be stated:
the residual-stream components (the norms, the residual adds, the requantize
seams, the dequant output bindings, the rotation), the boundary trees over the
residual stream and over the keys and values, the argmax on a head segment and
the embedding gadget on a layer-0 segment. A witness that cannot state one is
refused with a message naming the skip that gets past the refusal:

| `--unsound-skip-<name>` | what it gives up | when a witness forces it |
|---|---|---|
| `residual-stream` | the residual-stream components: edges 1 to 3 and 5 to 11 of the binding table | a dump extracted without `--residual-stream`, or a bare synthetic segment |
| `layer-boundary` | the residual-stream boundary trees (edge 13) | never |
| `kv-boundary` | the K/V boundary trees (edge 14) | a segment without its own block (`--diagonal-block`) |
| `argmax` | the head's argmax (edge 16) | a head dump without `key_head.u16`, or a synthetic head |
| `embedding` | the layer-0 embedding gadget (edge 15) | a layer-0 dump extracted without `--embed` |

One switch weakens a gadget instead of turning it off. `--unsound-argmax-lax`
proves that the emitted token attains the maximum of the logits where the
default proves that it is the lowest-indexed maximum, which is the rule the
model decodes by; on a position whose two highest logits are equal -- 15 of 512
at a context of 4096 on the real continuations -- the weaker statement admits
either token. It is off by default, it is refused on a statement that states no
argmax, it lists `argmax-lax` in `provenance.unsound_skips`, and the binding
table marks edge 16 unbound with that reason while it is on, so a run that used
it is visibly a control. The name it had before, `--argmax-lax`, is an error.

The skips in effect are listed in `provenance.unsound_skips`; an unknown name
is an error. The flags these replaced (`--bounds`, `--kv-bind`, `--embed`,
`--head-argmax`, `--head-key`, `--norm-tails`, `--swiglu`, `--deq-ties`,
`--no-glue`) are retired and reported once on stderr when seen. The five
`--gkr-*` flags are not soundness switches: they choose the LogUp-GKR backend
for a component and change the proof, not the statement.

## prover decisions: 2026-09-03-bf16-keyed-tables-stay-bf16-keyed.md

# Lookup tables keyed by a bf16 value keep bf16 keys

Date: 2026-09-03. Status: decided by the owner.

## Decision

No lookup table the AIR indexes by a bf16 value moves to an integer key. This
covers the softmax's exponential table and the normalisation's reciprocal
table, and any table added later whose input is a bf16 intermediate of the
quantized forward pass.

## Why

The harness scores the model on exactly the arithmetic the proof constrains:
the same bf16 intermediates, the same roundings, in the same order. Re-keying
a table by an integer changes that arithmetic, so the quality numbers would no
longer describe the proved computation, and every perplexity and task result
would have to be measured again on the new arithmetic before it could be
cited. A cheaper table is not worth a second quantization configuration.

## Consequence

A change that wants a smaller or faster table changes how the bf16 key is
formed or how the table is committed, not what it is keyed by.

## prover decisions: 2026-09-08-the-head-is-proved-over-the-last-prompt-block.md

# The output head is proved over the last prompt block as well

Date: 2026-09-08. Status: decided by the owner (2026-09-08).

## Decision

An end-to-end statement carries a head segment over the last block of the
prompt as well as over the generated block, so that every emitted token is
bound to a proved argmax (edge 16). The first generated token's id is the
argmax of the logits at the last prompt position; with a head segment over
the generated block only, that one id was compared against nothing.

## Why

Binding the emitted token is what makes the statement end to end rather than
a statement about layers. One unbound id out of 512 is a soundness gap, not a
rounding of the claim: a prover could emit any first token and prove the rest
honestly. The cost is one more head segment per statement, about a minute of
proving out of hours, and one more head dump.

## Consequence

The zk-results plans name both blocks for the head; the link pin and the grid's
`--verify --prompt` check cover every generated position. The run at context
16,384 in flight on 2026-09-08 carries the generated block's head only and is
recorded with the gap stated in one sentence; a head segment over its last
prompt block is added as the run's last step where the driver's restart path
allows it, else the campaign is run again. The recorded digests do not move:
nothing in the prover changes.

## prover decisions: 2026-09-08-the-rotation-gadget-pads-the-head-count.md

# The rotation gadget pads tokens times heads to a power of two

Date: 2026-09-08. Status: decided by the owner (2026-09-08).

## Decision

The prover supports models whose attention head count has an odd factor. The
rotation gadget, which today requires the block length times the head count to
be a power of two and refuses a layer otherwise, pads its rows to the next
power of two with rows that the constraints hold trivially on and that no
other component reads.

## Why

The prover is meant to prove more models than the one the paper measures. A
head count with a factor of five (Qwen2.5-14B has 40 query heads) can never
tile a power of two at any block length, so without padding a whole model
class is out of reach (zk-prover #73), and the registered-prediction campaign
has no shape to run on. Padding costs committed cells in proportion to the
gap to the next power of two (64 rows for 40 heads: 60% more rotation rows on
that model, none on the 8B) and changes nothing on a model that already tiles.

## Consequence

The gadget's row count becomes a statement parameter derived from the shape,
not an assertion; the binding table names the padded rows as unconstrained
padding, checked to be zero. The recorded digests do not move: every recorded
shape tiles exactly and takes the same path as before. The change is its own
issue with the digest gate on both backends.

## prover decisions: 2026-09-09-the-verifier-derives-the-shape-root.md

# The verifier derives the shape root instead of reading it

Date: 2026-09-09. Status: decided by the owner (2026-09-09).

## Decision

`verify_composed` rebuilds the shape tree from the statement's own parameters
and the per-layer calibration the model manifest publishes, and compares the
root it derives with the `pre_root` the statement declares. A mismatch is a
rejection naming both roots. The model root is not derived: it commits weights
the verifier does not hold, so it stays a comparison against the published
manifest.

The calibration is the verifier's input, given as `--verify-calibration FILE`,
and `boundary-grid --verify` demands it as it demands `--prompt`. A run given
none derives nothing and says so: the shape root is then asserted by the prover
and checked by nothing, which is what a single proof's verification did before
this.

## Why

The shape tree carries the columns the AIR reads as facts rather than as the
prover's values -- every selector, the causal mask, the marker for the rows a
key grid really holds, the range tables' indices. A verifier that read the root
off the statement accepted one proof against whatever shape that statement
named, and the mask invariant the attention component rests on held only because
`boundary-grid --expect-pre-roots` compared the declaration with a table derived
elsewhere. A run that verified one proof alone made no such comparison.

The derivation became affordable in two steps. The shape tree was shown to be a
function of exactly the statement and the per-layer calibration, and cached
under that pair; then the loader was given a form that builds a segment from
those two alone, with no dump on disk. What was left was to make the comparison.

## Consequence

A verifier pays one preprocessed build per `(layer, shape)` in a process: a grid
of 290 segments over 32 layers pays about 32 derivations, not 290, and each is
the cost `expect-root --shape-only` already had. `--expect-pre-roots` becomes a
second opinion rather than the only one -- it compares the same statements
against a table derived outside the run.

Nothing about proving moves: no column, no constraint, no committed value, and
no recorded digest.

## prover decisions: 2026-09-11-cells-are-counted-from-the-layout-wherever-a-shape-can-be-stated.md

# Cells are counted from the layout wherever a shape can be stated

Date: 2026-09-11. Status: decided by the owner (2026-09-11).

## Decision

The exact formula is used wherever we can use it. Wherever a shape and a
context can be stated as a `params` block, the cost model and the frontier
table COUNT that segment's committed cells from the prover's own trace layout
(`harness/costmodel/exact_cells.py`) instead of pricing them from per-unit
constants read off a measured segment.

Three things are left, and each is named in the output rather than folded into
a residual:

1. The fitted per-unit constants stay for what the prover has no layout for.
   Today that is the mixture-of-experts routing inputs alone --
   `route_selection_cells` and `route_topk_cells` -- which no AIR in this
   project builds and which are priced by analogy with the nearest gadget that
   was measured. The output says `analogy` beside them.
2. The fields of a `params` block that a caller with a model and a context
   cannot know are ONE named assumption block with a stated size in cells. They
   are the calibration a run took off its own witness -- the master exponent
   table's height, the normalisation table's binades and the attention output's
   measured exponent ranges -- plus two knobs of the prover's command line, the
   head grouping and the attention variant.
3. A shape whose segment is not a `params` block is REFUSED with the reason.
   The latent-attention shapes are refused today: their layer has five matmuls
   and not four and their cache is one latent, so the key grids read a width
   the prover has no layout for. A refusal is printed where the row would have
   been; the fitted number is not printed under the same heading.

## Why

A per-unit constant is a ratio measured at one shape, and the frontier table's
whole purpose is to extrapolate to shapes no run has proved. zk-prover #168
computed the same per-unit quantities exactly at four other recorded segments
and they are not constants:

| per-unit constant | at `B8L16` / `B32L16` / `B8L0` | at the output head | at the c512 prefill shape |
| --- | --: | --: | --: |
| `dequant_chain_composed_cells_per_acc` | 16.059524 (+0.00%) | 11.250514 (-29.94%) | 13.196429 (-17.83%) |
| `attnout_composed_cells_per_acc` | 10.375 (+0.00%), but 11.375 (+9.64%) on `B8L0` | 10.375 (+0.00%) | 10.375 (+0.00%) |
| `quant_composed_cells_per_value` | 17.5 (+0.00%) | no quantize component | 26.25 (+50.00%) |
| `requant_composed_cells_per_value` | 18.437544 (+0.00%) | 17.118896 (-7.15%) | 23.450521 (+27.19%) |
| `weight_freivalds_composed_cells_per_weight` | 0.201923 (+0.00%) | 0.155148 (-23.16%) | 2.383929 (+1080.61%) |

The last row is the clearest. What a segment COMMITS for the Freivalds check is
the activations, `pq * 2^log_rows`; the weights are preprocessed. A per-weight
figure is therefore a ratio of two quantities that do not scale together: right
at the 8B layer segment it was read off, and an order of magnitude out at a
128-wide one.

The count that replaces them is not a better fit. It reproduces `cells.base`,
`cells.interaction` and `cells.fresh` to the cell on all 1,872 recorded chunks
in zk-results -- both headline runs, the older run at context 4,096, the memory
probe and every configuration of the reduction ablation -- and on every
single-segment run beside them, over S from 32 to 2,048, C from 128 to 16,384,
both attention variants and both roundings. Nothing in it is fitted and nothing
in it reads a measured input.

## What stays an assumption, and what it costs

A `params` block is not an architecture. Several of its fields are the
calibration a run took off its own witness, and three groups of them move the
cell count:

| what | what it sizes | on a recorded segment |
| --- | --- | --- |
| `log_table` | the master exponent table, `5 * 2^log_table` cells | 0.95% to 10.89% of a segment |
| `kmax` | the normalisation table and the fraction table | 0.22% to 0.39% |
| `ao_acc_hi_bits`, `ao_rem_bits`, `ao_jo_*`, `ao_jv_*` | three range tables and the exponent window | 0.01% to 0.38% |

`log_table` is the one that matters. It is 22, 23, 24 or 25 over the layer
segments of a single token block, and it is chosen so the table covers the
scores the witness actually produced -- a property of the activations, not of
the shape. Everything else in the segment is the architecture.

The assumption is each field at the modal value of the recorded 8B headline
runs. Priced against the 32 layer segments of one token block, that is +0.09%
at context 4,096 and -0.53% at context 16,384; given each segment's own
recorded fields the same count is exact, to the cell, on both blocks. So the
residual a projection carries is the price of a stated assumption and not a
modelling error, which is the whole point of the change.

## How a projection presents it

A projected row is not allowed to hide the assumption inside its number.

- The assumption is one block in the output (`result.assumptions`), one entry
  per field: the value, the run and segment its mode is read from, what it
  sizes in cells and what that is as a share of a segment.
- zk-results records each entry as its own constant, graded `derived` where it
  is the mode of measured values and `asserted` where it is a choice, and every
  projected row names those keys in its `inputs`.
- Every row prints an UPPER BOUND beside its point estimate: the same statement
  with every witness-calibrated field at the widest value the recorded runs
  carry. That is a bound over the evidence and not a theorem, and the output
  says so -- the prover's automatic path caps the exponent table at `2^22` and
  every value above it is the per-layer calibration a model manifest publishes.
- The calibration a run reports is the exact count of one token block's layer
  segments against `cells_per_position.headline.c{4096,16384}.fresh_layers_block`,
  which compares the same segments on both sides.

## Consequence

`harness/costmodel/frontier.py` counts by default and keeps the fitted path
behind `--cells fitted`, so the two can be compared and neither falls back to
the other. `harness/costmodel/cost_model.py` gains the same count under
`cells="exact"`; its default stays fitted because
`harness/eval/predict/predict.py` is a registration, and whether a registered
prediction moves to the counted number is the owner's to decide.

Two numbers move because the count is right where the constant was not. The
committed side of the Freivalds check does not scale with the expert count, so
a mixture-of-experts proof costs what its dense twin costs on the committed
side and the expert count lands on the preprocessed trace, which the measured
rates do not count. And the key tiles are committed per attention head rather
than per key/value group, which the count carries at every shape rather than at
the one it was read off.

## results decisions: 2026-09-03-end-to-end-statements-only.md

# The paper measures end-to-end statements only

Date: 2026-09-03. Status: decided by the owner.

## Decision

Every prover-side number the paper cites comes from a statement that proves
the prompt and the output from the embedding up: the whole forward pass over
every position, with the residual stream bound between layers and the keys
and values bound between token blocks. Decode-only sequences, which prove
512 output tokens against a key/value cache that is committed but not itself
proved, are not measured and do not appear in `constants.json`.

## Why

A decode-only rate leaves the prompt's computation asserted by the prover
and checked by nothing, so it is not a rate for the claim the paper makes.
Carrying both kinds of row invites the comparison of an end-to-end rate to a
decode-only one, which is the error the private archive's records made.

## Consequence

The campaign list has no decode driver. A comparison between cards, if
wanted, runs the end-to-end configuration on the second card. Positions per
second, not tokens per second, is the unit of every throughput constant.

## results decisions: 2026-09-03-gpu-time-priced-at-reference-rates.md

# GPU time is priced at reference market rates, never at what was paid

Date: 2026-09-03. Status: decided by the owner (2026-08-31).

## Decision

Every dollar figure divides a measured time by a published on-demand rental
rate for the card, from one provider, one tier and one date for all cards
compared (`cost.h100_reference_usd_per_hour`, `cost.h200_reference_usd_per_hour`).
What the project actually paid for its hosts is never a divisor and never
printed.

## Why

One host was sponsored and one was rented at a negotiated price; neither is
a rate a reader can obtain. A published list price is reproducible and, at
the higher tier, conservative for a cost claim.

## Consequence

The rates are `external` constants with their URLs. A cost constant names
them in its derivation, and `check.py` recomputes it.

## results decisions: 2026-09-03-paper-configuration-all-five-gkr-flags.md

# The paper's configuration has all five GKR flags on

Date: 2026-09-03. Status: decided by the owner (first recorded 2026-08-31).

## Decision

Every prover-side number the paper cites is measured with all five GKR
reductions enabled: on the attention key tiles, the dequantization gadgets,
the residual stream, the Freivalds checks of the weight matmuls, and the
attention output. The default build enables them; a run without them is a
control, reported as such, and never a headline.

## Why

The reductions remove committed cells without changing what is proved, and
the paper's throughput claim is about the prover as built. Reporting the
slower configuration would understate the system; reporting a mix would make
the numbers incomparable.

## Consequence

Drivers set the five flags in one place and write them into the manifest.
A run the paper cites with any of them off is a defect in the driver.

## results decisions: 2026-09-03-paper-quantization-delayed-requantization.md

# The paper's quantization configuration is the delayed-requantization variant

Date: 2026-09-03. Status: decided by the owner (2026-09-02).

## Decision

The paper reports the variant `y-delay-vw12`: the fixed configuration
`b10-final` with the value projection's requantization delayed to its
consumer and a 12-bit attention output. Every quality number, every witness
and every prover-side number the paper cites is on this variant; other
variants appear only as measured alternatives, labelled.

## Why

Both changes are improvements on the measured evidence: fewer committed
cells and a small quality gain against `b10-final`, at no cost to what the
proof binds. The owner's rule is that every optimisation that is one goes in.

## Consequence

The witness extraction and the task suite run on this variant. Rows measured
on `b10-final` before this decision are carried only where the variant does
not matter and say so.

## results decisions: 2026-09-07-the-measured-card-is-the-h100.md

# The measured card is the H100

Date: 2026-09-07. Status: decided by the owner (2026-09-07).

## Decision

Every campaign in the issue list runs on an H100 80 GB, and every constant
it produces names that card. The campaign issues were written for an H200;
they are run on the H100 as written, and the numbers the paper cites are the
H100's. An H200 number, if one is ever measured, is a second row labelled with
its card, never a replacement.

## Why

An H100 can be rented on demand; an H200 cannot. A measured number on the card
at hand outweighs a projected number for the card the issues named. The card
is recorded in every manifest as the machine reports it and in every constant,
so nothing in the record is ambiguous.

## Consequence

The `headline-c4096-second-card` campaign, which measured the H100 as the
second card against the H200, loses its object: the H100 is the card. It stays
open only for a memory probe of the pipelined loop at context 16,384, which the
archive estimated at 85 GB, until that loop has been tried on this card. The
cost model's cross-card ratios wait for a second card.

## results decisions: 2026-09-08-cost-per-proved-position-not-an-overhead-multiple.md

# The paper quotes cost per proved position, not an overhead multiple

Date: 2026-09-08. Status: decided by the owner (2026-09-08). Refines the
decision of the same day on the unproved baseline.

## Decision

The paper's cost claim is a cost per proved position: seconds per position at
the loop scope and at the whole wall-clock scope, and dollars per thousand positions
at the reference card rate. It does not quote a single "times slower" multiple
against an unproved baseline.

The unproved baseline is still measured, and in three numbers per point: the
prefill of the prompt on its own, the decode of the generated tokens on its
own, and the two end to end, each as positions per second over the positions
it covers. The reader multiplies the cost per proved position by their own mix
of prompt and generated positions and compares with the unproved cost of that
same mix.

## Why

Overhead is a property of the workload, not of the prover. The prover's cost is
the same per position whether the position was prompted or generated (about
78 million committed cells per position at context 4,096), while the unproved
cost differs by two orders of magnitude between a prefilled and a decoded
position. One prover on one card therefore looks a thousand times slower on a
prompt-heavy request and thirty times slower on a decode-heavy one. A single
multiple would be true only for one mix and would invite the argument about
which baseline it was taken against; a cost per position and a baseline in
its parts sidestep both.

## Consequence

The baseline driver records prefill, decode and end-to-end per point, in
positions per second over their own positions; none of the three is the
"overhead" denominator. The constants file carries `secs_per_position.*` and
`usd_per_1k_positions.*` as derived entries from the measured loop and
whole wall-clock rows and the reference card rate, and the export writes those for
the paper. The earlier decision's rule that the end-to-end figure counts the
prompt stands; its consequence that a prefill-only or decode-only baseline rate
is not recorded is replaced by this one.

## results decisions: 2026-09-08-the-unproved-baseline-is-end-to-end.md

# The unproved baseline is measured end to end

Date: 2026-09-08. Status: decided by the owner (2026-09-08).

## Decision

The unproved baseline that every "times slower" and every dollar-per-position
figure is stated against is measured over the same positions the proved rate
counts: the prompt's prefill and the 512 decoded tokens, as one wall-clock
time, in positions per second. A baseline rate that subtracts the prompt's time
is not recorded.

## Why

The decision of 2026-09-03 made every proved statement end to end: the measured
rows are 4,608 positions at context 4,096 and 16,896 at context 16,384, the
prompt included. The harness's like-for-like comparison was written when the
proved rate was decode-only and subtracts a one-token call from the baseline to
remove the prompt. Dividing an end-to-end proved rate by a decode-only baseline
rate compares two different quantities; the ratio would be wrong in the
paper's favour.

## Consequence

`unproved-baseline` measures prefill plus decode per point and records
positions per second; the prefill-subtraction path in the harness's comparison
is retired (zk-prover #74 and its follow-up issue), and the two constants that
described it (`scope.prefill_status`, `scope.sampling_status`) are not defined.

---

# Part 5. Working notes (HANDOFF.md), verbatim

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

---

# Part 6. Sources

- https://github.com/sg-ai-safety-hub/zk-inference-prover and https://github.com/sg-ai-safety-hub/zk-inference-results
- SASH research note: https://www.aisafety.sg/research/what-proving-llm-inference-actually-costs-research-note
- SASH ZKP introduction: https://www.aisafety.sg/blog/zkp-intro
- Study pages: ZK Inference Prover Flow (https://claude.ai/artifact/8F2qanpMugxKgX2eU9YZJE), Decode and Prove (https://claude.ai/artifact/Uec519WSekizajup7LUE3o), Tape to Polynomial (https://claude.ai/artifact/VJziCq1Q2kFgJ7bGHnUQnK)
