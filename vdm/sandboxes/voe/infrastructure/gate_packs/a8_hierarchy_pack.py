"""
A8 Hierarchy Gate Pack

Validates hierarchical partition structure:
- Logarithmic depth scaling: N(L) = Θ(log(L/λ))
- Area-law slope
- Scale-gap separation
- Detector sensitivity sweeps

Based on VDM T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md
"""

from typing import Dict, List

from vdm.sandboxes.voe.domain.models import Gate, GateOperator


class A8HierarchyGatePack:
    """
    A8 Axiom hierarchy validation gates

    Validates hierarchical partition structure and scaling laws
    """

    @staticmethod
    def create_gates() -> List[Gate]:
        """
        Create A8 hierarchy validation gates

        Returns:
            List of A8 gates
        """
        return [
            # Logarithmic depth scaling
            Gate(
                metric="depth_log_fit_slope",
                op=GateOperator.GTE,
                value=0.9,
                required=True,
            ),
            Gate(
                metric="depth_log_fit_slope",
                op=GateOperator.LTE,
                value=1.1,
                required=True,
            ),
            Gate(
                metric="depth_log_fit_r2",
                op=GateOperator.GTE,
                value=0.98,
                required=True,
            ),
            # Area law (2D case)
            Gate(
                metric="area_law_slope_2d",
                op=GateOperator.GTE,
                value=1.8,
                required=True,
            ),
            Gate(
                metric="area_law_slope_2d",
                op=GateOperator.LTE,
                value=2.2,
                required=True,
            ),
            # Area law (3D case)
            Gate(
                metric="area_law_slope_3d",
                op=GateOperator.GTE,
                value=2.8,
                required=True,
            ),
            Gate(
                metric="area_law_slope_3d",
                op=GateOperator.LTE,
                value=3.2,
                required=True,
            ),
            # Scale-gap separation
            Gate(
                metric="scale_gap_rho_min",
                op=GateOperator.GTE,
                value=1.5,
                required=True,
            ),
            Gate(
                metric="scale_gap_rho_max",
                op=GateOperator.LTE,
                value=10.0,
                required=True,
            ),
            # Boundary concentration fractions
            Gate(
                metric="boundary_energy_fraction",
                op=GateOperator.GT,
                value=0.0,
                required=True,
            ),
            Gate(
                metric="boundary_info_fraction",
                op=GateOperator.GT,
                value=0.0,
                required=True,
            ),
            # Detector sensitivity sweep
            Gate(
                metric="detector_resolution_sweep_pass",
                op=GateOperator.EQ,
                value=1.0,
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
            "name": "a8_hierarchy",
            "version": "1.0.0",
            "description": "A8 Axiom: Hierarchical partition structure validation",
            "domain": "hierarchy",
            "references": [
                "VDM T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md",
                "AXIOMS.md#A8",
                "VALIDATION_METRICS.md#hierarchy",
            ],
            "metrics": [
                "depth_log_fit_slope",
                "depth_log_fit_r2",
                "area_law_slope_2d",
                "area_law_slope_3d",
                "scale_gap_rho_min",
                "scale_gap_rho_max",
                "boundary_energy_fraction",
                "boundary_info_fraction",
                "detector_resolution_sweep_pass",
            ],
        }
