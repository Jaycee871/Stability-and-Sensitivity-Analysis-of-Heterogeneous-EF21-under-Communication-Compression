import math
import unittest

import numpy as np

from ef21_stability.core import TwoAgentConfig, cubic_coefficients
from ef21_stability.full_heterogeneity import FullHeterogeneityConfig, cubic_coefficients_full
from ef21_stability.structure import (
    admissible_tau_mu_bounds,
    cubic_discriminant_full,
    invariant_k2,
    k1_root_sensitivity,
    mismatch_gap_closed_form,
    regularity_shape_coordinates,
    weighted_shape_variance,
)


class Phase12StructureTests(unittest.TestCase):
    def test_k2_is_fixed_by_average_conditioning(self) -> None:
        for kappa in (2.0, 10.0, 100.0):
            expected = invariant_k2(kappa)
            for tau_L, tau_mu in ((1.0, 0.2), (0.5, 0.5), (0.2, 0.8)):
                config = FullHeterogeneityConfig(
                    epsilon=0.4,
                    tau_L=tau_L,
                    tau_mu=tau_mu,
                    L_bar=1.0,
                    mu_bar=1.0 / kappa,
                )
                try:
                    _, k2 = regularity_shape_coordinates(config)
                except ValueError:
                    continue
                self.assertAlmostEqual(k2, expected, places=13)

    def test_k1_minus_k2_matches_closed_form_and_weighted_variance(self) -> None:
        cases = (
            (2.0, 1.0, 0.05),
            (10.0, 0.05, 0.90),
            (10.0, 0.40, 0.70),
            (100.0, 0.05, 1.0),
            (100.0, 0.25, 0.80),
        )
        for kappa, tau_L, tau_mu in cases:
            config = FullHeterogeneityConfig(
                epsilon=0.35,
                tau_L=tau_L,
                tau_mu=tau_mu,
                L_bar=1.0,
                mu_bar=1.0 / kappa,
            )
            k1, k2 = regularity_shape_coordinates(config)
            gap = k1 - k2
            self.assertGreaterEqual(gap, -1e-14)
            self.assertAlmostEqual(
                gap,
                mismatch_gap_closed_form(tau_L, tau_mu, kappa),
                places=13,
            )
            self.assertAlmostEqual(gap, weighted_shape_variance(config), places=13)

    def test_aligned_heterogeneity_has_exact_homogeneous_cubic(self) -> None:
        for kappa in (2.0, 10.0, 100.0):
            for tau in (0.05, 0.20, 0.55, 1.0):
                for epsilon in (0.05, 0.40, 0.95):
                    full = FullHeterogeneityConfig(
                        epsilon=epsilon,
                        tau_L=tau,
                        tau_mu=tau,
                        L_bar=1.0,
                        mu_bar=1.0 / kappa,
                    )
                    homogeneous = TwoAgentConfig(
                        epsilon=epsilon,
                        tau=1.0,
                        L=1.0,
                        mu_bar=1.0 / kappa,
                    )
                    np.testing.assert_allclose(
                        cubic_coefficients_full(full),
                        cubic_coefficients(homogeneous),
                        rtol=0.0,
                        atol=2e-13,
                    )
                    k1, k2 = regularity_shape_coordinates(full)
                    self.assertAlmostEqual(k1, k2, places=13)
                    self.assertAlmostEqual(
                        mismatch_gap_closed_form(tau, tau, kappa), 0.0, places=15
                    )

    def test_admissibility_boundary_matches_worker_regularities(self) -> None:
        lower, upper = admissible_tau_mu_bounds(0.05, 2.0)
        self.assertAlmostEqual(lower, 0.0, places=15)
        self.assertAlmostEqual(upper, 2.0 * 0.05 / (1.0 - 0.05), places=15)

        lower, upper = admissible_tau_mu_bounds(0.05, 10.0)
        self.assertAlmostEqual(lower, 0.0, places=15)
        self.assertAlmostEqual(upper, 10.0 * 0.05 / (1.0 - 9.0 * 0.05), places=15)

        lower, upper = admissible_tau_mu_bounds(0.05, 100.0)
        self.assertAlmostEqual(lower, 0.0, places=15)
        self.assertAlmostEqual(upper, 1.0, places=15)

    def test_sampled_root_structure_gives_positive_k1_sensitivity(self) -> None:
        cases = (
            (2.0, 1.0, 0.05, 0.95),
            (10.0, 0.05, 0.90, 0.95),
            (10.0, 0.40, 0.70, 0.50),
            (100.0, 0.05, 1.0, 0.95),
            (100.0, 0.50, 0.50, 0.20),
        )
        for kappa, tau_L, tau_mu, epsilon in cases:
            config = FullHeterogeneityConfig(
                epsilon=epsilon,
                tau_L=tau_L,
                tau_mu=tau_mu,
                L_bar=1.0,
                mu_bar=1.0 / kappa,
            )
            self.assertGreater(cubic_discriminant_full(config), 0.0)
            self.assertGreater(k1_root_sensitivity(config), 0.0)


if __name__ == "__main__":
    unittest.main()
