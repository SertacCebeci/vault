---
id: policy-classification
title: "Policy — Classification"
category: policy
produced_by: lifecycle-bootstrap
domains: [meta]
tags: [policy, seed]
sources: []
aliases: []
created: 2026-04-27
updated: 2026-04-27
confidence: high
status: stub
notability_status: n/a
edit_hardness: restricted
high_stakes_class: none
quality: stub
rule_tier: policy
covers: "Every content entry must be classified by exactly one decision-tree lens, with `classified_by` recording which lens ruled, and the annotation pass must run for every applicable annotation lens."
linted_by: [classification-consistency, infrastructure-classified-by-lens, lens-self-classification]
---

# Policy — Classification

## Lead

Every content entry must be classified by exactly one decision-tree lens, with `classified_by` recording which lens ruled, and the annotation pass must run for every applicable annotation lens.

## Rule

The binding rule covered by this policy is specified in [`../../docs/spec/specification.md`](../../docs/spec/specification.md) at section **§7**. Until policy-tier prose is ratified separately, the spec section is authoritative.

## Rationale

Classification is auditable only if the deciding lens is recorded. Multiple-lens output, missing `classified_by`, or a lens whose `lens_covers_category` does not match the entry's `category` are all symptoms that the decision tree was not run.

## How violation is detected

Lint rules from §20.2 that enforce this policy:

- `classification-consistency` (§20.2)
- `infrastructure-classified-by-lens` (§20.2)
- `lens-self-classification` (§20.2)

## Promotion history

- 2026-04-27: created at seed as `policy` (bootstrap; see [`../../docs/spec/specification.md`](../../docs/spec/specification.md) §29.2).

## Notes

This entry is a **seed stub**. The spec is the authority during seed (§1.3); this entry exists to make the rule citeable from other entries and to reserve the slug. Flesh out the rule, examples, and edge cases as findings accumulate.
