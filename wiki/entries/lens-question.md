---
id: lens-question
title: "Lens — Question"
category: lens
classified_by: lens-lens
domains: [meta]
tags: [classification, gaps]
sources: []
aliases: []
created: 2026-04-27
updated: 2026-04-27
confidence: high
status: complete
notability_status: n/a
edit_hardness: restricted
high_stakes_class: none
quality: c
produced_by: lifecycle-bootstrap
lens_question: "Is this entry an open question pinning a gap the vault cannot yet answer?"
lens_priority: 35
lens_covers_category: question
lens_kind: decision-tree
lens_criteria:
  - "The entry's body is a question rather than an assertion or organizing prose."
  - "Frontmatter declares `asks_about`, `priority`, `opened_by`, `closes_when`."
  - "The question's `status` starts `open` and closes only when an entry, claim, or relation answers it."
  - "Slug uses the reserved prefix `question-`."
---

# Lens — Question

## Question

Is this entry an open question pinning a gap the vault cannot yet answer?

## How to apply

Run after [[lens-application]] (priority 30) and before [[lens-entity]] (priority 40). A question entry is an explicit gap — the vault saying "we noticed this and cannot answer it yet, here is what would close it." Opening a question is a deliberate act, not a placeholder; questions are always notable (§8.5).

Open a question when:

1. Ingestion noticed a topic referenced but never explained (a wikilink target with no entry).
2. An assessment pass found a domain whose canonical-questions list has a gap.
3. A discussion's closure produced a residual unanswered question.
4. A reader's query the vault could not answer cleanly.

Fill in `closes_when` at opening — the success criterion for closure (e.g., "An entry exists at `[[neuronal-recycling-hypothesis]]` with at least one A-grade source.").

A question with no path to closure is itself a finding worth raising — it suggests either the gap is too large or the closure criterion is wrong.

## Worked matches

- `question-mechanism-of-sleep-consolidation` — opened during ingestion of a chapter that referenced consolidation without explaining the mechanism. `closes_when` names the entry that would resolve it.
- `question-when-does-interleaving-fail` — a domain canonical question on the [[learning-theory]] domain entry, opened to focus future ingestion attention.

## Worked non-matches

- A question *about* the vault's structure (e.g., "should we have separate domains for X and Y?") — that's an `essay` or a `discussion`, not a content question. Route to [[lens-policy-tier]] (`essay` tier).
- A rhetorical question inside a concept's body — that's prose, not a question entry.

## Notes

Closing a question requires a resolving artifact named explicitly. Lint `unanswered-old-question` fires advisory for questions older than 6 months without progress. A closed question is not deleted; it remains as a record of the gap and how it was filled.

## Related lenses

- Meta-lens: [[lens-lens]]
- Previous lens in priority: [[lens-application]]
- Next lens in priority: [[lens-entity]]
