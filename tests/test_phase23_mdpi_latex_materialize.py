from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class Phase23MDPILatexMaterializeTests(unittest.TestCase):
    def test_exact_sources_materialize_with_expected_hashes(self) -> None:
        expected = {
            "manuscript.tex": "be4e9faa00cc48f05545d6da83df521778a14f748c83132cd9a552d16217706a",
            "references.bib": "56d1eb6eb77845a3a5b9d85212aedd3687b59eb9105308bf7f199bacab9cb2a1",
        }
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "materialize_phase23_mdpi_latex.py"),
                    "--output-dir",
                    str(out),
                ],
                cwd=ROOT,
                check=True,
            )
            for filename, digest in expected.items():
                data = (out / filename).read_bytes()
                self.assertEqual(hashlib.sha256(data).hexdigest(), digest)

            manuscript = (out / "manuscript.tex").read_text(encoding="utf-8")
            self.assertIn("Fu-Hsing Wang $^{1,}$* and Pack Kwan Low $^{1}$", manuscript)
            self.assertIn("Correspondence: Fu-Hsing Wang", manuscript)
            self.assertIn("does not claim to prove", manuscript)


if __name__ == "__main__":
    unittest.main()
