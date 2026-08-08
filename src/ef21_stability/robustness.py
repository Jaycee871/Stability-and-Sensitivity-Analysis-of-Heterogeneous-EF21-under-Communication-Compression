from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

import numpy as np

from .core import (
    TwoAgentConfig,
    analyze_config,
    cubic_coefficients,
    optimal_contraction_factor,
)


@dataclass(frozen=True)
class OffGridSummary:
    kappa_bar: float
    pairs: int
    seed: int
    max_tau_monotonicity_violation: float
    max_epsilon_monotonicity_violation: float
    max_root_residual: float
    min_normalized_penalty: float
    max_normalized_penalty: float

    def to_dict(self) -> dict[str, float | int]:
        return asdict(self)


@dataclass(frozen=True)
class BoundaryReference:
    kappa_bar: float
    epsilon: float
    retention_target: float
    tau_min: float
    tau_max: float
    continuous_boundary: float
    domain_fully_satisfies: bool

    def to_dict(self) -> dict[str, float | bool]:
        return asdict(self)


def _normalized_penalty(tau: float, epsilon: float, kappa_bar: float) -> float:
    row = analyze_config(
        TwoAgentConfig(
            epsilon=float(epsilon),
            tau=float(tau),
            L=1.0,
            mu_bar=1.0 / float(kappa_bar),
        )
    )
    return float(row["normalized_penalty"])


def paired_offgrid_validation(
    kappa_bar: float,
    *,
    pairs: int = 20_000,
    seed: int = 20_260_809,
    tau_min: float = 0.05,
    tau_max: float = 1.0,
    epsilon_min: float = 0.01,
    epsilon_max: float = 0.95,
) -> OffGridSummary:
    """Stress-test observed monotonic patterns at random off-grid points.

    The test is deliberately limited to the audited Phase 2/3 domain.  It is a
    numerical robustness check, not an analytic proof of monotonicity.
    """
    if pairs <= 0:
        raise ValueError("pairs must be positive")
    rng = np.random.default_rng(int(seed) + int(round(kappa_bar)))

    max_tau_violation = -np.inf
    max_epsilon_violation = -np.inf
    max_root_residual = 0.0
    min_penalty = np.inf
    max_penalty = -np.inf

    for _ in range(int(pairs)):
        tau_a, tau_b = np.sort(rng.uniform(tau_min, tau_max, 2))
        epsilon = float(rng.uniform(epsilon_min, epsilon_max))
        penalty_a = _normalized_penalty(float(tau_a), epsilon, kappa_bar)
        penalty_b = _normalized_penalty(float(tau_b), epsilon, kappa_bar)
        # Lower tau means stronger heterogeneity, so penalty_a should be >= penalty_b.
        max_tau_violation = max(max_tau_violation, penalty_b - penalty_a)

        epsilon_a, epsilon_b = np.sort(rng.uniform(epsilon_min, epsilon_max, 2))
        tau = float(rng.uniform(tau_min, tau_max))
        penalty_low = _normalized_penalty(tau, float(epsilon_a), kappa_bar)
        penalty_high = _normalized_penalty(tau, float(epsilon_b), kappa_bar)
        # Higher compression error should not reduce the normalized penalty.
        max_epsilon_violation = max(
            max_epsilon_violation, penalty_low - penalty_high
        )

        config = TwoAgentConfig(
            epsilon=epsilon,
            tau=tau,
            L=1.0,
            mu_bar=1.0 / float(kappa_bar),
        )
        rho = optimal_contraction_factor(config)
        residual = abs(float(np.polyval(cubic_coefficients(config), rho)))
        max_root_residual = max(max_root_residual, residual)

        penalty = _normalized_penalty(tau, epsilon, kappa_bar)
        min_penalty = min(min_penalty, penalty)
        max_penalty = max(max_penalty, penalty)

    return OffGridSummary(
        kappa_bar=float(kappa_bar),
        pairs=int(pairs),
        seed=int(seed),
        max_tau_monotonicity_violation=float(max_tau_violation),
        max_epsilon_monotonicity_violation=float(max_epsilon_violation),
        max_root_residual=float(max_root_residual),
        min_normalized_penalty=float(min_penalty),
        max_normalized_penalty=float(max_penalty),
    )


def continuous_retention_boundary(
    kappa_bar: float,
    *,
    epsilon: float = 0.95,
    retention_target: float = 0.99,
    tau_min: float = 0.05,
    tau_max: float = 1.0,
    iterations: int = 80,
) -> BoundaryReference:
    """Bisection reference for a retention boundary inside the audited domain."""
    if not (0.0 < retention_target <= 1.0):
        raise ValueError("retention_target must lie in (0, 1]")
    limit = 1.0 - float(retention_target)
    low_penalty = _normalized_penalty(tau_min, epsilon, kappa_bar)
    if low_penalty <= limit:
        return BoundaryReference(
            kappa_bar=float(kappa_bar),
            epsilon=float(epsilon),
            retention_target=float(retention_target),
            tau_min=float(tau_min),
            tau_max=float(tau_max),
            continuous_boundary=float(tau_min),
            domain_fully_satisfies=True,
        )

    high_penalty = _normalized_penalty(tau_max, epsilon, kappa_bar)
    if high_penalty > limit + 1e-10:
        raise RuntimeError("tau_max does not satisfy the requested retention target")

    lo = float(tau_min)
    hi = float(tau_max)
    for _ in range(int(iterations)):
        mid = 0.5 * (lo + hi)
        if _normalized_penalty(mid, epsilon, kappa_bar) > limit:
            lo = mid
        else:
            hi = mid

    return BoundaryReference(
        kappa_bar=float(kappa_bar),
        epsilon=float(epsilon),
        retention_target=float(retention_target),
        tau_min=float(tau_min),
        tau_max=float(tau_max),
        continuous_boundary=float(hi),
        domain_fully_satisfies=False,
    )


def grid_retention_boundary(
    kappa_bar: float,
    tau_points: int,
    *,
    epsilon: float = 0.95,
    retention_target: float = 0.99,
    tau_min: float = 0.05,
    tau_max: float = 1.0,
) -> float:
    if tau_points < 2:
        raise ValueError("tau_points must be at least two")
    limit = 1.0 - float(retention_target)
    taus = np.linspace(tau_min, tau_max, int(tau_points))
    penalties = np.asarray(
        [_normalized_penalty(float(tau), epsilon, kappa_bar) for tau in taus],
        dtype=float,
    )
    passing = np.flatnonzero(penalties <= limit + 1e-12)
    if len(passing) == 0:
        raise RuntimeError("no grid point satisfies the requested retention target")
    return float(taus[int(passing[0])])


def boundary_convergence_table(
    kappas: Iterable[float] = (2.0, 10.0, 100.0),
    resolutions: Iterable[int] = (96, 191, 381, 761, 1521),
    *,
    epsilon: float = 0.95,
    retention_target: float = 0.99,
) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    for kappa in kappas:
        reference = continuous_retention_boundary(
            float(kappa),
            epsilon=epsilon,
            retention_target=retention_target,
        )
        grids = {
            str(int(points)): grid_retention_boundary(
                float(kappa),
                int(points),
                epsilon=epsilon,
                retention_target=retention_target,
            )
            for points in resolutions
        }
        output.append(
            {
                **reference.to_dict(),
                "grid_boundaries": grids,
            }
        )
    return output
