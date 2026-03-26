# VOE Integration Guide

## Overview

This guide explains how to integrate VOE (VDM-Optimized Openevolve) with the existing OpenEvolve codebase and how to use it for gate-driven evolution.

## Architecture Summary

VOE extends OpenEvolve with:

1. **Gate-based constraints** - Hard requirements that must pass
2. **Blinded evaluation** - Scorecards with aggregates only
3. **Security hardening** - ROCm-only, syscall limits, network deny
4. **Provenance tracking** - Full reproducibility metadata

## Quick Start

### 1. Using VOE Domain Models

```python
from vdm.sandboxes.voe.domain.models import Gate, GateOperator, Candidate

# Define hard gates
gates = [
    Gate(metric="pass_rate", op=GateOperator.GTE, value=0.9),
    Gate(metric="runtime_ms", op=GateOperator.LTE, value=500.0),
]

# Create candidate
candidate = Candidate(
    id="unique-uuid",
    code="def my_function(): pass",
    language="python",
)
```

### 2. Running Evaluation

```python
from vdm.sandboxes.voe.infrastructure.evaluator import Verifier, Scorecarder

config = {"timeout": 60}
verifier = Verifier(config)
scorecarder = Scorecarder(verifier)

# Collect metrics (from real execution)
metrics = {
    "pass_rate": 0.95,
    "runtime_ms": 450.0,
}

# Evaluate gates
gate_verdict = scorecarder.evaluate_gates(gates, metrics)

# Create blinded scorecard
scorecard = scorecarder.create_scorecard(
    candidate_id=candidate.id,
    metrics=metrics,
    gate_verdict=gate_verdict,
)

# Check if eligible
if scorecard.passes_gates():
    print("Candidate eligible for selection")
```

### 3. Using the CLI (Stub)

```bash
# Submit candidate
voe submit path/to/code.py

# Run evaluation
voe run <candidate-id> --gate gate_spec.json

# Review results
voe review <candidate-id>

# Export bundle
voe export <candidate-id> --bundle
```

## Integration with OpenEvolve

### Phase 1: Coexistence (Current)

VOE lives in `/vdm/sandboxes/voe/` and can be used alongside OpenEvolve:

```python
# Use OpenEvolve for evolution loop
from openevolve import OpenEvolve

# Use VOE for gate evaluation
from vdm.sandboxes.voe.domain.models import Gate, GateOperator
from vdm.sandboxes.voe.infrastructure.evaluator import Scorecarder

# Custom evaluator that applies VOE gates
def voe_evaluator(program_path):
    # Run OpenEvolve's normal evaluation
    base_result = evaluate(program_path)
    
    # Apply VOE gates
    gates = [...]
    scorecarder = Scorecarder(...)
    verdict = scorecarder.evaluate_gates(gates, base_result.metrics)
    
    # Return combined result
    return {"metrics": base_result.metrics, "gates_passed": verdict.passed}
```

### Phase 2: Integration (Future)

VOE components will be integrated into OpenEvolve core:

1. `openevolve/evaluator.py` will support blinded scorecards
2. `openevolve/database.py` will filter by gate constraints
3. `openevolve/controller.py` will generate provenance receipts

## Gate Specifications

### Example: FFT Benchmark

```json
{
  "$schema": "vdm://schemas/gate.v1.json",
  "name": "vdm-fft-bench",
  "version": "1.0.0",
  "hard_gates": [
    {"metric": "unit_pass_rate", "op": ">=", "value": 1.0},
    {"metric": "mutation_score", "op": ">=", "value": 0.85},
    {"metric": "wall_time_ms", "op": "<=", "value": 500}
  ],
  "soft_objectives": [
    {"metric": "avg_latency_ms", "goal": "min"}
  ]
}
```

### Loading Gate Specs

