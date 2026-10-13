# Brief for Claude: a 3Blue1Brown-style video on how the zk-inference-prover works

Prepared 12 October 2026 from the public repositories `sg-ai-safety-hub/zk-inference-prover`
and `sg-ai-safety-hub/zk-inference-results` (author Pascal Berrang, Singapore AI Safety Hub,
485 commits between 19 August and 26 September 2026), their module docstrings, the results
repository's `constants.json`, and a real run of `unsloth/Llama-3.1-8B-Instruct` on an Apple
M4 Pro made on 7 October 2026 for the visuals. Every number below was read from those files
on 12 October 2026. Where a number carries a grade in brackets, that is the results
repository's own grade: **measured**, **derived**, **projected** or **asserted**.

---

## 0. How to use this file

1. Attach this whole file to a new conversation in the Claude desktop app.
2. Paste the short prompt in section 1 as your message.
3. Claude will return a script, a storyboard and a Manim program. Manim is the Python
   animation library Grant Sanderson wrote for 3Blue1Brown. Claude cannot render video
   itself, so you render it on your machine:

```
pip install manim            # needs Python 3.9+, ffmpeg; LaTeX only if the code uses MathTex
manim -pqh video.py Act1     # one scene; -pql for a fast low-quality preview
manim -pqh video.py          # every scene, then concatenate the mp4 files
```

4. If you would rather not install Manim, ask Claude for the same storyboard as a single
   self-contained HTML page with animated SVG and a narration track, and open it in a browser.
5. Record the narration yourself from the script, or feed the script to a text-to-speech tool,
   and lay it over the rendered scenes with any video editor.

---

## 1. The prompt to give Claude

> Using only the attached brief, write a 3Blue1Brown-style explainer video of 20 to 30 minutes
> on how the SASH zk-inference-prover proves that a language model really produced an answer.
> Deliver four things. (a) A narration script of about 3,600 words with a timestamp at every
> scene change, in plain words, one idea at a time, building each idea from a small concrete
> example before stating it in general. (b) A storyboard: for every scene, what is on screen,
> what moves, what is highlighted, and which line of narration it is synced to. (c) A complete
> Manim Community Edition program, one Scene class per act, that draws every scene in the
> storyboard, with the render commands. (d) A closing one-page list of what a viewer should be
> able to explain afterwards. Use only the facts, numbers and examples in the brief; quote the
> grade next to every number; invent nothing. Keep the seven honesty points of section 6 in the
> video. Follow the act structure and time budget of section 3 unless you have a clear reason
> to change it, and say so if you do.

### Style rules for the writer

- One idea per scene. Show the concrete case first (a 2 by 2 matrix, an eight-cell tape, three
  numbers in a table), then say the general rule in one sentence.
- Recurring visual characters: the **prover** in amber (it chooses values and commits), the
  **verifier** in teal (it holds no weights and no GPU), the **hash channel** as a grey box that
  swallows roots and spits out dice, the **challenge** as a yellow die, a **Merkle tree** as a
  blue triangle with a 32-byte root on top, and the **grid** of 290 proofs as a wall of tiles.
- Prefer a transform over a cut: a column of numbers becomes a curve, a curve becomes a tree,
  a tree becomes a root.
- Every "why" gets an "or else": what a dishonest prover could do if this step were missing.
- Plain words. Say "segment", "cell", "lookup", "seam", "root". The code's own identifiers
  appear once, in the glossary scene, and nowhere else.
- No claim stronger than the source. The proof is **not hiding**, nothing is **formally
  verified**, the arithmetic proved is a **quantised stand-in** for the model served.
- Narration pace about 150 words a minute: 20 minutes is 3,000 words, 30 minutes is 4,500.

---

## 2. The statement in one sentence, and the cast

**What is proved.** "For these published prompt token ids, under the model whose weight
commitment is this 32-byte root, greedy decoding in this fixed integer-and-bf16 arithmetic
produces these 512 token ids." Every layer of every position is proved, from the embedding row
to the argmax, for all 4,096 prompt positions and all 512 generated positions, 4,608 positions
in all [measured]. The verifier holds the prompt ids, the published model root and a small
per-layer calibration file. It holds no weights and needs no GPU.

**The cast.**

| Who | What they hold | What they do |
|---|---|---|
| the model publisher | the weights | commits them once as a Merkle tree and publishes the root (the "model root") |
| the prover (the provider running inference) | the weights, a GPU | reruns the decode in fixed arithmetic, keeps every intermediate value, turns each layer-by-block piece into a table, commits it, answers random challenges, writes a proof |
| the verifier (anyone) | the prompt ids, the model root, the calibration file, a CPU | checks each proof alone, then checks that the pieces fit together, then checks that each emitted id is the argmax the proof says it is |

**What is not inside the proof.** The text of the prompt (only ids are), the tokeniser and
chat template, the sampling rule a real server uses (the proof is greedy only), batching,
who was served and when, and the bf16 or fp8 kernels a real server runs (the proof covers a
quantised version of the model). Section 6 lists these honestly.

**Model.** Llama-3.1-8B-Instruct: hidden size 4,096; 32 layers; 32 query heads and 8 key/value
heads of 128 channels (four query heads share one key/value head); MLP width 14,336;
vocabulary 128,256; rotary position embedding with theta 500,000; RMSNorm epsilon 1e-5; no
projection bias. Weights per layer: q 16.8M, k 4.2M, v 4.2M, o 16.8M, gate 58.7M, up 58.7M,
down 58.7M, total 218M; embedding and output head 525M each; about 8.03B in all.

---

## 3. The story arc: seven acts, 20 to 30 minutes

Minutes are a budget, not a cage. The short end of each range gives a 20-minute video, the long
end 30.

### Act 1. The question (2 to 3 min)

**Goal.** Make the viewer want a receipt for a computation.

- Scene 1.1. A prompt goes into a box labelled "8 billion numbers". Out comes " a city of
  romance". (That is the real greedy continuation of "The capital of France is" on this model
  without a chat template; the top two scores at the first step were " a" at 16 and " Paris" at
  15.938, so the model nearly said Paris.) Question on screen: how would you know this box ran
  the model it claims, on your prompt, without rerunning it yourself and without seeing its
  weights?
- Scene 1.2. The three things a receipt must do: fix the input (the ids), fix the machine (the
  weights, behind a commitment), and make every step checkable. Show the cast of section 2.
