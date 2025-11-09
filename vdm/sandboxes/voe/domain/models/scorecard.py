"""
Scorecard domain model - blinded evaluation results

A scorecard contains only aggregate metrics, never exposing:
- Individual test case inputs/outputs
- Failing test indices or labels
- Ground truth data
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Scorecard:
    """
    Blinded scorecard with aggregate metrics only

    Attributes:
        candidate_id: UUID of evaluated candidate
        hard_gates: Summary of gate pass/fail
        metrics: Aggregate performance metrics
        properties: Property test results (counts only)
        hints: Advisory feedback for improvement (optional)
        error_budget: Remaining evaluation budget if applicable
    """

    candidate_id: str
    hard_gates: Dict[str, Any]
    metrics: Dict[str, float]
    properties: Dict[str, Dict[str, int]] = field(default_factory=dict)
    hints: List[str] = field(default_factory=list)
    error_budget: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "candidate_id": self.candidate_id,
            "hard_gates": self.hard_gates,
            "metrics": self.metrics,
            "properties": self.properties,
            "hints": self.hints,
            "error_budget": self.error_budget,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Scorecard":
        """Create from dictionary"""
        return cls(
            candidate_id=data["candidate_id"],
            hard_gates=data["hard_gates"],
            metrics=data["metrics"],
            properties=data.get("properties", {}),
            hints=data.get("hints", []),
            error_budget=data.get("error_budget"),
        )

    def passes_gates(self) -> bool:
        """Check if all hard gates passed"""
        return self.hard_gates.get("pass", False)

    def get_metric(self, name: str, default: float = 0.0) -> float:
        """Get a metric value safely"""
        return self.metrics.get(name, default)