```python
import json
from vdm.sandboxes.voe.domain.models import Gate, GateOperator

def load_gate_spec(path):
    with open(path) as f:
        spec = json.load(f)
    
    gates = []
    for g in spec["hard_gates"]:
        gates.append(Gate(
            metric=g["metric"],
            op=GateOperator(g["op"]),
            value=g["value"],
        ))
    
    return gates
```

## Blinded Evaluation Principles

### What Scorecards Contain

✅ **Allowed** (aggregates):
- Pass rates
- Percentile metrics (p50, p95, p99)
- Resource usage (mean, max)
- Violation counts

❌ **Forbidden** (specifics):
- Individual test case inputs/outputs
- Failing test indices
- Ground truth labels
- Exact failure messages

### Example Scorecard

```json
{
  "candidate_id": "uuid-123",
  "hard_gates": {
    "pass": false,
    "violations": ["runtime"]
  },
  "metrics": {
    "pass_rate": 0.92,
    "runtime_p95_ms": 63.2,
    "error_q50": 1.2e-5,
    "error_q90": 4.1e-5
  },
  "properties": {
    "linearity": {"violations": 0, "passed": 100}
  },
  "hints": ["reduce_runtime"]
}
```

## Testing

### Running VOE Tests

```bash
# Domain model tests
python -m unittest discover -s vdm/sandboxes/voe/tests/domain -v

# Infrastructure tests
python -m unittest discover -s vdm/sandboxes/voe/tests/infrastructure -v

# All VOE tests
PYTHONPATH=. python -m unittest discover -s vdm/sandboxes/voe/tests -v
```

### Example Test

```python
from vdm.sandboxes.voe.domain.models import Gate, GateOperator

def test_gate_evaluation():
    gate = Gate(metric="pass_rate", op=GateOperator.GTE, value=0.9)
    assert gate.evaluate(0.95) == True
    assert gate.evaluate(0.85) == False
```

## Security Considerations

### Policy Configuration

VOE enforces security through `voe.policy.json`:

```json
{
  "hardware": {"accel": "ROCm", "gpus": "auto"},
  "sandbox": {
    "network": "deny",
    "seccomp": "strict"
  },
  "limits": {
    "cpu_seconds": 60,
    "rss_mb": 1024
  }
}
```

### Anti-Cheat Measures

1. **Read-only tests**: Tests/gold data mounted read-only
2. **Hash verification**: Test tree hashed pre/post
3. **Network deny**: No outbound connections
4. **Constant-time I/O**: Reduces timing side-channels

## Code Constraints (AMOS)

All VOE code follows these rules:

- **≤ 500 LOC per file**: Enforced via gates
- **Clean Architecture**: No outer→inner imports
- **Framework-free domain**: Pure Python dataclasses
- **≥ 90% coverage**: Unit test requirement
- **≥ 0.85 mutation score**: Quality gate

### Checking Compliance

```bash
# Line counts
find vdm/sandboxes/voe -name "*.py" -exec wc -l {} + | sort -n

# All files should be ≤ 500 LOC
```

## Next Steps

### For Developers

1. Review `vdm/sandboxes/voe/README.md`
2. Run `vdm/sandboxes/voe/example_usage.py`
3. Explore domain models in `domain/models/`
4. Check test examples in `tests/`

### For Integration

1. Phase B: Refactor OpenEvolve modules
2. Phase C: Add VDM physics gate packs
3. Phase D: Complete acceptance tests
4. Promotion: Move to `/common/helpers/voe_bridge/`

## References

- **VOE README**: `vdm/sandboxes/voe/README.md`
- **Gate Schema**: `vdm/sandboxes/voe/domain/specs/gate_schema_v1.json`
- **Example Usage**: `vdm/sandboxes/voe/example_usage.py`
- **OpenEvolve Docs**: Main README.md

## Support

For questions or issues:
- Check VOE README and examples
- Review test files for usage patterns
- Consult Clean Architecture principles
- Follow AMOS guidelines (≤500 LOC/file)

---

**Status**: Phase A Complete  
**Next Phase**: Phase B - OpenEvolve Integration & Hardening
