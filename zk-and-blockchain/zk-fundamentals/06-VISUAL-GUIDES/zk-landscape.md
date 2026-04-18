# ZK Landscape: Visual Overview

## The Complete ZK Ecosystem Map

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ZK ECOSYSTEM LANDSCAPE                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                        LAYER 1: FOUNDATIONS                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────────┐              ┌──────────────────────┐            │
│  │   PROOF SYSTEMS      │              │   CRYPTOGRAPHY       │            │
│  ├──────────────────────┤              ├──────────────────────┤            │
│  │ • SNARKs             │              │ • Elliptic Curves    │            │
│  │   - Groth16          │              │ • Pairings (BLS12)   │            │
│  │   - PLONK            │              │ • Hash Functions     │            │
│  │   - Halo2            │              │ • Polynomial Commit  │            │
│  │   - Marlin           │              │   - KZG              │            │
│  │   - Bulletproofs     │              │   - FRI              │            │
│  │                      │              │   - IPA              │            │
│  │ • STARKs             │              │ • Finite Fields      │            │
│  │   - FRI-based        │              │ • Merkle Trees       │            │
│  │   - Plonky2          │              │                      │            │
│  │   - Plonky3          │              │                      │            │
│  └──────────────────────┘              └──────────────────────┘            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                    LAYER 2: INFRASTRUCTURE & TOOLS                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐               │
│  │   LANGUAGES    │  │   FRAMEWORKS   │  │   LIBRARIES    │               │
│  ├────────────────┤  ├────────────────┤  ├────────────────┤               │
│  │ • Circom       │  │ • Halo2        │  │ • libsnark     │               │
│  │ • Noir         │  │ • Arkworks     │  │ • libSTARK     │               │
│  │ • Cairo        │  │ • Bellman      │  │ • gnark        │               │
│  │ • Leo          │  │ • Plonky2/3    │  │ • snarkjs      │               │
│  │ • ZoKrates     │  │ • Risc0        │  │ • Winterfell   │               │
│  │ • Miden ASM    │  │ • SP1          │  │ • Barretenberg │               │
│  └────────────────┘  └────────────────┘  └────────────────┘               │
│                                                                             │
│  ┌────────────────────────────────────────────────────────┐                │
│  │              DEVELOPER TOOLS                           │                │
│  ├────────────────────────────────────────────────────────┤                │
│  │ • Hardhat-ZK (zkSync)                                  │                │
│  │ • Foundry-ZK                                           │                │
│  │ • Cairo-lang toolchain                                 │                │
│  │ • Noir VSCode extension                                │                │
│  │ • ZK debuggers & profilers                             │                │
│  └────────────────────────────────────────────────────────┘                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                    LAYER 3: PLATFORMS & PROTOCOLS                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────┐          │
│  │                    ZK ROLLUPS (L2s)                          │          │
│  ├──────────────────────────────────────────────────────────────┤          │
│  │                                                              │          │
│  │  Type 1 (Ethereum-Equivalent)                                │          │
│  │  └─ Taiko (Multi-prover)                                     │          │
│  │                                                              │          │
│  │  Type 2 (EVM-Equivalent)                                     │          │
│  │  ├─ Scroll (Halo2)                                           │          │
│  │  ├─ Polygon zkEVM (Plonky2)                                  │          │
│  │  └─ Linea (Custom)                                           │          │
│  │                                                              │          │
│  │  Type 4 (High-Level Equivalent)                              │          │
│  │  ├─ zkSync Era (PLONK/Boojum)                                │          │
│  │  └─ StarkNet (STARKs/Cairo)                                  │          │
│  │                                                              │          │
│  └──────────────────────────────────────────────────────────────┘          │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────┐          │
│  │                    ZK VIRTUAL MACHINES                       │          │
│  ├──────────────────────────────────────────────────────────────┤          │
│  │ • Polygon Miden (STARK-based, stack VM)                      │          │
│  │ • Cairo VM (STARK-based, register VM)                        │          │
│  │ • RISC Zero zkVM (RISC-V, STARKs)                            │          │
│  │ • SP1 (RISC-V, PLONK)                                        │          │
│  │ • Valida (Minimal, STARKs)                                   │          │
│  └──────────────────────────────────────────────────────────────┘          │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────┐          │
│  │                 PRIVACY PLATFORMS                            │          │
│  ├──────────────────────────────────────────────────────────────┤          │
│  │ • Aztec (Privacy rollup, Noir)                               │          │
│  │ • Zcash (Shielded payments)                                  │          │
│  │ • Aleo (Private smart contracts)                             │          │
│  │ • Mina (Succinct blockchain)                                 │          │
│  │ • Penumbra (Private DEX)                                     │          │
│  └──────────────────────────────────────────────────────────────┘          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                      LAYER 4: APPLICATIONS                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│  │   SCALING   │  │   PRIVACY   │  │  IDENTITY   │  │    DeFi     │       │
│  ├─────────────┤  ├─────────────┤  ├─────────────┤  ├─────────────┤       │
│  │ • zkSync    │  │ • Zcash     │  │ • zkPassport│  │ • dYdX      │       │
│  │ • StarkNet  │  │ • Tornado   │  │ • ZK Email  │  │ • Penumbra  │       │
│  │ • Polygon   │  │ • Aztec     │  │ • Semaphore │  │ • Aztec     │       │
│  │ • Scroll    │  │ • Railgun   │  │ • Sismo     │  │ • Sorare    │       │
│  │ • Linea     │  │ • Penumbra  │  │ • Polygon   │  │ • Immutable │       │
│  └─────────────┘  └─────────────┘  │   ID        │  └─────────────┘       │
│                                    └─────────────┘                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│  │   GAMING    │  │ GOVERNANCE  │  │   BRIDGES   │  │  EMERGING   │       │
│  ├─────────────┤  ├─────────────┤  ├─────────────┤  ├─────────────┤       │
│  │ • Dark      │  │ • MACI      │  │ • Telepathy │  │ • ZK ML     │       │
│  │   Forest    │  │ • Snapshot  │  │ • Axiom     │  │ • ZK Oracle │       │
│  │ • Isaac     │  │   X         │  │ • Brevis    │  │ • ZK Social │       │
│  │ • Loot      │  │ • Aragon    │  │ • Lagrange  │  │ • ZK Supply │       │
│  │   Realms    │  │   ZK        │  │ • Succinct  │  │   Chain     │       │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                   LAYER 5: RESEARCH & ECOSYSTEM                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────┐          │
│  │                    RESEARCH GROUPS                           │          │
│  ├──────────────────────────────────────────────────────────────┤          │
│  │ • PSE (Ethereum Foundation)                                  │          │
│  │ • 0xPARC                                                     │          │
│  │ • a16z Crypto Research                                       │          │
│  │ • Geometry                                                   │          │
│  │ • Toposware (Polygon Zero)                                   │          │
│  │ • StarkWare Research                                         │          │
│  └──────────────────────────────────────────────────────────────┘          │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────┐          │
│  │                    ACADEMIC LABS                             │          │
│  ├──────────────────────────────────────────────────────────────┤          │
│  │ • UC Berkeley (RDI)                                          │          │
│  │ • Stanford (Applied Crypto)                                  │          │
│  │ • MIT (CSAIL)                                                │          │
│  │ • Technion (Israel)                                          │          │
│  │ • Georgetown (Thaler)                                        │          │
│  └──────────────────────────────────────────────────────────────┘          │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────┐          │
│  │                    COMMUNITY & EVENTS                        │          │
│  ├──────────────────────────────────────────────────────────────┤          │
│  │ • ZKProof (Standards)                                        │          │
│  │ • ZKHack (Hackathons, puzzles)                               │          │
│  │ • ZK Summit                                                  │          │
│  │ • ZK Whiteboard Sessions                                     │          │
│  │ • ZK Podcast                                                 │          │
│  └──────────────────────────────────────────────────────────────┘          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Technology Stack Breakdown

