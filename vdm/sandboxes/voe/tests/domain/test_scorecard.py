"""
Unit tests for Scorecard domain model
"""

import unittest

from vdm.sandboxes.voe.domain.models.scorecard import Scorecard


class TestScorecard(unittest.TestCase):
    """Test Scorecard model"""

    def test_scorecard_creation(self):
        """Test creating a scorecard"""
        scorecard = Scorecard(
            candidate_id="test-123",
            hard_gates={"pass": True, "violations": []},
            metrics={"pass_rate": 0.95, "runtime_ms": 50.0},
        )
        self.assertEqual(scorecard.candidate_id, "test-123")
        self.assertTrue(scorecard.hard_gates["pass"])
        self.assertEqual(scorecard.metrics["pass_rate"], 0.95)

    def test_scorecard_passes_gates(self):
        """Test checking if gates passed"""
        scorecard_pass = Scorecard(
            candidate_id="test-1",
            hard_gates={"pass": True},
            metrics={},
        )
        self.assertTrue(scorecard_pass.passes_gates())

        scorecard_fail = Scorecard(
            candidate_id="test-2",
            hard_gates={"pass": False, "violations": ["runtime"]},
            metrics={},
        )
        self.assertFalse(scorecard_fail.passes_gates())

    def test_scorecard_get_metric(self):
        """Test getting metric values"""
        scorecard = Scorecard(
            candidate_id="test-1",
            hard_gates={"pass": True},
            metrics={"pass_rate": 0.95},
        )
        self.assertEqual(scorecard.get_metric("pass_rate"), 0.95)
        self.assertEqual(scorecard.get_metric("missing", default=0.5), 0.5)

    def test_scorecard_with_properties(self):
        """Test scorecard with property test results"""
        scorecard = Scorecard(
            candidate_id="test-1",
            hard_gates={"pass": True},
            metrics={},
            properties={
                "linearity": {"violations": 0, "passed": 10},
                "parseval": {"violations": 1, "passed": 9},
            },
        )
        self.assertEqual(scorecard.properties["linearity"]["violations"], 0)
        self.assertEqual(scorecard.properties["parseval"]["violations"], 1)

    def test_scorecard_with_hints(self):
        """Test scorecard with improvement hints"""
        scorecard = Scorecard(
            candidate_id="test-1",
            hard_gates={"pass": False},
            metrics={},
            hints=["reduce_runtime", "improve_accuracy"],
        )
        self.assertEqual(len(scorecard.hints), 2)
        self.assertIn("reduce_runtime", scorecard.hints)

    def test_scorecard_to_dict(self):
        """Test serializing scorecard to dictionary"""
        scorecard = Scorecard(
            candidate_id="test-1",
            hard_gates={"pass": True},
            metrics={"pass_rate": 0.95},
            hints=["optimize_further"],
        )
        data = scorecard.to_dict()
        self.assertEqual(data["candidate_id"], "test-1")
        self.assertTrue(data["hard_gates"]["pass"])
        self.assertEqual(data["metrics"]["pass_rate"], 0.95)
        self.assertIn("optimize_further", data["hints"])

    def test_scorecard_from_dict(self):
        """Test creating scorecard from dictionary"""
        data = {
            "candidate_id": "test-1",
            "hard_gates": {"pass": True},
            "metrics": {"pass_rate": 0.95},
            "hints": ["hint1"],
        }
        scorecard = Scorecard.from_dict(data)
        self.assertEqual(scorecard.candidate_id, "test-1")
        self.assertEqual(scorecard.metrics["pass_rate"], 0.95)


if __name__ == "__main__":
    unittest.main()
