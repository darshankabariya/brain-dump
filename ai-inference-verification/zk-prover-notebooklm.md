# How the zk-inference-prover works, taught for intuition

A source document for NotebookLM. It explains, from the ground up, how SASH's open
`zk-inference-prover` turns one run of a language model into a proof that anyone can check.
It is written intuition first: every chapter starts with the question, gives a picture or an
analogy, works a tiny example by hand, and only then states what the real system does and why
it is built that way. Every number carries its grade: **measured** (read from the published
run), **derived** (arithmetic on measured numbers) or **projected** (from a cost model, not a
run). Written 12 October 2026 from the repositories listed at the end.

---

## 0. How to use this file with NotebookLM

1. Make a new notebook and add this file as a source. Upload the Markdown file, or open it,
   copy all the text and add it as a pasted-text source. Either works.
2. Keep the notebook small. This file already carries the intuition. If you add more, add in
   this order: the SASH research note (a web link), then the prover repository's
   `docs/statement.md` and `README.md` as pasted text. Many raw sources make the overviews
   drift toward lists of facts and away from the story.
3. Generate a Video Overview. If the generator offers a box for instructions or focus, paste
   the focus text below. Do the same for an Audio Overview, and pick the longest length it
   offers. The focus text is what makes the result an explanation and not a summary.
4. Afterwards, use the notebook's chat with the questions in chapter 12. The answers there are
   short; the chat can expand any of them with the detail of the earlier chapters.

### Focus text to paste into the overview generator

> Teach how the zk-inference-prover works to someone who knows what a language model is and
> has heard of hashes and Merkle trees but has never seen a STARK. Build intuition before
> precision and follow the source's order: the receipt problem; why the model is rerun in fixed
> arithmetic; the Fibonacci tape as a polynomial with a rule, a random audit and a commitment;
> one segment proof with its five trees and the hash box; the three tricks, Freivalds with the
> two-by-two example, LogUp with the one-two-three table, and seams with Horner bindings; the
> grid of 290 tiles chained by roots; the measured numbers; the seven honesty points. Use the
> analogies in the source and keep returning to the one principle: seal first, roll the dice
> after. For every design choice say what would break without it. Keep the numbers with their
> grades. Do not use code identifiers. Correct the misconceptions the source lists. Make it
> long, slow and thorough; thirty minutes is better than ten.

---

## 1. The whole idea in one paragraph

A provider says: "I ran this language model on your prompt and it answered this." You want a
receipt you can check without rerunning the model and without seeing its weights. The
prover's answer has four moves. **Rerun the model in an arithmetic where every operation has
exactly one right answer**, so each step is a rule. **Write every intermediate value into
tables**, so the whole computation becomes rows and columns of numbers that must obey the
rules. **Seal the tables** with a hash fingerprint before anything else happens. **Then let
randomness audit the sealed tables**: a few random questions whose answers can only be right
if every rule holds in every row. The rest of this document unpacks those four moves. If you
remember one principle, remember this one: **seal first, roll the dice after.** It appears
seven times in the design, and every time it is the thing that makes cheating impossible.

---

## 2. The receipt problem

**The question.** A box holds eight billion numbers, the weights of Llama 3.1 8B. You type
"The capital of France is". Out comes " a city of romance". That is the real greedy answer of
the public model without a chat template; at the first step it scored the word " a" at 16 and
" Paris" at 15.938, so it nearly said Paris. How would you know the box really ran the model
it claims, on your prompt, if you cannot rerun it and may not see the weights?

**The picture.** Think of an exam. A bare answer tells you nothing. A paper where every line
of working is written down can be checked line by line by someone who never solved the
problem. The prover produces the working, and it produces it in a form where you do not even
have to read every line: you check a handful of random lines and the sealing guarantees the
rest.

**Three things a receipt must fix.**
- The input: which token ids went in. These are public.
- The machine: which weights were used. They stay secret, but they are fixed by a commitment,
  a 32-byte fingerprint the publisher announced once.
- Every step in between: so that no wrong step can hide in the middle.

**The cast.**
- The model publisher holds the weights, commits to them once as a Merkle tree, and publishes
  the root. Call it the model root.
- The prover is the provider running inference. It holds the weights and a GPU. It reruns the
  decode in fixed arithmetic, keeps every intermediate value, turns each piece of the run into
  tables, seals them, answers the random audit and writes the proof.
- The verifier is anyone with a CPU. It holds the prompt ids, the model root and a small
  per-layer calibration file. It holds no weights and needs no GPU.

**Say this early.** The letters ZK name the family of proof systems. This prototype hides
nothing except the weights behind their root. No random blinding is added to the tables, the
architecture is public and the prompt ids are public. It is a proof of correctness, not a
privacy tool. Chapter 10 lists everything else it is not.

**What is proved, in one sentence.** For these published prompt ids, under the model whose
weight commitment is this root, greedy decoding in this fixed arithmetic produces these 512
ids. Every layer of every position is proved, from the embedding row to the final argmax,
for all 4,096 prompt positions and all 512 generated positions, 4,608 in all [measured].

