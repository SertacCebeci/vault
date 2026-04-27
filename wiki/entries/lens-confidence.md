---
id: lens-confidence
title: "Lens — Confidence"
category: lens
classified_by: lens-lens
domains: [meta]
tags: [annotation, convergence, contestation]
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
lens_question: "How well-supported is this entry across its sources?"
lens_priority: 230
lens_covers_category: confidence
lens_kind: annotation
lens_criteria:
  - "Stamps `confidence` ∈ {high, medium, low, contested} on every content entry."
  - "`contested` overrides everything else when sources actively disagree about the claim or framing."
  - "Downgraded by one tier when a high-stakes finding is open against the entry (§14.3.1)."
  - "Read by retrieval: `confidence: contested` entries are returned with an explicit `[CONTESTED] ` prefix."
---

# Lens — Confidence

## Question

How well-supported is this entry across its sources?

## How to apply

Run during the annotation pass after [[lens-high-stakes]]. Stamps `confidence` on every content entry; not applied to infrastructure.

Levels:

- **`high`** — multiple independent sources converge on the same finding or framing.
- **`medium`** — one source, or weak convergence (e.g., two sources but one is derivative of the other).
- **`low`** — single weak source (anecdote, blog, opinion piece) and no corroboration.
- **`contested`** — sources actively disagree. The disagreement itself is preserved in the entry (the body should describe both sides).

Rules:

1. When in doubt between two adjacent levels, prefer the more conservative.
2. `contested` is sticky — once set, only a discussion can resolve it back to `high`/`medium`/`low`.
3. A claim's `confidence` interacts with `evidence_grade`: a single A-source claim is `medium` here even though it is `A` on grade. Confidence tracks convergence; grade tracks source strength.
4. When [[lens-high-stakes]] fires the asymmetric removal regime, the parent entry's confidence is automatically downgraded by one tier until the finding resolves.

## Worked stampings

- A concept like [[desirable-difficulty]] cited in `[[make-it-stick]]`, `[[learning-how-to-learn]]`, plus primary literature → `high`.
- An entry drawing solely from one popular book → `medium`.
- An entry with one anecdote and no corroboration → `low`.
- [[learning-styles-myth]] — sources actively disagree on whether VAK has any predictive validity → `contested`.

## Retrieval interaction

Retrieval (§27) prefixes `[CONTESTED] ` to leads of `confidence: contested` entries so the consumer can downstream-handle the contested status. Other confidence levels are not surfaced to the consumer at retrieval time but feed assessment signals (§28.3).

## Notes

Distinct from `evidence_grade`: an entry can have high-grade evidence (A) and `medium` confidence (only one source), or low-grade evidence (D) but `high` confidence (many converging anecdotes). The two axes are orthogonal.

## Related lenses

- Meta-lens: [[lens-lens]]
- Runs after [[lens-high-stakes]], before [[lens-recency]].
- Read by retrieval (§27.4) and by assessment (§28.3).
