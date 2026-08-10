import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class Phase17PrimarySourceClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = json.loads(
            (ROOT / "literature" / "phase17_primary_source_closure.json").read_text(
                encoding="utf-8"
            )
        )

    def test_named_chain_is_closed_without_certifying_universal_novelty(self) -> None:
        self.assertEqual(self.payload["status"], "NAMED_REFERENCE_CHAIN_CLOSED")
        self.assertFalse(self.payload["universal_novelty_certified"])

    def test_all_named_sources_are_primary_source_checked(self) -> None:
        sources = self.payload["sources"]
        self.assertEqual(len(sources), 12)
        self.assertTrue(all(source["primary_source_checked"] for source in sources))

    def test_only_source_paper_is_anchor(self) -> None:
        anchors = [s for s in self.payload["sources"] if s["classification"] == "ANCHOR"]
        self.assertEqual([s["id"] for s in anchors], ["S01_Tho26"])

    def test_no_direct_equivalent_is_recorded_in_named_chain(self) -> None:
        result = self.payload["closure_result"]
        self.assertEqual(result["direct_equivalents_to_N1b_N4"], 0)
        self.assertIn("not a proof of universal novelty", result["interpretation"].lower())

    def test_scoped_contribution_language_is_allowed_but_absolute_novelty_is_blocked(self) -> None:
        gate = self.payload["manuscript_gate"]
        self.assertEqual(gate["scoped_contribution_wording"], "ALLOWED")
        self.assertEqual(gate["absolute_novelty_wording"], "BLOCKED")
        self.assertIn("novel", gate["blocked_terms"])
        self.assertIn("first", gate["blocked_terms"])

    def test_n1a_remains_non_novel(self) -> None:
        self.assertEqual(
            self.payload["claims"]["N1a"]["status"],
            "INHERITED_ALGEBRAIC_REINTERPRETATION_NO_NOVELTY",
        )

    def test_n1b_n2_n3_n4_have_scoped_ready_status(self) -> None:
        for claim_id in ("N1b", "N2", "N3", "N4"):
            self.assertIn("READY_FOR_SCOPED_CONTRIBUTION_WORDING", self.payload["claims"][claim_id]["status"])

    def test_econtrol_near_neighbor_has_local_L_but_not_local_mu_family(self) -> None:
        source = next(s for s in self.payload["sources"] if s["id"] == "S08_EControl23")
        self.assertEqual(source["classification"], "C")
        self.assertIn("single global mu", source["regularity_structure"])
        self.assertIn("local smoothness constants L_i", source["regularity_structure"])

    def test_cross_model_unresolved_reference_stays_quarantined(self) -> None:
        guardrails = "\n".join(self.payload["remaining_guardrails"])
        self.assertIn("[[ef21-stability-analysis]]", guardrails)
        self.assertIn("remains unusable", guardrails)


if __name__ == "__main__":
    unittest.main()
