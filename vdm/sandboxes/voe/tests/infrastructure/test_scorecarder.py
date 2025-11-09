"""
Unit tests for Scorecarder infrastructure component
"""

import unittest

from vdm.sandboxes.voe.domain.models import Gate, GateOperator
from vdm.sandboxes.voe.infrastructure.evaluator import Scorecarder, Verifier


class TestScorecarder(unittest.TestCase):
    """Test Scorecarder"""

    def setUp(self):
        """Set up test fixtures"""
        config = {"timeout": 60}
        self.verifier = Verifier(config)
        self.scorecarder = Scorecarder(self.verifier)

    def test_evaluate_gates_all_pass(self):
        """Test gate evaluation when all pass"""
        gates = [
            Gate(metric="pass_rate", op=GateOperator.GTE, value=0.9),
            Gate(metric="runtime_ms", op=GateOperator.LTE, value=100.0),
        ]

        metrics = {"pass_rate": 0.95, "runtime_ms": 90.0}

        verdict = self.scorecarder.evaluate_gates(gates, metrics)

        self.assertTrue(verdict.passed)
        self.assertEqual(len(verdict.violations), 0)
        self.assertEqual(len(verdict.gate_results), 2)
        self.assertTrue(all(r.passed for r in verdict.gate_results))

    def test_evaluate_gates_some_fail(self):
        """Test gate evaluation when some fail"""
        gates = [
            Gate(metric="pass_rate", op=GateOperator.GTE, value=0.9),
            Gate(metric="runtime_ms", op=GateOperator.LTE, value=100.0),
        ]

        metrics = {"pass_rate": 0.85, "runtime_ms": 90.0}

        verdict = self.scorecarder.evaluate_gates(gates, metrics)

        self.assertFalse(verdict.passed)
        self.assertIn("pass_rate", verdict.violations)
        self.assertEqual(len(verdict.violations), 1)

    def test_generate_hints_runtime(self):
        """Test hint generation for high runtime"""
        metrics = {"runtime_p95_ms": 150.0}
        verdict = self.scorecarder.evaluate_gates([], metrics)

        hints = self.scorecarder.generate_hints(metrics, verdict)

        self.assertIn("reduce_runtime", hints)

    def test_generate_hints_error(self):
        """Test hint generation for high error"""
        metrics = {"error_q99": 2e-3}
        verdict = self.scorecarder.evaluate_gates([], metrics)

        hints = self.scorecarder.generate_hints(metrics, verdict)

        self.assertIn("reduce_high_k_error", hints)

    def test_generate_hints_gate_violations(self):
        """Test hint generation for gate violations"""
        gates = [Gate(metric="pass_rate", op=GateOperator.GTE, value=0.9)]
        metrics = {"pass_rate": 0.8}

        verdict = self.scorecarder.evaluate_gates(gates, metrics)
        hints = self.scorecarder.generate_hints(metrics, verdict)

        self.assertIn("fix_gate_violations", hints)

    def test_create_scorecard_passing(self):
        """Test creating scorecard for passing candidate"""
        gates = [Gate(metric="pass_rate", op=GateOperator.GTE, value=0.9)]
        metrics = {"pass_rate": 0.95, "runtime_ms": 50.0}

        verdict = self.scorecarder.evaluate_gates(gates, metrics)
        scorecard = self.scorecarder.create_scorecard(
            candidate_id="test-1",
            metrics=metrics,
            gate_verdict=verdict,
        )

        self.assertEqual(scorecard.candidate_id, "test-1")
        self.assertTrue(scorecard.passes_gates())
        self.assertEqual(scorecard.metrics["pass_rate"], 0.95)

    def test_create_scorecard_with_properties(self):
        """Test creating scorecard with property results"""
        gates = [Gate(metric="pass_rate", op=GateOperator.GTE, value=0.9)]
        metrics = {"pass_rate": 0.95}
        properties = {"linearity": {"violations": 0, "passed": 10}}

        verdict = self.scorecarder.evaluate_gates(gates, metrics)
        scorecard = self.scorecarder.create_scorecard(
            candidate_id="test-1",
            metrics=metrics,
            gate_verdict=verdict,
            properties=properties,
        )

        self.assertIn("linearity", scorecard.properties)
        self.assertEqual(scorecard.properties["linearity"]["violations"], 0)

    def test_scorecard_blinded(self):
        """Test that scorecard contains no test case details"""
        gates = []
        metrics = {"pass_rate": 0.95}

        verdict = self.scorecarder.evaluate_gates(gates, metrics)
        scorecard = self.scorecarder.create_scorecard(
            candidate_id="test-1",
            metrics=metrics,
            gate_verdict=verdict,
        )

        # Scorecard should only have aggregates
        data = scorecard.to_dict()
        self.assertIn("metrics", data)
        self.assertNotIn("test_cases", data)
        self.assertNotIn("failures", data)
        self.assertNotIn("inputs", data)
        self.assertNotIn("outputs", data)


if __name__ == "__main__":
    unittest.main()