---

## 3. Why the model is rerun in fixed arithmetic

**The question.** The provider already ran the model once. Why run it again?

**The picture.** A recipe that says "a pinch of salt" cannot be audited; a recipe that says
"3.0 grams" can. A GPU kernel adds floating-point numbers in whatever order is fastest and
rounds in ways nobody wrote down. Two runs of the same prompt need not agree. The repository
records exactly this gap: rerunning the same prompt on the standard Hugging Face backend did
not reproduce the same ids three times out of three. So "verify by rerunning" is not a check
anyone can make, and a proof needs every operation to be a rule with one right answer.

**What the harness does.** It reruns the model in a fixed quantisation, named `y-delay-vw12`
in the repository:
- activations are 8-bit integers with one scale per token;
- weights are 8-bit integers with one scale per output channel;
- matrix sums are exact integers;
- dequantisation back to 16-bit floats (bf16) is a chain of correctly rounded steps, round half
  to even;
- the nonlinear functions run in bf16, and each is a table of all 65,536 possible inputs;
- the softmax runs on integers: queries at 12 bits, keys at 11, and the exponential is a lookup
  table that returns a 9-bit numerator;
- the attention output is rounded straight to a 12-bit integer with a power-of-two scale.

**One token through one layer**, left to right along the residual stream: normalise;
requantise to int8; three matrix multiplies make queries, keys and values; dequantise to
bf16; rotate queries and keys by position and quantise them again; attention, where each
token looks at all keys so far and takes a weighted sum of the values; round the result to 12
bits; one more matrix multiply; dequantise; add to the stream; normalise again; two matrix
multiplies, a gate, a product, requantise, one more multiply, dequantise, add to the stream.
Llama does this 32 times, then one final normalisation, one multiply to 128,256 scores, and
the largest score wins. The model has hidden size 4,096, 32 query heads and 8 key/value heads
of 128 channels, MLP width 14,336, and about 8.03 billion weights, of which each layer holds
218 million.

**The price of the fixed arithmetic.** On the same 20,440 scored tokens the float model has a
perplexity of 4.408 and the proved arithmetic 4.715, which is 6.96 % worse [measured]. A naive
static per-tensor int8 scheme scores 65.99 [measured], so the careful choices above are what
keep the model usable. Task scores were unchanged within error.

**A real requantisation, by hand.** Last token of the France prompt, layer 0, after the first
normalisation. The largest magnitude among the 4,096 values is 4.03125. Divide by 127 and
round up to the next bf16: the token's scale is 0.031982421875. Now divide every value by the
scale and round. The first eight values [-0.0171, 0.0201, 0.0152, 0.0093, -0.3203, -0.0099,
0, 0.0022] become the integers [-1, 1, 0, 0, -10, 0, 0, 0]. The first eight weights of row 0
of the query matrix, with their channel scale 0.00045, become [11, -65, -14, -40, -7, 59, -2,
-5]. Everything downstream is integer arithmetic, and integer arithmetic has one right answer.
(The study's own script recorded the scale as 0.03173828125 because its helper rounded to the
nearest bf16 rather than up; the eight integers are the same under either scale.)

**The witness.** While the model reruns, nothing is thrown away. Every int8 activation, every
exact accumulator, every bf16 bit pattern, every attention score, every key and value, and the
residual stream entering and leaving each layer is written to disk, per layer and per block of
512 positions. This pile is the witness: the lab notebook from which the tables are built. On
the France prompt the residual stream's typical size grows from 0.006 after the embedding to
0.145 after layer 14, 0.835 after layer 31 and 2.176 after the final normalisation. At layer
31, head 0, the last token " is" attends 0.5117 of its weight to itself and 0.1953 to
" France". Attention is the one operation whose cost grows with the length of the context,
which matters for the numbers at the end.

**Remember this.** The thing proved is not the served model. It is a fixed, slightly worse,
exactly specified stand-in, and the rerun is both the computation and its own evidence.

---

## 4. The one cryptographic idea: a table becomes a curve

This is the one piece of cryptography to learn slowly. Everything else in the prover is
engineering on top of it. We use a toy with eight cells.

**The tape.** Eight cells: 1, 1, 2, 3, 5, 8, 13, 21. The rule: each cell is the sum of the two
before it. For our purposes a computation is exactly this, a tape of values and a rule that
every hop along the tape obeys. A language model run is a very wide tape with a few hundred
rules.

**Idea 1: through N points there is exactly one curve of degree below N.** Put the eight cells
at eight fixed positions on the x-axis and draw the unique polynomial of degree at most 7
through them. Call it P. The tape has become a curve, and the curve remembers every cell.

