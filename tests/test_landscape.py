from pathlib import Path
import sys
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ef21_stability.core import TwoAgentConfig, analyze_config  # noqa: E402
from ef21_stability.landscape import analyze_conditioning_strata, summarize_stratum  # noqa: E402


class LandscapeTests(unittest.TestCase):
    def test_normalized_penalty_monotonicity_on_coarse_grid(self):
        taus = np.linspace(0.05, 1.0, 20)
        epsilons = np.linspace(0.05, 0.95, 19)
        for kappa in (2.0, 10.0, 100.0):
            _, summary = summarize_stratum(kappa, taus, epsilons)
            self.assertTrue(summary.tau_monotone_nonincreasing)
            self.assertTrue(summary.epsilon_monotone_nondecreasing)

    def test_conditioning_order_of_relative_penalty(self):
        rows = [
            analyze_config(TwoAgentConfig(0.95, 0.05, L=1.0, mu_bar=1.0 / kappa))
            for kappa in (2.0, 10.0, 100.0)
        ]
        penalties = [row["normalized_penalty"] for row in rows]
        self.assertGreater(penalties[0], penalties[1])
        self.assertGreater(penalties[1], penalties[2])

    def test_extreme_cell_regression_values(self):
        expected = {
            2.0: 0.050735736426212354,
            10.0: 0.016990131036983214,
            100.0: 0.0020054918884285923,
        }
        for kappa, target in expected.items():
            row = analyze_config(
                TwoAgentConfig(0.95, 0.05, L=1.0, mu_bar=1.0 / kappa)
            )
            self.assertAlmostEqual(row["normalized_penalty"], target, places=10)

    def test_three_strata_are_audited_together(self):
        taus = np.linspace(0.05, 1.0, 8)
        epsilons = np.linspace(0.05, 0.95, 7)
        all_rows, summaries = analyze_conditioning_strata(
            (2.0, 10.0, 100.0), taus, epsilons
        )
        self.assertEqual(set(all_rows), {2.0, 10.0, 100.0})
        self.assertEqual([summary.cells for summary in summaries], [56, 56, 56])


if __name__ == "__main__":
    unittest.main()
