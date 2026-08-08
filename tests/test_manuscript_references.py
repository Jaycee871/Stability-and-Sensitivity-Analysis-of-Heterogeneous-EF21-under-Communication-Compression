from __future__ import annotations

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ManuscriptReferenceTests(unittest.TestCase):
    def test_all_manuscript_citation_keys_exist_in_bib(self) -> None:
        manuscript = (ROOT / "manuscript" / "draft.md").read_text(encoding="utf-8")
        bibliography = (ROOT / "manuscript" / "references.bib").read_text(encoding="utf-8")

        cited = set(re.findall(r"@([A-Za-z0-9_:-]+)", manuscript))
        available = set(re.findall(r"@[A-Za-z]+\{([^,]+),", bibliography))

        self.assertTrue(cited)
        self.assertEqual(cited - available, set())

    def test_no_reference_placeholders_remain(self) -> None:
        manuscript = (ROOT / "manuscript" / "draft.md").read_text(encoding="utf-8")
        self.assertNotIn("REF-ORIGINAL", manuscript)
        self.assertNotIn("REF-EF21", manuscript)
        self.assertNotIn("pending Zotero pass", manuscript)

    def test_figure_caption_inventory_matches_manuscript_map(self) -> None:
        captions = (ROOT / "manuscript" / "figure_captions.md").read_text(encoding="utf-8")
        for label in ("Figure 1", "Figure 2", "Figure 3", "Figure 4", "Figure 5", "Figure S1", "Table 1"):
            self.assertIn(label, captions)


if __name__ == "__main__":
    unittest.main()
