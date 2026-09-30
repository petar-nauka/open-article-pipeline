#!/usr/bin/env python3
"""Check article run files for structural consistency; never claim fact verification."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


SOURCE_ID = re.compile(r"S\d{3,}$")
CLAIM_ID = re.compile(r"C\d{3,}$")
CLAIM_MARKER = re.compile(r"\[(C\d{3,})\]")
PLACEHOLDER = re.compile(
    r"\b(?:TBD|TODO|XXXX+)\b|"
    r"\[(?:source|citation needed|insert[^]]*|източник|за проверка|автор|дата)\]",
    re.IGNORECASE,
)
INLINE_LINK_END = re.compile(
    r"(?:[ \t]+(?:\"(?:\\.|[^\"\\\r\n])*\"|'(?:\\.|[^'\\\r\n])*'))?[ \t]*\)"
)
VERDICT = re.compile(r"(?im)^\s*(?:-\s*)?Verdict:\s*(PASS WITH FIXES|PASS|BLOCKED)\s*$")
SOURCE_HEADERS = ["ID", "Title", "URL or file", "Published or updated", "Accessed", "Role and limitation"]
CLAIM_HEADERS = [
    "Claim ID", "Importance", "Claim", "Source IDs", "Locator",
    "Status date", "Last checked", "Permitted wording", "Limits",
]
FILES = ("brief.md", "evidence-ledger.md", "draft.md", "verification-report.md", "final.md")


def has_inline_destination(text: str, start: int) -> bool:
    """Recognize a complete inline target, including balanced URL parentheses."""
    if text[start:start + 1] != "(":
        return False
    cursor = start + 1
    if text[cursor:cursor + 1] == "<":
        end = text.find(">", cursor + 1)
        if end <= cursor + 1 or any(char in text[cursor:end] for char in "\r\n"):
            return False
        cursor = end + 1
    else:
        depth = 0
        while cursor < len(text) and not text[cursor].isspace():
            char = text[cursor]
            if char == "\\":
                cursor += 1
                if cursor == len(text) or text[cursor].isspace():
                    return False
            elif char == "(":
                depth += 1
            elif char == ")":
                if depth == 0:
                    return cursor > start + 1
                depth -= 1
            cursor += 1
        if cursor == start + 1 or depth:
            return False
    return INLINE_LINK_END.match(text, cursor) is not None


def has_unfinished_placeholder(text: str) -> bool:
    for match in PLACEHOLDER.finditer(text):
        if match.group().casefold() in ("[source]", "[източник]") and has_inline_destination(text, match.end()):
            continue
        return True
    return False


def split_table_row(line: str) -> list[str]:
    """Split template rows on unescaped pipes, keeping cell text intact."""
    line = line.strip()
    cells = []
    cell = []
    escaped = False
    for char in line:
        if char == "|" and not escaped:
            cells.append("".join(cell).strip())
            cell = []
        else:
            cell.append(char)
        escaped = char == "\\" and not escaped
    cells.append("".join(cell).strip())
    if line.startswith("|"):
        cells.pop(0)
    if line.endswith("|") and cells and not cells[-1]:
        cells.pop()
    return cells


def table_rows(document: str, heading: str, headers: list[str], errors: list[str]) -> list[list[str]]:
    match = re.search(rf"(?im)^##\s+{re.escape(heading)}\s*$", document)
    if not match:
        errors.append(f"Evidence ledger: missing '{heading}' section")
        return []
    section = document[match.end():].split("\n## ", 1)[0]
    lines = [line.strip() for line in section.splitlines() if line.strip().startswith("|")]
    if len(lines) < 3:
        errors.append(f"Evidence ledger: '{heading}' needs a header, separator, and data row")
        return []
    actual_headers = split_table_row(lines[0])
    if actual_headers != headers:
        errors.append(f"Evidence ledger: unexpected '{heading}' table headers")
        return []
    separators = split_table_row(lines[1])
    if len(separators) != len(headers) or not all(re.fullmatch(r":?-{3,}:?", cell) for cell in separators):
        errors.append(f"Evidence ledger: invalid '{heading}' table separator")
        return []
    rows = []
    for line_number, line in enumerate(lines[2:], start=1):
        cells = split_table_row(line)
        if len(cells) != len(headers):
            errors.append(f"Evidence ledger: '{heading}' row {line_number} has {len(cells)} cells, expected {len(headers)}")
            continue
        rows.append(cells)
    return rows


def validate(run_dir: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not run_dir.is_dir():
        return [f"Run directory does not exist: {run_dir}"], warnings

    documents: dict[str, str] = {}
    for filename in FILES:
        path = run_dir / filename
        if not path.is_file():
            errors.append(f"Missing file: {filename}")
        else:
            documents[filename] = path.read_text(encoding="utf-8-sig")
    if errors:
        return errors, warnings

    ledger = documents["evidence-ledger.md"]
    sources = table_rows(ledger, "Sources", SOURCE_HEADERS, errors)
    claims = table_rows(ledger, "Claims", CLAIM_HEADERS, errors)

    source_ids: set[str] = set()
    for row_number, row in enumerate(sources, start=1):
        source_id = row[0]
        if not SOURCE_ID.fullmatch(source_id):
            errors.append(f"Sources row {row_number}: invalid ID '{source_id}'")
        elif source_id in source_ids:
            errors.append(f"Sources row {row_number}: duplicate ID {source_id}")
        source_ids.add(source_id)
        if not row[1] or not row[2]:
            errors.append(f"Sources row {row_number}: title and URL or file are required")

    claim_ids: set[str] = set()
    for row_number, row in enumerate(claims, start=1):
        claim_id = row[0]
        if not CLAIM_ID.fullmatch(claim_id):
            errors.append(f"Claims row {row_number}: invalid ID '{claim_id}'")
        elif claim_id in claim_ids:
            errors.append(f"Claims row {row_number}: duplicate ID {claim_id}")
        claim_ids.add(claim_id)
        if not row[1] or not row[2] or not row[3] or not row[4] or not row[7]:
            errors.append(f"Claims row {row_number}: importance, claim, source IDs, locator, and permitted wording are required")
        for source_id in re.split(r"[,;\s]+", row[3]):
            if source_id and source_id not in source_ids:
                errors.append(f"Claims row {row_number}: unknown source ID {source_id}")
        if row[5] and not row[6]:
            warnings.append(f"Claims row {row_number}: status date is set but last checked is blank")

    draft_ids = set(CLAIM_MARKER.findall(documents["draft.md"]))
    for claim_id in sorted(draft_ids - claim_ids):
        errors.append(f"Draft references unknown claim ID {claim_id}")
    if claims and not draft_ids:
        warnings.append("Draft has no claim markers; coverage cannot be checked mechanically")

    final = documents["final.md"]
    if not final.strip():
        errors.append("Final article is empty")
    if CLAIM_MARKER.search(final):
        errors.append("Final article contains internal claim markers")
    if has_unfinished_placeholder(final):
        errors.append("Final article contains an unfinished placeholder")

    report = documents["verification-report.md"]
    if not VERDICT.search(report):
        errors.append("Verification report needs 'Verdict: PASS', 'PASS WITH FIXES', or 'BLOCKED'")
    if "BLOCKED" in report.upper() and VERDICT.search(report) and VERDICT.search(report).group(1) == "BLOCKED":
        warnings.append("Verification is BLOCKED; do not label the article READY")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path, help="Folder containing the five article run files")
    args = parser.parse_args()
    errors, warnings = validate(args.run_dir)
    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARN: {message}")
    print(f"errors={len(errors)} warnings={len(warnings)}; structural checks only, not fact verification")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
