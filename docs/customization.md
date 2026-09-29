# Adapt the pipeline

Keep upstream skills neutral. Add a local layer for house style, audience, terminology, citation format, accessibility rules, CMS fields, or approval workflow. Tell the agent which layer to apply in the prompt or add a separate publication-specific skill that invokes `article-pipeline`.

Example local profile:

```markdown
# Publication profile: Example Review

Use article-pipeline for evidence, drafting, checking, and final editing.
Audience: informed general readers.
Voice: concise, explanatory; attribute contested claims.
Citation style: inline links plus a short source list.
Default genres: explainer and reported news.
Approval: editorial lead reviews organization statements before publication.
```

Keep any internal names, unpublished materials, account details, or organization-specific commitments in the local profile, not in a public fork. A profile may override length, tone, output format, and extra review requirements; it should not relax source integrity or turn an unapproved statement into an official position.

## Add a new source route

1. Identify a repeated claim type the current [routing guide](../skills/article-research/references/source-routing.md) handles poorly.
2. Add the primary source class, what it establishes, and one common limitation.
3. Test the new route on a current and a historical case. Check whether it changes the wording allowed by the evidence.

## Improve through observed cases

Keep a small set of private evaluation prompts and expected observable outcomes: source-only fidelity, a changing-status check, a quote check, a disputed source, and a genre change. Compare actual outputs before and after a rule change. Record failures and fixes without publishing private drafts or copyrighted full text. Avoid adding one-off rigid rules for an isolated failure.
