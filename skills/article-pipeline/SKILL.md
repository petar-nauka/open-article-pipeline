---
name: article-pipeline
description: Produce a sourced, checked, edited article from a topic, notes, transcript, supplied sources, or draft. Use for an end-to-end publication workflow across genres and languages, not for a short standalone fact answer.
---

# Article pipeline

Turn one request into a defensible article. Coordinate `article-research`, `article-writer`, `article-verifier`, and `article-editor`; do not repeat their full instructions here. If an individual skill is unavailable, perform its essential checks directly and describe any review limitation honestly.

## 1. Scope the request

Identify the deliverable, genre, audience, language, approximate length, publication channel, source boundary, and requested extras. Use sensible neutral defaults only for missing choices. Preserve the user's specified format and source restrictions. Read [modes](references/modes.md) to choose proportionate evidence and review depth. An article that contains material legal, medical, financial, safety, reputational, or fast-changing claims needs stronger current evidence.

Choose **source-only**, **researched**, or **opinion** evidence handling. Source-only means no added external facts; checking the supplied material's claims against outside evidence is a separate scope that must be explicitly authorized. If material risk calls for broader review, state the need while honoring the user's source and tool restrictions. Opinion permits a stated viewpoint but does not exempt its factual premises from checking.

## 2. Build evidence before writing

Use `article-research` to inspect sources and capture the material claims in a ledger. A search result, abstract alone when the full result matters, or another AI summary is a lead rather than proof. For changing facts, record the publication date, the date of the reported state, and the latest-event check. If a central claim lacks support, seek it, qualify the claim, or remove it. Do not choose the final angle until evidence is assessed.

## 3. Draft, challenge, repair

Use `article-writer` to draft within the evidence boundary. Use `article-verifier` on the draft and source ledger. Give a separate reviewer a clean brief when one is available and authorized: draft, ledger, access to supplied originals, review date and mode, evidence boundary, verification scope, and explicit user restrictions. Exclude the author's rationale and expected verdict. The reviewer must inspect originals and seek contrary or later evidence within the permitted scope; the ledger is a map, not proof. For source-only work, check fidelity to the supplied corpus unless external verification is explicitly authorized. If no independent reviewer exists, perform a distinct adversarial pass and label it as a self-review. Do not imply independence.

Use `article-editor` to resolve verified defects, improve structure and language, and prepare the final version. Recheck changed or newly added factual claims. Use targeted follow-up research within the evidence boundary for any affected claim that needs additional support. Repeat the full research stage only when a correction changes the central conclusion.

## 4. Decide readiness and deliver

Read [run artifacts](references/run-artifacts.md) when saving intermediate files. If working from the full repository checkout, its optional `scripts/validate_run.py` performs mechanical checks; its success is never a fact-check result. Deliver only requested outputs. Include the sources actually used when the user requests them or the format calls for them; name material uncertainty briefly outside the article.

Use `READY` only when all material claims and quotations have adequate inspected support, current-status checks are complete where needed, and no blocking issue remains. Use `READY AFTER CHECKS` when a finite, noncritical check remains. Use `DRAFT ONLY` when a key source, authority, independent high-risk review, or material fact is unresolved. State what is missing. Do not publish, represent an organization, or create unrelated assets unless requested and authorized.