- Scene 1.3. The shape of the answer, in one line: "rerun the model in arithmetic that can be
  written as rules, write every intermediate value into tables, commit the tables, then let a
  random audit check the rules." The rest of the video unpacks that line.
- Scene 1.4. The honest frame, early: the word "ZK" here names the proof-system family. The
  proof does not hide anything except the weights behind their root. Say it now so the viewer
  never expects privacy.

### Act 2. Inside the model, rerun in fixed arithmetic (4 to 6 min)

**Goal.** The viewer sees one transformer layer as a short list of operations, each on
integers or 16-bit floats, so that "write every step as a rule" sounds possible.

- Scene 2.1. One token's journey through one layer, left to right, as the residual stream: norm
  1, requantise to int8, three matmuls (q, k, v), dequantise to bf16, rotate (RoPE) and
  quantise q and k, attention, attention output rounded to a 12-bit integer, the o matmul,
  dequantise, add to the stream, norm 2, requantise, gate and up matmuls, SwiGLU, requantise,
  down matmul, dequantise, add to the stream. Then 31 more layers, the final norm, the head
  matmul to 128,256 scores, the argmax.
- Scene 2.2. Why fixed arithmetic. A floating-point kernel on a GPU adds numbers in an order
  nobody wrote down. A proof needs every operation to be a rule with one right answer. So the
  harness reruns the model in a fixed quantisation named `y-delay-vw12`: int8 activations with
  one scale per token, int8 weights with one scale per output channel, exact integer sums, a
  chain of correctly rounded bf16 steps for dequantisation (round half to even), bf16
  nonlinearities, an integer softmax (queries 12 bits, keys 11 bits, a 9-bit numerator read from
  an exp table), the attention output rounded straight to a 12-bit integer with a power-of-two
  scale, and the value projection's requantisation delayed to where it is consumed.
- Scene 2.3. The price of that arithmetic, measured on the same 20,440 scored tokens: fp32
  perplexity 4.408 [measured], the proved configuration 4.715 [measured], a cost of +6.96 %
  [measured]. For contrast, naive static per-tensor int8 scores 65.99 [measured], +1,397 %. Task
  scores unchanged within error.
- Scene 2.4. A real requantisation, with real numbers from the 7 October run on "The capital of
  France is", last token, layer 0, norm-1 output: the largest magnitude was 4.03125; divided
  by 127 that is 0.03174, and rounded up to the next bf16 it is 0.031982421875. (The study's
  own script recorded the bf16 just below, 0.03173828125, because its helper rounded to nearest
  instead of up; the int8 values are the same under either scale.) The first eight values
  [-0.0171, 0.0201, 0.0152, 0.0093, -0.3203, -0.0099, 0, 0.0022] become the int8s
  [-1, 1, 0, 0, -10, 0, 0, 0]. The first eight weights of row 0 of W_q
  [0.00516, -0.0293, -0.00644, -0.01819, -0.00327, 0.02637, -0.0007, -0.0023] with the channel
  scale 0.00045 become [11, -65, -14, -40, -7, 59, -2, -5]. Animate the scaling and rounding.
- Scene 2.5. The witness. Everything a rule will later read is kept rather than thrown away:
  int8 activations, exact accumulators, bf16 bit patterns, attention scores, keys and values,
  the residual stream in and out of each layer. Dumped per layer and per block of 512
  positions. Show the residual-stream RMS growing through the 32 layers on the real prompt:
  0.006 after the embedding, 0.145 after layer 14, 0.835 after layer 31, 2.176 after the final
  norm, as a rising bar chart.
- Scene 2.6. Grouped attention, one picture: at layer 31, head 0, the last prompt token " is"
  attends 0.5117 to itself and 0.1953 to " France" (real numbers), and at layer 0 the same head
  attends mostly to the begin-of-text marker (0.4629). Attention is the one operation whose cost
  grows with the context, which matters in Act 7.

### Act 3. From a table to a polynomial: a STARK in one toy (5 to 7 min)

**Goal.** The viewer understands why "commit a table, then audit it at random points" catches
any wrong cell, using an eight-cell Fibonacci tape. This is the one piece of cryptography the
video must teach, and it should be taught slowly.

- Scene 3.1. The tape. Eight cells: 1, 1, 2, 3, 5, 8, 13, 21. The rule: each cell is the sum of
  the two before it. A computation is a tape plus a rule that every hop obeys.
- Scene 3.2. Through any N points there is exactly one polynomial of degree below N. Put the
  eight cells at eight fixed positions and draw the unique degree-7 curve through them. The
  tape became a curve: P.
- Scene 3.3. Apply the rule to the curve. C(x) = P(next-next x) − P(next x) − P(x). At the six
  positions where the rule applies, C is zero. Six separate facts about cells become one
  statement about a curve.
- Scene 3.4. Division. A polynomial that is zero at six known points is divisible by Z(x), the
  polynomial whose roots are exactly those six points. So C = Z times some quotient Q, and the
  prover can compute Q. If one cell is wrong, C is not zero at that point, the division leaves a
  remainder, and "Q" is not a polynomial at all.
- Scene 3.5. The audit. The verifier picks a random position r far outside the tape and asks
  for P and Q there, then checks C(r) = Z(r) times Q(r). Two different low-degree polynomials
  agree at very few points, so a lie survives one random question only with probability about
  degree over field size. Say the field: the prime p = 2^31 − 1 (Mersenne 31, "M31"), and for
  the challenges a four-fold extension of it with about 2^124 elements.
- Scene 3.6. Commitment. The prover cannot answer the audit by inventing P after seeing r. It
  first evaluates P on a bigger domain (twice as many points as the table: blowup 2) and hashes
  those evaluations into a Merkle tree. The tree's root is published before r is drawn. Later it
  opens the requested leaves with their hash paths. Show the tree, the 32-byte root, and the
  opening of one leaf.
- Scene 3.7. The low-degree test. The verifier also needs to know that the committed
  evaluations really come from a low-degree polynomial, not from a pointwise cheat that happens
  to pass at r. FRI does that by repeatedly folding the polynomial in half and committing each
  half. Treat FRI as a black box with the right interface: "a committed list is low-degree, with
  100 random queries". This system uses blowup 2, 100 queries and no proof-of-work, which
  stwo's accounting calls 100 conjectured bits of security [asserted in `prover/src/util.rs`].
