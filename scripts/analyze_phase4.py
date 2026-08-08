#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ef21_stability.robustness import (  # noqa: E402
    boundary_convergence_table,
    paired_offgrid_validation,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pairs", type=int, default=20_000)
    parser.add_argument("--seed", type=int, default=20_260_809)
    parser.add_argument("--output", type=Path, default=Path("results/phase4_summary.json"))
    args = parser.parse_args()

    kappas = (2.0, 10.0, 100.0)
    offgrid = [
        paired_offgrid_validation(kappa, pairs=args.pairs, seed=args.seed).to_dict()
        for kappa in kappas
    ]
    boundaries = boundary_convergence_table(kappas)

    report = {
        "study": "phase4_robustness_and_symbolic_structure",
        "audited_domain": {
            "tau": [0.05, 1.0],
            "epsilon": [0.01, 0.95],
            "kappa_bar": list(kappas),
        },
        "offgrid_validation": offgrid,
        "boundary_convergence": boundaries,
        "symbolic_cross_check": {
            "engine": "Wolfram Language 15.0.1 for Linux x86 (64-bit) (July 2, 2026)",
            "scale_invariance_K1_K2": True,
            "homogeneous_K1_K2": "((L-mu_bar)/(L+mu_bar))^2",
            "discriminant_positive_on_open_domain_for_tested_strata": True,
            "tested_kappa_bar": list(kappas),
            "interpretation": "For each tested conditioning stratum, the factored cubic discriminant is a positive prefactor times a bivariate polynomial with strictly positive coefficients for 0<s=sqrt(epsilon)<1 and tau>0.",
        },
        "guardrail": "All monotonicity and retention claims remain computational statements on the audited domain. The discriminant sign statement is an analytic symbolic result for the three fixed conditioning strata only.",
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
