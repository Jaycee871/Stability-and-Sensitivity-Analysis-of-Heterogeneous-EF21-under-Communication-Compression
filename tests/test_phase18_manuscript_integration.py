from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "draft.md"
BIB = ROOT / "manuscript" / "references.bib"


class Phase18ManuscriptIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = MANUSCRIPT.read_text(encoding="utf-8")
        cls.lower = cls.text.lower()
        cls.bib = BIB.read_text(encoding="utf-8")

    def test_phase18_or_later_manuscript_preserves_integration(self) -> None:
        match = re.search(r"Working manuscript draft — Phase (\d+)", self.text)
        self.assertIsNotNone(match)
        self.assertGreaterEqual(int(match.group(1)), 18)

    def test_full_regularity_parameterization_is_integrated(self) -> None:
        for token in ("tau_L", "tau_\\mu", "bar\\kappa", "273{,}885", "258,400"):
            self.assertIn(token, self.text)

    def test_n1a_is_framed_as_inherited_interpretation(self) -> None:
        self.assertIn("exact algebraic reinterpretation of the inherited coefficients", self.text)
        self.assertIn("K_1-K_2=\\operatorname{Var}_w(q_i)", self.text)

    def test_n1b_factorization_contains_unique_mismatch_factor(self) -> None:
        self.assertIn("(\\tau_L-\\tau_\\mu)^2", self.text)
        self.assertIn("fixed-average mismatch factorization", self.lower)

    def test_aligned_invariance_is_in_main_results(self) -> None:
        self.assertIn("Proportional heterogeneity is invisible to the inherited cubic", self.text)
        self.assertIn("\\tau_L=\\tau_\\mu", self.text)

    def test_generic_root_sensitivity_is_in_main_results(self) -> None:
        self.assertIn("Regularity mismatch strictly worsens the inherited largest-root prediction", self.text)
        self.assertIn("\\frac{d\\rho^\\star}{dK_1}>0", self.text)
        self.assertIn("conditional on Empirical Law 4.3", self.text)

    def test_absolute_novelty_claims_remain_blocked(self) -> None:
        forbidden = [
            r"\bwe (?:are|provide|give|present|derive|establish|show) the first\b",
            r"\bwe (?:introduce|present|propose|establish|derive|show) (?:a )?novel\b",
            r"\bthis is the first (?:analysis|result|characterization|proof|theorem)\b",
            r"\bno prior work (?:has|had|does|did|provides|derives|shows|establishes)\b",
        ]
        for pattern in forbidden:
            self.assertIsNone(re.search(pattern, self.lower), pattern)

    def test_scope_lint_literal_guardrails_survive(self) -> None:
        required = [
            "does not attempt to prove the full heterogeneous empirical law",
            "not universal convergence thresholds",
            "not proofs of global monotonicity",
            "only for the three fixed conditioning strata",
            "not a direct communication-cost optimum",
        ]
        for phrase in required:
            self.assertIn(phrase, self.lower)

    def test_new_related_work_citations_are_resolved(self) -> None:
        for key in ("richtarik2024reloaded", "gao2023econtrol", "colla2024symmetries"):
            self.assertRegex(self.bib, rf"@[A-Za-z]+\{{{re.escape(key)},")
            self.assertIn(f"[@{key}]", self.text)


if __name__ == "__main__":
    unittest.main()
