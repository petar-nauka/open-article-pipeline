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

    def test_inline_citation_labels_are_not_placeholders(self) -> None:
        citations = (
            "[source](https://example.org/sample)",
            "[източник](https://example.org/sample)",
            '[Source](https://example.org/sample "Sample statement")',
            "[източник](<sample statement.md>)",
            "[source](https://example.org/Report_(2026))",
            "[източник](https://example.org/Report_(part_(2026)))",
            '[source](https://example.org/Report_(2026) "Annual report")',
            r"[source](https://example.org/Report_\(2026\))",
        )
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_run(root)
            for citation in citations:
                with self.subTest(citation=citation):
                    (root / "final.md").write_text(f"A statement was issued. {citation}\n", encoding="utf-8")
                    errors, _ = MODULE.validate(root)
                    self.assertEqual(errors, [])

    def test_real_placeholders_near_citation_still_fail(self) -> None:
        placeholders = (
            "[source]", "[източник]", "[citation needed]", "[insert date]",
            "[за проверка]", "[автор]", "[дата]", "TODO", "TBD", "XXXX",
            "[source](", "[източник](https://example.org/unfinished",
            "[source](https://example.org/Report_(2026)",
            "[source](https://example.org/Report_(2026",
            "[източник](https://example.org/Report_(part_(2026))",
            '[source](https://example.org/Report_(2026) "Annual report"',
            "[source]()", "[source](please insert actual url)",
        )
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_run(root)
            for placeholder in placeholders:
                with self.subTest(placeholder=placeholder):
                    (root / "final.md").write_text(
                        f"[source](https://example.org/sample) {placeholder}\n", encoding="utf-8",
                    )
                    errors, _ = MODULE.validate(root)
                    self.assertIn("Final article contains an unfinished placeholder", errors)

    def test_escaped_pipes_in_source_and_claim_cells_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_run(root)
            ledger = root / "evidence-ledger.md"
            text = ledger.read_text(encoding="utf-8")
            text = text.replace("Sample statement", r"Research \| Annual statement")
            text = text.replace("A statement was issued", r"A statement \| update was issued")
            text = text.replace("Self-reported", r"Self-reported \|")
            ledger.write_text(text, encoding="utf-8")
            errors, warnings = MODULE.validate(root)
            self.assertEqual(errors, [])
            self.assertEqual(warnings, [])

    def test_unescaped_extra_pipe_still_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_run(root)
            ledger = root / "evidence-ledger.md"
            ledger.write_text(
                ledger.read_text(encoding="utf-8").replace("Sample statement", "Research | Annual statement"),
                encoding="utf-8",
            )
            errors, _ = MODULE.validate(root)
            self.assertIn("Evidence ledger: 'Sources' row 1 has 7 cells, expected 6", errors)

    def test_malformed_table_separator_fails(self) -> None:
        valid_separator = "| --- | --- | --- | --- | --- | --- |"
        invalid_separators = (
            "| --- | --- | -- | --- | --- | --- |",
            "| --- | --- | --- | --- | --- |",
            "| --- | --- | --- | --- | --- | --- | --- |",
            r"| --- | --- | ---\|--- | --- | --- | --- |",
        )
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for separator in invalid_separators:
                with self.subTest(separator=separator):
                    self.make_run(root)
                    ledger = root / "evidence-ledger.md"
                    ledger.write_text(
                        ledger.read_text(encoding="utf-8").replace(valid_separator, separator, 1),
                        encoding="utf-8",
                    )
                    errors, _ = MODULE.validate(root)
                    self.assertIn("Evidence ledger: invalid 'Sources' table separator", errors)


if __name__ == "__main__":
    unittest.main()
