"""
Example: Using VOE to evolve an FFT-like transform with property oracles

This demonstrates the VOE workflow:
1. Define gate specification
2. Create candidate
3. Evaluate with blinded scorecard
4. Check gates and make evolution decisions
"""

import asyncio
import uuid
from typing import Dict, Any

from vdm.sandboxes.voe.domain.models import (
    Candidate,
    Gate,
    GateOperator,
    Scorecard,
)
from vdm.sandboxes.voe.infrastructure.evaluator import Scorecarder, Verifier


async def example_fft_evolution():
    """Example of evolving FFT-like code with VOE"""

    # 1. Define gate specification (hard constraints)
    gates = [
        Gate(metric="unit_pass_rate", op=GateOperator.GTE, value=1.0),
        Gate(metric="wall_time_ms", op=GateOperator.LTE, value=500.0),
        Gate(metric="max_rss_mb", op=GateOperator.LTE, value=256.0),
        Gate(metric="mutation_score", op=GateOperator.GTE, value=0.85),
    ]

    # 2. Create a candidate (initial code)
    candidate = Candidate(
        id=str(uuid.uuid4()),
        code="""
import numpy as np

def fft_transform(data):
    '''FFT-like transform'''
    # EVOLVE-BLOCK-START
    n = len(data)
    result = np.fft.fft(data)
    # EVOLVE-BLOCK-END
    return result
""",
        language="python",
        generation=0,
    )

    print(f"Evaluating candidate: {candidate.id}")
    print(f"Generation: {candidate.generation}")

    # 3. Evaluate candidate (in real system, this would run in container)
    config: Dict[str, Any] = {"timeout": 60}
    verifier = Verifier(config)
    scorecarder = Scorecarder(verifier)

    # Collect metrics (mock data for example)
    metrics = {
        "unit_pass_rate": 1.0,
        "wall_time_ms": 450.0,
        "max_rss_mb": 200.0,
        "mutation_score": 0.87,
        "runtime_p95_ms": 55.0,
        "error_q50": 1.2e-5,
        "error_q90": 4.1e-5,
        "error_q99": 2.3e-4,
    }

    # Property test results (counts only, no test cases exposed)
    properties = {
        "linearity": {"violations": 0, "passed": 100},
        "parseval": {"violations": 1, "passed": 99},
    }

    # 4. Evaluate gates
    gate_verdict = scorecarder.evaluate_gates(gates, metrics)

    print(f"\nGate Evaluation:")
    print(f"  Overall Pass: {gate_verdict.passed}")
    print(f"  Violations: {gate_verdict.violations}")

    for result in gate_verdict.gate_results:
        status = "✓" if result.passed else "✗"
        print(
            f"  {status} {result.gate.metric}: "
            f"{result.actual_value} {result.gate.op.value} {result.gate.value}"
        )

    # 5. Create blinded scorecard
    scorecard = scorecarder.create_scorecard(
        candidate_id=candidate.id,
        metrics=metrics,
        gate_verdict=gate_verdict,
        properties=properties,
    )

    print(f"\nScorecard (Blinded):")
    print(f"  Candidate ID: {scorecard.candidate_id}")
    print(f"  Gates Passed: {scorecard.passes_gates()}")
    print(f"\nMetrics (aggregates only):")
    for name, value in scorecard.metrics.items():
        print(f"    {name}: {value}")

    print(f"\nProperty Tests (counts only):")
    for prop, results in scorecard.properties.items():
        print(f"    {prop}: {results['passed']} passed, {results['violations']} violations")

    if scorecard.hints:
        print(f"\nHints for improvement:")
        for hint in scorecard.hints:
            print(f"    - {hint}")

    # 6. Decision logic
    if scorecard.passes_gates():
        print(f"\n✓ Candidate ELIGIBLE for selection")
        print("  → Will run hidden holdouts")
        print("  → Will perform cold replay")
        print("  → May be promoted if holdouts pass")
    else:
        print(f"\n✗ Candidate REJECTED (gate failures)")
        print("  → Will not be added to population")
        print("  → Feedback sent to LLM for next mutation")

    return candidate, scorecard


if __name__ == "__main__":
    print("=" * 70)
    print("VOE Example: FFT Transform Evolution with Blinded Evaluation")
    print("=" * 70)
    print()

    # Run the example
    candidate, scorecard = asyncio.run(example_fft_evolution())

    print()
    print("=" * 70)
    print("Key VOE Principles Demonstrated:")
    print("  1. Hard gates as constraints (not scores)")
    print("  2. Blinded scorecard (no test case exposure)")
    print("  3. Property tests (violation counts only)")
    print("  4. Advisory hints (not prescriptive)")
    print("  5. Gate-first selection logic")
    print("=" * 70)
