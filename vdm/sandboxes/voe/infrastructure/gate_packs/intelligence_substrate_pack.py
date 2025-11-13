"""
Intelligence Substrate Gate Pack

Validates intelligence substrate certification:
- Determinism receipts
- Energy drift envelope
- Computational stability
- Substrate integrity

Keeps substrate certification separate from physics meters.
"""

from typing import Dict, List

from vdm.sandboxes.voe.domain.models import Gate, GateOperator


class IntelligenceSubstrateGatePack:
    """
    Intelligence substrate certification gates

    Promotes reuse across agent work with dedicated substrate metrics
    """

    @staticmethod
    def create_gates() -> List[Gate]:
        """
        Create intelligence substrate validation gates

        Returns:
            List of substrate gates
        """
        return [
            # Determinism receipts
            Gate(
                metric="determinism_receipt_valid",
                op=GateOperator.EQ,
                value=1.0,
                required=True,
            ),
            Gate(
                metric="replay_divergence_count",
                op=GateOperator.EQ,
                value=0.0,
                required=True,
            ),
            Gate(
                metric="state_reproducibility",
                op=GateOperator.GTE,
                value=0.9999,
                required=True,
            ),
            # Energy drift envelope
            Gate(
                metric="substrate_energy_drift_max",
                op=GateOperator.LTE,
                value=1e-10,
                required=True,
            ),
            Gate(
                metric="energy_drift_envelope_bounded",
                op=GateOperator.EQ,
                value=1.0,
                required=True,
            ),
            # Computational stability
            Gate(
                metric="numerical_stability_index",
                op=GateOperator.GTE,
                value=0.98,
                required=True,
            ),
            Gate(
                metric="overflow_underflow_count",
                op=GateOperator.EQ,
                value=0.0,
                required=True,
            ),
            # Substrate integrity
            Gate(
                metric="memory_corruption_detected",
                op=GateOperator.EQ,
                value=0.0,
                required=True,
            ),
            Gate(
                metric="substrate_checksum_valid",
                op=GateOperator.EQ,
                value=1.0,
                required=True,
            ),
            # Agent certifications
            Gate(
                metric="agent_invariant_violations",
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
            "name": "intelligence_substrate",
            "version": "1.0.0",
            "description": "Intelligence substrate certification and integrity",
            "domain": "substrate_certification",
            "references": [
                "VDM VALIDATION_METRICS.md#substrate",
                "CANON_PROGRESS.md#intelligence-substrate",
            ],
            "metrics": [
                "determinism_receipt_valid",
                "replay_divergence_count",
                "state_reproducibility",
                "substrate_energy_drift_max",
                "energy_drift_envelope_bounded",
                "numerical_stability_index",
                "overflow_underflow_count",
                "memory_corruption_detected",
                "substrate_checksum_valid",
                "agent_invariant_violations",
            ],
        }
