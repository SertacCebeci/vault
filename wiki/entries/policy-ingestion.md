---
id: policy-ingestion
title: "Policy — Ingestion"
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
covers: "The four-phase ingestion pipeline (intake, chapter setup, per-sub-section staging, merge, closeout) governs how a raw source becomes vault content."
linted_by: []
---

# Policy — Ingestion

## Lead

The four-phase ingestion pipeline (intake, chapter setup, per-sub-section staging, merge, closeout) governs how a raw source becomes vault content.

## Rule

The binding rule covered by this policy is specified in [`../../docs/spec/specification.md`](../../docs/spec/specification.md) at section **§17**. Until policy-tier prose is ratified separately, the spec section is authoritative.

## Rationale

A predictable per-chapter cycle keeps a long source from drifting out of sync with the vault's classification and merge rules. The phase boundaries are also the natural points at which lint, structure-note coverage, and notability promotion are run.

## How violation is detected

_No named lint rule directly enforces this policy in the catalog (§20.2). Violations surface through closeout review or via findings raised by editor or assessment runs._

## Promotion history

- 2026-04-27: created at seed as `policy` (bootstrap; see [`../../docs/spec/specification.md`](../../docs/spec/specification.md) §29.2).

## Notes

This entry is a **seed stub**. The spec is the authority during seed (§1.3); this entry exists to make the rule citeable from other entries and to reserve the slug. Flesh out the rule, examples, and edge cases as findings accumulate.
