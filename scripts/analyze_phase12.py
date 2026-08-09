#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ef21_stability.full_heterogeneity import (  # noqa: E402
    FullHeterogeneityConfig,
    analyze_full_config,
    cubic_coefficients_full,
)
from ef21_stability.structure import (  # noqa: E402
    admissible_tau_mu_bounds,
    cubic_discriminant_full,
    invariant_k2,
    mismatch_gap_closed_form,
    regularity_shape_coordinates,
    weighted_shape_variance,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tau-points", type=int, default=31)
    parser.add_argument("--epsilon-points", type=int, default=95)
    parser.add_argument("--tau-min", type=float, default=0.05)
    parser.add_argument("--epsilon-min", type=float, default=0.01)
    parser.add_argument("--epsilon-max", type=float, default=0.95)
    parser.add_argument("--L-bar", type=float, default=1.0)
    parser.add_argument(
        "--output", type=Path, default=Path("results/phase12_summary.json")
    )
    args = parser.parse_args()

    if args.tau_points < 2 or args.epsilon_points < 2:
        raise ValueError("grid dimensions require at least two points")
    if not (0.0 < args.tau_min <= 1.0):
        raise ValueError("tau-min must lie in (0,1]")
    if not (0.0 < args.epsilon_min < args.epsilon_max < 1.0):
        raise ValueError("require 0 < epsilon-min < epsilon-max < 1")

    taus = np.linspace(args.tau_min, 1.0, args.tau_points)
    epsilons = np.linspace(args.epsilon_min, args.epsilon_max, args.epsilon_points)
    kappas = (2.0, 10.0, 100.0)

    strata: list[dict[str, object]] = []
    total_requested = len(taus) * len(taus) * len(epsilons) * len(kappas)
    total_valid = 0

    for kappa in kappas:
        mu_bar = args.L_bar / kappa
        expected_k2 = invariant_k2(kappa)
        attempted = len(taus) * len(taus) * len(epsilons)
        valid = 0
        invalid = 0
        negative_penalties = 0

        max_k2_error = 0.0
        max_gap_identity_error = 0.0
        max_weighted_variance_error = 0.0
        max_aligned_rho_error = 0.0
        min_gap = math.inf
        max_gap = -math.inf
        max_gap_location: dict[str, float] | None = None
        min_discriminant = math.inf
        min_q_prime = math.inf
        min_rho_minus_s = math.inf
        min_k1_sensitivity = math.inf
        max_normalized_penalty = -math.inf
        max_penalty_location: dict[str, float] | None = None

        for tau_L in taus:
            for tau_mu in taus:
                pair_gap_checked = False
                for epsilon in epsilons:
                    config = FullHeterogeneityConfig(
                        epsilon=float(epsilon),
                        tau_L=float(tau_L),
                        tau_mu=float(tau_mu),
                        L_bar=args.L_bar,
                        mu_bar=mu_bar,
                    )
                    try:
                        row = analyze_full_config(config)
                    except ValueError:
                        invalid += 1
                        continue

                    valid += 1
                    k1, k2 = regularity_shape_coordinates(config)
                    gap = k1 - k2
                    closed_gap = mismatch_gap_closed_form(tau_L, tau_mu, kappa)
                    weighted_gap = weighted_shape_variance(config)
                    max_k2_error = max(max_k2_error, abs(k2 - expected_k2))
                    max_gap_identity_error = max(
                        max_gap_identity_error, abs(gap - closed_gap)
                    )
                    max_weighted_variance_error = max(
                        max_weighted_variance_error, abs(gap - weighted_gap)
                    )

                    if math.isclose(tau_L, tau_mu, rel_tol=0.0, abs_tol=1e-14):
                        max_aligned_rho_error = max(
                            max_aligned_rho_error,
                            abs(row["rho_star"] - row["rho_homogeneous"]),
                        )

                    if row["heterogeneity_penalty"] < -1e-10:
                        negative_penalties += 1

                    if not pair_gap_checked:
                        min_gap = min(min_gap, gap)
                        if gap > max_gap:
                            max_gap = gap
                            max_gap_location = {
                                "tau_L": float(tau_L),
                                "tau_mu": float(tau_mu),
                                "K1": float(k1),
                                "K2": float(k2),
                            }
                        pair_gap_checked = True

                    coeffs = cubic_coefficients_full(config)
                    rho = row["rho_star"]
                    s = math.sqrt(epsilon)
                    r = (1.0 - s) ** 2 / (1.0 + s)
                    q_prime = 3.0 * rho * rho + 2.0 * coeffs[1] * rho + coeffs[2]
                    discriminant = cubic_discriminant_full(config)
                    if abs(q_prime) <= 1e-14:
                        sensitivity = math.inf
                    else:
                        sensitivity = r * s * rho * (rho - s) / q_prime

                    min_discriminant = min(min_discriminant, discriminant)
                    min_q_prime = min(min_q_prime, q_prime)
                    min_rho_minus_s = min(min_rho_minus_s, rho - s)
                    min_k1_sensitivity = min(min_k1_sensitivity, sensitivity)

                    if row["normalized_penalty"] > max_normalized_penalty:
                        max_normalized_penalty = row["normalized_penalty"]
                        max_penalty_location = {
                            "tau_L": float(tau_L),
                            "tau_mu": float(tau_mu),
                            "epsilon": float(epsilon),
                            "rho_star": float(rho),
                            "rho_homogeneous": float(row["rho_homogeneous"]),
                        }

        total_valid += valid
        lower_at_tau_min, upper_at_tau_min = admissible_tau_mu_bounds(
            args.tau_min, kappa
        )
        strata.append(
            {
                "kappa_bar": kappa,
                "attempted_cells": attempted,
                "valid_cells": valid,
                "invalid_regularity_cells": invalid,
                "valid_fraction": valid / attempted,
                "K2_invariant": expected_k2,
                "max_abs_K2_invariance_error": max_k2_error,
                "min_K1_minus_K2": min_gap,
                "max_K1_minus_K2": max_gap,
                "max_K1_minus_K2_location": max_gap_location,
                "max_closed_form_gap_error": max_gap_identity_error,
                "max_weighted_variance_identity_error": max_weighted_variance_error,
                "max_aligned_rho_error": max_aligned_rho_error,
                "negative_penalty_cells_below_minus_1e_10": negative_penalties,
                "minimum_cubic_discriminant": min_discriminant,
                "minimum_Qprime_at_selected_root": min_q_prime,
                "minimum_rho_minus_sqrt_epsilon": min_rho_minus_s,
                "minimum_d_rho_d_K1": min_k1_sensitivity,
                "maximum_normalized_penalty": max_normalized_penalty,
                "maximum_normalized_penalty_location": max_penalty_location,
                "tau_mu_admissible_bounds_at_tau_L_min": [
                    lower_at_tau_min,
                    upper_at_tau_min,
                ],
            }
        )

    report = {
        "phase": 12,
        "study": "regularity_mismatch_structure",
        "audited_grid": {
            "tau_L": [float(taus[0]), float(taus[-1]), len(taus)],
            "tau_mu": [float(taus[0]), float(taus[-1]), len(taus)],
            "epsilon": [float(epsilons[0]), float(epsilons[-1]), len(epsilons)],
            "kappa_bar": list(kappas),
        },
        "requested_cells": total_requested,
        "valid_cells": total_valid,
        "invalid_regularity_cells": total_requested - total_valid,
        "exact_identities": {
            "K2": "((kappa_bar-1)/(kappa_bar+1))^2",
            "K1_minus_K2": (
                "4*kappa_bar^2*(tau_L-tau_mu)^2 / "
                "[(kappa_bar+1)^2*(tau_L+kappa_bar*tau_mu+kappa_bar+1)"
                "*(kappa_bar*tau_L*tau_mu+tau_L*tau_mu+"
                "kappa_bar*tau_L+tau_mu)]"
            ),
            "interpretation": (
                "K1-K2 is the Sigma-weighted variance of "
                "q_i=(L_i-mu_i)/(L_i+mu_i). It is nonnegative and vanishes "
                "exactly when the two local condition ratios are aligned."
            ),
        },
        "strata": strata,
        "claim_guardrail": (
            "The K2 invariance, K1-K2 identity, weighted-variance representation, "
            "and aligned-path equality are algebraic properties of the inherited "
            "two-agent Empirical Law 4.3 under the controlled fixed-average "
            "parameterization. Positive root sensitivity and discriminant statements "
            "reported here are numerical audits on the stated grid unless separately "
            "proved symbolically."
        ),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
