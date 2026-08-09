from __future__ import annotations

import unittest

import numpy as np

from ef21_stability.core import (
    TwoAgentConfig,
    cubic_coefficients,
    empirical_eta_star,
    homogeneous_theorem_rate,
    optimal_contraction_factor,
)
from ef21_stability.full_heterogeneity import (
    FullHeterogeneityConfig,
    analyze_full_config,
    cubic_coefficients_full,
    empirical_eta_star_full,
    optimal_contraction_factor_full,
    regularity_parameters,
    run_full_grid,
)


class Phase11FullHeterogeneityTests(unittest.TestCase):
    def test_equal_smoothness_slice_recovers_phase1_core(self) -> None:
        old = TwoAgentConfig(epsilon=0.73, tau=0.31, L=1.0, mu_bar=0.1)
        new = FullHeterogeneityConfig(
            epsilon=0.73,
            tau_L=1.0,
            tau_mu=0.31,
            L_bar=1.0,
            mu_bar=0.1,
        )
        np.testing.assert_allclose(
            cubic_coefficients_full(new), cubic_coefficients(old), rtol=0.0, atol=1e-14
        )
        self.assertAlmostEqual(
            optimal_contraction_factor_full(new), optimal_contraction_factor(old), places=12
        )
        self.assertAlmostEqual(
            empirical_eta_star_full(new), empirical_eta_star(old), places=14
        )

    def test_homogeneous_corner_recovers_theorem_baseline(self) -> None:
        config = FullHeterogeneityConfig(
            epsilon=0.41, tau_L=1.0, tau_mu=1.0, L_bar=1.0, mu_bar=0.1
        )
        _, rho_h = homogeneous_theorem_rate(0.41, 1.0, 0.1)
        self.assertAlmostEqual(optimal_contraction_factor_full(config), rho_h, places=12)
        result = analyze_full_config(config)
        self.assertAlmostEqual(result["heterogeneity_penalty"], 0.0, places=12)
        self.assertAlmostEqual(result["retention"], 1.0, places=12)
        self.assertAlmostEqual(result["log_alignment_gap"], 0.0, places=14)

    def test_step_size_is_invariant_when_both_averages_are_fixed(self) -> None:
        configs = [
            FullHeterogeneityConfig(0.8, 1.0, 0.2, 1.0, 0.1),
            FullHeterogeneityConfig(0.8, 0.2, 1.0, 1.0, 0.1),
            FullHeterogeneityConfig(0.8, 0.3, 0.7, 1.0, 0.1),
            FullHeterogeneityConfig(0.8, 0.7, 0.3, 1.0, 0.1),
        ]
        values = [empirical_eta_star_full(config) for config in configs]
        for value in values[1:]:
            self.assertAlmostEqual(value, values[0], places=14)

    def test_scale_invariance_of_cubic_is_preserved(self) -> None:
        a = FullHeterogeneityConfig(0.62, 0.35, 0.7, 1.0, 0.1)
        b = FullHeterogeneityConfig(0.62, 0.35, 0.7, 7.0, 0.7)
        np.testing.assert_allclose(
            cubic_coefficients_full(a), cubic_coefficients_full(b), rtol=0.0, atol=1e-14
        )
        self.assertAlmostEqual(
            optimal_contraction_factor_full(a), optimal_contraction_factor_full(b), places=12
        )
        self.assertAlmostEqual(
            empirical_eta_star_full(b), empirical_eta_star_full(a) / 7.0, places=14
        )

    def test_invalid_regularity_region_is_rejected(self) -> None:
        config = FullHeterogeneityConfig(
            epsilon=0.5, tau_L=0.05, tau_mu=1.0, L_bar=1.0, mu_bar=0.5
        )
        L1, L2, mu1, mu2 = regularity_parameters(config)
        self.assertLess(L2, mu2)
        self.assertGreater(L1, mu1)
        with self.assertRaises(ValueError):
            config.validate()

    def test_grid_can_mask_invalid_regularity_cells(self) -> None:
        rows, invalid = run_full_grid(
            tau_Ls=[0.05, 1.0],
            tau_mus=[1.0],
            epsilons=[0.5],
            L_bar=1.0,
            mu_bar=0.5,
            skip_invalid=True,
        )
        self.assertEqual(len(rows), 1)
        self.assertEqual(invalid, 1)
        self.assertAlmostEqual(rows[0]["tau_L"], 1.0)


if __name__ == "__main__":
    unittest.main()
