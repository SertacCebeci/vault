---
id: lens-claim
title: "Lens — Claim"
category: lens
classified_by: lens-lens
domains: [meta]
tags: [classification, atoms, evidence]
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
lens_question: "Is this entry a single atomic assertion with declared evidence?"
lens_priority: 25
lens_covers_category: claim
lens_kind: decision-tree
lens_criteria:
  - "Frontmatter declares `claim_text` as a single declarative sentence."
  - "Frontmatter declares `evidence_grade`, `evidence_pointers`, `asserts_about`, `verifiable`."
  - "The assertion is segmented per `policy-claim-segmentation` (§10.1.1) — one verifiable atom, neither too coarse nor fragmented."
  - "Slug uses the reserved prefix `claim-`."
  - "The claim either deserves its own entry per §8.5 (multi-source, contested, or carries `high_stakes_class != none`) or is referenced from another entry."
---

# Lens — Claim

## Question

Is this entry a single atomic assertion with its own declared evidence?

## How to apply

Run after [[lens-relation]] (priority 22) and before [[lens-application]] (priority 30). A claim is the smallest verifiable unit the vault recognizes (§10.1). It carries one assertion in `claim_text`, one or more evidence pointers, and a grade.

Most claims live *inside* concept entries as sentences with citations — they do **not** need their own claim entry. Promote a claim to its own `claim-{slug}` entry only when (§8.5):

1. The claim has multiple inbound `supports` or `contradicts` relations, **or**
2. The claim carries `high_stakes_class != none`, **or**
3. The claim is the locus of an active discussion or contradiction.

Apply the segmentation rule from `policy-claim-segmentation`:

- Split when a sentence carries more than one verifiable assertion that could be independently true or false.
- Split when assertions are qualified differently ("X is true under condition Y, but Z under condition W").
- Do **not** split when the parts are bound by causation or sequence.
- When uncertain, prefer the coarser claim — fragmentation is harder to reverse.

## Worked matches

- `claim-spaced-practice-improves-long-term-retention-vs-massed` — single assertion, multiple primary-literature evidence pointers, multiple inbound `supports` relations from related concepts. Promoted to its own entry.
- A medical claim about an intervention's efficacy with `high_stakes_class: medical` — promoted regardless of citation count because of the high-stakes class.

## Worked non-matches

- A sentence "Spaced practice improves long-term retention" inside the body of a `spaced-practice` concept entry with a citation — lives inline, no claim entry needed.
- A relationship between two entries with evidence, e.g. "spaced practice supports long-term retention" — that's a [[lens-relation]] match (the predicate makes it an edge, not a claim).
- A multi-clause sentence asserting two independent things — split first, then each piece lands separately.

## Notes

`evidence_grade` defaults to the lowest grade the claim's sources support. Multi-source claims take the strongest grade unless contradiction (in which case `confidence: contested` is set; see [[lens-evidence-grade]]). When `evidence_grade` falls below an active high-stakes floor (§14.3), the asymmetric removal regime fires — the claim is replaced by a placeholder and a blocking finding is opened.

## Related lenses

- Meta-lens: [[lens-lens]]
- Previous lens in priority: [[lens-relation]]
- Next lens in priority: [[lens-application]]
- Annotation lenses that stamp this entry: [[lens-evidence-grade]], [[lens-high-stakes]], [[lens-confidence]], [[lens-recency]]
