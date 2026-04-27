---
id: policy-thesis-eval
title: "Policy — Thesis Evaluation"
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
covers: "A fixed panel of verifiable tasks is run periodically with and without vault context; the headline metric is variance reduction (var(unaided) − var(vault-augmented)), and the panel is amended only by meta-rule quorum."
linted_by: []
---

# Policy — Thesis Evaluation

## Lead

A fixed panel of verifiable tasks is run periodically with and without vault context; the headline metric is variance reduction (var(unaided) − var(vault-augmented)), and the panel is amended only by meta-rule quorum.

## Rule

The binding rule covered by this policy is specified in [`../../docs/spec/specification.md`](../../docs/spec/specification.md) at section **§28.5**. Until policy-tier prose is ratified separately, the spec section is authoritative.

## Rationale

The vault's reason to exist is variance reduction on consequential tasks. The thesis-eval panel keeps that claim falsifiable.

## How violation is detected

_No named lint rule directly enforces this policy in the catalog (§20.2). Violations surface through closeout review or via findings raised by editor or assessment runs._

## Promotion history

- 2026-04-27: created at seed as `policy` (bootstrap; see [`../../docs/spec/specification.md`](../../docs/spec/specification.md) §29.2).

## Notes

This entry is a **seed stub**. The spec is the authority during seed (§1.3); this entry exists to make the rule citeable from other entries and to reserve the slug. Flesh out the rule, examples, and edge cases as findings accumulate.
