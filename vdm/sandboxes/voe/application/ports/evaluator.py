"""
Evaluator port - interface for code evaluation
"""

from abc import ABC, abstractmethod
from typing import Any, Dict

from vdm.sandboxes.voe.domain.models import Candidate, Scorecard, Verdict


class EvaluatorPort(ABC):
    """
    Abstract interface for evaluating candidates

    Implementations must provide blinded evaluation that never exposes:
    - Test case inputs/outputs
    - Ground truth labels
    - Specific failure indices
    """

    @abstractmethod
    async def evaluate(self, candidate: Candidate, gate_spec: Dict[str, Any]) -> Scorecard:
        """
        Evaluate candidate and return blinded scorecard

        Args:
            candidate: Code candidate to evaluate
            gate_spec: Gate specification dictionary

        Returns:
            Scorecard with aggregate metrics only
        """
        pass

    @abstractmethod
    async def evaluate_holdouts(self, candidate: Candidate, gate_spec: Dict[str, Any]) -> Scorecard:
        """
        Evaluate candidate on hidden holdout set

        Args:
            candidate: Code candidate to evaluate
            gate_spec: Gate specification with holdout config

        Returns:
            Scorecard for holdout evaluation
        """
        pass

    @abstractmethod
    async def cold_replay(self, candidate: Candidate, gate_spec: Dict[str, Any]) -> Verdict:
        """
        Reproduce evaluation in fresh container

        Args:
            candidate: Code candidate to replay
            gate_spec: Gate specification

        Returns:
            Complete verdict with reproducibility confirmation
        """
        pass
