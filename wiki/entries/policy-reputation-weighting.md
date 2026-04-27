---
id: policy-reputation-weighting
title: "Policy — Reputation Weighting"
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
covers: "Reputation events (gain and loss) and their weights are catalogued here; the external anchor (human review and thesis-eval results) counts for 3× internal-event weight at v0 and is recalibrated annually or when policy-thesis-eval registers a variance-reduction change."
linted_by: []
---

# Policy — Reputation Weighting

## Lead

Reputation events (gain and loss) and their weights are catalogued here; the external anchor (human review and thesis-eval results) counts for 3× internal-event weight at v0 and is recalibrated annually or when policy-thesis-eval registers a variance-reduction change.

## Rule

The binding rule covered by this policy is specified in [`../../docs/spec/specification.md`](../../docs/spec/specification.md) at section **§9.6**. Until policy-tier prose is ratified separately, the spec section is authoritative.

## Rationale

Reputation drives every edit-hardness gate, so its calibration is itself a load-bearing decision. The external anchor is what keeps in-population events from drifting.

## How violation is detected

_No named lint rule directly enforces this policy in the catalog (§20.2). Violations surface through closeout review or via findings raised by editor or assessment runs._

## Promotion history

- 2026-04-27: created at seed as `policy` (bootstrap; see [`../../docs/spec/specification.md`](../../docs/spec/specification.md) §29.2).

## Notes

This entry is a **seed stub**. The spec is the authority during seed (§1.3); this entry exists to make the rule citeable from other entries and to reserve the slug. Flesh out the rule, examples, and edge cases as findings accumulate.
