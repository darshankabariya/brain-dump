"""Narration for the zk-inference-prover explainer. One entry per Manim scene.

Every number is from zk-inference-results/constants.json or the prover's docstrings,
as collected in notes/zk-prover-video-brief.md on 12 October 2026.
"""

SCENES = [
    # ---------------------------------------------------------------- Act 1
    ("A1Hook", 1, """
Here is a box. Inside it are eight billion numbers, the weights of a language model.
You type: the capital of France is. Out comes: a city of romance.
That is the real greedy answer of Llama 3.1, eight B, without a chat template.
At the first step the model scored the word "a" at sixteen, and "Paris" at fifteen point nine.
It nearly said Paris.
Now the question this video is about. How would you know that this box really ran the model
it claims to have run, on your prompt, if you cannot rerun it yourself, and you are not allowed
to see its weights?
"""),
    ("A1Receipt", 1, """
What you want is a receipt for a computation.
A receipt has to do three things. It has to fix the input: which tokens went in.
It has to fix the machine: which weights were used, without revealing them.
And it has to make every step checkable, so that a wrong step somewhere in the middle
cannot hide.
There are three characters in this story.
The model publisher, who holds the weights and commits to them once.
The prover, the provider running the model, who has the weights and a GPU.
And the verifier: anyone with a CPU, who holds the prompt ids, a thirty-two byte commitment
to the model, and a small calibration file. The verifier holds no weights and needs no GPU.
"""),
    ("A1Shape", 1, """
The whole answer fits in one line.
Rerun the model in an arithmetic that can be written down as rules.
Write every intermediate value into tables.
Commit to the tables.
Then let a random audit check the rules.
The rest of this video unpacks that line, one piece at a time.
"""),
    ("A1Honest", 1, """
One thing to say early, so you never expect something the system does not give.
The letters Z K name a family of proof systems. In this prototype nothing is hidden,
except the weights behind their commitment. No random blinding is added to the tables.
The architecture is public. The prompt ids are public.
It is a proof of correctness, not a privacy tool. Keep that in mind throughout.
"""),
    # ---------------------------------------------------------------- Act 2
    ("A2Layer", 2, """
Let us open the box. One token travels through one layer along what is called the residual
stream.
First a normalisation. Then the values are requantised to eight-bit integers.
Three matrix multiplies make queries, keys and values. Their results are dequantised back to
sixteen-bit floats. Queries and keys are rotated by position, then quantised again.
Then attention: each token looks at all the keys so far, and takes a weighted sum of the values.
The attention output is rounded to a twelve-bit integer, multiplied by one more matrix,
dequantised, and added back to the stream.
A second normalisation, two more matrix multiplies, a gate, one more multiply, and a second
addition to the stream.
That is one layer. Llama does it thirty-two times, then one final normalisation, one matrix
multiply to one hundred twenty-eight thousand scores, and the largest score wins.
"""),
    ("A2Fixed", 2, """
Why rerun the model at all? Because a real GPU kernel adds floating point numbers in an order
nobody wrote down, and rounds in ways nobody specified. A proof needs every operation to be a
rule with exactly one right answer.
So the harness reruns the model in a fixed arithmetic.
Activations are eight-bit integers with one scale per token. Weights are eight-bit integers
with one scale per output channel. Sums are exact.
Dequantisation is a chain of correctly rounded sixteen-bit float steps.
The softmax runs on integers: queries at twelve bits, keys at eleven, and the exponential is a
lookup table that returns a nine-bit numerator.
This arithmetic has a price. On twenty thousand scored tokens, the float model has a
perplexity of four point four one. The proved arithmetic has four point seven two.
That is seven percent worse, measured. A naive static eight-bit scheme, for comparison,
scores sixty-six.
"""),
    ("A2Requant", 2, """
Here is one requantisation with real numbers from the France prompt, at layer zero.
After the first normalisation, the largest magnitude among the four thousand ninety-six values
is four point zero three one two five.
Divide by one hundred twenty-seven, round up to the next sixteen-bit float: the scale for this
token is zero point zero three two.
Now every value is divided by that scale and rounded. Minus zero point three two becomes minus
ten. Zero point zero two becomes one. Most of the small ones become zero.
The weights get the same treatment, with one scale per output channel: the first row of the
query matrix becomes eleven, minus sixty-five, minus fourteen, minus forty, and so on.
Everything downstream is now integer arithmetic, and integer arithmetic has one right answer.
"""),
    ("A2Witness", 2, """
While the model reruns, nothing is thrown away. Every integer activation, every exact
accumulator, every float bit pattern, every attention score, every key and value, and the
residual stream going in and out of each layer, is written to disk.
This pile of values is called the witness. It is dumped per layer and per block of five
hundred twelve positions.
Here is the residual stream's size growing through the layers on the France prompt: tiny after
the embedding, about zero point one five by layer fourteen, zero point eight by layer
thirty-one, and two point two after the final normalisation.
And here is attention on the same prompt. At layer thirty-one, head zero, the last token "is"
attends half of its weight to itself and a fifth to "France". Attention is the one operation
whose cost grows with the length of the context. Remember that for the end.
"""),
    # ---------------------------------------------------------------- Act 3
    ("A3Tape", 3, """
Now the one piece of cryptography this video has to teach. We will do it with a toy.
A tape of eight cells: one, one, two, three, five, eight, thirteen, twenty-one.
The rule: every cell is the sum of the two before it.
A computation, for our purposes, is exactly this: a tape of values, and a rule that every hop
along the tape obeys.
"""),
    ("A3Curve", 3, """
Here is the first idea. Through any eight points there is exactly one polynomial of degree
below eight.
Place the eight cells at eight fixed positions, and draw the unique curve through them.
Call it P. The tape has become a curve, and the curve remembers every cell.
"""),
    ("A3Rule", 3, """
Second idea: apply the rule to the curve itself.
Define C of x as P at two steps ahead, minus P at one step ahead, minus P at x.
Wherever the rule holds, C is zero. That is at six positions: the first six hops.
Six separate facts about cells have become one statement about one curve.
"""),
    ("A3Divide", 3, """
Third idea: division. A polynomial that is zero at six known points is divisible by Z, the
polynomial whose roots are exactly those six points.
So C equals Z times some quotient Q, and the prover can compute Q.
Now change one cell. Say thirteen becomes fourteen. At that hop, C is fourteen minus eight
minus five, which is one, not zero. Z no longer divides C. There is no polynomial Q at all.
A single wrong cell anywhere destroys the quotient everywhere.
"""),
    ("A3Audit", 3, """
Fourth idea: the audit. The verifier picks a random position r, far outside the tape, and asks
for the values of P and Q there. Then it checks: C at r equals Z at r times Q at r.
Two different low degree polynomials can agree at only a few points. So a lie survives one
random question with probability about the degree divided by the size of the number field.
In this system the field is the integers modulo two to the thirty-one minus one, a Mersenne
prime, and the random positions are drawn from an extension with about two to the one hundred
twenty-four elements. One random question is enough to make a lie essentially impossible.
"""),
    ("A3Commit", 3, """
But wait. What stops the prover from inventing P after it sees the random position?
Commitment. Before any question is asked, the prover evaluates P on a bigger domain, twice as
many points as the tape, and hashes all those values into a Merkle tree: pairs of hashes,
hashed again, up to a single thirty-two byte root.
The root is published first. Later, when asked about position r, the prover opens the leaf at
r together with its path of hashes up to the root. Change any leaf, and the root changes.
"""),
    ("A3Fri", 3, """
One more thing the verifier needs: that the committed values really come from a low degree
polynomial, and not from a pointwise cheat that happens to pass at r.
That is the job of a protocol called FRI. It folds the polynomial in half, commits the half,
folds again, and so on, with random queries at every level.
Treat it as a black box with one promise: a committed list is low degree, checked with one
hundred random queries.
This system uses a blowup of two, one hundred queries and no proof of work, which its library
accounts as one hundred bits of conjectured security.
"""),
    ("A3FiatShamir", 3, """
There is no live verifier while the proof is made. So where does the randomness come from?
From a hash. The prover feeds every Merkle root into a hash function, Blake 2 s, and the
random position is the hash output.
Picture it as a grey box. Roots go in the slot. Dice come out of the tray.
Because the root goes in before the die comes out, the prover cannot fit its values to the
randomness. This box will come back in the next act.
"""),
    ("A3Scale", 3, """
Now scale up. The Fibonacci tape had one column and one rule.
A transformer layer segment has thousands of columns and hundreds of rules, which together are
called the A I R, the algebraic intermediate representation.
One field element, in one column, at one row, is called a cell. It is the unit of prover work.
A single proof here commits about one and a quarter billion cells.
Everything else is the same: commit, draw randomness, check the rules at random points.
"""),
    # ---------------------------------------------------------------- Act 4
    ("A4Segment", 4, """
What is the unit of proof? Not the whole request. A segment: one transformer layer, or the
output head, applied to one block of five hundred twelve positions, against the context of
all earlier positions.
A request with a four thousand ninety-six token prompt and five hundred twelve generated tokens
becomes a grid: nine token blocks, times thirty-two layers, plus the output head proved twice.
Two hundred ninety proofs, measured. There is no recursion. The proofs are chained by
something simpler, which act six shows.
"""),
    ("A4Trees", 4, """
Inside one segment proof there are five kinds of Merkle tree, committed in this order.
Tree zero, the shape tree: everything the rules read as a fact. Selectors, the causal mask,
the lookup tables, the rotation angles for this block's positions. It is a pure function of
public parameters, so the verifier rebuilds it and rejects on a root mismatch. No weight is
in it.
Tree one, the model tree: this layer's integer weights and scales. The verifier cannot derive
it, so it compares the root with the publisher's manifest.
Tree two, the base trace: everything the prover chose. Activations, accumulators, scores,
numerators, token ids. This is where most cells live.
Tree three, the interaction tree: lookup bookkeeping that depends on the random challenges.
And trees four and up, the boundary trees: the residual stream in and out, and the keys and
values this block wrote. Small trees whose only job is to be compared with a neighbour.
"""),
    ("A4Transcript", 4, """
Here is the transcript of one segment proof, with the hash box at the side.
Commit trees zero, one and two. Mix each root into the box.
Draw the challenges: a pair for every lookup table, the weights that fold whole matrices into
one number, and the binding challenge for the residual stream.
Build every lookup fraction. Run five sumcheck reductions. Commit tree three.
Commit the boundary trees.
Then the STARK itself: draw the out of domain point, evaluate every rule's quotient there, the
generated CUDA kernels do this, commit the composition polynomial, and run FRI.
Finally, write three documents: Fixed, the statement; Claims, every published sum; and the
proof, about sixty-five megabytes.
"""),
    ("A4Order", 4, """
Why is the order the whole argument? Rewind.
If the prover knew a challenge before committing, it could choose values that pass that
one challenge.
So every root goes into the box before the die that depends on it comes out.
That makes the byte order of the proof load bearing. The project turns it into a rule: the
S H A two fifty-six of the proof bytes must come out identical on the CPU backend and on the
GPU backend before any change is merged. They call it the digest gate.
"""),
    ("A4Bf16", 4, """
A small detail that shapes everything: how a sixteen-bit float is stored.
Because the blowup is only two, every rule must stay at low degree. So a float is not stored
as a bit pattern. It is stored as two cells: a signed significand between one hundred
twenty-eight and two hundred fifty-six, or zero, and an exponent field.
The value is the significand times two to the exponent minus one hundred thirty-four.
One point five is one hundred ninety-two times two to the minus seven. Zero is simply a
significand of zero.
"""),
    ("A4Cells", 4, """
How much is committed? Per proved position, at a context of four thousand ninety-six:
fifty-eight million cells in the base trace, eighteen million in the interaction tree, three
million in the boundary trees. About seventy-nine million fresh cells per position, measured.
Another twenty-three million model cells and four million shape cells are preprocessed and
cached, not paid again per segment.
At a context of sixteen thousand the fresh total rises to about one hundred five million per
position, because attention grows with the context.
"""),
    # ---------------------------------------------------------------- Act 5
    ("A5Freivalds", 5, """
Inside the table live three tricks. The first one handles matrix multiplication.
One layer has seven matrix multiplies over two hundred eighteen million weights. Writing a rule
for every output cell is hopeless.
Here is the trick, on a two by two toy. W is one, two, three, four. X is the vector one, one.
The honest product is three, seven. A prover claims three, eight.
After the claim is committed, the verifier draws a random vector r, and checks one equation:
r dot the claimed product, against r times W, dotted with X.
The left side is three r one plus eight r two. The right side is three r one plus seven r two.
They differ by r two. A random r two is zero with probability one in the field size.
"""),
    ("A5FreivaldsGeneral", 5, """
That is Freivalds' check: r transpose W X equals r transpose W, times X, at a random r.
It costs one pass over the weights, linear instead of cubic, and a wrong product survives
with probability about the degree divided by two to the one hundred twenty-four.
In the code, r is the powers of a drawn challenge. One gadget folds the committed inputs and
the preprocessed weights into one number per matrix. The dequantisation gadget folds the same
committed accumulators the other way. The verifier requires the two numbers to be equal.
Nothing is committed twice. And the weights come from tree one, the model tree, so the proof
is about the committed model and no other.
"""),
    ("A5LogUp", 5, """
The second trick handles everything that is not a polynomial rule. Is this float the
correctly rounded result? Is this numerator the exponential of this score? Is this value
below two to the fifteen?
Each of these is a table membership: the row I used must be a row of a table that was
committed before any challenge.
The toy. The table holds one, two, three. The prover used two, two, three. It commits a
multiplicity per table row: zero, two, one.
After a random z is drawn, both sides become sums of fractions.
The uses: one over z minus two, plus one over z minus two, plus one over z minus three.
The table: two over z minus two, plus one over z minus three. Equal, for every z.
Now cheat: use a four. That adds one over z minus four, a pole that no multiplicity over one,
two, three can ever cancel. The two sums differ at every z but a vanishing few.
This is called LogUp, and the running sums of these fractions are the interaction tree.
"""),
    ("A5Tables", 5, """
Rows with several columns are first folded into one number with a second challenge, alpha.
And here is a cost rule worth remembering: a table row costs one multiplicity cell plus one
fraction in the extension field, which is four base cells. Five cells a row, whether or not
the row is used.
Which tables? The normalisation and fraction tables that prove a correctly rounded float.
A table of all sixty-five thousand sixteen-bit inputs for the reciprocal square root, and
another for the gate function. The exponential table of the integer softmax, returning a
nine-bit numerator. Range tables for eight-bit activations and fifteen-bit comparisons.
And the whole embedding matrix, one hundred twenty-eight thousand rows by four thousand
ninety-six, is a table in tree one: selecting one row by a committed index costs one pass over
the table, almost all of it preprocessed.
"""),
    ("A5Gkr", 5, """
One sentence on the biggest optimisation. For the five largest lookup families the running
sums are not committed as columns at all. A sumcheck protocol, called G K R, proves them, and a
link ties its final claim back to the committed columns.
At a context of sixteen thousand this shrinks the interaction tree from ninety-three thousand
columns to five thousand six hundred.
Building these fractions and running the sumchecks is forty-two percent of proving time,
measured. It is the largest phase.
"""),
    ("A5Seams", 5, """
The third trick makes the gadgets talk about the same numbers.
Each gadget proves its own step correctly. Without a link, the prover could feed the matrix
multiply one input and the normalisation another, and each proof would be true about the
wrong numbers.
The link is a Horner claim. Under a challenge w drawn after commitment, a gadget publishes one
number: the sum of its output values, each weighted by a power of w. The next gadget publishes
the same sum over the values it consumed. The verifier compares the two numbers.
Equal sums under a random weight mean equal sequences, position by position.
Where a float producer meets an integer consumer, the requantisation step is proved as its own
component, called a seam, so the matrix multiply multiplies exactly the integers the producer
made.
"""),
    ("A5Edges", 5, """
Around one layer there are sixteen such links, called edges.
Seven bind the residual stream: the two normalisations read the committed stream, the adds and
the gate read the dequantised outputs, attention reads the rotated queries, keys and values,
and the output projection reads the attention output.
Three are seams: into the query, key and value multiplies, into the gate and up multiplies,
into the down multiply.
One is the attention component itself. One is the Freivalds check itself.
Two are boundaries: the residual stream to the next layer, and the keys and values to the next
block. Layer zero adds the embedding edge. The head adds the argmax edge. Sixteen.
Every edge is on by default. A witness that cannot state one is refused. A flag can turn one
off, loudly: the run's provenance lists it, and that run is a control, never a result.
"""),
    ("A5Argmax", 5, """
The argmax edge deserves a closer look, because greedy decoding takes the first maximal
index, and ties are real: on the recorded continuations, fifteen of five hundred twelve
positions had two or three equal top scores.
The prover commits the maximum's pattern, the emitted token, and an indicator b that is one
before the token and zero from the token on.
A range check on the maximum minus each score minus b says: strictly below the maximum before
the token, at most the maximum from the token on.
The indicator must be zero or one and never increase, and its sum must equal the token. That
sum is the binding itself.
A weaker form that only says "the token attains the maximum" exists as a flagged control.
It would let the prover pick the token on every tied row.
"""),
    # ---------------------------------------------------------------- Act 6
    ("A6Grid", 6, """
Now zoom out to the grid. Columns are token blocks, zero to eight. Rows are layers, zero to
thirty-one. Two head tiles sit over blocks seven and eight, because the first generated
token's argmax was computed at the last prompt position.
Every vertical arrow says: the residual stream root leaving this tile equals the residual
stream root entering the tile above. Two hundred eighty-one layer links.
Every horizontal arrow says: the keys and values this block wrote equal the prefix the next
block attended over. Two hundred fifty-six token links.
Five hundred thirty-seven links in all, measured. Layer zero also binds the embedding row, and
the head binds the emitted id.
"""),
    ("A6Roots", 6, """
Why a root and not a challenge? Each tile's internal claims are taken under a challenge drawn
inside that tile. Two tiles weigh their boundaries differently, so their claims cannot be
compared.
And the obvious repair, drawing the challenge from public data so both tiles share it, is
unsound: a challenge known before the values are committed makes "my image equals yours" one
linear equation the prover can simply solve.
So the exposed value is a Merkle root of the boundary values themselves, bound to the table by
a plain equality rule. The link check is five integer comparisons that pin the layout, then
one thirty-two byte comparison. Constant time. No recursion anywhere.
"""),
    ("A6Verifier", 6, """
What does the verifier actually do, per tile?
Parse the statement, the claims and the proof. Refuse if the shapes do not match the plan or
the security parameters drifted.
Replay the hash box and redraw every challenge. Verify the sumchecks. Run the STARK verifier:
out of domain sampling and FRI.
Check that every lookup's fractions cancel. Check every Freivalds equality, the attention
identities, and every binding equality.
Rebuild the shape tree from public parameters and compare its root. Compare the model root
with the published manifest.
Then the grid: every link, and every emitted id chained to the prompt or to a proved argmax.
"""),
    ("A6Cost", 6, """
What does verification cost? Over the two hundred ninety proofs, the verifier's own time on
the run host's CPU cores was one hundred nineteen seconds: a median of zero point four seconds
per segment, measured.
On a consumer class machine with four cores and no graphics card, one reference segment at a
context of sixteen thousand took forty-three seconds. Forty-two of those were spent rebuilding
the shape tree; checking the proof itself took under one second. Peak memory was twenty-eight
gigabytes.
The shape tree is the verifier's main cost, and a grid pays it once per layer and context
shape, not once per proof.
"""),
    # ---------------------------------------------------------------- Act 7
    ("A7Numbers", 7, """
The numbers, for one request on one H100: a four thousand ninety-six token prompt and five
hundred twelve generated tokens.
Two hundred ninety segments. The proving loop took sixty-one minutes; the whole run, with
extraction, ninety-one minutes. That is one point two five positions per second.
At three dollars twenty-nine per GPU hour, between three and five dollars per request.
Unproved serving with vLLM handles the same request at about thirteen hundred positions per
second end to end. The overhead is roughly a thousand times.
The proofs add up to eighteen and a half gigabytes, about sixty-five megabytes per segment.
At a context of sixteen thousand: one thousand fifty-eight segments, six hours of loop time,
and one hundred nine gigabytes of proofs. All measured.
"""),
    ("A7Time", 7, """
Where does the time go? From a serial loop over thirty-two layer segments:
building the lookup fractions and running the sumchecks, forty-two percent. Building the base
trace, thirty-five percent. Loading and decoding the witness, twelve percent. Other host work,
six percent. And the STARK itself, the commit and the prove: under five percent.
The cryptography is the cheap part. Building the tables on the host is the ceiling.
Moving constraint evaluation to the GPU is already done: with those kernels left on the CPU the
same loop took over six times longer.
The published projections for larger models, from the cost model, not measurements: a
seventy billion parameter model in the order of five to eight hours per request, four hundred
five billion, sixteen to twenty-four hours.
"""),
    ("A7Honesty", 7, """
Seven things this proof is not, in the project's own words.
One. Not hiding. Only the weights are hidden, behind their root.
Two. Not the served model. It proves a quantised stand-in, seven percent worse in perplexity.
Three. Greedy only. Sampling and early stopping are outside the statement.
Four. Ids, not text. The tokeniser is unproved.
Five. No binding to traffic. It proves ids map to ids under a commitment, not that anyone was
served this answer.
Six. Not formally verified. What exists is the digest gate, negative controls and self-tests.
Seven. A measurement tool. Quote: not something anyone should rely on yet. Nobody outside our
team has checked the correctness of our implementation.
"""),
    ("A7Next", 7, """
What is next, in the authors' framing. Move witness generation to the GPU. Real seventy and
four hundred five billion parameter runs. Close the gap to real serving: float arithmetic,
tokenisation, batching, binding to traffic records.
And prove only a random sample of segments after the provider commits to boundary roots.
Their sampling argument: prove one percent of requests, and a provider who cheats repeatedly
is caught with ninety-nine percent probability after about four hundred sixty cheats.
Now you can read the one sentence we started from. For these published prompt ids, under the
model whose weight commitment is this root, greedy decoding in this fixed arithmetic produces
these five hundred twelve ids. Every word in it now has a picture behind it.
"""),
]


def words():
    return sum(len(t.split()) for _, _, t in SCENES)


if __name__ == "__main__":
    print(len(SCENES), "scenes,", words(), "words")
