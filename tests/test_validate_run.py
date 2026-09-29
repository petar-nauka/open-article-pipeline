"""Behavioral tests for the optional structural validator."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_run.py"
SPEC = importlib.util.spec_from_file_location("validate_run", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ValidateRunTests(unittest.TestCase):
    def make_run(self, root: Path) -> None:
        (root / "brief.md").write_text("# Brief\nSource-only news adaptation\n", encoding="utf-8")
        (root / "evidence-ledger.md").write_text(
            "# Evidence ledger\n\n## Sources\n\n"
            "| ID | Title | URL or file | Published or updated | Accessed | Role and limitation |\n"
            "| --- | --- | --- | --- | --- | --- |\n"
            "| S001 | Sample statement | https://example.org/sample | 2026-01-01 | 2026-01-02 | Primary statement |\n\n"
            "## Claims\n\n"
            "| Claim ID | Importance | Claim | Source IDs | Locator | Status date | Last checked | Permitted wording | Limits |\n"
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
            "| C001 | important | A statement was issued | S001 | paragraph 2 | 2026-01-01 | 2026-01-02 | Organization states | Self-reported |\n",
            encoding="utf-8",
        )
        (root / "draft.md").write_text("The organization issued a statement. [C001]\n", encoding="utf-8")
        (root / "verification-report.md").write_text("# Verification report\n\n- Verdict: PASS\n", encoding="utf-8")
        (root / "final.md").write_text("# Article\n\nThe organization issued a statement.\n", encoding="utf-8")

    def test_complete_structure_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_run(root)
            errors, warnings = MODULE.validate(root)
            self.assertEqual(errors, [])
            self.assertEqual(warnings, [])

    def test_unknown_source_and_final_marker_fail(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_run(root)
            ledger = root / "evidence-ledger.md"
            ledger.write_text(ledger.read_text(encoding="utf-8").replace("| S001 | paragraph 2", "| S999 | paragraph 2"), encoding="utf-8")
            (root / "final.md").write_text("# Article\n\nUnfinished [C001] [source]\n", encoding="utf-8")
            errors, _ = MODULE.validate(root)
            self.assertTrue(any("unknown source ID S999" in error for error in errors))
            self.assertTrue(any("internal claim markers" in error for error in errors))
            self.assertTrue(any("unfinished placeholder" in error for error in errors))

    def test_missing_report_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_run(root)
            (root / "verification-report.md").unlink()
            errors, _ = MODULE.validate(root)
            self.assertIn("Missing file: verification-report.md", errors)


if __name__ == "__main__":
    unittest.main()
