"""
Axiom Gate Pack (A0-A7)

Global cross-run gates implementing VDM program axioms.
Ensures "accidental physics" prevention through foundational constraints.

Based on VDM AXIOMS.md specifications.
"""

from typing import Dict, List

from vdm.sandboxes.voe.domain.models import Gate, GateOperator


class AxiomGatePack:
    """
    Axiom validation gates (A0-A7)

    Enforces foundational VDM program axioms across all physics domains
    """

    @staticmethod
    def create_gates(grid_size: int = 1, tolerance_scale: float = 1.0) -> List[Gate]:
        """
        Create axiom validation gates

        Args:
            grid_size: Grid dimension N for scaling (default 1)
            tolerance_scale: Global tolerance scaling factor (default 1.0)

        Returns:
            List of axiom gates
        """
        # Scale tolerances
        noether_tol = 1e-12 * tolerance_scale
        h_theorem_tol = 1e-10 * tolerance_scale
        degeneracy_tol = 1e-10 * grid_size * tolerance_scale

        return [
            # A0: Closure (system self-consistency)
            Gate(
                metric="closure_residual",
                op=GateOperator.LTE,
                value=1e-10,
                required=True,
            ),
            # A2: Metriplectic degeneracies (J/M split)
            Gate(
                metric="j_degeneracy_global",
                op=GateOperator.LTE,
                value=degeneracy_tol,
                required=True,
            ),
            Gate(
                metric="m_degeneracy_global",
                op=GateOperator.LTE,
                value=degeneracy_tol,
                required=True,
            ),
            # A3: Locality/Causality audit
            Gate(
                metric="causality_cone_violation",
                op=GateOperator.EQ,
                value=0.0,
                required=True,
            ),
            Gate(
                metric="noether_energy_global_drift",
                op=GateOperator.LTE,
                value=noether_tol,
                required=True,
            ),
            Gate(
                metric="noether_momentum_global_drift",
                op=GateOperator.LTE,
                value=noether_tol,
                required=True,
            ),
            # A4/A5: H-theorem (entropy monotonicity)
            Gate(
                metric="h_theorem_violation",
                op=GateOperator.LTE,
                value=h_theorem_tol,
                required=True,
            ),
            Gate(
                metric="entropy_decrease_count",
                op=GateOperator.EQ,
                value=0.0,
                required=True,
            ),
            # A6: Scaling collapse check
            Gate(
                metric="scaling_collapse_detected",
                op=GateOperator.EQ,
                value=0.0,
                required=True,
            ),
            # A7: Measurability protocol
            Gate(
                metric="observables_well_defined",
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
            "name": "axiom",
            "version": "1.0.0",
            "description": "VDM program axioms (A0-A7) - global cross-run gates",
            "domain": "foundational",
            "references": [
                "VDM AXIOMS.md#A0-A7",
                "VALIDATION_METRICS.md#axiom-compliance",
            ],
            "metrics": [
                "closure_residual",
                "j_degeneracy_global",
                "m_degeneracy_global",
                "causality_cone_violation",
                "noether_energy_global_drift",
                "noether_momentum_global_drift",
                "h_theorem_violation",
                "entropy_decrease_count",
                "scaling_collapse_detected",
                "observables_well_defined",
            ],
        }
