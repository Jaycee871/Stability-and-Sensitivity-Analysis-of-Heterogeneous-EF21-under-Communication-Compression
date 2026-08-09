#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ef21_stability.full_heterogeneity import run_full_grid  # noqa: E402


def compact_row(row: dict[str, float]) -> dict[str, float]:
    keys = (
        "epsilon",
        "tau_L",
        "tau_mu",
        "kappa_bar",
        "L1",
        "L2",
        "mu1",
        "mu2",
        "eta_star",
        "rho_star",
        "rho_homogeneous",
        "heterogeneity_penalty",
        "normalized_penalty",
        "retention",
        "regularity_margin",
        "log_alignment_gap",
    )
    return {key: row[key] for key in keys}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tau-l-points", type=int, default=31)
    parser.add_argument("--tau-mu-points", type=int, default=31)
    parser.add_argument("--epsilon-points", type=int, default=95)
    parser.add_argument("--tau-min", type=float, default=0.05)
    parser.add_argument("--epsilon-min", type=float, default=0.01)
    parser.add_argument("--epsilon-max", type=float, default=0.95)
    parser.add_argument("--L-bar", type=float, default=1.0)
    parser.add_argument("--output-dir", type=Path, default=Path("results/phase11"))
    args = parser.parse_args()

    if args.tau_l_points < 2 or args.tau_mu_points < 2 or args.epsilon_points < 2:
        raise ValueError("all grid dimensions require at least two points")
    if not (0.0 < args.tau_min <= 1.0):
        raise ValueError("tau-min must lie in (0,1]")
    if not (0.0 < args.epsilon_min < args.epsilon_max < 1.0):
        raise ValueError("require 0 < epsilon-min < epsilon-max < 1")

    tau_Ls = np.linspace(args.tau_min, 1.0, args.tau_l_points)
    tau_mus = np.linspace(args.tau_min, 1.0, args.tau_mu_points)
    epsilons = np.linspace(args.epsilon_min, args.epsilon_max, args.epsilon_points)
    kappas = (2.0, 10.0, 100.0)

    all_rows: list[dict[str, float]] = []
    strata: list[dict[str, object]] = []
    attempted_per_stratum = len(tau_Ls) * len(tau_mus) * len(epsilons)

    for kappa in kappas:
        mu_bar = args.L_bar / kappa
        rows, invalid = run_full_grid(
            tau_Ls=tau_Ls,
            tau_mus=tau_mus,
            epsilons=epsilons,
            L_bar=args.L_bar,
            mu_bar=mu_bar,
            skip_invalid=True,
        )
        all_rows.extend(rows)

        if not rows:
            raise RuntimeError(f"no valid Phase 11 cells for kappa_bar={kappa}")

        min_penalty = min(rows, key=lambda row: row["normalized_penalty"])
        max_penalty = max(rows, key=lambda row: row["normalized_penalty"])
        slowest = max(rows, key=lambda row: row["rho_star"])
        strata.append(
            {
                "kappa_bar": kappa,
                "attempted_cells": attempted_per_stratum,
                "valid_cells": len(rows),
                "invalid_regularity_cells": invalid,
                "valid_fraction": len(rows) / attempted_per_stratum,
                "normalized_penalty_range": [
                    min_penalty["normalized_penalty"],
                    max_penalty["normalized_penalty"],
                ],
                "minimum_penalty_location": {
                    "tau_L": min_penalty["tau_L"],
                    "tau_mu": min_penalty["tau_mu"],
                    "epsilon": min_penalty["epsilon"],
                    "rho_star": min_penalty["rho_star"],
                },
                "maximum_penalty_location": {
                    "tau_L": max_penalty["tau_L"],
                    "tau_mu": max_penalty["tau_mu"],
                    "epsilon": max_penalty["epsilon"],
                    "rho_star": max_penalty["rho_star"],
                },
                "slowest_location": {
                    "tau_L": slowest["tau_L"],
                    "tau_mu": slowest["tau_mu"],
                    "epsilon": slowest["epsilon"],
                    "rho_star": slowest["rho_star"],
                },
            }
        )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = args.output_dir / "phase11_full_grid.csv"
    fieldnames = list(compact_row(all_rows[0]).keys())
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in all_rows:
            writer.writerow(compact_row(row))

    report = {
        "phase": 11,
        "study": "controlled_full_heterogeneous_regularity_extension",
        "parameterization": {
            "tau_L": "L2/L1",
            "tau_mu": "mu2/mu1",
            "L_bar": "(L1+L2)/2 held fixed",
            "mu_bar": "(mu1+mu2)/2 held fixed within each conditioning stratum",
            "kappa_bar": "L_bar/mu_bar",
        },
        "audited_grid": {
            "tau_L": [float(tau_Ls[0]), float(tau_Ls[-1]), len(tau_Ls)],
            "tau_mu": [float(tau_mus[0]), float(tau_mus[-1]), len(tau_mus)],
            "epsilon": [float(epsilons[0]), float(epsilons[-1]), len(epsilons)],
            "kappa_bar": list(kappas),
        },
        "attempted_cells": attempted_per_stratum * len(kappas),
        "valid_cells": len(all_rows),
        "invalid_regularity_cells": attempted_per_stratum * len(kappas) - len(all_rows),
        "strata": strata,
        "guardrail": (
            "Phase 11 extends the inherited n=2 Empirical Law 4.3 parameter space by "
            "varying L_i and mu_i independently at fixed arithmetic means. Results are "
            "computational characterizations on the audited admissible domain, not a proof "
            "of Empirical Law 4.3 or a new general EF21 convergence theorem."
        ),
    }
    summary_path = args.output_dir / "phase11_summary.json"
    summary_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
