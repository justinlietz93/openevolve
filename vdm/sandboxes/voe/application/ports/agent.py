"""
Agent port - interface for LLM-based code mutation
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from vdm.sandboxes.voe.domain.models import Candidate


class AgentPort(ABC):
    """
    Abstract interface for LLM agent that mutates code
    """

    @abstractmethod
    async def mutate(
        self,
        candidate: Candidate,
        inspiration: List[Candidate],
        feedback: Optional[str] = None,
    ) -> Candidate:
        """
        Generate mutated candidate

        Args:
            candidate: Base candidate to mutate
            inspiration: Top-performing candidates for context
            feedback: Scorecard hints or artifact feedback

        Returns:
            New mutated candidate
        """
        pass

    @abstractmethod
    async def generate_from_spec(
        self, specification: str, language: str = "python"
    ) -> Candidate:
        """
        Generate initial candidate from specification

        Args:
            specification: Problem description
            language: Target programming language

        Returns:
            Initial candidate
        """
        pass
