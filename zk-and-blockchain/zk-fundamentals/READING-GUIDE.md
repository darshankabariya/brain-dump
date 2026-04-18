# How to Read ZK Tweets & Blogs

> **Your guide to understanding ZK content on Twitter, blogs, and forums**

## When You See a Tweet About...

### "We just deployed to mainnet!"

**What to check:**
1. Which ZK rollup? (zkSync, StarkNet, Polygon zkEVM, Scroll, etc.)
2. What type of zkEVM? (Type 1-4)
3. What proof system? (PLONK, STARKs, Halo2)
4. TVL (Total Value Locked)?

**Where to learn more:** `04-COMPANIES-AND-PROJECTS.md`

---

### "New proof system breakthrough!"

**What to check:**
1. SNARK or STARK?
2. Proof size vs verification time trade-off
3. Trusted setup required?
4. Recursion support?

**Where to learn more:** `02-TECHNICAL-CONCEPTS.md`, `QUICK-REFERENCE.md`

---

### "Research paper published"

**What to check:**
1. Who are the authors? (Check if they're key researchers)
2. What problem does it solve?
3. Is it theoretical or practical?
4. Any implementations yet?

**Where to learn more:** `03-RESEARCH-AND-RESEARCHERS.md`

---

### "New ZK application launched"

**What to check:**
1. Category: Scaling, Privacy, Identity, Gaming, DeFi?
2. Which platform? (zkSync, StarkNet, standalone?)
3. What does it prove?
4. Is it production-ready?

**Where to learn more:** `05-APPLICATIONS-AND-USE-CASES.md`

---

### "Funding announcement: $XXM raised"

**What to check:**
1. What do they build?
2. Who invested? (Paradigm, a16z, Sequoia = serious)
3. What's their tech stack?
4. Mainnet or still in development?

**Where to learn more:** `04-COMPANIES-AND-PROJECTS.md`

---

## Common Tweet Patterns Decoded

### Pattern 1: Technical Announcement

```
"Excited to announce Plonky3 with 10x faster proving!"
```

**How to understand:**
1. Look up "Plonky3" in `GLOSSARY.md`
2. Check what Plonky2 was (predecessor)
3. Understand it's a STARK framework
4. "10x faster" = prover time improvement

**Context needed:** `02-TECHNICAL-CONCEPTS.md` (Plonky2 section)

---

### Pattern 2: Comparison Thread

```
"🧵 Thread on SNARKs vs STARKs..."
```

**How to understand:**
1. Open `QUICK-REFERENCE.md` for quick comparison
2. Read `02-TECHNICAL-CONCEPTS.md` for details
3. Check `06-VISUAL-GUIDES/proof-systems-comparison.md` for visuals

**Key points to look for:**
- Proof size
- Verification time
- Trusted setup
- Quantum resistance

---

### Pattern 3: Application Showcase

```
"Built a ZK passport verifier using Noir!"
```

**How to understand:**
1. "ZK passport" = Identity application (`05-APPLICATIONS-AND-USE-CASES.md`)
2. "Noir" = Programming language by Aztec (`GLOSSARY.md`)
3. Use case: Prove passport validity without revealing data

**Context needed:** `05-APPLICATIONS-AND-USE-CASES.md` (Identity section)

---

### Pattern 4: Research Discussion

```
"Thaler's new paper on lookup arguments is 🔥"
```

**How to understand:**
1. "Thaler" = Justin Thaler, key researcher (`03-RESEARCH-AND-RESEARCHERS.md`)
2. "Lookup arguments" = Efficient table lookups in ZK (`GLOSSARY.md`)
3. Check his recent work (Lasso, Jolt)

**Context needed:** `03-RESEARCH-AND-RESEARCHERS.md`

---

### Pattern 5: Ecosystem Update

```
"zkSync TVL hits $500M!"
```

**How to understand:**
1. "zkSync" = Type 4 zkEVM rollup (`04-COMPANIES-AND-PROJECTS.md`)
2. "TVL" = Total Value Locked (adoption metric)
3. $500M = significant traction

**Context needed:** `04-COMPANIES-AND-PROJECTS.md` (zkSync section)

---

## Blog Post Reading Strategy

### 1. Scan the Introduction

**Look for:**
- What problem is being solved?
- Is it scaling, privacy, or something else?
- Which proof system is used?

**Quick lookup:** `00-ZK-ECOSYSTEM-OVERVIEW.md`

---

### 2. Identify Key Terms

**Common terms you'll see:**
- Circuit, constraint, witness, proof, verifier
- SNARK, STARK, zkEVM, zkVM
- Groth16, PLONK, Halo2, STARKs

**Quick lookup:** `GLOSSARY.md` or `QUICK-REFERENCE.md`

---

### 3. Understand the Tech Stack

**Questions to answer:**
- What proof system? (Groth16, PLONK, STARKs, etc.)
- What language? (Circom, Noir, Cairo, etc.)
- What platform? (zkSync, StarkNet, standalone, etc.)

**Quick lookup:** `02-TECHNICAL-CONCEPTS.md`

---

### 4. Check the Use Case

**Categories:**
- Scaling (rollups)
- Privacy (shielded transactions)
- Identity (zkPassport, ZK Email)
- DeFi (private trading, lending)
- Gaming (Dark Forest)
- Governance (MACI)

**Quick lookup:** `05-APPLICATIONS-AND-USE-CASES.md`

---

### 5. Evaluate Credibility

**Check:**
- Who wrote it? (Known researcher/company?)
- Is there code/implementation?
- Peer-reviewed or just claims?
- Community reception?

**Quick lookup:** `03-RESEARCH-AND-RESEARCHERS.md`

---

## Twitter Accounts to Follow (by Category)

### Researchers
- @danboneh (Dan Boneh)
- @jthaler (Justin Thaler)
- @EliBenSasson (Eli Ben-Sasson)
- @VitalikButerin (Vitalik)
- @barrywhitehat (Barry WhiteHat)

### Companies
- @zksync (zkSync)
- @StarkWareLtd (StarkWare)
- @0xPolygon (Polygon)
- @Scroll_ZKP (Scroll)
- @aztecnetwork (Aztec)
- @succinctlabs (Succinct)
- @risczero (RISC Zero)

### Community
- @PrivacyScaling (PSE)
- @0xPARC
- @zkvalidator (ZK news)

---

## Common Confusion Points in Tweets

### "ZK rollup vs Optimistic rollup"

**Quick answer:**
- **ZK rollup**: Validity proofs (instant finality, more complex)
- **Optimistic rollup**: Fraud proofs (7-day withdrawal, simpler)

**Detail:** `00-ZK-ECOSYSTEM-OVERVIEW.md`

---

### "Type 1 vs Type 4 zkEVM"

**Quick answer:**
- **Type 1**: 100% Ethereum compatible (slower)
- **Type 4**: ~90% compatible (faster)

**Detail:** `02-TECHNICAL-CONCEPTS.md` (zkEVM section)

---

### "Trusted setup - is it bad?"

**Quick answer:**
- Not necessarily bad if done correctly
- Universal setup (PLONK) better than circuit-specific (Groth16)
- No setup (STARKs, Halo2) is ideal but has trade-offs

**Detail:** `02-TECHNICAL-CONCEPTS.md`

---

### "Quantum resistant - why does it matter?"

**Quick answer:**
- Future-proofing against quantum computers
- STARKs are quantum-resistant, SNARKs aren't
- Not urgent now, but important long-term

**Detail:** `02-TECHNICAL-CONCEPTS.md`

---

## How to Fact-Check ZK Claims

### Claim: "Our proof system is 100x faster!"

**Check:**
1. Faster at what? (Proving, verification, or both?)
2. Compared to what? (Groth16, PLONK, STARKs?)
3. What's the trade-off? (Proof size, setup, security?)
4. Is there code/benchmarks?

**Reference:** `02-TECHNICAL-CONCEPTS.md` (Performance section)

---

### Claim: "First ZK [application]"

**Check:**
1. Search in `05-APPLICATIONS-AND-USE-CASES.md`
2. Check if similar apps exist
3. What's actually novel?

---

### Claim: "No trusted setup!"

**Check:**
1. What proof system? (STARKs, Halo2 = no setup)
2. Is it truly transparent?
3. What's the trade-off? (Usually larger proofs)

**Reference:** `QUICK-REFERENCE.md`

---

## Reading Technical Papers

### Step 1: Abstract & Introduction (5 min)
- What's the problem?
- What's the solution?
- What's the improvement?

### Step 2: Skim Results (5 min)
- Performance numbers
- Comparison to prior work
- Limitations

### Step 3: Decide if Worth Deep Dive
- Relevant to your interests?
- Practical or theoretical?
- Implementation available?

### Step 4: Deep Dive (if yes)
- Read construction
- Understand security proof
- Check implementation

**Guide:** `03-RESEARCH-AND-RESEARCHERS.md` (How to Read Papers section)

---

## Quick Decision Tree: "Should I Read This?"

```
Is it about ZK?
    ↓ YES
Is it relevant to my interests?
    ↓ YES
Is it from credible source?
    ↓ YES
Do I understand the basics?
    ↓ NO → Read 00-ZK-ECOSYSTEM-OVERVIEW.md first
    ↓ YES
Read it! Use this guide to look up unfamiliar terms.
```

---

## Bookmark These for Quick Reference

1. **Unfamiliar term?** → `GLOSSARY.md`
2. **Need quick facts?** → `QUICK-REFERENCE.md`
3. **Company mentioned?** → `04-COMPANIES-AND-PROJECTS.md`
4. **Researcher mentioned?** → `03-RESEARCH-AND-RESEARCHERS.md`
5. **Application mentioned?** → `05-APPLICATIONS-AND-USE-CASES.md`
6. **Technical detail?** → `02-TECHNICAL-CONCEPTS.md`

---

## Practice Exercise

**Try reading this tweet:**

> "Excited to share that our Type 2 zkEVM using Halo2 just processed 10k TPS on testnet! No trusted setup, full EVM compatibility. Mainnet Q1 2025."

**How to decode:**
1. "Type 2 zkEVM" → Check `02-TECHNICAL-CONCEPTS.md` (EVM-equivalent)
2. "Halo2" → Check `GLOSSARY.md` (No trusted setup SNARK)
3. "10k TPS" → High throughput claim (verify when mainnet)
4. "Full EVM compatibility" → Type 2 means bytecode-level compatibility
5. "No trusted setup" → Halo2 property (transparent)

**Verdict:** Promising if true. Check for code/benchmarks. Follow for mainnet launch.

---

**Happy reading! Use this guide whenever you encounter ZK content.** 🚀
