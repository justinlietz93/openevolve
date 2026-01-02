"""
Gate domain model - represents hard constraints and soft objectives

A gate defines pass/fail criteria for candidate code evaluation.
Hard gates must pass for a candidate to be eligible for selection.
Soft objectives guide Pareto ranking among passing candidates.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Literal, Optional


class GateOperator(str, Enum):
    """Comparison operators for gate conditions"""

    EQ = "=="
    NEQ = "!="
    LT = "<"
    LTE = "<="
    GT = ">"
    GTE = ">="


@dataclass(frozen=True)
class Gate:
    """
    Single gate constraint definition

    Attributes:
        metric: Name of the metric to evaluate (e.g., "unit_pass_rate")
        op: Comparison operator
        value: Threshold value for comparison
        required: If True, failure is fatal; if False, gate is advisory
    """

    metric: str
    op: GateOperator
    value: float
    required: bool = True

    def evaluate(self, actual_value: float) -> bool:
        """
        Evaluate gate against actual metric value

        Args:
            actual_value: The measured value to compare

        Returns:
            True if gate passes, False otherwise
        """
        if self.op == GateOperator.EQ:
            return abs(actual_value - self.value) < 1e-9
        elif self.op == GateOperator.NEQ:
            return abs(actual_value - self.value) >= 1e-9
        elif self.op == GateOperator.LT:
            return actual_value < self.value
        elif self.op == GateOperator.LTE:
            return actual_value <= self.value
        elif self.op == GateOperator.GT:
            return actual_value > self.value
        elif self.op == GateOperator.GTE:
            return actual_value >= self.value
        return False


@dataclass
class GateResult:
    """
    Result of evaluating a single gate

    Attributes:
        gate: The gate that was evaluated
        passed: Whether the gate evaluation passed
        actual_value: The measured value
        message: Optional explanation
    """

    gate: Gate
    passed: bool
    actual_value: float
    message: Optional[str] = None


@dataclass
class GateVerdict:
    """
    Aggregate result of all gate evaluations for a candidate

    Attributes:
        passed: True if all required gates passed
        gate_results: Individual results for each gate
        violations: List of failed gate names
    """

    passed: bool
    gate_results: List[GateResult] = field(default_factory=list)
    violations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "passed": self.passed,
            "violations": self.violations,
            "gate_results": [
                {
                    "metric": gr.gate.metric,
                    "op": gr.gate.op.value,
                    "threshold": gr.gate.value,
                    "actual": gr.actual_value,
                    "passed": gr.passed,
                    "message": gr.message,
                }
                for gr in self.gate_results
            ],
        }


@dataclass
class SoftObjective:
    """
    Soft optimization objective (not a hard constraint)

    Attributes:
        metric: Name of the metric
        goal: "min" or "max"
    """

    metric: str
    goal: Literal["min", "max"]
