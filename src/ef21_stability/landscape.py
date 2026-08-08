from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable, Sequence

import numpy as np

from .core import run_grid


@dataclass(frozen=True)
class StratumSummary:
    kappa_bar: float
    mu_bar: float
    cells: int
    rho_min: float
    rho_max: float
    max_abs_penalty: float
    max_abs_at_tau: float
    max_abs_at_epsilon: float
    max_normalized_penalty: float
    max_norm_at_tau: float
    max_norm_at_epsilon: float
    max_tau_monotonicity_diff: float
    min_epsilon_monotonicity_diff: float
    tau_monotone_nonincreasing: bool
    epsilon_monotone_nondecreasing: bool

    def to_dict(self) -> dict[str, float | int | bool]:
        return asdict(self)


def _axis(values: Iterable[float]) -> np.ndarray:
    array = np.asarray(list(values), dtype=float)
    if array.ndim != 1 or len(array) < 2:
        raise ValueError("axis must contain at least two values")
    if np.any(np.diff(array) <= 0):
        raise ValueError("axis values must be strictly increasing")
    return array


def metric_matrix(
    rows: Sequence[dict[str, float]],
    taus: Iterable[float],
    epsilons: Iterable[float],
    metric: str,
) -> np.ndarray:
    tau_axis = _axis(taus)
    epsilon_axis = _axis(epsilons)
    lookup = {
        (round(float(row["tau"]), 14), round(float(row["epsilon"]), 14)): float(row[metric])
        for row in rows
    }
    matrix = np.empty((len(tau_axis), len(epsilon_axis)), dtype=float)
    for i, tau in enumerate(tau_axis):
        for j, epsilon in enumerate(epsilon_axis):
            key = (round(float(tau), 14), round(float(epsilon), 14))
            if key not in lookup:
                raise ValueError(f"missing grid cell tau={tau}, epsilon={epsilon}")
            matrix[i, j] = lookup[key]
    return matrix


def summarize_stratum(
    kappa_bar: float,
    taus: Iterable[float],
    epsilons: Iterable[float],
    *,
    L: float = 1.0,
    atol: float = 1e-9,
) -> tuple[list[dict[str, float]], StratumSummary]:
    if kappa_bar < 1.0:
        raise ValueError("kappa_bar must be at least 1")
    tau_axis = _axis(taus)
    epsilon_axis = _axis(epsilons)
    mu_bar = L / float(kappa_bar)
    rows = run_grid(tau_axis, epsilon_axis, L=L, mu_bar=mu_bar)

    rho = np.asarray([row["rho_star"] for row in rows], dtype=float)
    abs_penalty = np.asarray([row["heterogeneity_penalty"] for row in rows], dtype=float)
    norm_penalty = np.asarray([row["normalized_penalty"] for row in rows], dtype=float)

    abs_idx = int(np.argmax(abs_penalty))
    norm_idx = int(np.argmax(norm_penalty))
    norm_matrix = metric_matrix(rows, tau_axis, epsilon_axis, "normalized_penalty")

    tau_diffs = np.diff(norm_matrix, axis=0)
    epsilon_diffs = np.diff(norm_matrix, axis=1)

    summary = StratumSummary(
        kappa_bar=float(kappa_bar),
        mu_bar=mu_bar,
        cells=len(rows),
        rho_min=float(np.min(rho)),
        rho_max=float(np.max(rho)),
        max_abs_penalty=float(abs_penalty[abs_idx]),
        max_abs_at_tau=float(rows[abs_idx]["tau"]),
        max_abs_at_epsilon=float(rows[abs_idx]["epsilon"]),
        max_normalized_penalty=float(norm_penalty[norm_idx]),
        max_norm_at_tau=float(rows[norm_idx]["tau"]),
        max_norm_at_epsilon=float(rows[norm_idx]["epsilon"]),
        max_tau_monotonicity_diff=float(np.max(tau_diffs)),
        min_epsilon_monotonicity_diff=float(np.min(epsilon_diffs)),
        tau_monotone_nonincreasing=bool(np.all(tau_diffs <= atol)),
        epsilon_monotone_nondecreasing=bool(np.all(epsilon_diffs >= -atol)),
    )
    return rows, summary


def analyze_conditioning_strata(
    kappas: Iterable[float],
    taus: Iterable[float],
    epsilons: Iterable[float],
    *,
    L: float = 1.0,
    atol: float = 1e-9,
) -> tuple[dict[float, list[dict[str, float]]], list[StratumSummary]]:
    all_rows: dict[float, list[dict[str, float]]] = {}
    summaries: list[StratumSummary] = []
    for kappa in kappas:
        rows, summary = summarize_stratum(
            float(kappa), taus, epsilons, L=L, atol=atol
        )
        all_rows[float(kappa)] = rows
        summaries.append(summary)
    return all_rows, summaries
