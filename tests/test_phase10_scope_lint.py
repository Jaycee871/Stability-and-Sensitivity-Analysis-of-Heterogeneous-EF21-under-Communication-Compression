from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "lint_manuscript_scope", ROOT / "scripts" / "lint_manuscript_scope.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class Phase10ScopeLintTests(unittest.TestCase):
    def test_current_manuscript_passes_scope_lint(self) -> None:
        text = (ROOT / "manuscript" / "draft.md").read_text(encoding="utf-8")
        report = MODULE.lint(text)
        self.assertTrue(report["pass"], report)

    def test_explicit_negative_proof_statement_is_allowed(self) -> None:
        text = (
            "This study does not attempt to prove the full heterogeneous empirical law. "
            "It does not prove Empirical Law 4.3. "
            "These tests are not proofs of global monotonicity. "
            "These are not universal convergence thresholds. "
            "The symbolic result is only for the three fixed conditioning strata. "
            "The retention boundary is not a direct communication-cost optimum."
        )
        report = MODULE.lint(text)
        self.assertTrue(report["pass"], report)

    def test_positive_overclaim_is_rejected(self) -> None:
        baseline = (
            "This study does not attempt to prove the full heterogeneous empirical law. "
            "These tests are not proofs of global monotonicity. "
            "These are not universal convergence thresholds. "
            "The symbolic result is only for the three fixed conditioning strata. "
            "The retention boundary is not a direct communication-cost optimum. "
        )
        report = MODULE.lint(baseline + "We prove Empirical Law 4.3 for EF21.")
        self.assertFalse(report["pass"])
        self.assertTrue(report["forbidden_pattern_violations"])

    def test_missing_guardrail_is_rejected(self) -> None:
        report = MODULE.lint("A short manuscript with no scope statements.")
        self.assertFalse(report["pass"])
        self.assertGreater(len(report["missing_required_guardrails"]), 0)

    def test_reviewer_premortem_and_novelty_statement_exist(self) -> None:
        self.assertTrue((ROOT / "submission" / "reviewer_premortem.md").exists())
        self.assertTrue((ROOT / "submission" / "novelty_statement.md").exists())
        self.assertTrue((ROOT / "manuscript" / "terminology_guardrails.md").exists())


if __name__ == "__main__":
    unittest.main()
