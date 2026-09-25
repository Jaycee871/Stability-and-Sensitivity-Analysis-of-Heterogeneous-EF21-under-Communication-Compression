#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import subprocess
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ef21_stability.guidelines import analyze_guidelines  # noqa: E402
from ef21_stability.landscape import analyze_conditioning_strata, metric_matrix  # noqa: E402
from ef21_stability.robustness import (  # noqa: E402
    boundary_convergence_table,
    continuous_retention_boundary,
)


def save_heatmap(matrix, taus, epsilons, title, label, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.2, 5.1))
    image = ax.imshow(
        matrix,
        origin="lower",
        aspect="auto",
        extent=[epsilons[0], epsilons[-1], taus[0], taus[-1]],
    )
    ax.set_xlabel(r"Compression error $\epsilon$")
    ax.set_ylabel(r"Heterogeneity ratio $\tau=\mu_2/\mu_1$")
    ax.set_title(title)
    fig.colorbar(image, ax=ax, label=label)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, format="svg", bbox_inches="tight")
    plt.close(fig)


def save_conditioning_comparison(all_rows, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.2, 4.9))
    for kappa, rows in sorted(all_rows.items()):
        tau_min = min(float(row["tau"]) for row in rows)
        selected = sorted(
            (row for row in rows if abs(float(row["tau"]) - tau_min) <= 1e-12),
            key=lambda row: float(row["epsilon"]),
        )
        ax.plot(
            [float(row["epsilon"]) for row in selected],
            [float(row["normalized_penalty"]) for row in selected],
            label=rf"$\bar{{\kappa}}={kappa:g}$",
        )
    ax.set_xlabel(r"Compression error $\epsilon$")
    ax.set_ylabel(r"Normalized heterogeneity penalty $H_{\mathrm{norm}}$")
    ax.set_title("Compression amplifies the relative heterogeneity burden")
    ax.legend()
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, format="svg", bbox_inches="tight")
    plt.close(fig)


def save_retention_boundaries(boundaries, target: float, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.2, 4.9))
    kappas = sorted({float(row.kappa_bar) for row in boundaries})
    for kappa in kappas:
        selected = sorted(
            (
                row
                for row in boundaries
                if float(row.kappa_bar) == kappa
                and abs(float(row.retention_target) - target) <= 1e-12
            ),
            key=lambda row: float(row.epsilon),
        )
        ax.plot(
            [float(row.epsilon) for row in selected],
            [float(row.minimum_tau) for row in selected],
            label=rf"$\bar{{\kappa}}={kappa:g}$",
        )
    ax.set_xlabel(r"Compression error $\epsilon$")
    ax.set_ylabel(r"Minimum heterogeneity ratio $\tau$")
    ax.set_title(f"Minimum heterogeneity ratio for {target:.0%} margin retention")
    ax.set_ylim(0.0, 1.0)
    ax.legend()
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, format="svg", bbox_inches="tight")
    plt.close(fig)


def save_boundary_convergence(records, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.2, 4.9))
    for row in records:
        kappa = float(row["kappa_bar"])
        points = np.asarray([int(value) for value in row["grid_boundaries"]], dtype=int)
        estimates = np.asarray(
            [float(row["grid_boundaries"][str(value)]) for value in points], dtype=float
        )
        ax.plot(points, estimates, marker="o", label=rf"Grid $\bar{{\kappa}}={kappa:g}$")
        ax.axhline(
            float(row["continuous_boundary"]),
            linestyle="--",
            label=rf"Bisection $\bar{{\kappa}}={kappa:g}$",
        )
    ax.set_xscale("log")
    ax.set_xlabel(r"Number of $\tau$ grid points")
    ax.set_ylabel(r"99% retention boundary at $\epsilon=0.95$")
    ax.set_title("Boundary convergence under grid refinement")
    ax.legend(fontsize=8)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, format="svg", bbox_inches="tight")
    plt.close(fig)


def save_root_structure_note(path: Path) -> None:
    text = (
        "Wolfram symbolic audit (kappa_bar = 2, 10, 100):\n"
        "Delta = positive prefactor x P(s, tau),\n"
        "with all 63 coefficients of P strictly positive.\n\n"
        "Therefore, for 0 < s = sqrt(epsilon) < 1 and tau > 0,\n"
        "Delta > 0 and the inherited cubic has three distinct real roots\n"
        "on each audited fixed-conditioning open domain."
    )
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    ax.axis("off")
    ax.text(0.04, 0.92, text, va="top", ha="left", fontsize=12)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, format="svg", bbox_inches="tight")
    plt.close(fig)


