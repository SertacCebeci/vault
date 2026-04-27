---
id: agent-test-thesis-eval-difficulty-testing
title: "Agent Test — Thesis Eval — Difficulty Testing"
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
question: "What is the relationship between desirable difficulty and the testing effect?"
expected_shape: "Cites both ([[desirable-difficulty]], [[testing-effect]]); names the connection (the testing effect is one mechanism by which desirable difficulty produces stronger learning — effortful retrieval is…"
authoritative: true
last_run: null
last_result: stale
---

# Agent Test — Thesis Eval — Difficulty Testing

## Lead

Thesis-eval panel task per [[policy-thesis-eval]] (§28.5). The panel compares an unaided baseline (model answers without vault context) against vault-augmented runs (model answers with retrieved context); the headline metric is variance reduction.

## Question

What is the relationship between desirable difficulty and the testing effect?

## Expected answer shape

Cites both ([[desirable-difficulty]], [[testing-effect]]); names the connection (the testing effect is one mechanism by which desirable difficulty produces stronger learning — effortful retrieval is itself a desirable difficulty; the testing effect's strength scales with retrieval effort, consistent with the desirable-difficulty framework).

## Baselines

- **Unaided:** TBD — to be recorded once during seed by running a baseline model N times against this question with no vault context. Variance over N runs is the reference variance.
- **Vault-augmented:** TBD — to be re-run periodically (per [[policy-assessment]] cadence). Per-run variance is compared to the unaided baseline; reduction is logged in the thesis-eval dashboard.

## Notes

This task is `authoritative: true`. Amendments to the panel itself require meta-rule quorum (§9.4). Per-task amendments may be made via the same rule.
