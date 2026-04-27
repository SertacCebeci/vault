---
id: agent-test-thesis-eval-primary-secondary-implications
title: "Agent Test — Thesis Eval — Primary Secondary Implications"
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
question: "List three pedagogical implications of the primary/secondary biological knowledge distinction."
expected_shape: "Three defensible practices (e.g., scaffold secondary material more than primary; expect productive struggle for secondary; use guided rather than discovery instruction for novices; leverage primary…"
authoritative: true
last_run: null
last_result: stale
---

# Agent Test — Thesis Eval — Primary Secondary Implications

## Lead

Thesis-eval panel task per [[policy-thesis-eval]] (§28.5). The panel compares an unaided baseline (model answers without vault context) against vault-augmented runs (model answers with retrieved context); the headline metric is variance reduction.

## Question

List three pedagogical implications of the primary/secondary biological knowledge distinction.

## Expected answer shape

Three defensible practices (e.g., scaffold secondary material more than primary; expect productive struggle for secondary; use guided rather than discovery instruction for novices; leverage primary capacities like social interaction as a vehicle for secondary content); cites [[biologically-primary-and-secondary-knowledge]] and [[david-geary]].

## Baselines

- **Unaided:** TBD — to be recorded once during seed by running a baseline model N times against this question with no vault context. Variance over N runs is the reference variance.
- **Vault-augmented:** TBD — to be re-run periodically (per [[policy-assessment]] cadence). Per-run variance is compared to the unaided baseline; reduction is logged in the thesis-eval dashboard.

## Notes

This task is `authoritative: true`. Amendments to the panel itself require meta-rule quorum (§9.4). Per-task amendments may be made via the same rule.
