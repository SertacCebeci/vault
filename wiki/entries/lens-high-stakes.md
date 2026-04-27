---
id: lens-high-stakes
title: "Lens — High-Stakes"
category: lens
classified_by: lens-lens
domains: [meta]
tags: [annotation, safety, asymmetric-removal]
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
lens_question: "Is acting on this claim consequential for medical, legal, safety, or named-individual interests?"
lens_priority: 220
lens_covers_category: high_stakes_class
lens_kind: annotation
lens_criteria:
  - "Stamps `high_stakes_class` ∈ {none, medical, legal, safety, identifiable-individual} on every claim entry and on concept entries that contain inline claims."
  - "Multi-class is not allowed; ties take the highest-stakes class (medical > legal > safety > identifiable-individual)."
  - "Triggers the asymmetric removal regime (§14.3) when the stamped class is non-`none` AND `evidence_grade` is below the floor for that class (v0: B for medical/legal/safety, A for identifiable-individual)."
---

# Lens — High-Stakes

## Question

Is acting on this claim consequential enough that weak evidence becomes unsafe?

## How to apply

Run during the annotation pass after [[lens-evidence-grade]] has stamped the grade. The lens reads the claim's content (and where applicable the body of the parent concept) and stamps `high_stakes_class`.

Class criteria (§14.2):

- **`medical`** — claim is about a human-health intervention, condition, or biological mechanism, *and* is consequential for choosing or refusing care. Abstract physiology that does not direct care is `none`.
- **`legal`** — claim asserts a legal status, requirement, or consequence, *and* acting on the claim could expose a reader to legal risk.
- **`safety`** — claim is about a procedure, threshold, or condition where being wrong creates physical risk to a human.
- **`identifiable-individual`** — claim identifies a specific living person and asserts something contestable about them (actions, views, character, associations). The vault's analog of Wikipedia's BLP rule.
- **`none`** — none of the above.

If a claim plausibly fits two classes, stamp the highest-stakes one (medical > legal > safety > identifiable-individual).

## The asymmetric removal regime

When a claim is stamped non-`none` AND its `evidence_grade` is below the floor, the regime fires (§14.3.1):

1. The claim is **not** written into the staging entry. A placeholder `> [HIGH-STAKES CLAIM REMOVED — see finding-{slug}]` is left at the location, where `{slug}` is the slug of the resulting `finding-high-stakes-removal-*` entry.
2. A `finding-high-stakes-removal-` is emitted with `severity: blocking`.
3. The parent entry's `confidence` is downgraded by one tier until the finding resolves.
4. Retrieval treats the placeholder as a non-fragment.

Reinstatement requires either a higher-graded source or an explicit `wontfix` justified at meta-rule quorum.

## Worked stampings

- A claim about the dosage of a stimulant for ADHD treatment → `medical`. If only D-grade sources, asymmetric removal fires.
- A claim about the legal liability of a teaching practice → `legal`.
- A claim about a specific named educator's pedagogical methodology → `identifiable-individual`. Floor: A.
- A claim that "spaced practice improves long-term retention" → `none`. Acting on a wrong answer here makes a learner less efficient, not unsafe.

## Notes

Concept entries that contain inline claims inherit a stamp from their content: if any of their claims is stamped non-`none`, the concept's `high_stakes_class` rises to that level. The class is **not** retrieved from the concept's overall topic; it is computed from the actual assertions inside.

## Related lenses

- Meta-lens: [[lens-lens]]
- Runs after [[lens-evidence-grade]], before [[lens-confidence]].
- Read by: [[lens-edit-hardness]] (raises tier when class is non-`none`).