**Why a polynomial and not any curve.** Because a low-degree polynomial is rigid. Two
different polynomials of degree at most 7 can agree at no more than 7 points. If you change
one cell, the new curve differs from the old one almost everywhere, not just at the changed
cell. A lie in one cell wrinkles the whole curve. That rigidity is what lets a random spot
check stand in for a full check.

**Idea 2: apply the rule to the curve.** Define C(x) = P(x two steps ahead) − P(x one step
ahead) − P(x). Wherever the rule holds, C is zero. It holds at the first six positions, the
six hops. Six separate facts about cells have become one statement about one curve: C has
roots at six known places.

**Idea 3: division.** A polynomial that is zero at six known points is divisible by Z(x), the
polynomial whose roots are exactly those six points. So C = Z × Q for some quotient Q, and an
honest prover can compute Q. Now change one cell: let 13 become 14. At that hop C equals
14 − 8 − 5 = 1, not zero. Z no longer divides C, and there is no polynomial Q at all. One wrong
cell anywhere destroys the quotient everywhere.

**Idea 4: the random audit.** The verifier picks a random position r far outside the tape and
asks for the values of P and Q there, then checks C(r) = Z(r) × Q(r). If the prover lied, its
"Q" is not a real polynomial, and the equation fails at all but a handful of positions. A lie
survives one random question with probability about the degree divided by the size of the
number field. The arithmetic runs in a finite field, the integers modulo the Mersenne prime
2^31 − 1 (about 2.1 billion elements), where every operation is exact. The random positions
and all challenges are drawn from a four-fold extension of that field with about 2^124
elements, so one random question makes a lie essentially impossible.

**Idea 5: seal before the question.** What stops the prover from inventing P after it sees r?
A commitment. Before any question, the prover evaluates P on a bigger domain, twice as many
points as the tape (the "blowup" of 2), and hashes all those values into a Merkle tree: hash
pairs of values, hash pairs of hashes, up to a single 32-byte root. The root is published
first. When asked about r, the prover opens the leaf at r together with its path of hashes to
the root. Change any leaf and the root changes. The root is a fingerprint of the whole table.

**Idea 6: the low-degree promise.** The verifier also needs to know that the sealed values
really lie on a low-degree curve, and not on a pointwise cheat that happens to pass at r. A
protocol called FRI does this: fold the polynomial in half, seal the half, fold again, with
random queries at every level. Treat it as a black box with one promise: a sealed list is low
degree, checked with 100 random queries. This system uses blowup 2, 100 queries and no
proof-of-work, which its library accounts as 100 bits of conjectured security, and the code
asserts that number and refuses to run if it drifts.

**Idea 7: the hash box.** There is no live verifier while the proof is made. The randomness
comes from a hash. The prover feeds every root into a hash function (Blake2s) and the random
position is the hash output. Picture a grey box: roots go into the slot, dice come out of the
tray. Because the root goes in before the die comes out, the prover cannot fit its values to
the randomness. This is the Fiat–Shamir transform, and the box comes back in every later
chapter.

**Scaling up.** The Fibonacci tape had one column and one rule. A transformer layer segment
has thousands of columns and hundreds of rules, together called the AIR (algebraic
intermediate representation). One field element in one column at one row is called a cell,
and the cell is the unit of prover work. A single segment proof here seals about 1.25 billion
fresh cells on average (363.9 billion fresh cells over 290 proofs, measured; the division is
derived). Everything else is the same as the toy: seal, draw dice, check the rules at random
points.

**Remember this.** Rules become divisibility, divisibility is checked at a random point, and
the seal makes the random point honest.

---

## 5. One segment, one proof: five trees and one hash box

**The question.** What exactly is one proof about, and what happens inside it, in what order?

**The unit.** A segment is one transformer layer (or the output head) applied to one block of
512 positions against the context of all earlier positions, proved as one STARK. A request
with a 4,096-token prompt and 512 generated tokens becomes a grid: 9 token blocks (8 prompt
blocks and one generated block) times 32 layers, plus the output head proved twice, 290
proofs [measured]. The practical reason for segments is size: one proof sealing the whole
request would be hundreds of billions of cells. Segments keep each proof around a billion
cells, let the loop pipeline them, and chapter 7 shows how they are chained without any
recursion.

**The picture: five shelves, each with an owner.** Inside one segment proof there are five
kinds of Merkle tree, sealed in this order.
- Tree 0, the shape tree. Everything the rules read as a fact: selectors, the causal mask,
  the marker for which key rows are real, the lookup tables (the exponential table, the bf16
  rounding tables, the range tables), the rotation angles for this block's positions. It is a
  pure function of the public parameters and the per-layer calibration file, so the verifier
  rebuilds it from scratch and rejects on a root mismatch. No weight is in it.
- Tree 1, the model tree. This layer's int8 weights and per-channel scales, and on the
  segments that need them the embedding matrix or the output head. The verifier cannot
  derive it; it compares the root with the publisher's manifest. Built once per layer and
  cached on the GPU.
