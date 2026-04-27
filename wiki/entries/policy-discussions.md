---
id: policy-discussions
title: "Policy — Discussions"
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
covers: "Discussions are bounded to 5 rounds (3 in contentious domains); termination protocols (`content-quorum`, `meta-rule-quorum`, `human-escalation`, `confirmed-vote`) are selected by the disputed object's kind; discussions inactive past 4 weeks raise `finding-stale-discussion`."
linted_by: [stale-discussion, discussion-round-bound-exceeded]
---

# Policy — Discussions

## Lead

Discussions are bounded to 5 rounds (3 in contentious domains); termination protocols (`content-quorum`, `meta-rule-quorum`, `human-escalation`, `confirmed-vote`) are selected by the disputed object's kind; discussions inactive past 4 weeks raise `finding-stale-discussion`.

## Rule

The binding rule covered by this policy is specified in [`../../docs/spec/specification.md`](../../docs/spec/specification.md) at section **§22**. Until policy-tier prose is ratified separately, the spec section is authoritative.

## Rationale

Disputes resolve in finite time or become findings; nothing dangles in chat state. Round bounds force termination; protocols match the gravity of the disputed object.

## How violation is detected

Lint rules from §20.2 that enforce this policy:

- `stale-discussion` (§20.2)
- `discussion-round-bound-exceeded` (§20.2)

## Promotion history

- 2026-04-27: created at seed as `policy` (bootstrap; see [`../../docs/spec/specification.md`](../../docs/spec/specification.md) §29.2).

## Notes

This entry is a **seed stub**. The spec is the authority during seed (§1.3); this entry exists to make the rule citeable from other entries and to reserve the slug. Flesh out the rule, examples, and edge cases as findings accumulate.
