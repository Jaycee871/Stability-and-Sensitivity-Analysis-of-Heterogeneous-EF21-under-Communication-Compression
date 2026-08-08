from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PaperAssetTests(unittest.TestCase):
    def test_paper_asset_smoke_build(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "paper_assets"
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "build_paper_assets.py"),
                    "--output-dir",
                    str(output),
                    "--tau-points",
                    "11",
                    "--epsilon-points",
                    "9",
                ],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )

            manifest = json.loads((output / "manifest.json").read_text())
            self.assertEqual(manifest["study"], "phase5_paper_assets")
            self.assertEqual(manifest["grid"]["total_cells"], 11 * 9 * 3)
            self.assertEqual(len(manifest["figures"]), 6)

            for filename in manifest["figures"]:
                path = output / "figures" / filename
                self.assertTrue(path.exists(), filename)
                self.assertGreater(path.stat().st_size, 100, filename)

            table = output / "tables" / manifest["table"]
            self.assertTrue(table.exists())
            self.assertGreater(table.stat().st_size, 100)

            boundaries = manifest["continuous_99pct_boundaries_at_epsilon_095"]
            self.assertAlmostEqual(
                boundaries["2.0"]["continuous_boundary"],
                0.4076217486520454,
                places=10,
            )
            self.assertAlmostEqual(
                boundaries["10.0"]["continuous_boundary"],
                0.17985615951449502,
                places=10,
            )
            self.assertTrue(boundaries["100.0"]["domain_fully_satisfies"])


if __name__ == "__main__":
    unittest.main()
