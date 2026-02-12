"""
Flux/Continuity Gate Pack

Validates conservation laws with:
- Flux continuity: ∂_t e + ∇·s → 0 (RMS thresholds)
- Energy drift: max |ΔE| ≤ 1e-10
- Momentum drift: max |ΔP| ≤ 1e-10
"""

from typing import Dict, List

from vdm.sandboxes.voe.domain.models import Gate, GateOperator


class FluxContinuityGatePack:
    """
    Flux/Continuity conservation validation gates

    Based on VDM conservation law requirements
    """

    @staticmethod
    def create_gates() -> List[Gate]:
        """
        Create Flux/Continuity validation gates

        Returns:
            List of flux conservation gates
        """
        return [
            # Flux continuity equation
            Gate(
                metric="flux_continuity_rms",
                op=GateOperator.LTE,
                value=1e-8,
                required=True,
            ),
            # Energy conservation
            Gate(
                metric="energy_drift_max",
                op=GateOperator.LTE,
                value=1e-10,
                required=True,
            ),
            # Momentum conservation
            Gate(
                metric="momentum_drift_max",
                op=GateOperator.LTE,
                value=1e-10,
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
            "name": "flux_continuity",
            "version": "1.0.0",
            "description": "Flux/Continuity conservation law validation",
            "domain": "conservation_laws",
            "references": [
                "VDM AXIOMS.md#conservation",
                "VALIDATION_METRICS.md#conservation",
            ],
            "metrics": [
                "flux_continuity_rms",
                "energy_drift_max",
                "momentum_drift_max",
            ],
        }
