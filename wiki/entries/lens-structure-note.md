---
id: lens-structure-note
title: "Lens — Structure Note"
category: lens
classified_by: lens-lens
domains: [meta]
tags: [classification, organization, clusters]
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
lens_question: "Does the body organize a cluster of entries via annotated links rather than assert facts about a single subject?"
lens_priority: 15
lens_covers_category: structure-note
lens_kind: decision-tree
lens_criteria:
  - "The entry's primary work is organizing prose plus annotated wikilinks into other entries — it does not assert facts about its own subject."
  - "Body has the structure-note section shape (§11.2): Lead, How the cluster is held together, Load-bearing entries, Subregions, Open questions, Cross-cluster bridges."
  - "Frontmatter declares `organizes` (≥5 slugs by convention) and a single `domain_frame`."
  - "Slug uses the reserved prefix `structure-`."
  - "A `## Lead` is required regardless of body size (§5.2.1)."
---

# Lens — Structure Note

## Question

Does the body organize a cluster of entries via annotated links rather than assert facts about a single subject?

## How to apply

Run after [[lens-source]] (priority 10) and before [[lens-disambiguation]] (priority 18). A structure note is the substrate's answer to "how do you carry big information without imposing a hierarchy" (§11.1). Where a `concept` makes claims about *its* subject, a structure note frames *a region of the graph* — naming the dominant axis, the subregions, the load-bearing entries, the unresolved tensions.

A cluster may be held together by more than one structure note, each from a different `domain_frame`. The frame is the lens through which the cluster is being viewed (cognitive-mechanism vs. brain-mechanism vs. teaching-practice). Multiple peer structure notes are encouraged; none is canonical.

If the candidate is asserting facts about itself rather than organizing other entries, fall through to a later lens. If it is doing both — making one principled assertion *and* organizing — split into a `concept` plus a structure note (§3.1 atomicity).

## Worked matches

- A note titled "Misunderstood learning traps" whose body doesn't define a single phenomenon but enumerates and frames `[[fluency-illusion]]`, `[[testing-effect]]`, `[[metacognitive-failure]]` and how they interrelate — slug: `structure-misunderstood-learning-traps`.
- A note framing the memory cluster from the cognitive-mechanism frame, organizing `[[encoding]]`, `[[consolidation]]`, `[[retrieval]]`, `[[forgetting]]` — slug: `structure-memory-learning-theory`.

## Worked non-matches

- [[desirable-difficulty]] — asserts facts about a single principle, even though it links many other entries. Route to [[lens-concept]].
- A `policy-` entry that bundles many sub-rules — route to [[lens-policy-tier]] (priority 5 already fired).

## Notes

[[structure-building]] currently lives at `category: concept` but reads more like a structure note. It is a candidate for reclassification in a later phase — Phase 5 of the spec migration.

## Related lenses

- Meta-lens: [[lens-lens]]
- Previous lens in priority: [[lens-source]]
- Next lens in priority: [[lens-disambiguation]]