### The ZK Stack (Web Dev Analogy)

```
┌─────────────────────────────────────────────────────────────┐
│                    WEB DEVELOPMENT                          │
├─────────────────────────────────────────────────────────────┤
│ Applications    │ Twitter, Facebook, Gmail                  │
│ Frameworks      │ React, Vue, Angular                       │
│ Languages       │ JavaScript, TypeScript                    │
│ Runtime         │ Node.js, Browsers                         │
│ Protocols       │ HTTP, WebSocket                           │
│ Infrastructure  │ AWS, Cloudflare                           │
└─────────────────────────────────────────────────────────────┘

                            ↓ ANALOGY ↓

┌─────────────────────────────────────────────────────────────┐
│                    ZK DEVELOPMENT                           │
├─────────────────────────────────────────────────────────────┤
│ Applications    │ zkSync dApps, Dark Forest, MACI          │
│ Platforms       │ zkSync, StarkNet, Aztec                   │
│ Languages       │ Noir, Cairo, Circom                       │
│ VMs             │ zkEVM, Cairo VM, Miden VM                 │
│ Proof Systems   │ PLONK, STARKs, Groth16                    │
│ Infrastructure  │ Proving networks, Sequencers              │
└─────────────────────────────────────────────────────────────┘
```

---

## Market Segmentation

