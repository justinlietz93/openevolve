"""
Tachyonic Tube Gate Pack

Validates tachyon condensation and tube spectrum:
- Spectrum completeness
- Energy curvature
- Condensation phase transitions
- Tube stability

Based on VDM tachyonic condensation results.
"""

from typing import Dict, List

from vdm.sandboxes.voe.domain.models import Gate, GateOperator


class TachyonicTubeGatePack:
    """
    Tachyonic tube and condensation validation gates

    Based on VDM tachyon condensation proposals and results
    """

    @staticmethod
    def create_gates() -> List[Gate]:
        """
        Create tachyonic tube validation gates

        Returns:
            List of tachyon gates
        """
        return [
            # Spectrum completeness
            Gate(
                metric="spectrum_completeness_ratio",
                op=GateOperator.GTE,
                value=0.95,
                required=True,
            ),
            Gate(
                metric="spectrum_gap_violations",
                op=GateOperator.EQ,
                value=0.0,
                required=True,
            ),
            # Energy curvature
            Gate(
                metric="energy_curvature_bound",
                op=GateOperator.LTE,
                value=1.05,
                required=True,
            ),
            Gate(
                metric="curvature_sign_consistency",
                op=GateOperator.EQ,
                value=1.0,
                required=True,
            ),
            # Condensation phase
            Gate(
                metric="condensation_threshold_crossing",
                op=GateOperator.EQ,
                value=1.0,
                required=True,
            ),
            Gate(
                metric="phase_transition_hysteresis",
                op=GateOperator.LTE,
                value=0.02,
                required=True,
            ),
            # Tube stability
            Gate(
                metric="tube_stability_index",
                op=GateOperator.GTE,
                value=0.98,
                required=True,
            ),
            Gate(
                metric="tube_coherence_length",
                op=GateOperator.GTE,
                value=10.0,
                required=True,
            ),
            # Vacuum fluctuations
            Gate(
                metric="vacuum_fluctuation_bound",
                op=GateOperator.LTE,
                value=1e-8,
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
            "name": "tachyonic_tube",
            "version": "1.0.0",
            "description": "Tachyonic condensation and tube spectrum validation",
            "domain": "tachyon_condensation",
            "references": [
                "VDM VALIDATION_METRICS.md#tachyon",
                "CANON_PROGRESS.md#tachyonic-tube",
            ],
            "metrics": [
                "spectrum_completeness_ratio",
                "spectrum_gap_violations",
                "energy_curvature_bound",
                "curvature_sign_consistency",
                "condensation_threshold_crossing",
                "phase_transition_hysteresis",
                "tube_stability_index",
                "tube_coherence_length",
                "vacuum_fluctuation_bound",
            ],
        }
