"""
Causality Gate Pack (Telegraph-Fisher + DAG)

Validates causality constraints including:
- Telegraph-Fisher dispersion and cone slope
- DAG temporal ordering
- Interval metrics
- Locality bounds

Based on VDM causality proposals and CANON_PROGRESS.md.
"""

from typing import Dict, List

from vdm.sandboxes.voe.domain.models import Gate, GateOperator


class CausalityGatePack:
    """
    Causality validation gates

    Enforces Telegraph-Fisher dynamics and DAG causal structure
    """

    @staticmethod
    def create_gates(c_max: float = 1.0) -> List[Gate]:
        """
        Create causality validation gates

        Args:
            c_max: Maximum propagation speed (default 1.0)

        Returns:
            List of causality gates
        """
        # Causal cone threshold with tolerance
        cone_threshold = c_max * 1.02

        return [
            # Telegraph-Fisher dispersion
            Gate(
                metric="tf_dispersion_r2",
                op=GateOperator.GTE,
                value=0.999,
                required=True,
            ),
            Gate(
                metric="tf_cone_slope",
                op=GateOperator.LTE,
                value=cone_threshold,
                required=True,
            ),
            Gate(
                metric="tf_cone_fit_r2",
                op=GateOperator.GTE,
                value=0.999,
                required=True,
            ),
            # DAG temporal ordering
            Gate(
                metric="dag_cycle_count",
                op=GateOperator.EQ,
                value=0.0,
                required=True,
            ),
            Gate(
                metric="dag_ordering_violations",
                op=GateOperator.EQ,
                value=0.0,
                required=True,
            ),
            # Interval metrics
            Gate(
                metric="timelike_interval_violations",
                op=GateOperator.EQ,
                value=0.0,
                required=True,
            ),
            Gate(
                metric="spacelike_interval_violations",
                op=GateOperator.EQ,
                value=0.0,
                required=True,
            ),
            # Locality bounds
            Gate(
                metric="superluminal_propagation_detected",
                op=GateOperator.EQ,
                value=0.0,
                required=True,
            ),
            Gate(
                metric="locality_violation_count",
                op=GateOperator.EQ,
                value=0.0,
                required=True,
            ),
        ]

    @staticmethod
    def get_spec() -> Dict:
        """
        Get gate pack specification

        Returns:
            Dictionary describing the pack
        """
        return {
            "name": "causality",
            "version": "1.0.0",
            "description": "Telegraph-Fisher causality + DAG temporal ordering",
            "domain": "causality",
            "references": [
                "VDM Causality/PROPOSAL_Metriplectic_Causal_Dominance_v1.md",
                "CANON_PROGRESS.md#causality",
                "VALIDATION_METRICS.md#causality",
            ],
            "metrics": [
                "tf_dispersion_r2",
                "tf_cone_slope",
                "tf_cone_fit_r2",
                "dag_cycle_count",
                "dag_ordering_violations",
                "timelike_interval_violations",
                "spacelike_interval_violations",
                "superluminal_propagation_detected",
                "locality_violation_count",
            ],
        }
