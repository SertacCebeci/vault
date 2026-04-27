---
id: agent-lint-frontmatter
title: "Agent — Lint — Frontmatter"
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
prompt_ref: "scripts/wiki_lint.py"
slice:
  read_domains: [meta, learning-theory, neuroscience, pedagogy, self-regulation, assessment]
  write_domains: []
  voice_rules: []
  refusal_rules: []
  policy_targets:
    - "[[policy-classification]]"
    - "[[policy-entry-layout]]"
    - "[[policy-lint]]"
reputation: 10.0
lifecycle_stage: proposed
seed_tests: []
created_via: "[[run-bootstrap-2026-04-27]]"
---

# Agent — Lint — Frontmatter

## Lead

Lint agent enforcing frontmatter schema correctness across every entry. Targets [[policy-classification]] and [[policy-entry-layout]]; raises blocking findings for schema violations and advisory findings for soft-tier issues.

## Slice

- **Read domains:** all (frontmatter rules apply vault-wide).
- **Write domains:** _(none — lint agents only produce findings and notifications.)_
- **Policy targets:** [[policy-classification]], [[policy-entry-layout]], [[policy-lint]].

## Rules enforced (subset of §20.2)

| rule | severity | implemented |
|---|---|---|
| `id-filename-mismatch` | blocking | `scripts/wiki_lint.py` |
| `unknown-category` | blocking | `scripts/wiki_lint.py` |
| `classification-consistency` | blocking | `scripts/wiki_lint.py` |
| `infrastructure-classified-by-lens` | blocking | `scripts/wiki_lint.py` |
| `lens-self-classification` | blocking | `scripts/wiki_lint.py` |
| `unknown-domain` | blocking | `scripts/wiki_lint.py` |
| `entry-without-domain` | blocking | `scripts/wiki_lint.py` |
| `tag-shadowing-domain` | advisory | `scripts/wiki_lint.py` |
| `reserved-prefix-misuse` | blocking | `scripts/wiki_lint.py` |
| `notability-stamp-missing` | blocking | `scripts/wiki_lint.py` |
| `lead-missing` | blocking/advisory | `scripts/wiki_lint.py` |
| `slug-uniqueness` | blocking | `scripts/wiki_lint.py` |
| `frontmatter-yaml-invalid` | blocking | _v0 partial_ |
| `missing-required-list` | blocking | _v0 partial_ |
| `category-fields-presence` | blocking | _not yet_ |
| `edit-hardness-consistency` | blocking | _not yet_ |
| `body-section-order` | advisory | _not yet_ |
| `low-quality-lead` | advisory | _not yet (needs a quality grader)_ |

## Prompt strategy

This lint agent is mechanical, not LLM-based. Its `prompt_ref` points at the Python script that implements its rules. As rules become non-mechanical (e.g., `low-quality-lead` requires judgement on whether a lead actually compresses the body), they may be split off into a separate LLM-based lint agent.

## Reputation history

- 2026-04-27: started at 10.0 (seed; mechanical lint agents start above editors so their findings are not pending-routed).

## Seed tests

_(none yet — lint regression tests measure whether the rule output stays stable on a fixed corpus and require a mature lint suite to anchor.)_

## Notes

- Findings are not yet emitted as `finding-*` entries; the v0 lint script reports to stdout (per `scripts/wiki_lint.py`'s `--report` mode). When the runtime can manage finding lifecycle, a `--emit-findings` mode will produce real entries.
- This agent's reputation does not change until findings are first-class entries.
