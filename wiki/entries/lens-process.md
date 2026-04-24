---
id: lens-process
title: "Lens — Process"
category: lens
classified_by: lens-lens
domains: [meta]
tags: [classification, sequence]
sources: []
aliases: []
created: 2026-04-21
updated: 2026-04-21
confidence: high
status: complete
lens_question: "Does this describe a multi-stage sequence with transitions between stages, where understanding requires knowing triggers, dependencies, and failure modes?"
lens_priority: 50
lens_covers_category: process
lens_criteria:
  - "The entry describes 2+ stages where each stage depends on or transforms the output of the previous one."
  - "Understanding the whole requires knowing the transitions, not just the parts."
  - "Frontmatter declares `stages` (ordered list of stage slugs)."
  - "Body addresses triggers, dependencies, and failure modes — what moves the system between stages and where it can break."
---

# Lens — Process

## Question

Does this describe a multi-stage sequence with transitions between stages, where understanding requires knowing triggers, dependencies, and failure modes?

## How to apply

A process is about *flow*. Each stage is its own concept (and likely has a concept entry); the process entry is about the pipeline itself — what happens at each handoff, what triggers each transition, what can go wrong and where.

Distinguishing from:

- **Application** — applications tell you what to *do*; processes tell you how something *works* as a sequence. `pomodoro-technique` is an application; `encoding-consolidation-retrieval-pipeline` is a process.
- **Concept** — a concept explains one idea; a process explains the flow between ideas. Both coexist: a process entry links to concept entries for depth on each stage.

The `stages` frontmatter field must be an ordered list; order is load-bearing.

## Worked matches

- Encoding → consolidation → retrieval pipeline — three-stage sequence with triggers, dependencies, failure modes.
- Learn-it-link-it four-phase sequence — four stages with different actors; breaks if reordered.
- Habit loop (cue → routine → reward) — three-stage cycle with triggers between stages.

## Worked non-matches

- [[encoding]] — one stage *of* the pipeline, not the pipeline itself. Route to [[lens-concept]].
- [[leitner-box]] — a practitioner-followable procedure, not a conceptual sequence. Route to [[lens-application]].
- "Education changes LTM, not WM" — an observation about relationships, not a sequence. Route to [[lens-insight]].

## Related lenses

- Meta-lens: [[lens-lens]]
- Previous lens in priority: [[lens-entity]]
- Next lens in priority: [[lens-insight]]
- Routes away to: [[lens-concept]], [[lens-application]], [[lens-insight]].
