---
id: policy-archival
title: "Policy — Archival"
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
covers: "Infrastructure entries (runs, resolved findings, closed discussions, retired notifications) older than 30 days are moved to `wiki/_meta/archive/{kind}/{year}/{month}/`; runs older than 30 days are also rolled up into `run-rollup-{agent}-{period}` summaries."
linted_by: []
---

# Policy — Archival

## Lead

Infrastructure entries (runs, resolved findings, closed discussions, retired notifications) older than 30 days are moved to `wiki/_meta/archive/{kind}/{year}/{month}/`; runs older than 30 days are also rolled up into `run-rollup-{agent}-{period}` summaries.

## Rule

The binding rule covered by this policy is specified in [`../../docs/spec/specification.md`](../../docs/spec/specification.md) at section **§26.3**. Until policy-tier prose is ratified separately, the spec section is authoritative.

## Rationale

Without aggressive archival, the entry pile is dominated by `run-*` and `notification-*` entries within weeks. Content lives forever; infrastructure ages out of the hot index.

## How violation is detected

_No named lint rule directly enforces this policy in the catalog (§20.2). Violations surface through closeout review or via findings raised by editor or assessment runs._

## Promotion history

- 2026-04-27: created at seed as `policy` (bootstrap; see [`../../docs/spec/specification.md`](../../docs/spec/specification.md) §29.2).

## Notes

This entry is a **seed stub**. The spec is the authority during seed (§1.3); this entry exists to make the rule citeable from other entries and to reserve the slug. Flesh out the rule, examples, and edge cases as findings accumulate.
