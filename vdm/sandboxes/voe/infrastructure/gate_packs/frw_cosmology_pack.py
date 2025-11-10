"""
FRW Cosmology Gate Pack

Validates Friedmann-Robertson-Walker cosmology metrics:
- FRW continuity equation residual
- Energy density evolution
- Scale factor dynamics

Small, decisive pack with already-passing RESULTS from VDM.
"""

from typing import Dict, List

from vdm.sandboxes.voe.domain.models import Gate, GateOperator


class FRWCosmologyGatePack:
    """
    FRW cosmology validation gates

    Based on passing VDM FRW continuity results
    """

    @staticmethod
    def create_gates() -> List[Gate]:
        """
        Create FRW cosmology validation gates

        Returns:
            List of FRW gates
        """
        return [
            # FRW continuity equation
            Gate(
                metric="frw_continuity_residual",
                op=GateOperator.LTE,
                value=1e-10,
                required=True,
            ),
            Gate(
                metric="frw_residual_rms",
                op=GateOperator.LTE,
                value=1e-8,
                required=True,
            ),
            # Energy density conservation
            Gate(
                metric="energy_density_drift",
                op=GateOperator.LTE,
                value=1e-10,
                required=True,
            ),
            # Scale factor evolution
            Gate(
                metric="scale_factor_monotonicity_violations",
                op=GateOperator.EQ,
                value=0.0,
                required=True,
            ),
            Gate(
                metric="hubble_parameter_consistency",
                op=GateOperator.GTE,
                value=0.99,
                required=True,
            ),
            # ΛCDM residual
            Gate(
                metric="lcdm_w_plus_one_residual",
                op=GateOperator.LTE,
                value=0.02,
                required=False,  # Advisory
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
            "name": "frw_cosmology",
            "version": "1.0.0",
            "description": "Friedmann-Robertson-Walker cosmology validation",
            "domain": "cosmology",
            "references": [
                "VDM VALIDATION_METRICS.md#kpi-lcdm-residual",
                "CANON_PROGRESS.md#cosmology",
            ],
            "metrics": [
                "frw_continuity_residual",
                "frw_residual_rms",
                "energy_density_drift",
                "scale_factor_monotonicity_violations",
                "hubble_parameter_consistency",
                "lcdm_w_plus_one_residual",
            ],
        }
