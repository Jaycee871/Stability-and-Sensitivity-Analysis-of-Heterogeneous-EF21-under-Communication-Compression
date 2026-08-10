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

from ef21_stability.full_heterogeneity import (  # noqa: E402
    FullHeterogeneityConfig,
    analyze_full_config,
)
from ef21_stability.structure import (  # noqa: E402
    mismatch_gap_closed_form,
)


def evaluate_surface(
    *,
    kappa: float,
    epsilon: float,
    tau_min: float,
    points: int,
    L_bar: float = 1.0,
) -> dict[str, object]:
    taus = np.linspace(tau_min, 1.0, points)
    gap = np.full((points, points), np.nan, dtype=float)
    penalty = np.full((points, points), np.nan, dtype=float)
    rho = np.full((points, points), np.nan, dtype=float)
    valid = np.zeros((points, points), dtype=bool)
    records: list[dict[str, float]] = []

    mu_bar = L_bar / kappa
    for i, tau_mu in enumerate(taus):
        for j, tau_L in enumerate(taus):
            config = FullHeterogeneityConfig(
                epsilon=epsilon,
                tau_L=float(tau_L),
                tau_mu=float(tau_mu),
                L_bar=L_bar,
                mu_bar=mu_bar,
            )
            try:
                row = analyze_full_config(config)
            except ValueError:
                continue

            g = mismatch_gap_closed_form(float(tau_L), float(tau_mu), kappa)
            gap[i, j] = g
            penalty[i, j] = row["normalized_penalty"]
            rho[i, j] = row["rho_star"]
            valid[i, j] = True
            records.append(
                {
                    "kappa_bar": float(kappa),
                    "epsilon": float(epsilon),
                    "tau_L": float(tau_L),
                    "tau_mu": float(tau_mu),
                    "K1_minus_K2": float(g),
                    "rho_star": float(row["rho_star"]),
                    "rho_homogeneous": float(row["rho_homogeneous"]),
                    "normalized_penalty": float(row["normalized_penalty"]),
                }
            )

    return {
        "taus": taus,
        "gap": gap,
        "penalty": penalty,
        "rho": rho,
        "valid": valid,
        "records": records,
    }


def save_heatmap(
    values: np.ndarray,
    taus: np.ndarray,
    path: Path,
    *,
    title: str,
    colorbar_label: str,
) -> None:
    fig, ax = plt.subplots(figsize=(6.4, 5.2))
    image = ax.imshow(
        values,
        origin="lower",
        extent=[taus[0], taus[-1], taus[0], taus[-1]],
        aspect="equal",
        interpolation="nearest",
    )
    ax.plot([taus[0], 1.0], [taus[0], 1.0], linestyle="--", linewidth=1.5)
    ax.set_xlabel(r"Smoothness ratio $\tau_L=L_2/L_1$")
    ax.set_ylabel(r"Strong-convexity ratio $\tau_\mu=\mu_2/\mu_1$")
    ax.set_title(title)
    cbar = fig.colorbar(image, ax=ax)
    cbar.set_label(colorbar_label)
    fig.tight_layout()
    fig.savefig(path, format="svg", bbox_inches="tight")
    plt.close(fig)


