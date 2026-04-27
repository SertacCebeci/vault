---
id: policy-agent-lifecycle
title: "Policy — Agent Lifecycle"
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
covers: "An agent's lifecycle has three named protocols: `lifecycle-agent-create`, `lifecycle-agent-mutate`, `lifecycle-agent-retire`; each requires an explicit run entry and (for create/retire) quorum approval."
linted_by: []
---

# Policy — Agent Lifecycle

## Lead

An agent's lifecycle has three named protocols: `lifecycle-agent-create`, `lifecycle-agent-mutate`, `lifecycle-agent-retire`; each requires an explicit run entry and (for create/retire) quorum approval.

## Rule

The binding rule covered by this policy is specified in [`../../docs/spec/specification.md`](../../docs/spec/specification.md) at section **§16.3**. Until policy-tier prose is ratified separately, the spec section is authoritative.

## Rationale

Agents are the writes that change the vault's behavior; the lifecycle gates them so a population's composition does not drift quietly.

## How violation is detected

_No named lint rule directly enforces this policy in the catalog (§20.2). Violations surface through closeout review or via findings raised by editor or assessment runs._

## Promotion history

- 2026-04-27: created at seed as `policy` (bootstrap; see [`../../docs/spec/specification.md`](../../docs/spec/specification.md) §29.2).

## Notes

This entry is a **seed stub**. The spec is the authority during seed (§1.3); this entry exists to make the rule citeable from other entries and to reserve the slug. Flesh out the rule, examples, and edge cases as findings accumulate.