### By Use Case

```
                    ZK MARKET SEGMENTATION

    ┌──────────────────────────────────────────────────┐
    │         SCALING (Largest Market)                 │
    │  • ZK Rollups: zkSync, StarkNet, Polygon         │
    │  • Market Size: $500M+ TVL                       │
    │  • Growth: 10x in 2 years                        │
    └──────────────────────────────────────────────────┘
                            │
    ┌──────────────────────────────────────────────────┐
    │         PRIVACY (Growing)                        │
    │  • Payments: Zcash, Tornado Cash                 │
    │  • DeFi: Aztec, Penumbra                         │
    │  • Market Size: $1B+ market cap                  │
    └──────────────────────────────────────────────────┘
                            │
    ┌──────────────────────────────────────────────────┐
    │         IDENTITY (Emerging)                      │
    │  • zkPassport, ZK Email, Semaphore               │
    │  • Market Size: Early stage                      │
    │  • Potential: Massive (billions of users)        │
    └──────────────────────────────────────────────────┘
                            │
    ┌──────────────────────────────────────────────────┐
    │         INFRASTRUCTURE (Enabling)                │
    │  • zkVMs: RISC Zero, SP1, Miden                  │
    │  • Languages: Noir, Cairo                        │
    │  • Market Size: $100M+ funding                   │
    └──────────────────────────────────────────────────┘
                            │
    ┌──────────────────────────────────────────────────┐
    │         EMERGING (Future)                        │
    │  • ZK ML, ZK Oracles, ZK Compliance              │
    │  • Market Size: Research stage                   │
    │  • Potential: Huge (AI + blockchain)             │
    └──────────────────────────────────────────────────┘
```

---

## Competitive Landscape

### ZK Rollups Competition

```
                    COMPATIBILITY
                         ↑
                         │
    Type 1 (100%)        │         Taiko
                         │
                         │
    Type 2 (99%)         │    Scroll, Polygon zkEVM
                         │
                         │
    Type 3 (95%)         │
                         │
                         │
    Type 4 (90%)         │    zkSync, StarkNet
                         │
                         └────────────────────────→
                                              PERFORMANCE
                                              (Proving Speed)

Legend:
• Left (High Compatibility): Easier migration, slower proving
• Right (High Performance): Faster proving, some incompatibilities
```

### Proof System Trade-offs

```
                    TRANSPARENCY
                         ↑
                         │
    Transparent          │    STARKs (StarkNet, Miden)
    (No Setup)           │    Halo2 (Scroll, Zcash)
                         │
                         │
    Universal            │    PLONK (zkSync, Aztec)
    Setup                │
                         │
                         │
    Trusted              │    Groth16 (Zcash old, Tornado)
    Setup                │
                         │
                         └────────────────────────→
                                              PROOF SIZE
                                              (Smaller = Better)

Legend:
• Top-Left: Transparent but larger proofs
• Bottom-Right: Smallest proofs but trusted setup
```

---

## Funding Landscape

### Top Funded ZK Projects (2020-2024)

