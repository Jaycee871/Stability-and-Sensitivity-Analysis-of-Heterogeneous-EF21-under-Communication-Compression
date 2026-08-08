#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ef21_stability.guidelines import analyze_guidelines  # noqa: E402


def write_csv(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not records:
        raise ValueError("cannot write an empty CSV")
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)


def save_boundary_plot(boundaries, selected_target: float, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.4, 5.0))
    kappas = sorted({row.kappa_bar for row in boundaries})
    for kappa in kappas:
        selected = sorted(
            (
                row
                for row in boundaries
                if row.kappa_bar == kappa
                and abs(row.retention_target - selected_target) <= 1e-12
            ),
            key=lambda row: row.epsilon,
        )
        ax.plot(
            [row.epsilon for row in selected],
            [row.minimum_tau for row in selected],
            label=f"kappa_bar={kappa:g}",
        )
    ax.set_xlabel("compression error epsilon")
    ax.set_ylabel("minimum tau retaining target margin")
    ax.set_title(f"EF21 heterogeneity guideline: {selected_target:.0%} margin retention")
    ax.set_ylim(0.0, 1.0)
    ax.legend()
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, format="svg", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase3"))
    parser.add_argument("--figure-dir", type=Path, default=Path("figures/phase3"))
    parser.add_argument("--tau-min", type=float, default=0.05)
    parser.add_argument("--tau-points", type=int, default=381)
    parser.add_argument("--epsilon-min", type=float, default=0.01)
    parser.add_argument("--epsilon-max", type=float, default=0.95)
    parser.add_argument("--epsilon-points", type=int, default=189)
    parser.add_argument("--kappas", type=float, nargs="+", default=[2.0, 10.0, 100.0])
    parser.add_argument(
        "--retention-targets", type=float, nargs="+", default=[0.99, 0.98, 0.95]
    )
    args = parser.parse_args()

    taus = np.linspace(args.tau_min, 1.0, args.tau_points)
    epsilons = np.linspace(args.epsilon_min, args.epsilon_max, args.epsilon_points)

    all_rows, boundaries, amplification, slow_regions = analyze_guidelines(
        args.kappas,
        taus,
        epsilons,
        retention_targets=args.retention_targets,
    )

    boundary_records = [row.to_dict() for row in boundaries]
    amplification_records = [row.to_dict() for row in amplification]
    slow_records = [row.to_dict() for row in slow_regions]

    # Report a compact table at interpretable compression levels that are
    # represented exactly on the default 0.005 epsilon grid.
    selected_epsilons = [0.05, 0.20, 0.50, 0.80, 0.95]
    selected_records = [
        row.to_dict()
        for row in boundaries
        if any(abs(row.epsilon - value) <= 1e-12 for value in selected_epsilons)
    ]

    payload = {
        "study": "phase3_interaction_and_guidelines",
        "parameterization": {
            "n": 2,
            "L": 1.0,
            "tau_min": float(taus[0]),
            "tau_max": float(taus[-1]),
            "tau_points": len(taus),
            "epsilon_min": float(epsilons[0]),
            "epsilon_max": float(epsilons[-1]),
            "epsilon_points": len(epsilons),
            "kappa_bar": [float(value) for value in args.kappas],
            "retention_targets": [float(value) for value in args.retention_targets],
            "cells_per_stratum": len(taus) * len(epsilons),
            "total_cells": len(args.kappas) * len(taus) * len(epsilons),
        },
        "definition": {
            "normalized_penalty": "(rho_star-rho_homogeneous)/(1-rho_homogeneous)",
            "margin_retention": "(1-rho_star)/(1-rho_homogeneous) = 1-normalized_penalty",
            "guideline": "minimum studied tau retaining at least the target fraction of homogeneous contraction margin",
        },
        "compression_amplification_at_tau_min": amplification_records,
        "slow_region_summary": slow_records,
        "selected_guideline_boundaries": selected_records,
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "phase3_summary.json").write_text(
        json.dumps(payload, indent=2) + "\n"
    )
    write_csv(args.output_dir / "guideline_boundaries.csv", boundary_records)
    write_csv(args.output_dir / "selected_guidelines.csv", selected_records)
    write_csv(args.output_dir / "compression_amplification.csv", amplification_records)
    write_csv(args.output_dir / "slow_regions.csv", slow_records)

    save_boundary_plot(
        boundaries,
        selected_target=max(args.retention_targets),
        path=args.figure_dir / "retention_boundary_99pct.svg",
    )

    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
