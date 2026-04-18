# NEAR Protocol: Overview & Architecture

## Table of Contents
1. [What is NEAR Protocol?](#what-is-near-protocol)
2. [Core Architecture](#core-architecture)
3. [Key Features](#key-features)
4. [Why Choose NEAR?](#why-choose-near)

---

## What is NEAR Protocol?

NEAR Protocol is a **layer-1 blockchain** designed to be developer-friendly, scalable, and user-friendly. Founded in 2018 by Alex Skidanov and Illia Polosukhin, it launched its mainnet in April 2020.

### Key Characteristics

- **Sharded blockchain** using Nightshade consensus
- **Proof-of-Stake (PoS)** consensus mechanism  
- **Human-readable account names** (e.g., `alice.near` instead of `0x123...`)
- **Progressive onboarding** for mainstream users
- **Carbon-neutral** blockchain
- **WebAssembly (WASM)** runtime for smart contracts
- **Fast finality**: ~2 seconds
- **Low transaction costs**: ~$0.01 per transaction

### Mission

To create a blockchain that is simple enough for everyday users while being powerful enough for developers to build decentralized applications at scale.

### Network Statistics (2024)

- **20M+ accounts** created
- **350M+ transactions** processed
- **800+ projects** building on NEAR
- **Carbon neutral** certified
- **$3B+ TVL** at peak

---

## Core Architecture

### 1. Nightshade Sharding

NEAR uses a unique sharding approach called **Nightshade**, which differs from traditional sharding:

```
┌─────────────────────────────────────────────────────┐
│              NEAR Blockchain                        │
├─────────────────────────────────────────────────────┤
│  Shard 0  │  Shard 1  │  Shard 2  │  Shard 3       │
├───────────┼───────────┼───────────┼────────────────┤
│  Chunk 0  │  Chunk 1  │  Chunk 2  │  Chunk 3       │
└───────────┴───────────┴───────────┴────────────────┘
            ↓           ↓           ↓           ↓
        ┌───────────────────────────────────────┐
        │     Single Blockchain (Beacon)        │
        └───────────────────────────────────────┘
```

**How Nightshade Works:**

1. **Chunk Production**: Each shard produces a "chunk" of transactions
2. **Block Assembly**: All chunks are combined into a single block
3. **Parallel Validation**: Validators validate chunks in parallel
4. **State Sync**: Cross-shard communication is built-in

**Benefits:**
- **Linear scalability**: More shards = more capacity
- **Unified state**: Single blockchain view across all shards
- **Simple cross-shard calls**: No complex messaging protocols
- **Dynamic resharding**: Network can add/remove shards as needed

**Sharding Phases:**

- **Phase 0 (Current)**: Simple Nightshade - 4 shards
- **Phase 1**: Chunk-only producers
- **Phase 2**: Dynamic resharding - unlimited shards
- **Phase 3**: Full sharding with state sharding

### 2. Consensus Mechanism: Doomslug

NEAR uses **Doomslug**, a block production mechanism that works with Nightshade:

**Key Features:**
- **Fast finality**: ~2 seconds for practical finality
- **Efficient**: Single round of communication per block
- **Safe**: Byzantine Fault Tolerant (BFT)
- **Optimistic**: Assumes network is mostly honest

**Block Production Process:**

```
Block N-1 → Block Producer Selected → Create Block N → Validators Vote
                                                              ↓
                                                    2/3+ Approve?
                                                              ↓
                                                    Block N Finalized
                                                              ↓
                                                    Select Next Producer
```

**Finality Guarantees:**
- **Practical finality**: 1-2 seconds (optimistic)
- **Economic finality**: ~2 blocks (~4 seconds)
- **Absolute finality**: After epoch boundary

### 3. Account Model

NEAR uses an **account-based model** (not UTXO like Bitcoin):

```
Account Structure:
alice.near
├── Balance: 100 NEAR
├── Storage Used: 10 KB
├── Access Keys
│   ├── Full Access Key (owner)
│   │   └── Can do anything with account
│   └── Function Call Keys (limited permissions)
│       ├── Key 1: Can call contract A
│       └── Key 2: Can call contract B with 1 NEAR allowance
├── Contract Code (optional)
│   └── WASM bytecode
└── Contract State (optional)
    └── Key-value storage
```

**Account Types:**

1. **Named Accounts**: `alice.near`, `myapp.near`
   - Human-readable
   - Must be registered
   - Can create subaccounts

2. **Subaccounts**: `token.myapp.near`, `nft.myapp.near`
   - Hierarchical structure
   - Only parent can create
   - Independent from parent

3. **Implicit Accounts**: `98793cd91a3f870fb126f66285808c7e094afcfc4eda8a970f6648cdf0dbd6de`
   - Derived from public key (ED25519)
   - Like Ethereum addresses
   - Automatically created on first transaction

**Account Creation:**

```bash
# Create top-level account (requires NEAR tokens)
near create-account alice.near --masterAccount funding.near

# Create subaccount (only parent can do this)
near create-account app.alice.near --masterAccount alice.near

# Implicit account (auto-created on first transaction)
# Just send NEAR to the public key hash
```

### 4. Storage Model

**Storage Staking Mechanism:**

NEAR requires users to "stake" NEAR tokens for the storage they use:

```
Storage Cost Formula:
1 NEAR ≈ 100 KB of storage

Example:
- Store 1 KB of data = 0.01 NEAR locked
- Store 100 KB = 1 NEAR locked
- Delete data = NEAR refunded
```

**Why Storage Staking?**
- **Prevents spam**: Cost to store data
- **Sustainable**: Users pay for what they use
- **Refundable**: Get tokens back when deleting data
- **Fair**: No permanent blockchain bloat

**Storage Management:**

```rust
// Check storage usage
let initial_storage = env::storage_usage();

// ... perform operations ...

let final_storage = env::storage_usage();
let storage_used = final_storage - initial_storage;

// Calculate cost
let storage_cost = storage_used as u128 * env::storage_byte_cost();

// Require user to cover storage
require!(
    env::attached_deposit() >= storage_cost,
    "Insufficient deposit for storage"
);
```

### 5. Gas Model

**Gas Economics:**

```
Transaction Components:
├── Base cost: ~0.0001 NEAR
├── Function call: Depends on computation
├── Storage operations: Depends on data size
└── Cross-contract calls: Additional gas
```

**Gas Units:**
- **Gas**: Computational unit
- **1 TGas** = 1 trillion gas units
- **Typical transaction**: 2-5 TGas
- **Complex contract call**: 30-300 TGas

**Gas Price:**
- **Dynamic**: Adjusts based on network load
- **Typical**: 0.0001 NEAR per TGas
- **Predictable**: Changes slowly over time

**Gas Refunds:**
- Unused gas is refunded automatically
- Encourages efficient code
- No penalty for overestimating

---

## Key Features

### 1. Human-Readable Accounts

**Traditional vs NEAR:**

```
Ethereum:     0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb27
NEAR:         alice.near
Subaccount:   token.alice.near
```

**Benefits:**
- **Easy to remember**: Share accounts like email addresses
- **Hierarchical**: Organize with subaccounts
- **Brandable**: Companies can use their name
- **Phishing resistant**: Easier to verify correct recipient

**Subaccount Structure:**

```
company.near
├── token.company.near (token contract)
├── nft.company.near (NFT contract)
├── dao.company.near (governance)
└── app.company.near (main application)
```

### 2. Progressive Security (Access Keys)

**Access Key Types:**

**Full Access Key:**
```rust
// Can do ANYTHING with the account:
- Transfer NEAR
- Deploy contracts
- Delete account
- Add/remove keys
- Call any function
```

**Function Call Key:**
```rust
FunctionCallKey {
    allowance: Some(1_000_000_000_000_000_000_000_000), // 1 NEAR
    receiver_id: "myapp.near",
    method_names: vec!["play_game", "claim_reward"],
}
```

**Use Cases:**

1. **Gaming**: Limited key for in-game actions
   ```
   User → Game Key → Can only call game functions
                  → Cannot transfer NEAR
                  → Cannot delete account
   ```

2. **DeFi**: Trading key with allowance
   ```
   User → Trading Key → Can swap on DEX
                     → Limited to 10 NEAR allowance
                     → Cannot access main balance
   ```

3. **Social Apps**: Posting key
   ```
   User → Social Key → Can create posts
                    → Can like/comment
                    → Cannot transfer tokens
   ```

**Security Benefits:**
- **Gradual onboarding**: Start with limited keys
- **Risk management**: Limit exposure
- **Better UX**: No wallet popup for every action
- **Mobile-friendly**: Keep full key secure, use limited keys daily

### 3. Rainbow Bridge (Ethereum ↔ NEAR)

**Trustless Bridge Architecture:**

```
Ethereum                Rainbow Bridge              NEAR
   │                          │                      │
   │  Lock ETH/ERC-20         │                      │
   ├──────────────────────────►                      │
   │                          │                      │
   │                          │  Mint wrapped token  │
   │                          ├─────────────────────►│
   │                          │                      │
   │                          │  Burn wrapped token  │
   │                          ◄─────────────────────┤
   │                          │                      │
   │  Unlock ETH/ERC-20       │                      │
   ◄──────────────────────────┤                      │
```

**How It Works:**

1. **Light Clients**: Both chains run light clients of each other
2. **Proof Verification**: Cryptographic proofs verify transactions
3. **No Trusted Party**: Fully decentralized
4. **Bi-directional**: Transfer assets both ways

**Supported Assets:**
- ETH → wETH on NEAR
- ERC-20 → NEP-141 on NEAR
- ERC-721 → NEP-171 on NEAR
- NEAR → wNEAR on Ethereum

**Benefits:**
- **Low fees**: NEAR side costs ~$0.01
- **Fast**: 4-6 minutes for Ethereum → NEAR
- **Secure**: Trustless, no custodians
- **Composable**: Use Ethereum assets in NEAR DeFi

### 4. Aurora (EVM on NEAR)

**What is Aurora?**

Aurora is an **Ethereum Virtual Machine (EVM)** running as a smart contract on NEAR:

```
Ethereum Dapp (Solidity)
         ↓
    Aurora EVM
         ↓
    NEAR Protocol
```

**Features:**

- **Full EVM compatibility**: Run Solidity contracts unchanged
- **Ethereum tooling**: Use MetaMask, Hardhat, Truffle, etc.
- **Low fees**: ~$0.02 per transaction (vs $50+ on Ethereum)
- **Fast finality**: ~2 seconds
- **Ethereum bridge**: Built-in Rainbow Bridge integration

**Developer Experience:**

```javascript
// Deploy Ethereum contract to Aurora
// No code changes needed!

// 1. Configure network
const aurora = {
  chainId: 1313161554,
  url: 'https://mainnet.aurora.dev',
};

// 2. Deploy with Hardhat
npx hardhat run scripts/deploy.js --network aurora

// 3. Interact with MetaMask
// Users connect to Aurora like any Ethereum network
```

**Use Cases:**
- **Port Ethereum dapps**: Move to NEAR without rewriting
- **Multi-chain strategy**: Deploy on both Ethereum and Aurora
- **Cost optimization**: Reduce fees for users
- **Ethereum liquidity**: Access Ethereum assets via bridge

### 5. NEAR Social (On-Chain Social Graph)

**Decentralized Social Network:**

```
Traditional Social:        NEAR Social:
Company owns data    →    Users own data
Centralized servers  →    On-chain storage
Algorithmic feed     →    User-controlled feed
Platform lock-in     →    Portable identity
```

**Key Concepts:**

1. **On-chain profiles**: Store profile data on NEAR
2. **Social graph**: Follow relationships on-chain
3. **Content storage**: Posts, images, metadata on-chain
4. **Composability**: Any app can read/write social data

**Example Use Cases:**
- Decentralized Twitter alternative
- Creator platforms with direct monetization
- Social DAOs and communities
- Reputation systems

---

## Why Choose NEAR?

### Comparison Matrix

| Feature | NEAR | Ethereum | Solana | Polygon |
|---------|------|----------|--------|---------|
| **TPS** | 100,000+ (sharded) | 15-30 | 65,000 | 7,000 |
| **Finality** | 2 seconds | 12+ minutes | 2.5 seconds | 2 seconds |
| **Transaction Cost** | ~$0.01 | $1-50+ | ~$0.001 | ~$0.01 |
| **Account Model** | Human-readable | Hex addresses | Base58 | Hex addresses |
| **Sharding** | Yes (Nightshade) | Planned | No | No |
| **Smart Contracts** | Rust, AssemblyScript | Solidity | Rust | Solidity |
| **Carbon Neutral** | Yes | No (PoS now) | No | No |

### When to Choose NEAR

**✅ Choose NEAR if you need:**
- Human-readable accounts for better UX
- Scalability through sharding
- Low, predictable transaction costs
- Fast finality (~2 seconds)
- Progressive security (access keys)
- Rust or TypeScript for smart contracts
- Carbon-neutral blockchain
- Easy onboarding for mainstream users

**❌ Consider alternatives if you need:**
- Maximum decentralization (Ethereum)
- Highest throughput (Solana)
- Largest DeFi ecosystem (Ethereum)
- Solidity-only development (Ethereum/Polygon)

### Developer Benefits

1. **Easy to learn**: Rust or TypeScript
2. **Great tooling**: CLI, SDKs, testing frameworks
3. **Fast iteration**: Quick deployment and testing
4. **Low costs**: Affordable to experiment
5. **Good documentation**: Comprehensive guides
6. **Active community**: Helpful developers

### User Benefits

1. **Simple accounts**: alice.near vs 0x123...
2. **Low fees**: Affordable for everyone
3. **Fast transactions**: No waiting
4. **Progressive onboarding**: Start simple, add features
5. **Eco-friendly**: Carbon-neutral
6. **Secure**: Multiple security layers

---

## Next Steps

- **[Technical Concepts](./02-near-technical-concepts.md)**: Deep dive into smart contracts and development
- **[Case Studies](./03-near-case-studies.md)**: Real-world implementations
- **[Use Cases](./04-near-use-cases.md)**: Practical applications
- **[Code Examples](./05-near-code-examples.md)**: Working code samples

## Resources

- **Official Website**: https://near.org
- **Documentation**: https://docs.near.org
- **GitHub**: https://github.com/near
- **Discord**: https://near.chat
- **Forum**: https://gov.near.org
