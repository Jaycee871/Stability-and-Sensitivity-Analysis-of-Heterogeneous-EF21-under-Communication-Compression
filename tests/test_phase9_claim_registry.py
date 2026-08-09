from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "audit_claim_registry", ROOT / "scripts" / "audit_claim_registry.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)

REGISTRY = ROOT / "claims" / "claim_registry.json"


class Phase9ClaimRegistryTests(unittest.TestCase):
    def test_all_registered_claims_verify(self) -> None:
        report = MODULE.audit(REGISTRY)
        self.assertTrue(report["all_claims_verified"])
        self.assertEqual(report["claims_total"], 9)
        self.assertEqual(report["claims_passed"], 9)

    def test_claims_keep_explicit_evidence_levels_and_guardrails(self) -> None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        allowed = {
            "computational",
            "computational-robustness",
            "analytic-symbolic",
            "inherited-literature",
        }
        for claim in registry["claims"]:
            self.assertIn(claim["evidence_level"], allowed)
            self.assertTrue(claim["guardrail"].strip())
            self.assertTrue(claim["evidence"])

    def test_offgrid_tolerance_is_not_overstated(self) -> None:
        payload = json.loads(
            (ROOT / "results" / "phase4_summary.json").read_text(encoding="utf-8")
        )
        residual = payload["offgrid_validation"][2]["max_epsilon_monotonicity_violation"]
        self.assertGreater(residual, 0.0)
        self.assertLess(residual, 1e-9)

    def test_symbolic_claim_scope_is_fixed_strata_only(self) -> None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        symbolic = {
            claim["id"]: claim
            for claim in registry["claims"]
            if claim["evidence_level"] == "analytic-symbolic"
        }
        self.assertEqual(set(symbolic), {"C07", "C08"})
        for claim in symbolic.values():
            guardrail = claim["guardrail"].lower()
            self.assertTrue(
                "fixed" in guardrail or "does not prove" in guardrail,
                msg=claim["guardrail"],
            )

    def test_inherited_empirical_law_is_not_promoted_to_theorem(self) -> None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        inherited = next(claim for claim in registry["claims"] if claim["id"] == "C09")
        self.assertEqual(inherited["evidence_level"], "inherited-literature")
        self.assertIn("empirical", inherited["guardrail"].lower())


if __name__ == "__main__":
    unittest.main()
