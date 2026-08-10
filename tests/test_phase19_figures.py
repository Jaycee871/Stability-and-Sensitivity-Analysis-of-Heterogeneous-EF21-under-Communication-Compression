from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_phase19_figures.py"
SPEC = importlib.util.spec_from_file_location("phase19_figures", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class Phase19FigureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.surface = MODULE.evaluate_surface(
            kappa=10.0,
            epsilon=0.95,
            tau_min=0.05,
            points=15,
        )

    def test_surface_contains_valid_and_masked_cells(self) -> None:
        valid = self.surface["valid"]
        self.assertGreater(int(np.sum(valid)), 0)
        self.assertGreater(int(valid.size - np.sum(valid)), 0)

    def test_aligned_path_is_zero_mismatch_and_zero_penalty(self) -> None:
        records = self.surface["records"]
        diagonal = [row for row in records if abs(row["tau_L"] - row["tau_mu"]) <= 1e-14]
        self.assertGreater(len(diagonal), 0)
        self.assertLess(max(abs(row["K1_minus_K2"]) for row in diagonal), 1e-12)
        self.assertLess(max(abs(row["normalized_penalty"]) for row in diagonal), 1e-9)

    def test_penalty_is_nonnegative_and_increases_with_mismatch_coordinate(self) -> None:
        records = sorted(self.surface["records"], key=lambda row: row["K1_minus_K2"])
        self.assertGreaterEqual(min(row["normalized_penalty"] for row in records), -1e-10)
        # At fixed kappa and epsilon, the Phase 13 result implies the inherited
        # largest-root penalty is a monotone function of K1-K2. Allow tiny root noise.
        running_max = -float("inf")
        for row in records:
            value = row["normalized_penalty"]
            self.assertGreaterEqual(value + 1e-8, running_max)
            running_max = max(running_max, value)

    def test_svg_builders_emit_nonempty_publication_assets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            taus = self.surface["taus"]
            MODULE.save_heatmap(
                self.surface["gap"],
                taus,
                out / "gap.svg",
                title="gap",
                colorbar_label="K1-K2",
            )
            MODULE.save_heatmap(
                self.surface["penalty"],
                taus,
                out / "penalty.svg",
                title="penalty",
                colorbar_label="normalized penalty",
            )
            MODULE.save_rate_collapse({10.0: self.surface}, out / "collapse.svg")
            for name in ("gap.svg", "penalty.svg", "collapse.svg"):
                path = out / name
                self.assertTrue(path.exists())
                self.assertGreater(path.stat().st_size, 1000)


if __name__ == "__main__":
    unittest.main()
