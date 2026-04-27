---
id: policy-reingestion
title: "Policy — Reingestion"
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
covers: "A previously-completed chapter may be reingested by reverting its row to `in-progress`, running phases 1–3 fresh, and treating the existing entry as the richer side at merge time (the reingested version is a depth upgrade on prose, not a replacement on connections)."
linted_by: []
---

# Policy — Reingestion

## Lead

A previously-completed chapter may be reingested by reverting its row to `in-progress`, running phases 1–3 fresh, and treating the existing entry as the richer side at merge time (the reingested version is a depth upgrade on prose, not a replacement on connections).

## Rule

The binding rule covered by this policy is specified in [`../../docs/spec/specification.md`](../../docs/spec/specification.md) at section **§18**. Until policy-tier prose is ratified separately, the spec section is authoritative.

## Rationale

Reingestion is how a chapter benefits from later context without erasing the connections accumulated since it first ran. The depth-upgrade rule is what makes reingestion safe.

## How violation is detected

_No named lint rule directly enforces this policy in the catalog (§20.2). Violations surface through closeout review or via findings raised by editor or assessment runs._

## Promotion history

- 2026-04-27: created at seed as `policy` (bootstrap; see [`../../docs/spec/specification.md`](../../docs/spec/specification.md) §29.2).

## Notes

This entry is a **seed stub**. The spec is the authority during seed (§1.3); this entry exists to make the rule citeable from other entries and to reserve the slug. Flesh out the rule, examples, and edge cases as findings accumulate.
