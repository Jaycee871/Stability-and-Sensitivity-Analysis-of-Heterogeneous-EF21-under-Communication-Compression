from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "build_submission_package", ROOT / "scripts" / "build_submission_package.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class Phase8SubmissionTests(unittest.TestCase):
    def test_citations_are_resolved(self) -> None:
        manuscript = MODULE.build_manuscript()
        self.assertNotIn("[@", manuscript)
        for number in range(1, 8):
            self.assertIn(f"{number}.", manuscript)

    def test_required_sections_present(self) -> None:
        manuscript = MODULE.build_manuscript()
        required = [
            "## Abstract",
            "## 1. Introduction",
            "## 3. Methods",
            "### 3.8 AI-assisted research workflow",
            "## 4. Results",
            "## 5. Discussion",
            "## 6. Limitations",
            "## 7. Conclusion",
            "## Author Contributions",
            "## Funding",
            "## Data Availability Statement",
            "## Acknowledgments",
            "## Conflicts of Interest",
            "## References",
        ]
        for heading in required:
            self.assertIn(heading, manuscript)

    def test_figure_and_table_captions_embedded(self) -> None:
        manuscript = MODULE.build_manuscript()
        for label in ["Figure 1.", "Figure 2.", "Figure 3.", "Figure 4.", "Figure 5.", "Figure S1.", "Table 1."]:
            self.assertIn(label, manuscript)

    def test_submission_blockers_are_explicit_not_silent(self) -> None:
        manuscript = MODULE.build_manuscript()
        for token in MODULE.BLOCKERS:
            self.assertIn(token, manuscript)

    def test_builder_writes_readiness_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "package"
            manuscript = MODULE.build_manuscript()
            out.mkdir(parents=True)
            (out / "manuscript_free_format.md").write_text(manuscript, encoding="utf-8")
            unresolved = [token for token in MODULE.BLOCKERS if token in manuscript]
            report = {
                "content_ready": True,
                "final_submission_ready": not unresolved,
                "citations_resolved_to_numbered_references": "[@" not in manuscript,
            }
            (out / "readiness_report.json").write_text(json.dumps(report), encoding="utf-8")
            parsed = json.loads((out / "readiness_report.json").read_text(encoding="utf-8"))
            self.assertTrue(parsed["content_ready"])
            self.assertFalse(parsed["final_submission_ready"])
            self.assertTrue(parsed["citations_resolved_to_numbered_references"])


if __name__ == "__main__":
    unittest.main()
