---
id: lens-relation
title: "Lens — Relation"
category: lens
classified_by: lens-lens
domains: [meta]
tags: [classification, edges, predicates]
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
lens_question: "Is this entry a typed, directed edge between two other entries with its own evidence?"
lens_priority: 22
lens_covers_category: relation
lens_kind: decision-tree
lens_criteria:
  - "The entry asserts a relationship between exactly two endpoint entries declared in `from` and `to`."
  - "The predicate is one of the load-bearing set: `supports`, `contradicts`, `instance-of`, `supersedes`, `depends-on` (§10.2.1)."
  - "Frontmatter declares `evidence_grade` and `evidence_pointers` — a relation carries its own evidence, not just its endpoints'."
  - "Slug follows the deterministic pattern `relation-{from-slug}-{predicate}-{to-slug}` (§10.2.3)."
---

# Lens — Relation

## Question

Is this entry a typed, directed edge between two other entries, carrying its own evidence?

## How to apply

Run after [[lens-illustration]] (priority 20) and before [[lens-claim]] (priority 25). A relation is the formalized version of a load-bearing connection: it has a typed predicate, two named endpoints, and its own evidence. Inline `## Connections` bullets with informal predicates ("Related to", "Coined by", "Used in") **do not** require a relation entry — those are wikilinks with annotations, not edges in the graph.

Formalize as a relation entry when at least one of (§10.2.2):

1. The predicate is in the load-bearing set above.
2. The relation carries evidence not visible in either endpoint.
3. The relation is itself the locus of a discussion or contradiction.

A relation is **not**:
- a passing wikilink with no predicate,
- an `is-a` link (use `instance-of`),
- a `related-to` link (just a wikilink).

Slugs follow the deterministic pattern so they do not duplicate. Two relations between the same endpoints with the same predicate are the same relation; merge them.

## Worked matches

- `relation-spaced-practice-supports-long-term-retention` — `from: spaced-practice`, `to: long-term-retention`, `predicate: supports`, `evidence_grade: A` (illustrative; both endpoint slugs would need to exist).
- `relation-learning-styles-myth-contradicts-vak-classification` — `from: [[learning-styles-myth]]`, `to: vak-classification`, `predicate: contradicts`.
- `relation-leitner-box-instance-of-spaced-repetition` — `from: [[leitner-box]]`, `to: [[spaced-repetition]]`, `predicate: instance-of`.

## Worked non-matches

- A `## Connections` line "Related to: [[chunking]]" in a concept entry — informal predicate, no separate relation entry needed.
- An `insight` that names a non-trivial relationship between 2+ concepts — the insight *is* the synthesized claim about the relationship, not the typed edge. Route to [[lens-insight]].

## Notes

A relation entry merge fails closed: `predicate`, `from`, `to` must agree (§19.11). Mismatch is a blocking finding. Evidence grade combines as the strongest of the two; if the two sides disagree by more than one grade, `confidence: contested` is set.

## Related lenses

- Meta-lens: [[lens-lens]]
- Previous lens in priority: [[lens-illustration]]
- Next lens in priority: [[lens-claim]]
