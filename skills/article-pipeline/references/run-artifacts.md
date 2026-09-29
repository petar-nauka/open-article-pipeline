# Run artifacts

For a substantial article or a handoff to a separate reviewer, create a unique folder such as `runs/<short-topic>-<YYYYMMDD-HHMM>/`. Do not overwrite a previous run. Suggested files:

- `brief.md`: purpose, audience, genre, constraints, evidence boundary, mode, date, deliverables.
- `evidence-ledger.md`: source list, claim rows, locators, permitted wording, limitations, missing evidence.
- `draft.md`: working article; optional `[C001]` claim markers for traceability.
- `verification-report.md`: checked claims, defects, fixes, coverage, remaining access limits.
- `final.md`: reader-facing version without internal markers or placeholders.

The full repository checkout has optional templates; a standalone installed skill does not need them. Small source-only edits may need just a draft and a compact check note. Keep intermediate work private unless requested. Do not store complete copies of copyrighted sources merely for convenience; record a URL, page/section, and short excerpt where necessary.

The optional `python scripts/validate_run.py <run-folder>` checks expected files, IDs, references, and placeholders. It does not determine truth, source credibility, quotation fidelity, or publication permission.