- Scene 3.8. Fiat–Shamir. There is no live verifier at proving time. The prover feeds every
  root into a hash (Blake2s) and the "random" r is the hash output. Because the root goes in
  first, the prover cannot fit the values to the randomness. On screen: the hash channel box
  eats a root, emits a die. This exact picture returns in Act 4.
- Scene 3.9. Scale up in one cut: the Fibonacci tape has one column and one rule; a layer
  segment has thousands of columns and hundreds of rules (an "AIR", algebraic intermediate
  representation), and the field element in one column at one row is called a **cell**. A
  single proof here commits about 1.25 billion fresh cells (363.9 billion over 290 proofs, measured; the division is derived).

### Act 4. One segment, one proof: five trees, one hash channel (5 to 7 min)

**Goal.** The viewer can narrate the order of events in one segment proof and say why the
order matters.

- Scene 4.1. The unit. A **segment** is one transformer layer (or the output head) applied to
  one block of S = 512 positions against a context of C earlier positions, proved as one STARK.
  The request is a grid of them: 9 token blocks (8 prompt blocks of 512, one generated block of
  512) times 32 layers, plus the head proved twice, 290 proofs [measured]. There is no
  recursion. Hold the grid picture; Act 6 chains it.
- Scene 4.2. The five kinds of tree in one segment, drawn as five blue triangles in commit
  order:
  - **Tree 0, the shape tree.** Everything the rules read as a fact: selectors, the causal mask,
    the marker for which key rows are real, the lookup tables (exp, the bf16 NORM, FRAC and
    POW tables, the range tables), the rotation angles for this block's absolute positions. It
    is a pure function of the public parameters plus a per-layer calibration file, so the
    verifier rebuilds it and rejects on a root mismatch. No weight is in it.
  - **Tree 1, the model tree.** This layer's int8 weights and per-channel scales, and on the
    segments that need them the embedding matrix and the output head. The verifier cannot
    derive it; it compares the root with the publisher's manifest. Built once per layer and
    cached on the device.
  - **Tree 2, the base trace.** Everything the prover chose for this segment: int8 activations,
    accumulators, bf16 patterns of the residual stream, attention scores and numerators, the
    rotated and quantised q, k, v, the token ids, and the multiplicity column of every lookup
    table. This is where most cells live.
  - **Tree 3, the interaction tree.** The lookup bookkeeping (Act 5) that depends on the random
    challenges, so it can only be committed after they are drawn.
  - **Trees 4 and up, the boundary trees.** The residual stream in, the residual stream out,
    and the keys and values this block wrote. Small trees whose only job is to be compared with
    a neighbouring segment's trees (Act 6).
- Scene 4.3. The transcript, as a vertical timeline with the hash channel on the side:
  1. commit trees 0, 1, 2; mix each root into the Blake2s channel;
  2. draw the challenges: a pair (z, alpha) per lookup table, the Horner weights r, s, rv that
     fold whole matrices into one field element, and the binding pair for the residual-stream
     claims;
  3. build every lookup fraction and running sum; run five GKR sumchecks (one each for the key
     tiles, the dequant, the residual stream, the Freivalds checks and the attention output);
     commit tree 3;
  4. commit the boundary trees (they are tied to base columns by plain equality rules checked
     at the out-of-domain point, which is why they may come after tree 3);
  5. stwo draws the out-of-domain point, evaluates every rule's quotient there (generated CUDA
     kernels do this), commits the composition polynomial, runs FRI;
  6. serialise three documents: Fixed (the statement: shapes, parameters, security config, the
     two preprocessed roots), Claims (every published sum and fold), Proof (about 65 MiB).
- Scene 4.4. Why the order is the whole argument. Rewind the timeline and show the attack: if
  the prover knew a challenge before committing, it could choose values that pass that one
  challenge. Every root goes in before the die that depends on it comes out. The serialised
  byte order is therefore load-bearing, and the SHA-256 of the proof bytes is what the project
  calls the digest gate: a change that should not alter the proof must reproduce the recorded
  digest on both the CPU and the GPU backend before it merges.
- Scene 4.5. A bf16 number as two cells. Every constraint must stay at low degree because the
  blowup is only 2. So a bf16 value is not stored as a 16-bit pattern but as two field cells:
  a signed significand sm in {0} or ±[128, 256) and an exponent field ef in [1, 255), with value
  sm · 2^(ef − 134), and "is zero" is simply sm = 0. Show 1.5 = 192 · 2^(127 − 134).
- Scene 4.6. How much. Fresh cells committed per position at context 4,096: base trace 58.5M,
  interaction 17.8M, boundary 2.6M, about 79.0M in all [measured]; plus 22.9M model and 4.5M
  shape cells that are preprocessed and cached, not paid per segment [measured]. At context
  16,384 the fresh total is about 105M per position [measured].

### Act 5. The three tricks inside the table (6 to 8 min)

**Goal.** The viewer can derive Freivalds on a whiteboard, explain a lookup as balancing
fractions, and say what a seam is.

**Trick 1: matmuls by Freivalds, not cell by cell.**

- Scene 5.1. The problem. One layer has seven matmuls over 218M weights. Writing "this output
  cell equals this dot product" for every output cell is hopeless.
- Scene 5.2. The toy. W = [[1, 2], [3, 4]], X = [1, 1]ᵀ, so Y = W X = [3, 7]ᵀ. A prover claims
  Y' = [3, 8]ᵀ. The verifier draws a random vector r = (r1, r2) after Y' is committed and checks
  rᵀ Y' = (rᵀ W) X. Left side 3 r1 + 8 r2. Right side (r1 + 3 r2, 2 r1 + 4 r2) · (1, 1) =
  3 r1 + 7 r2. They differ unless r2 = 0, which a random r2 hits with probability 1 in p.
- Scene 5.3. The general rule. Checking rᵀ(W X) = (rᵀ W) X at a random r costs one pass over
  the weights, linear instead of cubic, and a wrong Y passes with probability about degree over
  2^124. In the code the random vector is powers of challenges: per input channel k the
  Freivalds gadget folds v = Σ_t s^t · X[k, t] and, per matmul m, u_m = Σ_i rv^i · W_m[i, k],
  and accumulates acc_m += u_m · v; the dequant gadget folds the same committed accumulators the
  other way, h_m = Σ_{t,i} s^t rv^i · acc[t, i]; the verifier requires acc_m = h_m. Nothing is
  committed twice: the accumulators the matmul check reads are the ones the rounding gadget
  rounds.
