"""
Unit tests for Additional VDM Physics Gate Packs (Full Coverage)
"""

import unittest

from vdm.sandboxes.voe.domain.models import GateOperator
from vdm.sandboxes.voe.infrastructure.gate_packs import (
    DarkPhotonPortalGatePack,
    IntelligenceSubstrateGatePack,
    QuantumGravityBridgeGatePack,
    TachyonicTubeGatePack,
    WaveFluxGatePack,
)


class TestWaveFluxGatePack(unittest.TestCase):
    """Test Wave-Flux gate pack"""

    def test_create_gates(self):
        """Test creating wave-flux gates"""
        gates = WaveFluxGatePack.create_gates()
        self.assertGreaterEqual(len(gates), 9)

        # Check closed-box energy gate
        energy_gate = next(
            g for g in gates if g.metric == "closed_box_energy_drift"
        )
        self.assertEqual(energy_gate.op, GateOperator.LTE)
        self.assertEqual(energy_gate.value, 1e-10)

    def test_port_symmetry_gates(self):
        """Test open-port symmetry gates"""
        gates = WaveFluxGatePack.create_gates()

        port_sym = next(g for g in gates if g.metric == "port_symmetry_violation")
        self.assertEqual(port_sym.op, GateOperator.LTE)
        self.assertEqual(port_sym.value, 1e-8)

    def test_absorber_gates(self):
        """Test absorber budget gates"""
        gates = WaveFluxGatePack.create_gates()

        absorber = next(g for g in gates if g.metric == "absorber_budget_residual")
        self.assertEqual(absorber.value, 1e-9)

    def test_get_spec(self):
        """Test gate pack specification"""
        spec = WaveFluxGatePack.get_spec()
        self.assertEqual(spec["name"], "wave_flux")
        self.assertEqual(spec["domain"], "thermodynamic_routing")


class TestTachyonicTubeGatePack(unittest.TestCase):
    """Test Tachyonic Tube gate pack"""

    def test_create_gates(self):
        """Test creating tachyon gates"""
        gates = TachyonicTubeGatePack.create_gates()
        self.assertGreaterEqual(len(gates), 9)

        # Check spectrum completeness
        spectrum = next(
            g for g in gates if g.metric == "spectrum_completeness_ratio"
        )
        self.assertEqual(spectrum.op, GateOperator.GTE)
        self.assertEqual(spectrum.value, 0.95)

    def test_energy_curvature_gates(self):
        """Test energy curvature validation"""
        gates = TachyonicTubeGatePack.create_gates()

        curvature = next(g for g in gates if g.metric == "energy_curvature_bound")
        self.assertEqual(curvature.op, GateOperator.LTE)
        self.assertEqual(curvature.value, 1.05)

    def test_condensation_gates(self):
        """Test condensation phase gates"""
        gates = TachyonicTubeGatePack.create_gates()

        condensation = next(
            g for g in gates if g.metric == "condensation_threshold_crossing"
        )
        self.assertEqual(condensation.value, 1.0)

    def test_get_spec(self):
        """Test gate pack specification"""
        spec = TachyonicTubeGatePack.get_spec()
        self.assertEqual(spec["name"], "tachyonic_tube")
        self.assertEqual(spec["domain"], "tachyon_condensation")


class TestDarkPhotonPortalGatePack(unittest.TestCase):
    """Test Dark-Photon Portal gate pack"""

    def test_create_gates(self):
        """Test creating dark-photon gates"""
        gates = DarkPhotonPortalGatePack.create_gates()
        self.assertGreaterEqual(len(gates), 9)

        # Check Fisher information
        fisher = next(g for g in gates if g.metric == "fisher_information_bound")
        self.assertEqual(fisher.op, GateOperator.GTE)
        self.assertEqual(fisher.value, 1.0)

    def test_coupling_gates(self):
        """Test portal coupling bounds"""
        gates = DarkPhotonPortalGatePack.create_gates()

        coupling_gates = [
            g for g in gates if g.metric == "portal_coupling_strength"
        ]
        self.assertEqual(len(coupling_gates), 2)

        # Check upper and lower bounds
        values = [g.value for g in coupling_gates]
        self.assertIn(1e-6, values)
        self.assertIn(1e-2, values)

    def test_advisory_gates(self):
        """Test advisory gates"""
        gates = DarkPhotonPortalGatePack.create_gates()

        interaction = next(
            g for g in gates if g.metric == "hidden_sector_interaction_rate"
        )
        self.assertFalse(interaction.required)  # Advisory

    def test_get_spec(self):
        """Test gate pack specification"""
        spec = DarkPhotonPortalGatePack.get_spec()
        self.assertEqual(spec["name"], "dark_photon_portal")
        self.assertEqual(spec["domain"], "dark_photon")


