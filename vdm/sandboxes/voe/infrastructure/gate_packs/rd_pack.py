"""
Reaction-Diffusion (RD) Gate Pack

Validates Fisher-KPP reaction-diffusion dynamics with:
- Front speed: c = 2√(Dr) (rel_err ≤ 0.05)
- Front position linear fit: R² ≥ 0.98
- Dispersion: σ(k) = r - Dk² (median rel_err ≤ 0.10)
- Dispersion array fit: R² ≥ 0.98
"""

from typing import Dict, List

from vdm.sandboxes.voe.domain.models import Gate, GateOperator


class ReactionDiffusionGatePack:
    """
    Reaction-Diffusion validation gates

    Based on Fisher-KPP pulled front theory and linear stability analysis
    """

    @staticmethod
    def create_gates() -> List[Gate]:
        """
        Create Reaction-Diffusion validation gates

        Returns:
            List of RD gates
        """
        return [
            # KPP front speed
            Gate(
                metric="rd_front_speed_rel_err",
                op=GateOperator.LTE,
                value=0.05,
                required=True,
            ),
            Gate(
                metric="rd_front_r2", op=GateOperator.GTE, value=0.98, required=True
            ),
            # Dispersion (linear stability)
            Gate(
                metric="rd_dispersion_med_rel_err",
                op=GateOperator.LTE,
                value=0.10,
                required=True,
            ),
            Gate(
                metric="rd_dispersion_r2",
                op=GateOperator.GTE,
                value=0.98,
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
            "name": "reaction_diffusion",
            "version": "1.0.0",
            "description": "Fisher-KPP reaction-diffusion validation",
            "domain": "reaction_diffusion",
            "references": [
                "VDM VALIDATION_METRICS.md#kpi-front-speed-rel-err",
                "VDM VALIDATION_METRICS.md#kpi-r2-front-fit",
                "VDM VALIDATION_METRICS.md#kpi-dispersion-med-rel-err",
                "EQUATIONS.md#vdm-e-033-035",
            ],
            "metrics": [
                "rd_front_speed_rel_err",
                "rd_front_r2",
                "rd_dispersion_med_rel_err",
                "rd_dispersion_r2",
            ],
        }
