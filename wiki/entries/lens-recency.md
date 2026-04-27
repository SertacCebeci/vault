---
id: lens-recency
title: "Lens — Recency"
category: lens
classified_by: lens-lens
domains: [meta]
tags: [annotation, time-bounded, staleness]
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
lens_question: "Is this claim or source's content time-bounded such that it may go stale?"
lens_priority: 240
lens_covers_category: time_bounded_tag
lens_kind: annotation
lens_criteria:
  - "Adds the tag `time-bounded` to the `tags` list when the content's truth depends on a date, version, or current state of an external system."
  - "Applies to claim and source entries primarily; concept entries inherit the tag if they are dominated by time-bounded claims."
  - "Time-bounded entries are eligible for `stale-finding` review at scheduled lint passes."
---

# Lens — Recency

## Question

Is this claim or source's content time-bounded such that it may go stale?

## How to apply

Run during the annotation pass after [[lens-confidence]]. The lens does not stamp a dedicated frontmatter field; it adds the tag `time-bounded` to the entry's `tags` list when the content has an implicit expiration.

A unit is time-bounded if any of the following hold:

1. The assertion depends on the **current state** of an external system, body of work, technology, or institution (e.g., "the leading evidence-based learning textbook is X" — depends on what's leading right now).
2. The assertion references a **version, year, or release** that may be superseded.
3. The source itself is dated and the field is moving — a 2014 review of a fast-moving research area is more time-bounded than a 1980s textbook on a stable topic.

A unit is **not** time-bounded if it asserts a stable phenomenon (e.g., "spaced practice produces stronger long-term retention than massed practice" — empirical regularity, not a year-dependent fact).

## Effects

- Tagged entries are eligible for periodic review by a recency-checking lint or assessment agent.
- Retrieval may filter for `recency`-tagged content explicitly when the consumer's task is time-sensitive.
- A stale time-bounded entry whose `updated` date is more than the policy threshold (per `policy-archival` or a future `policy-recency`) raises an advisory `finding-stale-time-bounded-{slug}`.

## Worked stampings

- A source entry for a 2024 paper reporting recent fMRI findings → `time-bounded`.
- A claim like "the current best evidence on spaced repetition is reviewed in this 2019 meta-analysis" → `time-bounded` (the "current best" qualifier).
- A claim like "spaced practice improves long-term retention" → not time-bounded; the empirical regularity is stable across decades of study.
- A source entry for a 1932 monograph on Pavlovian conditioning → not time-bounded by default; the source's date is captured in `year`.

## Notes

This lens does not generate findings on its own; it tags. Findings about staleness are produced by a separate scheduled check that reads the tag. The tag is the cheap, persistent signal; the finding is the action.

## Related lenses

- Meta-lens: [[lens-lens]]
- Runs after [[lens-confidence]], before [[lens-edit-hardness]].
