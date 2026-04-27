---
id: lens-evidence-grade
title: "Lens — Evidence Grade"
category: lens
classified_by: lens-lens
domains: [meta]
tags: [annotation, evidence, sourcing]
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
lens_question: "What is the strongest source backing this claim or relation?"
lens_priority: 210
lens_covers_category: evidence_grade
lens_kind: annotation
lens_criteria:
  - "Stamps `evidence_grade` ∈ {A, B, C, D} on claim and relation entries."
  - "Defaults to the lowest grade the claim's sources support."
  - "Multi-source claims take the strongest grade unless the sources contradict, in which case `confidence: contested` is set."
  - "Skipped silently for kinds where evidence-grade does not apply (concept, illustration, application, entity, process, insight, source, structure-note, lens, policy, …)."
---

# Lens — Evidence Grade

## Question

What is the strongest source backing this claim or relation?

## How to apply

Run during the annotation pass after the decision-tree pass has set `category`. Applies only to `claim` and `relation` entries. Stamps the `evidence_grade` field; produces no finding by itself, but downstream lenses and policies (notably [[lens-high-stakes]] and `policy-content-quality`) read the grade to decide further treatment.

The grade scale (§10.1.2):

| grade | meaning |
|---|---|
| `A` | Primary literature: peer-reviewed empirical studies, meta-analyses, or original derivations from those. |
| `B` | Secondary scholarly: textbooks, review articles, expert syntheses citing primary work. |
| `C` | Popular or applied: well-regarded practitioner books, expert essays, applied references. |
| `D` | Anecdotal: single-case reports, blog posts, opinion pieces, claims without traceable evidence. |

Rules:

1. A claim defaults to the **lowest** grade its sources support.
2. Multi-source claims take the **strongest** grade among their sources.
3. If two sources disagree by more than one grade (e.g., one A, one D), set `confidence: contested` and keep the higher grade.
4. A claim below an active `evidence_grade_floor` (per its domain entry) emits `finding-evidence-below-floor-{slug}`. In a [[lens-confidence|contentious]] domain, this finding is blocking.

## Worked stampings

- A claim citing a peer-reviewed RCT → `A`.
- A claim citing only [[make-it-stick]] (a popular synthesis of primary work) → `C` initially; upgrades to `B` if a later review article is added; upgrades to `A` if the underlying primary study is added directly.
- A claim citing only a blog post → `D`. Likely fails an evidence floor and is held until a higher grade is found.

## Notes

Evidence grade describes the **evidence**; high-stakes class describes the **action when evidence is weak** (§14.4). The two are orthogonal axes — graders need not know the high-stakes class to grade evidence.

## Related lenses

- Meta-lens: [[lens-lens]]
- Runs after [[lens-notability]], before [[lens-high-stakes]].
- Read by: [[lens-high-stakes]] (asymmetric removal regime), [[lens-confidence]].
