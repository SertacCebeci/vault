---
id: policy-merge
title: "Policy — Merge"
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
covers: "Per-kind merge rules govern how a temp file combines with an existing entry: prose consolidation for `concept` and `insight`, structured append for `entity`, `application`, `process`, replace for `illustration`, append-only sections for `structure-note`, and immutability for runs/findings/discussions/notifications."
linted_by: [agent-direct-merge, immutable-merge]
---

# Policy — Merge

## Lead

Per-kind merge rules govern how a temp file combines with an existing entry: prose consolidation for `concept` and `insight`, structured append for `entity`, `application`, `process`, replace for `illustration`, append-only sections for `structure-note`, and immutability for runs/findings/discussions/notifications.

## Rule

The binding rule covered by this policy is specified in [`../../docs/spec/specification.md`](../../docs/spec/specification.md) at section **§19**. Until policy-tier prose is ratified separately, the spec section is authoritative.

## Rationale

Merge rules protect accumulated connections from being overwritten by fresh blind reads. The append-only convention for `## Connections`, `## Sources`, structure-note `## Load-bearing entries`, etc. is the canonical mechanism.

## How violation is detected

Lint rules from §20.2 that enforce this policy:

- `agent-direct-merge` (§20.2)
- `immutable-merge` (§20.2)

## Promotion history

- 2026-04-27: created at seed as `policy` (bootstrap; see [`../../docs/spec/specification.md`](../../docs/spec/specification.md) §29.2).

## Notes

This entry is a **seed stub**. The spec is the authority during seed (§1.3); this entry exists to make the rule citeable from other entries and to reserve the slug. Flesh out the rule, examples, and edge cases as findings accumulate.
