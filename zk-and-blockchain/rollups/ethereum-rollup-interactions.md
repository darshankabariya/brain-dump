# Ethereum Rollup Interactions: A Comprehensive Guide

## Table of Contents
1. [Types of Rollups](#types-of-rollups)
2. [How Ethereum Interacts with Rollups](#how-ethereum-interacts-with-rollups)
3. [Ethereum Upgrades for Rollups](#ethereum-upgrades-for-rollups)
4. [Rollup Comparison Matrix](#rollup-comparison-matrix)
5. [Technical Deep Dive](#technical-deep-dive)

---

## Types of Rollups

### 1. **Optimistic Rollups**
Assume transactions are valid by default and use fraud proofs to challenge invalid transactions.

**Examples:**
- **Arbitrum** (Arbitrum One, Arbitrum Nova)
- **Optimism** (OP Mainnet)
- **Base** (Built on OP Stack)
- **Blast, Mode, Zora** (OP Stack variants)

**Key Characteristics:**
- 7-day challenge period for withdrawals
- Lower computational overhead
- EVM-equivalent or EVM-compatible
- Fraud proof mechanism

### 2. **ZK Rollups (Zero-Knowledge Rollups)**
Use cryptographic proofs (validity proofs) to prove transaction correctness.

#### 2a. **zkEVM Rollups**
**Examples:**
- **zkSync Era** (zkEVM using custom VM)
- **Polygon zkEVM** (Type 2/3 zkEVM)
- **Scroll** (Type 2 zkEVM, bytecode-level compatible)
- **Linea** (ConsenSys, Type 2 zkEVM)
- **Taiko** (Type 1 zkEVM, most Ethereum-equivalent)

**Key Characteristics:**
- EVM compatibility at various levels
- Faster finality (minutes to hours)
- SNARK or STARK proofs
- No challenge period

#### 2b. **ZK Rollups with Custom VMs**
**Examples:**
- **StarkNet** (Cairo VM, uses STARKs)
- **Aztec** (Privacy-focused, custom VM)
- **Miden** (Polygon, STARK-based, custom VM)

**Key Characteristics:**
- Not EVM-compatible (require custom languages)
- Optimized for specific use cases
- Better performance for certain operations
- Require transpilation or custom development

### 3. **Validium / Hybrid Solutions**
Store data off-chain but post proofs on-chain.

**Examples:**
- **StarkEx** (Data availability off-chain)
- **Immutable X** (Gaming-focused)
- **Polygon Miden** (Hybrid approach)

---

## How Ethereum Interacts with Rollups

### Core Interaction Model

Ethereum acts as a **settlement and data availability layer** for rollups. Here's how:

```
┌─────────────────────────────────────────────────────────┐
│                    ROLLUP LAYER                         │
│  (Executes transactions, maintains state)               │
│                                                         │
│  Examples: Arbitrum, zkSync, Optimism, etc.            │
└─────────────────┬───────────────────────────────────────┘
                  │
                  │ Posts:
                  │ 1. Transaction data (calldata/blobs)
                  │ 2. State roots
                  │ 3. Proofs (ZK proofs or fraud proofs)
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│              ETHEREUM LAYER 1                           │
│                                                         │
│  • Stores rollup data                                  │
│  • Verifies proofs                                     │
│  • Manages deposits/withdrawals                        │
│  • Provides security & finality                        │
└─────────────────────────────────────────────────────────┘
```

### Key Components on Ethereum

#### 1. **Rollup Smart Contracts**
Each rollup deploys contracts on Ethereum L1:

- **State Root Contract**: Stores the current state root of the rollup
- **Bridge Contracts**: Handle deposits and withdrawals (L1 ↔ L2)
- **Sequencer/Proposer Contract**: Manages who can submit batches
- **Verifier Contract**: Validates proofs (for ZK rollups)
- **Challenge Contract**: Handles fraud proofs (for Optimistic rollups)

#### 2. **Data Posting**
Rollups post transaction data to Ethereum:

**Before EIP-4844 (Pre-Dencun):**
```solidity
// Posted as calldata
function submitBatch(bytes calldata batchData) external {
    // Expensive: ~16 gas per byte
}
```

**After EIP-4844 (Post-Dencun, March 2024):**
```solidity
// Posted as blob data
function submitBatch(bytes32 blobHash) external {
    // Cheaper: blob data stored temporarily
    // ~1 gas per byte equivalent
}
```

#### 3. **Proof Verification**

**Optimistic Rollups:**
```solidity
contract OptimisticRollup {
    mapping(uint256 => StateRoot) public stateRoots;
    uint256 constant CHALLENGE_PERIOD = 7 days;
    
    function proposeStateRoot(bytes32 root) external {
        // Anyone can propose
        stateRoots[blockNumber] = StateRoot(root, block.timestamp);
    }
    
    function challengeStateRoot(uint256 blockNumber, bytes proof) external {
        // Challenge within 7 days
        require(block.timestamp < stateRoots[blockNumber].timestamp + CHALLENGE_PERIOD);
        // Fraud proof verification logic
    }
}
```

**ZK Rollups:**
```solidity
contract ZKRollup {
    IVerifier public verifier; // SNARK/STARK verifier
    
    function submitBatch(
        bytes32 newStateRoot,
        bytes calldata proof,
        bytes calldata publicInputs
    ) external {
        // Verify ZK proof on-chain
        require(verifier.verify(proof, publicInputs), "Invalid proof");
        
        // Update state root immediately (no challenge period)
        currentStateRoot = newStateRoot;
    }
}
```

---

## Ethereum Upgrades for Rollups

### Does Ethereum Need Specific Upgrades for Different Rollups?

**Short Answer:** No, Ethereum doesn't need specific upgrades for individual rollups, but it has implemented **general upgrades** that benefit ALL rollups.

### Key Ethereum Upgrades Supporting Rollups

#### 1. **EIP-4844: Proto-Danksharding (Dencun Upgrade, March 2024)**

**What it does:**
- Introduces "blob-carrying transactions" (blob space)
- Temporary data storage (~18 days) for rollup data
- Reduces rollup costs by 10-100x

**Impact on Rollups:**
```
Before EIP-4844:
- Calldata cost: ~16 gas/byte
- Typical rollup transaction: $0.50-$5.00

After EIP-4844:
- Blob cost: ~1 gas/byte equivalent
- Typical rollup transaction: $0.01-$0.50
```

**Beneficiaries:** ALL rollups (Arbitrum, Optimism, zkSync, Polygon zkEVM, Scroll, Linea, Base, StarkNet, etc.)

#### 2. **EIP-1559: Fee Market Reform (London, August 2021)**

**Impact:**
- More predictable gas fees
- Better fee estimation for rollup sequencers
- Helps rollups manage L1 posting costs

#### 3. **EIP-4488: Reduced Calldata Costs (Proposed, not implemented)**

**Status:** Superseded by EIP-4844
**Would have:** Reduced calldata gas costs specifically for rollups

#### 4. **Future: Full Danksharding (EIP-4844 → Full Danksharding)**

**Timeline:** 2025-2026+
**What it will do:**
- Increase blob space from ~0.375 MB/block to ~16 MB/block
- Further reduce rollup costs
- Enable more rollup throughput

**Target:** 16 MB/block = ~1.3 GB/day of rollup data

#### 5. **Future: Verkle Trees (Planned)**

**Impact:**
- Smaller state proofs
- Easier for rollups to verify L1 state
- Better for cross-rollup communication

#### 6. **Future: Proposer-Builder Separation (PBS) & MEV Improvements**

**Impact:**
- Better MEV protection for rollup users
- More efficient block building
- Fairer transaction ordering

---

## Rollup Comparison Matrix

| Rollup | Type | Proof System | EVM Compatibility | L1 Data | Finality | Main Use Case |
|--------|------|--------------|-------------------|---------|----------|---------------|
| **Arbitrum One** | Optimistic | Fraud Proofs | EVM-equivalent | Calldata/Blobs | 7 days | General purpose |
| **Arbitrum Nova** | Optimistic | Fraud Proofs | EVM-equivalent | AnyTrust (DAC) | 7 days | Gaming, social |
| **Optimism** | Optimistic | Fraud Proofs | EVM-equivalent | Calldata/Blobs | 7 days | General purpose |
| **Base** | Optimistic | Fraud Proofs | EVM-equivalent | Calldata/Blobs | 7 days | Coinbase ecosystem |
| **zkSync Era** | ZK | SNARK (PLONK) | EVM-compatible | Calldata/Blobs | Hours | General purpose |
| **Polygon zkEVM** | ZK | SNARK | EVM-equivalent | Calldata/Blobs | Hours | General purpose |
| **Scroll** | ZK | SNARK | EVM-equivalent | Calldata/Blobs | Hours | General purpose |
| **Linea** | ZK | SNARK | EVM-equivalent | Calldata/Blobs | Hours | ConsenSys ecosystem |
| **StarkNet** | ZK | STARK | Cairo VM (custom) | Calldata/Blobs | Hours | Custom apps, gaming |
| **Aztec** | ZK | SNARK | Custom VM | Calldata/Blobs | Hours | Privacy |
| **Miden** | ZK | STARK | Custom VM | Hybrid | Hours | High-performance |
| **Taiko** | ZK | SNARK | Type-1 zkEVM | Calldata/Blobs | Hours | Most Ethereum-like |

---

## Technical Deep Dive

### 1. Rollup Architecture Components

```
┌─────────────────────────────────────────────────────────┐
│                  ROLLUP ARCHITECTURE                    │
└─────────────────────────────────────────────────────────┘

┌──────────────┐
│   USERS      │ Submit transactions
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────────────────────┐
│  SEQUENCER                                           │
│  • Orders transactions                               │
│  • Executes state transitions                        │
│  • Provides soft confirmations                       │
└──────┬───────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────┐
│  BATCH SUBMISSION                                    │
│  • Compresses transaction data                       │
│  • Posts to Ethereum L1 (calldata or blobs)         │
└──────┬───────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────┐
│  PROOF GENERATION (ZK) or CHALLENGE PERIOD (Opt)    │
│  • ZK: Generate validity proof                       │
│  • Optimistic: Wait for challenges                   │
└──────┬───────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────┐
│  ETHEREUM L1                                         │
│  • Stores data                                       │
│  • Verifies proofs                                   │
│  • Finalizes state                                   │
└──────────────────────────────────────────────────────┘
```

### 2. How Each Rollup Type Interacts with Ethereum

#### Optimistic Rollups (Arbitrum, Optimism, Base)

```javascript
// Simplified interaction flow

// 1. Sequencer submits batch to L1
function submitBatch(bytes batchData) {
    // Post transaction data to L1
    // Cost: ~0.001-0.01 ETH per batch (with blobs)
    emit BatchSubmitted(batchNumber, batchData);
}

// 2. State root proposal
function proposeStateRoot(bytes32 newRoot) {
    stateRoots[batchNumber] = StateRoot({
        root: newRoot,
        timestamp: block.timestamp,
        status: Status.Pending
    });
}

// 3. Challenge mechanism (if fraud detected)
function provefraud(
    uint256 batchNumber,
    bytes fraudProof
) {
    // Interactive fraud proof game
    // If successful, batch is reverted
}

// 4. Finalization (after 7 days)
function finalizeBatch(uint256 batchNumber) {
    require(block.timestamp > stateRoots[batchNumber].timestamp + 7 days);
    stateRoots[batchNumber].status = Status.Finalized;
}
```

**Ethereum Requirements:**
- ✅ Standard EVM execution (no special opcodes)
- ✅ Calldata or blob storage
- ✅ Time-based logic for challenge periods
- ❌ No special L1 upgrades needed

#### ZK Rollups (zkSync, Polygon zkEVM, Scroll, Linea)

```javascript
// Simplified interaction flow

// 1. Sequencer submits batch + proof to L1
function commitBatch(
    bytes batchData,
    bytes32 newStateRoot,
    bytes zkProof,
    bytes publicInputs
) {
    // Post data to L1
    emit BatchCommitted(batchNumber, batchData);
    
    // Verify ZK proof on-chain
    require(
        verifier.verify(zkProof, publicInputs),
        "Invalid proof"
    );
    
    // Update state root immediately (no waiting!)
    currentStateRoot = newStateRoot;
    
    emit StateRootUpdated(newStateRoot);
}

// 2. Proof verification (happens on L1)
contract Verifier {
    function verify(
        bytes proof,
        bytes publicInputs
    ) returns (bool) {
        // Verify SNARK/STARK proof
        // Uses pairing operations (bn254 curve)
        // Gas cost: 200k-500k gas
        return verifyProof(proof, publicInputs);
    }
}
```

**Ethereum Requirements:**
- ✅ Precompiled contracts for elliptic curve operations (already exists)
- ✅ Sufficient gas limits for proof verification
- ✅ Calldata or blob storage
- ❌ No special L1 upgrades needed per rollup

#### StarkNet (STARK-based, Custom VM)

```javascript
// StarkNet uses STARKs (different from SNARKs)

function updateState(
    uint256[] programOutput,
    bytes starkProof
) {
    // Verify STARK proof
    // STARKs are quantum-resistant
    // Larger proof size but no trusted setup
    require(
        starkVerifier.verify(programOutput, starkProof),
        "Invalid STARK proof"
    );
    
    // Update state
    stateRoot = programOutput[0];
}
```

**Ethereum Requirements:**
- ✅ Uses custom STARK verifier contract
- ✅ No special L1 features needed
- ✅ Works with standard Ethereum

### 3. Data Availability Strategies

```
┌─────────────────────────────────────────────────────────┐
│           DATA AVAILABILITY SPECTRUM                    │
└─────────────────────────────────────────────────────────┘

Full On-Chain (Most Secure, Most Expensive)
├── Calldata (Pre-EIP-4844)
│   └── Used by: All rollups before March 2024
│
├── Blobs (Post-EIP-4844)
│   └── Used by: Most rollups after March 2024
│       • Arbitrum, Optimism, Base
│       • zkSync, Polygon zkEVM, Scroll, Linea
│       • StarkNet
│
Hybrid
├── Validium (Proofs on-chain, data off-chain)
│   └── Used by: StarkEx, some Polygon solutions
│
├── Data Availability Committees (DAC)
│   └── Used by: Arbitrum Nova
│
Off-Chain (Least Secure, Cheapest)
└── Centralized storage
    └── Not used by major rollups
```

### 4. Bridge Mechanisms

All rollups use similar bridge patterns:

```solidity
// L1 → L2 Deposit
contract L1Bridge {
    function depositETH() payable external {
        // Lock ETH on L1
        emit DepositInitiated(msg.sender, msg.value);
        
        // Message sent to L2 (via rollup inbox)
        // L2 will mint equivalent amount
    }
    
    function depositERC20(address token, uint256 amount) external {
        // Lock tokens on L1
        IERC20(token).transferFrom(msg.sender, address(this), amount);
        emit TokenDepositInitiated(msg.sender, token, amount);
    }
}

// L2 → L1 Withdrawal
contract L2Bridge {
    function withdrawETH(uint256 amount) external {
        // Burn ETH on L2
        // Create withdrawal message
        emit WithdrawalInitiated(msg.sender, amount);
    }
}

// L1 Withdrawal Finalization
contract L1Bridge {
    function finalizeWithdrawal(
        address recipient,
        uint256 amount,
        bytes merkleProof
    ) external {
        // For Optimistic: Wait 7 days
        // For ZK: Can be immediate after proof
        
        require(verifyWithdrawal(merkleProof), "Invalid proof");
        
        // Release funds
        payable(recipient).transfer(amount);
    }
}
```

---

## Key Takeaways

### 1. **Ethereum is Rollup-Agnostic**
- Ethereum doesn't need specific upgrades for individual rollups
- All rollups use the same L1 infrastructure
- Rollups are just smart contracts + data posting

### 2. **General Upgrades Benefit All Rollups**
- EIP-4844 (blobs) helps ALL rollups reduce costs
- Future upgrades (full danksharding) will benefit ALL rollups
- Ethereum focuses on being a good data availability + settlement layer

### 3. **Rollups Choose Their Own Trade-offs**
```
Optimistic Rollups:
✅ EVM-equivalent (easy to deploy existing contracts)
✅ Lower computational overhead
❌ 7-day withdrawal period
❌ Potential for fraud

ZK Rollups:
✅ Faster finality (hours)
✅ Cryptographic security
✅ No challenge period
❌ Higher computational cost
❌ Some have limited EVM compatibility
```

### 4. **The Rollup-Centric Roadmap**
Ethereum's strategy is to become the best settlement layer for rollups:

```
Ethereum's Role:
├── Security (consensus)
├── Data Availability (blobs)
├── Settlement (finality)
└── Censorship Resistance

Rollups' Role:
├── Execution (running transactions)
├── Scalability (high throughput)
└── Innovation (new features)
```

### 5. **No Rollup Needs Special Treatment**
- Arbitrum: Uses standard Ethereum features
- zkSync: Uses standard Ethereum features
- StarkNet: Uses standard Ethereum features
- Polygon zkEVM: Uses standard Ethereum features
- All others: Use standard Ethereum features

The beauty of the design is that Ethereum provides a **neutral, permissionless platform** where any rollup can deploy without needing Ethereum to change for them.

---

## Further Reading

### Official Resources
- [Ethereum Rollup-Centric Roadmap](https://ethereum-magicians.org/t/a-rollup-centric-ethereum-roadmap/4698)
- [EIP-4844 Specification](https://eips.ethereum.org/EIPS/eip-4844)
- [Vitalik's Rollup Guide](https://vitalik.ca/general/2021/01/05/rollup.html)

### Rollup Documentation
- [Arbitrum Docs](https://docs.arbitrum.io/)
- [Optimism Docs](https://docs.optimism.io/)
- [zkSync Docs](https://docs.zksync.io/)
- [Polygon zkEVM Docs](https://docs.polygon.technology/zkEVM/)
- [Scroll Docs](https://docs.scroll.io/)
- [StarkNet Docs](https://docs.starknet.io/)
- [Linea Docs](https://docs.linea.build/)

### Technical Deep Dives
- [L2Beat](https://l2beat.com/) - Rollup analytics and comparisons
- [Rollup Economics](https://www.galaxy.com/research/insights/rollup-economics/)
