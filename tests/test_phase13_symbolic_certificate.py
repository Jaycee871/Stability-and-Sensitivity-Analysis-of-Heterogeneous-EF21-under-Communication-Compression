import json
from pathlib import Path
import unittest


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


if __name__ == "__main__":
    unittest.main()
