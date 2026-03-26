"""
Provenance domain model - reproducibility metadata

Tracks all information needed to reproduce an evaluation:
- Source code versions
- Toolchain details
- Hardware environment
- Random seeds
- Timing data
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class Provenance:
    """
    Complete provenance record for reproducibility

    Attributes:
        candidate_id: UUID of the candidate
        timestamp: ISO 8601 timestamp
        git_tree: Git tree hash of source
        container_digest: Container image SHA256
        toolchain: Compiler/interpreter versions
        hardware: CPU/GPU model info
        rocm_version: ROCm driver version
        seeds: Random seeds used
        cpu_seconds: CPU time consumed
        wall_seconds: Wall clock time
        memory_mb_peak: Peak memory usage
        gate_spec_version: Version of gate specification
        environment: Additional env vars
    """

    candidate_id: str
    timestamp: str
    git_tree: Optional[str] = None
    container_digest: Optional[str] = None
    toolchain: Dict[str, str] = field(default_factory=dict)
    hardware: Dict[str, str] = field(default_factory=dict)
    rocm_version: Optional[str] = None
    seeds: Dict[str, int] = field(default_factory=dict)
    cpu_seconds: float = 0.0
    wall_seconds: float = 0.0
    memory_mb_peak: float = 0.0
    gate_spec_version: str = "1.0.0"
    environment: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def create(cls, candidate_id: str) -> "Provenance":
        """Create provenance record with current timestamp"""
        return cls(
            candidate_id=candidate_id,
            timestamp=datetime.utcnow().isoformat() + "Z",
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "candidate_id": self.candidate_id,
            "timestamp": self.timestamp,
            "git_tree": self.git_tree,
            "container_digest": self.container_digest,
            "toolchain": self.toolchain,
            "hardware": self.hardware,
            "rocm_version": self.rocm_version,
            "seeds": self.seeds,
            "cpu_seconds": self.cpu_seconds,
            "wall_seconds": self.wall_seconds,
            "memory_mb_peak": self.memory_mb_peak,
            "gate_spec_version": self.gate_spec_version,
            "environment": self.environment,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Provenance":
        """Create from dictionary"""
        return cls(**data)