- Tree 2, the base trace. Everything the prover chose: int8 activations, accumulators, bf16
  patterns of the residual stream, attention scores and numerators, the rotated and quantised
  queries, keys and values, the token ids, and one multiplicity column per lookup table. Most
  cells live here.
- Tree 3, the interaction tree. The lookup bookkeeping of chapter 6, which depends on the
  random challenges and so can only be sealed after they are drawn.
- Trees 4 and up, the boundary trees. The residual stream in, the residual stream out, and the
  keys and values this block wrote. Small trees whose only job is to be compared with a
  neighbouring segment's trees.

**The transcript, with the hash box at the side.**
1. Seal trees 0, 1 and 2 and mix each root into the box.
2. Draw the challenges from the box: a pair (z, alpha) for every lookup table, the weights
   r, s, rv that fold whole matrices into one number, and the binding challenge w for the
   residual stream.
3. Build every lookup fraction and running sum; run five sumcheck reductions (chapter 6); seal
   tree 3.
4. Seal the boundary trees. They are tied to base-trace columns by plain equality rules, which
   is why they may come after tree 3.
5. The STARK proper: draw the out-of-domain point, evaluate every rule's quotient there
   (generated CUDA kernels do this), seal the composition polynomial, run FRI.
6. Write three documents: Fixed (the statement: shapes, parameters, security settings, the
   two preprocessed roots), Claims (every published sum and fold) and Proof. The median proof
   is 64.97 MiB [measured].

**Why the order is the whole argument.** Rewind the transcript. If the prover knew a challenge
before sealing, it could choose values that pass that one challenge. So every root goes into
the box before the die that depends on it comes out. This makes the byte order of the proof
load-bearing, and the project turns that into a rule: the SHA-256 of the proof bytes must
come out identical on the CPU backend and the GPU backend before any change is merged. They
call it the digest gate.

**A float as two cells.** The blowup is only 2, so every rule must stay at degree 2 or below.
A bf16 number is therefore not stored as a 16-bit pattern but as two cells: a signed
significand sm that is 0 or lies in ±[128, 256), and an exponent field ef in [1, 255), with
value sm × 2^(ef − 134). For example 1.5 = 192 × 2^(127 − 134) = 192 / 128. "Is zero" is simply
sm = 0, one cell to test.

**How much is sealed.** Per proved position at context 4,096: 58.5 million cells in the base
trace, 17.8 million in the interaction tree, 2.6 million in the boundary trees, about 79.0
million fresh cells per position [measured]. Another 22.9 million model cells and 4.5 million
shape cells are preprocessed and cached, not paid again per segment [measured]. At context
16,384 the fresh total is about 105 million per position [measured], because attention grows
with the context.

