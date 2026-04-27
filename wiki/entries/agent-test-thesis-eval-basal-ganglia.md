---
id: agent-test-thesis-eval-basal-ganglia
title: "Agent Test — Thesis Eval — Basal Ganglia"
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
question: "Describe the role of the basal ganglia in skill acquisition."
expected_shape: "Names basal-ganglia involvement in procedural learning (action selection, stimulus-response associations, habit formation, reinforcement-based selection of motor programs); distinguishes from…"
authoritative: true
last_run: null
last_result: stale
---

# Agent Test — Thesis Eval — Basal Ganglia

## Lead

Thesis-eval panel task per [[policy-thesis-eval]] (§28.5). The panel compares an unaided baseline (model answers without vault context) against vault-augmented runs (model answers with retrieved context); the headline metric is variance reduction.

## Question

Describe the role of the basal ganglia in skill acquisition.

## Expected answer shape

Names basal-ganglia involvement in procedural learning (action selection, stimulus-response associations, habit formation, reinforcement-based selection of motor programs); distinguishes from declarative-system roles; cites primary literature; if the vault lacks the explicit entry, names the gap.

## Baselines

- **Unaided:** TBD — to be recorded once during seed by running a baseline model N times against this question with no vault context. Variance over N runs is the reference variance.
- **Vault-augmented:** TBD — to be re-run periodically (per [[policy-assessment]] cadence). Per-run variance is compared to the unaided baseline; reduction is logged in the thesis-eval dashboard.

## Notes

This task is `authoritative: true`. Amendments to the panel itself require meta-rule quorum (§9.4). Per-task amendments may be made via the same rule.
