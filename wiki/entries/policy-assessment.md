---
id: policy-assessment
title: "Policy — Assessment"
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
covers: "Periodic assessment passes compute coverage, internal-consistency, and source-grounding signals; results are recorded in `run-assess-*` entries and projected onto domain dashboards."
linted_by: []
---

# Policy — Assessment

## Lead

Periodic assessment passes compute coverage, internal-consistency, and source-grounding signals; results are recorded in `run-assess-*` entries and projected onto domain dashboards.

## Rule

The binding rule covered by this policy is specified in [`../../docs/spec/specification.md`](../../docs/spec/specification.md) at section **§28**. Until policy-tier prose is ratified separately, the spec section is authoritative.

## Rationale

Assessment is how the vault notices its own slow trends — domains saturating, evidence quality drifting, contradictions accumulating. The signals defined here are the early-warning system.

## How violation is detected

_No named lint rule directly enforces this policy in the catalog (§20.2). Violations surface through closeout review or via findings raised by editor or assessment runs._

## Promotion history

- 2026-04-27: created at seed as `policy` (bootstrap; see [`../../docs/spec/specification.md`](../../docs/spec/specification.md) §29.2).

## Notes

This entry is a **seed stub**. The spec is the authority during seed (§1.3); this entry exists to make the rule citeable from other entries and to reserve the slug. Flesh out the rule, examples, and edge cases as findings accumulate.
