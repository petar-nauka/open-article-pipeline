# Prompt examples

Replace bracketed parts with your material. These prompts request articles; they do not assert any example facts.

## Current explainer

> Use `$article-pipeline` for an 800–1,100 word explainer in [language] for [audience] about [topic]. Research current sources, distinguish facts from forecasts, verify important claims and the latest status, and deliver the article with the sources actually used and only material remaining uncertainties. Do not publish.

## Source-only news adaptation

> Use `$article-pipeline` to turn [attached announcement/report] into a 500-word news article in [language]. Use only the supplied material. Attribute claims the material does not prove, keep quotes exact, and state whether any important external fact check remains.

## Interview

> Use `$article-pipeline` to edit [transcript] into a readable Q&A for [audience]. Preserve the speaker's meaning and the order of ideas; do not invent questions or quotes. Flag unclear passages for review, and return the edited Q&A plus a concise list of material uncertainties.

## Opinion

> Use `$article-pipeline` to help develop a clearly labeled opinion article arguing [thesis] for [audience]. Research and verify the factual premises, include the strongest relevant counterpoint, and separate my viewpoint from sourced facts. Return a draft for my approval.

## Tight revision

> Use `$article-verifier` to check the attached article's headline, key numbers, quotations, and present-tense project statuses against original sources. Return the issues with source locators. Then use `$article-editor` to apply supported corrections and deliver a clean version.
