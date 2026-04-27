---
id: policy-edit-hardness
title: "Policy — Edit Hardness"
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
covers: "The five tiers (`open`, `confirmed`, `extended-confirmed`, `restricted`, `locked`) gate writes by reputation and (for `extended-confirmed`) declared scope; defaults are set by kind (§9.2), raised by domain inheritance, raised by high-stakes class, and never lowered by ordinary edits."
linted_by: [edit-hardness-consistency]
---

# Policy — Edit Hardness

## Lead

The five tiers (`open`, `confirmed`, `extended-confirmed`, `restricted`, `locked`) gate writes by reputation and (for `extended-confirmed`) declared scope; defaults are set by kind (§9.2), raised by domain inheritance, raised by high-stakes class, and never lowered by ordinary edits.

## Rule

The binding rule covered by this policy is specified in [`../../docs/spec/specification.md`](../../docs/spec/specification.md) at section **§9**. Until policy-tier prose is ratified separately, the spec section is authoritative.

## Rationale

Edit-hardness is the population's permission lattice; a tier is a claim about how rare and how scrutinized writes to this entry should be.

## How violation is detected

Lint rules from §20.2 that enforce this policy:

- `edit-hardness-consistency` (§20.2)

## Promotion history

- 2026-04-27: created at seed as `policy` (bootstrap; see [`../../docs/spec/specification.md`](../../docs/spec/specification.md) §29.2).

## Notes

This entry is a **seed stub**. The spec is the authority during seed (§1.3); this entry exists to make the rule citeable from other entries and to reserve the slug. Flesh out the rule, examples, and edge cases as findings accumulate.
