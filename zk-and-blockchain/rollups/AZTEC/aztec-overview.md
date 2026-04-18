# Aztec L2: Privacy-First ZK Rollup

## Quick Overview

**Aztec** is a privacy-first Layer 2 rollup on Ethereum that enables **confidential smart contracts** using zero-knowledge proofs.

### Key Characteristics

| Property | Value |
|----------|-------|
| **Type** | ZK Rollup (Privacy-focused) |
| **Proof System** | PLONK/Honk (SNARKs) |
| **VM** | Aztec Virtual Machine (AVM) - Custom |
| **Language** | Noir (Rust-like) |
| **EVM Compatible** | ❌ No (by design) |
| **Privacy** | ✅ Full programmable privacy |
| **State Model** | Note-based (UTXO-like) |
| **Mainnet** | In development (testnet live) |
| **Founded** | 2018 |

---

## What Makes Aztec Different

### 1. Privacy as Core Feature

```
Traditional Rollups (zkSync, Arbitrum, etc.):
├── ❌ Public balances
├── ❌ Public transaction amounts
├── ❌ Public sender/receiver
└── ❌ Public smart contract state

Aztec:
├── ✅ Private balances
├── ✅ Private transaction amounts  
├── ✅ Private sender/receiver
├── ✅ Private smart contract state
└── ✅ Selective disclosure
```

### 2. Not EVM-Compatible (By Design)

**Why?**
- EVM was designed for transparency
- Privacy requires different architecture
- Custom VM enables better privacy primitives
- Optimized for ZK proof generation

### 3. Encrypted State

```
Public Rollups:
State = { alice: 100 ETH, bob: 50 ETH } ← Everyone can see

Aztec:
State = { 
  note_1: Enc(alice, 100 ETH),
  note_2: Enc(bob, 50 ETH)
} ← Only owner can decrypt
```

---

## Architecture Overview

```
┌─────────────────────────────────────────┐
│         USER LAYER                      │
│  • Wallets with viewing keys            │
│  • Private Execution Client (PXE)       │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│         AZTEC L2                        │
│  • Sequencer (orders transactions)      │
│  • Prover Network (generates proofs)    │
│  • AVM (executes contracts)             │
│  • Note Database (encrypted state)      │
└────────────────┬────────────────────────┘
                 │
                 │ Encrypted data + proofs
                 ▼
┌─────────────────────────────────────────┐
│         ETHEREUM L1                     │
│  • Verifies proofs                      │
│  • Stores commitments                   │
│  • Bridge contracts                     │
└─────────────────────────────────────────┘
```

---

## Privacy Model

### Note-Based State

Aztec uses **notes** (like Bitcoin UTXOs) instead of accounts:

```
Account Model (Ethereum):
accounts = {
  alice: { balance: 100 ETH }
}

Note Model (Aztec):
notes = {
  note_1: Enc(owner: alice, value: 60 ETH),
  note_2: Enc(owner: alice, value: 40 ETH)
}
```

### How Privacy Works

#### 1. Encrypted Notes
```rust
struct Note {
    owner: Address,        // Encrypted
    value: u64,           // Encrypted
    asset_id: u32,        // Encrypted
    randomness: Field,    // For uniqueness
    note_hash: Field      // Public commitment (only this is on-chain)
}
```

#### 2. Nullifiers (Prevent Double-Spending)
```
Spending a note:
1. Compute nullifier = hash(note, owner_secret)
2. Publish nullifier (doesn't reveal note details)
3. Nullifier set prevents re-spending

Public on-chain: [0x1a2b3c..., 0x4d5e6f...]
← Can't tell which notes these are!
```

#### 3. Multiple Keys
```
User Keys:
├── Spending Key → Spend notes
├── Viewing Key → Decrypt and view notes
└── Address → Receive notes

You can share viewing keys for auditing without giving spending rights!
```

---

## Noir Programming Language

**Noir** is Aztec's language for writing ZK circuits and private contracts.

### Syntax (Rust-like)

```rust
// Simple Noir function
fn main(x: Field, y: pub Field) -> pub Field {
    assert(x != y);
    x + y
}

// Private inputs: x (not revealed)
// Public inputs: y (revealed)
```

### Private Token Example

```rust
contract PrivateToken {
    use dep::aztec::prelude::*;
    
    #[aztec(storage)]
    struct Storage {
        balances: PrivateSet<ValueNote>,
    }

    #[aztec(private)]
    fn transfer(amount: u64, to: AztecAddress) {
        let from = context.msg_sender();
        
        // Consume input notes
        let balance = storage.balances.pop_notes(from, amount);
        
        // Create output note for recipient
        let mut note = ValueNote::new(amount, to);
        storage.balances.insert(&mut note, true);
        
        // Create change note
        let change = balance.sum() - amount;
        if change > 0 {
            let mut change_note = ValueNote::new(change, from);
            storage.balances.insert(&mut change_note, true);
        }
    }
}
```

---

## Transaction Flow

### Private Transfer Example

