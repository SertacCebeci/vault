---
id: agent-lint-evidence
title: "Agent — Lint — Evidence"
category: agent
produced_by: lifecycle-agent-create
domains: [meta]
tags: [agent, lint, seed]
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
agent_kind: lint
prompt_ref: "runner/prompts/agent-lint-evidence.md"
slice:
  read_domains: [meta, learning-theory, neuroscience, pedagogy, self-regulation, assessment]
  write_domains: []
  voice_rules: []
  refusal_rules: []
  policy_targets:
    - "[[policy-content-quality]]"
    - "[[policy-high-stakes]]"
    - "[[policy-contentious-domain]]"
reputation: 10.0
lifecycle_stage: proposed
seed_tests: []
created_via: "[[run-bootstrap-2026-04-27]]"
---

# Agent — Lint — Evidence

## Lead

Lint agent enforcing evidence-quality and high-stakes rules: claims meet their domain's evidence floor; high-stakes claims clear the asymmetric removal regime; contentious-domain entries cite sources for every claim.

## Slice

- **Read domains:** all (evidence rules apply vault-wide).
- **Write domains:** _(none.)_
- **Policy targets:** [[policy-content-quality]], [[policy-high-stakes]], [[policy-contentious-domain]].

## Rules enforced (subset of §20.2)

| rule | severity | implemented |
|---|---|---|
| `evidence-below-floor` | blocking in contentious / advisory else | _not yet (needs claim entries)_ |
| `source-missing-contentious` | blocking | _not yet_ |
| `high-stakes-floor-violation` | blocking | _not yet_ |
| `source-frontmatter-mismatch` | advisory | _not yet (needs source-section parser)_ |
| `wontfix-without-justification` | blocking | _not yet (needs finding entries)_ |

## Prompt strategy

Unlike [[agent-lint-frontmatter]] and [[agent-lint-links]], evidence-grade and high-stakes lint require **judgement**, not just regex. The agent's prompt — once authored — instructs an LLM to:

1. Identify claims in the entry under review (whether their own `claim-` entry or inline assertions in concept/insight bodies).
2. For each claim, assess whether `evidence_grade` matches the cited sources (the agent does not assign grades; it flags mismatches against the existing stamp).
3. For each claim, assess whether `high_stakes_class` is correctly stamped per [[lens-high-stakes]] criteria.
4. For each contentious-domain entry, verify that every claim has at least one source pointer.

Findings the agent raises are reviewable; the agent's reputation moves with whether findings are sustained vs. wontfix-as-false-positive.

## Reputation history

- 2026-04-27: started at 10.0 (seed).

## Seed tests

_(none yet — evidence-judgement seed tests require a corpus of pre-graded claims to anchor the agent's decisions; tracked for follow-up.)_

## Notes

- This is the most LLM-dependent of the three seed lint agents. It will be activated only after [[lens-high-stakes]] and [[lens-evidence-grade]] have been run on a non-trivial subset of entries (i.e., not until Phase 5+ when claim entries start to exist).
