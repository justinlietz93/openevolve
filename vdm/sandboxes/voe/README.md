# VDM-Optimized Openevolve (VOE)

**Status**: Phase A + C Partial - Core Infrastructure + Extended Gate Packs

## Status Reconciliation

**Implemented**: 
- ✅ Phase A: Core infrastructure (domain models, ports, services, evaluator)
- ✅ Phase C (Partial): 9 gate packs covering numerics core + extended physics

**Not Yet Implemented**:
- ❌ Phase B: OpenEvolve integration, mutation testing, syscall hardening
- ❌ Phase C (Remaining): VDM export bridge, benchmark suite, additional domain packs
- ❌ Phase D: Acceptance tests AT-01→AT-10

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
└── tests/               # Test suite (52 tests passing)
```

## Implementation Status

### Phase A: Core Infrastructure ✅ COMPLETE
- [x] Clean Architecture directory structure
- [x] Domain models (Gate, Scorecard, Verdict, Provenance, Candidate)
- [x] JSON schemas for validation
- [x] Application layer ports (interfaces)
- [x] Services (EvolverEngine, Selector)
- [x] Infrastructure (Verifier, Scorecarder)
- [x] Blinded scorecard system
- [x] Gate-based constraint filtering

### Phase C: VDM Gate Packs ✅ PARTIAL (9/15+ domains)
**Implemented** (numerics core + high-priority extensions):
- [x] **Metriplectic Pack** - A2 Axiom structure validation
- [x] **Klein-Gordon Pack** - J-only hyperbolic dynamics
- [x] **Reaction-Diffusion Pack** - Fisher-KPP fronts
- [x] **Flux/Continuity Pack** - Conservation laws
- [x] **Axiom Pack (NEW)** - A0-A7 global cross-run gates
- [x] **Causality Pack (NEW)** - Telegraph-Fisher + DAG ordering
- [x] **A8 Hierarchy Pack (NEW)** - Area-law, depth scaling
- [x] **FRW Cosmology Pack (NEW)** - Friedmann equations
- [x] **Quantum Echoes Pack (NEW)** - CEG/SIE/SMAE validation

**Missing** (identified gaps):
- [ ] Thermodynamic Routing / Wave-Flux Pack
- [ ] Tachyonic Tube Pack (spectrum, condensation)
- [ ] Dark-Photon Portal Pack
- [ ] Quantum-Gravity Bridge Pack (Myrheim-Meyer, holonomy)
- [ ] Intelligence Substrate Pack (determinism receipts)
- [ ] Additional domain-specific packs per VDM proposals

### Phase B: P1 Hardening ⏸️ DEFERRED
- [ ] Refactor OpenEvolve modules
- [ ] Syscall/network/clock hardening
- [ ] Mutation testing integration
- [ ] Property/metamorphic test support
- [ ] CI security pipeline

### Phase D: Validation & Testing ⏸️ NOT STARTED
- [ ] Acceptance tests AT-01 through AT-10
- [ ] VDM export bridge
- [ ] Benchmark suite with real VDM runners
- [ ] Promotion criteria documentation

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

VOE includes **9 gate packs** spanning numerics core and extended physics domains:

### Core Numerics (Original 4)

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

### Extended Physics Surface (New +5)

### 5. Axiom Pack (A0-A7)
Global cross-run gates enforcing VDM program axioms:
- A0: Closure (system self-consistency)
- A2: J/M degeneracies (metriplectic split)
- A3: Causality/locality audits, Noether conservation
- A4/A5: H-theorem (entropy monotonicity)
- A6: Scaling collapse checks
- A7: Measurability protocol

Prevents "accidental physics" by enforcing foundational constraints across all domains.

### 6. Causality Pack
Telegraph-Fisher dynamics + DAG temporal ordering:
- TF dispersion: R² ≥ 0.999
- TF cone slope: v ≤ c(1+0.02)
- DAG: No cycles, no ordering violations
- Interval metrics: Timelike/spacelike validation
- Locality: No superluminal propagation

### 7. A8 Hierarchy Pack
Hierarchical partition structure (Lietz Infinity Conjecture):
- Depth scaling: N(L) = Θ(log(L/λ)), R² ≥ 0.98
- Area law: 2D slope ∈ [1.8, 2.2], 3D slope ∈ [2.8, 3.2]
- Scale-gap: ρ ∈ [1.5, 10.0]
- Boundary concentration: Energy/info fractions > 0
- Detector sensitivity sweeps

### 8. FRW Cosmology Pack
Friedmann-Robertson-Walker validation (decisive, already passing in VDM):
- FRW continuity residual ≤ 1e-10
- Energy density conservation
- Scale factor monotonicity
- Hubble parameter consistency ≥ 0.99
- ΛCDM w+1 residual ≤ 0.02 (advisory)

### 9. Quantum Echoes Pack
CEG/SIE/SMAE quantum echo phenomena:
- CEG: Echo gain ≥ 0, cost delta = 0, instrument trustworthy
- SIE: Stability ≥ 0.95, no weight saturation, plasticity modulation valid
- Ablation: Baseline valid, echo delta significant
- J/M sanity: Echo branch degeneracies ≤ 1e-10
- Momentum drift: `max |ΔP| ≤ 1e-10`

### Usage

```python
from vdm.sandboxes.voe.infrastructure.gate_packs import (
    # Core numerics
    MetriplecticGatePack,
    KleinGordonGatePack,
    ReactionDiffusionGatePack,
    FluxContinuityGatePack,
    # Extended physics
    AxiomGatePack,
    CausalityGatePack,
    A8HierarchyGatePack,
    FRWCosmologyGatePack,
    QuantumEchoesGatePack,
)

