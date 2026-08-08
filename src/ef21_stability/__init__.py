"""Controlled stability and sensitivity analysis for heterogeneous EF21."""

from .core import (
    TwoAgentConfig,
    analyze_config,
    cubic_coefficients,
    empirical_eta_star,
    fixed_average_mus,
    homogeneous_theorem_rate,
    optimal_contraction_factor,
    run_grid,
)

__all__ = [
    "TwoAgentConfig",
    "analyze_config",
    "cubic_coefficients",
    "empirical_eta_star",
    "fixed_average_mus",
    "homogeneous_theorem_rate",
    "optimal_contraction_factor",
    "run_grid",
]
