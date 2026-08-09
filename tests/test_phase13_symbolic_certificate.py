import json
import math
from pathlib import Path
import unittest

import numpy as np

from ef21_stability.core import TwoAgentConfig, cubic_coefficients, optimal_contraction_factor
from ef21_stability.full_heterogeneity import (
    FullHeterogeneityConfig,
    cubic_coefficients_full,
    optimal_contraction_factor_full,
)


ROOT = Path(__file__).resolve().parents[1]


class Phase13SymbolicCertificateTests(unittest.TestCase):
    def test_symbolic_certificate_preserves_required_proof_results(self) -> None:
        payload = json.loads(
            (ROOT / "results" / "phase13_symbolic_certificate.json").read_text(
                encoding="utf-8"
            )
        )

        self.assertEqual(payload["phase"], 13)
        self.assertTrue(payload["structure_certificate"]["K2_invariant_verified"])
        self.assertTrue(
            payload["structure_certificate"]["K1_minus_K2_closed_form_verified"]
        )

        root = payload["generic_root_certificate"]
        self.assertFalse(root["discriminant_nonpositive_feasible"])
        self.assertFalse(root["nonpositive_root_feasible"])
        self.assertFalse(root["root_at_or_above_one_feasible"])
        self.assertFalse(root["Q_at_one_nonpositive_feasible"])
        self.assertIn("K2*(s-1)^3*s^2", root["Q_at_s"])
        self.assertIn("three distinct real roots", root["root_consequence"])

        sensitivity = payload["sensitivity_certificate"]
        self.assertIn("d rho_star/dK1 > 0", sensitivity["consequence"])
        self.assertIn("Q'(rho_star)", sensitivity["implicit_derivative"])

    def test_guardrail_does_not_promote_empirical_law_to_theorem(self) -> None:
        payload = json.loads(
            (ROOT / "results" / "phase13_symbolic_certificate.json").read_text(
                encoding="utf-8"
            )
        )
        guardrail = payload["guardrail"]
        self.assertIn("does not prove Empirical Law 4.3 itself", guardrail)
        self.assertIn("does not establish a new general EF21 convergence theorem", guardrail)

        doc = (ROOT / "docs" / "phase13_symbolic_root_sensitivity.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("conditional on the inherited Empirical Law 4.3 cubic", doc)
        self.assertIn("does **not** prove the empirical law itself", doc)

    def test_full_heterogeneity_selector_is_literal_largest_real_root(self) -> None:
        cases = (
            (2.0, 1.0, 0.05, 0.95),
            (2.0, 0.40, 0.08, 0.40),
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
            roots = np.roots(cubic_coefficients_full(config))
            self.assertTrue(np.all(np.abs(roots.imag) < 1e-7))
            real = roots.real
            self.assertTrue(np.all(real > 0.0))
            self.assertTrue(np.all(real < 1.0))
            expected = float(np.max(real))
            actual = optimal_contraction_factor_full(config)
            self.assertAlmostEqual(actual, expected, places=13)
            self.assertGreater(actual, math.sqrt(epsilon))

    def test_equal_smoothness_selector_obeys_same_root_contract(self) -> None:
        for kappa in (2.0, 10.0, 100.0):
            for tau in (0.05, 0.30, 1.0):
                config = TwoAgentConfig(
                    epsilon=0.73,
                    tau=tau,
                    L=1.0,
                    mu_bar=1.0 / kappa,
                )
                try:
                    config.validate()
                except ValueError:
                    continue
                roots = np.roots(cubic_coefficients(config))
                self.assertTrue(np.all(np.abs(roots.imag) < 1e-7))
                expected = float(np.max(roots.real))
                self.assertAlmostEqual(
                    optimal_contraction_factor(config), expected, places=13
                )


if __name__ == "__main__":
    unittest.main()
