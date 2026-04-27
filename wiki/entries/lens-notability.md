---
id: lens-notability
title: "Lens — Notability"
category: lens
classified_by: lens-lens
domains: [meta]
tags: [annotation, gating, deferred-units]
sources: []
aliases: []
created: 2026-04-27
updated: 2026-04-27
confidence: high
status: complete
notability_status: n/a
edit_hardness: restricted
high_stakes_class: none
quality: c
produced_by: lifecycle-bootstrap
lens_question: "Does this candidate unit deserve its own entry?"
lens_priority: 200
lens_covers_category: notability_status
lens_kind: annotation
lens_criteria:
  - "Stamps `notability_status` ∈ {passes, borderline, fails, n/a}."
  - "Runs FIRST during classification (§7.5 step 1), before the decision-tree pass."
  - "`passes` requires at least one of: multi-source coverage, routing necessity (≥N inbound, v0: N=2), or explicit policy carve-out (§8.1)."
  - "`borderline` is held in `temp/pending-` and migrated to `raw/{source}/pending/` at closeout."
  - "`fails` units are folded into the parent entry's body and a `finding-deferred-` is emitted."
  - "Infrastructure entries are stamped `n/a` (their notability is by virtue of their kind)."
---

# Lens — Notability

## Question

Does this candidate unit deserve its own entry, or should its content live inside another entry's body?

## How to apply

Run **first** during classification, before the decision-tree pass (§7.5 step 1). The output gates whether the unit proceeds to a category at all.

The predicate (§8.1):

1. **Multi-source coverage.** Covered by at least 2 independent sources (translations, abridgements, reprints are not independent).
2. **Routing necessity.** Referenced by at least N other entries (v0: N=2) that would otherwise need anchor links into a parent.
3. **Explicit policy carve-out.** The unit is in a class declared notable by `policy-notability` — every `source`, `domain`, `lens`, `policy`, `guideline`, `essay`, `agent`, `agent-test`, `discussion`; and any concept naming a foundational framework cited in primary literature.

Stamp values:

- **`passes`** — at least one predicate holds.
- **`borderline`** — none holds at the moment, but the unit is referenced once or is plausibly notable on its content. Staged as `pending-` and revisited at later closeouts.
- **`fails`** — clearly fails all predicates: a passing mention, a one-source aside.
- **`n/a`** — infrastructure entries (lens, policy, agent, run, finding, …) are notable by their kind; the predicate does not apply.

`fails` units are folded into the parent entry's body in phase 1 (§17.4.2 step 3), and a `finding-deferred-{parent}-{topic}` is emitted with `severity: advisory` so a future ingestion can promote the topic if more material arrives.

## Promotion and retirement

A `borderline` unit promotes to `passes` when (§8.3.2):

- a later sub-section produces a wikilink to its slug, **or**
- a later ingestion adds a second independent source.

It retires when (§8.3.3):

- the source completes without the unit ever being referenced, **or**
- the unit has been pending for 90 days, **or**
- a later finding declares it a duplicate of an existing entry.

## Worked stampings

- A concept like the existing [[desirable-difficulty]] cited in two textbooks → `passes`.
- A passing mention of an obscure procedure named once in one chapter → `fails` (folded into parent).
- A new term referenced once but plausibly notable on its content (e.g., a future "fluency-illusion" entry referenced from one chapter) → `borderline` (staged as pending; revisited).
- Any `lens-`, `policy-`, `domain-` entry → `n/a`.

## Notes

Special cases per §8.5: claims always pass through this lens differently — the gate decides whether the claim deserves its own `claim-` entry vs. living inline. Relations are notable iff they connect two notable entries with a load-bearing predicate. Questions and disambiguations are always notable.

## Related lenses

- Meta-lens: [[lens-lens]]
- Runs before all decision-tree lenses.
- Sibling annotation lenses: [[lens-evidence-grade]], [[lens-high-stakes]], [[lens-confidence]], [[lens-recency]], [[lens-edit-hardness]]
