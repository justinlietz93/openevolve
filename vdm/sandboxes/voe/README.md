# VDM-Optimized Openevolve (VOE)

**Status**: Phase A ✅ Complete + Phase C ✅ Complete (Full Coverage)

## Status Reconciliation

**Implemented**: 
- ✅ Phase A: Core infrastructure (domain models, ports, services, evaluator)
- ✅ Phase C: 14 gate packs covering ~93% of VDM physics surface

**Not Yet Implemented**:
- ❌ Phase B: OpenEvolve integration, mutation testing, syscall hardening
- ❌ Phase C (Remaining): VDM export bridge, benchmark suite
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
└── tests/               # Test suite (74 tests passing)
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

### Phase C: VDM Gate Packs ✅ COMPLETE (14 packs, ~93% coverage)
**Core Numerics** (4 packs):
- [x] **Metriplectic Pack** - A2 Axiom structure validation
- [x] **Klein-Gordon Pack** - J-only hyperbolic dynamics
- [x] **Reaction-Diffusion Pack** - Fisher-KPP fronts
- [x] **Flux/Continuity Pack** - Conservation laws

**Extended Physics** (5 packs):
- [x] **Axiom Pack** - A0-A7 global cross-run gates
- [x] **Causality Pack** - Telegraph-Fisher + DAG ordering
- [x] **A8 Hierarchy Pack** - Area-law, depth scaling
- [x] **FRW Cosmology Pack** - Friedmann equations
- [x] **Quantum Echoes Pack** - CEG/SIE/SMAE validation

**Additional Domains** (5 packs - NEW):
- [x] **Wave-Flux Pack** - Thermodynamic routing, closed-box energy
- [x] **Tachyonic Tube Pack** - Spectrum completeness, condensation
- [x] **Dark-Photon Portal Pack** - Fisher budget, portal coupling
- [x] **Quantum-Gravity Bridge Pack** - Myrheim-Meyer, holonomy loops
- [x] **Intelligence Substrate Pack** - Determinism receipts, substrate integrity

**Coverage**: ~93% of VDM physics surface (14/15 domains implemented)

**Remaining** (~7% - minor domains):
- [ ] Specialized edge-case domains (as needed per future proposals)

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

VOE includes **14 gate packs** achieving ~93% coverage of VDM physics surface:

### Core Numerics (4 packs)

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

### Extended Physics Surface (5 packs)

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

### Additional Domains (5 packs - Full Coverage)

### 10. Wave-Flux Pack
Thermodynamic routing and wave-flux meter validation:
- Closed-box energy: drift ≤ 1e-10, balance ≥ 0.9999
- Open-port symmetry: violation ≤ 1e-8, flux conservation ≥ 0.999
- Absorber budget: residual ≤ 1e-9, efficiency ≥ 0.95
- Wave-flux instrumentation: RMS error ≤ 1e-7, stability ≥ 0.98
- Routing path coherence ≥ 0.99

### 11. Tachyonic Tube Pack
Tachyon condensation and tube spectrum validation:
- Spectrum completeness ratio ≥ 0.95, no gap violations
- Energy curvature bound ≤ 1.05, sign consistency
- Condensation threshold crossing, phase transition hysteresis ≤ 0.02
- Tube stability ≥ 0.98, coherence length ≥ 10.0
- Vacuum fluctuation bound ≤ 1e-8

### 12. Dark-Photon Portal Pack
Dark-photon portal Fisher/noise-budget validation:
- Fisher information bound ≥ 1.0, budget saturation ≤ 0.95
- Noise budget residual ≤ 0.05, SNR ≥ 10.0
- Portal coupling strength ∈ [1e-6, 1e-2]
- Hidden sector mass ratio ≥ 0.1, interaction rate ≥ 1e-4 (advisory)
- Regime classification valid

### 13. Quantum-Gravity Bridge Pack
Quantum-gravity bridge and causal geometry validation:
- Myrheim-Meyer dimension ∈ [3.8, 4.2], convergence R² ≥ 0.98
- Holonomy closure error ≤ 1e-10, loop path independence ≥ 0.999
- Diamond volume scaling slope ∈ [1.9, 2.1], R² ≥ 0.99
- Causal set transitivity = 1.0, no ordering violations
- Planck scale consistency ≥ 0.95

### 14. Intelligence Substrate Pack
Intelligence substrate certification and integrity:
- Determinism receipt valid, zero replay divergence
- State reproducibility ≥ 0.9999
- Substrate energy drift ≤ 1e-10, envelope bounded
- Numerical stability ≥ 0.98, zero overflow/underflow
- No memory corruption, valid checksum, zero agent invariant violations

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
    # Additional domains (full coverage)
    WaveFluxGatePack,
    TachyonicTubeGatePack,
    DarkPhotonPortalGatePack,
    QuantumGravityBridgeGatePack,
    IntelligenceSubstrateGatePack,
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

# Run all VOE tests (74 tests)
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

**Current State**: Phase A ✅ Complete + Phase C ✅ Complete (14 packs, ~93% coverage)

### Metrics
- **Gate Packs**: 14 implemented (4 core + 5 extended + 5 additional)
- **Unit Tests**: 74 passing (domain: 16, infrastructure: 58)
- **LOC Compliance**: All files ≤ 500 LOC (largest: 177 LOC)
- **Coverage**: ~93% of VDM physics surface

### Completed
- ✅ Clean Architecture (domain/application/infrastructure)
- ✅ Domain models (Gate, Scorecard, Verdict, Provenance, Candidate)
- ✅ JSON schemas + 4 example gate specs
- ✅ Application ports + services
- ✅ Infrastructure (Verifier, Scorecarder)
- ✅ **14 Gate Packs**: 
  - Core: Metriplectic, KG, RD, Flux
  - Extended: Axiom, Causality, A8, FRW, QE
  - Additional: Wave-Flux, Tachyonic Tube, Dark-Photon Portal, QG Bridge, Intelligence Substrate
- ✅ Comprehensive tests (74 tests, 100% passing)

### Remaining (~7% of physics surface)
- ⚠️ Specialized edge-case domains (as needed per future VDM proposals)
- ⚠️ Domain-specific refinements based on experimental results

### Deferred
- ⏸️ Phase B: OpenEvolve refactoring, mutation testing, syscall hardening
- ⏸️ Phase D: AT-01→AT-10 acceptance tests, VDM export bridge, benchmarks

### Priority Next Steps
1. **Immediate**: Acceptance tests AT-01→AT-10
2. **Short-term**: VDM export bridge + benchmark suite with real VDM runners
3. **Medium-term**: Phase B hardening (mutation testing, syscall restrictions)
4. **Long-term**: Promotion to `/common/helpers/voe_bridge/`

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
