from pathlib import Path
import json
import sys
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ef21_stability.core import (  # noqa: E402
    TwoAgentConfig,
    cubic_coefficients,
    optimal_contraction_factor,
)


class WolframBridgeTests(unittest.TestCase):
    def test_shared_reference_cases_are_valid_python_cells(self):
        payload = json.loads((ROOT / "wolfram/reference_cases.json").read_text())
        cases = payload["cases"]
        self.assertGreaterEqual(len(cases), 6)
        for row in cases:
            kappa = float(row["kappa_bar"])
            cfg = TwoAgentConfig(
                epsilon=float(row["epsilon"]),
                tau=float(row["tau"]),
                L=1.0,
                mu_bar=1.0 / kappa,
            )
            coeffs = cubic_coefficients(cfg)
            rho = optimal_contraction_factor(cfg)
            self.assertTrue(np.all(np.isfinite(coeffs)))
            self.assertGreaterEqual(rho, 0.0)
            self.assertLessEqual(rho, 1.0 + 1e-10)

    def test_cloud_api_has_no_arbitrary_expression_evaluation(self):
        text = (ROOT / "wolfram/cloud_api.wl").read_text()
        forbidden = (
            "ToExpression",
            "ExternalEvaluate",
            'Interpreter["Expression"]',
            "WolframAlpha[",
        )
        for token in forbidden:
            self.assertNotIn(token, text)
        for action in ("coefficients", "roots", "retention", "discriminant"):
            self.assertIn(f'"{action}"', text)

    def test_cloud_api_defaults_to_private(self):
        text = (ROOT / "wolfram/cloud_api.wl").read_text()
        self.assertIn('$EF21APIPermissions = "Private";', text)


if __name__ == "__main__":
    unittest.main()