class TestQuantumGravityBridgeGatePack(unittest.TestCase):
    """Test Quantum-Gravity Bridge gate pack"""

    def test_create_gates(self):
        """Test creating QG bridge gates"""
        gates = QuantumGravityBridgeGatePack.create_gates()
        self.assertGreaterEqual(len(gates), 11)

        # Check Myrheim-Meyer dimension
        mm_gates = [
            g for g in gates if g.metric == "myrheim_meyer_dimension"
        ]
        self.assertEqual(len(mm_gates), 2)

    def test_dimension_bounds(self):
        """Test Myrheim-Meyer dimension bounds"""
        gates = QuantumGravityBridgeGatePack.create_gates()

        mm_gates = [
            g for g in gates if g.metric == "myrheim_meyer_dimension"
        ]
        values = [g.value for g in mm_gates]
        self.assertIn(3.8, values)
        self.assertIn(4.2, values)

    def test_holonomy_gates(self):
        """Test holonomy loop gates"""
        gates = QuantumGravityBridgeGatePack.create_gates()

        holonomy = next(g for g in gates if g.metric == "holonomy_closure_error")
        self.assertEqual(holonomy.op, GateOperator.LTE)
        self.assertEqual(holonomy.value, 1e-10)

    def test_diamond_scaling_gates(self):
        """Test diamond scaling gates"""
        gates = QuantumGravityBridgeGatePack.create_gates()

        diamond_gates = [
            g for g in gates if g.metric == "diamond_volume_scaling_slope"
        ]
        self.assertEqual(len(diamond_gates), 2)

    def test_get_spec(self):
        """Test gate pack specification"""
        spec = QuantumGravityBridgeGatePack.get_spec()
        self.assertEqual(spec["name"], "quantum_gravity_bridge")
        self.assertEqual(spec["domain"], "quantum_gravity")


class TestIntelligenceSubstrateGatePack(unittest.TestCase):
    """Test Intelligence Substrate gate pack"""

    def test_create_gates(self):
        """Test creating substrate gates"""
        gates = IntelligenceSubstrateGatePack.create_gates()
        self.assertGreaterEqual(len(gates), 10)

        # Check determinism receipt
        determinism = next(
            g for g in gates if g.metric == "determinism_receipt_valid"
        )
        self.assertEqual(determinism.op, GateOperator.EQ)
        self.assertEqual(determinism.value, 1.0)

    def test_energy_drift_gates(self):
        """Test energy drift envelope gates"""
        gates = IntelligenceSubstrateGatePack.create_gates()

        energy_drift = next(
            g for g in gates if g.metric == "substrate_energy_drift_max"
        )
        self.assertEqual(energy_drift.op, GateOperator.LTE)
        self.assertEqual(energy_drift.value, 1e-10)

    def test_stability_gates(self):
        """Test computational stability gates"""
        gates = IntelligenceSubstrateGatePack.create_gates()

        stability = next(
            g for g in gates if g.metric == "numerical_stability_index"
        )
        self.assertEqual(stability.op, GateOperator.GTE)
        self.assertEqual(stability.value, 0.98)

    def test_integrity_gates(self):
        """Test substrate integrity gates"""
        gates = IntelligenceSubstrateGatePack.create_gates()

        corruption = next(
            g for g in gates if g.metric == "memory_corruption_detected"
        )
        self.assertEqual(corruption.op, GateOperator.EQ)
        self.assertEqual(corruption.value, 0.0)

    def test_get_spec(self):
        """Test gate pack specification"""
        spec = IntelligenceSubstrateGatePack.get_spec()
        self.assertEqual(spec["name"], "intelligence_substrate")
        self.assertEqual(spec["domain"], "substrate_certification")


if __name__ == "__main__":
    unittest.main()