# Create gates for a specific physics domain
gates = MetriplecticGatePack.create_gates(grid_size=512)

# Or Klein-Gordon with custom speed of light
gates = KleinGordonGatePack.create_gates(c=1.0)

# Global axiom gates with tolerance scaling
gates = AxiomGatePack.create_gates(grid_size=1024, tolerance_scale=2.0)

# Causality gates
gates = CausalityGatePack.create_gates(c_max=1.0)

# Evaluate against metrics
verdict = scorecarder.evaluate_gates(gates, metrics)
```

See `example_gate_packs.py` for complete examples.

## Testing

```bash
# Run domain tests
python -m unittest discover -s vdm/sandboxes/voe/tests/domain -v

# Run all VOE tests (52 tests)
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

## Development Status Summary

**Current State**: Phase A ✅ Complete + Phase C 🟡 Partial (9/15+ domains)

### Metrics
- **Gate Packs**: 9 implemented (4 core + 5 extended)
- **Unit Tests**: 52 passing (domain: 16, infrastructure: 36)
- **LOC Compliance**: All files ≤ 500 LOC (largest: 167 LOC)
- **Coverage**: Numerics core + foundational axioms + high-priority physics

### Completed
- ✅ Clean Architecture (domain/application/infrastructure)
- ✅ Domain models (Gate, Scorecard, Verdict, Provenance, Candidate)
- ✅ JSON schemas + 4 example gate specs
- ✅ Application ports + services
- ✅ Infrastructure (Verifier, Scorecarder)
- ✅ **9 Gate Packs**: Metriplectic, KG, RD, Flux, Axiom, Causality, A8, FRW, QE
- ✅ Comprehensive tests (52 tests, 100% passing)

### Gaps Identified (Phase C Remaining)
Per VDM physics surface analysis:
- ❌ Thermodynamic Routing / Wave-Flux Pack
- ❌ Tachyonic Tube Pack (spectrum, condensation)
- ❌ Dark-Photon Portal Pack
- ❌ Quantum-Gravity Bridge Pack
- ❌ Intelligence Substrate Pack
- ❌ Additional domain-specific packs (~6+ more)

### Deferred
- ⏸️ Phase B: OpenEvolve refactoring, mutation testing, syscall hardening
- ⏸️ Phase D: AT-01→AT-10 acceptance tests, VDM export bridge, benchmarks

### Priority Next Steps
1. **Immediate**: Complete remaining high-impact gate packs (Wave-Flux, Tachyonic Tube)
2. **Short-term**: Implement AT-01→AT-10 acceptance tests
3. **Medium-term**: VDM export bridge + benchmark suite
4. **Long-term**: Phase B hardening + promotion to `/common/helpers/`

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
