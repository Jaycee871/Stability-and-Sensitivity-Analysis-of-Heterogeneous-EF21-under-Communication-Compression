from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class Phase24MDPILatexMaterializeTests(unittest.TestCase):
    def test_round2_author_review_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "materialize_phase24_mdpi_latex.py"),
                    "--output-dir",
                    str(out),
                ],
                cwd=ROOT,
                check=True,
            )

            manuscript = (out / "manuscript.tex").read_text(encoding="utf-8")
            references_bib = (out / "references.bib").read_text(encoding="utf-8")

            # Authorship and PDF-string-safe EF21 notation.
            self.assertIn("Pack Kwan Low $^{1}$ and Fu-Hsing Wang $^{1,}$*", manuscript)
            self.assertIn("\\texorpdfstring{EF$^{21}$}{EF21}", manuscript)
            self.assertIn("\\setlength{\\headheight}{19pt}", manuscript)

            # First-use definitions: q_i and w_i must precede K1/K2, and the
            # weighted variance is defined immediately rather than deferred.
            q_pos = manuscript.index("q_i=\n\\frac{\\Delta_i}{\\Sigma_i}")
            k_pos = manuscript.index("K_1=\\sum_{i=1}^{2} w_iq_i^2")
            self.assertLess(q_pos, k_pos)
            self.assertIn("\\operatorname{Var}_w(q_i)\n:=", manuscript)
            self.assertNotIn("their difference will later be shown", manuscript)

            # Round 2 narrative rebalance.
            self.assertIn("The study makes three main contributions.", manuscript)
            self.assertIn("collapses onto a single nonnegative mismatch coordinate", manuscript)
            self.assertIn("\\begin{Proposition}[Conditional mismatch principle]", manuscript)
            self.assertEqual(
                manuscript.count("\\begin{Proposition}[Conditional mismatch principle]"),
                1,
            )
            self.assertLess(
                manuscript.index("\\section{Results}"),
                manuscript.index("\\begin{Proposition}[Conditional mismatch principle]"),
            )
            self.assertLess(
                manuscript.index("\\begin{Proposition}[Conditional mismatch principle]"),
                manuscript.index("\\section{Discussion}"),
            )

            # Internal project labels must not leak into the journal manuscript.
            for token in ("N1a", "N1b", "Phase 4", "Phase 13"):
                self.assertNotIn(token, manuscript)

            # Source attribution and notation consistency.
            self.assertIn(
                "homogeneous baseline $\\rho_{\\mathrm{hom}}$ from Theorem 3.1 of Ref.~\\citep{thomsen2026tight}",
                manuscript,
            )
            self.assertNotIn("\\rho_{\\rm homogeneous}", manuscript)
            self.assertIn("Algebraic generalizability beyond two agents", manuscript)
            self.assertIn(
                "Future work should test whether analogous mismatch coordinates emerge for $n>2$",
                manuscript,
            )

            # Bibliographic and DOI guards.
            self.assertIn(
                "EF21: A new, simpler, theoretically better, and practically faster error feedback.",
                manuscript,
            )
            self.assertIn("{\\nolinkurl{doi:10.48550/arXiv.2402.10774}}", manuscript)
            self.assertIn(
                "A Tight Theory of Error Feedback Algorithms in Distributed Optimization",
                references_bib,
            )


if __name__ == "__main__":
    unittest.main()
