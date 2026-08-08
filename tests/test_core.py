from pathlib import Path
import sys
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ef21_stability.core import (  # noqa: E402
    TwoAgentConfig,
    cubic_coefficients,
    empirical_eta_star,
    fixed_average_mus,
    homogeneous_theorem_rate,
    optimal_contraction_factor,
)


class CoreTests(unittest.TestCase):
    def test_fixed_average_parameterization(self):
        for tau in (1.0, 0.5, 0.1, 0.05):
            mu1, mu2 = fixed_average_mus(tau, 0.1)
            self.assertAlmostEqual((mu1 + mu2) / 2.0, 0.1, places=15)
            self.assertAlmostEqual(mu2 / mu1, tau, places=15)

    def test_eta_is_constant_when_average_curvature_is_fixed(self):
        values = [
            empirical_eta_star(TwoAgentConfig(0.2, tau, L=1.0, mu_bar=0.1))
            for tau in (1.0, 0.5, 0.1, 0.05)
        ]
        self.assertLess(max(values) - min(values), 1e-14)

    def test_homogeneous_limit_matches_theorem_3_1(self):
        for epsilon in (0.05, 0.2, 0.5, 0.8, 0.95):
            cfg = TwoAgentConfig(epsilon, 1.0, L=1.0, mu_bar=0.1)
            rho = optimal_contraction_factor(cfg)
            eta_h, rho_h = homogeneous_theorem_rate(epsilon, 1.0, 0.1)
            self.assertAlmostEqual(rho, rho_h, places=10)
            self.assertAlmostEqual(empirical_eta_star(cfg), eta_h, places=14)

    def test_selected_heterogeneous_cells_have_admissible_roots(self):
        for tau in (0.05, 0.1, 0.2, 0.5, 1.0):
            for epsilon in (0.01, 0.2, 0.5, 0.8, 0.95):
                cfg = TwoAgentConfig(epsilon, tau, L=1.0, mu_bar=0.1)
                rho = optimal_contraction_factor(cfg)
                self.assertGreaterEqual(rho, 0.0)
                self.assertLessEqual(rho, 1.0 + 1e-10)
                self.assertLess(abs(np.polyval(cubic_coefficients(cfg), rho)), 2e-10)

    def test_scale_invariance(self):
        for epsilon in (0.1, 0.5, 0.9):
            for tau in (0.05, 0.3, 0.8):
                base = optimal_contraction_factor(
                    TwoAgentConfig(epsilon, tau, L=1.0, mu_bar=0.1)
                )
                scaled = optimal_contraction_factor(
                    TwoAgentConfig(epsilon, tau, L=7.0, mu_bar=0.7)
                )
                self.assertAlmostEqual(base, scaled, places=11)


if __name__ == "__main__":
    unittest.main()
