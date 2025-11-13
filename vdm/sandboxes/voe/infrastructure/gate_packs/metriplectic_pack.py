"""
Metriplectic Structure Gate Pack

Validates metriplectic operator structure (A2 Axiom) with:
- Degeneracy constraints: ⟨J·δΣ, δΣ⟩ ≤ 1e-10·N and ⟨M·δℐ, δℐ⟩ ≤ 1e-10·N
- J skew-symmetry: ||J + J^T|| ≤ 1e-12
- M positive semi-definite: λ_min(M) ≥ -1e-12
- Lyapunov non-increase: ΔL_h ≤ 0
- Noether conservation: |ΔE|, |ΔP| ≤ 1e-12
"""

from typing import Dict, List

from vdm.sandboxes.voe.domain.models import Gate, GateOperator


class MetriplecticGatePack:
    """
    Metriplectic structure validation gates

    Based on VDM A2 Axiom and VALIDATION_METRICS.md requirements
    """

    @staticmethod
    def create_gates(grid_size: int = 1) -> List[Gate]:
        """
        Create metriplectic validation gates

        Args:
            grid_size: Grid dimension N for degeneracy scaling (default 1)

        Returns:
            List of metriplectic gates
        """
        # Scale degeneracy thresholds by grid size
        degeneracy_threshold = 1e-10 * grid_size

        return [
            # Degeneracy constraints (A2)
            Gate(
                metric="g1_degeneracy",
                op=GateOperator.LTE,
                value=degeneracy_threshold,
                required=True,
            ),
            Gate(
                metric="g2_degeneracy",
                op=GateOperator.LTE,
                value=degeneracy_threshold,
                required=True,
            ),
            # Structure properties
            Gate(
                metric="j_skew_symmetry_norm",
                op=GateOperator.LTE,
                value=1e-12,
                required=True,
            ),
            Gate(
                metric="m_psd_min_eigenvalue",
                op=GateOperator.GTE,
                value=-1e-12,
                required=True,
            ),
            # Lyapunov non-increase
            Gate(
                metric="delta_L_h", op=GateOperator.LTE, value=0.0, required=True
            ),
            # Noether conservation (energy)
            Gate(
                metric="noether_energy_drift",
                op=GateOperator.LTE,
                value=1e-12,
                required=True,
            ),
            # Noether conservation (momentum)
            Gate(
                metric="noether_momentum_drift",
                op=GateOperator.LTE,
                value=1e-12,
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
            "name": "metriplectic",
            "version": "1.0.0",
            "description": "Metriplectic structure validation (A2 Axiom)",
            "domain": "metriplectic_dynamics",
            "references": [
                "VDM AXIOMS.md#A2",
                "VALIDATION_METRICS.md#metriplectic",
                "EQUATIONS.md#vdm-e-metriplectic",
            ],
            "metrics": [
                "g1_degeneracy",
                "g2_degeneracy",
                "j_skew_symmetry_norm",
                "m_psd_min_eigenvalue",
                "delta_L_h",
                "noether_energy_drift",
                "noether_momentum_drift",
            ],
        }
