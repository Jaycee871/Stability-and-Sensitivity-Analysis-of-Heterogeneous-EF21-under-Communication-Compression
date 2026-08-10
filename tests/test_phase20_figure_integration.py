from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "build_submission_package", ROOT / "scripts" / "build_submission_package.py"
)
SUBMISSION = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(SUBMISSION)


class Phase20FigureIntegrationTests(unittest.TestCase):
    def test_manuscript_has_full_regularity_figure_markers(self) -> None:
        text = (ROOT / "manuscript" / "draft.md").read_text(encoding="utf-8")
        self.assertIn("Working manuscript draft — Phase 20", text)
        for filename in (
            "figure6_mismatch_geometry.svg",
            "figure7_full_regularity_penalty.svg",
            "figure8_rate_collapse.svg",
        ):
            self.assertIn(filename, text)

    def test_submission_render_embeds_full_regularity_captions(self) -> None:
        text = SUBMISSION.build_manuscript()
        for label in ("[Insert Figure 6 here]", "[Insert Figure 7 here]", "[Insert Figure 8 here]"):
            self.assertIn(label, text)
        self.assertIn("zero-mismatch valley", text)
        self.assertIn("Collapse of two-dimensional regularity heterogeneity", text)

    def test_integrated_asset_tree_is_copyable_into_submission_package(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            assets = root / "paper_assets"
            package = root / "submission"
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "build_paper_assets.py"),
                    "--output-dir",
                    str(assets),
                    "--tau-points",
                    "9",
                    "--epsilon-points",
                    "7",
                    "--phase19-points",
                    "9",
                ],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "build_submission_package.py"),
                    "--output-dir",
                    str(package),
                    "--paper-assets-dir",
                    str(assets),
                ],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            for filename in (
                "figure6_mismatch_geometry.svg",
                "figure7_full_regularity_penalty.svg",
                "figure8_rate_collapse.svg",
            ):
                path = package / "paper_assets" / "phase19_full_regularity" / filename
                self.assertTrue(path.exists(), filename)
                self.assertGreater(path.stat().st_size, 1000)


if __name__ == "__main__":
    unittest.main()
