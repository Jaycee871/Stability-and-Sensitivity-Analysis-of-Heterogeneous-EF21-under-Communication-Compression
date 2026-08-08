from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SUBMISSION = ROOT / "submission"


class SubmissionPackageTests(unittest.TestCase):
    def test_required_submission_files_exist(self) -> None:
        required = (
            "submission_metadata.md",
            "cover_letter.md",
            "back_matter.md",
            "editorial_independence_note.md",
            "checklist.md",
            "mdpi_policy_snapshot.md",
        )
        for filename in required:
            path = SUBMISSION / filename
            self.assertTrue(path.exists(), filename)
            self.assertGreater(path.stat().st_size, 200, filename)

    def test_target_and_deadline_are_consistent(self) -> None:
        metadata = (SUBMISSION / "submission_metadata.md").read_text(encoding="utf-8")
        policy = (SUBMISSION / "mdpi_policy_snapshot.md").read_text(encoding="utf-8")
        for text in (metadata, policy):
            self.assertIn("Artificial Intelligence and Algorithms", text)
            self.assertIn("30 November 2026", text)
            self.assertIn("Fuhsing Wang", text)

    def test_editorial_independence_is_explicit(self) -> None:
        cover = (SUBMISSION / "cover_letter.md").read_text(encoding="utf-8")
        note = (SUBMISSION / "editorial_independence_note.md").read_text(encoding="utf-8")
        self.assertIn("academic advisor", cover)
        self.assertIn("independent Editorial Board Member", cover)
        self.assertIn("academic advisor", note)
        self.assertIn("independent", note.lower())

    def test_genai_disclosure_is_not_omitted(self) -> None:
        back = (SUBMISSION / "back_matter.md").read_text(encoding="utf-8")
        self.assertIn("GPT-5.6 Sol", back)
        self.assertIn("Wolfram Language 15.0.1", back)
        self.assertIn("human authors", back)

    def test_data_availability_is_not_falsely_finalized(self) -> None:
        back = (SUBMISSION / "back_matter.md").read_text(encoding="utf-8")
        self.assertIn("will be archived", back)
        self.assertIn("before final submission", back)
        self.assertIn("Do **not** use", back)


if __name__ == "__main__":
    unittest.main()
