#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ef21_stability.core import run_grid  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("outputs/stability_grid.csv"))
    parser.add_argument("--tau-min", type=float, default=0.05)
    parser.add_argument("--tau-points", type=int, default=96)
    parser.add_argument("--epsilon-min", type=float, default=0.01)
    parser.add_argument("--epsilon-max", type=float, default=0.95)
    parser.add_argument("--epsilon-points", type=int, default=95)
    parser.add_argument("--L", type=float, default=1.0)
    parser.add_argument("--mu-bar", type=float, default=0.1)
    args = parser.parse_args()

    taus = np.linspace(args.tau_min, 1.0, args.tau_points)
    epsilons = np.linspace(args.epsilon_min, args.epsilon_max, args.epsilon_points)
    rows = run_grid(taus, epsilons, L=args.L, mu_bar=args.mu_bar)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    penalties = [row["heterogeneity_penalty"] for row in rows]
    normalized = [row["normalized_penalty"] for row in rows]
    rhos = [row["rho_star"] for row in rows]
    print(f"wrote {len(rows)} cells to {args.output}")
    print(f"rho_star range: {min(rhos):.12f} .. {max(rhos):.12f}")
    print(f"max heterogeneity penalty: {max(penalties):.12e}")
    print(f"max normalized penalty: {max(normalized):.6%}")


if __name__ == "__main__":
    main()
