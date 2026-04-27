---
id: meta
title: "Meta"
category: domain
produced_by: lifecycle-bootstrap
domains: [meta]
tags: [domain, governance]
sources: []
aliases: ["vault meta", "self-reference"]
created: 2026-04-27
updated: 2026-04-27
confidence: high
status: complete
notability_status: n/a
edit_hardness: restricted
high_stakes_class: none
quality: c
scope: "Entries about the vault itself: lenses that classify, policies that bind, guidelines that advise, essays under development, agents that act, the seed configuration, and the assessment of the vault as a system. Self-referential infrastructure."
out_of_scope: "Subject-matter content (route to [[learning-theory]], [[neuroscience]], [[pedagogy]], [[self-regulation]], or [[assessment]] depending on topic)."
canonical_questions: []
contentious: false
evidence_grade_floor: D
edit_hardness_floor: confirmed
subscribed_agents: []
load_bearing_structure_notes: []
---

# Meta

## Lead

The self-referential domain — every entry that is *about* the vault rather than about the subject matter the vault studies. Lenses classify entries; policies bind agent behavior; guidelines advise; essays propose; agents act; runs record; findings notice; discussions resolve. All of those infrastructure entries live here.

## Scope

This domain holds the vault's own infrastructure:

- All `lens-*` entries — both decision-tree (assigning `category`) and annotation (stamping orthogonal fields).
- All `policy-*`, `guideline-*`, and `essay-*` entries — the three-tier rule system.
- All `domain-*` entries (this one is itself a member).
- All `agent-*` entries — editors, personas, and lint agents.
- All `agent-test-*` entries.
- The bootstrap and ingestion-pipeline-related entries when they exist as their own subjects.

## Out of scope

- Anything about a subject the vault studies — those go in their topical domain. A `concept` entry on metacognition is not `meta`-domain; it is `self-regulation`.
- Source entries — they live in the domain of the source's content, not in `meta`.

## Canonical questions

- Are the lens criteria stable enough that two independent classifiers agree, and how often?
- What's the failure mode that the asymmetric removal regime catches that ordinary lint would miss?
- How does the population's reputation distribution evolve over time, and is the external anchor preventing drift?
- What's the right cadence and structure for amending this domain's load-bearing rules without creating churn?

## Load-bearing structure notes

_(empty at seed; expect a structure note framing the lens system, a structure note framing the policy lattice, and a structure note framing agent lifecycles once the system has been operating for some time)_

## Subscribed editor agents

_(empty at seed; the meta domain edits at `restricted` tier — only quorum or human reviewers act here.)_

## Sourcing standards

- Minimum evidence grade: `D`. Most meta entries cite the spec and intent documents, not external literature. Per §1.3, [`docs/spec/specification.md`](../../docs/spec/specification.md) is the authority during seed; policy entries take precedence as they land.
- Mandatory citation: meta entries should reference the relevant spec section.
- Contentious: `false` at seed. Meta amendments require meta-rule quorum (§9.4) regardless.

## Related domains

- Every other domain — meta is the one that other domains' lint and editor agents interact with structurally.

## Notes

The `edit_hardness_floor` for meta is set to `confirmed` (one tier above `open`) because most meta entries are infrastructural and benefit from a higher review bar. Specific meta entries — lenses, policies — carry their own `restricted` tier per kind defaults (§9.2).
