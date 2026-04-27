---
id: policy-lint
title: "Policy — Lint"
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
covers: "Every named lint rule is enforced on every write that affects an entry under its scope, on every closeout, and on a daily full pass; advisory findings are recorded for later review while blocking findings stop the offending write or merge."
linted_by: [slug-uniqueness, id-filename-mismatch, unknown-category, broken-wikilink]
---

# Policy — Lint

## Lead

Every named lint rule is enforced on every write that affects an entry under its scope, on every closeout, and on a daily full pass; advisory findings are recorded for later review while blocking findings stop the offending write or merge.

## Rule

The binding rule covered by this policy is specified in [`../../docs/spec/specification.md`](../../docs/spec/specification.md) at section **§20**. Until policy-tier prose is ratified separately, the spec section is authoritative.

## Rationale

Lint is the vault's continuous self-check. Without lint as a first-class infrastructure citizen, schema drift accumulates silently.

## How violation is detected

Lint rules from §20.2 that enforce this policy:

- `slug-uniqueness` (§20.2)
- `id-filename-mismatch` (§20.2)
- `unknown-category` (§20.2)
- `broken-wikilink` (§20.2)

## Promotion history

- 2026-04-27: created at seed as `policy` (bootstrap; see [`../../docs/spec/specification.md`](../../docs/spec/specification.md) §29.2).

## Notes

This entry is a **seed stub**. The spec is the authority during seed (§1.3); this entry exists to make the rule citeable from other entries and to reserve the slug. Flesh out the rule, examples, and edge cases as findings accumulate.
