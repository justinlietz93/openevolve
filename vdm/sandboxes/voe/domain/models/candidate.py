"""
Candidate domain model - represents evolved code under evaluation
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class CandidateStatus(str, Enum):
    """Status of a candidate in the evaluation pipeline"""

    SUBMITTED = "submitted"
    BUILDING = "building"
    TESTING = "testing"
    HOLDOUT = "holdout"
    REPLAY = "replay"
    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"


@dataclass
class Candidate:
    """
    Code candidate with metadata

    Attributes:
        id: Unique identifier (UUID)
        code: Source code string
        language: Programming language
        parent_id: Parent candidate ID if mutated
        generation: Generation number in evolution
        status: Current evaluation status
        artifact_uri: Path to artifact bundle
        metadata: Additional metadata
    """

    id: str
    code: str
    language: str = "python"
    parent_id: Optional[str] = None
    generation: int = 0
    status: CandidateStatus = CandidateStatus.SUBMITTED
    artifact_uri: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "code": self.code,
            "language": self.language,
            "parent_id": self.parent_id,
            "generation": self.generation,
            "status": self.status.value,
            "artifact_uri": self.artifact_uri,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Candidate":
        """Create from dictionary"""
        data_copy = data.copy()
        if "status" in data_copy and isinstance(data_copy["status"], str):
            data_copy["status"] = CandidateStatus(data_copy["status"])
        return cls(**data_copy)
