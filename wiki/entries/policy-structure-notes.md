---
id: policy-structure-notes
title: "Policy — Structure Notes"
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
covers: "A structure note is required for every connected component of >8 content entries; the body must follow the section template (Lead, How the cluster is held together, Load-bearing entries, Subregions, Open questions, Cross-cluster bridges)."
linted_by: [structure-note-coverage, structure-note-low-link-density]
---

# Policy — Structure Notes

## Lead

A structure note is required for every connected component of >8 content entries; the body must follow the section template (Lead, How the cluster is held together, Load-bearing entries, Subregions, Open questions, Cross-cluster bridges).

## Rule

The binding rule covered by this policy is specified in [`../../docs/spec/specification.md`](../../docs/spec/specification.md) at section **§11**. Until policy-tier prose is ratified separately, the spec section is authoritative.

## Rationale

Big clusters need narrative substrate or they degrade into bag-of-entries. The structure-note pattern is how the vault carries cluster-level information without imposing a hierarchy.

## How violation is detected

Lint rules from §20.2 that enforce this policy:

- `structure-note-coverage` (§20.2)
- `structure-note-low-link-density` (§20.2)

## Promotion history

- 2026-04-27: created at seed as `policy` (bootstrap; see [`../../docs/spec/specification.md`](../../docs/spec/specification.md) §29.2).

## Notes

This entry is a **seed stub**. The spec is the authority during seed (§1.3); this entry exists to make the rule citeable from other entries and to reserve the slug. Flesh out the rule, examples, and edge cases as findings accumulate.