def save_rate_collapse(
    surfaces: dict[float, dict[str, object]],
    path: Path,
) -> None:
    fig, ax = plt.subplots(figsize=(6.6, 5.0))
    for kappa, surface in surfaces.items():
        records = surface["records"]
        x = np.array([row["K1_minus_K2"] for row in records], dtype=float)
        y = np.array([row["normalized_penalty"] for row in records], dtype=float)
        order = np.argsort(x)
        ax.scatter(x[order], y[order], s=7, alpha=0.18, label=rf"$\bar\kappa={kappa:g}$")

    ax.set_xlabel(r"Mismatch coordinate $K_1-K_2$")
    ax.set_ylabel("Normalized contraction penalty")
    ax.set_title(r"Two-dimensional heterogeneity collapses onto $K_1-K_2$")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, format="svg", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--points", type=int, default=101)
    parser.add_argument("--tau-min", type=float, default=0.05)
    parser.add_argument("--epsilon", type=float, default=0.95)
    parser.add_argument("--focus-kappa", type=float, default=10.0)
    parser.add_argument(
        "--output-dir", type=Path, default=Path("paper_assets/phase19_full_regularity")
    )
    args = parser.parse_args()

    if args.points < 5:
        raise ValueError("points must be at least 5")
    if not (0.0 < args.tau_min <= 1.0):
        raise ValueError("tau-min must lie in (0,1]")
    if not (0.0 < args.epsilon < 1.0):
        raise ValueError("epsilon must lie in (0,1)")

    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)

    kappas = (2.0, 10.0, 100.0)
    surfaces = {
        kappa: evaluate_surface(
            kappa=kappa,
            epsilon=args.epsilon,
            tau_min=args.tau_min,
            points=args.points,
        )
        for kappa in kappas
    }

    focus = surfaces[args.focus_kappa]
    taus = focus["taus"]
    save_heatmap(
        focus["gap"],
        taus,
        out / "figure6_mismatch_geometry.svg",
        title=rf"Regularity mismatch geometry ($\bar\kappa={args.focus_kappa:g}$)",
        colorbar_label=r"$K_1-K_2$",
    )
    save_heatmap(
        focus["penalty"],
        taus,
        out / "figure7_full_regularity_penalty.svg",
        title=rf"Full-regularity contraction penalty ($\bar\kappa={args.focus_kappa:g}$, $\epsilon={args.epsilon:g}$)",
        colorbar_label="Normalized contraction penalty",
    )
    save_rate_collapse(surfaces, out / "figure8_rate_collapse.svg")

    csv_path = out / "phase19_rate_collapse_data.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "kappa_bar",
                "epsilon",
                "tau_L",
                "tau_mu",
                "K1_minus_K2",
                "rho_star",
                "rho_homogeneous",
                "normalized_penalty",
            ],
        )
        writer.writeheader()
        for kappa in kappas:
            writer.writerows(surfaces[kappa]["records"])

    summary = {
        "phase": 19,
        "study": "full_regularity_publication_figures",
        "epsilon": args.epsilon,
        "tau_range": [args.tau_min, 1.0],
        "points_per_axis": args.points,
        "focus_kappa": args.focus_kappa,
        "figures": [
            "figure6_mismatch_geometry.svg",
            "figure7_full_regularity_penalty.svg",
            "figure8_rate_collapse.svg",
        ],
        "strata": [],
        "interpretation": (
            "Figure 6 visualizes the exact nonnegative mismatch valley on tau_L=tau_mu. "
            "Figure 7 shows the corresponding zero-penalty aligned valley in the inherited cubic prediction. "
            "Figure 8 tests the structural reduction by plotting the rate penalty against K1-K2; "
            "at fixed kappa_bar and epsilon, two-dimensional ratio pairs collapse onto the single mismatch coordinate."
        ),
        "guardrail": (
            "These figures visualize the inherited Empirical Law 4.3 under the controlled parameterization. "
            "They do not constitute an independent proof that the empirical law is a general EF21 convergence theorem."
        ),
    }

    for kappa in kappas:
        surface = surfaces[kappa]
        records = surface["records"]
        diagonal = [
            row for row in records if abs(row["tau_L"] - row["tau_mu"]) <= 1e-14
        ]
        max_diag_penalty = max(abs(row["normalized_penalty"]) for row in diagonal)
        summary["strata"].append(
            {
                "kappa_bar": kappa,
                "valid_ratio_pairs": int(np.sum(surface["valid"])),
                "invalid_ratio_pairs": int(surface["valid"].size - np.sum(surface["valid"])),
                "max_K1_minus_K2": float(np.nanmax(surface["gap"])),
                "max_normalized_penalty": float(np.nanmax(surface["penalty"])),
                "max_abs_aligned_normalized_penalty": float(max_diag_penalty),
            }
        )

    (out / "phase19_figure_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
