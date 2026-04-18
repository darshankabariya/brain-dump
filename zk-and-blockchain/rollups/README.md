# Ethereum Rollups

This directory contains learning materials about Ethereum Layer 2 rollup solutions and scaling technologies.

## Contents

### General Rollup Documentation
- **[ethereum-rollup-interactions.md](./ethereum-rollup-interactions.md)** - Comprehensive guide on how Ethereum interacts with different types of rollups

### Specific Rollup Deep Dives
- **[aztec-overview.md](./aztec-overview.md)** - Complete overview of Aztec's privacy-first architecture
- **[aztec-technical.md](./aztec-technical.md)** - Technical implementation details of Aztec

## Topics Covered

### Rollup Types
- **Optimistic Rollups** (Arbitrum, Optimism, Base)
- **ZK Rollups** (zkSync, Polygon zkEVM, Scroll, Linea)
- **Custom VM Rollups** (StarkNet, Aztec, Miden)
- **Validium & Hybrid Solutions**

### Key Concepts
- How rollups interact with Ethereum L1
- Data availability strategies
- Proof mechanisms (fraud proofs vs validity proofs)
- Bridge architecture
- Ethereum upgrades for rollups (EIP-4844, Danksharding)
- Rollup economics and cost structures

### Rollup Comparisons
- Architecture differences
- EVM compatibility levels
- Finality times
- Security models
- Use cases and trade-offs

## Focus

This directory focuses on:
- Ethereum Layer 2 scaling solutions
- Rollup architecture and design
- How rollups use ZK proofs for scaling (not ZK fundamentals)
- Ethereum's rollup-centric roadmap
- Cross-rollup communication
- Rollup deployment and operations
- Privacy-focused rollups (Aztec)

For fundamental ZK cryptography and proof systems, see the **[../zk-fundamentals/](../zk-fundamentals/)** directory.

## Relationship with ZK Fundamentals

While some rollups (ZK Rollups) use zero-knowledge proofs, this directory focuses on:
- **Rollup architecture** and how they scale Ethereum
- **Practical implementation** of rollups
- **Ethereum L1/L2 interactions**

For understanding the underlying ZK cryptography (SNARKs, STARKs, proof systems), refer to the ZK Fundamentals directory.