```
┌─────────────────────────────────────────────────────────┐
│  zkSync (Matter Labs)         │ $458M  ████████████████ │
├─────────────────────────────────────────────────────────┤
│  Aleo                          │ $298M  ██████████████   │
├─────────────────────────────────────────────────────────┤
│  StarkWare                     │ $273M  █████████████    │
├─────────────────────────────────────────────────────────┤
│  Polygon (incl. ZK)            │ $450M  ███████████████  │
├─────────────────────────────────────────────────────────┤
│  Mina Protocol                 │ $140M  ████████         │
├─────────────────────────────────────────────────────────┤
│  Aztec                         │ $120M  ███████          │
├─────────────────────────────────────────────────────────┤
│  Scroll                        │  $80M  █████            │
├─────────────────────────────────────────────────────────┤
│  Succinct                      │  $55M  ████             │
├─────────────────────────────────────────────────────────┤
│  RISC Zero                     │  $48M  ███              │
├─────────────────────────────────────────────────────────┤
│  Taiko                         │  $37M  ███              │
└─────────────────────────────────────────────────────────┘

Total ZK Funding (2020-2024): $2B+
```

---

## Geographic Distribution

### ZK Companies by Region

```
┌─────────────────────────────────────────────────────────┐
│                    NORTH AMERICA                        │
├─────────────────────────────────────────────────────────┤
│ • Aztec (San Francisco)                                 │
│ • Aleo (San Francisco)                                  │
│ • RISC Zero (Seattle)                                   │
│ • Succinct (San Francisco)                              │
│ • 0xPARC (San Francisco)                                │
│ • Mina Protocol (San Francisco)                         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                       EUROPE                            │
├─────────────────────────────────────────────────────────┤
│ • Matter Labs/zkSync (Berlin)                           │
│ • StarkWare (Israel)                                    │
│ • Polygon (Switzerland/Global)                          │
│ • Scroll (Global, EU presence)                          │
│ • =nil; Foundation (Russia/Global)                      │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                        ASIA                             │
├─────────────────────────────────────────────────────────┤
│ • Scroll (China/Singapore)                              │
│ • Taiko (Singapore)                                     │
│ • PSE (Global, Asia presence)                           │
└─────────────────────────────────────────────────────────┘
```

---

## Timeline Evolution

### ZK Development Timeline

```
2016 ─────────────────────────────────────────────────────
      │
      ├─ Zcash Launch (First major ZK application)
      │
2018 ─────────────────────────────────────────────────────
      │
      ├─ STARKs Paper (Ben-Sasson et al.)
      │
2019 ─────────────────────────────────────────────────────
      │
      ├─ PLONK Paper (Universal setup)
      ├─ Halo Paper (No trusted setup recursion)
      │
2020 ─────────────────────────────────────────────────────
      │
      ├─ Dark Forest (First ZK game)
      ├─ Halo 2 Release
      ├─ ZK Rollup race begins
      │
2021 ─────────────────────────────────────────────────────
      │
      ├─ StarkNet Alpha
      ├─ zkSync 2.0 Testnet
      ├─ Aztec Connect Launch
      │
2022 ─────────────────────────────────────────────────────
      │
      ├─ Plonky2 Release (Fast recursion)
      ├─ ZK-EVM announcements (Polygon, Scroll)
      ├─ Tornado Cash sanctions
      │
2023 ─────────────────────────────────────────────────────
      │
      ├─ zkSync Era Mainnet
      ├─ Polygon zkEVM Mainnet
      ├─ Scroll Mainnet
      ├─ Linea Mainnet
      ├─ ZK identity boom (zkPassport, ZK Email)
      │
2024 ─────────────────────────────────────────────────────
      │
      ├─ Plonky3 Release
      ├─ Taiko Mainnet
      ├─ Aleo Mainnet
      ├─ ZK ML research explosion
      ├─ ZK coprocessors emerge
      │
2025+ ────────────────────────────────────────────────────
      │
      ├─ ZK-EVM maturity
      ├─ ZK AI integration
      ├─ Mainstream ZK adoption
      └─ ZK compliance solutions
```

---

## Key Relationships

### Ecosystem Connections