**Where the cells come from, per operation** [measured, from the results' model constants]:
one requantised value costs 11.5 cells; one dequantised accumulator costs 15.1 cells with a
power-of-two scale and 26.1 with the full rounding chain; one attention output costs 10.1
cells; one residual-stream add costs 24.3 cells and one multiply 8.75; one argmax comparison
costs 9.05 cells; attention costs 4 cells per head, key and token; and a weight costs only
0.088 fresh cells plus 1.03 preprocessed cells, which is the Freivalds trick of the next
chapter at work. This is the intuition for the thousand-fold overhead: every arithmetic
operation of the model becomes ten to thirty sealed numbers, and every sealed number is
hashed and interpolated.

**Remember this.** Five trees, sealed in order, with the dice drawn only after the roots they
depend on are in the box.

---

## 6. The three tricks inside the tables

Three problems would make a naive encoding impossible. Each has a trick, and each trick is the
same principle again: seal first, roll the dice after.

### Trick 1. Matrix multiplication by Freivalds, not cell by cell

**The problem.** One layer has seven matrix multiplies over 218 million weights. Writing a
rule "this output equals this dot product" for every output cell would be hopeless.

**The picture.** You do not check a huge multiplication by redoing it. You weigh the result
with random weights and compare against the same weighing of the inputs. A wrong answer almost
never balances under weights it did not know in advance.

**The toy.** W = [[1, 2], [3, 4]] and X = (1, 1), so the honest product is Y = (3, 7). A prover
claims Y' = (3, 8). After Y' is sealed, the verifier draws a random vector r = (r1, r2) and
checks one equation: r · Y' against (r × W) · X. The left side is 3 r1 + 8 r2. The right side is
(r1 + 3 r2, 2 r1 + 4 r2) · (1, 1) = 3 r1 + 7 r2. They differ by r2, and a random r2 is zero with
probability one in the field size.

**The general rule.** Check rᵀ (W X) = (rᵀ W) X at a random r. This costs one pass over the
weights, linear instead of cubic, and a wrong product survives with probability about the
degree over 2^124. In the code r is the powers of a drawn challenge. One gadget folds the sealed
inputs and the preprocessed weights into one number per matrix; the dequantisation gadget
folds the same sealed accumulators the other way; the verifier requires the two numbers to be
equal. Nothing is sealed twice, and because the weights come from tree 1, the proof is about
the committed model and no other.

### Trick 2. Everything else by LogUp, the balancing of fractions

**The problem.** Many steps are not polynomial rules at all. "This bf16 is the correctly
rounded result." "This numerator is the exponential of this score." "This value is below
2^15." Each is really a membership claim: the row I used must be a row of a table that was
sealed before any challenge.

**The picture.** The table is a menu. Every dish the prover claims to have ordered must be on
the menu, and the prover must say how many times each dish was ordered. The check is a
fingerprint of a multiset that a dish not on the menu can never match.

**The toy.** The table holds {1, 2, 3}. The prover used [2, 2, 3] and seals a multiplicity per
table row: (0, 2, 1). After a random z is drawn, both sides become sums of fractions. The uses
give 1/(z − 2) + 1/(z − 2) + 1/(z − 3). The table gives 0/(z − 1) + 2/(z − 2) + 1/(z − 3). They
are equal for every z. Now cheat and use a 4. That adds 1/(z − 4), a pole at 4, and no
multiplicity over {1, 2, 3} can ever cancel a pole at 4. The two sums differ at every z but a
vanishing few. Think of 1/(z − x) as a flag planted at x that only another flag at x can take
down.

**In the real system.** Rows with several columns are first folded into one number with a
second challenge alpha, then the same fractions are formed. The running sums of those
fractions are the interaction tree of chapter 5. A cost rule worth remembering: a table row
costs one multiplicity cell plus one fraction in the extension field, which is four base cells,
so five cells a row, whether or not the row is used. A range table with 2^20 rows costs five
times 2^20 cells even if only a few rows are ever looked up.

**Which tables.** The rounding tables that prove a correctly rounded bf16 (the magnitude is
split as a 9-bit mantissa times a power of two plus a remainder, injectively, so the field's
wraparound cannot fake a rounding); a table of all 65,536 bf16 inputs for the reciprocal
square root and another for the gate function; the exponential table of the integer softmax,
whose rows are (score shift, 9-bit numerator); range tables for int8 activations, 15-bit
comparisons and the attention output's remainder and denominator; and the whole embedding
matrix, 128,256 rows by 4,096, which is a table in tree 1, so selecting one row by a sealed
token id costs one pass over the table, almost all of it preprocessed.

**GKR, in one sentence.** For the five largest lookup families the running sums are not
sealed as columns at all; a sumcheck protocol proves them and a link ties its final claim back
to the sealed columns. On the 32-segment ablation this cut the sealed cells from 71.6 billion
to 44.6 billion, 37.8 % fewer [measured, derived], and at context 16,384 it shrinks the
interaction tree from 93,184 columns to 5,600. Building the fractions and running the
sumchecks is 41.8 % of proving time [measured], the largest phase.

### Trick 3. Seams and bindings, so the gadgets talk about the same numbers

**The problem.** Each gadget proves its own step correctly. Without a link, the prover could
feed the matrix multiply one input and the normalisation another, and each proof would be true
about the wrong numbers.

**The picture.** Two accountants describe the same ledger. You do not compare every entry; you
pick random weights after both have signed their books and compare one weighted total. Equal
totals under random weights mean equal books, entry by entry.

**The Horner claim.** Under a challenge w drawn after sealing, a gadget publishes one number,
the sum of its output values each weighted by a power of w. The next gadget publishes the same
sum over the values it consumed. The verifier compares the two numbers. The cost is about half
a cell per value, and the values are sealed once.

**Seams.** Where a bf16 producer meets an int8 consumer, the requantisation step between them
is proved as its own component, called a seam, so the matrix multiply multiplies exactly the
integers the producer made. In a seam the prover seals, per token, the maximum's magnitude
pattern, a selector bit per element, the scale and the int8 values; every element's pattern is
range-checked against the maximum; the pair (maximum, scale) is one lookup into a table of
ceil(v / 127) in bf16; each nonzero integer is one lookup into a division table; each zero is
one range lookup proving the value was below half a scale; and three Horner folds close the
seam to its producer and its consumer.

**The 16 edges of a layer.** Around one layer there are sixteen such links. Seven bind the
residual stream: the two normalisations read the sealed stream, the adds and the gate read
the dequantised outputs, attention reads the rotated queries, keys and values, and the output
projection reads the attention output. Three are seams: into the query, key and value
multiplies, into the gate and up multiplies, into the down multiply. One is the attention
component itself. One is the Freivalds check itself. Two are boundaries: the residual stream
to the next layer and the keys and values to the next block. Layer 0 adds the embedding edge
and the head adds the argmax edge. Every edge is on by default. A witness that cannot state
one is refused. A flag can turn one off loudly: the run's provenance lists it and that run is a
control, never a result.

**The argmax edge, because ties are real.** Greedy decoding takes the first maximal index. On
the recorded continuations 15 of 512 positions had two or three equal top scores [measured].
The prover seals the maximum's pattern, the emitted token, and an indicator b that is 1 before
the token and 0 from the token on. A range check on (maximum − score − b) says: strictly below
the maximum before the token, at most the maximum from the token on. The indicator must be 0
or 1, never increase, and sum to the token; that sum is the binding itself. A weaker form that
only says "the token attains the maximum" exists as a flagged control; it would let the prover
pick the token on every tied row.

**Remember this.** Freivalds weighs products, LogUp fingerprints multisets, Horner bindings
fingerprint sequences. All three draw their weights only after the values are sealed.

---

## 7. The grid: 290 proofs chained by roots, and what the verifier does

**The question.** If there is no recursion, how do 290 separate proofs add up to one claim
about one request?

**The picture.** A wall of tiles. Columns are token blocks 0 to 8, rows are layers 0 to 31,
and two head tiles sit over blocks 7 and 8, because the first generated token's argmax was
computed at the last prompt position. Each tile has a fingerprint on each edge, and neighbours
must match fingerprint to fingerprint.

**The links.** Every vertical arrow says: the residual-stream root leaving this tile equals the
root entering the tile above, 281 layer links. Every horizontal arrow says: the keys and values
this block wrote equal the prefix the next block attended over, 256 token links. 537 links in
all [measured]. Layer 0 also binds the embedding row and the head binds the emitted id, so
every generated id is chained to the prompt or to a proved argmax.

**Why a root and not a challenge.** Each tile's internal claims are taken under challenges
drawn inside that tile, so two tiles weigh their boundaries differently and their Horner
claims cannot be compared. The obvious repair, drawing one shared challenge from public data,
breaks the one principle: a challenge known before the values are sealed turns "my total
equals yours" into one linear equation the prover can solve. So the exposed value is a Merkle
root of the boundary values themselves, bound to the base trace by a plain equality rule. The
link check is five integer comparisons that pin the layout, then one 32-byte comparison.
Constant time, no recursion anywhere.

**What the verifier does per tile.** Parse Fixed, Claims and Proof. Refuse if the shapes do not
match the plan or the security parameters drifted. Replay the hash box and redraw every
challenge. Verify the five sumchecks. Run the STARK verifier: out-of-domain sampling and FRI.
Check that every lookup's fractions cancel. Check every Freivalds equality, the attention
identities and every binding equality. Rebuild the shape tree from the public parameters and
the calibration file and compare its root. Compare the model root with the published manifest.
Then, over the grid: every link, then every id.

**What verification costs.** Over the 290 proofs the verifier's own time on the run host's CPU
cores was 119 s, a median of 0.41 s per segment [measured]. On a consumer machine with four
cores and no graphics card, one reference segment at context 16,384 took 43.2 s, of which
42.25 s was rebuilding the shape tree and 0.92 s was checking the proof itself, at a peak of
28.5 GiB of memory [measured]. The shape tree is the verifier's main cost, and a grid pays it
once per layer-and-context shape, not once per proof.

**Remember this.** Tiles are chained by fingerprints of their edges, not by proofs of proofs,
and the verifier replays the whole game with a hash box of its own.

---

## 8. The seven stages of a run

1. Generate the ids (Python, GPU). Take a 4,096-token prompt, run the quantised model greedily
   for 512 tokens. This decode is itself the thing proved.
2. Extract the witness (Python, GPU). Rerun the forward pass in explicit fixed arithmetic and
   dump every value a rule will read, per layer and per block. The most expensive host step.
3. Shape table and plan (Python, CPU). Read every dump, compute the model-wide worst case for
   the widths every segment must share (the code calls them pins), refuse early if a layer
   would not fit the field's 31 bits, and write one plan line per segment: 290 lines.
4. Emit CUDA kernels (Rust, once per shape). Lower the rules to straight-line code, check that
   lowering against the CPU evaluator on random data, build. Without them the GPU build still
   works but evaluates rules on the CPU; the proof bytes are identical either way.
5. Commit the model (Rust, once per model). For every layer-and-context shape build only the
   preprocessed trees and read off the shape root and the model root.
6. Prove every segment (Rust, GPU, the loop). Pipelined so segment k + 1 is built while
   segment k is proved. Per segment: load the dump, build every gadget's columns, seal the
   trees, draw challenges, build the lookups and run the five sumchecks, seal the boundary
   trees, STARK, serialise.
7. Verify and chain (Rust, CPU). Every segment, then every link, then every id. A gate script
   refuses the run if any segment lists a skip flag, any edge is unbound, any kernel fell back
   to the CPU or any link failed. Only then does the run become a row in the published
   constants.

---

## 9. The numbers, with their grades

One request on one H100: 4,096 prompt tokens and 512 generated tokens.

- Segments: 290 [measured].
- Proving loop: 3,683 s, 61 minutes [measured]. Whole run including extraction: 5,485 s, 91
  minutes [measured].
- Throughput: 1.25 positions per second in the loop, 0.84 over the whole wall [derived]. About
  12.7 s per segment in the loop [derived].
- Cost at 3.29 USD per GPU-hour: 0.73 to 1.09 USD per 1,000 positions, so 3.37 to 5.01 USD per
  request [derived].
- Unproved serving with vLLM, one request at a time: 42,231 prompt positions per second, 153
  generated per second, 1,342 end to end [measured].
- Overhead: about 1,070 times against the proving loop and about 1,600 times against the whole
  wall [derived from the two measured rates].
- Proof size: 18.46 GiB serialised for the 290 proofs, 7.19 GiB in memory before serialisation
  (not "compressed"); median segment 64.97 MiB, range 48.4 to 120.0 MiB [measured].
- Fresh cells: 363.9 billion for the request, about 79.0 million per position, about 1.25
  billion per segment [measured, derived].
- Context 16,384: 1,058 segments; loop 21,586 s, 6.0 hours; 0.78 positions per second; about
  105 million fresh cells per position; 108.9 GiB of proofs [measured, derived].

**Where the time goes**, from a serial loop over 32 layer segments taking 748 s [measured]:
building the lookup fractions and running the sumchecks 41.8 %; building the base trace
35.4 %; loading and decoding the witness 11.8 %; other host work 6.4 %; the STARK itself, the
seal and the prove, 4.6 %. The cryptography is the cheap part. Building the tables on the host
is the ceiling. Moving rule evaluation to the GPU is already done: with those kernels left on
the CPU the same loop took 4,737 s [measured].

**Projections, from the results repository's cost model, not measurements** [projected]: a
70B model in the order of 5 to 8 hours per request; 405B, 16 to 24 hours; a 1T dense model, 32
to 48 hours. These hours are derived from the model's projected cost per million positions at
3.29 USD per GPU-hour and 4,608 positions per request.

---

## 10. The seven honesty points, and the other gaps

1. Not hiding. No random blinding is added to the sealed trace. Only the weights are hidden,
   behind their root. "ZK" names the proof-system family.
2. Not the served model. The proof is about a fixed quantised arithmetic that costs 6.96 %
   perplexity on the 8B model. A real server runs bf16 or fp8 kernels. Nobody has yet counted
   what a bf16 statement would cost.
3. Greedy only. Temperature and top-p sampling, and early stop at end of sequence, are outside
   the statement.
4. Ids, not text. The tokeniser and the chat template are unproved; the public input is the
   list of ids.
5. No binding to traffic. No proof names a request, a client or a time. It proves ids map to
   ids under a commitment, not that anyone was served this answer.
6. Not formally verified. Nothing machine-checks that the rules equal the model's arithmetic.
   What exists is empirical: the digest gate, negative controls and self-tests that rebuild
   cell counts from the layout.
7. A measurement tool. In SASH's own words the prototype is "a measurement tool, not something
   anyone should rely on yet", and "nobody outside our team has checked the correctness of our
   implementation".

Other recorded gaps: determinism (rerunning on the standard backend did not reproduce the
ids), batching (no batch index in the statement), architecture (dense Llama only; no
projection bias, no sliding window, no mixture of experts; a model with a projection bias
such as Qwen2.5 is refused at the third edge).

**What SASH says is next.** Move witness generation to the GPU; real 70B and 405B runs; close
the gap to real serving (float arithmetic, tokenisation, non-determinism, batching, binding
to traffic records); prove only a random sample of segments after the provider commits to the
boundary roots; and restructure into small auditable gadgets. The sampling argument: prove a
random fraction p of requests, and a provider who cheats m times escapes with probability
(1 − p)^m; at p = 1 % that is about 460 cheats before 99 % detection.

---

## 11. Misconceptions to correct

- "ZK means the prompt and answer are private." No. Only the weights are hidden. The ids are
  public and the trace is not blinded.
- "The proof shows that ChatGPT or the served model gave this answer." No. It shows that a
  fixed quantised stand-in of Llama 3.1 8B, under a committed set of weights, gives these ids
  by greedy decoding.
- "The verifier reruns the model." No. The verifier never touches a weight. It replays the
  hash box, checks random openings, rebuilds the shape tree and compares roots.
- "The 290 proofs are folded into one proof by recursion." No. They are chained by comparing
  boundary roots, one 32-byte comparison per link.
- "The STARK is the slow part." No. The seal and the prove are 4.6 % of the loop. Building the
  tables and the lookup fractions on the host is the cost.
- "The proof is 7.2 GiB compressed." No. 7.19 GiB is the in-memory size before serialisation;
  the serialised proofs total 18.46 GiB.
- "A segment proof seals tens of millions of cells." No. About 1.25 billion fresh cells on
  average; tens of millions is the per-position figure.
- "Randomness comes from the verifier." No. It comes from hashing the sealed roots, so the
  prover cannot see a challenge before sealing what it depends on.
- "A wrong value in one cell might slip past a spot check." No. One wrong cell makes the
  quotient not a polynomial, and the sealed low-degree curve then fails at almost every random
  point.
- "Ties in the argmax do not matter." They do: 15 of 512 positions had tied top scores, and a
  lax argmax rule would let the prover choose the token there.

---

## 12. Questions to ask the notebook, with short answers

- What is being proved, in one sentence? That for these prompt ids, under the model whose
  weight commitment is this root, greedy decoding in a fixed arithmetic produces these 512
  ids.
- Why rerun the model instead of proving the real forward pass? Because GPU float kernels do
  not have one right answer per operation; the rerun is a specification with exactly one
  answer, and it is both the computation and the witness.
- What is a cell, and why does it matter? One field element in one column at one row. It is
  the unit of prover work; a segment seals about 1.25 billion of them.
- What does the Fibonacci tape teach? That a table is a curve, a rule is divisibility, a random
  point checks divisibility, and a seal makes the random point honest.
- Why are polynomials used at all? Because a low-degree polynomial is rigid: changing one
  value changes the curve almost everywhere, so a random spot check catches it.
- What are the five trees? Shape (verifier rebuilds), model (publisher's root), base trace
  (the prover's values), interaction (lookup bookkeeping after challenges), boundary (edges to
  compare with neighbours).
- Why does the order of the transcript matter? Because any challenge known before the values
  it tests are sealed lets the prover fit the values to the challenge.
- What is Freivalds' trick? Check rᵀ (W X) = (rᵀ W) X at a random r drawn after the product is
  sealed; linear cost, a wrong product almost never balances.
- What is LogUp? Membership in a sealed table proved by comparing sums of 1/(z − value) with
  multiplicities, where a value not in the table plants a pole nothing can cancel.
- What is a seam? The requantisation step between a bf16 producer and an int8 consumer, proved
  as its own component and bound on both sides by Horner claims.
- What is a Horner binding? Two gadgets publish the same power-weighted sum over the values
  one produced and the other consumed, under a challenge drawn after sealing.
- Why roots and not shared challenges between segments? A shared challenge would be known
  before sealing, which is unsound; a root is a fingerprint and can simply be compared.
- What does the verifier do? Replay the hash box, verify the sumchecks and the STARK, check
  every identity and binding, rebuild the shape tree, compare the model root, then check every
  link and every id.
- How slow is it? About a thousand times slower than unproved serving, 61 minutes of proving
  for one 4,608-position request on one H100, three to five dollars.
- Where does the time go? 41.8 % lookups and sumchecks, 35.4 % base trace, 4.6 % the STARK.
- What is it not? Not hiding, not the served model, greedy only, ids not text, no binding to
  traffic, not formally verified, a measurement tool.

---

## 13. Glossary in plain words

- Segment: one layer (or the head) over 512 positions at some context, one STARK proof. The
  code calls it a chunk.
- Cell: one sealed field element in one column at one row.
- Witness: every intermediate value of the rerun forward pass, dumped per layer and block.
- Seal, commit: hash a table into a Merkle tree and publish the 32-byte root.
- Hash box, channel: the Fiat–Shamir transcript every root is mixed into and every challenge
  is drawn from.
- Shape tree, model tree: the two preprocessed trees; the verifier rebuilds the first and
  compares the second with the manifest.
- Base trace, interaction tree, boundary trees: the prover's values, the lookup bookkeeping,
  the chain links.
- Lookup, LogUp: proof that used rows are a sub-multiset of a sealed table.
- Freivalds check: the random-weight check of a matrix product.
- Horner claim, binding, edge: a verifier-side equality between two gadgets' power-weighted
  sums; 16 per layer segment.
- Seam: a requantisation proved as its own component between a float producer and an integer
  consumer.
- GKR reduction: a sumcheck that proves a lookup's running sums instead of sealing them.
- Pin: a width every segment of a loop must share, set to the model-wide worst case.
- Digest gate: the proof bytes must reproduce on both backends before a change merges.
- Negative control: a deliberate break the verifier must reject.
- Grid check: per-segment verification, then every root link, then every id.
- M31, QM31: the field of integers modulo 2^31 − 1, and its four-fold extension of about 2^124
  elements used for challenges.

---

## 14. Sources

- Code: https://github.com/sg-ai-safety-hub/zk-inference-prover (README, `docs/statement.md`,
  `GLOSSARY.md`, `prover/README.md`, the gadget docstrings, `nitroo/README.md`).
- Measurements: https://github.com/sg-ai-safety-hub/zk-inference-results (`constants.json`,
  `docs/quantization.md`, `docs/statement-gap.md`, `docs/cost-model.md`).
- SASH research note: https://www.aisafety.sg/research/what-proving-llm-inference-actually-costs-research-note
- SASH ZKP introduction: https://www.aisafety.sg/blog/zkp-intro
- The real decode data (7 October 2026, bf16 on an Apple M4 Pro): the data folder of this
  brain-dump. The STARK toy follows the "Going further" section of Vitalik Buterin's "STARKs,
  Part I".
