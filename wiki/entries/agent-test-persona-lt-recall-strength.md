---
id: agent-test-persona-lt-recall-strength
title: "Agent Test — Recall Strength"
category: agent-test
produced_by: lifecycle-agent-test-create
domains: [meta]
tags: [agent-test, persona, seed, authoritative]
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
agent: "[[agent-persona-learning-theory]]"
question: "What does the recall-strength model predict about spaced repetition?"
expected_shape: "References the recall-strength model entry; describes the prediction (the more effortful the retrieval, the more retention strengthens; weak retrievals reinforce weakly; this implies optimal spacing…"
authoritative: true
last_run: null
last_result: stale
---

# Agent Test — Recall Strength

## Lead

Authoritative seed test for [[agent-persona-learning-theory]]. Measures whether the persona can answer the question below in the expected shape using only its declared read slice.

## Question

What does the recall-strength model predict about spaced repetition?

## Expected answer shape

References the recall-strength model entry; describes the prediction (the more effortful the retrieval, the more retention strengthens; weak retrievals reinforce weakly; this implies optimal spacing maximizes effortful-but-successful retrieval); cites [[spaced-repetition]] or names if no entry exists.

## Notes

This test is `authoritative: true` (§24.2.1) — its failure is a blocking finding (§24.4). It is run on every closeout that touches an entry in the persona's slice and on the daily schedule.