- Scene 5.4. Weights are preprocessed. The W side comes from tree 1, the model tree, so the
  proof is about the committed model and nobody else's.

**Trick 2: lookups by LogUp, the balancing of fractions.**

- Scene 5.5. The problem. Many steps are not polynomial rules: "this bf16 is the correctly
  rounded result", "this 9-bit numerator is exp of this score", "this value is below 2^15".
  Each is a table membership: the row I used must be a row of a table that was committed
  before any challenge.
- Scene 5.6. The toy. Table {1, 2, 3}. Uses [2, 2, 3]. The prover commits a multiplicity per
  table row: (0, 2, 1). After a random z is drawn, both sides form fractions:
  uses: 1/(z − 2) + 1/(z − 2) + 1/(z − 3); table: 0/(z − 1) + 2/(z − 2) + 1/(z − 3). They are
  equal for every z. Now a cheating use of 4 adds 1/(z − 4), a pole no multiplicity over
  {1, 2, 3} can cancel, so the two sums differ at every z but a vanishing few.
- Scene 5.7. Multi-column rows are first folded into one number with a second challenge alpha,
  combine(row) = Σ alpha^i · col_i, and then the same fractions are formed. The running sums of
  those fractions are the interaction columns of tree 3. Cost rule, worth saying on screen: a
  table row costs one multiplicity cell plus one fraction cell in the extension field, which is
  four base cells, five cells a row. A range table with 2^20 rows costs five times 2^20 cells
  even when few rows are used.
- Scene 5.8. Where the tables come from and what they prove, as a quick montage:
  - **NORM and FRAC** (the dequant): |acc| = M2 · ph + r with M2 in [256, 512) and ph a power of
    two; NORM(M2, ph, sticky) gives the correctly rounded bf16 (m7, ef, nz) and FRAC(ph, r,
    sticky) proves r < ph and the sticky bit, in one lookup each. The decomposition is injective
    below 2^(kmax + 9) < p, so a prover cannot use the field's wraparound to fake a rounding.
  - **The unary tables**: rsqrt and silu are tables of all 65,536 bf16 inputs with their
    correctly rounded outputs.
  - **The exp table** of the integer softmax: committed score shift d = row max − score, the
    pair (d, numerator) must be a row of the table; the numerator is 9 bits.
  - **The range tables**: int8 activations, the requantise's pattern differences in [0, 2^15),
    the attention output's remainder and denominator.
  - **The embedding table**: the whole 128,256 by 4,096 matrix is a table in tree 1; a layer-0
    segment's use rows (token id, a block of channels) must be a sub-multiset of it, and a
    Horner fold over those channels must equal the layer's stream-in claim. Selecting one row
    of a committed table by a committed index costs a pass over the table, and almost all of
    that pass is preprocessed.
- Scene 5.9. GKR, in one sentence. The running sums for the five biggest lookup families are
  not committed as columns; a sumcheck protocol proves them and a link ties its final claim
  back to the committed columns. Effect: at context 16,384 the interaction tree is 5,600 columns
  instead of 93,184. This is 41.8 % of loop time [measured], the largest phase.

**Trick 3: seams and bindings, so the gadgets talk about the same numbers.**

- Scene 5.10. The problem. Each gadget proves its own step correctly. Without a link, the
  prover could feed the matmul one input and the norm another, and each proof would be true
  about the wrong numbers.
- Scene 5.11. A Horner claim. Under a challenge w drawn after commitment, a gadget publishes
  one number, Σ_q w^(N−1−q) · value_q, over the values it produced; the next gadget publishes
  the same sum over the values it consumed; the verifier compares the two numbers. Equal sums
  under a random weight mean equal sequences, position by position. About half a cell per
  value, and the values are committed once.
- Scene 5.12. The 16 edges of a layer segment, as a ring around the layer diagram from Act 2.
  Seven are residual-stream bindings (the two norms read the committed stream, the dequant
  outputs are what the adds and the SwiGLU read, the rotated q, k, v are what attention reads,
  the attention output is what the o matmul reads), three are **seams** (a requantise step between a bf16 producer and an int8 consumer, proved
  on its own so the matmul multiplies exactly the integers the producer made: into q/k/v, into
  gate/up, into down), one is the attention component itself, one is the Freivalds check
  itself, and two are the boundaries (residual stream to the next layer, keys and values to the
  next block). That is 14; layer 0 adds the embedding edge and the head adds the argmax edge,
  which makes the 16 of the binding table.
- Scene 5.13. The requantise seam, in detail, because it is the one most often skipped in
  explanations: committed per token are the max's magnitude pattern pm, a selector bit per
  element, the scale and the int8 values; pm − pattern_i is range-checked for every element and
  the selector pins pm to an attained value; (pm, scale) is one lookup into the table
  bf16_ceil(v / 127); for each nonzero q one lookup into a division table proves q is the
  rounding of x / scale, and for q = 0 one range lookup proves |x| < scale / 2; and three Horner
  folds close the seam to its producer and its consumer.
- Scene 5.14. The argmax edge. Greedy decoding takes the first maximal index. Committed: the
  maximum's pattern pm, a monotone indicator b_i = [i < tok], the token. Range-check
  pm − k_i − b_i ≥ 0 for every vocabulary entry: strictly below the max before tok, at most the
  max from tok on; b_i is 0/1, non-increasing, and Σ b_i = tok, which is the binding itself. On
  the real continuations 15 of 512 positions at context 4,096 have two or three equal top
  logits, so the strict form is not academic: a lax proof would let the prover pick the token
  on those rows. The lax form exists only as a flagged control.
- Scene 5.15. Every binding is on by default; a witness that cannot state one is refused. A
  flag named `--unsound-skip-<edge>` turns one off loudly, the run's provenance lists it and
  the binding table marks the edge unbound; such a run is a control, never a result.

### Act 6. The grid: 290 proofs chained by roots, and the verifier (3 to 4 min)

**Goal.** The viewer sees why there is no recursion and what the verifier actually does.

