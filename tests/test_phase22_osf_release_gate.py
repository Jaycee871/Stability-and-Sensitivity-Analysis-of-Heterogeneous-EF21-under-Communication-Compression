from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_osf_release_candidate.py"
SPEC = importlib.util.spec_from_file_location("phase22_osf", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class Phase22OSFReleaseGateTests(unittest.TestCase):
    def test_scientific_gate_is_ready_but_does_not_certify_universal_novelty(self) -> None:
        gate = MODULE.validate_scientific_gate()
        self.assertTrue(gate["valid"], gate["errors"])
        self.assertEqual(gate["claim_registry_version"], 2)
        self.assertEqual(gate["registered_claims"], 18)
        self.assertEqual(gate["named_reference_chain"], "NAMED_REFERENCE_CHAIN_CLOSED")
        self.assertFalse(gate["universal_novelty_certified"])

    def test_osf_metadata_is_explicitly_unresolved(self) -> None:
        metadata = json.loads(
            (ROOT / "osf" / "osf_metadata_template.json").read_text(encoding="utf-8")
        )
        self.assertFalse(metadata["public"])
        self.assertEqual(metadata["registration_status"], "NOT_REGISTERED")
        self.assertIsNone(metadata["doi"])
        self.assertIsNone(metadata["osf_identifier"])
        self.assertIn("Do not claim", metadata["guardrail"])

    def test_reviewer_premortem_attacks_full_regularity_and_archive_claims(self) -> None:
        text = (ROOT / "submission" / "reviewer_premortem.md").read_text(encoding="utf-8")
        for phrase in (
            "Is `K1-K2 = Var_w(q_i)` merely elementary algebra?",
            "Is Figure 8 just a tautological replot?",
            "Did the literature audit merely fail to find a counterexample?",
            "Is the OSF record actually frozen and reproducible?",
            "READY_FOR_OSF_DRAFT_UPLOAD",
        ):
            self.assertIn(phrase, text)

    def test_candidate_inventory_uses_sha256_and_skips_secret_like_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "safe.txt").write_text("safe", encoding="utf-8")
            (root / "secret.key").write_text("not for archive", encoding="utf-8")
            rows = MODULE.inventory(root)
            self.assertEqual([row["path"] for row in rows], ["safe.txt", "secret.key"])
            # inventory is a generic digest function; filtering occurs during copy.
            self.assertEqual(len(rows[0]["sha256"]), 64)
            self.assertTrue(MODULE.should_skip(Path("secret.key")))
            self.assertFalse(MODULE.should_skip(Path("safe.txt")))

    def test_scoped_contribution_statement_blocks_absolute_precedence(self) -> None:
        text = (ROOT / "submission" / "novelty_statement.md").read_text(encoding="utf-8")
        self.assertIn("universal_novelty_certified=false", text)
        self.assertIn("does not use absolute precedence claims", text)
        self.assertIn("inherited algebraic reinterpretation", text)


if __name__ == "__main__":
    unittest.main()
