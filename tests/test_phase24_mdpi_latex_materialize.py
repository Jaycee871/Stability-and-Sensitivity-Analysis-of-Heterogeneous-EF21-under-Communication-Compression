from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class Phase24MDPILatexMaterializeTests(unittest.TestCase):
    def test_author_reviewed_front_matter_and_ef_notation(self) -> None:
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
            body, marker, bibliography = manuscript.partition("\\reftitle{References}")

            self.assertTrue(marker)
            self.assertIn(
                "Pack Kwan Low $^{1}$ and Fu-Hsing Wang $^{1,}$*",
                manuscript,
            )
            self.assertNotIn(
                "Fu-Hsing Wang $^{1,}$* and Pack Kwan Low $^{1}$",
                manuscript,
            )
            self.assertIn("Correspondence: Fu-Hsing Wang", manuscript)

            self.assertIn(
                "Stability and Sensitivity Analysis of Heterogeneous Error Feedback 21 "
                "(EF$^{21}$) under Communication Compression",
                manuscript,
            )
            self.assertNotIn(
                "Stability and Sensitivity Analysis of Heterogeneous Error Feedback "
                "(EF$^{21}$) under Communication Compression",
                manuscript,
            )
            self.assertIn(
                "without claiming a general EF$^{21}$ convergence proof",
                body,
            )
            self.assertNotIn("EF21", body)

            # Author-review readability edits: first-use technical concepts are
            # emphasized, and K1/K2 receive a concise reader-facing interpretation
            # immediately after their inherited definitions.
            self.assertIn("\\emph{Statistical or data heterogeneity} concerns", manuscript)
            self.assertIn("\\emph{Regularity heterogeneity} concerns", manuscript)
            self.assertIn(
                "weighted variance of \\emph{local condition-shape coordinates}",
                manuscript,
            )
            self.assertIn(
                "Hence \\emph{aligned heterogeneity} leaves the inherited cubic unchanged",
                manuscript,
            )
            self.assertIn(
                "Conditional on Empirical Law 4.3, \\emph{regularity mismatch} therefore worsens",
                manuscript,
            )
            guidance = (
                "These coefficients summarize the weighted second moment and squared weighted mean "
                "of the local condition-shape coordinates; their difference will later be shown to "
                "equal a weighted variance."
            )
            self.assertEqual(manuscript.count(guidance), 1)
            self.assertLess(manuscript.index("K_2="), manuscript.index(guidance))
            self.assertLess(manuscript.index(guidance), manuscript.index("Let\n\n\\[\n s=\\sqrt"))

            # The notation transform stops before References. Published titles must
            # remain verbatim even when they use the original plain EF21 spelling.
            self.assertIn(
                "EF21: A new, simpler, theoretically better, and practically faster error feedback.",
                bibliography,
            )
            self.assertIn(
                "A Tight Theory of Error Feedback Algorithms in Distributed Optimization",
                references_bib,
            )
            self.assertIn("Submission-draft display guard", manuscript)


if __name__ == "__main__":
    unittest.main()
