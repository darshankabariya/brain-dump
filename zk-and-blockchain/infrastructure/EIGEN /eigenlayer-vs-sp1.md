# SP1 vs EigenLayer: What They Do and How They Differ

## 1. One‑line Intuition

- **SP1 (Succinct)** → *"Make computations ZK‑verifiable"*
  - You run a program in a zkVM and get a **cryptographic proof** that it ran correctly.

- **EigenLayer** → *"Reuse Ethereum’s economic security"*
  - You use **restaked ETH and operators** to secure **off‑chain services (AVSs)** by slashing them if they misbehave.

They both extend what Ethereum can secure, but:

- SP1 secures **correct computation** via **ZK proofs**.
- EigenLayer secures **correct behavior** via **economic incentives + slashing**.

They are complementary, not competitors.

---

## 2. Analogy

### Cloud Analogy

- **SP1** is like:
  > A service that gives you a **mathematical certificate** that your code ran correctly.
  > Anyone can check the certificate cheaply without re‑running the code.

- **EigenLayer** is like:
  > A network of **servers with deposits**. If they misbehave, they **lose money**.
  > You trust them because it’s expensive to cheat.

### Court Analogy

- **SP1 (Proof‑based)**
  - You bring a **mathematical proof** to court.
  - The judge just checks the proof; if it verifies, the judge knows the computation was correct.

- **EigenLayer (Stake‑based)**
  - You rely on **a panel of security guards with big bonds**.
  - If they lie or cheat, they lose their bond (slashed).

---

## 3. What They Actually Are

### SP1 (Succinct zkVM)

- **What:** Zero‑knowledge virtual machine.
- **Input:** A program (Rust → RISC‑V) + inputs.
- **Output:**
  - Program output.
  - ZK proof:
    > "This program ran correctly on these inputs and produced this output."
- **Verification:** Cheap on‑chain or off‑chain.

**Example:**

```text
Program: Verify Ethereum light client
Input: Sequence of block headers
SP1 Proves: "These headers are a valid chain under Ethereum's consensus rules."
Output: Latest valid header + proof
On-chain: Contract verifies proof, updates stored header
```

You don’t trust a committee; you trust the **math**.

---

### EigenLayer

- **What:** Restaking + AVS (Actively Validated Services) platform.
- **Core ideas:**
  - Users restake ETH (via LSTs or native restaking).
  - Operators run **AVSs** (oracles, DA layers, bridges, etc.).
  - If operators cheat, their stake can be **slashed**.

**AVS Examples:**
- Oracle networks
- Data availability layers
- Bridges
- Off‑chain compute networks

You don’t get a ZK proof; you get **economic security + slashing conditions**.

---

## 4. How They Secure Things (Side‑by‑Side)

### SP1 Security Model

- Security comes from **cryptography**:
  - As long as the ZK proof system is sound, a valid proof means the computation is correct.
  - There is **no trust in a committee** to behave honestly.

```text
If proof verifies → computation is correct
If proof doesn’t verify → reject
No middle ground
```

### EigenLayer Security Model

- Security comes from **economic incentives**:
  - You assume a majority of staked value will behave honestly because cheating is expensive.
  - If an AVS detects misbehavior → slash operator stakes.

```text
If most staked operators are honest → AVS behaves correctly
If large collusion or broken incentives → AVS can be corrupted
```

---

## 5. Example 1: Cross‑Chain Bridge

### A. Bridge with SP1 (ZK‑based)

**Goal:** Destination chain wants to know Ethereum state is correct.

1. Implement an Ethereum light client in Rust.
2. Run it inside SP1.
3. SP1 outputs:
   - `latest_header`
   - `zk_proof`
4. Destination chain contract:
   - Verifies `zk_proof`.
   - Updates stored Ethereum header.

**Security:**
- As long as ZK proof system is sound, the header is correct.
- No need to trust a committee of signers.

### B. Bridge with EigenLayer (Restaking‑based)

**Goal:** Same: know Ethereum state on another chain.

1. An AVS (bridge service) runs off‑chain.
2. EigenLayer operators observe Ethereum chain.
3. Operators sign claims like:
   > "Block X has state root Y".
4. If later it’s proven they lied → AVS slashes their restaked ETH.
5. Destination chain contract trusts the signatures from this AVS.

**Security:**
- As long as majority of restaked stake is honest → safe.
- If enough stake colludes, they can lie (but lose money if caught).

### Difference in Feel

- **SP1 bridge:**
  - Trust = cryptographic proof.
  - Bad actors cannot produce a valid proof for an invalid state.

- **EigenLayer bridge:**
  - Trust = economic security of stakers.
  - Bad actors *can* lie, but they risk being slashed.

They can **even be combined**:
- AVS uses SP1 internally to generate proofs.
- EigenLayer ensures operators actually run SP1 correctly / timely.

---

## 6. Example 2: Off‑Chain Compute Service

### With SP1 (ZK Coprocessor)

**Scenario:** DEX wants complex risk computation.

1. DEX defines function `f(params, market_data) → result` in Rust.
2. Service runs `f` inside SP1.
3. Outputs `(result, zk_proof)`.
4. DEX contract verifies `zk_proof` and trusts `result`.

- No operator trust needed.
- Anyone can run the compute and prove correctness.

### With EigenLayer (Restaked Compute AVS)

1. AVS operators run `f` off‑chain.
2. They sign `result` and submit to the contract.
3. If later proven wrong, they are slashed.

- You trust the AVS + slashing logic.
- No cryptographic guarantee per execution.

---

## 7. Where They Sit in Your Mental Stack

```text
             ┌────────────────────────────────┐
             │   Your Application / Protocol  │
             └────────────────┬───────────────┘
                              │
          ┌───────────────────┴─────────────────────┐
          │                                         │
┌─────────▼─────────┐                    ┌──────────▼─────────┐
│  SP1 (zkVM)       │                    │  EigenLayer        │
│  • Prove code     │                    │  • Restaked ETH    │
│  • Output proof   │                    │  • AVS + operators │
└─────────┬─────────┘                    └──────────┬─────────┘
          │                                         │
┌─────────▼─────────┐                    ┌──────────▼─────────┐
│  On-chain verifier│                    │  AVS contracts     │
│  • Checks proof   │                    │  • Checks sigs     │
└────────────────────┘                    └────────────────────┘
```

- **SP1**: Cryptographic correctness of computation.
- **EigenLayer**: Economic security + slashing for off‑chain services.

You can:
- Use **SP1 alone**.
- Use **EigenLayer alone**.
- Or **combine them** for stronger guarantees.

---

## 8. Short Answer to Your Intuition

> *"EigenLayer doing same thing as SP1, making any software verifiable?"*

- **Similar goal at a high level:** extend what can be considered "trustworthy" off‑chain.
- **But different mechanisms:**
  - SP1 → **verifiable by math** (ZK proofs).
  - EigenLayer → **verifiable by incentives** (stake + slashing).

So EigenLayer doesn’t make software *cryptographically ZK‑verifiable* in the SP1 sense; it makes software **economically accountable** via restaked ETH.

---

## 9. How This Fits Your `infrastructure/` Directory

This file is meant as a **conceptual comparison** so you can:
- Keep SP1 (Succinct) and EigenLayer clearly separated in your mental model.
- Reuse analogies (court, cloud, bridge examples) when explaining to others.
- See where they can be combined in future designs.
