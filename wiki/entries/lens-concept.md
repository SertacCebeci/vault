---
id: lens-concept
title: "Lens — Concept"
category: lens
classified_by: lens-lens
domains: [meta]
tags: [classification, default]
sources: []
aliases: []
created: 2026-04-21
updated: 2026-04-21
confidence: high
status: complete
lens_question: "Is this one idea, explainable on its own terms, without citing a specific source?"
lens_priority: 99
lens_covers_category: concept
lens_criteria:
  - "The entry describes a single mechanism, principle, phenomenon, or cognitive process."
  - "It can be explained without citing 'the book' or 'Chapter N' — prose is source-independent."
  - "It passes no more specific lens (source, illustration, application, entity, process, insight)."
---

# Lens — Concept

## Question

Is this one idea, explainable on its own terms, that does not fit any more specific lens?

## How to apply

This is the **default** lens — priority 99, the catch-all. It fires when every earlier lens has missed. When genuinely unsure between concept and another category, default to concept; it is the most flexible type.

Before concluding concept, run through the earlier lenses and rule each out:

- If the candidate has a protagonist, setting, and outcome → [[lens-illustration]].
- If the candidate prescribes steps a practitioner could follow → [[lens-application]].
- If the candidate is a proper noun → [[lens-entity]].
- If the candidate is a multi-stage sequence with transitions → [[lens-process]].
- If stating the candidate requires naming 2+ concepts and observing their relationship → [[lens-insight]].
- If the candidate is a literature note about a raw source document → [[lens-source]].
- Otherwise this lens matches and the category is `concept`.

Levels of abstraction all match this lens — low-level mechanisms, cognitive phenomena, named principles, learnable skills, even myths and misconceptions (a debunked belief is still a single idea; use `confidence: contested`).

## Worked matches

- [[desirable-difficulty]] — one named principle with its own mechanism. Many connections do not change its type.
- [[chunking]] — one cognitive phenomenon, source-independent.
- [[transfer]] — one skill, a distinct describable capability.
- [[testing-effect]] — one empirical finding.
- [[learning-styles-myth]] — a myth note; explains the belief and why it's wrong. `confidence: contested`.

## Worked non-matches

- "DD is the unifying principle tying spacing, interleaving, and retrieval together" — an observation *about* multiple concepts. Route to [[lens-insight]].
- [[beanbag-toss-study]] — a specific study with protagonists and an outcome. Route to [[lens-illustration]].
- [[leitner-box]] — a practitioner-followable procedure. Route to [[lens-application]].
- [[robert-bjork]] — a proper noun. Route to [[lens-entity]].

## Related lenses

- Meta-lens: [[lens-lens]]
- Previous lens in priority: [[lens-insight]]
- Routes away to: [[lens-illustration]], [[lens-application]], [[lens-entity]], [[lens-process]], [[lens-insight]], [[lens-source]].
