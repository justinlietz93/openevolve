"""
VDM Physics Gate Packs

Each pack provides domain-specific validation gates based on VDM physics requirements.
"""

# Core numerics packs
from .metriplectic_pack import MetriplecticGatePack
from .kg_pack import KleinGordonGatePack
from .rd_pack import ReactionDiffusionGatePack
from .flux_pack import FluxContinuityGatePack

# Extended physics surface packs
from .axiom_pack import AxiomGatePack
from .causality_pack import CausalityGatePack
from .a8_hierarchy_pack import A8HierarchyGatePack
from .frw_cosmology_pack import FRWCosmologyGatePack
from .quantum_echoes_pack import QuantumEchoesGatePack

__all__ = [
    # Core numerics
    "MetriplecticGatePack",
    "KleinGordonGatePack",
    "ReactionDiffusionGatePack",
    "FluxContinuityGatePack",
    # Extended physics
    "AxiomGatePack",
    "CausalityGatePack",
    "A8HierarchyGatePack",
    "FRWCosmologyGatePack",
    "QuantumEchoesGatePack",
]