- Scene 6.1. The wall of tiles: columns are token blocks B0 to B8, rows are layers L0 to L31,
  plus two head tiles over B7 and B8 (the first generated token's argmax was computed at the
  last prompt position). Vertical arrows: the residual-stream root leaving a tile must equal
  the residual-stream root entering the tile above, 281 layer links. Horizontal arrows: the
  keys and values a block wrote must equal the key/value prefix the next block attended over,
  256 token links. 537 links in all [measured]. Layer 0 also binds the embedding row; the head
  binds the emitted id.
- Scene 6.2. Why a root and not a challenge. Each tile's internal claims are taken under a
  challenge drawn inside that tile, so two tiles weigh their boundaries differently and the
  claims cannot be compared. Drawing the challenge from public data so both tiles share it is
  unsound: a challenge known before the values are committed makes "my image equals yours" one
  linear equation the prover can solve. So the exposed value is a Merkle root of the boundary
  values themselves, bound to the base columns by a plain equality rule; the link check is five
  integer comparisons that pin the layout, then one 32-byte root equality. Constant time, no
  recursion anywhere.
- Scene 6.3. Attention across blocks. Block b's queries attend to the keys of blocks 0 to b;
  the context C grows by 512 per block. The key/value boundary root is what ties "the keys I
  attended over" to "the keys the previous block actually wrote".
- Scene 6.4. The verifier, one tile at a time, as a checklist that fills in: parse Fixed,
  Claims, Proof; refuse if the claim shapes do not match the plan or the security parameters
  drifted; replay the hash channel and re-draw every challenge; verify the GKR sumchecks; run
  the STARK verifier (out-of-domain sampling and FRI); check that every lookup's fractions
  cancel; check every Freivalds equality, the attention and denominator identities, and every
  binding equality; rebuild the shape tree from the public parameters and the calibration and
  compare its root with the declared one; compare the model root with the published manifest.
  Then the grid: every link, then every id chained to the prompt or to a proved argmax.
- Scene 6.5. Verification cost. Over the 290 proofs the verifier's own time on the run host's
  CPU cores was 119 s, a median of 0.41 s per segment [measured]. On a consumer-class machine
  with four cores and no card, one reference segment at context 16,384 took 43.2 s, of which
  42.25 s was deriving the shape root and 0.92 s was checking the proof itself, at a peak of
  28.5 GiB of memory [measured]. The shape tree is the verifier's main cost, and a grid pays it
  once per (layer, context) shape, not once per proof.

### Act 7. The numbers, the honesty, and what is next (3 to 4 min)

**Goal.** Leave the viewer with accurate magnitudes and an accurate sense of what this
prototype is and is not.

- Scene 7.1. One request, one H100, 4,096 prompt + 512 generated:

| Quantity | Value | Grade |
|---|---|---|
| segments | 290 | measured |
| proving loop | 3,683 s (61 min) | measured |
| whole wall, extraction included | 5,485 s (91 min) | measured |
| throughput | 1.25 positions/s in the loop; 0.84 whole wall | derived |
| cost at 3.29 USD per GPU-hour | 0.73 to 1.09 USD per 1,000 positions, so 3.37 to 5.01 USD per request | derived |
| unproved serving (vLLM, one request at a time) | 42,231 prompt positions/s, 153 generated/s, 1,342 end to end | measured |
| overhead | about 1,070 times against the proving loop (1,342 / 1.25) and about 1,600 times against the whole wall (1,342 / 0.84) | derived here from the two measured rates |
| proof size | 18.46 GiB serialised for the 290 proofs (7.19 GiB before serialisation); median segment 64.97 MiB, range 48.4 to 120.0 MiB | measured |
| cells per position, fresh | about 79.0M (base 58.5M, interaction 17.8M, boundary 2.6M) | measured |
| context 16,384 | 1,058 segments; loop 21,586 s (6.0 h); 0.78 positions/s; about 105M fresh cells per position; 108.9 GiB of proofs | measured, derived |

- Scene 7.2. Where the time goes, from a serial loop over 32 layer segments (748 s) [measured]:
  lookup interaction columns and GKR 41.8 %, base trace 35.4 %, load, decode, check and build
  11.8 %, other host work 6.4 %, the STARK commit and prove 4.6 %. Animate as a stacked bar.
  The STARK is the cheap part; building the tables on the host is the ceiling (issue #2). With
  the constraint kernels left on the CPU the same loop took 4,737 s [measured], so moving
  constraint evaluation to the GPU is already done.
- Scene 7.3. Projections, clearly labelled as the results repository's cost model and not
  measurements: a 70B model in the order of 5 to 8 hours per request, 405B 16 to 24 hours, a
  1T dense model 32 to 48 hours [projected]. These hours are derived here from the cost
  model's projected cost per million positions (70B: 3,640 USD in the loop, 5,420 whole wall;
  405B: 11,586 and 17,254; 1T dense: 23,122 and 34,433) at 3.29 USD per GPU-hour and 4,608
  positions per request. Show them in a lighter colour than the measured bars.
- Scene 7.4. The seven honesty points of section 6, each as one line that stays on screen.
- Scene 7.5. What SASH says is next, in their own framing: prover optimisation (host witness
  generation to the GPU; the commitment alone could run far faster than the loop), real 70B
  and 405B runs, closing the gap to real serving (bf16 or fp8 arithmetic, tokenisation,
  non-determinism, batching, binding to traffic records), proving a random sample of segments
  after the provider commits to boundary roots, and restructuring into small auditable gadgets.
  Their sampling argument: prove a random fraction p of requests; a provider cheating m times
  escapes with probability (1 − p)^m; at p = 1 % about 460 cheats before 99 % detection.
- Scene 7.6. Close on the one-sentence statement from section 2, now fully unpacked, and the
  list of what the viewer can explain.

---

## 4. Reference facts for the writer

### 4.1 The seven stages a run executes, in order

1. **Generate the ids** (Python, GPU). Take a 4,096-token prompt from the fixed corpus, run the
   quantised model greedily for 512 new tokens, write prompt followed by continuation. This
   decode is itself the thing being proved; greedy means argmax, so each emitted token is a
   deterministic function of the logits.
2. **Extract the witness** (Python, GPU). Rerun the forward pass in explicit fixed arithmetic,
   every operation written out, and dump per layer and per 512-position block every value a
   rule will read. Layer 0 also dumps the embedding rows. The most expensive host step.
