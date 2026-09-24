# Aleo vs Ethereum vs Aztec

Snapshot as of September 2026. Adoption numbers change fast; re-check the sources before quoting them.

## Two ways to put ZK in a blockchain

```
 ALEO: "prove each TRANSACTION"               ETHEREUM PLAN: "prove each BLOCK"
 user runs their own function                 transactions stay public
 user's device makes the proof                a GPU prover runs the whole block
 private inputs never leave the device        one proof for the block
 validators verify per-transaction proofs     validators verify it instead of re-executing
 Goal: PRIVACY (+ off-chain compute)          Goal: SCALABILITY / cheap validation
```

Correction worth remembering: Aleo doesn't remove re-execution entirely. The public `finalize` part of a program is still re-run by every validator; only the `function` part is proven by the user.

## Aleo vs Ethereum

| | Ethereum | Aleo |
| --- | --- | --- |
| Who executes | Every validator re-runs every transaction | User proves; validators verify (plus re-run `finalize`) |
| Privacy | Everything public | Private by default (records), public optional (mappings) |
| State | Accounts + contract storage | Encrypted records (UTXO-like) + public mappings |
| Where ZK lives | L2 rollups today; L1 zkEVM planned | Layer 1, every transaction |
| Language | Solidity/Vyper → EVM | Leo → Aleo instructions → circuits |
| Limits | Gas; unbounded loops possible | Fixed-size circuits; loops bounded at compile time |
| Consensus | PoS (Gasper) | PoS (AleoBFT = Narwhal + Bullshark) + coinbase-puzzle provers |

### Ethereum's ZK roadmap (2026)

- **L1 zkEVM:** validators verify block proofs (several independent zkVMs) instead of re-executing. Real-time proving was demonstrated in 2025. EF targets: < 10 s for 99% of blocks, 128-bit security (100-bit at launch), proofs < 300 KiB, prover hardware < ~$100k and 10 kW. Glamsterdam (mid-2026) widens the proving window. Rollout: optional proofs first, then mandatory.
- **Lean Ethereum** (formerly Beam Chain / Lean Consensus): multi-year rebuild with recursive STARK verification, hash-based post-quantum signatures, faster finality, and protocol-level privacy as a long-term goal. Core post-quantum infrastructure targeted around 2029.
- Proving blocks doesn't make Ethereum private. Privacy on Ethereum today comes from L2s like Aztec or privacy apps.

## Aleo vs Aztec

| | Aleo | Aztec |
| --- | --- | --- |
| Type | Its own Layer 1 | Ethereum L2 zk-rollup |
| Security from | Aleo PoS validators | Ethereum |
| Mainnet | Sep 2024; consensus V21 by Sep 2026 | Alpha network 31 Mar 2026 (V5), V6 planned |
| Language | Leo | Noir |
| Proof system | Varuna (Marlin-style, BLS12-377) | PLONK-family "Honk" |
| Private state | Records | Notes (nearly the same model) |
| Public execution | `finalize`, re-run by validators, not proven | Public functions in Aztec's VM, also proven |
| Hides which function was called? | No: `program_id` and `function_name` are plaintext in every transition | Yes, for private calls |
| Ethereum composability | Via bridges / Circle xReserve | Native (e.g. private Aave yield via Nyx) |
| Main audience | Institutions and fintech: private, compliant stablecoin payments | Ethereum-native developers and DeFi users |

**L2BEAT (Aztec):** Stage 2 (immutable contracts, permissionless proposing, escape hatch, walkaway test passed), but flagged with a known critical V5 proving-system vulnerability (found 27 Jul 2026, fix planned for V6). Total value secured was about $1.1K when checked. Aleo isn't listed because it's an L1.

**Aleo adoption signals:** USDCx (Circle, backed 1:1 by USDC via xReserve), USAD (Paxos Labs), Utila institutional wallet integration, Shield wallet (Feb 2026). Q2 2025: ~6.7M transactions, only ~9.6% private.

### Verdict

- **Production and adoption today:** Aleo is clearly ahead.
- **Protocol properties:** Aztec is stronger on paper (Ethereum security, function privacy, proven public execution) but is alpha software.
- Both rely on quantum-vulnerable curves.

## Aleo's moat, honestly

Strengths: private-by-default L1; programmable (not just payments); client-side proving with a universal setup; view keys for selective disclosure; real private-stablecoin adoption; a two-year production lead.

Weaknesses: liquidity and network effects sit on Ethereum; Ethereum and Aztec are converging on privacy; post-quantum exposure; client-side proving cost and circuit limits.

## Sources

- [Shipping an L1 zkEVM #1: Realtime Proving (EF blog)](https://blog.ethereum.org/en/2025/07/10/realtime-proving)
- [zkEVM for L1 block verification (ethereum.org)](https://ethereum.org/roadmap/zkevm/)
- [Post-quantum cryptography on Ethereum (ethereum.org)](https://ethereum.org/roadmap/security/quantum-resistance/)
- [Lean Consensus Roadmap](https://leanroadmap.org/)
- [L2BEAT: Aztec Network](https://l2beat.com/scaling/projects/aztecnetwork)
- [Aztec: Announcing the Alpha Network](https://aztec.network/blog/announcing-the-alpha-network)
- [Aztec: Alpha V5 Proving System Vulnerability](https://aztec.network/blog/alpha-v5-proving-system-vulnerability)
- [Aleo and Circle launch USDCx](https://aleo.org/post/aleo-circle-launch-of-usdcx/)
- [Utila & Aleo](https://aleo.org/post/utila-integration-announcement/)
- [Messari: State of Aleo Q2 2025](https://messari.io/report/state-of-aleo-q2-2025)
