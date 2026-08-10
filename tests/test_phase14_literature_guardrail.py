import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_phase14_literature_audit.py"
SPEC = importlib.util.spec_from_file_location("phase14_validator", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class Phase14LiteratureGuardrailTests(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = json.loads(
            (ROOT / "literature" / "phase14_candidate_matrix.json").read_text(
                encoding="utf-8"
            )
        )

    def _synthetic_pending_payload(self) -> dict:
        payload = json.loads(json.dumps(self.payload))
        payload["status"] = "PENDING_EXTERNAL_AUDIT"
        payload["candidates"] = []
        for claim in payload["claims"].values():
            claim["status"] = "PENDING_EXTERNAL_AUDIT"
            claim["strongest_candidate_id"] = None
            claim["manual_equivalence_verified"] = False
        return payload

    def test_current_matrix_is_a_valid_post_search_guardrail_state(self) -> None:
        report = MODULE.validate(self.payload)
        self.assertTrue(report["valid"])
        self.assertEqual(
            report["status"], "PARTIAL_EXTERNAL_AUDIT_N1_N2_ADJUDICATED"
        )
        self.assertEqual(report["candidate_count"], 7)
        self.assertIn("source adjudication", report["interpretation"])

    def test_synthetic_pending_matrix_is_valid_but_not_novelty_evidence(self) -> None:
        payload = self._synthetic_pending_payload()
        report = MODULE.validate(payload)
        self.assertTrue(report["valid"])
        self.assertEqual(report["status"], "PENDING_EXTERNAL_AUDIT")
        self.assertEqual(report["candidate_count"], 0)
        self.assertIn("not evidence", report["interpretation"])

    def test_claim_cannot_be_promoted_while_overall_audit_is_pending(self) -> None:
        payload = self._synthetic_pending_payload()
        payload["claims"]["N1"]["status"] = "CLEAR_TO_PROMOTE"
        report = MODULE.validate(payload)
        self.assertFalse(report["valid"])
        self.assertTrue(
            any("N1 must remain PENDING_EXTERNAL_AUDIT" in error for error in report["errors"])
        )

    def test_direct_candidate_requires_manual_source_check_before_promotion(self) -> None:
        payload = self._synthetic_pending_payload()
        payload["status"] = "EXTERNAL_SEARCH_COMPLETE"
        required = payload["required_candidate_fields"]
        candidate = {field: "unknown" for field in required}
        candidate.update(
            {
                "candidate_id": "P001",
                "citation": "Example prior work",
                "identifier": "example",
                "url": "https://example.invalid",
                "publication_year": 2024,
                "venue": "Example",
                "paper_family": "error_feedback",
                "exact_location": "Theorem 1",
                "local_Li_heterogeneity": "yes",
                "local_mui_heterogeneity": "yes",
                "both_Li_and_mui": "yes",
                "fixed_average_conditioning": "unclear",
                "heterogeneity_measure": "example",
                "algebraic_mapping_to_K1K2": "pending",
                "aligned_invariance_overlap": "unclear",
                "root_sensitivity_overlap": "unclear",
                "cubic_root_structure_overlap": "unclear",
                "classification": "A",
                "confidence": "medium",
                "novelty_threat": "critical",
                "manual_source_checked": False,
                "notes": "test candidate",
            }
        )
        payload["candidates"] = [candidate]
        for claim in payload["claims"].values():
            claim["status"] = "CLEAR_TO_PROMOTE"
            claim["strongest_candidate_id"] = "P001"
            claim["manual_equivalence_verified"] = False
        report = MODULE.validate(payload)
        self.assertFalse(report["valid"])
        self.assertTrue(any("A/B candidates remain unchecked" in e for e in report["errors"]))

    def test_protocol_contains_adversarial_search_instruction(self) -> None:
        protocol = (
            ROOT / "docs" / "phase14_undermind_novelty_protocol.md"
        ).read_text(encoding="utf-8")
        self.assertIn("adversarial novelty audit", protocol)
        self.assertIn("Be deliberately skeptical of novelty", protocol)
        self.assertIn("Class `A` requires", protocol)
        self.assertIn("OSF is intentionally not part of Phase 14", protocol)


if __name__ == "__main__":
    unittest.main()
