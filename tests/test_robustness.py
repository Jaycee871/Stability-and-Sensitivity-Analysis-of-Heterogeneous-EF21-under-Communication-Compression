from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ef21_stability.robustness import (  # noqa: E402
    boundary_convergence_table,
    continuous_retention_boundary,
    paired_offgrid_validation,
)


class RobustnessTests(unittest.TestCase):
    def test_offgrid_monotonicity_smoke(self):
        for kappa in (2.0, 10.0, 100.0):
            summary = paired_offgrid_validation(kappa, pairs=200, seed=20260809)
            self.assertLessEqual(summary.max_tau_monotonicity_violation, 1e-8)
            self.assertLessEqual(summary.max_epsilon_monotonicity_violation, 1e-8)
            self.assertLessEqual(summary.max_root_residual, 1e-12)

    def test_continuous_99pct_boundaries(self):
        expected = {
            2.0: 0.4076217486520454,
            10.0: 0.17985615951449502,
        }
        for kappa, target in expected.items():
            result = continuous_retention_boundary(kappa)
            self.assertFalse(result.domain_fully_satisfies)
            self.assertAlmostEqual(result.continuous_boundary, target, places=8)

        result = continuous_retention_boundary(100.0)
        self.assertTrue(result.domain_fully_satisfies)
        self.assertEqual(result.continuous_boundary, 0.05)

    def test_grid_boundaries_converge_toward_bisection_reference(self):
        table = boundary_convergence_table(
            resolutions=(96, 381, 1521),
        )
        by_kappa = {row["kappa_bar"]: row for row in table}

        row2 = by_kappa[2.0]
        errors2 = [
            abs(float(value) - float(row2["continuous_boundary"]))
            for value in row2["grid_boundaries"].values()
        ]
        self.assertLessEqual(errors2[-1], errors2[0])
        self.assertLess(errors2[-1], 1e-3)

        row10 = by_kappa[10.0]
        self.assertAlmostEqual(
            float(row10["grid_boundaries"]["1521"]), 0.18, places=12
        )

        row100 = by_kappa[100.0]
        self.assertTrue(row100["domain_fully_satisfies"])
        self.assertTrue(
            all(float(value) == 0.05 for value in row100["grid_boundaries"].values())
        )


if __name__ == "__main__":
    unittest.main()
