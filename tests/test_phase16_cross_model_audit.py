import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class Phase16CrossModelAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = json.loads(
            (ROOT / "literature" / "phase16_cross_model_audit.json").read_text(
                encoding="utf-8"
            )
        )

    def test_n1a_is_explicitly_non_novel(self) -> None:
        n1a = self.payload["claims"]["N1a"]
        self.assertEqual(
            n1a["status"], "INHERITED_ALGEBRAIC_REINTERPRETATION_NO_NOVELTY"
        )
        self.assertIn("never as a novel theorem", n1a["manuscript_rule"])

    def test_n1b_n2_n3_n4_remain_reference_closure_pending(self) -> None:
        for claim_id in ("N1b", "N2", "N3", "N4"):
            self.assertIn(
                "REFERENCE_CLOSURE_PENDING",
                self.payload["claims"][claim_id]["status"],
            )

    def test_manuscript_novelty_language_is_blocked(self) -> None:
        gate = self.payload["promotion_gate"]
        self.assertEqual(gate["manuscript_novelty_language"], "BLOCKED")
        self.assertIn("primary-source reference closure", gate["required_before_unblocking"])

    def test_cross_model_jury_reference_is_quarantined(self) -> None:
        unresolved = self.payload["unresolved_cross_model_references"]
        self.assertEqual(len(unresolved), 1)
        self.assertEqual(
            unresolved[0]["status"], "UNRESOLVED_CROSS_MODEL_REFERENCE"
        )
        self.assertIn("must not enter", unresolved[0]["reason"])

    def test_closure_gap_does_not_treat_search_absence_as_proof(self) -> None:
        gaps = "\n".join(self.payload["closure_gaps"])
        self.assertIn("not proof of universal novelty", gaps)
        self.assertIn("theorem/equation/page", gaps)


if __name__ == "__main__":
    unittest.main()
