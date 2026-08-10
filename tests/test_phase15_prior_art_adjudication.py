import csv
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class Phase15PriorArtAdjudicationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.matrix = json.loads(
            (ROOT / "literature" / "phase14_candidate_matrix.json").read_text(
                encoding="utf-8"
            )
        )
        self.summary = json.loads(
            (ROOT / "results" / "phase15_manual_adjudication_summary.json").read_text(
                encoding="utf-8"
            )
        )

    def test_n1_n2_partial_audit_is_adjudicated_but_n3_n4_stay_blocked(self) -> None:
        self.assertEqual(
            self.matrix["status"], "PARTIAL_EXTERNAL_AUDIT_N1_N2_ADJUDICATED"
        )
        self.assertEqual(
            self.matrix["claims"]["N1"]["status"],
            "PROMOTE_WITH_PRIOR_ART_POSITIONING",
        )
        self.assertEqual(
            self.matrix["claims"]["N2"]["status"],
            "PROMOTE_WITH_PRIOR_ART_POSITIONING",
        )
        self.assertEqual(
            self.matrix["claims"]["N3"]["status"],
            "REQUIRES_MANUAL_EQUIVALENCE_CHECK",
        )
        self.assertEqual(
            self.matrix["claims"]["N4"]["status"],
            "REQUIRES_MANUAL_EQUIVALENCE_CHECK",
        )

    def test_no_class_a_equivalent_is_recorded_for_supplied_shortlist(self) -> None:
        candidates = self.matrix["candidates"]
        self.assertEqual(len(candidates), 7)
        counts = {label: 0 for label in "ABCD"}
        for candidate in candidates:
            counts[candidate["classification"]] += 1
            self.assertTrue(candidate["manual_source_checked"])
        self.assertEqual(counts, {"A": 0, "B": 2, "C": 5, "D": 0})
        self.assertEqual(self.summary["classification_counts"], counts)

    def test_anchor_and_material_overlap_are_not_misrepresented_as_class_a(self) -> None:
        candidates = {
            candidate["candidate_id"]: candidate
            for candidate in self.matrix["candidates"]
        }
        self.assertEqual(candidates["C01_Tho26"]["classification"], "B")
        self.assertIn(
            "defines K1 and K2",
            candidates["C01_Tho26"]["algebraic_mapping_to_K1K2"],
        )
        self.assertEqual(candidates["C04_Ric24"]["classification"], "B")
        self.assertIn(
            "L_var",
            candidates["C04_Ric24"]["heterogeneity_measure"],
        )
        self.assertIn(
            "No algebraic mapping",
            candidates["C04_Ric24"]["algebraic_mapping_to_K1K2"],
        )

    def test_undermind_export_is_archived_and_has_seven_rows(self) -> None:
        csv_path = (
            ROOT
            / "literature"
            / "undermind"
            / "Adversarial_N1_N2_Novelty_Audit.csv"
        )
        self.assertTrue(csv_path.exists())
        with csv_path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 7)
        self.assertEqual(rows[0]["Cite Key"], "Tho26")
        self.assertEqual(rows[3]["Cite Key"], "Ric24")

    def test_manuscript_is_still_blocked(self) -> None:
        self.assertFalse(self.summary["manuscript_promotion"])
        self.assertIn("N3-N4", self.summary["next_action"])
        doc = (
            ROOT / "docs" / "phase15_manual_prior_art_adjudication.md"
        ).read_text(encoding="utf-8")
        self.assertIn("not yet inserted into the manuscript", doc)
        self.assertIn("Do **not** prepend", doc)


if __name__ == "__main__":
    unittest.main()
