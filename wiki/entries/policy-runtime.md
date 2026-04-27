---
id: policy-runtime
title: "Policy — Runtime"
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
covers: "The `runner/` directory holds the runtime; it is the only enforcer of write-scope, reputation gates, edit-hardness, and pending-changes routing; it does not decide content, classification, or promotion."
linted_by: []
---

# Policy — Runtime

## Lead

The `runner/` directory holds the runtime; it is the only enforcer of write-scope, reputation gates, edit-hardness, and pending-changes routing; it does not decide content, classification, or promotion.

## Rule

The binding rule covered by this policy is specified in [`../../docs/spec/specification.md`](../../docs/spec/specification.md) at section **§26.6**. Until policy-tier prose is ratified separately, the spec section is authoritative.

## Rationale

The boundary between vault state (entries) and runtime behavior (the writer-gate) must be sharp; otherwise it becomes impossible to reason about either.

## How violation is detected

_No named lint rule directly enforces this policy in the catalog (§20.2). Violations surface through closeout review or via findings raised by editor or assessment runs._

## Promotion history

- 2026-04-27: created at seed as `policy` (bootstrap; see [`../../docs/spec/specification.md`](../../docs/spec/specification.md) §29.2).

## Notes

This entry is a **seed stub**. The spec is the authority during seed (§1.3); this entry exists to make the rule citeable from other entries and to reserve the slug. Flesh out the rule, examples, and edge cases as findings accumulate.
