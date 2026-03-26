"""
Unit tests for Extended VDM Physics Gate Packs
"""

import unittest

from vdm.sandboxes.voe.domain.models import GateOperator
from vdm.sandboxes.voe.infrastructure.gate_packs import (
    A8HierarchyGatePack,
    AxiomGatePack,
    CausalityGatePack,
    FRWCosmologyGatePack,
    QuantumEchoesGatePack,
)


class TestAxiomGatePack(unittest.TestCase):
    """Test Axiom gate pack"""

    def test_create_gates_default(self):
        """Test creating axiom gates with defaults"""
        gates = AxiomGatePack.create_gates()
        self.assertGreaterEqual(len(gates), 10)

        # Check closure gate
        closure_gate = next(g for g in gates if g.metric == "closure_residual")
        self.assertEqual(closure_gate.op, GateOperator.LTE)
        self.assertEqual(closure_gate.value, 1e-10)

    def test_create_gates_scaled(self):
        """Test creating gates with scaling"""
        gates = AxiomGatePack.create_gates(grid_size=1024, tolerance_scale=2.0)

        # Check scaled degeneracy
        j_deg = next(g for g in gates if g.metric == "j_degeneracy_global")
        self.assertEqual(j_deg.value, 1e-10 * 1024 * 2.0)

    def test_get_spec(self):
        """Test gate pack specification"""
        spec = AxiomGatePack.get_spec()
        self.assertEqual(spec["name"], "axiom")
        self.assertEqual(spec["domain"], "foundational")
        self.assertGreaterEqual(len(spec["metrics"]), 10)


class TestCausalityGatePack(unittest.TestCase):
    """Test Causality gate pack"""

    def test_create_gates_default(self):
        """Test creating causality gates"""
        gates = CausalityGatePack.create_gates()
        self.assertGreaterEqual(len(gates), 9)

        # Check Telegraph-Fisher gates
        tf_r2 = next(g for g in gates if g.metric == "tf_dispersion_r2")
        self.assertEqual(tf_r2.op, GateOperator.GTE)
        self.assertEqual(tf_r2.value, 0.999)

    def test_dag_gates(self):
        """Test DAG ordering gates"""
        gates = CausalityGatePack.create_gates()

        dag_cycles = next(g for g in gates if g.metric == "dag_cycle_count")
        self.assertEqual(dag_cycles.op, GateOperator.EQ)
        self.assertEqual(dag_cycles.value, 0.0)

    def test_get_spec(self):
        """Test gate pack specification"""
        spec = CausalityGatePack.get_spec()
        self.assertEqual(spec["name"], "causality")
        self.assertEqual(spec["domain"], "causality")


class TestA8HierarchyGatePack(unittest.TestCase):
    """Test A8 Hierarchy gate pack"""

    def test_create_gates(self):
        """Test creating A8 gates"""
        gates = A8HierarchyGatePack.create_gates()
        self.assertGreaterEqual(len(gates), 12)

        # Check depth scaling gates
        depth_gates = [g for g in gates if "depth_log_fit_slope" in g.metric]
        self.assertEqual(len(depth_gates), 2)

    def test_area_law_gates(self):
        """Test area law validation gates"""
        gates = A8HierarchyGatePack.create_gates()

        # 2D area law
        area_2d_gates = [g for g in gates if "area_law_slope_2d" in g.metric]
        self.assertEqual(len(area_2d_gates), 2)

        # 3D area law
        area_3d_gates = [g for g in gates if "area_law_slope_3d" in g.metric]
        self.assertEqual(len(area_3d_gates), 2)

    def test_get_spec(self):
        """Test gate pack specification"""
        spec = A8HierarchyGatePack.get_spec()
        self.assertEqual(spec["name"], "a8_hierarchy")
        self.assertEqual(spec["domain"], "hierarchy")


class TestFRWCosmologyGatePack(unittest.TestCase):
    """Test FRW Cosmology gate pack"""

    def test_create_gates(self):
        """Test creating FRW gates"""
        gates = FRWCosmologyGatePack.create_gates()
        self.assertGreaterEqual(len(gates), 6)

        # Check continuity gate
        continuity = next(g for g in gates if g.metric == "frw_continuity_residual")
        self.assertEqual(continuity.op, GateOperator.LTE)
        self.assertEqual(continuity.value, 1e-10)

    def test_advisory_gates(self):
        """Test advisory vs required gates"""
        gates = FRWCosmologyGatePack.create_gates()

        lcdm_gate = next(g for g in gates if "lcdm_w_plus_one" in g.metric)
        self.assertFalse(lcdm_gate.required)  # Advisory

    def test_get_spec(self):
        """Test gate pack specification"""
        spec = FRWCosmologyGatePack.get_spec()
        self.assertEqual(spec["name"], "frw_cosmology")
        self.assertEqual(spec["domain"], "cosmology")


class TestQuantumEchoesGatePack(unittest.TestCase):
    """Test Quantum Echoes gate pack"""

    def test_create_gates(self):
        """Test creating quantum echo gates"""
        gates = QuantumEchoesGatePack.create_gates()
        self.assertGreaterEqual(len(gates), 10)

        # Check CEG gates
        ceg_gain = next(g for g in gates if g.metric == "ceg_echo_gain")
        self.assertEqual(ceg_gain.op, GateOperator.GTE)
        self.assertEqual(ceg_gain.value, 0.0)

    def test_sie_gates(self):
        """Test SIE stability gates"""
        gates = QuantumEchoesGatePack.create_gates()

        sie_stability = next(g for g in gates if g.metric == "sie_stability_index")
        self.assertEqual(sie_stability.op, GateOperator.GTE)
        self.assertEqual(sie_stability.value, 0.95)

    def test_get_spec(self):
        """Test gate pack specification"""
        spec = QuantumEchoesGatePack.get_spec()
        self.assertEqual(spec["name"], "quantum_echoes")
        self.assertEqual(spec["domain"], "quantum_echoes")


if __name__ == "__main__":
    unittest.main()
