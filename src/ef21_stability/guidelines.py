from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable, Sequence

import numpy as np

from .landscape import analyze_conditioning_strata, metric_matrix


@dataclass(frozen=True)
class GuidelineBoundary:
    kappa_bar: float
    epsilon: float
    retention_target: float
    penalty_limit: float
    minimum_tau: float
    domain_fully_satisfies: bool

    def to_dict(self) -> dict[str, float | bool]:
        return asdict(self)


@dataclass(frozen=True)
class CompressionAmplification:
    kappa_bar: float
    tau: float
    epsilon_low: float
    epsilon_high: float
    normalized_penalty_low: float
    normalized_penalty_high: float
    absolute_increase: float
    ratio: float

    def to_dict(self) -> dict[str, float]:
        return asdict(self)


@dataclass(frozen=True)
class SlowRegionSummary:
    kappa_bar: float
    cells: int
    fraction_rho_ge_090: float
    fraction_rho_ge_095: float
    fraction_rho_ge_099: float

    def to_dict(self) -> dict[str, float | int]:
        return asdict(self)


def retained_margin(row: dict[str, float]) -> float:
    """Fraction of the homogeneous contraction margin retained by heterogeneity.

    By construction,

        retained = (1 - rho_star) / (1 - rho_homogeneous)
                 = 1 - normalized_penalty.
    """
    denominator = 1.0 - float(row["rho_homogeneous"])
    if denominator <= 0.0:
        raise ValueError("homogeneous contraction factor must be below one")
    return (1.0 - float(row["rho_star"])) / denominator


def _nearest_index(values: np.ndarray, target: float, atol: float = 1e-12) -> int:
    index = int(np.argmin(np.abs(values - target)))
    if abs(float(values[index]) - float(target)) > atol:
        raise ValueError(f"target {target} is not represented on the supplied axis")
    return index


def guideline_boundaries(
    rows: Sequence[dict[str, float]],
    taus: Iterable[float],
    epsilons: Iterable[float],
    *,
    kappa_bar: float,
    retention_targets: Iterable[float] = (0.99, 0.98, 0.95),
    atol: float = 1e-9,
) -> list[GuidelineBoundary]:
    tau_axis = np.asarray(list(taus), dtype=float)
    epsilon_axis = np.asarray(list(epsilons), dtype=float)
    penalty = metric_matrix(rows, tau_axis, epsilon_axis, "normalized_penalty")

    # A one-sided boundary is meaningful only when increasing tau (less
    # heterogeneity) does not worsen the normalized penalty on the tested grid.
    if np.any(np.diff(penalty, axis=0) > atol):
        raise ValueError("tau monotonicity failed; do not derive a one-sided guideline")

    output: list[GuidelineBoundary] = []
    for target in retention_targets:
        if not (0.0 < target <= 1.0):
            raise ValueError("retention targets must lie in (0, 1]")
        limit = 1.0 - float(target)
        for j, epsilon in enumerate(epsilon_axis):
            mask = penalty[:, j] <= limit + atol
            if not np.any(mask):
                raise RuntimeError("tau=1 should always satisfy any nonnegative penalty limit")
            first = int(np.flatnonzero(mask)[0])
            if not np.all(mask[first:]):
                raise ValueError("passing tau set is disconnected; boundary is not interpretable")
            output.append(
                GuidelineBoundary(
                    kappa_bar=float(kappa_bar),
                    epsilon=float(epsilon),
                    retention_target=float(target),
                    penalty_limit=limit,
                    minimum_tau=float(tau_axis[first]),
                    domain_fully_satisfies=bool(first == 0),
                )
            )
    return output


def compression_amplification(
    rows: Sequence[dict[str, float]],
    taus: Iterable[float],
    epsilons: Iterable[float],
    *,
    kappa_bar: float,
    tau: float,
    epsilon_low: float,
    epsilon_high: float,
) -> CompressionAmplification:
    tau_axis = np.asarray(list(taus), dtype=float)
    epsilon_axis = np.asarray(list(epsilons), dtype=float)
    penalty = metric_matrix(rows, tau_axis, epsilon_axis, "normalized_penalty")
    i = _nearest_index(tau_axis, tau)
    j0 = _nearest_index(epsilon_axis, epsilon_low)
    j1 = _nearest_index(epsilon_axis, epsilon_high)
    low = float(penalty[i, j0])
    high = float(penalty[i, j1])
    ratio = high / low if low > 0.0 else float("inf")
    return CompressionAmplification(
        kappa_bar=float(kappa_bar),
        tau=float(tau),
        epsilon_low=float(epsilon_low),
        epsilon_high=float(epsilon_high),
        normalized_penalty_low=low,
        normalized_penalty_high=high,
        absolute_increase=high - low,
        ratio=ratio,
    )


def summarize_slow_region(
    rows: Sequence[dict[str, float]], *, kappa_bar: float
) -> SlowRegionSummary:
    rho = np.asarray([float(row["rho_star"]) for row in rows], dtype=float)
    return SlowRegionSummary(
        kappa_bar=float(kappa_bar),
        cells=len(rows),
        fraction_rho_ge_090=float(np.mean(rho >= 0.90)),
        fraction_rho_ge_095=float(np.mean(rho >= 0.95)),
        fraction_rho_ge_099=float(np.mean(rho >= 0.99)),
    )


def analyze_guidelines(
    kappas: Iterable[float],
    taus: Iterable[float],
    epsilons: Iterable[float],
    *,
    retention_targets: Iterable[float] = (0.99, 0.98, 0.95),
    L: float = 1.0,
    atol: float = 1e-9,
) -> tuple[
    dict[float, list[dict[str, float]]],
    list[GuidelineBoundary],
    list[CompressionAmplification],
    list[SlowRegionSummary],
]:
    tau_axis = np.asarray(list(taus), dtype=float)
    epsilon_axis = np.asarray(list(epsilons), dtype=float)
    all_rows, _ = analyze_conditioning_strata(
        kappas, tau_axis, epsilon_axis, L=L, atol=atol
    )

    boundaries: list[GuidelineBoundary] = []
    amplification: list[CompressionAmplification] = []
    slow_regions: list[SlowRegionSummary] = []
    tau_min = float(tau_axis[0])
    epsilon_low = float(epsilon_axis[0])
    epsilon_high = float(epsilon_axis[-1])

    for kappa, rows in sorted(all_rows.items()):
        boundaries.extend(
            guideline_boundaries(
                rows,
                tau_axis,
                epsilon_axis,
                kappa_bar=kappa,
                retention_targets=retention_targets,
                atol=atol,
            )
        )
        amplification.append(
            compression_amplification(
                rows,
                tau_axis,
                epsilon_axis,
                kappa_bar=kappa,
                tau=tau_min,
                epsilon_low=epsilon_low,
                epsilon_high=epsilon_high,
            )
        )
        slow_regions.append(summarize_slow_region(rows, kappa_bar=kappa))

    return all_rows, boundaries, amplification, slow_regions