3. **Shape table and plan file** (Python, CPU). Read every dump's manifest, compute the
   model-wide worst case for the parameters every segment must share (the widths of the
   lookup windows; the code calls them pins), refuse early if a layer would not fit the field's
   31 bits, and write one plan line per segment: 290 lines.
4. **Emit and install CUDA kernels** (Rust, once per shape). For each distinct constraint shape,
   lower the rules to straight-line code, check that lowering against the CPU evaluator on
   random data, generate the kernels and rebuild. Without them the GPU build still works but
   evaluates constraints on the CPU; the proof bytes are the same either way.
5. **Commit the model** (Rust, once per model). For every (layer, context) shape build only
   the preprocessed trees and read off two roots: the shape root (anyone can recompute it) and
   the model root (only the publisher can make it, anyone can compare against it). The manifest
   also carries the per-layer attention calibration the verifier needs.
6. **Prove every segment** (Rust, GPU, the loop). One process per slice of plan lines,
   pipelined so segment k + 1 is generated while segment k is proved. Per segment: load and
   decode the dump, build every gadget's columns, commit the trees, draw challenges, build the
   lookup columns and run the five GKR sumchecks, commit the boundary trees, STARK prove,
   serialise three files.
7. **Verify and chain** (Rust, CPU only). For each segment replay the transcript, rebuild the
   shape tree and compare roots, compare the model root with the manifest, run the STARK
   verifier, check every application identity. Then every link, then every id. A gate script
   then refuses the run if any segment lists a skip flag, any edge is unbound, any kernel fell
   back to the CPU, or any link failed. Only then does the run become a row in the constants.

### 4.2 The proof system, precisely

- Circle STARK over the Mersenne prime p = 2^31 − 1 (M31), using StarkWare's stwo library in a
  vendored fork (NitrooZK-stwo) with a CUDA backend. Challenges and lookup fractions live in
  QM31, the degree-4 extension, about 2^124 elements.
- Merkle trees hashed with Blake2s; the same hash drives the Fiat–Shamir channel.
- FRI with log blowup 1 (blowup factor 2), 100 queries, 0 proof-of-work bits, which stwo's
  accounting (pow_bits + log_blowup × n_queries) reports as 100 conjectured bits. The code
  asserts this value and refuses to run if it drifts.
- Two backends, one cargo feature: SIMD on the CPU (the reference every digest is compared
  against) and CUDA. Both share witness and trace construction, the hash channel and the
  serialisation, so the proof bytes must be identical.
- Not zero-knowledge in the hiding sense: no random blinding is added to the committed trace.
  The weights are hidden only behind the model root. The public parameters reveal the
  architecture.
- Lookups by LogUp. Matmuls by Freivalds. Five GKR sumcheck reductions replace the committed
  running sums of the five largest lookup families.

### 4.3 The 18 decode steps and how each is proved (condensed)

| # | Step | The model does | The proof does |
|---|---|---|---|
| 0 | prompt | text arrives | nothing is committed; text never enters a proof |
| 1 | tokenise | 128,256-piece dictionary, start marker 128000 first | ids are the public input; every layer-0 segment commits them in the base trace; the verifier is handed the same ids |
| 2 | embed | each id selects one row of a 128,256 by 4,096 table | table in tree 1 (525M preprocessed cells); use rows per (token, channel block); LogUp sub-multiset; Horner fold equals the stream-in claim |
| 3 | norm 1 | RMSNorm: mean of squares, epsilon, reciprocal square root, gain | bf16 square and balanced tree sum by the bf16 multiply and add gadgets; rsqrt one 65,536-entry table; the reduction's roots published and bound |
| 4 | requantise | one scale per token, divide, round to int8 | the seam of scene 5.13 |
| 5 | q, k, v matmuls | three exact integer matmuls, 4,096 to 4,096, 1,024, 1,024 | Freivalds against tree-1 weights, one shared input fold; int8 inputs range-checked |
| 6 | dequantise | accumulator times token scale times weight scale, three roundings | NORM and FRAC lookups per rounding; power-of-two scales collapse to one |
| 7 | RoPE + quantise | rotate channel pairs by position angles; round q, k, v to 12, 11, 8 bits | angles preprocessed in tree 0 per absolute position; rotation as bf16 multiply and add; quantise with a preprocessed power-of-two scale; bound in against the dequant outputs and out against the key tiles |
| 8 | attention | integer scores, causal mask, subtract row max, exp table to 9-bit numerators, sum | per key tile commit scores, the shift d = max − score, numerators, sums; mask and real-row marker from tree 0; exp table lookups; Q·Kᵀ and A·V exact identities; GKR for the running sums |
| 9 | attention out | weighted sum of values per head, one rounding to 12 bits | commit acc = A·V, the denominator, quotient, remainder, result; rounding identity in a 31-bit window; denominator range-checked; this is also the o matmul's input seam |
| 10 | o + residual | one matmul, add to the stream | Freivalds and dequant again; the add proved on the same rows as norm 1 so the stream is committed once |
| 11 | MLP + residual | norm, requantise, gate and up, SwiGLU, requantise, down, add | two more seams; silu one unary table; the SwiGLU product one bf16 multiply; second add |
| 12 | segment proof | the layer's output goes on; K, V go to the cache | the transcript of scene 4.3 |
| 13 | layers 1 to 31 | the same 31 more times | each its own segment; shape tree cached per (layer, shape), model tree per layer; residual roots compared |
| 14 | head | final norm, one matmul to 128,256 logits | its own segment; the head matrix in tree 1 (about 570M preprocessed cells); one requantise seam; power-of-two dequant |
| 15 | argmax | highest score, lowest index on a tie | scene 5.14 |
| 16 | next tokens | append the id, run again for the new position | a generated position is one more row of the same block; the grid check chains ids to proved argmaxes; earlier keys and values enter as a boundary root |
| 17 | verify | | scene 6.4 |

### 4.4 Attention in integers, the piece most worth drawing carefully

- Queries are quantised to 12 bits, keys to 11, with power-of-two scales and one query scale
  per head. Scores are exact integer dot products over 128 channels.
- Because Q·Kᵀ reduces over the channel axis and A·V reduces over the key axis, the two inner
  products want different row layouts, and the (token, key) grid can live in only one of them.
  It lives in the key-major one. The price is that the row maximum, a per-token value, is not
  in a key-major row; so the prover commits d[t, c] = max_t − score[t, c] instead of the score,
  and the Q·Kᵀ identity absorbs the shift.
