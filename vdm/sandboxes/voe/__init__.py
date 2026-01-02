"""
VDM-Optimized Openevolve (VOE) - Main Package

A gate-driven, security-hardened code evolution system for VDM physics simulations.
Built on OpenEvolve with Clean Architecture principles.
"""

__version__ = "0.1.0"
__author__ = "VDM Systems"

from .domain.models import (
    Candidate,
    Gate,
    GateResult,
    GateVerdict,
    Provenance,
    Scorecard,
    Verdict,
)

__all__ = [
    "Candidate",
    "Gate",
    "GateResult",
    "GateVerdict",
    "Provenance",
    "Scorecard",
    "Verdict",
]