```
ALICE'S DEVICE (Client-side):
1. Find input notes: [Note(30), Note(20)]
2. Create outputs: Note(Bob, 10), Note(Alice, 40)
3. Generate ZK proof locally
4. Submit: [nullifiers, commitments, proof]
   ← Actual values NEVER sent!

SEQUENCER:
5. Verify proof
6. Check nullifiers not used
7. Add to block

BOB'S DEVICE:
8. Download new commitments
9. Try to decrypt with viewing key
10. If successful, add to wallet
```

**What's Public vs Private:**

```
Public (On-chain):
├── Nullifiers: [0x1a2b..., 0x3c4d...]
├── Commitments: [0x5e6f..., 0x7g8h...]
└── Proof

Private (Only parties know):
├── Alice's identity
├── Bob's identity
├── Amount: 10 tokens
└── Note values
```

---

## Comparison with Other L2s

| Feature | Aztec | zkSync | Arbitrum | StarkNet |
|---------|-------|--------|----------|----------|
| **Goal** | Privacy | Scaling | Scaling | Scaling |
| **Privacy** | ✅ Full | ❌ None | ❌ None | ❌ None |
| **EVM** | ❌ No | ✅ Yes | ✅ Yes | ❌ No |
| **Language** | Noir | Solidity | Solidity | Cairo |
| **State** | Note-based | Account | Account | Account |
| **Proofs** | PLONK | PLONK | Fraud | STARKs |

### Privacy Levels

```
Ethereum L1 → Fully transparent
Optimistic Rollups → Fully transparent (cheaper)
ZK Rollups (zkSync, etc.) → Fully transparent (proofs hide computation, not data)
Aztec → ✅ Fully private (encrypted state + ZK proofs)
```

---

## Use Cases

### 1. Private DeFi
- **Private DEX**: Trade without revealing strategy, amounts, or assets
- **Private Lending**: Borrow without revealing collateral or debt
- **Dark Pools**: Institutional trading without information leakage

### 2. Confidential Payments
- Private payroll
- Confidential business transactions
- Anonymous donations

### 3. Private Governance
- Vote without revealing choice or voting power
- Confidential proposals
- Anonymous participation

### 4. Compliant Privacy
- Selective disclosure for auditors
- Regulatory compliance with privacy
- Audit trails without public exposure

### 5. Private NFTs
- Own NFTs without revealing collection
- Confidential art ownership
- Private gaming assets

---

## Key Technical Components

### 1. Aztec Virtual Machine (AVM)
- Custom VM optimized for privacy
- Executes Noir bytecode
- Manages encrypted state
- Handles private/public transitions

### 2. Private Execution Client (PXE)
- Runs on user's device
- Stores private keys
- Generates proofs locally
- Decrypts notes
- **Privacy benefit**: Private data never leaves device!

### 3. Cryptographic Primitives
- **PLONK/Honk**: Proof system
- **Pedersen Commitments**: Note commitments
- **Poseidon Hash**: ZK-friendly hashing
- **BN254 Curve**: Elliptic curve

### 4. Network Components
- **Sequencer**: Orders transactions, executes public functions
- **Prover Network**: Generates ZK proofs (distributed)
- **L1 Contracts**: Verify proofs, manage bridges

---

## Current Status (2024)

### Development Phases

```
✅ Phase 1: Aztec Connect (2021-2023)
   - Privacy bridge to Ethereum DeFi
   - Shut down to focus on full network

🔄 Phase 2: Aztec Network (Current)
   - Full programmable privacy
   - Testnet live
   - Mainnet in development

🔮 Future:
   - Mainnet launch
   - Decentralized sequencer
   - Cross-chain privacy
```

### Testnet
- **Status**: Live and active
- **Access**: Public testnet available
- **Features**: Private contracts, Noir development

---

## When to Use Aztec

### ✅ Use Aztec When:
- Privacy is critical
- Building private DeFi
- Confidential voting/governance
- Private NFTs or gaming
- Compliance with privacy regulations
- Selective disclosure needed

### ❌ Use Other Rollups When:
- Transparency is acceptable
- Need EVM compatibility
- Want to deploy existing Solidity contracts
- Privacy not required
- Lower development complexity

---

## Resources

### Official Links
- **Website**: https://aztec.network/
- **Docs**: https://docs.aztec.network/
- **GitHub**: https://github.com/AztecProtocol
- **Noir Docs**: https://noir-lang.org/

### Learning Resources
- Aztec Documentation
- Noir Language Guide
- Aztec Developer Tutorials
- Community Discord

### Key Repositories
- `aztec-packages`: Main Aztec protocol
- `noir`: Noir language and compiler
- `barretenberg`: Proof system backend

---

## Summary

**Aztec is the only Ethereum L2 focused on programmable privacy:**

1. **Private by default** - Encrypted state and confidential transactions
2. **Custom architecture** - Not EVM-compatible, designed for privacy
3. **Noir language** - Rust-like language for ZK circuits
4. **Note-based state** - UTXO-like model for better privacy
5. **Selective disclosure** - Control what you reveal
6. **Full smart contracts** - Programmable privacy, not just transfers

**Key Insight**: While other rollups use ZK proofs for scaling, Aztec uses them for **privacy**. This fundamental difference shapes every design decision.
