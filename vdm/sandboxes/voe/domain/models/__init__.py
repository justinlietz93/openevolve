"""
Domain models for VDM-Optimized Openevolve (VOE)

Clean Architecture - Domain Layer
Framework-agnostic core business logic and data structures
"""

from .candidate import Candidate, CandidateStatus
from .gate import Gate, GateOperator, GateResult, GateVerdict, SoftObjective
from .provenance import Provenance
from .scorecard import Scorecard
from .verdict import Verdict

__all__ = [
    "Candidate",
    "CandidateStatus",
    "Gate",
    "GateOperator",
    "GateResult",
    "GateVerdict",
    "Provenance",
    "Scorecard",
    "SoftObjective",
    "Verdict",
]
