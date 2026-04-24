---
id: lens-insight
title: "Lens — Insight"
category: lens
classified_by: lens-lens
domains: [meta]
tags: [classification, synthesis]
sources: []
aliases: []
created: 2026-04-21
updated: 2026-04-21
confidence: high
status: complete
lens_question: "Does stating this require naming 2+ existing concepts and observing their relationship?"
lens_priority: 60
lens_covers_category: insight
lens_criteria:
  - "Stating the entry requires naming 2+ existing concepts."
  - "It is an observation *about* the relationships between, implications of, or results achieved by those concepts — not a mechanism in its own right."
  - "It is the wiki's own synthesis, not a source's thesis restated."
  - "Frontmatter declares `connects: [concept-slug, …]` listing the concepts being tied together."
---

# Lens — Insight

## Question

Does stating this require naming 2+ existing concepts, and is it an observation about their relationship (not a mechanism in its own right)?

## How to apply

An insight is the wiki talking back to itself. After enough concepts accrue, structural observations become visible — "X and Y together produce Z", "A is the keystone that ties B, C, D together", "the real lever is not P but Q". These are insights.

Exclusion tests (all must fail for a match):

- A concept with many connections is still a concept. Link density alone doesn't promote a note.
- A source's thesis restated is a source entry or part of a source's `## Key ideas`, not an insight.
- An interesting factoid is not an insight.
- A concept that happens to be abstract is still a concept.

The insight entry's body should name the concepts up front, then describe the relationship and its consequences.

## Worked matches

- "Education changes LTM, not WM" — requires naming LTM, WM, expertise-reversal-effect, chunking. A meta-observation about teaching's real target.
- "Practice precedes motivation" — synthesizes schemas, dopamine, procedural-learning into a reversed assumption.
- "Metacognition as the keystone" — structural observation about metacognition's role relative to other concepts.
- "DD is the unifying principle tying spacing, interleaving, and retrieval together" — observation across multiple concepts.

## Worked non-matches

- [[desirable-difficulty]] — a named principle with its own mechanism, even though it has many connections. Route to [[lens-concept]].
- [[transfer]] — one cognitive phenomenon; involves multiple concepts but *is* one describable thing. Route to [[lens-concept]].
- [[make-it-stick]] book-level thesis — belongs in the source entry, not a standalone insight. Route to [[lens-source]].

## Related lenses

- Meta-lens: [[lens-lens]]
- Previous lens in priority: [[lens-process]]
- Next lens in priority: [[lens-concept]]
- Routes away to: [[lens-concept]], [[lens-source]].
