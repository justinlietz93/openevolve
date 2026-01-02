"""
Verdict domain model - final evaluation decision

Combines gate results, scorecard, and provenance into a final verdict.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .gate import GateVerdict
from .provenance import Provenance
from .scorecard import Scorecard


@dataclass
class Verdict:
    """
    Final evaluation verdict for a candidate

    Attributes:
        candidate_id: UUID of candidate
        passed: Overall pass/fail
        gate_verdict: Gate evaluation results
        scorecard: Blinded metrics
        provenance: Reproducibility data
        holdout_passed: Whether hidden holdouts passed
        cold_replay_passed: Whether cold replay succeeded
        eligible_for_selection: Final eligibility flag
        notes: Additional context
    """

    candidate_id: str
    passed: bool
    gate_verdict: GateVerdict
    scorecard: Scorecard
    provenance: Provenance
    holdout_passed: bool = False
    cold_replay_passed: bool = False
    eligible_for_selection: bool = False
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "candidate_id": self.candidate_id,
            "passed": self.passed,
            "gate_verdict": self.gate_verdict.to_dict(),
            "scorecard": self.scorecard.to_dict(),
            "provenance": self.provenance.to_dict(),
            "holdout_passed": self.holdout_passed,
            "cold_replay_passed": self.cold_replay_passed,
            "eligible_for_selection": self.eligible_for_selection,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Verdict":
        """Create from dictionary"""
        # This is simplified - full implementation would reconstruct nested objects
        return cls(
            candidate_id=data["candidate_id"],
            passed=data["passed"],
            gate_verdict=data["gate_verdict"],  # Would need proper reconstruction
            scorecard=Scorecard.from_dict(data["scorecard"]),
            provenance=Provenance.from_dict(data["provenance"]),
            holdout_passed=data.get("holdout_passed", False),
            cold_replay_passed=data.get("cold_replay_passed", False),
            eligible_for_selection=data.get("eligible_for_selection", False),
            notes=data.get("notes", []),
        )
