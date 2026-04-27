---
id: policy-high-stakes
title: "Policy — High-Stakes"
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
covers: "Claims classified `medical`, `legal`, `safety`, or `identifiable-individual` carry a higher evidence floor; below-floor high-stakes claims are replaced by a placeholder and a blocking finding rather than persisted."
linted_by: [high-stakes-floor-violation]
---

# Policy — High-Stakes

## Lead

Claims classified `medical`, `legal`, `safety`, or `identifiable-individual` carry a higher evidence floor; below-floor high-stakes claims are replaced by a placeholder and a blocking finding rather than persisted.

## Rule

The binding rule covered by this policy is specified in [`../../docs/spec/specification.md`](../../docs/spec/specification.md) at section **§14**. Until policy-tier prose is ratified separately, the spec section is authoritative.

## Rationale

The asymmetric removal regime is the wikipedia-MEDRS / BLP analog: weak evidence on consequential claims is more harmful than absence. Better a hole and a finding than a vague assertion.

## How violation is detected

Lint rules from §20.2 that enforce this policy:

- `high-stakes-floor-violation` (§20.2)

## Promotion history

- 2026-04-27: created at seed as `policy` (bootstrap; see [`../../docs/spec/specification.md`](../../docs/spec/specification.md) §29.2).

## Notes

This entry is a **seed stub**. The spec is the authority during seed (§1.3); this entry exists to make the rule citeable from other entries and to reserve the slug. Flesh out the rule, examples, and edge cases as findings accumulate.
