"""
Program store port - interface for candidate persistence
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from vdm.sandboxes.voe.domain.models import Candidate, Verdict


class ProgramStorePort(ABC):
    """
    Abstract interface for storing and retrieving candidates
    """

    @abstractmethod
    async def store(self, candidate: Candidate) -> None:
        """
        Store a candidate

        Args:
            candidate: Candidate to store
        """
        pass

    @abstractmethod
    async def get(self, candidate_id: str) -> Optional[Candidate]:
        """
        Retrieve a candidate by ID

        Args:
            candidate_id: UUID of candidate

        Returns:
            Candidate if found, None otherwise
        """
        pass

    @abstractmethod
    async def archive_verdict(self, verdict: Verdict) -> None:
        """
        Archive evaluation verdict

        Args:
            verdict: Complete verdict to archive
        """
        pass

    @abstractmethod
    async def get_top_candidates(self, n: int, gate_passed: bool = True) -> List[Candidate]:
        """
        Retrieve top N candidates

        Args:
            n: Number of candidates to retrieve
            gate_passed: Filter for gate-passing candidates only

        Returns:
            List of top candidates
        """
        pass

    @abstractmethod
    async def dedup_by_ast(self, candidate: Candidate) -> bool:
        """
        Check if candidate is duplicate by AST hash

        Args:
            candidate: Candidate to check

        Returns:
            True if duplicate, False if unique
        """
        pass
