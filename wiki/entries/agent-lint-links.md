---
id: agent-lint-links
title: "Agent — Lint — Links"
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
    - "[[policy-lint]]"
reputation: 10.0
lifecycle_stage: proposed
seed_tests: []
created_via: "[[run-bootstrap-2026-04-27]]"
---

# Agent — Lint — Links

## Lead

Lint agent enforcing link-graph rules: every wikilink resolves; entries carry sufficient outbound link density; structure notes have enough inbound coverage; orphan entries are surfaced.

## Slice

- **Read domains:** all (link rules apply vault-wide).
- **Write domains:** _(none.)_
- **Policy targets:** [[policy-classification]], [[policy-lint]].

## Rules enforced (subset of §20.2)

| rule | severity | implemented |
|---|---|---|
| `broken-wikilink` | blocking | `scripts/wiki_lint.py` |
| `low-link-density` | advisory | `scripts/wiki_lint.py` |
| `orphan-entry` | advisory | `scripts/wiki_lint.py` |
| `structure-note-low-link-density` | blocking | _v0 partial via low-link-density_ |
| `structure-note-coverage` | advisory | _not yet (cluster detection needed)_ |
| `relation-not-formalized` | advisory | _not yet_ |
| `disambiguation-orphan` | advisory | _not yet_ |
| `disambiguation-no-hatnote` | advisory | _not yet_ |
| `lens-version-drift` | advisory | _not yet (lens versioning not wired)_ |

## Prompt strategy

Mechanical, like [[agent-lint-frontmatter]]. Cluster detection (for `structure-note-coverage`) requires a connected-component analysis on the wikilink graph; planned for a follow-up extension of the lint script.

## Reputation history

- 2026-04-27: started at 10.0 (seed).

## Seed tests

_(none yet.)_

## Notes

- The legacy vault has 16 known broken wikilinks (mostly case-sensitivity bugs in older entries); they are tracked as Phase 5 cleanup work and not yet emitted as `finding-broken-wikilink-*` entries.
