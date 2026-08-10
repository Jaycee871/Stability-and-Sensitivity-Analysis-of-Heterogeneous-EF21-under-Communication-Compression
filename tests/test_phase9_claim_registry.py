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
        self.assertEqual(report["registry_version"], 2)
        self.assertTrue(report["all_claims_verified"])
        self.assertEqual(report["claims_total"], 18)
        self.assertEqual(report["claims_passed"], 18)

    def test_claims_keep_explicit_evidence_levels_and_guardrails(self) -> None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        allowed = {
            "computational",
            "computational-robustness",
            "computational-full-regularity",
            "analytic-symbolic-fixed-strata",
            "analytic-symbolic-generic-cubic",
            "analytic-symbolic-controlled-consequence",
            "algebraic-inherited-interpretation",
            "algebraic-controlled",
            "inherited-literature",
            "literature-audit",
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

    def test_fixed_stratum_symbolic_claims_remain_scoped(self) -> None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        symbolic = {
            claim["id"]: claim
            for claim in registry["claims"]
            if claim["evidence_level"] == "analytic-symbolic-fixed-strata"
        }
        self.assertEqual(set(symbolic), {"C07", "C08"})
        for claim in symbolic.values():
            guardrail = claim["guardrail"].lower()
            self.assertTrue("fixed" in guardrail or "does not prove" in guardrail)

    def test_inherited_empirical_law_is_not_promoted_to_theorem(self) -> None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        by_id = {claim["id"]: claim for claim in registry["claims"]}
        self.assertEqual(by_id["C09"]["evidence_level"], "inherited-literature")
        self.assertIn("empirical", by_id["C09"]["guardrail"].lower())
        self.assertEqual(by_id["C12"]["evidence_level"], "algebraic-inherited-interpretation")
        self.assertIn("do not present", by_id["C12"]["guardrail"].lower())

    def test_full_regularity_claim_family_is_registered(self) -> None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        by_id = {claim["id"]: claim for claim in registry["claims"]}
        self.assertEqual(set(by_id), {f"C{i:02d}" for i in range(1, 19)})
        for claim_id in ("C10", "C11", "C12", "C13", "C14", "C15", "C16", "C17"):
            sources = {item["source"] for item in by_id[claim_id]["evidence"]}
            self.assertTrue(
                "results/phase12_summary.json" in sources
                or "results/phase13_symbolic_certificate.json" in sources
                or "literature/phase17_primary_source_closure.json" in sources
            )

    def test_generic_root_and_sensitivity_claims_use_phase13_certificate(self) -> None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        by_id = {claim["id"]: claim for claim in registry["claims"]}
        for claim_id in ("C15", "C16", "C17"):
            self.assertTrue(
                all(
                    item["source"] == "results/phase13_symbolic_certificate.json"
                    for item in by_id[claim_id]["evidence"]
                )
            )
            self.assertIn("inherited", by_id[claim_id]["guardrail"].lower())

    def test_literature_closure_does_not_certify_universal_novelty(self) -> None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        c18 = next(claim for claim in registry["claims"] if claim["id"] == "C18")
        self.assertEqual(c18["evidence_level"], "literature-audit")
        self.assertIn("universal", c18["guardrail"].lower())
        payload = json.loads(
            (ROOT / "literature" / "phase17_primary_source_closure.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertFalse(payload["universal_novelty_certified"])


if __name__ == "__main__":
    unittest.main()
