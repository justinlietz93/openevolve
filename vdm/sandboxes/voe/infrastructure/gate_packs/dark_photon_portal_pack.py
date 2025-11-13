"""
Dark-Photon Portal Gate Pack

Validates dark-photon portal dynamics:
- Fisher information budget
- Regime annotations
- Portal coupling strength
- Hidden sector interactions

Based on VDM dark-photon portal proposals.
"""

from typing import Dict, List

from vdm.sandboxes.voe.domain.models import Gate, GateOperator


class DarkPhotonPortalGatePack:
    """
    Dark-photon portal validation gates

    Based on VDM dark-photon portal proposals with Fisher/noise-budget gates
    """

    @staticmethod
    def create_gates() -> List[Gate]:
        """
        Create dark-photon portal validation gates

        Returns:
            List of dark-photon gates
        """
        return [
            # Fisher information budget
            Gate(
                metric="fisher_information_bound",
                op=GateOperator.GTE,
                value=1.0,
                required=True,
            ),
            Gate(
                metric="fisher_budget_saturation",
                op=GateOperator.LTE,
                value=0.95,
                required=True,
            ),
            # Noise budget
            Gate(
                metric="noise_budget_residual",
                op=GateOperator.LTE,
                value=0.05,
                required=True,
            ),
            Gate(
                metric="signal_to_noise_ratio",
                op=GateOperator.GTE,
                value=10.0,
                required=True,
            ),
            # Portal coupling
            Gate(
                metric="portal_coupling_strength",
                op=GateOperator.GTE,
                value=1e-6,
                required=True,
            ),
            Gate(
                metric="portal_coupling_strength",
                op=GateOperator.LTE,
                value=1e-2,
                required=True,
            ),
            # Hidden sector
            Gate(
                metric="hidden_sector_mass_ratio",
                op=GateOperator.GTE,
                value=0.1,
                required=True,
            ),
            Gate(
                metric="hidden_sector_interaction_rate",
                op=GateOperator.GTE,
                value=1e-4,
                required=False,  # Advisory
            ),
            # Regime annotations
            Gate(
                metric="regime_classification_valid",
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
            "name": "dark_photon_portal",
            "version": "1.0.0",
            "description": "Dark-photon portal Fisher/noise-budget validation",
            "domain": "dark_photon",
            "references": [
                "VDM VALIDATION_METRICS.md#dark-photon",
                "PROPOSALS.md#dark-photon-portal",
            ],
            "metrics": [
                "fisher_information_bound",
                "fisher_budget_saturation",
                "noise_budget_residual",
                "signal_to_noise_ratio",
                "portal_coupling_strength",
                "hidden_sector_mass_ratio",
                "hidden_sector_interaction_rate",
                "regime_classification_valid",
            ],
        }
