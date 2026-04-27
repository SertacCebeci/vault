---
id: agent-test-thesis-eval-declarative-procedural
title: "Agent Test — Thesis Eval — Declarative Procedural"
category: agent-test
produced_by: lifecycle-agent-test-create
domains: [meta]
tags: [agent-test, thesis-eval, seed, authoritative]
sources: []
aliases: []
created: 2026-04-27
updated: 2026-04-27
confidence: high
status: complete
notability_status: n/a
edit_hardness: extended-confirmed
high_stakes_class: none
quality: c
agent: "[[policy-thesis-eval]]"
question: "Explain why declarative learning and procedural learning have different forgetting curves."
expected_shape: "Names both systems ([[declarative-learning-system]], [[procedural-learning-system]]); names the distinction (declarative: rapid hippocampal indexing, susceptible to interference and relatively rapid…"
authoritative: true
last_run: null
last_result: stale
---

# Agent Test — Thesis Eval — Declarative Procedural

## Lead

Thesis-eval panel task per [[policy-thesis-eval]] (§28.5). The panel compares an unaided baseline (model answers without vault context) against vault-augmented runs (model answers with retrieved context); the headline metric is variance reduction.

## Question

Explain why declarative learning and procedural learning have different forgetting curves.

## Expected answer shape

Names both systems ([[declarative-learning-system]], [[procedural-learning-system]]); names the distinction (declarative: rapid hippocampal indexing, susceptible to interference and relatively rapid decay without retrieval; procedural: slow incremental tuning of basal-ganglia/cerebellar pathways, much more durable once consolidated); cites the [[declarative-procedural-seesaw]] or equivalent.

## Baselines

- **Unaided:** TBD — to be recorded once during seed by running a baseline model N times against this question with no vault context. Variance over N runs is the reference variance.
- **Vault-augmented:** TBD — to be re-run periodically (per [[policy-assessment]] cadence). Per-run variance is compared to the unaided baseline; reduction is logged in the thesis-eval dashboard.

## Notes

This task is `authoritative: true`. Amendments to the panel itself require meta-rule quorum (§9.4). Per-task amendments may be made via the same rule.
