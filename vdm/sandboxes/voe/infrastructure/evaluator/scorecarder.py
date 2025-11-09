"""
Scorecarder - aggregates metrics and generates blinded scorecards
"""

import logging
from typing import Any, Dict, List, Optional

from vdm.sandboxes.voe.domain.models import Gate, GateResult, GateVerdict, Scorecard
from vdm.sandboxes.voe.infrastructure.evaluator import Verifier

logger = logging.getLogger(__name__)


class Scorecarder:
    """
    Converts raw metrics into blinded scorecards with gate evaluation
    """

    def __init__(self, verifier: Verifier):
        self.verifier = verifier

    def evaluate_gates(self, gates: List[Gate], metrics: Dict[str, float]) -> GateVerdict:
        """
        Evaluate all gates against metrics

        Args:
            gates: List of gate constraints
            metrics: Measured metrics

        Returns:
            Gate verdict with results
        """
        results = []
        violations = []

        for gate in gates:
            actual = metrics.get(gate.metric, 0.0)
            passed = gate.evaluate(actual)

            result = GateResult(
                gate=gate,
                passed=passed,
                actual_value=actual,
                message=None if passed else f"{gate.metric} failed constraint",
            )
            results.append(result)

            if not passed and gate.required:
                violations.append(gate.metric)

        all_passed = len(violations) == 0
        return GateVerdict(passed=all_passed, gate_results=results, violations=violations)

    def generate_hints(self, metrics: Dict[str, float], gate_verdict: GateVerdict) -> List[str]:
        """
        Generate advisory hints for improvement

        Args:
            metrics: Performance metrics
            gate_verdict: Gate evaluation results

        Returns:
            List of hint strings
        """
        hints = []

        # Check for specific issues
        if metrics.get("runtime_p95_ms", 0) > 100:
            hints.append("reduce_runtime")

        if metrics.get("error_q99", 0) > 1e-3:
            hints.append("reduce_high_k_error")

        if not gate_verdict.passed:
            hints.append("fix_gate_violations")

        return hints

    def create_scorecard(
        self,
        candidate_id: str,
        metrics: Dict[str, float],
        gate_verdict: GateVerdict,
        properties: Optional[Dict[str, Dict[str, int]]] = None,
    ) -> Scorecard:
        """
        Create blinded scorecard

        Args:
            candidate_id: Candidate UUID
            metrics: Aggregate metrics
            gate_verdict: Gate evaluation
            properties: Property test results

        Returns:
            Blinded scorecard
        """
        hints = self.generate_hints(metrics, gate_verdict)

        return Scorecard(
            candidate_id=candidate_id,
            hard_gates={"pass": gate_verdict.passed, "violations": gate_verdict.violations},
            metrics=metrics,
            properties=properties or {},
            hints=hints,
        )
