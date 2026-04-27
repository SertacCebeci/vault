---
id: policy-entry-layout
title: "Policy — Entry Layout"
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
covers: "Every entry's body follows the section template appropriate to its kind; a `## Lead` is required when body length exceeds the threshold and unconditionally for structure notes, sources, and entries in contentious domains."
linted_by: [lead-missing, lead-too-long, low-quality-lead, body-section-order]
---

# Policy — Entry Layout

## Lead

Every entry's body follows the section template appropriate to its kind; a `## Lead` is required when body length exceeds the threshold and unconditionally for structure notes, sources, and entries in contentious domains.

## Rule

The binding rule covered by this policy is specified in [`../../docs/spec/specification.md`](../../docs/spec/specification.md) at section **§5**. Until policy-tier prose is ratified separately, the spec section is authoritative.

## Rationale

Retrieval returns leads first; the lead is therefore a load-bearing artifact, not optional decoration. Section order makes orthogonality predictable for downstream tools.

## How violation is detected

Lint rules from §20.2 that enforce this policy:

- `lead-missing` (§20.2)
- `lead-too-long` (§20.2)
- `low-quality-lead` (§20.2)
- `body-section-order` (§20.2)

## Promotion history

- 2026-04-27: created at seed as `policy` (bootstrap; see [`../../docs/spec/specification.md`](../../docs/spec/specification.md) §29.2).

## Notes

This entry is a **seed stub**. The spec is the authority during seed (§1.3); this entry exists to make the rule citeable from other entries and to reserve the slug. Flesh out the rule, examples, and edge cases as findings accumulate.