def write_key_results(path: Path, summaries, boundary_records) -> None:
    by_kappa = {float(row["kappa_bar"]): row for row in boundary_records}
    rows = []
    for summary in summaries:
        record = summary.to_dict()
        kappa = float(record["kappa_bar"])
        boundary = by_kappa[kappa]
        rows.append(
            {
                "kappa_bar": kappa,
                "max_normalized_penalty": float(record["max_normalized_penalty"]),
                "max_abs_penalty": float(record["max_abs_penalty"]),
                "rho_min": float(record["rho_min"]),
                "rho_max": float(record["rho_max"]),
                "tau_99pct_at_epsilon_095": float(boundary["continuous_boundary"]),
                "full_domain_meets_99pct": bool(boundary["domain_fully_satisfies"]),
            }
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def build_full_regularity_assets(output_dir: Path, points: int) -> None:
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "build_phase19_figures.py"),
            "--points",
            str(points),
            "--output-dir",
            str(output_dir / "phase19_full_regularity"),
        ],
        cwd=ROOT,
        check=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("paper_assets"))
    parser.add_argument("--tau-points", type=int, default=381)
    parser.add_argument("--epsilon-points", type=int, default=189)
    parser.add_argument("--phase19-points", type=int, default=101)
    args = parser.parse_args()

    kappas = (2.0, 10.0, 100.0)
    taus = np.linspace(0.05, 1.0, args.tau_points)
    epsilons = np.linspace(0.01, 0.95, args.epsilon_points)

    all_rows, summaries = analyze_conditioning_strata(kappas, taus, epsilons)
    _, boundaries, _, _ = analyze_guidelines(
        kappas,
        taus,
        epsilons,
        retention_targets=(0.99,),
    )
    boundary_records = boundary_convergence_table(kappas)

    figures = args.output_dir / "figures"
    tables = args.output_dir / "tables"

    primary_rows = all_rows[10.0]
    save_heatmap(
        metric_matrix(primary_rows, taus, epsilons, "rho_star"),
        taus,
        epsilons,
        r"EF$^{21}$ contraction landscape at fixed average conditioning ($\bar{\kappa}=10$)",
        r"Predicted contraction factor $\rho_\star$",
        figures / "figure1_contraction_landscape.svg",
    )
    save_heatmap(
        metric_matrix(primary_rows, taus, epsilons, "normalized_penalty"),
        taus,
        epsilons,
        r"Normalized heterogeneity penalty ($\bar{\kappa}=10$)",
        r"Normalized penalty $H_{\mathrm{norm}}$",
        figures / "figure2_normalized_penalty.svg",
    )
    save_conditioning_comparison(
        all_rows,
        figures / "figure3_conditioning_interaction.svg",
    )
    save_retention_boundaries(
        boundaries,
        0.99,
        figures / "figure4_retention_boundary.svg",
    )
    save_boundary_convergence(
        boundary_records,
        figures / "figure5_boundary_convergence.svg",
    )
    save_root_structure_note(
        figures / "figureS1_symbolic_root_structure.svg",
    )
    write_key_results(
        tables / "table1_key_results.csv",
        summaries,
        boundary_records,
    )

    build_full_regularity_assets(args.output_dir, args.phase19_points)

    manifest = {
        "study": "phase20_integrated_paper_assets",
        "baseline_grid": {
            "tau_points": len(taus),
            "epsilon_points": len(epsilons),
            "kappa_bar": list(kappas),
            "total_cells": len(taus) * len(epsilons) * len(kappas),
        },
        "full_regularity_grid": {
            "tau_L_points": args.phase19_points,
            "tau_mu_points": args.phase19_points,
            "epsilon": 0.95,
            "kappa_bar": list(kappas),
        },
        "figures": [
            "figures/figure1_contraction_landscape.svg",
            "figures/figure2_normalized_penalty.svg",
            "figures/figure3_conditioning_interaction.svg",
            "figures/figure4_retention_boundary.svg",
            "figures/figure5_boundary_convergence.svg",
            "figures/figureS1_symbolic_root_structure.svg",
            "phase19_full_regularity/figure6_mismatch_geometry.svg",
            "phase19_full_regularity/figure7_full_regularity_penalty.svg",
            "phase19_full_regularity/figure8_rate_collapse.svg",
        ],
        "table": "tables/table1_key_results.csv",
        "full_regularity_data": "phase19_full_regularity/phase19_rate_collapse_data.csv",
        "continuous_99pct_boundaries_at_epsilon_095": {
            str(k): continuous_retention_boundary(k).to_dict() for k in kappas
        },
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
