"""
Evaluation system for OpenEvolve
"""

import asyncio
import importlib.util
import json
import logging
import os
import subprocess
import sys
import tempfile
import time
import traceback
import uuid
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
import traceback

from openevolve.config import EvaluatorConfig
from openevolve.evaluation_result import EvaluationResult
from openevolve.llm.ensemble import LLMEnsemble
from openevolve.utils.async_utils import TaskPool, run_in_executor
from openevolve.prompt.sampler import PromptSampler
from openevolve.utils.format_utils import format_metrics_safe

logger = logging.getLogger(__name__)


class Evaluator:
    """
    Evaluates programs and assigns scores

    The evaluator is responsible for executing programs, measuring their performance,
    and assigning scores based on the evaluation criteria.
    """

    def __init__(
        self,
        config: EvaluatorConfig,
        evaluation_file: str,
        llm_ensemble: Optional[LLMEnsemble] = None,
        prompt_sampler: Optional[PromptSampler] = None,
    ):
        self.config = config
        self.evaluation_file = evaluation_file
        self.llm_ensemble = llm_ensemble
        self.prompt_sampler = prompt_sampler

        # Create a task pool for parallel evaluation
        self.task_pool = TaskPool(max_concurrency=config.parallel_evaluations)

        # Set up evaluation function if file exists
        self._load_evaluation_function()

        # Pending artifacts storage for programs
        self._pending_artifacts: Dict[str, Dict[str, Union[str, bytes]]] = {}

        logger.info(f"Initialized evaluator with {evaluation_file}")

    def _load_evaluation_function(self) -> None:
        """Load the evaluation function from the evaluation file"""
        if not os.path.exists(self.evaluation_file):
            raise ValueError(f"Evaluation file {self.evaluation_file} not found")

        try:
            spec = importlib.util.spec_from_file_location("evaluation_module", self.evaluation_file)
            if spec is None or spec.loader is None:
                raise ImportError(f"Failed to load spec from {self.evaluation_file}")

            module = importlib.util.module_from_spec(spec)
            sys.modules["evaluation_module"] = module
            spec.loader.exec_module(module)

            if not hasattr(module, "evaluate"):
                raise AttributeError(
                    f"Evaluation file {self.evaluation_file} does not contain an 'evaluate' function"
                )

            self.evaluate_function = module.evaluate
            logger.info(f"Successfully loaded evaluation function from {self.evaluation_file}")
        except Exception as e:
            logger.error(f"Error loading evaluation function: {str(e)}")
            raise

    async def evaluate_program(
        self,
        program_code: str,
        program_id: str = "",
    ) -> Dict[str, float]:
        """
        Evaluate a program and return scores

        Args:
            program_code: Code to evaluate
            program_id: Optional ID for logging

        Returns:
            Dictionary of metric name to score
        """
        start_time = time.time()
        program_id_str = f" {program_id}" if program_id else ""

        # Check if artifacts are enabled
        artifacts_enabled = os.environ.get("ENABLE_ARTIFACTS", "true").lower() == "true"

        # Retry logic for evaluation
        last_exception = None
        for attempt in range(self.config.max_retries + 1):
            # Create a temporary file for the program
            with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp_file:
                temp_file.write(program_code.encode("utf-8"))
                temp_file_path = temp_file.name

            try:
                # Run evaluation
                if self.config.cascade_evaluation:
                    # Run cascade evaluation
                    result = await self._cascade_evaluate(temp_file_path)
                else:
                    # Run direct evaluation
                    result = await self._direct_evaluate(temp_file_path)

                # Process the result based on type
                eval_result = self._process_evaluation_result(result)

                # Add LLM feedback if configured
                if self.config.use_llm_feedback and self.llm_ensemble:
                    feedback_metrics = await self._llm_evaluate(program_code)

                    # Combine metrics
                    for name, value in feedback_metrics.items():
                        eval_result.metrics[f"llm_{name}"] = value * self.config.llm_feedback_weight

                # Store artifacts if enabled and present
                if artifacts_enabled and eval_result.has_artifacts() and program_id:
                    self._pending_artifacts[program_id] = eval_result.artifacts

                elapsed = time.time() - start_time
                logger.info(
                    f"Evaluated program{program_id_str} in {elapsed:.2f}s: "
                    f"{format_metrics_safe(eval_result.metrics)}"
                )

                # Return just metrics for backward compatibility
                return eval_result.metrics

            except Exception as e:
                last_exception = e
                logger.warning(
                    f"Evaluation attempt {attempt + 1}/{self.config.max_retries + 1} failed for program{program_id_str}: {str(e)}"
                )

                # Capture failure artifacts if enabled
                if artifacts_enabled and program_id:
                    self._pending_artifacts[program_id] = {
                        "stderr": str(e),
                        "traceback": traceback.format_exc(),
                        "failure_stage": "evaluation",
                    }

                # If this is not the last attempt, wait a bit before retrying
                if attempt < self.config.max_retries:
                    await asyncio.sleep(1.0)  # Wait 1 second before retry

            finally:
                # Clean up temporary file
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)

        # All retries failed
        logger.error(
            f"All evaluation attempts failed for program{program_id_str}. Last error: {str(last_exception)}"
        )
        return {"error": 0.0}

    def _process_evaluation_result(self, result: Any) -> EvaluationResult:
        """
        Process evaluation result to handle both dict and EvaluationResult returns

        Args:
            result: Raw result from evaluation function

        Returns:
            EvaluationResult instance
        """
        if isinstance(result, dict):
            # Backward compatibility - wrap dict in EvaluationResult
            return EvaluationResult.from_dict(result)
        elif isinstance(result, EvaluationResult):
            # New format - use directly
            return result
        else:
            # Error case - return error metrics
            logger.warning(f"Unexpected evaluation result type: {type(result)}")
            return EvaluationResult(metrics={"error": 0.0})

    def get_pending_artifacts(self, program_id: str) -> Optional[Dict[str, Union[str, bytes]]]:
        """
        Get and clear pending artifacts for a program

        Args:
            program_id: Program ID

        Returns:
            Artifacts dictionary or None if not found
        """
        return self._pending_artifacts.pop(program_id, None)

    @run_in_executor
    def _direct_evaluate(self, program_path: str) -> Dict[str, float]:
        """
        Directly evaluate a program using the evaluation function

        Args:
            program_path: Path to the program file

        Returns:
            Dictionary of metric name to score
        """
        try:
            # Run the evaluation with timeout
            result = self.evaluate_function(program_path)

            # Validate result
            if not isinstance(result, dict):
                logger.warning(f"Evaluation returned non-dictionary result: {result}")
                return {"error": 0.0}

            return result

        except Exception as e:
            logger.error(f"Error in direct evaluation: {str(e)}")
            return {"error": 0.0}

    async def _cascade_evaluate(
        self, program_path: str
    ) -> Union[Dict[str, float], EvaluationResult]:
        """
        Run cascade evaluation with increasingly challenging test cases

        Args:
            program_path: Path to the program file

        Returns:
            Dictionary of metrics or EvaluationResult with metrics and artifacts
        """
        # Import the evaluation module to get cascade functions if they exist
        try:
            spec = importlib.util.spec_from_file_location("evaluation_module", self.evaluation_file)
            if spec is None or spec.loader is None:
                return await self._direct_evaluate(program_path)

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Check if cascade functions exist
            if not hasattr(module, "evaluate_stage1"):
                return await self._direct_evaluate(program_path)

            # Run first stage
            try:
                stage1_result = await run_in_executor(module.evaluate_stage1)(program_path)
                stage1_eval_result = self._process_evaluation_result(stage1_result)
            except Exception as e:
                logger.error(f"Error in stage 1 evaluation: {str(e)}")
                # Capture stage 1 failure as artifacts
                return EvaluationResult(
                    metrics={"stage1_passed": 0.0, "error": 0.0},
                    artifacts={
                        "stderr": str(e),
                        "traceback": traceback.format_exc(),
                        "failure_stage": "stage1",
                    },
                )

            # Check threshold
            if not self._passes_threshold(
                stage1_eval_result.metrics, self.config.cascade_thresholds[0]
            ):
                return stage1_eval_result

            # Check if second stage exists
            if not hasattr(module, "evaluate_stage2"):
                return stage1_eval_result

            # Run second stage
            try:
                stage2_result = await run_in_executor(module.evaluate_stage2)(program_path)
                stage2_eval_result = self._process_evaluation_result(stage2_result)
            except Exception as e:
                logger.error(f"Error in stage 2 evaluation: {str(e)}")
                # Capture stage 2 failure, but keep stage 1 results
                stage1_eval_result.artifacts.update(
                    {
                        "stage2_stderr": str(e),
                        "stage2_traceback": traceback.format_exc(),
                        "failure_stage": "stage2",
                    }
                )
                stage1_eval_result.metrics["stage2_passed"] = 0.0
                return stage1_eval_result

            # Merge results from stage 1 and 2
            merged_metrics = {}
            # Convert all values to float to avoid type errors
            for name, value in stage1_eval_result.metrics.items():
                if isinstance(value, (int, float)) and name != "error":
                    merged_metrics[name] = float(value)

            for name, value in stage2_eval_result.metrics.items():
                if isinstance(value, (int, float)) and name != "error":
                    merged_metrics[name] = float(value)

            # Merge artifacts
            merged_artifacts = {}
            merged_artifacts.update(stage1_eval_result.artifacts)
            merged_artifacts.update(stage2_eval_result.artifacts)

            merged_result = EvaluationResult(metrics=merged_metrics, artifacts=merged_artifacts)

            # Check threshold for stage 3
            if len(self.config.cascade_thresholds) < 2 or not self._passes_threshold(
                merged_result.metrics, self.config.cascade_thresholds[1]
            ):
                return merged_result

            # Check if third stage exists
            if not hasattr(module, "evaluate_stage3"):
                return merged_result

            # Run third stage
            try:
                stage3_result = await run_in_executor(module.evaluate_stage3)(program_path)
                stage3_eval_result = self._process_evaluation_result(stage3_result)
            except Exception as e:
                logger.error(f"Error in stage 3 evaluation: {str(e)}")
                # Capture stage 3 failure, but keep previous results
                merged_result.artifacts.update(
                    {
                        "stage3_stderr": str(e),
                        "stage3_traceback": traceback.format_exc(),
                        "failure_stage": "stage3",
                    }
                )
                merged_result.metrics["stage3_passed"] = 0.0
                return merged_result

            # Merge stage 3 results
            for name, value in stage3_eval_result.metrics.items():
                if isinstance(value, (int, float)) and name != "error":
                    merged_result.metrics[name] = float(value)

            merged_result.artifacts.update(stage3_eval_result.artifacts)

            return merged_result

        except Exception as e:
            logger.error(f"Error in cascade evaluation: {str(e)}")
            return EvaluationResult(
                metrics={"error": 0.0},
                artifacts={
                    "stderr": str(e),
                    "traceback": traceback.format_exc(),
                    "failure_stage": "cascade_setup",
                },
            )

    async def _llm_evaluate(self, program_code: str) -> Dict[str, float]:
        """
        Use LLM to evaluate code quality

        Args:
            program_code: Code to evaluate

        Returns:
            Dictionary of metric name to score
        """
        if not self.llm_ensemble:
            return {}

        try:
            # Create prompt for LLM
            prompt = self.prompt_sampler.build_prompt(
                current_program=program_code, template_key="evaluation"
            )

            # Get LLM response
            responses = await self.llm_ensemble.generate_all_with_context(
                prompt["system"], [{"role": "user", "content": prompt["user"]}]
            )

            # Extract JSON from response
            try:
                # Try to find JSON block
                json_pattern = r"```json\n(.*?)\n```"
                import re

                avg_metrics = {}
                for i, response in enumerate(responses):
                    json_match = re.search(json_pattern, response, re.DOTALL)

                    if json_match:
                        json_str = json_match.group(1)
                    else:
                        # Try to extract JSON directly
                        json_str = response
                        # Remove non-JSON parts
                        start_idx = json_str.find("{")
                        end_idx = json_str.rfind("}") + 1
                        if start_idx >= 0 and end_idx > start_idx:
                            json_str = json_str[start_idx:end_idx]

                    # Parse JSON
                    result = json.loads(json_str)

                    # Filter all non-numeric values
                    metrics = {
                        name: float(value)
                        for name, value in result.items()
                        if isinstance(value, (int, float))
                    }

                    # Weight of the model in the ensemble
                    weight = self.llm_ensemble.weights[i] if self.llm_ensemble.weights else 1.0

                    # Average the metrics
                    for name, value in metrics.items():
                        if name in avg_metrics:
                            avg_metrics[name] += value * weight
                        else:
                            avg_metrics[name] = value * weight

                return avg_metrics

            except Exception as e:
                logger.warning(f"Error parsing LLM response: {str(e)}")
                return {}

        except Exception as e:
            logger.error(f"Error in LLM evaluation: {str(e)}")
            traceback.print_exc()
            return {}

    def _passes_threshold(self, metrics: Dict[str, float], threshold: float) -> bool:
        """
        Check if metrics pass a threshold

        Args:
            metrics: Dictionary of metric name to score
            threshold: Threshold to pass

        Returns:
            True if metrics pass threshold
        """
        if not metrics:
            return False

        # Calculate average score, skipping non-numeric values and 'error' key
        valid_metrics = []
        for name, value in metrics.items():
            # Skip 'error' keys and ensure values are numeric
            if name != "error" and isinstance(value, (int, float)):
                try:
                    valid_metrics.append(float(value))
                except (TypeError, ValueError):
                    logger.warning(f"Skipping non-numeric metric: {name}={value}")
                    continue

        if not valid_metrics:
            return False

        avg_score = sum(valid_metrics) / len(valid_metrics)
        return avg_score >= threshold

    async def evaluate_multiple(
        self,
        programs: List[Tuple[str, str]],
    ) -> List[Dict[str, float]]:
        """
        Evaluate multiple programs in parallel

        Args:
            programs: List of (program_code, program_id) tuples

        Returns:
            List of metric dictionaries
        """
        tasks = [
            self.task_pool.create_task(self.evaluate_program, program_code, program_id)
            for program_code, program_id in programs
        ]

        return await asyncio.gather(*tasks)
