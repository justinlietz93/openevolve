# VDM-Optimized Openevolve (VOE)

**Status**: Phase C Complete - VDM Physics Gate Packs Implemented

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
│   └── specs/           # JSON schemas + example gate specs
├── application/         # Use cases and coordination
│   ├── ports/           # Abstract interfaces
│   └── services/        # Business logic orchestration
├── infrastructure/      # Concrete implementations
│   ├── adapters/        # External system adapters
│   ├── evaluator/       # Verifier, Scorecarder, etc.
│   ├── gate_packs/      # VDM physics gate packs (NEW)
│   └── repos/           # Data persistence
├── presentation/        # User interfaces
│   └── cli/             # Command-line tools
└── tests/               # Test suite (37 tests passing)
```

## Key Features

### Phase A: P0 Migration ✅ COMPLETE
- [x] Clean Architecture directory structure
- [x] Domain models (Gate, Scorecard, Verdict, Provenance, Candidate)
- [x] JSON schemas for validation
- [x] Application layer ports (interfaces)
- [x] Basic application services (EvolverEngine, Selector)
- [x] Blinded scorecard system
- [x] Gate-based constraint filtering
- [x] Infrastructure (Verifier, Scorecarder)

### Phase B: P1 Hardening (Deferred)
- [ ] Refactor OpenEvolve modules
- [ ] Syscall/network/clock hardening
- [ ] Mutation testing integration
- [ ] Property/metamorphic test support
- [ ] CI security pipeline

### Phase C: VDM Integration ✅ COMPLETE
- [x] Physics gate packs (Metriplectic, KG, RD, Flux)
- [x] Example gate specifications for each pack
- [x] Comprehensive unit tests (13 new tests)
- [x] Usage examples and documentation
- [ ] VDM export bridge (pending)
- [ ] Benchmark suite (pending)

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

## VDM Physics Gate Packs

VOE includes four physics gate packs based on VDM validation requirements:

### 1. Metriplectic Pack
Validates metriplectic operator structure (A2 Axiom):
- Degeneracy constraints: `⟨J·δΣ, δΣ⟩ ≤ 1e-10·N`, `⟨M·δℐ, δℐ⟩ ≤ 1e-10·N`
- J skew-symmetry: `||J + J^T|| ≤ 1e-12`
- M positive semi-definite: `λ_min(M) ≥ -1e-12`
- Lyapunov non-increase: `ΔL_h ≤ 0`
- Noether conservation: `|ΔE|, |ΔP| ≤ 1e-12`

Example: `domain/specs/example_metriplectic_gate.json`

### 2. Klein-Gordon Pack
Validates J-only hyperbolic dynamics:
- Dispersion: `ω² = c²k² + m²` (R² ≥ 0.999)
- Causal cone: `v_front ≤ c(1+0.02)`
- Energy oscillation: slope p ∈ [1.95, 2.05]
- Time-reversal: `||Δ||_∞ ≤ 1e-12`
- Fine-step amplitude: `(A_H/H̄) ≤ 1e-4`

Example: `domain/specs/example_kg_gate.json`

### 3. Reaction-Diffusion Pack
Validates Fisher-KPP pulled fronts:
- Front speed: `c = 2√(Dr)` (rel_err ≤ 0.05)
- Linear fit: R² ≥ 0.98
- Dispersion: `σ(k) = r - Dk²` (median rel_err ≤ 0.10)

Example: `domain/specs/example_rd_gate.json`

### 4. Flux/Continuity Pack
Validates conservation laws:
- Flux continuity: `∂_t e + ∇·s → 0` (RMS ≤ 1e-8)
- Energy drift: `max |ΔE| ≤ 1e-10`
- Momentum drift: `max |ΔP| ≤ 1e-10`

### Usage

```python
from vdm.sandboxes.voe.infrastructure.gate_packs import (
    MetriplecticGatePack,
    KleinGordonGatePack,
    ReactionDiffusionGatePack,
    FluxContinuityGatePack,
)

# Create gates for a specific physics domain
gates = MetriplecticGatePack.create_gates(grid_size=512)

# Or Klein-Gordon with custom speed of light
gates = KleinGordonGatePack.create_gates(c=1.0)

# Evaluate against metrics
verdict = scorecarder.evaluate_gates(gates, metrics)
```

See `example_gate_packs.py` for complete examples.

## Testing

```bash
# Run domain tests
python -m unittest discover -s vdm/sandboxes/voe/tests/domain -v

# Run all VOE tests (37 tests)
PYTHONPATH=. python -m unittest discover -s vdm/sandboxes/voe/tests -v

# Run gate pack examples
PYTHONPATH=. python vdm/sandboxes/voe/example_gate_packs.py
```

## Example Gate Spec

See `domain/specs/example_fft_gate.json` for a complete example with:
- Hard gates (pass rate, mutation score, performance, LOC)
- Soft objectives (latency, complexity)
- Hidden holdouts configuration
- Library and syscall allowlists

## Development Status

**Current Phase**: Phase C Complete - VDM Physics Gate Packs Operational

### Completed (Phase A + C)
- ✅ Directory structure (Clean Architecture)
- ✅ Domain models with dataclasses
- ✅ JSON schemas (gate, scorecard)
- ✅ Application ports (abstract interfaces)
- ✅ Services (EvolverEngine, Selector)
- ✅ Infrastructure (Verifier, Scorecarder)
- ✅ **VDM Physics Gate Packs** (Metriplectic, KG, RD, Flux)
- ✅ **Example gate specifications** (4 complete examples)
- ✅ Unit tests: 37 tests passing (domain + infrastructure + gate packs)
- ✅ Working examples: `example_usage.py`, `example_gate_packs.py`

### Deferred (Phase B)
- ⏸️ OpenEvolve module refactoring
- ⏸️ Mutation testing integration
- ⏸️ Syscall/network hardening
- ⏸️ CI security pipeline

### Next Steps (Phase D)
1. Implement acceptance tests AT-01 through AT-10
2. Create benchmark suite with VDM runners
3. Add VDM export bridge
4. Document promotion criteria to `/common/helpers/`
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
