from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class Phase24MDPILatexMaterializeTests(unittest.TestCase):
    def test_author_order_is_reversed_and_correspondence_is_preserved(self) -> None:
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
            self.assertIn(
                "Pack Kwan Low $^{1}$ and Fu-Hsing Wang $^{1,}$*",
                manuscript,
            )
            self.assertNotIn(
                "Fu-Hsing Wang $^{1,}$* and Pack Kwan Low $^{1}$",
                manuscript,
            )
            self.assertIn("Correspondence: Fu-Hsing Wang", manuscript)
            self.assertIn("without claiming a general EF21 convergence proof", manuscript)
            self.assertIn("Submission-draft display guard", manuscript)


if __name__ == "__main__":
    unittest.main()
