---
id: lens-lens
title: "Lens — Lens (meta)"
category: lens
classified_by: lens-lens
domains: [meta]
tags: [classification, self-reference]
sources: []
aliases: []
created: 2026-04-21
updated: 2026-04-21
confidence: high
status: complete
lens_question: "Is this entry a lens — an aggregation of questions that enables us to categorize knowledge?"
lens_priority: 0
lens_covers_category: lens
lens_criteria:
  - "Frontmatter declares `category: lens`."
  - "Frontmatter declares a non-empty `lens_question`."
  - "Frontmatter declares a non-empty `lens_covers_category`."
  - "Body describes how to apply the question, including at least one worked match and one worked non-match."
---

# Lens — Lens (meta)

## Question

Is this entry a lens — i.e., does it define a question used to aggregate a category of knowledge?

## How to apply

Run this lens **first**, before every other lens in the decision tree. If all four criteria in frontmatter hold, the candidate's category is `lens` and the job is done. Otherwise, fall through to the rest of the lenses in ascending `lens_priority` order.

The four criteria are literal checks against the candidate's frontmatter and body:

1. The candidate's frontmatter sets `category: lens`.
2. The candidate's frontmatter includes a non-empty `lens_question`.
3. The candidate's frontmatter includes a non-empty `lens_covers_category`.
4. The candidate's body has sections that describe how to apply the question, with at least one worked match and one worked non-match.

If any criterion fails, this lens does not match. Route to the next lens in priority order.

## Self-reference

Applying this lens to itself yields yes:

- frontmatter declares `category: lens` ✓
- frontmatter declares `lens_question` ✓
- frontmatter declares `lens_covers_category: lens` ✓
- body has the four criteria and worked examples below ✓

So `lens-lens` is categorized as `lens` by `lens-lens`. This is the fixed-point that makes the whole classification scheme consistent.

## Worked matches

- [[lens-concept]] — covers the concept category; frontmatter declares `category: lens`, `lens_question`, `lens_covers_category: concept`; body has criteria and worked examples.
- [[lens-insight]] — covers the insight category; explicitly defines the "requires naming 2+ existing concepts" rule as its criterion.

## Worked non-matches

- [[desirable-difficulty]] — declares `category: concept`, not `category: lens`; has no `lens_question`. Route to [[lens-concept]].
- [[beanbag-toss-study]] — declares `category: illustration`, not `lens`; describes a specific study, not a classification question. Route to [[lens-illustration]].

## Related lenses

All other lenses fall under this one. In priority order:

- [[lens-source]] (10) — literature notes
- [[lens-illustration]] (20) — stories with protagonist, setting, outcome
- [[lens-application]] (30) — practitioner-followable steps
- [[lens-entity]] (40) — proper-noun people, institutions, frameworks
- [[lens-process]] (50) — multi-stage sequences with transitions
- [[lens-insight]] (60) — observations connecting 2+ concepts
- [[lens-concept]] (99) — catch-all for atomic ideas
