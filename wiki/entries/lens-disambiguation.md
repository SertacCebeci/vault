---
id: lens-disambiguation
title: "Lens — Disambiguation"
category: lens
classified_by: lens-lens
domains: [meta]
tags: [classification, routing, polysemy]
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
lens_question: "Is this entry a routing target for a polysemous slug?"
lens_priority: 18
lens_covers_category: disambiguation
lens_kind: decision-tree
lens_criteria:
  - "The entry exists because more than one entry in the vault could naturally claim the same base slug."
  - "Body lists 2+ variants with one-line distinguishers — no substantive content of its own."
  - "Frontmatter declares a `variants` list with at least 2 entries, each pairing a slug with a distinguisher."
  - "Slug uses the reserved prefix `disambiguation-` followed by the contested base slug."
---

# Lens — Disambiguation

## Question

Is this entry a routing target for a polysemous slug?

## How to apply

Run after [[lens-structure-note]] (priority 15) and before [[lens-illustration]] (priority 20). A disambiguation entry exists for one reason: the bare base slug (e.g., `mercury`, `transfer`) could refer to two or more notable subjects in the vault. The disambiguation entry holds the bare base slug while each variant lives at a disambiguated slug (`mercury-element`, `mercury-planet`).

Apply by checking:

1. Does the slug correspond to a term that could mean more than one thing in this vault's domains?
2. Does the body do *only* navigation work — listing variants with one-line distinguishers — and *no* substantive synthesis?
3. Are there at least two variants in `wiki/entries/` that the entry routes to?

A disambiguation entry's body is short by design. Add inline hatnotes (`> For X, see [[other-variant]]. For routing, see [[disambiguation-base]].`) at the top of each variant entry per §6.4 step 4.

## Worked matches

- `disambiguation-transfer` — routes between `[[transfer-learning]]` (educational-psychology concept) and `[[transfer-finance]]` (financial concept).
- `disambiguation-memory` — routes between several frame-specific entries on memory if the cluster grows enough to warrant variants.

## Worked non-matches

- [[chunking]] — single concept, no polysemy. Route to [[lens-concept]].
- A structure note that organizes a cluster — even if it touches polysemous terms in its variants list, its work is organizing, not routing. Route to [[lens-structure-note]].

## Notes

A disambiguation is always notable (§8.5) — its existence is justified by the variants it routes to. Lint `disambiguation-orphan` flags a disambiguation entry whose variants have all been renamed or merged.

## Related lenses

- Meta-lens: [[lens-lens]]
- Previous lens in priority: [[lens-structure-note]]
- Next lens in priority: [[lens-illustration]]
