---
id: policy-notability
title: "Policy — Notability"
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
covers: "A unit deserves its own entry iff it has multi-source coverage, routing necessity (≥2 inbound), or a policy carve-out; borderline units are staged as `pending-` and either promoted on later inbound link / second source or retired after 90 days."
linted_by: [notability-stamp-missing]
---

# Policy — Notability

## Lead

A unit deserves its own entry iff it has multi-source coverage, routing necessity (≥2 inbound), or a policy carve-out; borderline units are staged as `pending-` and either promoted on later inbound link / second source or retired after 90 days.

## Rule

The binding rule covered by this policy is specified in [`../../docs/spec/specification.md`](../../docs/spec/specification.md) at section **§8**. Until policy-tier prose is ratified separately, the spec section is authoritative.

## Rationale

Without an explicit gate, the vault floods with one-source asides; without explicit promotion, useful borderline units retire silently. This policy makes both paths legible.

## How violation is detected

Lint rules from §20.2 that enforce this policy:

- `notability-stamp-missing` (§20.2)

## Promotion history

- 2026-04-27: created at seed as `policy` (bootstrap; see [`../../docs/spec/specification.md`](../../docs/spec/specification.md) §29.2).

## Notes

This entry is a **seed stub**. The spec is the authority during seed (§1.3); this entry exists to make the rule citeable from other entries and to reserve the slug. Flesh out the rule, examples, and edge cases as findings accumulate.