```
                    ETHEREUM FOUNDATION
                            │
                ┌───────────┼───────────┐
                │           │           │
               PSE      Vitalik    Grants Program
                │           │           │
        ┌───────┼───────┐   │   ┌───────┼───────┐
        │       │       │   │   │       │       │
      zkEVM   MACI  Semaphore │ Scroll Taiko  Aztec
                              │
                    ┌─────────┼─────────┐
                    │                   │
              ZK Rollups          Research Labs
                    │                   │
        ┌───────────┼───────────┐       │
        │           │           │       │
     zkSync    StarkNet    Polygon   a16z, Paradigm
        │           │           │       │
    Boojum      Cairo VM    Plonky2    │
                                        │
                                   Funding →
                                   Research →
```

### Technology Dependencies

```
                    PROOF SYSTEMS
                    (Groth16, PLONK, STARKs)
                            │
                ┌───────────┼───────────┐
                │                       │
        POLYNOMIAL COMMITMENTS    CONSTRAINT SYSTEMS
        (KZG, FRI, IPA)           (R1CS, PLONK, AIR)
                │                       │
                └───────────┬───────────┘
                            │
                    CIRCUIT COMPILERS
                    (Circom, Noir, Cairo)
                            │
                ┌───────────┼───────────┐
                │           │           │
            ZK ROLLUPS   ZK VMs    PRIVACY APPS
            (zkSync)   (Miden)     (Zcash)
```

---

## Market Dynamics

### Competitive Moats

```
┌─────────────────────────────────────────────────────────┐
│  NETWORK EFFECTS (Strongest)                            │
│  • zkSync: Largest ecosystem, most dApps                │
│  • StarkNet: Cairo developer community                  │
│  • Polygon: Brand + existing user base                  │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  TECHNOLOGY MOATS (Strong)                              │
│  • Plonky2/3: Fastest recursion (Polygon)               │
│  • Boojum: Custom STARK (zkSync)                        │
│  • Halo2: No trusted setup (Scroll, Zcash)              │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  DEVELOPER TOOLS (Growing)                              │
│  • Noir: Easiest ZK language (Aztec)                    │
│  • Cairo: Most mature ZK-native (StarkWare)             │
│  • Hardhat-ZK: Familiar tooling (zkSync)                │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  ECOSYSTEM FUNDING (Moderate)                           │
│  • zkSync: $458M raised                                 │
│  • Polygon: $450M raised                                │
│  • StarkWare: $273M raised                              │
└─────────────────────────────────────────────────────────┘
```

---

## Future Outlook (2024-2026)

### Expected Developments

```
┌─────────────────────────────────────────────────────────┐
│  SHORT TERM (2024-2025)                                 │
├─────────────────────────────────────────────────────────┤
│ ✓ ZK-EVM maturity (Type 1-2 production ready)           │
│ ✓ ZK identity mainstream (zkPassport, ZK Email)         │
│ ✓ ZK coprocessors (Axiom, Brevis, Lagrange)             │
│ ✓ Proof aggregation services                            │
│ ✓ Hardware acceleration (GPUs, FPGAs, ASICs)            │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  MEDIUM TERM (2025-2026)                                │
├─────────────────────────────────────────────────────────┤
│ ⧗ ZK ML integration (verifiable AI)                     │
│ ⧗ ZK compliance solutions (regulatory friendly)         │
│ ⧗ Cross-chain ZK (universal proofs)                     │
│ ⧗ ZK gaming explosion (private state games)             │
│ ⧗ ZK social networks (privacy + verification)           │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  LONG TERM (2026+)                                      │
├─────────────────────────────────────────────────────────┤
│ ○ Mainstream adoption (billions of users)               │
│ ○ ZK as default (not optional)                          │
│ ○ Quantum-resistant ZK (STARKs dominant?)               │
│ ○ ZK hardware (phones, laptops with ZK chips)           │
│ ○ ZK AI (verifiable AGI)                                │
└─────────────────────────────────────────────────────────┘

Legend: ✓ High confidence  ⧗ Medium confidence  ○ Speculative
```

---

## Key Takeaways

1. **Layered ecosystem**: Foundations → Infrastructure → Platforms → Applications
2. **Multiple winners**: Different solutions for different use cases
3. **Rapid innovation**: New breakthroughs every 6-12 months
4. **Massive funding**: $2B+ invested, more coming
5. **Early stage**: Most applications still emerging

**The ZK landscape is vast and growing rapidly!**
