# NEAR Protocol: Technical Concepts & Development

## Table of Contents
1. [Smart Contract Development](#smart-contract-development)
2. [Token Standards](#token-standards)
3. [Cross-Contract Calls](#cross-contract-calls)
4. [Storage Management](#storage-management)
5. [Testing & Deployment](#testing--deployment)

---

## Smart Contract Development

### Supported Languages

NEAR smart contracts compile to **WebAssembly (WASM)** and can be written in:

1. **Rust** (Recommended for production)
2. **AssemblyScript** (TypeScript-like, easier for web developers)
3. **JavaScript** (via QuickJS, experimental)

### Rust Smart Contract Basics

**Setup:**

```toml
# Cargo.toml
[package]
name = "my-contract"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib"]

[dependencies]
near-sdk = "4.1.1"

[profile.release]
codegen-units = 1
opt-level = "z"
lto = true
debug = false
panic = "abort"
overflow-checks = true
```

**Basic Contract Structure:**

```rust
use near_sdk::borsh::{self, BorshDeserialize, BorshSerialize};
use near_sdk::{near_bindgen, env, PanicOnDefault};

// Contract struct - holds contract state
#[near_bindgen]
#[derive(BorshDeserialize, BorshSerialize, PanicOnDefault)]
pub struct MyContract {
    owner: AccountId,
    counter: u64,
}

// Implementation block - contract methods
#[near_bindgen]
impl MyContract {
    // Initialization method (called once on deployment)
    #[init]
    pub fn new(owner: AccountId) -> Self {
        Self {
            owner,
            counter: 0,
        }
    }
    
    // Mutable method (changes state)
    pub fn increment(&mut self) {
        self.counter += 1;
        env::log_str(&format!("Counter: {}", self.counter));
    }
    
    // View method (read-only, no gas cost)
    pub fn get_counter(&self) -> u64 {
        self.counter
    }
    
    // Private method (can only be called internally)
    #[private]
    pub fn reset(&mut self) {
        self.counter = 0;
    }
}
```

**Key Macros:**

- `#[near_bindgen]`: Marks struct/impl as contract
- `#[init]`: Initialization method
- `#[payable]`: Method can receive NEAR tokens
- `#[private]`: Only callable by contract itself
- `#[derive(BorshSerialize, BorshDeserialize)]`: Serialization

### Environment Functions

```rust
use near_sdk::env;

// Account information
let caller = env::predecessor_account_id();  // Who called this method
let current = env::current_account_id();     // This contract's account
let signer = env::signer_account_id();       // Original transaction signer

// Financial
let deposit = env::attached_deposit();       // NEAR attached to call
let balance = env::account_balance();        // Contract's balance

// Block information
let timestamp = env::block_timestamp();      // Nanoseconds since epoch
let height = env::block_height();            // Current block height

// Randomness
let random = env::random_seed();             // 32 bytes of randomness

// Storage
let usage = env::storage_usage();            // Bytes used
let cost = env::storage_byte_cost();         // Cost per byte

// Logging
env::log_str("Hello from contract!");
env::log_str(&format!("Value: {}", value));
```

### Collections (Efficient Storage)

NEAR SDK provides gas-efficient collections:

```rust
use near_sdk::collections::{
    LookupMap,      // HashMap-like, O(1) access
    UnorderedMap,   // Iterable HashMap
    UnorderedSet,   // Iterable HashSet
    Vector,         // Iterable array
    LookupSet,      // HashSet-like, O(1) access
    TreeMap,        // Ordered map
};

#[near_bindgen]
#[derive(BorshDeserialize, BorshSerialize)]
pub struct MyContract {
    // LookupMap: Fast access, not iterable
    balances: LookupMap<AccountId, Balance>,
    
    // UnorderedMap: Iterable, slightly more gas
    metadata: UnorderedMap<String, String>,
    
    // Vector: Ordered list
    items: Vector<Item>,
    
    // UnorderedSet: Unique values
    members: UnorderedSet<AccountId>,
}

#[near_bindgen]
impl MyContract {
    #[init]
    pub fn new() -> Self {
        Self {
            balances: LookupMap::new(b"b"),      // Prefix for storage
            metadata: UnorderedMap::new(b"m"),
            items: Vector::new(b"i"),
            members: UnorderedSet::new(b"mem"),
        }
    }
    
    pub fn add_balance(&mut self, account: AccountId, amount: Balance) {
        let current = self.balances.get(&account).unwrap_or(0);
        self.balances.insert(&account, &(current + amount));
    }
    
    pub fn get_balance(&self, account: AccountId) -> Balance {
        self.balances.get(&account).unwrap_or(0)
    }
}
```

**Collection Choice Guide:**

| Collection | Iterable | Ordered | Use Case |
|------------|----------|---------|----------|
| `LookupMap` | ❌ | ❌ | Fast key-value lookup |
| `UnorderedMap` | ✅ | ❌ | Iterable key-value pairs |
| `TreeMap` | ✅ | ✅ | Sorted key-value pairs |
| `Vector` | ✅ | ✅ | Ordered list |
| `LookupSet` | ❌ | ❌ | Fast membership check |
| `UnorderedSet` | ✅ | ❌ | Iterable unique values |

### AssemblyScript Contracts

**Setup:**

```json
// package.json
{
  "scripts": {
    "build": "asb"
  },
  "devDependencies": {
    "near-sdk-as": "^3.2.3"
  }
}
```

**Basic Contract:**

```typescript
import { context, storage, logging, PersistentMap } from "near-sdk-as";

// State stored on-chain
const balances = new PersistentMap<string, u64>("b");

// View function (read-only)
export function getBalance(account: string): u64 {
  return balances.getSome(account);
}

// Change function (modifies state)
export function addBalance(account: string, amount: u64): void {
  const current = balances.get(account, 0);
  balances.set(account, current + amount);
  logging.log(`Added ${amount} to ${account}`);
}

// Get caller information
export function whoAmI(): string {
  return context.sender;  // Who called this function
}
```

---

## Token Standards

### NEP-141: Fungible Tokens

**Core Interface:**

```rust
pub trait FungibleToken {
    // Transfer tokens
    fn ft_transfer(
        &mut self,
        receiver_id: AccountId,
        amount: U128,
        memo: Option<String>,
    );
    
    // Transfer and call receiver contract
    fn ft_transfer_call(
        &mut self,
        receiver_id: AccountId,
        amount: U128,
        memo: Option<String>,
        msg: String,
    ) -> PromiseOrValue<U128>;
    
    // Get total supply
    fn ft_total_supply(&self) -> U128;
    
    // Get account balance
    fn ft_balance_of(&self, account_id: AccountId) -> U128;
}
```

**Complete Implementation:**

```rust
use near_sdk::borsh::{self, BorshDeserialize, BorshSerialize};
use near_sdk::collections::LookupMap;
use near_sdk::json_types::U128;
use near_sdk::{env, near_bindgen, AccountId, Balance, PanicOnDefault};

#[near_bindgen]
#[derive(BorshDeserialize, BorshSerialize, PanicOnDefault)]
pub struct FungibleToken {
    total_supply: Balance,
    balances: LookupMap<AccountId, Balance>,
}

#[near_bindgen]
impl FungibleToken {
    #[init]
    pub fn new(owner_id: AccountId, total_supply: U128) -> Self {
        let mut ft = Self {
            total_supply: total_supply.0,
            balances: LookupMap::new(b"b"),
        };
        ft.balances.insert(&owner_id, &total_supply.0);
        ft
    }
    
    pub fn ft_transfer(&mut self, receiver_id: AccountId, amount: U128) {
        let sender = env::predecessor_account_id();
        self.internal_transfer(&sender, &receiver_id, amount.0);
    }
    
    pub fn ft_balance_of(&self, account_id: AccountId) -> U128 {
        U128(self.balances.get(&account_id).unwrap_or(0))
    }
    
    pub fn ft_total_supply(&self) -> U128 {
        U128(self.total_supply)
    }
    
    fn internal_transfer(&mut self, sender: &AccountId, receiver: &AccountId, amount: Balance) {
        let sender_balance = self.balances.get(sender).expect("Sender not registered");
        require!(sender_balance >= amount, "Insufficient balance");
        
        self.balances.insert(sender, &(sender_balance - amount));
        
        let receiver_balance = self.balances.get(receiver).unwrap_or(0);
        self.balances.insert(receiver, &(receiver_balance + amount));
        
        env::log_str(&format!("Transfer {} from {} to {}", amount, sender, receiver));
    }
}
```

### NEP-171: Non-Fungible Tokens (NFTs)

**Core Interface:**

```rust
pub trait NonFungibleToken {
    // Transfer NFT
    fn nft_transfer(
        &mut self,
        receiver_id: AccountId,
        token_id: TokenId,
        approval_id: Option<u64>,
        memo: Option<String>,
    );
    
    // Transfer and call receiver
    fn nft_transfer_call(
        &mut self,
        receiver_id: AccountId,
        token_id: TokenId,
        approval_id: Option<u64>,
        memo: Option<String>,
        msg: String,
    ) -> PromiseOrValue<bool>;
    
    // Get token info
    fn nft_token(&self, token_id: TokenId) -> Option<Token>;
}
```

**NFT Implementation:**

```rust
use near_sdk::borsh::{self, BorshDeserialize, BorshSerialize};
use near_sdk::collections::{LookupMap, UnorderedSet};
use near_sdk::serde::{Deserialize, Serialize};
use near_sdk::{env, near_bindgen, AccountId, PanicOnDefault};

pub type TokenId = String;

#[derive(BorshDeserialize, BorshSerialize, Serialize, Deserialize)]
#[serde(crate = "near_sdk::serde")]
pub struct Token {
    pub owner_id: AccountId,
    pub metadata: TokenMetadata,
}

#[derive(BorshDeserialize, BorshSerialize, Serialize, Deserialize)]
#[serde(crate = "near_sdk::serde")]
pub struct TokenMetadata {
    pub title: Option<String>,
    pub description: Option<String>,
    pub media: Option<String>,  // URL to media
    pub media_hash: Option<String>,  // Base64 hash
}

#[near_bindgen]
#[derive(BorshDeserialize, BorshSerialize, PanicOnDefault)]
pub struct NFTContract {
    owner_id: AccountId,
    tokens: LookupMap<TokenId, Token>,
    tokens_per_owner: LookupMap<AccountId, UnorderedSet<TokenId>>,
    token_counter: u64,
}

#[near_bindgen]
impl NFTContract {
    #[init]
    pub fn new(owner_id: AccountId) -> Self {
        Self {
            owner_id,
            tokens: LookupMap::new(b"t"),
            tokens_per_owner: LookupMap::new(b"o"),
            token_counter: 0,
        }
    }
    
    #[payable]
    pub fn nft_mint(&mut self, metadata: TokenMetadata, receiver_id: AccountId) -> TokenId {
        let token_id = self.token_counter.to_string();
        self.token_counter += 1;
        
        let token = Token {
            owner_id: receiver_id.clone(),
            metadata,
        };
        
        self.tokens.insert(&token_id, &token);
        
        let mut owner_tokens = self.tokens_per_owner
            .get(&receiver_id)
            .unwrap_or_else(|| UnorderedSet::new(format!("o{}", receiver_id).as_bytes()));
        owner_tokens.insert(&token_id);
        self.tokens_per_owner.insert(&receiver_id, &owner_tokens);
        
        token_id
    }
    
    pub fn nft_transfer(&mut self, receiver_id: AccountId, token_id: TokenId) {
        let sender = env::predecessor_account_id();
        let mut token = self.tokens.get(&token_id).expect("Token not found");
        
        require!(token.owner_id == sender, "Not token owner");
        
        // Remove from sender
        let mut sender_tokens = self.tokens_per_owner.get(&sender).unwrap();
        sender_tokens.remove(&token_id);
        self.tokens_per_owner.insert(&sender, &sender_tokens);
        
        // Add to receiver
        let mut receiver_tokens = self.tokens_per_owner
            .get(&receiver_id)
            .unwrap_or_else(|| UnorderedSet::new(format!("o{}", receiver_id).as_bytes()));
        receiver_tokens.insert(&token_id);
        self.tokens_per_owner.insert(&receiver_id, &receiver_tokens);
        
        // Update token owner
        token.owner_id = receiver_id;
        self.tokens.insert(&token_id, &token);
    }
    
    pub fn nft_token(&self, token_id: TokenId) -> Option<Token> {
        self.tokens.get(&token_id)
    }
    
    pub fn nft_tokens_for_owner(&self, account_id: AccountId) -> Vec<Token> {
        let token_ids = self.tokens_per_owner.get(&account_id);
        if let Some(token_ids) = token_ids {
            token_ids.iter()
                .filter_map(|token_id| self.tokens.get(&token_id))
                .collect()
        } else {
            vec![]
        }
    }
}
```

---

## Cross-Contract Calls

### Promise-Based Async Calls

NEAR uses **Promises** for cross-contract calls:

```rust
use near_sdk::{Promise, PromiseResult};

#[near_bindgen]
impl MyContract {
    // Simple cross-contract call
    pub fn call_other_contract(&self, account_id: AccountId) -> Promise {
        Promise::new(account_id)
            .function_call(
                "method_name".to_string(),
                json!({"arg": "value"}).to_string().into_bytes(),
                0,  // Attached deposit
                Gas(5 * TGAS),  // Gas
            )
    }
    
    // Call with callback
    pub fn call_with_callback(&self, account_id: AccountId) -> Promise {
        Promise::new(account_id)
            .function_call(
                "get_data".to_string(),
                b"{}".to_vec(),
                0,
                Gas(5 * TGAS),
            )
            .then(
                Promise::new(env::current_account_id())
                    .function_call(
                        "callback_method".to_string(),
                        b"{}".to_vec(),
                        0,
                        Gas(5 * TGAS),
                    )
            )
    }
    
    // Handle callback
    #[private]
    pub fn callback_method(&self) -> String {
        match env::promise_result(0) {
            PromiseResult::Successful(value) => {
                let data: String = near_sdk::serde_json::from_slice(&value).unwrap();
                format!("Success: {}", data)
            }
            PromiseResult::Failed => {
                "Call failed".to_string()
            }
        }
    }
}
```

### High-Level Cross-Contract Calls

Using `ext_contract` trait:

```rust
use near_sdk::ext_contract;

// Define external contract interface
#[ext_contract(ext_token)]
trait TokenContract {
    fn ft_transfer(&mut self, receiver_id: AccountId, amount: U128);
    fn ft_balance_of(&self, account_id: AccountId) -> U128;
}

// Define callback interface
#[ext_contract(ext_self)]
trait MyContractCallbacks {
    fn on_transfer_complete(&self) -> bool;
}

#[near_bindgen]
impl MyContract {
    pub fn transfer_tokens(&self, token_contract: AccountId, receiver: AccountId, amount: U128) -> Promise {
        ext_token::ext(token_contract)
            .with_attached_deposit(1)  // 1 yoctoNEAR for security
            .with_static_gas(Gas(10 * TGAS))
            .ft_transfer(receiver, amount)
            .then(
                ext_self::ext(env::current_account_id())
                    .with_static_gas(Gas(5 * TGAS))
                    .on_transfer_complete()
            )
    }
    
    #[private]
    pub fn on_transfer_complete(&self) -> bool {
        match env::promise_result(0) {
            PromiseResult::Successful(_) => {
                env::log_str("Transfer successful");
                true
            }
            PromiseResult::Failed => {
                env::log_str("Transfer failed");
                false
            }
        }
    }
}
```

---

## Storage Management

### Storage Cost Calculation

```rust
#[near_bindgen]
impl MyContract {
    #[payable]
    pub fn store_data(&mut self, key: String, value: String) {
        // Measure initial storage
        let initial_storage = env::storage_usage();
        
        // Store data
        self.data.insert(&key, &value);
        
        // Measure final storage
        let final_storage = env::storage_usage();
        let storage_used = final_storage - initial_storage;
        
        // Calculate cost
        let storage_cost = Balance::from(storage_used) * env::storage_byte_cost();
        let attached = env::attached_deposit();
        
        // Require sufficient deposit
        require!(attached >= storage_cost, "Insufficient deposit for storage");
        
        // Refund excess
        if attached > storage_cost {
            Promise::new(env::predecessor_account_id())
                .transfer(attached - storage_cost);
        }
    }
}
```

### Storage Management Trait

```rust
#[derive(Serialize, Deserialize)]
#[serde(crate = "near_sdk::serde")]
pub struct StorageBalance {
    pub total: U128,
    pub available: U128,
}

pub trait StorageManagement {
    fn storage_deposit(&mut self, account_id: Option<AccountId>) -> StorageBalance;
    fn storage_withdraw(&mut self, amount: Option<U128>) -> StorageBalance;
    fn storage_balance_of(&self, account_id: AccountId) -> Option<StorageBalance>;
}

#[near_bindgen]
impl StorageManagement for MyContract {
    #[payable]
    fn storage_deposit(&mut self, account_id: Option<AccountId>) -> StorageBalance {
        let account = account_id.unwrap_or_else(env::predecessor_account_id);
        let deposit = env::attached_deposit();
        
        let current = self.storage_deposits.get(&account).unwrap_or(0);
        let new_total = current + deposit;
        self.storage_deposits.insert(&account, &new_total);
        
        StorageBalance {
            total: U128(new_total),
            available: U128(new_total),
        }
    }
    
    fn storage_balance_of(&self, account_id: AccountId) -> Option<StorageBalance> {
        self.storage_deposits.get(&account_id).map(|balance| {
            StorageBalance {
                total: U128(balance),
                available: U128(balance),
            }
        })
    }
}
```

---

## Testing & Deployment

### Unit Tests

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use near_sdk::test_utils::{accounts, VMContextBuilder};
    use near_sdk::testing_env;

    fn get_context(predecessor: AccountId) -> VMContextBuilder {
        let mut builder = VMContextBuilder::new();
        builder
            .current_account_id(accounts(0))
            .predecessor_account_id(predecessor)
            .signer_account_id(predecessor.clone());
        builder
    }

    #[test]
    fn test_increment() {
        let context = get_context(accounts(1));
        testing_env!(context.build());
        
        let mut contract = MyContract::new(accounts(0));
        contract.increment();
        assert_eq!(contract.get_counter(), 1);
    }
    
    #[test]
    #[should_panic(expected = "Insufficient balance")]
    fn test_insufficient_balance() {
        let context = get_context(accounts(1));
        testing_env!(context.build());
        
        let mut contract = FungibleToken::new(accounts(0), U128(1000));
        contract.ft_transfer(accounts(2), U128(2000));
    }
}
```

### Integration Tests (Workspaces)

```rust
use workspaces::{Account, Contract, Worker};

#[tokio::test]
async fn test_contract_integration() -> anyhow::Result<()> {
    // Create sandbox environment
    let worker = workspaces::sandbox().await?;
    
    // Deploy contract
    let wasm = std::fs::read("target/wasm32-unknown-unknown/release/contract.wasm")?;
    let contract = worker.dev_deploy(&wasm).await?;
    
    // Create user account
    let user = worker.dev_create_account().await?;
    
    // Initialize contract
    contract.call("new")
        .args_json(json!({"owner_id": contract.id()}))?
        .transact()
        .await?;
    
    // Call method
    let outcome = user.call(contract.id(), "increment")
        .transact()
        .await?;
    
    assert!(outcome.is_success());
    
    // View method
    let count: u64 = contract.view("get_counter")
        .await?
        .json()?;
    
    assert_eq!(count, 1);
    
    Ok(())
}
```

### Build & Deploy

```bash
# Build contract
cargo build --target wasm32-unknown-unknown --release

# Deploy to testnet
near deploy --accountId mycontract.testnet \
    --wasmFile target/wasm32-unknown-unknown/release/contract.wasm

# Initialize contract
near call mycontract.testnet new \
    '{"owner_id": "alice.testnet"}' \
    --accountId alice.testnet

# Call method
near call mycontract.testnet increment \
    --accountId alice.testnet \
    --gas 30000000000000

# View method
near view mycontract.testnet get_counter
```

---

## Next Steps

- **[Case Studies](./03-near-case-studies.md)**: Real-world implementations
- **[Use Cases](./04-near-use-cases.md)**: Practical applications  
- **[Code Examples](./05-near-code-examples.md)**: Complete working examples