- The exp table maps the shifted score to a 9-bit numerator n; the denominator Z is the sum of
  the row's numerators. Numerators are range-checked; (shift, numerator) pairs are table
  lookups.
- Heads are packed onto one column set in "key tiles"; packing costs no extra committed column
  because the Horner fold already aggregates instances by public powers of the same challenge.
- The attention output acc = Σ n · v is divided by Z and rounded straight to a 12-bit integer.
  The rounding identity needs the denominator pinned: it is range-checked on its own, which is
  what closed a historical hole where a rounding by an unpinned denominator was accepted.

### 4.5 The 16 edges of a layer segment, from `docs/statement.md`

1 residual stream into norm 1's reduction; 2 norm 1's output into the q, k, v matmul inputs
(seam); 3 q, k, v outputs into attention; 4 attention scores and values into the attention
output (the component itself); 5 attention output into the o matmul input; 6 o output into the
first residual add; 7 first add into norm 2's reduction; 8 norm 2's output into gate and up
inputs (seam); 9 gate and up outputs into the SwiGLU product; 10 SwiGLU output into the down
input (seam); 11 down output into the second add; 12 each matmul's input times the pinned
weights into its accumulator (the Freivalds check itself); 13 residual stream out into the
next layer's segment; 14 keys and values out of this block into the next block; 15 embedding
row into the first segment's residual stream (layer 0 only); 16 logits into the emitted token
(head only). A head segment has no attention or MLP of its own, so edges 3 to 11 and 14 are
absent there.

### 4.6 Worked toy examples, ready to animate

**Freivalds (scene 5.2).** W = [[1, 2], [3, 4]]; X = (1, 1); honest Y = (3, 7); claimed
Y' = (3, 8). rᵀY' = 3 r1 + 8 r2; (rᵀW) X = 3 r1 + 7 r2. Difference r2. Random r2 is zero with
probability 1/p. In practice r = (1, r, r², …), powers of one challenge, so the check is a
polynomial identity in r and a lie survives with probability at most its degree over the field
size.

**LogUp (scene 5.6).** Table (1, 2, 3); uses (2, 2, 3); multiplicities (0, 2, 1).
Σ_uses 1/(z − u) = 2/(z − 2) + 1/(z − 3). Σ_table m/(z − t) = 2/(z − 2) + 1/(z − 3). Equal.
Cheat: uses (2, 2, 4) give 1/(z − 2) + 1/(z − 2) + 1/(z − 4); the pole at 4 cannot be matched.

**Range check (scene 5.8).** "v is below 2^15" is the lookup "v is a row of the table
0, 1, …, 2^15 − 1". The table costs five cells a row (one multiplicity plus one extension-field
fraction) whether or not every row is used. Issue #13 of the repository was a counting bug
where the harness assumed each dump's own window width while the proof used the model-wide
worst case, so counts came out short by five cells a row; it is a nice aside on how concrete
"five cells a row" is, but it is optional for the video.

**bf16 as two cells (scene 4.5).** 1.5 = 1.1₂ × 2^0: significand 192 (128 + 64), exponent field
127, value 192 · 2^(127 − 134) = 192 / 128 = 1.5. Zero is sm = 0.

**Fibonacci tape (Act 3).** Tape 1, 1, 2, 3, 5, 8, 13, 21 at positions x0 … x7. P interpolates.
C(x) = P(x_{i+2}) − P(x_{i+1}) − P(x_i) is zero for i = 0 … 5. Z(x) = Π_{i=0..5} (x − x_i).
Q = C / Z. A wrong cell, say 13 → 14, makes C(x_4) = 14 − 8 − 5 = 1 ≠ 0, so Z does not divide C.

**The real requantisation (scene 2.4).** See the numbers in Act 2; the rule is scale =
bf16_ceil(max |x| / 127), q = round(x / scale) with |q| ≤ 127.

### 4.7 Real run data for the visuals (7 October 2026, bf16 on an Apple M4 Pro, greedy, no chat template)

- "The capital of France is": ids [128000, 791, 6864, 315, 9822, 374]; continuation
  [264, 3363, 315, 30363] = " a city of romance". Step-0 top five: " a" 16, " Paris" 15.938,
  " known" 15.062, " home" 14.875, " the" 14.312. Residual RMS after the embedding and each
  layer: 0.006, 0.013, 0.022, 0.031, 0.051, 0.064, 0.07, 0.086, 0.091, 0.099, 0.111, 0.116,
  0.12, 0.137, 0.145, 0.154, 0.169, 0.198, 0.221, 0.243, 0.273, 0.305, 0.343, 0.383, 0.424,
  0.466, 0.512, 0.557, 0.609, 0.671, 0.747, 0.835, 2.176. Attention of " is" at layer 0 head 0:
  begin-of-text 0.4629, "The" 0.2188, " capital" 0.0859, " of" 0.1602, " France" 0.0459, " is"
  0.0261; at layer 31 head 0: begin-of-text 0.2539, "The" 0.0083, " capital" 0.0168, " of"
  0.015, " France" 0.1953, " is" 0.5117.
- "2 + 2 =": ids [128000, 17, 489, 220, 17, 284]; continuation " 4. This"; step-1 top five
  "4" 18.375, "5" 16.125, "6" 15.125, "3" 14.688, "8" 14.375.
- "Roses are red, violets are": continuation " blue, and the"; step-0 top five " blue" 20.5,
  " purple" 15.75, " green" 14.875, " too" 14.812, " violet" 14.5.
- These numbers are from a bf16 run of the public model, not from a witness dump; the int8
  values in scene 2.4 apply the harness's rule to that run's layer-0 norm output. The run's
  data file records the scale as 0.03173828125 because the script's rounding helper rounded
  to the nearest bf16 rather than up; the correct ceiling is 0.031982421875, and the eight
  int8 values are the same under both.

### 4.8 Why the harness reruns the model instead of reading the real forward pass

The served model runs on fused GPU kernels whose summation order and rounding are not
specified. The proof needs an arithmetic with one right answer per operation. The harness is
that specification: it is the model rewritten so that every operation is explicit, and its
output is both the thing proved and the witness. Rerunning the same prompt on the standard
Hugging Face backend did not reproduce the same ids three times out of three (the repository
records this as an open gap), so "verify by rerunning" is not a check anyone can make; the
proof is about one decode.

