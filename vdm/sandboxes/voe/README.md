# VDM-Optimized Openevolve (VOE)

**Status**: Phase A - Core Infrastructure Implementation

## Overview

VOE is a VDM-specific, gate-driven code evolution system built on OpenEvolve that produces high-precision solvers/instruments under strict scientific constraints. It is designed for the [Prometheus VDM](https://github.com/justinlietz93/Prometheus_VDM) computational physics framework.

## Architecture

VOE follows Clean Architecture principles:

```
presentation → application → domain ← infrastructure
```

### Directory Structure

```
vdm/sandboxes/voe/
├── domain/              # Core business logic (framework-free)
│   ├── models/          # Gate, Verdict, Scorecard, Provenance, Candidate
│   └── specs/           # JSON schemas for validation
├── application/         # Use cases and coordination
│   ├── ports/           # Abstract interfaces
│   └── services/        # Business logic orchestration
├── infrastructure/      # Concrete implementations
│   ├── adapters/        # External system adapters
│   ├── evaluator/       # Verifier, Scorecarder, etc.
│   └── repos/           # Data persistence
├── presentation/        # User interfaces
│   └── cli/             # Command-line tools
└── tests/               # Test suite
```

## Key Features (Planned)

### Phase A: P0 Migration (Current)
- [x] Clean Architecture directory structure
- [x] Domain models (Gate, Scorecard, Verdict, Provenance, Candidate)
- [x] JSON schemas for validation
- [x] Application layer ports (interfaces)
- [x] Basic application services (EvolverEngine, Selector)
- [ ] Blinded scorecard system (in progress)
- [ ] Gate-based constraint filtering
- [ ] C/V container split (logical)
- [ ] Provenance receipt generation

### Phase B: P1 Hardening
- [ ] LOC constraint enforcement (500 lines/file)
- [ ] Syscall/network/clock hardening
- [ ] Mutation testing integration
- [ ] Property/metamorphic test support
- [ ] CI security pipeline

### Phase C: VDM Integration
- [ ] Physics gate packs (Metriplectic, KG, RD, Flux)
- [ ] VDM export bridge
- [ ] Benchmark suite

## Design Principles

### 1. Blinded Evaluation
Candidates never see:
- Test case inputs/outputs
- Ground truth labels
- Specific failure indices

Only aggregate metrics are exposed via Scorecards.

### 2. Gate-First Selection
Hard gates are constraints, not scores:
1. Filter by gate pass/fail
2. Pareto rank survivors on soft objectives
3. Maintain diversity via MAP-Elites

### 3. Reproducibility
Every evaluation generates:
- `gates.verdict.json` - Final verdict
- `provenance.json` - Full reproducibility metadata
- `performance.json` - Performance metrics
- Build and evaluation logs

### 4. Security-First
- ROCm-only (no CUDA)
- Read-only filesystem for tests/gold
- Network deny
- Syscall whitelist
- Constant-time I/O to prevent timing attacks

## Code Constraints (AMOS)

All code must comply with the Apex Modular Organization Standard:

- **≤ 500 LOC per file** (enforced via gates)
- **≥ 90% test coverage**
- **≥ 0.85 mutation score**
- **Clean Architecture**: No outer→inner imports
- **Domain layer**: Framework-free

## Testing

```bash
# Run domain tests
python -m unittest discover -s vdm/sandboxes/voe/tests/domain -v

# Run all VOE tests (when available)
python -m unittest discover -s vdm/sandboxes/voe/tests -v
```

## Example Gate Spec

See `domain/specs/example_fft_gate.json` for a complete example with:
- Hard gates (pass rate, mutation score, performance, LOC)
- Soft objectives (latency, complexity)
- Hidden holdouts configuration
- Library and syscall allowlists

## Development Status

**Current Phase**: Phase A (P0 Migration)

### Completed
- ✅ Directory structure
- ✅ Domain models with dataclasses
- ✅ JSON schemas (gate, scorecard)
- ✅ Application ports (abstract interfaces)
- ✅ Basic services (EvolverEngine, Selector)
- ✅ Infrastructure stubs (Verifier, Scorecarder)
- ✅ Unit tests for core domain models

### In Progress
- 🔄 Blinded evaluator implementation
- 🔄 Gate evaluation system
- 🔄 Container split (C/V separation)

### Next Steps
1. Complete Phase A implementation
2. Add integration tests
3. Connect to OpenEvolve core
4. Begin Phase B hardening

## Integration with OpenEvolve

VOE extends OpenEvolve by:
- Adding gate-based constraints
- Implementing blinded evaluation
- Enforcing security policies
- Generating provenance receipts

It reuses OpenEvolve's:
- Async evolution loop
- Diff-based code mutation
- Program database (with extensions)
- LLM ensemble

## Promotion Criteria

To promote from `/sandboxes/voe/` to `/common/helpers/voe_bridge/`:

1. All acceptance tests (AT-01 through AT-10) pass
2. At least one VDM physics pack validates a solver
3. No security regressions for 2 releases
4. Full documentation and examples

## References

- **VDM Repository**: https://github.com/justinlietz93/Prometheus_VDM
- **OpenEvolve**: Parent project this extends
- **Requirements**: See original problem statement for full specification

---

**Maintainer**: VDM Systems  
**Reviewers**: VDM Research (physics gates), VDM Infra (ROCm compliance)  
**License**: Apache 2.0 (inherited from OpenEvolve)
