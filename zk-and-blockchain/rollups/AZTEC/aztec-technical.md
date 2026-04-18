# Aztec Technical Details

## State Management

### Note Lifecycle
```
1. CREATE → User creates note locally
2. COMMIT → commitment = Pedersen(owner, value, asset_id, randomness)
3. PUBLISH → Commitment added to tree (only hash is public)
4. SPEND → nullifier = Poseidon(commitment, secret_key)
5. NULLIFY → Nullifier published (prevents double-spend)
```

### Storage Types
```rust
// Private storage
#[aztec(storage)]
struct Storage {
    balances: PrivateSet<ValueNote>,      // Collection of notes
    owner: PrivateMutable<AztecAddress>,  // Single value
}

// Public storage
total_supply: PublicMutable<U128>,        // Transparent
```

## Function Types

### Private Functions
```rust
#[aztec(private)]
fn transfer(to: AztecAddress, amount: Field) {
    // Runs on user's device
    // Generates proof locally
    // Private data never leaves device
}
```

### Public Functions
```rust
#[aztec(public)]
fn mint(to: AztecAddress, amount: Field) {
    // Runs on sequencer
    // Updates public state
    // Transparent
}
```

### Unconstrained (View)
```rust
unconstrained fn balance_of(owner: AztecAddress) -> pub Field {
    // Read-only, no proof
    storage.balances.balance_of(owner)
}
```

## Proof System

### PLONK Characteristics
- Universal trusted setup
- ~1 KB proof size
- ~10ms verification
- Recursive composition

### Proof Pipeline
```
Noir Code → ACIR → Circuit → Witness → Proof (Barretenberg)
```

## Network Components

### Private Execution Client (PXE)
- Runs on user device
- Stores private keys
- Generates proofs locally
- Decrypts notes

### Sequencer
- Orders transactions
- Executes public functions
- Coordinates proving

### Prover Network
- Distributed proof generation
- Recursive aggregation
- Posts to L1

## Bridge Mechanism

### L1 → L2 (Deposit)
```solidity
// L1 Contract
function deposit(uint256 amount) external {
    // Lock tokens on L1
    token.transferFrom(msg.sender, address(this), amount);
    // Message to L2
    emit DepositInitiated(msg.sender, amount);
}
```

### L2 → L1 (Withdrawal)
```rust
// L2 Contract
#[aztec(private)]
fn withdraw(amount: Field) {
    // Burn private notes
    // Create withdrawal message
    context.message_portal(l1_recipient, amount);
}
```

## Advanced Patterns

### Selective Disclosure
```rust
fn transfer_with_audit(to: AztecAddress, amount: Field, auditor: PublicKey) {
    // Encrypt note for both recipient and auditor
    let note = ValueNote::new_with_auditor(amount, to, auditor);
    storage.balances.insert(&mut note, true);
}
```

### Private-Public Bridging
```rust
#[aztec(private)]
fn unshield(amount: Field) {
    // Burn private notes
    let notes = storage.private_balances.pop_notes(sender, amount);
    
    // Call public function
    context.call_public_function(
        self.address,
        "increase_public_balance",
        [sender, amount]
    );
}
```

## Cryptographic Primitives

- **PLONK/Honk**: Proof system
- **Pedersen**: Note commitments
- **Poseidon**: Nullifiers (ZK-friendly hash)
- **BN254**: Elliptic curve
- **Schnorr**: Signatures

## Key Differences from Other L2s

| Aspect | Aztec | Other ZK Rollups |
|--------|-------|------------------|
| State | Note-based (UTXO) | Account-based |
| Privacy | Encrypted | Public |
| Execution | Client-side + Sequencer | Sequencer only |
| Proofs | Per-user + Aggregated | Batch only |
| Keys | Spending + Viewing | Single key |

## Resources

- **Docs**: https://docs.aztec.network/
- **Noir**: https://noir-lang.org/
- **GitHub**: https://github.com/AztecProtocol