---

## 5. Glossary: plain words and the code's identifiers

| Plain word (use in narration) | Code identifier | Meaning |
|---|---|---|
| segment | chunk | one layer (or the head) over 512 positions at context C, one STARK |
| cell | cell | one committed field element in one column at one row; the unit of prover work |
| statement | Fixed + Claims | the two serialised documents a verifier is given beside the proof |
| seam | requant / requantize seam | a requantise step between a bf16 producer and an int8 consumer, proved as its own component |
| edge, binding | binding table | a verifier-side equality between two gadgets' claims; 16 per layer segment |
| key tile | key tile | a group of attention heads packed onto one column set over a slice of the keys |
| diagonal block | `--diagonal-block` | the 512 by 512 block where queries attend to keys of their own block; only it writes keys and values to the boundary |
| pin | `--kmax`, `--ao-rem-bits`, `--fold-rem-bits` | a width every segment of a loop must share, set to the model-wide worst case |
| shape tree, model tree | tree 0, tree 1 | the two preprocessed trees; the verifier rebuilds the first, compares the second with the manifest |
| base trace, interaction tree, boundary trees | trees 2, 3, 4+ | the prover's values, the lookup bookkeeping, the chain links |
| hash channel | Blake2s channel | the Fiat–Shamir transcript every root is mixed into |
| digest gate | `proof_sha256` | the proof bytes must reproduce on both backends before a change merges |
| negative control | `--unsound-skip-*`, tamper tests | a deliberate break the verifier must reject |
| grid check | `boundary-grid --verify` | per-segment verification, then every root link, then every id |
| witness | dump | every intermediate value of the rerun forward pass, per layer and block |
| lookup | LogUp relation | proof that used rows are a sub-multiset of a committed table |
| Freivalds check | `freivalds` gadget | rᵀ(W X) = (rᵀ W) X at a random r |
| GKR reduction | `--gkr-*` | a sumcheck that proves a lookup's running sums instead of committing them |

---

## 6. The seven honesty points (keep all of them in the video)

1. **Not hiding.** No random blinding is added to the committed trace. The only thing hidden is
   the weights, behind their Merkle root. "ZK" names the proof-system family.
2. **Not the served model.** The proof is about a fixed quantised arithmetic (int8 and bf16,
   integer softmax) that costs +6.96 % perplexity on the 8B model. A real server runs bf16 or
   fp8 kernels. Nobody has yet counted what a bf16 statement would cost.
3. **Greedy only.** Temperature and top-p sampling, and early stop at end-of-sequence, are
   outside the statement.
4. **Ids, not text.** The tokeniser and the chat template are unproved; the public input is the
   list of ids.
5. **No binding to traffic.** No proof names a request, a client or a time. It proves ids map to
   ids under a commitment, not that anyone was served this answer. SASH lists binding to
   traffic records, batching and architecture hiding as open work.
6. **Not formally verified.** Nothing machine-checks that the rules equal the model's
   arithmetic. What exists is empirical: the digest gate, negative controls, and self-tests
   that rebuild cell counts from the layout. SASH asks for a specification of what an inference
   proof must cover, a corpus of negative controls, and machine-checked constraint systems as
   public goods.
7. **A measurement tool.** In SASH's own words the prototype is "a measurement tool, not
   something anyone should rely on yet", and "nobody outside our team has checked the
   correctness of our implementation".

Other gaps the results repository records: determinism (rerunning on the standard backend
did not reproduce the ids), batching (no batch index in the statement), architecture (dense
Llama only: no bias site, no sliding window, no mixture of experts; a model with a projection
bias such as Qwen2.5 is refused at edge 3).

---

## 7. Visual motifs, suggested

- **The tape to the curve** (Act 3) is the one transform to spend real animation time on: cells
  rise off the tape onto a graph, a curve threads them, the rule becomes a second curve that
  touches zero at six marked points, division collapses it to a quotient.
- **The hash channel** as a grey box with an input slot (roots go in) and an output tray (dice
  come out). Reuse it in Act 4 for every challenge, and once in Act 6 inside the verifier, who
  owns an identical box.
- **Five triangles in a row** for the five trees, each labelled by who can build it: verifier
  (tree 0), publisher (tree 1), prover (trees 2 to 4+). Colour the labels by cast colour.
- **The wall of 290 tiles** for Act 6, with the two kinds of arrows in two colours; zoom into
  one tile to show the transcript of Act 4, zoom out to show the links.
- **A ring of 16 small locks** around the layer diagram for the edges; a skip flag opens one
  lock and turns the whole tile grey ("control, never a result").
- **Stacked bars** for the phase split and the fresh-cell split; a lighter tint for projected
  numbers than for measured ones, with the grade written beside every number.
- **The real prompt** "The capital of France is" threaded through the whole video: its ids in
  Act 1, its int8s in Act 2, its argmax in Act 5, its emitted ids chained in Act 6.

---

## 8. Sources

- Code: https://github.com/sg-ai-safety-hub/zk-inference-prover (`README.md`,
  `docs/statement.md`, `GLOSSARY.md`, `prover/README.md`, `prover/src/util.rs`,
  `prover/src/compose.rs`, `prover/src/boundary.rs`, the docstrings of
  `prover/src/gadgets/{freivalds,dequant,requant,attention,argmax,embed,residual_stream}`,
  `harness/witness/extract.py`, `nitroo/README.md`,
  `nitroo/crates/stwo/src/core/fields/{m31,qm31}.rs`).
- Measurements: https://github.com/sg-ai-safety-hub/zk-inference-results (`constants.json`,
  `docs/quantization.md`, `docs/statement-gap.md`, `docs/cost-model.md`).
- SASH research note: https://www.aisafety.sg/research/what-proving-llm-inference-actually-costs-research-note
- SASH ZKP introduction: https://www.aisafety.sg/blog/zkp-intro
- The real decode run and the step cards: `brain-dump/ai-inference-verification/notebooklm-source.md`
  and `decode-and-prove.html` in the same folder; the STARK toy follows the "Going further"
  section of Vitalik Buterin's "STARKs, Part I".
- Manim Community Edition: https://docs.manim.community
