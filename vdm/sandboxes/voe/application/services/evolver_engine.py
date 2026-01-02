"""
Evolver engine - orchestrates evolution loop

Main service that coordinates:
- Candidate selection
- Mutation via LLM agent
- Evaluation via evaluator
- Storage and archival
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

from vdm.sandboxes.voe.application.ports import (
    AgentPort,
    ArtifactRepoPort,
    EvaluatorPort,
    ProgramStorePort,
)
from vdm.sandboxes.voe.application.services import Selector
from vdm.sandboxes.voe.domain.models import Candidate, CandidateStatus, Verdict

logger = logging.getLogger(__name__)


class EvolverEngine:
    """
    Main evolution orchestrator

    Attributes:
        agent: LLM agent for mutation
        evaluator: Evaluator for scoring
        store: Program store
        artifact_repo: Artifact storage
        selector: Candidate selector
        config: Evolution configuration
    """

    def __init__(
        self,
        agent: AgentPort,
        evaluator: EvaluatorPort,
        store: ProgramStorePort,
        artifact_repo: ArtifactRepoPort,
        config: Dict[str, Any],
    ):
        self.agent = agent
        self.evaluator = evaluator
        self.store = store
        self.artifact_repo = artifact_repo
        self.selector = Selector(store, config.get("selector", {}))
        self.config = config

    async def run_iteration(self, gate_spec: Dict[str, Any], generation: int) -> Optional[Verdict]:
        """
        Run single evolution iteration

        Args:
            gate_spec: Gate specification
            generation: Current generation number

        Returns:
            Verdict if successful, None if failed
        """
        # Select inspiration candidates
        inspiration = await self.selector.select_for_mutation(
            n=self.config.get("num_inspiration", 3)
        )

        if not inspiration:
            logger.warning("No inspiration candidates available")
            return None

        # Mutate base candidate
        base = inspiration[0]
        mutated = await self.agent.mutate(base, inspiration)
        mutated.generation = generation

        # Evaluate
        scorecard = await self.evaluator.evaluate(mutated, gate_spec)

        # Check gates
        if not scorecard.passes_gates():
            logger.info(f"Candidate {mutated.id} failed gates")
            mutated.status = CandidateStatus.FAILED
            await self.store.store(mutated)
            return None

        # Run holdouts if gates passed
        holdout_scorecard = await self.evaluator.evaluate_holdouts(mutated, gate_spec)

        if not holdout_scorecard.passes_gates():
            logger.info(f"Candidate {mutated.id} failed holdouts")
            mutated.status = CandidateStatus.FAILED
            await self.store.store(mutated)
            return None

        # Cold replay for final verification
        verdict = await self.evaluator.cold_replay(mutated, gate_spec)

        if verdict.cold_replay_passed:
            mutated.status = CandidateStatus.PASSED
            verdict.eligible_for_selection = True
            await self.store.archive_verdict(verdict)
            logger.info(f"Candidate {mutated.id} passed all checks")
        else:
            mutated.status = CandidateStatus.ERROR
            logger.warning(f"Candidate {mutated.id} failed cold replay")

        await self.store.store(mutated)
        return verdict if verdict.cold_replay_passed else None
