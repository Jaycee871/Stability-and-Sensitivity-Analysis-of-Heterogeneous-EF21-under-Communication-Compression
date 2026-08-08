#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ef21_stability.core import (  # noqa: E402
    TwoAgentConfig,
    cubic_coefficients,
    homogeneous_theorem_rate,
    optimal_contraction_factor,
)


def cubic_discriminant(coeffs: np.ndarray) -> float:
    a, b, c, d = [float(x) for x in coeffs]
    return (
        18.0 * a * b * c * d
        - 4.0 * b**3 * d
        + b**2 * c**2
        - 4.0 * a * c**3
        - 27.0 * a**2 * d**2
    )


def close(name: str, actual: float, expected: float, *, atol: float, rtol: float) -> None:
    if not np.isclose(actual, expected, atol=atol, rtol=rtol):
        raise AssertionError(
            f"{name}: Wolfram={actual:.17g}, Python={expected:.17g}, "
            f"abs diff={abs(actual - expected):.3e}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        type=Path,
        nargs="?",
        default=Path("wolfram/outputs/wolfram_reference.json"),
    )
    parser.add_argument("--atol", type=float, default=2e-10)
    parser.add_argument("--rtol", type=float, default=2e-10)
    args = parser.parse_args()

    payload = json.loads(args.path.read_text())
    cases = payload.get("cases", [])
    if not cases:
        raise ValueError("Wolfram export contains no cases")

    for index, row in enumerate(cases):
        tau = float(row["tau"])
        epsilon = float(row["epsilon"])
        kappa = float(row["kappa_bar"])
        mu_bar = 1.0 / kappa
        cfg = TwoAgentConfig(epsilon=epsilon, tau=tau, L=1.0, mu_bar=mu_bar)

        coeffs = cubic_coefficients(cfg)
        wolfram_coeffs = np.asarray(row["coefficients"], dtype=float)
        if wolfram_coeffs.shape != (4,):
            raise AssertionError(f"case {index}: expected four cubic coefficients")
        if not np.allclose(wolfram_coeffs, coeffs, atol=args.atol, rtol=args.rtol):
            raise AssertionError(
                f"case {index}: coefficient mismatch\n"
                f"Wolfram={wolfram_coeffs}\nPython={coeffs}"
            )

        rho = optimal_contraction_factor(cfg)
        _, rho_h = homogeneous_theorem_rate(epsilon, 1.0, mu_bar)
        retention = (1.0 - rho) / (1.0 - rho_h)
        discriminant = cubic_discriminant(coeffs)

        close(f"case {index} rho_star", float(row["rho_star"]), rho, atol=args.atol, rtol=args.rtol)
        close(
            f"case {index} rho_homogeneous",
            float(row["rho_homogeneous"]),
            rho_h,
            atol=args.atol,
            rtol=args.rtol,
        )
        close(
            f"case {index} retained_margin",
            float(row["retained_margin"]),
            retention,
            atol=args.atol,
            rtol=args.rtol,
        )
        close(
            f"case {index} discriminant",
            float(row["discriminant"]),
            discriminant,
            atol=max(args.atol, 1e-9),
            rtol=max(args.rtol, 1e-9),
        )

    print(
        f"validated {len(cases)} Wolfram reference cases against the Python implementation"
    )
    print(f"Wolfram engine: {payload.get('version', 'unknown version')}")


if __name__ == "__main__":
    main()
