# Open Article Pipeline

An open, publication-oriented workflow for turning a topic, source pack, transcript, notes, or draft into a sourced article. Five portable [Agent Skills](https://agentskills.io/) cover planning, research, writing, verification, and final editing. The skills are editorial instructions, not a claim that AI can certify truth or replace an accountable editor.

The package is **domain-neutral**: news, explainers, analyses, interviews, profiles, guides, reviews, project updates, and clearly labeled opinion pieces. It does not carry a publisher's voice, organizational position, fixed word count, preferred topic, or mandatory source quota.

## Start here

1. Install the folders in `skills/` where your agent discovers skills. For Codex, copy them to `~/.codex/skills/` (Windows: `%USERPROFILE%\.codex\skills\`). Keep the directory names and `SKILL.md` files intact. Other Agent Skills-compatible hosts may use a different skills directory.
2. Invoke **`$article-pipeline`** and describe the topic or supply source files. Specify audience, language, approximate length, genre, source restrictions, and output format when these matter. The skill makes reasonable defaults when they do not.
3. Review the article and any remaining uncertainty. Publication and claims made on behalf of an organization require the appropriate human authority.

Example prompt:

> Use `$article-pipeline` to prepare a 1,000-word explainer in English for informed general readers about [topic]. Research current primary sources, distinguish established facts from projections, verify the draft, and return the final article with the sources actually used. Do not publish or create social posts.

For material limited to supplied sources:

> Use `$article-pipeline` to turn the attached report into a 700-word news article. Use only the attachment, keep quotations exact, identify anything the report does not establish, and return the article plus a short unresolved-check note.

See [more prompts](examples/prompts.md) and the [Bulgarian guide](README.bg.md).

## Skills

| Skill | Use it for |
| --- | --- |
| [`article-pipeline`](skills/article-pipeline/SKILL.md) | Coordinate the full workflow and deliver one finished article. |
| [`article-research`](skills/article-research/SKILL.md) | Find and assess evidence; build a traceable claim ledger. |
| [`article-writer`](skills/article-writer/SKILL.md) | Choose an evidence-supported angle and write a genre-appropriate draft. |
| [`article-verifier`](skills/article-verifier/SKILL.md) | Challenge the draft's material claims against inspected sources. |
| [`article-editor`](skills/article-editor/SKILL.md) | Apply verified corrections, edit for clarity, and prepare delivery. |

Each skill can be used alone. The pipeline calls the other four when an end-to-end article is requested. It uses source-only, researched, or opinion evidence rules as appropriate and scales checks to the material's risk; see [method](docs/method.md).

## Outputs and validation

For substantial work, the pipeline keeps an internal `brief.md`, `evidence-ledger.md`, `draft.md`, `verification-report.md`, and `final.md` in a run folder. [Templates](templates/) are optional starting points, not required layouts for the public article. The user receives only the requested deliverables and a concise note about material unresolved checks.

The optional standard-library-only validator checks file relationships and obvious unfinished markers:

```text
python scripts/validate_run.py path/to/run-folder
```

It **cannot** determine whether a source is reliable, whether a citation supports a claim, whether a quote is exact, or whether the article is true. Those require inspecting the original evidence and editorial judgment.

## Improve or adapt it

- Edit the genre, source, and verification guidance in the relevant skill; keep the five entrypoints short.
- Add a publication's house style as a separate local layer. Do not silently change the neutral upstream rules or imply that a draft is an official position.
- Add a source adapter or deterministic check only when it solves a repeated problem. Document what it checks and what it cannot check.
- Test changes on contrasting cases: a stable explainer, a fast-changing claim, a source-only rewrite, and a high-risk or disputed topic. Record observed failures before adding new rules.

See [CONTRIBUTING.md](CONTRIBUTING.md) for a contribution checklist and [customization](docs/customization.md) for local profiles. Open issues and pull requests with a reproducible example or a clear editorial failure mode.

## License

[MIT](LICENSE). The license covers this repository's original instructions, templates, and code. It does not grant rights to third-party sources or to articles produced with the skills.
