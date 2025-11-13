"""
Unit tests for VDM Physics Gate Packs
"""

import unittest

from vdm.sandboxes.voe.domain.models import GateOperator
from vdm.sandboxes.voe.infrastructure.gate_packs import (
    FluxContinuityGatePack,
    KleinGordonGatePack,
    MetriplecticGatePack,
    ReactionDiffusionGatePack,
)


class TestMetriplecticGatePack(unittest.TestCase):
    """Test Metriplectic gate pack"""

    def test_create_gates_default(self):
        """Test creating gates with default grid size"""
        gates = MetriplecticGatePack.create_gates()
        self.assertEqual(len(gates), 7)
        
        # Check degeneracy gates
        g1_gate = next(g for g in gates if g.metric == "g1_degeneracy")
        self.assertEqual(g1_gate.op, GateOperator.LTE)
        self.assertEqual(g1_gate.value, 1e-10)
        
    def test_create_gates_scaled(self):
        """Test creating gates with grid scaling"""
        gates = MetriplecticGatePack.create_gates(grid_size=1024)
        
        g1_gate = next(g for g in gates if g.metric == "g1_degeneracy")
        self.assertEqual(g1_gate.value, 1e-10 * 1024)
        
    def test_get_spec(self):
        """Test gate pack specification"""
        spec = MetriplecticGatePack.get_spec()
        self.assertEqual(spec["name"], "metriplectic")
        self.assertEqual(spec["version"], "1.0.0")
        self.assertEqual(len(spec["metrics"]), 7)


class TestKleinGordonGatePack(unittest.TestCase):
    """Test Klein-Gordon gate pack"""

    def test_create_gates_default(self):
        """Test creating gates with default c"""
        gates = KleinGordonGatePack.create_gates()
        self.assertEqual(len(gates), 10)
        
        # Check causal cone gate
        cone_gate = next(g for g in gates if g.metric == "kg_front_speed")
        self.assertEqual(cone_gate.op, GateOperator.LTE)
        self.assertEqual(cone_gate.value, 1.02)
        
    def test_create_gates_custom_c(self):
        """Test creating gates with custom speed of light"""
        c = 2.0
        gates = KleinGordonGatePack.create_gates(c=c)
        
        cone_gate = next(g for g in gates if g.metric == "kg_front_speed")
        self.assertEqual(cone_gate.value, c * 1.02)
        
    def test_energy_oscillation_gates(self):
        """Test energy oscillation slope bounds"""
        gates = KleinGordonGatePack.create_gates()
        
        slope_gates = [g for g in gates if g.metric == "kg_energy_osc_slope"]
        self.assertEqual(len(slope_gates), 2)
        
        # Check upper and lower bounds
        values = [g.value for g in slope_gates]
        self.assertIn(1.95, values)
        self.assertIn(2.05, values)
        
    def test_get_spec(self):
        """Test gate pack specification"""
        spec = KleinGordonGatePack.get_spec()
        self.assertEqual(spec["name"], "klein_gordon")
        self.assertEqual(spec["domain"], "klein_gordon")


class TestReactionDiffusionGatePack(unittest.TestCase):
    """Test Reaction-Diffusion gate pack"""

    def test_create_gates(self):
        """Test creating RD gates"""
        gates = ReactionDiffusionGatePack.create_gates()
        self.assertEqual(len(gates), 4)
        
        # Check front speed gate
        front_gate = next(g for g in gates if g.metric == "rd_front_speed_rel_err")
        self.assertEqual(front_gate.op, GateOperator.LTE)
        self.assertEqual(front_gate.value, 0.05)
        
    def test_r2_gates(self):
        """Test R² quality gates"""
        gates = ReactionDiffusionGatePack.create_gates()
        
        r2_gates = [g for g in gates if "r2" in g.metric]
        self.assertEqual(len(r2_gates), 2)
        
        for gate in r2_gates:
            self.assertEqual(gate.op, GateOperator.GTE)
            self.assertEqual(gate.value, 0.98)
            
    def test_get_spec(self):
        """Test gate pack specification"""
        spec = ReactionDiffusionGatePack.get_spec()
        self.assertEqual(spec["name"], "reaction_diffusion")
        self.assertEqual(len(spec["metrics"]), 4)


class TestFluxContinuityGatePack(unittest.TestCase):
    """Test Flux/Continuity gate pack"""

    def test_create_gates(self):
        """Test creating flux conservation gates"""
        gates = FluxContinuityGatePack.create_gates()
        self.assertEqual(len(gates), 3)
        
        # Check continuity gate
        flux_gate = next(g for g in gates if g.metric == "flux_continuity_rms")
        self.assertEqual(flux_gate.op, GateOperator.LTE)
        self.assertEqual(flux_gate.value, 1e-8)
        
    def test_conservation_gates(self):
        """Test energy and momentum conservation"""
        gates = FluxContinuityGatePack.create_gates()
        
        energy_gate = next(g for g in gates if g.metric == "energy_drift_max")
        momentum_gate = next(g for g in gates if g.metric == "momentum_drift_max")
        
        self.assertEqual(energy_gate.value, 1e-10)
        self.assertEqual(momentum_gate.value, 1e-10)
        
    def test_get_spec(self):
        """Test gate pack specification"""
        spec = FluxContinuityGatePack.get_spec()
        self.assertEqual(spec["name"], "flux_continuity")
        self.assertEqual(spec["domain"], "conservation_laws")


if __name__ == "__main__":
    unittest.main()
