from pathlib import Path
import sys
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ef21_stability.guidelines import (  # noqa: E402
    analyze_guidelines,
    compression_amplification,
    guideline_boundaries,
    retained_margin,
)
from ef21_stability.landscape import summarize_stratum  # noqa: E402


class GuidelineTests(unittest.TestCase):
    def test_retained_margin_identity(self):
        rows, _ = summarize_stratum(
            10.0,
            [0.05, 0.5, 1.0],
            [0.2, 0.5],
        )
        for row in rows:
            self.assertAlmostEqual(
                retained_margin(row),
                1.0 - row["normalized_penalty"],
                places=13,
            )

    def test_99pct_boundary_at_heavy_compression(self):
        taus = np.linspace(0.05, 1.0, 381)
        epsilons = [0.94, 0.95]
        expected = {2.0: 0.4100, 10.0: 0.1800, 100.0: 0.0500}
        for kappa, target_tau in expected.items():
            rows, _ = summarize_stratum(kappa, taus, epsilons)
            boundaries = guideline_boundaries(
                rows,
                taus,
                epsilons,
                kappa_bar=kappa,
                retention_targets=[0.99],
            )
            boundary = next(row for row in boundaries if abs(row.epsilon - 0.95) < 1e-12)
            self.assertAlmostEqual(boundary.minimum_tau, target_tau, places=12)

    def test_98pct_boundary_is_less_restrictive_than_99pct(self):
        taus = np.linspace(0.05, 1.0, 381)
        epsilons = [0.20, 0.50, 0.95]
        rows, _ = summarize_stratum(2.0, taus, epsilons)
        boundaries = guideline_boundaries(
            rows,
            taus,
            epsilons,
            kappa_bar=2.0,
            retention_targets=[0.99, 0.98],
        )
        by_key = {
            (row.retention_target, row.epsilon): row.minimum_tau for row in boundaries
        }
        for epsilon in epsilons:
            self.assertLessEqual(by_key[(0.98, epsilon)], by_key[(0.99, epsilon)])

    def test_compression_amplifies_normalized_heterogeneity_penalty(self):
        taus = [0.05, 0.50, 1.0]
        epsilons = [0.01, 0.95]
        expected_ratios = {
            2.0: 3.841472865355666,
            10.0: 3.1196789225846735,
            100.0: 3.032856014084366,
        }
        for kappa, expected in expected_ratios.items():
            rows, _ = summarize_stratum(kappa, taus, epsilons)
            result = compression_amplification(
                rows,
                taus,
                epsilons,
                kappa_bar=kappa,
                tau=0.05,
                epsilon_low=0.01,
                epsilon_high=0.95,
            )
            self.assertGreater(result.absolute_increase, 0.0)
            self.assertAlmostEqual(result.ratio, expected, places=10)

    def test_phase3_smoke_analysis(self):
        taus = np.linspace(0.05, 1.0, 21)
        epsilons = np.linspace(0.01, 0.95, 21)
        all_rows, boundaries, amplification, slow_regions = analyze_guidelines(
            [2.0, 10.0, 100.0],
            taus,
            epsilons,
            retention_targets=[0.99, 0.98, 0.95],
        )
        self.assertEqual(set(all_rows), {2.0, 10.0, 100.0})
        self.assertEqual(len(boundaries), 3 * 3 * len(epsilons))
        self.assertEqual(len(amplification), 3)
        self.assertEqual(len(slow_regions), 3)


if __name__ == "__main__":
    unittest.main()
