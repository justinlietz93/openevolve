"""
Unit tests for Gate domain model
"""

import unittest

from vdm.sandboxes.voe.domain.models.gate import Gate, GateOperator, GateResult, GateVerdict


class TestGate(unittest.TestCase):
    """Test Gate model"""

    def test_gate_creation(self):
        """Test creating a gate"""
        gate = Gate(metric="pass_rate", op=GateOperator.GTE, value=0.9)
        self.assertEqual(gate.metric, "pass_rate")
        self.assertEqual(gate.op, GateOperator.GTE)
        self.assertEqual(gate.value, 0.9)
        self.assertTrue(gate.required)

    def test_gate_evaluate_gte_pass(self):
        """Test GTE operator passes when value >= threshold"""
        gate = Gate(metric="pass_rate", op=GateOperator.GTE, value=0.9)
        self.assertTrue(gate.evaluate(0.95))
        self.assertTrue(gate.evaluate(0.9))

    def test_gate_evaluate_gte_fail(self):
        """Test GTE operator fails when value < threshold"""
        gate = Gate(metric="pass_rate", op=GateOperator.GTE, value=0.9)
        self.assertFalse(gate.evaluate(0.85))

    def test_gate_evaluate_lte(self):
        """Test LTE operator"""
        gate = Gate(metric="runtime_ms", op=GateOperator.LTE, value=100.0)
        self.assertTrue(gate.evaluate(90.0))
        self.assertTrue(gate.evaluate(100.0))
        self.assertFalse(gate.evaluate(110.0))

    def test_gate_evaluate_eq(self):
        """Test equality operator with tolerance"""
        gate = Gate(metric="exact_value", op=GateOperator.EQ, value=1.0)
        self.assertTrue(gate.evaluate(1.0))
        self.assertTrue(gate.evaluate(1.0 + 1e-10))  # Within tolerance
        self.assertFalse(gate.evaluate(1.1))

    def test_gate_result_creation(self):
        """Test GateResult creation"""
        gate = Gate(metric="pass_rate", op=GateOperator.GTE, value=0.9)
        result = GateResult(gate=gate, passed=True, actual_value=0.95)
        self.assertTrue(result.passed)
        self.assertEqual(result.actual_value, 0.95)
        self.assertIsNone(result.message)

    def test_gate_verdict_all_pass(self):
        """Test verdict when all gates pass"""
        gate1 = Gate(metric="pass_rate", op=GateOperator.GTE, value=0.9)
        gate2 = Gate(metric="runtime_ms", op=GateOperator.LTE, value=100.0)

        result1 = GateResult(gate=gate1, passed=True, actual_value=0.95)
        result2 = GateResult(gate=gate2, passed=True, actual_value=90.0)

        verdict = GateVerdict(passed=True, gate_results=[result1, result2], violations=[])
        self.assertTrue(verdict.passed)
        self.assertEqual(len(verdict.violations), 0)

    def test_gate_verdict_with_failures(self):
        """Test verdict when some gates fail"""
        gate1 = Gate(metric="pass_rate", op=GateOperator.GTE, value=0.9)
        gate2 = Gate(metric="runtime_ms", op=GateOperator.LTE, value=100.0)

        result1 = GateResult(gate=gate1, passed=False, actual_value=0.85)
        result2 = GateResult(gate=gate2, passed=True, actual_value=90.0)

        verdict = GateVerdict(
            passed=False, gate_results=[result1, result2], violations=["pass_rate"]
        )
        self.assertFalse(verdict.passed)
        self.assertIn("pass_rate", verdict.violations)

    def test_gate_verdict_to_dict(self):
        """Test serializing verdict to dict"""
        gate = Gate(metric="pass_rate", op=GateOperator.GTE, value=0.9)
        result = GateResult(gate=gate, passed=True, actual_value=0.95)
        verdict = GateVerdict(passed=True, gate_results=[result])

        data = verdict.to_dict()
        self.assertTrue(data["passed"])
        self.assertEqual(len(data["gate_results"]), 1)
        self.assertEqual(data["gate_results"][0]["metric"], "pass_rate")


if __name__ == "__main__":
    unittest.main()
