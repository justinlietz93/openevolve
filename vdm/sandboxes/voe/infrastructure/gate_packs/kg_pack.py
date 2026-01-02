"""
Klein-Gordon (KG) Gate Pack

Validates Klein-Gordon dynamics with:
- Dispersion relation: ω² = c²k² + m² (R² ≥ 0.999)
- Causal cone: v_front ≤ c(1+0.02)
- Energy oscillation scaling: slope p ∈ [1.95, 2.05], R² ≥ 0.999
- Time-reversal: ||Δ||_∞ ≤ 1e-12
- Fine-step amplitude: (A_H/H̄)_min ≤ 1e-4
"""

from typing import Dict, List

from vdm.sandboxes.voe.domain.models import Gate, GateOperator


class KleinGordonGatePack:
    """
    Klein-Gordon validation gates

    Based on VDM J-only (hyperbolic) diagnostics and KG instrument QC
    """

    @staticmethod
    def create_gates(c: float = 1.0) -> List[Gate]:
        """
        Create Klein-Gordon validation gates

        Args:
            c: Speed of light in code units (default 1.0)

        Returns:
            List of KG gates
        """
        # Causal cone threshold: v ≤ c(1+2%)
        cone_threshold = c * 1.02

        return [
            # Dispersion relation
            Gate(
                metric="kg_dispersion_r2",
                op=GateOperator.GTE,
                value=0.999,
                required=True,
            ),
            Gate(
                metric="kg_dispersion_slope_error",
                op=GateOperator.LTE,
                value=0.002,
                required=True,
            ),
            Gate(
                metric="kg_dispersion_intercept_error",
                op=GateOperator.LTE,
                value=0.01,
                required=True,
            ),
            # Causal cone
            Gate(
                metric="kg_front_speed",
                op=GateOperator.LTE,
                value=cone_threshold,
                required=True,
            ),
            Gate(
                metric="kg_cone_r2", op=GateOperator.GTE, value=0.999, required=True
            ),
            # Energy oscillation (instrument QC)
            Gate(
                metric="kg_energy_osc_slope",
                op=GateOperator.GTE,
                value=1.95,
                required=True,
            ),
            Gate(
                metric="kg_energy_osc_slope",
                op=GateOperator.LTE,
                value=2.05,
                required=True,
            ),
            Gate(
                metric="kg_energy_osc_r2",
                op=GateOperator.GTE,
                value=0.999,
                required=True,
            ),
            # Time-reversal
            Gate(
                metric="kg_reversal_sup_norm",
                op=GateOperator.LTE,
                value=1e-12,
                required=True,
            ),
            # Fine-step amplitude
            Gate(
                metric="kg_rel_amp_fine",
                op=GateOperator.LTE,
                value=1e-4,
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
            "name": "klein_gordon",
            "version": "1.0.0",
            "description": "Klein-Gordon J-only hyperbolic dynamics validation",
            "domain": "klein_gordon",
            "references": [
                "VDM CANON_PROGRESS.md#J-only",
                "VALIDATION_METRICS.md#kpi-kg-*",
                "EQUATIONS.md#vdm-e-090-092",
            ],
            "metrics": [
                "kg_dispersion_r2",
                "kg_dispersion_slope_error",
                "kg_dispersion_intercept_error",
                "kg_front_speed",
                "kg_cone_r2",
                "kg_energy_osc_slope",
                "kg_energy_osc_r2",
                "kg_reversal_sup_norm",
                "kg_rel_amp_fine",
            ],
        }
