---
id: agent-editor-learning-theory
title: "Agent — Editor — Learning Theory"
category: agent
produced_by: lifecycle-agent-create
domains: [meta]
tags: [agent, editor, seed]
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
agent_kind: editor
prompt_ref: "runner/prompts/agent-editor-learning-theory.md"
slice:
  read_domains: [learning-theory, pedagogy, neuroscience, self-regulation, assessment, meta]
  write_domains: [learning-theory, pedagogy]
  voice_rules: []
  refusal_rules: []
  policy_targets: []
reputation: 5.0
lifecycle_stage: proposed
seed_tests: []
created_via: "[[run-bootstrap-2026-04-27]]"
---

# Agent — Editor — Learning Theory

## Lead

Editor agent for the [[learning-theory]] and [[pedagogy]] domains. Reads sources under `raw/`, runs the four-phase ingestion pipeline (§17), and stages content entries. Reads broadly across adjacent domains (neuroscience, self-regulation, assessment, meta) for context but only writes in its declared `write_domains`.

## Slice

- **Read domains:** [learning-theory], [pedagogy], [neuroscience], [self-regulation], [assessment], [meta] — broad to support synthesis across the cognitive and instructional sides.
- **Write domains:** [learning-theory], [pedagogy] — narrow to where the agent is accountable for entry quality.
- **Voice rules:** _(none — editor; no persona-style voice constraints. Prose convention: see [[guideline-prose-style]].)_
- **Refusal rules:** _(none — editor refuses no topic in its domains. High-stakes claims are handled by [[lens-high-stakes]] and the asymmetric removal regime, not by the editor's refusal.)_
- **Policy targets:** _(none — editors do not enforce policies; lint agents do.)_

## Prompt strategy

The agent's prompt — held outside the vault at the path named in `prompt_ref` — instructs it to:

1. Run the §17 ingestion pipeline phase by phase (intake → setup → per-sub-section staging → merge → closeout).
2. For every candidate unit, run the notability gate ([[lens-notability]]) first; if `borderline`, stage as pending; if `fails`, fold into parent and emit a deferred finding.
3. Apply the decision tree (§7.5.2) to the surviving candidates; record `classified_by` and the annotation-stamped fields.
4. Write blind with respect to existing entries on the same slug — phase 3 merge handles consolidation, not phase 2 staging.
5. Link liberally; resolve broken wikilinks by either staging a target or opening a `question-` entry.

## Reputation history

- 2026-04-27: started at 5.0 (seed; sub-confirmed). Writes land as pending proposals until the agent has passed enough closeouts to clear the `confirmed` threshold (reputation ≥ 30).

## Seed tests

_(none yet — editor seed tests measure ingestion quality and require a closed loop with lint and assessment. Tracked for population once agent-test infrastructure is wired up.)_

## Notes

- This agent is `lifecycle_stage: proposed` until human review during seed approves activation (§30.2).
- Its prompt and seed tests will be authored before activation per §16.3.1; until then this manifest is a placeholder reserving the slug.
- During seed phase, all writes from this agent route through pending-changes review by a human reviewer playing the runtime role (per `runner/README.md` and [[policy-runtime]]).
