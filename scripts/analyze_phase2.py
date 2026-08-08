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

from ef21_stability.landscape import (  # noqa: E402
    analyze_conditioning_strata,
    metric_matrix,
)


def write_summary_csv(path: Path, summaries) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = [summary.to_dict() for summary in summaries]
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_slice_csv(path: Path, all_rows, tau_values, epsilon_values) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    records = []
    for kappa, rows in all_rows.items():
        lookup = {
            (round(row["tau"], 12), round(row["epsilon"], 12)): row
            for row in rows
        }
        for tau in tau_values:
            for epsilon in epsilon_values:
                key = (round(float(tau), 12), round(float(epsilon), 12))
                if key not in lookup:
                    continue
                row = lookup[key]
                records.append({
                    "kappa_bar": kappa,
                    "tau": row["tau"],
                    "epsilon": row["epsilon"],
                    "rho_star": row["rho_star"],
                    "rho_homogeneous": row["rho_homogeneous"],
                    "heterogeneity_penalty": row["heterogeneity_penalty"],
                    "normalized_penalty": row["normalized_penalty"],
                })
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)


def save_heatmap(matrix, taus, epsilons, title, label, path) -> None:
    fig, ax = plt.subplots(figsize=(7.4, 5.3))
    image = ax.imshow(
        matrix,
        origin="lower",
        aspect="auto",
        extent=[epsilons[0], epsilons[-1], taus[0], taus[-1]],
    )
    ax.set_xlabel("compression error epsilon")
    ax.set_ylabel("heterogeneity ratio tau = mu2 / mu1")
    ax.set_title(title)
    fig.colorbar(image, ax=ax, label=label)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, format="svg", bbox_inches="tight")
    plt.close(fig)


def save_conditioning_comparison(all_rows, path) -> None:
    fig, ax = plt.subplots(figsize=(7.4, 5.0))
    for kappa, rows in sorted(all_rows.items()):
        tau_min = min(row["tau"] for row in rows)
        selected = sorted(
            (row for row in rows if abs(row["tau"] - tau_min) <= 1e-12),
            key=lambda row: row["epsilon"],
        )
        ax.plot(
            [row["epsilon"] for row in selected],
            [row["normalized_penalty"] for row in selected],
            label=f"kappa_bar={kappa:g}",
        )
    ax.set_xlabel("compression error epsilon")
    ax.set_ylabel("normalized heterogeneity penalty")
    ax.set_title("Conditioning dependence at maximum studied heterogeneity")
    ax.legend()
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, format="svg", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/phase2"))
    parser.add_argument("--figure-dir", type=Path, default=Path("figures/phase2"))
    parser.add_argument("--tau-min", type=float, default=0.05)
    parser.add_argument("--tau-points", type=int, default=96)
    parser.add_argument("--epsilon-min", type=float, default=0.01)
    parser.add_argument("--epsilon-max", type=float, default=0.95)
    parser.add_argument("--epsilon-points", type=int, default=95)
    parser.add_argument("--kappas", type=float, nargs="+", default=[2.0, 10.0, 100.0])
    args = parser.parse_args()

    taus = np.linspace(args.tau_min, 1.0, args.tau_points)
    epsilons = np.linspace(args.epsilon_min, args.epsilon_max, args.epsilon_points)

    all_rows, summaries = analyze_conditioning_strata(
        args.kappas, taus, epsilons
    )

    payload = {
        "study": "phase2_stability_landscape",
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
            "cells_per_stratum": len(taus) * len(epsilons),
            "total_cells": len(args.kappas) * len(taus) * len(epsilons),
        },
        "strata": [summary.to_dict() for summary in summaries],
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "phase2_summary.json").write_text(
        json.dumps(payload, indent=2) + "\n"
    )
    write_summary_csv(args.output_dir / "strata_summary.csv", summaries)

    # These selected values are exactly represented on the default axes.
    slice_taus = [value for value in (0.05, 0.5, 1.0) if np.any(np.isclose(taus, value))]
    slice_eps = [
        value
        for value in (0.05, 0.2, 0.5, 0.8, 0.95)
        if np.any(np.isclose(epsilons, value))
    ]
    write_slice_csv(
        args.output_dir / "sensitivity_slices.csv",
        all_rows,
        slice_taus,
        slice_eps,
    )

    primary_kappa = 10.0 if 10.0 in all_rows else float(args.kappas[0])
    primary_rows = all_rows[primary_kappa]
    save_heatmap(
        metric_matrix(primary_rows, taus, epsilons, "rho_star"),
        taus,
        epsilons,
        f"EF21 contraction landscape (kappa_bar={primary_kappa:g})",
        "rho_star",
        args.figure_dir / "rho_landscape_kappa10.svg",
    )
    save_heatmap(
        metric_matrix(primary_rows, taus, epsilons, "normalized_penalty"),
        taus,
        epsilons,
        f"Normalized heterogeneity penalty (kappa_bar={primary_kappa:g})",
        "normalized penalty",
        args.figure_dir / "normalized_penalty_kappa10.svg",
    )
    save_conditioning_comparison(
        all_rows,
        args.figure_dir / "conditioning_comparison.svg",
    )

    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
