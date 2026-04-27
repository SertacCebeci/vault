---
id: policy-contentious-domain
title: "Policy — Contentious Domain"
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
covers: "Domains flagged `contentious: true` raise floors across every entry whose `domains` includes them: evidence grade one tier stricter, edit-hardness one tier higher, discussion bound from 5→3 rounds, citation mandatory, lead unconditional."
linted_by: [evidence-below-floor, source-missing-contentious, discussion-round-bound-exceeded]
---

# Policy — Contentious Domain

## Lead

Domains flagged `contentious: true` raise floors across every entry whose `domains` includes them: evidence grade one tier stricter, edit-hardness one tier higher, discussion bound from 5→3 rounds, citation mandatory, lead unconditional.

## Rule

The binding rule covered by this policy is specified in [`../../docs/spec/specification.md`](../../docs/spec/specification.md) at section **§15**. Until policy-tier prose is ratified separately, the spec section is authoritative.

## Rationale

Contestation merits stricter handling; the elevations make that explicit and consistent across the contentious domain rather than relying on case-by-case judgement.

## How violation is detected

Lint rules from §20.2 that enforce this policy:

- `evidence-below-floor` (§20.2)
- `source-missing-contentious` (§20.2)
- `discussion-round-bound-exceeded` (§20.2)

## Promotion history

- 2026-04-27: created at seed as `policy` (bootstrap; see [`../../docs/spec/specification.md`](../../docs/spec/specification.md) §29.2).

## Notes

This entry is a **seed stub**. The spec is the authority during seed (§1.3); this entry exists to make the rule citeable from other entries and to reserve the slug. Flesh out the rule, examples, and edge cases as findings accumulate.
