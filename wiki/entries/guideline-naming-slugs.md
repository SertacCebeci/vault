---
id: guideline-naming-slugs
title: "Guideline — Naming Slugs"
category: guideline
produced_by: lifecycle-bootstrap
domains: [meta]
tags: [guideline, slugs, naming, seed]
sources: []
aliases: []
created: 2026-04-27
updated: 2026-04-27
confidence: high
status: stub
notability_status: n/a
edit_hardness: extended-confirmed
high_stakes_class: none
quality: stub
rule_tier: guideline
covers: "Preferred slug-naming patterns: noun-first, lowercase, hyphenated, source-agnostic, no editorializing."
linted_by: []
---

# Guideline — Naming Slugs

## Lead

Choose entry slugs that read like canonical names of the subject — noun-first, source-agnostic, free of editorializing — so that future references resolve naturally and disambiguation is rarely needed.

## Recommendation

A slug is the entry's permanent name. It surfaces in wikilinks across the vault and is hard to change once set. Aim for:

- **Noun-first.** `desirable-difficulty`, not `the-desirable-difficulty-principle`.
- **Source-agnostic.** `testing-effect`, not `testing-effect-make-it-stick`. The source is captured in `sources:`, not the slug.
- **Lowercase, hyphenated, ASCII.** `[a-z0-9]+(-[a-z0-9]+)*`. No underscores, no camelCase, no spaces.
- **No editorializing.** `learning-styles-myth` is fine because "myth" is the topic; `learning-styles-debunked` or `bad-learning-styles-theory` editorializes.
- **Disambiguator suffixes when needed.** When a base term is polysemous, prefer `{base}-{disambiguator}` over invented synonyms (`mercury-element` over `quicksilver`).

Avoid:

- Trailing punctuation (`?`, `!`).
- Acronym-only slugs unless the acronym is the canonical name (`bdnf` is fine; `cl` for cognitive load is not).
- Date or version suffixes for content entries — those belong in the body's history, not the slug.

## Rationale

Slugs are the vault's primary stable identifier; renaming is expensive (every inbound wikilink must update). A naming convention that's predictable from the title reduces cognitive load when editors guess at slugs without checking. Source-agnostic naming prevents an entry from looking owned by one source when later ingestions add others.

## Examples

- Pass: `desirable-difficulty`, `chunking`, `transfer-learning`, `disambiguation-transfer`, `relation-spaced-practice-supports-long-term-retention`.
- Fail: `the-fluency-illusion-bjork-2014`, `cognitive_load_theory`, `learning-styles-bs`, `chunking-2`.

## Notes

A guideline; violations are advisory. Promotion to policy would happen if a lint rule consistently catches problems no editor has fixed informally.
