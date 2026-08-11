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
            references = (out / "references.bib").read_text(encoding="utf-8")

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
                "Stability and Sensitivity Analysis of Heterogeneous Error Feedback "
                "(EF$^{21}$) under Communication Compression",
                manuscript,
            )
            self.assertIn(
                "without claiming a general EF$^{21}$ convergence proof",
                manuscript,
            )
            self.assertNotIn("EF21", manuscript)

            # The typography transform is manuscript-only. Bibliographic source data
            # remain intact rather than being mechanically rewritten.
            self.assertIn(
                "A Tight Theory of Error Feedback Algorithms in Distributed Optimization",
                references,
            )
            self.assertIn("Submission-draft display guard", manuscript)


if __name__ == "__main__":
    unittest.main()
