"""
Example: Using VDM Physics Gate Packs

Demonstrates how to use the VDM physics gate packs for validation.
"""

import asyncio
import uuid

from vdm.sandboxes.voe.domain.models import Candidate
from vdm.sandboxes.voe.infrastructure.evaluator import Scorecarder, Verifier
from vdm.sandboxes.voe.infrastructure.gate_packs import (
    FluxContinuityGatePack,
    KleinGordonGatePack,
    MetriplecticGatePack,
    ReactionDiffusionGatePack,
)


def example_metriplectic_validation():
    """Example: Validate metriplectic structure"""
    print("=" * 70)
    print("Example 1: Metriplectic Structure Validation")
    print("=" * 70)

    # Create gates for a 512x512 grid
    gates = MetriplecticGatePack.create_gates(grid_size=512)

    print(f"\nMetriplectic gates created: {len(gates)}")
    print(f"Grid size: 512 (degeneracy threshold scaled)")

    # Mock metrics from VDM runner
    metrics = {
        "g1_degeneracy": 3.2e-11 * 512,  # Scaled by grid size
        "g2_degeneracy": 4.1e-11 * 512,
        "j_skew_symmetry_norm": 5.2e-13,
        "m_psd_min_eigenvalue": 1.3e-14,
        "delta_L_h": -1.2e-9,  # Negative (good)
        "noether_energy_drift": 8.3e-17,
        "noether_momentum_drift": 2.6e-17,
    }

    # Evaluate gates
    config = {"timeout": 60}
    verifier = Verifier(config)
    scorecarder = Scorecarder(verifier)

    verdict = scorecarder.evaluate_gates(gates, metrics)

    print(f"\nGate Evaluation Results:")
    print(f"  Overall Pass: {verdict.passed}")
    print(f"  Violations: {verdict.violations}")

    for result in verdict.gate_results:
        status = "✓" if result.passed else "✗"
        print(
            f"  {status} {result.gate.metric}: "
            f"{result.actual_value:.2e} {result.gate.op.value} {result.gate.value:.2e}"
        )

    return verdict.passed


def example_klein_gordon_validation():
    """Example: Validate Klein-Gordon dynamics"""
    print("\n" + "=" * 70)
    print("Example 2: Klein-Gordon Validation")
    print("=" * 70)

    # Create gates with c=1.0
    gates = KleinGordonGatePack.create_gates(c=1.0)

    print(f"\nKlein-Gordon gates created: {len(gates)}")
    print(f"Speed of light c: 1.0")
    print(f"Causal cone threshold: v ≤ 1.02")

    # Mock metrics from KG runner
    metrics = {
        "kg_dispersion_r2": 0.999999997,
        "kg_dispersion_slope_error": 0.0002,
        "kg_dispersion_intercept_error": 0.0022,
        "kg_front_speed": 0.998,  # Within causal cone
        "kg_cone_r2": 0.99985,
        "kg_energy_osc_slope": 1.999885,  # Within [1.95, 2.05]
        "kg_energy_osc_r2": 0.99999999937,
        "kg_reversal_sup_norm": 2.93e-16,
        "kg_rel_amp_fine": 1.346e-5,
    }

    # Evaluate gates
    config = {"timeout": 60}
    verifier = Verifier(config)
    scorecarder = Scorecarder(verifier)

    verdict = scorecarder.evaluate_gates(gates, metrics)

    print(f"\nGate Evaluation Results:")
    print(f"  Overall Pass: {verdict.passed}")

    # Show key results
    key_metrics = [
        "kg_dispersion_r2",
        "kg_front_speed",
        "kg_energy_osc_slope",
        "kg_reversal_sup_norm",
    ]

    for metric in key_metrics:
        result = next(r for r in verdict.gate_results if r.gate.metric == metric)
        status = "✓" if result.passed else "✗"
        print(
            f"  {status} {result.gate.metric}: {result.actual_value:.6e} "
            f"{result.gate.op.value} {result.gate.value:.6e}"
        )

    return verdict.passed


def example_reaction_diffusion_validation():
    """Example: Validate Reaction-Diffusion fronts"""
    print("\n" + "=" * 70)
    print("Example 3: Reaction-Diffusion (Fisher-KPP) Validation")
    print("=" * 70)

    # Create RD gates
    gates = ReactionDiffusionGatePack.create_gates()

    print(f"\nReaction-Diffusion gates created: {len(gates)}")
    print(f"Theory: c = 2√(Dr)")

    # Mock metrics from RD runner
    metrics = {
        "rd_front_speed_rel_err": 0.023,  # 2.3% error
        "rd_front_r2": 0.9921,
        "rd_dispersion_med_rel_err": 0.067,  # 6.7% median error
        "rd_dispersion_r2": 0.9912,
    }

    # Evaluate gates
    config = {"timeout": 60}
    verifier = Verifier(config)
    scorecarder = Scorecarder(verifier)

    verdict = scorecarder.evaluate_gates(gates, metrics)

    print(f"\nGate Evaluation Results:")
    print(f"  Overall Pass: {verdict.passed}")

    for result in verdict.gate_results:
        status = "✓" if result.passed else "✗"
        print(
            f"  {status} {result.gate.metric}: "
            f"{result.actual_value:.4f} {result.gate.op.value} {result.gate.value:.4f}"
        )

    return verdict.passed


def example_flux_continuity_validation():
    """Example: Validate flux/continuity conservation"""
    print("\n" + "=" * 70)
    print("Example 4: Flux/Continuity Conservation Validation")
    print("=" * 70)

    # Create flux gates
    gates = FluxContinuityGatePack.create_gates()

    print(f"\nFlux/Continuity gates created: {len(gates)}")
    print(f"Conservation law: ∂_t e + ∇·s → 0")

    # Mock metrics from conservation analysis
    metrics = {
        "flux_continuity_rms": 3.2e-9,
        "energy_drift_max": 1.7e-11,
        "momentum_drift_max": 2.3e-11,
    }

    # Evaluate gates
    config = {"timeout": 60}
    verifier = Verifier(config)
    scorecarder = Scorecarder(verifier)

    verdict = scorecarder.evaluate_gates(gates, metrics)

    print(f"\nGate Evaluation Results:")
    print(f"  Overall Pass: {verdict.passed}")

    for result in verdict.gate_results:
        status = "✓" if result.passed else "✗"
        print(
            f"  {status} {result.gate.metric}: "
            f"{result.actual_value:.2e} {result.gate.op.value} {result.gate.value:.2e}"
        )

    return verdict.passed


if __name__ == "__main__":
    print("VDM Physics Gate Packs - Usage Examples")
    print()

    results = []
    results.append(("Metriplectic", example_metriplectic_validation()))
    results.append(("Klein-Gordon", example_klein_gordon_validation()))
    results.append(("Reaction-Diffusion", example_reaction_diffusion_validation()))
    results.append(("Flux/Continuity", example_flux_continuity_validation()))

    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {name}: {status}")

    all_passed = all(p for _, p in results)
    print(f"\nOverall: {'✓ All gate packs validated' if all_passed else '✗ Some failures'}")
