# ZK Companies and Projects: The Industry Landscape

## Table of Contents
1. [ZK Rollups (Layer 2)](#zk-rollups-layer-2)
2. [ZK Infrastructure & Tooling](#zk-infrastructure--tooling)
3. [ZK Virtual Machines](#zk-virtual-machines)
4. [Privacy-Focused Projects](#privacy-focused-projects)
5. [ZK Application Platforms](#zk-application-platforms)
6. [Research & Development](#research--development)
7. [Funding & Ecosystem](#funding--ecosystem)

---

## ZK Rollups (Layer 2)

### zkSync (Matter Labs)

**Status**: Mainnet (zkSync Era)

```
Type: Type 4 ZK-EVM
Proof System: PLONK + Boojum (custom STARK)
Language: Solidity (compiled to zkEVM bytecode)
TPS: ~2000+
```

**Key Features**:
- Account abstraction (native)
- Paymaster (gasless transactions)
- Hyperchains (app-specific rollups)
- zkPorter (hybrid data availability)

**Technology Stack**:
- **Prover**: Boojum (STARK-based, no trusted setup)
- **Compiler**: zksolc (Solidity → zkEVM)
- **VM**: Custom zkEVM optimized for ZK

**Funding**: $458M+ (Series B led by a16z)

**Links**:
- Website: [zksync.io](https://zksync.io)
- Docs: [docs.zksync.io](https://docs.zksync.io)
- GitHub: [matter-labs](https://github.com/matter-labs)
- Twitter: [@zksync](https://twitter.com/zksync)

**Notable Projects on zkSync**:
- SyncSwap (DEX)
- Mute.io (DeFi)
- zkSync Name Service

---

### StarkNet (StarkWare)

**Status**: Mainnet

```
Type: Custom VM (Cairo)
Proof System: STARKs (FRI-based)
Language: Cairo
TPS: ~1000+
```

**Key Features**:
- No trusted setup (transparent)
- Quantum resistant
- Cairo language (ZK-native)
- Account abstraction

**Technology Stack**:
- **Prover**: STARK prover (proprietary + open-source)
- **Language**: Cairo (Rust-like, ZK-optimized)
- **VM**: Cairo VM

**Products**:
1. **StarkNet**: Public L2 rollup
2. **StarkEx**: Application-specific rollups
   - dYdX (derivatives)
   - Sorare (NFT gaming)
   - ImmutableX (NFT marketplace)
   - DeversiFi (DEX)

**Funding**: $273M (Paradigm, Sequoia, etc.)

**Links**:
- Website: [starkware.co](https://starkware.co)
- StarkNet: [starknet.io](https://starknet.io)
- Docs: [docs.starknet.io](https://docs.starknet.io)
- GitHub: [starkware-libs](https://github.com/starkware-libs)
- Twitter: [@StarkWareLtd](https://twitter.com/StarkWareLtd)

**Ecosystem**:
- Argent (wallet)
- Braavos (wallet)
- Jediswap (DEX)
- Ekubo (AMM)

---

### Polygon zkEVM

**Status**: Mainnet

```
Type: Type 2.5 ZK-EVM (near-equivalent)
Proof System: Plonky2 (recursive STARKs)
Language: Solidity (EVM bytecode)
TPS: ~2000+
```

**Key Features**:
- High EVM compatibility
- Fast finality
- Plonky2 (fastest recursive proofs)
- Ethereum security

**Technology Stack**:
- **Prover**: Plonky2 (developed by Polygon Zero)
- **Recursion**: ~170ms per level
- **Compatibility**: EVM opcodes with minor modifications

**Polygon's ZK Portfolio**:
1. **Polygon zkEVM**: EVM-compatible rollup
2. **Polygon Miden**: ZK-VM (STARK-based)
3. **Polygon Zero**: Research (Plonky2/3)

**Funding**: Part of Polygon ($450M raised)

**Links**:
- Website: [polygon.technology/polygon-zkevm](https://polygon.technology/polygon-zkevm)
- Docs: [docs.polygon.technology/zkEVM](https://docs.polygon.technology/zkEVM/)
- GitHub: [0xPolygonZero](https://github.com/0xPolygonZero)
- Twitter: [@0xPolygon](https://twitter.com/0xPolygon)

---

### Scroll

**Status**: Mainnet

```
Type: Type 2 ZK-EVM (EVM-equivalent)
Proof System: Halo2
Language: Solidity (native EVM)
TPS: ~1000+
```

**Key Features**:
- Bytecode-level EVM compatibility
- No trusted setup (Halo2)
- Decentralized sequencer (planned)
- Native Ethereum tooling support

**Technology Stack**:
- **Prover**: Halo2 (no trusted setup)
- **Compatibility**: Full EVM bytecode
- **Recursion**: Halo2 accumulation

**Funding**: $80M (Polychain, Sequoia, etc.)

**Links**:
- Website: [scroll.io](https://scroll.io)
- Docs: [docs.scroll.io](https://docs.scroll.io)
- GitHub: [scroll-tech](https://github.com/scroll-tech)
- Twitter: [@Scroll_ZKP](https://twitter.com/Scroll_ZKP)

**Differentiator**: Highest EVM compatibility (Type 2)

---

### Linea (ConsenSys)

**Status**: Mainnet

```
Type: Type 2 ZK-EVM
Proof System: Custom (lattice-based + Plonk)
Language: Solidity
TPS: ~2000+
```

**Key Features**:
- ConsenSys backing (MetaMask integration)
- EVM equivalence
- Quantum-resistant research
- Enterprise focus

**Funding**: ConsenSys-backed

**Links**:
- Website: [linea.build](https://linea.build)
- Docs: [docs.linea.build](https://docs.linea.build)
- Twitter: [@LineaBuild](https://twitter.com/LineaBuild)

---

### Taiko

**Status**: Mainnet (Alpha)

```
Type: Type 1 ZK-EVM (Ethereum-equivalent)
Proof System: Multi-prover (Halo2, SGX)
Language: Solidity
Goal: Full Ethereum equivalence
```

**Key Features**:
- Based rollup (Ethereum L1 for sequencing)
- Multi-prover system (ZK + TEE)
- Decentralized from day 1
- Full Ethereum compatibility

**Funding**: $37M (Sequoia, GGV, etc.)

**Links**:
- Website: [taiko.xyz](https://taiko.xyz)
- Docs: [docs.taiko.xyz](https://docs.taiko.xyz)
- GitHub: [taikoxyz](https://github.com/taikoxyz)
- Twitter: [@taikoxyz](https://twitter.com/taikoxyz)

**Unique**: Based rollup architecture (L1 sequencing)

---

## ZK Infrastructure & Tooling

### Aztec Network

**Status**: Mainnet (Aztec Connect sunset, Aztec 3.0 in development)

```
Type: Privacy-focused ZK rollup
Proof System: PLONK (UltraPLONK)
Language: Noir (ZK DSL)
Focus: Programmable privacy
```

**Key Innovations**:
- **Noir**: High-level ZK language
- **Private smart contracts**: Encrypted state
- **Partial privacy**: Public + private state
- **Recursive proofs**: Efficient aggregation

**Products**:
1. **Aztec Network**: Privacy rollup
2. **Noir**: ZK programming language
3. **Barretenberg**: Proving backend

**Funding**: $120M+ (Paradigm, a16z, etc.)

**Links**:
- Website: [aztec.network](https://aztec.network)
- Noir: [noir-lang.org](https://noir-lang.org)
- Docs: [docs.aztec.network](https://docs.aztec.network)
- GitHub: [AztecProtocol](https://github.com/AztecProtocol)
- Twitter: [@aztecnetwork](https://twitter.com/aztecnetwork)

**Impact**: Noir is widely used beyond Aztec (ZK circuits for any app)

---

### Succinct Labs

**Status**: Active (SP1 zkVM)

```
Type: ZK infrastructure
Product: SP1 (RISC-V zkVM)
Proof System: PLONK
Focus: General-purpose ZK
```

**Key Products**:
1. **SP1**: RISC-V zkVM (prove any Rust program)
2. **Telepathy**: ZK light client
3. **ZK coprocessors**: Offchain computation

**Technology**:
- Prove Rust programs in ZK
- RISC-V instruction set
- Recursive proofs
- GPU acceleration

**Funding**: $55M (Paradigm, Blockchain Capital, etc.)

**Links**:
- Website: [succinct.xyz](https://succinct.xyz)
- Docs: [docs.succinct.xyz](https://docs.succinct.xyz)
- GitHub: [succinctlabs](https://github.com/succinctlabs)
- Twitter: [@succinctlabs](https://twitter.com/succinctlabs)

**Use Cases**:
- ZK light clients
- Cross-chain bridges
- Verifiable computation

---

### RISC Zero

**Status**: Active

```
Type: ZK infrastructure
Product: zkVM (RISC-V)
Proof System: STARKs
Focus: General-purpose ZK
```

**Key Features**:
- Prove any Rust program
- RISC-V instruction set
- STARK-based (no trusted setup)
- Bonsai (proving network)

**Products**:
1. **zkVM**: RISC-V virtual machine
2. **Bonsai**: Proving as a service
3. **Steel**: Ethereum state access in zkVM

**Funding**: $48M (Blockchain Capital, etc.)

**Links**:
- Website: [risczero.com](https://risczero.com)
- Docs: [dev.risczero.com](https://dev.risczero.com)
- GitHub: [risc0](https://github.com/risc0)
- Twitter: [@risczero](https://twitter.com/risczero)

**Differentiator**: STARK-based (vs SNARK competitors)

---

### Axiom

**Status**: Mainnet

```
Type: ZK coprocessor
Proof System: Halo2
Focus: Ethereum historical data
```

**Key Innovation**: Trustless access to Ethereum history
- Prove any historical Ethereum data
- Smart contracts can query past state
- ZK proofs of blockchain data

**Use Cases**:
- Airdrops based on historical activity
- Reputation systems
- DeFi analytics

**Funding**: $20M (Paradigm, Standard Crypto)

**Links**:
- Website: [axiom.xyz](https://axiom.xyz)
- Docs: [docs.axiom.xyz](https://docs.axiom.xyz)
- GitHub: [axiom-crypto](https://github.com/axiom-crypto)
- Twitter: [@axiom_xyz](https://twitter.com/axiom_xyz)

---

### =nil; Foundation

**Status**: Active

```
Type: ZK infrastructure
Focus: zkLLVM, database proofs
Proof System: Placeholder (custom)
```

**Key Products**:
1. **zkLLVM**: Compile C++ to ZK circuits
2. **Proof Market**: Decentralized proving
3. **Database proofs**: Verifiable queries

**Innovation**: Prove any C++ program

**Links**:
- Website: [nil.foundation](https://nil.foundation)
- GitHub: [nilfoundation](https://github.com/nilfoundation)
- Twitter: [@nilfoundation](https://twitter.com/nilfoundation)

---

## ZK Virtual Machines

### Polygon Miden

**Status**: Development

```
Type: ZK-VM
Proof System: STARKs
Language: Miden Assembly
Architecture: Stack-based
```

**Key Features**:
- STARK-based (transparent)
- Turing-complete
- Parallel transaction execution
- Client-side proving

**Innovation**: Local proving (privacy by default)

**Links**:
- Website: [polygon.technology/polygon-miden](https://polygon.technology/polygon-miden)
- Docs: [docs.polygon.technology/miden](https://docs.polygon.technology/miden/)
- GitHub: [0xPolygonMiden](https://github.com/0xPolygonMiden)

---

### Cairo VM (StarkWare)

**Status**: Production

```
Type: ZK-native VM
Proof System: STARKs
Language: Cairo
Architecture: Register-based
```

**Key Features**:
- Designed for ZK from ground up
- Provable computation
- Efficient STARK generation

**Used By**: StarkNet, StarkEx

**Links**:
- Docs: [cairo-lang.org](https://www.cairo-lang.org/)
- GitHub: [starkware-libs/cairo](https://github.com/starkware-libs/cairo)

---

### Valida (Lita)

**Status**: Development

```
Type: ZK-VM
Proof System: STARKs
Focus: Minimal, verifiable
```

**Key Features**:
- Minimal instruction set
- Optimized for ZK
- Rust-based

**Links**:
- GitHub: [lita-xyz/valida](https://github.com/lita-xyz/valida)

---

## Privacy-Focused Projects

### Zcash

**Status**: Mainnet (since 2016)

```
Type: Privacy cryptocurrency
Proof System: Groth16 → Halo 2 (Orchard)
Focus: Shielded transactions
```

**Key Features**:
- Optional privacy (t-addr vs z-addr)
- Shielded transactions (hide sender, receiver, amount)
- Halo 2 (no trusted setup in Orchard)

**Evolution**:
- Sprout (2016): Groth16
- Sapling (2018): Improved Groth16
- Orchard (2022): Halo 2

**Funding**: Bootstrap, ECC, Zcash Foundation

**Links**:
- Website: [z.cash](https://z.cash)
- Docs: [zcash.readthedocs.io](https://zcash.readthedocs.io)
- GitHub: [zcash](https://github.com/zcash)
- Twitter: [@zcash](https://twitter.com/zcash)

**Impact**: Pioneered ZK in crypto (2016)

---

### Aleo

**Status**: Mainnet (2024)

```
Type: Privacy-focused L1
Proof System: Marlin (SNARK)
Language: Leo
Focus: Private applications
```

**Key Features**:
- Private smart contracts
- Leo language (Rust-like)
- Decentralized proving (Proof of Succinct Work)
- Private DeFi

**Funding**: $298M (Kora, SoftBank, a16z)

**Links**:
- Website: [aleo.org](https://aleo.org)
- Docs: [developer.aleo.org](https://developer.aleo.org)
- GitHub: [AleoHQ](https://github.com/AleoHQ)
- Twitter: [@AleoHQ](https://twitter.com/AleoHQ)

---

### Mina Protocol

**Status**: Mainnet

```
Type: Succinct blockchain
Proof System: Pickles (recursive SNARKs)
Size: ~22 KB (constant)
Focus: Lightweight verification
```

**Key Innovation**: Constant-size blockchain
- Recursive proofs compress entire chain
- 22 KB proof of full blockchain state
- Snapps (ZK smart contracts)

**Funding**: $140M+ (Three Arrows, Paradigm, etc.)

**Links**:
- Website: [minaprotocol.com](https://minaprotocol.com)
- Docs: [docs.minaprotocol.com](https://docs.minaprotocol.com)
- GitHub: [MinaProtocol](https://github.com/MinaProtocol)
- Twitter: [@minaprotocol](https://twitter.com/minaprotocol)

**Use Case**: ZK identity, lightweight clients

---

### Penumbra

**Status**: Mainnet

```
Type: Privacy-focused DEX
Proof System: Groth16
Focus: Private DeFi
Chain: Cosmos-based
```

**Key Features**:
- Private DEX (shielded trading)
- IBC integration (Cosmos)
- Sealed-bid batch auctions
- Private staking

**Links**:
- Website: [penumbra.zone](https://penumbra.zone)
- Docs: [guide.penumbra.zone](https://guide.penumbra.zone)
- GitHub: [penumbra-zone](https://github.com/penumbra-zone)

---

## ZK Application Platforms

### Privacy & Scaling Explorations (PSE)

**Status**: Active (Ethereum Foundation)

```
Type: Research & development
Focus: Privacy, scaling, ZK applications
Funding: Ethereum Foundation
```

**Key Projects**:
1. **zkEVM**: Type 1 Ethereum-equivalent
2. **MACI**: Anti-collusion voting
3. **Semaphore**: Anonymous signaling
4. **TLSNotary**: Verifiable web data
5. **ZK Email**: Email proofs
6. **Bandada**: Group management

**Links**:
- Website: [pse.dev](https://pse.dev)
- GitHub: [privacy-scaling-explorations](https://github.com/privacy-scaling-explorations)
- Twitter: [@PrivacyScaling](https://twitter.com/PrivacyScaling)

**Impact**: Driving ZK adoption on Ethereum

---

### 0xPARC

**Status**: Active

```
Type: Research collective
Focus: ZK applications, programmability
```

**Key Projects**:
1. **Dark Forest**: ZK game
2. **ZK learning resources**
3. **ZKHack**: Puzzles and workshops

**Links**:
- Website: [0xparc.org](https://0xparc.org)
- Learning: [learn.0xparc.org](https://learn.0xparc.org)
- Twitter: [@0xPARC](https://twitter.com/0xPARC)

---

## Research & Development

### Geometry

**Status**: Active

```
Type: Research & development
Focus: ZK infrastructure, cryptography
Team: Kobi Gurkan, et al.
```

**Projects**:
- Trusted setup ceremonies
- ZK tooling
- Cryptographic research

**Links**:
- Website: [geometry.xyz](https://geometry.xyz)
- Twitter: [@geometry_xyz](https://twitter.com/geometry_xyz)

---

### Toposware (formerly Polygon Zero)

**Status**: Active

```
Type: Research
Focus: Plonky3, proof systems
```

**Key Contributions**:
- Plonky2 (fastest recursive proofs)
- Plonky3 (modular framework)

**Links**:
- GitHub: [Plonky3](https://github.com/Plonky3/Plonky3)

---

## Funding & Ecosystem

### Major Investors in ZK

| Investor | Notable Investments |
|----------|---------------------|
| **Paradigm** | StarkWare, Aztec, zkSync, Axiom |
| **a16z** | zkSync, Aleo, Aztec |
| **Sequoia** | StarkWare, Scroll, Taiko |
| **Polychain** | Scroll, Mina, Aleo |
| **Blockchain Capital** | RISC Zero, Succinct |
| **Coinbase Ventures** | zkSync, Aztec, StarkWare |

### ZK Market Size

**Funding (2020-2024)**: $2B+ raised
**Market Cap**: $10B+ (ZK tokens)
**Growth**: 10x increase in ZK projects (2020-2024)

---

## Comparison Matrix

### ZK Rollups Comparison

| Project | Type | Proof System | Mainnet | TPS | TVL (approx) |
|---------|------|--------------|---------|-----|--------------|
| **zkSync Era** | Type 4 | PLONK/Boojum | ✅ | 2000+ | $150M+ |
| **StarkNet** | Custom | STARKs | ✅ | 1000+ | $50M+ |
| **Polygon zkEVM** | Type 2.5 | Plonky2 | ✅ | 2000+ | $100M+ |
| **Scroll** | Type 2 | Halo2 | ✅ | 1000+ | $80M+ |
| **Linea** | Type 2 | Custom | ✅ | 2000+ | $50M+ |
| **Taiko** | Type 1 | Multi | ✅ (Alpha) | TBD | TBD |

### ZK Infrastructure Comparison

| Project | Focus | Proof System | Language | Status |
|---------|-------|--------------|----------|--------|
| **Aztec/Noir** | Privacy + DSL | PLONK | Noir | Active |
| **Succinct/SP1** | zkVM | PLONK | Rust | Active |
| **RISC Zero** | zkVM | STARKs | Rust | Active |
| **Axiom** | Coprocessor | Halo2 | Solidity | Mainnet |
| **Miden** | zkVM | STARKs | Miden ASM | Development |

---

## Emerging Trends (2024)

### 1. ZK Coprocessors
- **Axiom**: Ethereum history
- **Brevis**: Cross-chain data
- **Lagrange**: State proofs

### 2. Proof Aggregation Services
- **Nebra**: Universal proof aggregation
- **Aligned Layer**: Proof verification layer

### 3. ZK-as-a-Service
- **Bonsai** (RISC Zero): Proving network
- **Proof Market** (=nil;): Decentralized proving

### 4. Application-Specific ZK
- **ZK Email**: Email proofs
- **ZK Passport**: Identity
- **RLN** (Rate Limiting Nullifier): Spam prevention

---

## Key Takeaways

1. **zkSync & StarkNet**: Leading ZK rollups (different approaches)
2. **Polygon**: Multi-pronged ZK strategy (zkEVM, Miden, research)
3. **Scroll & Taiko**: High EVM compatibility focus
4. **Aztec**: Privacy + Noir language (widely adopted)
5. **Succinct & RISC Zero**: General-purpose zkVMs
6. **PSE**: Ethereum Foundation driving ZK applications

**Market**: Highly competitive, rapid innovation, billions in funding

---

## Next Steps

- **Applications**: Read `05-APPLICATIONS-AND-USE-CASES.md` for real-world use cases
- **Visuals**: Check `06-VISUAL-GUIDES/` for landscape maps
- **Deep Dive**: Pick a project and explore their docs

---

**Resources**:
- [L2Beat](https://l2beat.com/) - L2 metrics and comparison
- [ZK Podcast](https://zeroknowledge.fm/) - Interviews with teams
- [ZK Validator](https://zkvalidator.com/) - ZK project tracker
