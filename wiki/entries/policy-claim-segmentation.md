---
id: policy-claim-segmentation
title: "Policy — Claim Segmentation"
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
covers: "A sentence splits into multiple claim entries when it carries multiple independently verifiable assertions, when the assertions are qualified differently, or when the assertion is the locus of a known disagreement; otherwise prefer the coarser claim."
linted_by: []
---

# Policy — Claim Segmentation

## Lead

A sentence splits into multiple claim entries when it carries multiple independently verifiable assertions, when the assertions are qualified differently, or when the assertion is the locus of a known disagreement; otherwise prefer the coarser claim.

## Rule

The binding rule covered by this policy is specified in [`../../docs/spec/specification.md`](../../docs/spec/specification.md) at section **§10.1.1**. Until policy-tier prose is ratified separately, the spec section is authoritative.

## Rationale

Atomicity at the wrong scale produces either un-citeable mush (too coarse) or a fog of fragments (too fine). The default of `prefer the coarser claim` errs on the safer side because joining is easier than splitting.

## How violation is detected

_No named lint rule directly enforces this policy in the catalog (§20.2). Violations surface through closeout review or via findings raised by editor or assessment runs._

## Promotion history

- 2026-04-27: created at seed as `policy` (bootstrap; see [`../../docs/spec/specification.md`](../../docs/spec/specification.md) §29.2).

## Notes

This entry is a **seed stub**. The spec is the authority during seed (§1.3); this entry exists to make the rule citeable from other entries and to reserve the slug. Flesh out the rule, examples, and edge cases as findings accumulate.
